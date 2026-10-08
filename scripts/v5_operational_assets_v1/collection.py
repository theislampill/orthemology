def operational_output_file(root, name):
    path = path_in(root, name)
    require(path.is_file(), 'Missing exact operational source/output file')
    return path


def operational_output_read_json(root, name):
    return read_json(operational_output_file(root, name))


def operational_output_log(root, name):
    raw = operational_output_file(root, name).read_bytes()
    return raw.decode('utf-8'), sha(raw)


def operational_validate_physical_row(packet, row, parent, successful):
    keys(row, {'physical_id', 'source_binding', 'source_argv', 'argv', 'cwd', 'started_at', 'ended_at',
        'terminal', 'exit_code', 'log_sha256', 'output_hashes', 'capture_sha256', 'log_assembly', 'parent_process_id'})
    specifications = {spec['id']: spec for spec in operational_physical_specs(packet)}
    require(row['physical_id'] in specifications, 'Foreign operational physical child')
    spec = specifications[row['physical_id']]
    operational_validate_source_binding(packet, row['physical_id'], row['source_binding'])
    require(all(row[k] == spec[k] for k in ('source_argv', 'argv', 'cwd', 'log_assembly', 'parent_process_id')),
            'Changed physical child command, cwd, stream, or parent binding')
    digest(row['capture_sha256'])
    require(isinstance(row['started_at'], str) and row['started_at'].endswith('Z') and
            parent['started_at'] <= row['started_at'] <= parent['ended_at'], 'Child start was not measured inside actual parent')
    if row['ended_at'] is not None:
        require(isinstance(row['ended_at'], str) and row['ended_at'].endswith('Z') and
                row['started_at'] <= row['ended_at'] <= parent['ended_at'], 'Child interval was not measured inside actual parent')
    if row['log_sha256'] is not None: digest(row['log_sha256'])
    require(row['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED', 'RUNNING', 'TIMEOUT_WAITING_FOR_ORIGINAL_REAP'}, 'Unknown physical child terminal')
    if row['terminal'] == 'COMPLETED':
        require(type(row['exit_code']) is int and 0 <= row['exit_code'] < 124 and row['ended_at'] is not None and row['log_sha256'] is not None,
                'Completed child has no actual terminal/log')
    else:
        require(row['exit_code'] is None or type(row['exit_code']) is int and row['exit_code'] < 0, 'Noncompleted child gained terminal credit')
    expected_outputs = {name.removeprefix('{out}/') for name in spec['output_paths']}
    require(isinstance(row['output_hashes'], dict) and set(row['output_hashes']) <= expected_outputs, 'Foreign or unexpected physical output')
    for value in row['output_hashes'].values(): digest(value)
    if successful:
        require(parent['terminal'] == 'COMPLETED' and type(parent['exit_code']) is int and parent['exit_code'] == 0,
                'Failed original parent cannot qualify children')
        require(row['terminal'] == 'COMPLETED' and row['exit_code'] == spec['expected_exit'] and set(row['output_hashes']) == expected_outputs,
                'Missing or incomplete expected physical child terminal/output')


