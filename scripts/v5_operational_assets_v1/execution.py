def operational_preflight_output(suite, source_root, output, tools, inputs):
    """Check source-owned protected roots before even creating the projection."""
    output = no_symlinks(output).absolute()
    require(not output.exists(), 'Operational run output must be absent')
    protected = {Path(source_root).resolve()}
    for path in inputs.values(): protected.add(Path(path).resolve().parent)
    definitions = {'lean': {'path_kind': 'EXECUTABLE'}, **{row['name']: row for row in suite['replay']['tools']}}
    for name, value in tools.items():
        path = Path(value).absolute()
        if name == 'mathlib': protected.add(path.resolve()); continue
        require(name in definitions, 'Unreviewed operational tool input')
        kind = definitions[name]['path_kind']
        root = path if kind == 'DISTRIBUTION_ROOT' else path.parent if kind == 'BIN_DIRECTORY' else path.parent.parent
        protected.add(root.resolve())
        if kind == 'EXECUTABLE': protected.add(path.resolve().parent.parent)
    require(all(output != root and not output.is_relative_to(root) for root in protected),
            'Operational output overlaps protected source, input, tool, or dependency tree')
    return output


def operational_archive_roots(packet, plan, inputs, output, mappings):
    inventories = {}; owner = _OPERATIONAL_DATA['packets'][packet]
    for iid, row in plan['inputs'].items():
        require(row['kind'] == 'FILE', 'Operational recipe admitted only exact archive files')
        archive = path_in(output, 'archives/' + iid)
        inventories[iid] = (archive, extract_source_zip(inputs[iid], archive))
        if iid == 'source-archive': prefix = owner['root']
        elif iid == 'batch-science-archive': prefix = str(PurePosixPath(_OPERATIONAL_DATA['popen'][packet]['source_driver']['member_chain'][-1]).parent)
        else:
            helpers = [_OPERATIONAL_DATA['helpers'][hid] for hid in owner['helper_ids'] if _OPERATIONAL_DATA['helpers'][hid]['input_id'] == iid]
            require(len(helpers) == 1, 'Unbound helper archive root')
            prefix = str(PurePosixPath(helpers[0]['member']).parent)
        mappings['archive:' + iid] = archive if prefix in ('', '.') else path_in(archive, prefix)
    source_root = mappings['archive:source-archive']; operational_verify_root(packet, source_root)
    mappings['driver:original'] = source_root / PurePosixPath(owner['driver']['member_chain'][-1]).name
    return inventories


def operational_helper_spec(helper_id):
    owner = _OPERATIONAL_DATA['helpers'][helper_id]; packet = owner['physical_suite']
    if owner['input_id'] == 'source-archive': prefix = _OPERATIONAL_DATA['packets'][packet]['root']
    elif owner['input_id'] == 'batch-science-archive': prefix = str(PurePosixPath(_OPERATIONAL_DATA['popen'][packet]['source_driver']['member_chain'][-1]).parent)
    else: prefix = str(PurePosixPath(owner['member']).parent)
    path = PurePosixPath(owner['member']).relative_to(prefix).as_posix() if prefix not in ('', '.') else owner['member']
    root = '{archive:' + owner['input_id'] + '}'
    argv = ['{tool:python}', '-B', root + '/' + path]
    if owner['kind'] == 'unittest': argv.append('-v')
    elif owner['kind'] == 'json-checks': argv += ['--checkpoint', '{archive:source-archive}', '--output', '{out}/wrapper-checks/common-boundary.json']
    else: argv += ['--output', '{out}/wrapper-checks/controller-environment']
    return {'stage_id': helper_id, 'argv': argv, 'cwd': root, 'source_binding': {'kind': 'ARCHIVE_MEMBER',
        'archive_source_id': owner['archive_source_id'], 'archive_sha256': owner['archive_sha256'],
        'member': owner['member'], 'source_sha256': owner['source']['sha256']}}