def operational_collect_ledger(packet, trace, parent, mappings, *, successful):
    """Collect actual first-run captures. Missing rows are never synthesized."""
    rows = []; paths = {}; expected_files = set()
    specs = operational_physical_specs(packet)
    for spec in specs:
        stem = path_in(trace, spec['capture']); record_path = stem.with_suffix('.json')
        if not record_path.exists():
            require(not successful, 'Missing actual source-owned child capture')
            continue
        raw_record = record_path.read_bytes(); captured = read_json(record_path)
        expanded = operational_expand_value(spec, mappings)
        require(captured['argv'] == expanded['argv'] and captured['cwd'] == expanded['cwd'], 'Captured actual child argv/cwd differs from original source')
        if spec['capture_kind'] == 'POPEN':
            require(captured['source_child_id'] == spec['id'] and captured['source_argv'] == expanded['source_argv'] and
                    captured['argv_translation'] is (expanded['argv'] != expanded['source_argv']), 'Nested/Popen source invocation changed')
        if spec['capture_kind'] == 'METADATA':
            stdout = stem.with_suffix('.stdout'); stderr = stem.with_suffix('.stderr')
            raw = stdout.read_bytes() + stderr.read_bytes() if stdout.exists() and stderr.exists() else None
            if raw is not None:
                require(sha(stdout.read_bytes()) == captured['stdout_sha256'] and sha(stderr.read_bytes()) == captured['stderr_sha256'], 'Metadata capture streams changed')
            log_sha = sha(raw) if raw is not None else None
            expected_files.update({spec['capture'] + '.stdout', spec['capture'] + '.stderr'})
        else:
            log = stem.with_suffix('.log'); raw = log.read_bytes() if log.exists() else None
            log_sha = sha(raw) if raw is not None else None
            require(log_sha == captured['log_sha256'], 'Captured physical log changed')
            paths[spec['id']] = log
            expected_files.add(spec['capture'] + '.log')
        expected_files.add(spec['capture'] + '.json')
        outputs = {}
        for name, value in captured.get('output_hashes', {}).items():
            p = no_symlinks(name)
            require(p.is_relative_to(mappings['out']), 'Captured output escapes fresh run')
            require(p.is_file() and sha(p.read_bytes()) == value, 'Physical object changed after producer exit')
            outputs[p.relative_to(mappings['out']).as_posix()] = value
        row = {'physical_id': spec['id'], 'source_binding': spec['source_binding'], 'source_argv': spec['source_argv'],
            'argv': spec['argv'], 'cwd': spec['cwd'], 'started_at': captured['started_at'], 'ended_at': captured['ended_at'],
            'terminal': captured['terminal'], 'exit_code': captured['exit_code'], 'log_sha256': log_sha, 'output_hashes': outputs,
            'capture_sha256': sha(raw_record), 'log_assembly': spec['log_assembly'], 'parent_process_id': spec['parent_process_id']}
        operational_validate_physical_row(packet, row, parent, successful)
        rows.append(row)
    actual_files = {p.relative_to(trace).as_posix() for p in trace.rglob('*') if p.is_file()}
    require(actual_files <= expected_files, 'Foreign physical trace file')
    if successful: require(actual_files == expected_files and len(rows) == len(specs), 'Incomplete actual physical capture census')
    return rows, paths