def operational_validate_helpers(rows, packet, stages, evidence, successful):
    helpers = indexed(rows, 'stage_id'); expected = _OPERATIONAL_DATA['packets'][packet]['helper_ids']
    require(list(helpers) == expected, 'Missing or reordered mandatory operational helper evidence')
    for hid, row in helpers.items():
        keys(row, {'stage_id', 'argv', 'cwd', 'source_binding', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'output_hashes'})
        spec = operational_helper_spec(hid)
        require(all(row[k] == spec[k] for k in spec), 'Changed operational helper source/argv/cwd')
        require(all(row[k] == stages[hid][k] for k in ('started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'output_hashes')),
                'Helper invocation differs from actual helper stage')
        require(row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and row['exit_code'] == 0 and
                row['ended_at'] <= stages['original-driver']['started_at'], 'Original driver preceded mandatory helper completion')
        for name, digest_value in row['output_hashes'].items():
            require(evidence['output_hashes'].get(name) == digest_value, 'Helper output lacks actual evidence binding')


def operational_execute_suite(suite, sources, root, output, tools, inputs, scope=None, *, reviews=None):
    require(scope is None or scope == suite['replay']['scope'], 'Execute only the exact admitted operational scope')
    require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'Missing source-bound review identities')
    plan = validate_suite(suite, sources, root); packet = plan['operational_packet']
    operational_preflight_output(suite, root, output, tools, inputs)
    project_suite(suite, sources, root, output)
    output = Path(output).absolute(); project = output / 'project'; logs = output / 'logs'; logs.mkdir()
    receipt = _initial_receipt(suite, sources, reviews); evidence = receipt['replay_evidence']
    results = indexed(evidence['stage_results']); completed = {}; controls = indexed(suite['controls'])
    current = results['_prerequisites']; current['started_at'] = utc()
    captured = {}; child_logs = {}; helper_invocations = []; archives = {}; invocation = None; mappings = {}
    def save():
        receipt['stages'] = [{k: row[k] for k in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in evidence['stage_results']]
        receipt['log_sha256'] = canonical({row['id']: row['log_sha256'] for row in evidence['stage_results']})
        write_json(output / 'RECEIPT.json', receipt)
    save()
    try:
        resolved, fingerprints, dependencies, env, input_hashes = _verify_environment(suite, plan, tools, inputs, output)
        evidence['tool_fingerprints'] = fingerprints; evidence['dependency_checks'] = dependencies
        definitions = {'lean': {'path_kind': 'EXECUTABLE'}, **{row['name']: row for row in suite['replay']['tools']}}
        mappings = {'project': project, 'out': output, 'build': output / 'build', 'adapter': Path(__file__).resolve(),
                    'dependency:mathlib': Path(tools['mathlib']).resolve()}
        mappings.update({'tool:' + name: tool_argument(definitions[name], path) for name, path in resolved.items()})
        mappings.update({'input:' + name: Path(path).resolve() for name, path in inputs.items()})
        archives = operational_archive_roots(packet, plan, inputs, output, mappings)
        log = logs / 'prerequisites.log'; log.write_text('Exact operational tools, dependencies, archive inventory and selected source projection verified.\n')
        current.update(terminal='COMPLETED', exit_code=0, ended_at=utc(), log_sha256=sha(log.read_bytes()))
        for sid, stage in plan['stages'].items():
            current = results[sid]; current['started_at'] = utc(); log = logs / (sid + '.log')
            for dependency in stage['depends_on']:
                require(completed.get(dependency, {}).get('matched') is True, 'Required operational stage is incomplete')
            for name in stage['output_paths']:
                path = path_in(output, name); require(not path.exists(), 'Operational output already exists'); path.parent.mkdir(parents=True, exist_ok=True)
            if sid in plan['operational_helpers']:
                spec = operational_helper_spec(sid); argv = [_expand(arg, mappings) for arg in spec['argv']]
                helper = no_symlinks(argv[2]); require(sha(helper.read_bytes()) == spec['source_binding']['source_sha256'], 'Mandatory original helper changed')
                run = run_process(argv, Path(_expand(spec['cwd'], mappings)), stage_environment(stage, plan, output, env), log, stage['timeout_seconds'])
                current.update(run); text = log.read_text(encoding='utf-8', errors='replace')
                # Failed helper attempts still retain their actual invocation.
                private = output / 'helper-captures'; private.mkdir(exist_ok=True)
                write_json(private / (sid + '.json'), {**spec, **run, 'actual_argv': argv, 'actual_cwd': _expand(spec['cwd'], mappings)})
                assess_stage(stage, run, text, completed)
                operational_check_helper(sid, text, output, mappings)
            elif stage['argv'][:1] == ['{builtin:observe-child}']:
                parent_id, child_id = stage['argv'][1:]; observed = captured[(parent_id, child_id)]
                raw = child_logs[child_id].read_bytes(); require(sha(raw) == observed['log_sha256'], 'Physical child log changed before observation')
                log.write_bytes(raw)
                run = {'terminal': observed['terminal'], 'exit_code': observed['exit_code'], 'started_at': current['started_at'],
                       'ended_at': utc(), 'log_sha256': observed['log_sha256']}
                current.update(run); text = raw.decode('utf-8', errors='replace')
                evidence['child_observations'].append({**observed, 'stage_id': sid, 'observed_at': run['ended_at']})
                assess_stage(stage, run, text, completed)
            else:
                require(stage['kind'] == 'DRIVER' and sid == 'original-driver', 'Unreviewed operational stage dispatch')
                driver = plan['drivers'][stage['driver_id']]; launch = operational_tracer_argv(stage, packet)
                invocation = {'parent_stage_id': sid, 'driver_sha256': driver['sha256'], 'source_argv': stage['argv'],
                    'launch_argv': launch, 'launch_cwd': '{archive:source-archive}', 'runner_sha256': evidence['runner_sha256'],
                    'trace_sha256': None, 'parent_log_sha256': sha(b''), 'child_count': 0, 'physical_children': [],
                    'helper_invocations': copy.deepcopy(helper_invocations), 'original_receipt_sha256': None}
                evidence['driver_invocations'].append(invocation)
                run = run_process([_expand(arg, mappings) for arg in launch], mappings['archive:source-archive'],
                                  stage_environment(stage, plan, output, env), log, stage['timeout_seconds'])
                current.update(run); text = log.read_text(encoding='utf-8', errors='replace')
                invocation['parent_log_sha256'] = run['log_sha256']; trace = output / 'traces' / sid
                if trace.exists():
                    invocation['trace_sha256'] = _file_hashes(trace)
                    invocation['physical_children'], child_logs = operational_collect_ledger(packet, trace, current, mappings, successful=False)
                    invocation['child_count'] = len(invocation['physical_children'])
                if run['terminal'] != 'COMPLETED' or any(row['terminal'] != 'COMPLETED' for row in invocation['physical_children']):
                    receipt.update(outcome='RESOURCE_INCONCLUSIVE', exit_code=1)
                    raise ValueError('Original operational process is resource-inconclusive or incomplete')
                assess_stage(stage, run, text, completed)
                captured, child_logs, objects = operational_collect_original(packet, stage, current, text, plan, output, mappings, invocation)
                evidence['output_hashes'].update(objects)
            current['output_hashes'] = {name: _file_hashes(path_in(output, name)) for name in stage['output_paths']}
            evidence['output_hashes'].update(current['output_hashes'])
            if sid in plan['operational_helpers']:
                helper_invocations.append({**operational_helper_spec(sid), **{k: current[k] for k in ('started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'output_hashes')}})
            completed[sid] = {**run, 'matched': True}
            for cid in stage['control_ids']:
                control = controls[cid]; actual = control['expected_outcome']
                receipt['controls'].append({k: control[k] for k in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
                    'actual_outcome': actual, 'actual_outcome_sha256': sha(actual.encode()), 'terminal': run['terminal'], 'exit_code': run['exit_code'], 'log_sha256': run['log_sha256']})
                evidence['control_diagnostics'].append({'control_id': cid, 'stage_id': sid, 'prerequisite_stage_ids': stage['depends_on'],
                    'expected': stage['expected_diagnostics'], 'observed_log_sha256': run['log_sha256'], 'match': 'MATCHED'})
            save()
        if plan['targets']:
            for name in suite['replay']['module_order']:
                object_name = name.replace('.', '/') + '.olean'
                candidates = [path_in(output, prefix + '/' + object_name) for prefix in suite['replay']['build_roots']]
                require(any(path.is_file() and evidence['output_hashes'].get(path.relative_to(output).as_posix()) == sha(path.read_bytes()) for path in candidates),
                        'Target/import custom object was not freshly generated by this run')
            generated = output / 'generated'; generated.mkdir(); audit = generated / 'V5SuccessorReadback.lean'
            audit.write_text(_audit_source(list(plan['targets'].values())), encoding='utf-8')
            current = results['_target_audit']; log = logs / 'target-audit.log'
            run = run_process([resolved['lean'], '-j1', audit], project, env, log, current['budget_seconds']); current.update(run)
            if run['terminal'] != 'COMPLETED': receipt.update(outcome='RESOURCE_INCONCLUSIVE', exit_code=1)
            require(run['terminal'] == 'COMPLETED' and run['exit_code'] == 0, 'Target proof-closure audit failed')
            audits = parse_readbacks(log.read_text(encoding='utf-8'), list(plan['targets'].values()))
            evidence['target_audits'] = [{'target_id': tid, **value, 'stage_id': '_target_audit', 'log_sha256': run['log_sha256']} for tid, value in audits.items()]
            receipt['axioms'] = sorted({axis for value in audits.values() for axis in value['axioms']})
        if packet in {'t08-common', 't09-transport'}:
            operational_direct_verify_post_dependencies(packet, mappings['archive:source-archive'], resolved['lean'].parent.parent, mappings['dependency:mathlib'])
        for name, path in resolved.items(): require(sha(path.read_bytes()) == fingerprints[name]['executable_sha256'], 'Operational execution tool changed')
        for iid, row in plan['inputs'].items(): require(_input_inventory(row, inputs[iid], plan) == input_hashes[iid], 'Operational external input changed')
        for archive, inventory in archives.values():
            require({p.relative_to(archive).as_posix(): sha(no_symlinks(p).read_bytes()) for p in archive.rglob('*') if p.is_file()} == inventory, 'Extracted operational archive changed')
        for sid, row in plan['files'].items(): require(path_in(project, row['path']).read_bytes() == plan['contents'][sid], 'Operational projected source changed')
        evidence['source_hashes_after'] = {sid: sha(public_bytes(root, sources[sid])) for sid in suite['source_ids']}
        receipt['target_readbacks'] = [{k: target[k] for k in ('source_id', 'target_sha256')} | {'target_id': target['id'], 'outcome': 'CHECKED'} for target in suite['targets']]
        selected = suite['replay']['scope']
        receipt.update(outcome={'FINITE': 'FINITE_ONLY', 'COMPONENTS': 'FRESH_KERNEL_COMPONENTS', 'DECLARED_SUITE': 'QUALIFIED_DECLARED_SUITE'}[selected], exit_code=0, proof_scope=selected)
    except (FileNotFoundError, ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        write_json(output / 'FAILURE.json', {'stage_id': current['id'], 'observed_at': utc(), 'error': type(error).__name__ + ': ' + str(error)})
        if isinstance(error, MissingInput): receipt.update(outcome='BLOCKED_EXTERNAL_INPUT', exit_code=2)
        elif isinstance(error, MissingTool): receipt.update(outcome='BLOCKED_TOOLCHAIN', exit_code=2)
        elif receipt['outcome'] != 'RESOURCE_INCONCLUSIVE': receipt.update(outcome='FAILED', exit_code=1)
        receipt['proof_scope'] = 'NONE'
        if current['terminal'] == 'SKIPPED':
            private_log = logs / (current['id'] + '-failure.log'); private_log.write_text(type(error).__name__ + ': ' + str(error) + '\n')
            current.update(terminal='MISSING' if isinstance(error, FileNotFoundError) else 'COMPLETED',
                exit_code=None if isinstance(error, FileNotFoundError) else 1, ended_at=utc(), log_sha256=sha(private_log.read_bytes()))
        if invocation is not None and invocation['parent_stage_id'] == current['id']:
            invocation['parent_log_sha256'] = current['log_sha256']
    receipt['ended_at'] = utc(); save()
    validate_receipt(receipt, suite, sources, root)
    return receipt