def operational_collect_original(packet, stage, parent, text, plan, output, mappings, invocation):
    trace = path_in(output, 'traces/' + stage['id']); original = output / 'original'; root = mappings['archive:source-archive']
    ledger, logs = operational_collect_ledger(packet, trace, parent, mappings, successful=True)
    if packet in _OPERATIONAL_DATA['direct']:
        result = operational_direct_collect_original(packet, root, original, trace / 'calls', parent, text, mappings['tool:lean'], root)
        normalized_rows = {row['source_child_id']: row for row in result['children']}
        receipt_sha = result['original_receipt_sha256']
        record_hashes = {key: row['original_record_sha256'] for key, row in normalized_rows.items()}
    else:
        source_roots = {owner['driver']['parent_archive_sha256']: mappings['archive:source-archive'].parent if owner['root'] else mappings['archive:source-archive']
                        for name, owner in _OPERATIONAL_DATA['packets'].items() if name == packet}
        if packet == 't08-batch':
            source_roots[_OPERATIONAL_DATA['popen'][packet]['source_driver']['parent_archive_sha256']] = original / 'extracted source'
        result = operational_output_normalize(packet, source_roots, original, parent, None, raw_logs=logs if packet == 't09-controller' else None)
        contract = _OPERATIONAL_DATA['packets'][packet]['original_contract']; record_hashes = {}
        for spec in contract['stages']:
            receipt = read_json(original / spec['receipt'])
            row = next(r for r in receipt[spec['receipt_table']] if r[spec['receipt_stage_key']] == spec['receipt_stage_name'])
            record_hashes[spec['id']] = canonical(row)
            if packet == 't09-controller':
                raw = logs[spec['id']].read_text(encoding='utf-8')
                require(raw.replace(str(root) + os.sep, '').encode() == (original / spec['log_path']).read_bytes(), 'T09 original path-only log projection changed')
            else:
                captured = next(r for r in ledger if r['physical_id'] == spec['id'])
                require(logs[spec['id']].read_bytes() == (original / spec['log_path']).read_bytes(), 'Nested/reviewer original log differs from actual captured child')
                require(row['command'] == operational_expand_value(captured['source_argv'], mappings) and
                        row['compiler_cwd'] == operational_expand_value(captured['cwd'], mappings), 'Nested/reviewer original command or cwd differs')
        original_receipt = read_json(original / contract['receipt'])
        receipt_sha = result['original_receipt_sha256']
        if packet == 't08-batch':
            require(json.loads(text) == {k: original_receipt[k] for k in ['status', 'source_zip_sha256', 'source_named_declarations', 'reviewer_named_declarations']},
                    'Original batch terminal stdout changed')
            p = operational_expand_value(_OPERATIONAL_DATA['execution_plans'][packet]['plan'], mappings)
            operational_verify_tree(Path(p['nested_source_root']), _OPERATIONAL_DATA['popen'][packet]['source_input_files'])
            for child in p['science_children'] + p['review_children']:
                if child['binding_kind'] == 'GENERATED_BY_ORIGINAL':
                    body = no_symlinks(child['actual_source_path']).read_bytes()
                    require(body == child['generated_text'].encode() and sha(body) == child['generated_source_sha256'], 'Original generated audit changed after compilation')
                    source_receipt = read_json(original / child['receipt'])
                    source_row = next(r for r in source_receipt[child['receipt_table']] if r[child['receipt_stage_key']] == child['receipt_stage_name'])
                    require(source_row['source_sha256'] == child['generated_source_sha256'], 'Original generated audit receipt source binding changed')
            nested_log = logs['source-component'].read_bytes()
            require(nested_log == (original / 'logs/source-component.log').read_bytes(), 'Nested parent capture differs from original log')
            nested_receipt = read_json(original / 'fresh science/RECEIPT.json')
            require(json.loads(nested_log) == {k: nested_receipt[k] for k in ['status', 'scientific_manifest_sha256', 'custom_source_modules', 'named_declarations_audited', 'author_theorems_audited']},
                    'Nested original terminal stdout differs')
            require(nested_receipt['native_source_bytes'] == 3013 and nested_receipt['native_source_sha256'] == 'e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359' and
                    nested_receipt['compiler_sha256'] == LEAN_SHA and nested_receipt['prior_custom_objects_reused'] == 0, 'Nested native fixture/tool/freshness boundary differs')
            version = next(row for row in ledger if row['physical_id'] == 'compiler_version')
            require(nested_receipt['stages'][0]['log_sha256'] == version['log_sha256'] and logs['compiler_version'].read_bytes() == (original / 'fresh science/logs/version.log').read_bytes(), 'Nested version probe log differs')
        else:
            expected = [('PASS_EXPECTED_FAILURE' if s['expected_exit'] else 'PASS') + ': ' + s['id'] for s in contract['stages']]
            require(text.splitlines() == expected + [contract['terminal_status']], 'Original T09 terminal stdout changed')
            require(logs['compiler_version'].read_text().strip() == original_receipt['lean_version'], 'T09 version probe log differs')
            require(original_receipt['package_manifest_sha256'] == sha((root / 'MANIFEST.json').read_bytes()), 'T09 source manifest receipt binding differs')
            groups = read_json(root / 'ORIGINAL_TO_PUBLIC.json')['milestones']
            coverage = [{'milestone': group['accepted_milestone'], 'entries': len(group['entries'])} for group in groups]
            require(original_receipt['original_manifest_coverage'] == coverage, 'T09 original/public coverage receipt differs')
            for filename, field, table, census in [('LEAN_DISTRIBUTION_PIN.json', 'lean_pin', 'entries', 'lean_census'),
                    ('MATHLIB_SOURCE_PIN.json', 'mathlib_source_pin', 'files', None), ('MATHLIB_CACHE_PIN.json', 'mathlib_cache_pin', 'entries', 'mathlib_cache_census')]:
                entries = read_json(root / 'dependencies' / filename)[table]
                pin_result = original_receipt[field]
                keys(pin_result, {'files_verified', 'accepted_metadata_exceptions'})
                require(type(pin_result['files_verified']) is int and pin_result['files_verified'] == sum(row.get('kind', 'file') == 'file' for row in entries), 'T09 dependency file count changed')
                allowed = {row['path'] for row in read_json(root / 'dependencies/METADATA_EXCEPTIONS.json')['files']} if field == 'mathlib_cache_pin' else set()
                require(isinstance(pin_result['accepted_metadata_exceptions'], list) and len(pin_result['accepted_metadata_exceptions']) == len(set(pin_result['accepted_metadata_exceptions'])) and
                        set(pin_result['accepted_metadata_exceptions']) <= allowed, 'T09 dependency metadata exception contract differs')
                if census is not None: require(type(original_receipt[census]) is int and original_receipt[census] == len(entries), 'T09 dependency census changed')
        for probe in [r for r in ledger if r['source_binding']['kind'] == 'TOOL_PROBE']:
            raw = logs[probe['physical_id']].read_text()
            require('4.19.0' in raw and '6caaee842e94' in raw, 'Original compiler probe identity differs')
    invocation['physical_children'] = ledger
    invocation['child_count'] = len(ledger)
    invocation['original_receipt_sha256'] = receipt_sha
    invocation['trace_sha256'] = _file_hashes(trace)
    children = {}; objects = {}
    for row in ledger:
        objects.update(row['output_hashes'])
        if row['physical_id'] not in {spec['id'] for spec in operational_physical_specs(packet) if spec['observer']}:
            continue
        child = row['physical_id']
        children[(stage['id'], child)] = {
            'source_child_id': child, 'parent_stage_id': stage['id'], 'driver_sha256': plan['drivers'][stage['driver_id']]['sha256'],
            'parser_id': _OPERATIONAL_DATA['packets'][packet]['recipe'], 'mode': 'NONEXECUTING_OBSERVATION', 'argv_provenance': 'CAPTURED',
            'argv': row['argv'], 'cwd': row['cwd'], 'started_at': row['started_at'], 'ended_at': row['ended_at'],
            'physical_run_sha256': invocation['trace_sha256'], 'parent_log_sha256': parent['log_sha256'],
            'terminal': row['terminal'], 'exit_code': row['exit_code'], 'actual_outcome': 'ACCEPT' if row['exit_code'] == 0 else 'REJECT',
            'log_sha256': row['log_sha256'], 'result_record_sha256': record_hashes[child],
            'source_binding': row['source_binding'], 'output_hashes': row['output_hashes'], 'log_assembly': row['log_assembly'],
            'physical_record_sha256': canonical(row)}
    actual_objects = {p.relative_to(output).as_posix(): sha(p.read_bytes()) for p in original.rglob('*.olean')}
    require(actual_objects == objects, 'Fresh original object census differs from captured producers')
    return children, logs, objects


def operational_validate_child_evidence(evidence, plan, stages, successful):
    packet = plan['operational_packet']; expected = operational_physical_specs(packet)
    launches = indexed(evidence['driver_invocations'], 'parent_stage_id')
    require(set(launches) <= {'original-driver'}, 'Foreign or repeated operational original invocation')
    if successful: require(set(launches) == {'original-driver'}, 'Missing operational original invocation')
    observations = indexed(evidence['child_observations'], 'stage_id')
    declared = {sid: row for sid, row in plan['stages'].items() if row['argv'][:1] == ['{builtin:observe-child}']}
    require(set(observations) <= set(declared), 'Foreign operational observer')
    if successful: require(set(observations) == set(declared), 'Missing complete operational observer inventory')
    physical = {}
    for pid, invocation in launches.items():
        keys(invocation, {'parent_stage_id', 'driver_sha256', 'source_argv', 'launch_argv', 'launch_cwd', 'runner_sha256',
            'trace_sha256', 'parent_log_sha256', 'child_count', 'physical_children', 'helper_invocations', 'original_receipt_sha256'})
        stage = plan['stages'][pid]; driver = plan['drivers'][stage['driver_id']]
        require(invocation['source_argv'] == stage['argv'] and invocation['launch_argv'] == operational_tracer_argv(stage, packet) and
                invocation['launch_cwd'] == '{archive:source-archive}' and invocation['driver_sha256'] == driver['sha256'] and
                invocation['runner_sha256'] == evidence['runner_sha256'] and invocation['parent_log_sha256'] == stages[pid]['log_sha256'],
                'Operational original launch or terminal binding differs')
        require(isinstance(invocation['physical_children'], list), 'Malformed physical child ledger')
        physical = {}
        for actual in invocation['physical_children']:
            name = actual['physical_id']
            require(isinstance(name, str) and name not in physical and name in {spec['id'] for spec in expected},
                    'Duplicate or foreign source-owned physical child identity')
            physical[name] = actual
        require(type(invocation['child_count']) is int and invocation['child_count'] == len(physical) <= len(expected), 'Physical operational child census differs')
        allowed_order = [spec['id'] for spec in expected]
        require(list(physical) == [name for name in allowed_order if name in physical], 'Physical source call order changed')
        if invocation['trace_sha256'] is not None: digest(invocation['trace_sha256'])
        if invocation['original_receipt_sha256'] is not None: digest(invocation['original_receipt_sha256'])
        if successful:
            require(set(physical) == set(allowed_order) and invocation['trace_sha256'] is not None and invocation['original_receipt_sha256'] is not None,
                    'Incomplete physical original execution/terminal receipt')
        prior_ends = {}
        for row in physical.values():
            operational_validate_physical_row(packet, row, stages[pid], successful)
            group = row['parent_process_id']
            if group in prior_ends:
                require(prior_ends[group] is not None and prior_ends[group] <= row['started_at'], 'Source-owned serial child intervals overlap')
            prior_ends[group] = row['ended_at']
            if row['parent_process_id'] is not None:
                require(row['parent_process_id'] in physical, 'Nested child lost actual parent')
                parent = physical[row['parent_process_id']]
                require(parent['started_at'] <= row['started_at'] and (row['ended_at'] is None or parent['ended_at'] is not None and row['ended_at'] <= parent['ended_at']),
                        'Nested child interval differs from actual nested parent')
            if successful:
                for path, digest_value in row['output_hashes'].items():
                    require(evidence['output_hashes'].get(path) == digest_value, 'Physical object lacks output binding')
        operational_validate_helpers(invocation['helper_invocations'], packet, stages, evidence, successful)
    for sid, row in observations.items():
        keys(row, {'stage_id', 'source_child_id', 'parent_stage_id', 'driver_sha256', 'parser_id', 'mode', 'argv_provenance',
            'argv', 'cwd', 'started_at', 'ended_at', 'observed_at', 'physical_run_sha256', 'parent_log_sha256', 'terminal', 'exit_code',
            'actual_outcome', 'log_sha256', 'result_record_sha256', 'source_binding', 'output_hashes', 'log_assembly', 'physical_record_sha256'})
        stage = declared[sid]; pid, child = stage['argv'][1:]
        require(row['source_child_id'] == child and row['parent_stage_id'] == pid and child in physical and pid in launches, 'Observation has no actual physical child')
        actual = physical[child]
        require(row['physical_record_sha256'] == canonical(actual) and row['physical_run_sha256'] == launches[pid]['trace_sha256'] and
                row['parent_log_sha256'] == stages[pid]['log_sha256'] and row['driver_sha256'] == launches[pid]['driver_sha256'] and
                row['parser_id'] == _OPERATIONAL_DATA['packets'][packet]['recipe'] and row['mode'] == 'NONEXECUTING_OBSERVATION' and row['argv_provenance'] == 'CAPTURED',
                'Observation physical/source/parser association changed')
        for key in ('argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'source_binding', 'output_hashes', 'log_assembly'):
            require(row[key] == actual[key], 'Observation differs from actual physical child')
        require(row['terminal'] == 'COMPLETED' and row['exit_code'] in stage['expected_exit_codes'] and
                row['actual_outcome'] == ('ACCEPT' if row['exit_code'] == 0 else 'REJECT'), 'Observation has no expected actual terminal')
        require(all(row[key] == stages[sid][key] for key in ('terminal', 'exit_code', 'log_sha256')), 'Observer stage and physical result differ')
        require(stages[pid]['ended_at'] <= stages[sid]['started_at'] <= row['observed_at'] <= stages[sid]['ended_at'], 'Observation parsing time differs')
        digest(row['result_record_sha256'])

