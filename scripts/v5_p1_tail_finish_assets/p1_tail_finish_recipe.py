"""Source-bound final P1 child plus audit; prior captures are retained, never replayed."""

def p1_tail_finish_handles(suite):
    return isinstance(suite, dict) and isinstance(suite.get('replay'), dict) and suite['replay'].get('schema') == p1_tail_finish_meta['replay_schema']


def p1_tail_finish_descriptor(api, mode='CONTINUATION'):
    api.require(mode in {'CONTINUATION', 'FINITE_VIEW'}, 'Unknown P1 finish mode')
    suite = p1_tail_descriptor(api, mode)
    suite['id'] = p1_tail_finish_meta['physical_suite_id'] if mode == 'CONTINUATION' else p1_tail_finish_meta['finite_suite_id']
    suite['replay'].update(schema=p1_tail_finish_meta['replay_schema'], recipe=p1_tail_finish_meta['recipe'],
        physical_suite_id=p1_tail_finish_meta['physical_suite_id'], prior_tail=p1_tail_clone(p1_tail_finish_meta['prior_tail']),
        execute_names=['IndependentPythonControls', '_target_audit'], reused_names=['SourceShape', 'SourceContract', 'PythonEdges'],
        original_driver_prerequisite=p1_tail_clone(p1_tail_finish_meta['original_driver_prerequisite']),
        budgets=p1_tail_clone(p1_tail_finish_meta['budgets']))
    return suite


def p1_tail_finish_validate_suite(api, suite, sources, root):
    try:
        expected = p1_tail_finish_descriptor(api, suite['replay']['mode'])
        api.require(suite == expected, 'P1 finish descriptor is not the exact two-stage continuation')
        original = p1_tail_validate_suite(api, p1_tail_descriptor(api, suite['replay']['mode']), sources, root)
        api.require(p1_tail_finish_meta['prior_tail']['completed_names'] == expected['replay']['reused_names'], 'P1 finish retained prefix differs')
        return {**original, **suite['replay']}
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError('Malformed P1 finish descriptor: ' + str(error)) from error


def p1_tail_finish_retain(api, suite, sources, root, inputs, tools):
    p1_tail_finish_validate_suite(api, suite, sources, root)
    old_names = {'p1-prior-receipt', 'p1-prior-command', 'p1-private-parameters'}
    api.require(set(inputs) == old_names | {'p1-failed-tail-receipt', 'p1-failed-tail-command'}, 'P1 finish retained inputs differ')
    old_inputs = {k: inputs[k] for k in old_names}
    prior = p1_tail_finish_meta['prior_tail']
    receipt_path = api.no_symlinks(inputs['p1-failed-tail-receipt']).resolve()
    command_path = api.no_symlinks(inputs['p1-failed-tail-command']).resolve()
    api.require(receipt_path.name == 'RECEIPT.json' and command_path.name == 'COMMAND.json', 'P1 failed-tail record names differ')
    api.require(api.sha(receipt_path.read_bytes()) == prior['receipt_sha256'] and api.sha(command_path.read_bytes()) == prior['command_sha256'], 'P1 failed-tail authority bytes differ')
    p1_tail_verify_custody(api, receipt_path.parent, prior['run_files'])
    p1_tail_verify_custody(api, command_path.parent, prior['command_files'])
    tail = p1_tail_readback(api, p1_tail_descriptor(api), sources, root, receipt_path.parent, tools, old_inputs)
    api.require(api.canonical(tail) == prior['receipt_canonical_sha256'], 'P1 failed-tail receipt content differs')
    command = api.read_json(command_path)
    api.require(command['terminal'] == 'COMPLETED' and command['exit_code'] == 1 and command['formal_slots'] == 1 and
        command['log_sha256'] == api.sha((command_path.parent / 'combined.log').read_bytes()), 'P1 failed-tail outer terminal/log differs')
    stages = tail['replay_evidence']['stage_results']
    api.require(tail['outcome'] == 'FAILED' and tail['proof_scope'] == 'NONE' and tail['exit_code'] == 1 and
        [s['exit_code'] for s in stages] == prior['expected_exit_codes'] and [s['outcome'] for s in stages] == ['ACCEPT'] * 3 + ['FAILED'], 'P1 retained tail failure/prefix changed')
    api.require([api.canonical(s) for s in stages[:3]] == prior['reused_stage_sha256'] and
        stages[-1]['id'] == prior['failed_name'] and tail['replay_evidence']['new_audit_processes'] == 0 and
        tail['replay_evidence']['finite'] is None, 'P1 finish prior observations are not the exact failed tail')
    original = p1_tail_retain(api, p1_tail_descriptor(api), sources, root, old_inputs, tools)
    return {'original': original, 'tail_receipt': tail, 'tail_root': receipt_path.parent, 'tail_command': command_path,
        'prefix': p1_tail_clone(stages[:3]), 'old_inputs': old_inputs}


def p1_tail_finish_runtime(api, context, output, *, existing=False):
    runtime = p1_tail_runtime(api, context['original'], output, existing=existing)
    runtime['input_binding_sha256'] = api.canonical({'prior_tail_receipt_sha256': p1_tail_finish_meta['prior_tail']['receipt_sha256'],
        'prior_tail_receipt_canonical_sha256': p1_tail_finish_meta['prior_tail']['receipt_canonical_sha256'],
        'original_input_binding_sha256': runtime['input_binding_sha256'], 'descriptor': p1_tail_finish_descriptor(api)['replay']})
    return runtime


def p1_tail_finish_prepare_output(api, runtime):
    output = runtime['output']
    output.mkdir(parents=True); (output / 'traces').mkdir(); (output / 'original').mkdir()
    for name, data in runtime['copies'].items():
        target = api.path_in(output / 'original', name)
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    control = api.path_in(output / 'original', p1_copy_control)
    evidence = control.parents[1] / 'evidence'
    api.require(evidence == api.path_in(output, p1_tail_finish_meta['original_driver_prerequisite']['output_relative_path']), 'P1 output evidence directory differs from original driver')
    # Exact source prerequisite: replay.py SHA3c6cd0c6, line160.
    evidence.mkdir()


def p1_tail_finish_collect(api, context, runtime):
    output = runtime['output']; trace = api.no_symlinks(output / 'traces')
    api.require({p.name for p in trace.iterdir()} <= {'0003.json', '0003.log', 'audit.json', 'audit.log'}, 'P1 finish has duplicate/replayed/unprescribed captures')
    copies = {}
    for name, data in runtime['copies'].items():
        api.require(api.path_in(output / 'original', name).read_bytes() == data, 'P1 finish exact output copy changed')
        copies[name] = api.sha(data)
    path = trace / '0003.json'
    if not path.exists(): return {'stage_results': [], 'finite': None, 'copies': copies, 'outcome': 'INCOMPLETE'}
    cap = api.read_json(api.no_symlinks(path)); event = runtime['events'][3]
    api.keys(cap, {'id', 'index', 'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256', 'argv', 'cwd', 'source_sha256',
        'source_binding', 'environment_sha256', 'input_binding_sha256', 'required_copies', 'output_hashes', 'derivation'})
    for key in ('id', 'index', 'argv', 'cwd', 'source_sha256', 'source_binding', 'required_copies'):
        api.require(cap[key] == event[key], 'P1 finish actual remaining-child/source binding differs: ' + key)
    api.require(cap['environment_sha256'] == runtime['environment_sha256'] and cap['input_binding_sha256'] == runtime['input_binding_sha256'], 'P1 finish captured environment/input differs')
    p1_time(api, cap['started_at']); p1_time(api, cap['ended_at'])
    api.require(context['tail_receipt']['ended_at'] <= cap['started_at'] <= cap['ended_at'], 'P1 finish child precedes the failed tail')
    raw = api.no_symlinks(path.with_suffix('.log')).read_bytes()
    api.require(api.sha(raw) == cap['log_sha256'], 'P1 finish raw output changed')
    neutral = api.no_symlinks(output / 'original/logs/IndependentPythonControls.log').read_bytes()
    derived = p1_neutralize(api, raw, runtime['replacements'], cap['terminal'] == 'TIMEOUT')
    api.require(derived['derived_bytes'] == neutral and cap['derivation'] == {k: v for k, v in derived.items() if k != 'derived_bytes'}, 'P1 finish raw/neutral derivation differs')
    api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 finish child source changed')
    expected_outputs = {}
    report = output / 'original' / p1_finite_rel
    if report.exists(): expected_outputs[str(report)] = api.sha(api.no_symlinks(report).read_bytes())
    api.require(cap['output_hashes'] == expected_outputs, 'P1 finish report/capture binding differs')
    texts = {}
    for stage in context['prefix']:
        prior_log = api.no_symlinks(context['tail_root'] / 'original/logs' / (stage['id'] + '.log')).read_bytes()
        api.require(api.sha(prior_log) == stage['derivation']['derived_sha256'], 'P1 retained successful finite log changed')
        texts[stage['id']] = prior_log.decode('utf8')
        p1_tail_partial_semantics(api, runtime['packet'], stage['id'], texts)
    outcome = p1_tail_outcome(api, cap, raw); finite = None
    if outcome == 'ACCEPT':
        try:
            texts['IndependentPythonControls'] = neutral.decode('utf8')
            finite = p1_tail_finite(api, runtime['packet'], output / 'original', texts)
            from datetime import datetime
            created = datetime.fromisoformat(api.read_json(report)['created_utc'].replace('Z', '+00:00'))
            api.require(p1_time(api, cap['started_at']) <= created <= p1_time(api, cap['ended_at']), 'P1 finish report lies outside its actual child interval')
        except (ValueError, KeyError, TypeError, UnicodeError): outcome = 'FAILED'; finite = None
    public = p1_symbolize(api, cap, runtime['mapping'])
    stage = {**public, 'outcome': outcome, 'capture_sha256': api.sha(path.read_bytes()), 'timeout_seconds': 180, 'rejecting_subprocesses': 0}
    return {'stage_results': [stage], 'finite': finite, 'copies': copies, 'outcome': 'COMPLETE' if outcome == 'ACCEPT' else outcome}


def p1_tail_finish_implementation(api):
    return {'runner_sha256': api.sha(Path(api.__file__).read_bytes()), 'assets': p1_tail_clone(p1_tail_finish_asset_pins)}


def p1_tail_finish_initial(api, suite, sources, reviews, context, runtime, dependencies):
    receipt = p1_initial_receipt(api, suite, sources, reviews)
    receipt['replay_evidence'] = {'schema': p1_tail_finish_meta['evidence_schema'], 'recipe': p1_tail_finish_meta['recipe'],
        'mode': suite['replay']['mode'], 'descriptor_sha256': api.canonical(suite['replay']), 'implementation': p1_tail_finish_implementation(api),
        'source_hashes_before': dict(receipt['source_hashes']), 'source_hashes_after': dict(receipt['source_hashes']),
        'retained_tail': p1_tail_clone(context['tail_receipt']), 'retained_prefix': p1_tail_clone(context['prefix']),
        'source_python': p1_tail_clone(p1_tail_meta['source_python']), 'dependency_checks_before': dependencies, 'dependency_checks_after': None,
        'runtime_sha256': api.sha((runtime['output'] / 'RUNTIME.json').read_bytes()), 'output_custody_sha256': None,
        'created_directories': [p1_tail_finish_meta['original_driver_prerequisite']['output_relative_path']],
        'copies': {k: api.sha(v) for k, v in runtime['copies'].items()}, 'stage_results': [], 'finite': None, 'target_audits': [], 'audit_source_sha256': None,
        'retained_builds': 9, 'reused_finite_observations': 3, 'new_finite_processes': 0, 'new_audit_processes': 0,
        'new_builds': 0, 'new_wrapper_runs': 0, 'independent_evidence_increment': 0, 'post_verified': False, 'scope_ceiling': p1_ceiling}
    return receipt


def p1_tail_finish_controls(api, suite, ev):
    combined = {'retained': ev['retained_tail']['replay_evidence']['retained'], 'stage_results': ev['retained_prefix'] + ev['stage_results'][:1]}
    return p1_tail_controls(api, suite, combined)


def p1_tail_finish_output_rows(api, output):
    rows = p1_tail_output_rows(api, output)
    forbidden = {'traces/' + f'{i:04}' + suffix for i in range(3) for suffix in ('.json', '.log')} | {
        'original/logs/' + name + '.log' for name in p1_tail_finish_meta['prior_tail']['completed_names']}
    api.require(not {r['path'] for r in rows} & forbidden, 'P1 finish copied or recreated prior successful observations')
    return rows


def p1_tail_finish_execute_suite(api, suite, sources, root, output, tools, inputs, scope=None, reviews=None):
    plan = p1_tail_finish_validate_suite(api, suite, sources, root)
    api.require(scope is None or scope == plan['scope'], 'P1 finish scope differs')
    api.require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'P1 finish reviews missing')
    output = api.no_symlinks(output).resolve(); api.require(not output.exists(), 'P1 finish output must be fresh')
    for path in [root, *tools.values(), *inputs.values(), *(Path(p).parent for k, p in inputs.items() if k.endswith(('receipt', 'command')))]:
        resolved = Path(path).resolve()
        api.require(not output.is_relative_to(resolved) and not resolved.is_relative_to(output), 'P1 finish output overlaps retained inputs')
    if plan['mode'] == 'FINITE_VIEW': return p1_tail_finish_join_finite(api, suite, sources, root, output, tools, inputs, reviews)
    import sys
    api.require(sys.version_info[:3] == (3, 11, 9) and api.sha(Path(sys.executable).read_bytes()) == p1_tail_meta['orchestration_python']['sha256'], 'P1 finish orchestration Python differs')
    context = p1_tail_finish_retain(api, suite, sources, root, inputs, tools)
    runtime = p1_tail_finish_runtime(api, context, output)
    original = context['original']
    deps = p1_verify_dependencies(api, original['packet'], original['lean_root'], original['tools']['paths']['mathlib'], original['private'])
    api.require(deps == original['receipt']['replay_evidence']['dependency_checks'], 'P1 finish imported source/object closure changed')
    p1_tail_finish_prepare_output(api, runtime)
    api.write_json(output / 'SUITE.json', suite)
    record = {'event': runtime['events'][3], 'environment_sha256': runtime['environment_sha256'], 'input_binding_sha256': runtime['input_binding_sha256'],
        'replacements': runtime['replacements'], 'audit_source_sha256': api.sha(runtime['audit_source'].encode()),
        'prior_tail_receipt_sha256': p1_tail_finish_meta['prior_tail']['receipt_sha256']}
    api.write_json(output / 'RUNTIME.json', record)
    receipt = p1_tail_finish_initial(api, suite, sources, reviews, context, runtime, deps); ev = receipt['replay_evidence']
    p1_save_receipt(api, receipt, output)
    try:
        event = runtime['events'][3]; log = output / 'traces/0003.log'
        api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 finish source changed before child')
        result = api.run_process(event['argv'], Path(event['cwd']), runtime['env'], log, 180)
        api.write_json(log.with_suffix('.json'), p1_tail_capture(api, runtime, event, result, log.read_bytes()))
        collected = p1_tail_finish_collect(api, context, runtime)
        ev['stage_results'] = p1_tail_clone(collected['stage_results']); ev['finite'] = collected['finite']; ev['copies'] = collected['copies']
        ev['new_finite_processes'] = int(ev['stage_results'][0]['terminal'] != 'MISSING')
        if collected['outcome'] != 'COMPLETE':
            receipt['outcome'] = collected['outcome']; raise ValueError('P1 remaining finite child did not complete its source contract')
        generated = output / 'generated'; generated.mkdir()
        audit = generated / 'P1TailCheckedReadback.lean'; audit.write_text(runtime['audit_source'], encoding='utf8')
        ev['audit_source_sha256'] = api.sha(audit.read_bytes())
        result = api.run_process([original['tools']['paths']['lean'], '-j1', audit], original['packet'], runtime['env'], output / 'traces/audit.log', 300)
        api.write_json(output / 'traces/audit.json', result)
        stage, audits = p1_tail_audit_capture(api, runtime, result)
        ev['stage_results'].append(stage); ev['target_audits'] = audits; ev['new_audit_processes'] = int(result['terminal'] != 'MISSING')
        if stage['outcome'] != 'ACCEPT':
            receipt['outcome'] = stage['outcome']; raise ValueError('P1 finish safe target audit did not complete')
        api.require(audit.read_bytes() == runtime['audit_source'].encode(), 'P1 finish audit source changed')
        again = p1_tail_finish_retain(api, suite, sources, root, inputs, tools)
        api.require(again['tail_receipt'] == context['tail_receipt'] and again['prefix'] == context['prefix'], 'P1 finish retained observations changed')
        post = p1_verify_dependencies(api, original['packet'], original['lean_root'], original['tools']['paths']['mathlib'], original['private'])
        api.require(post == deps, 'P1 finish transitive source/cache inventory changed')
        ev['dependency_checks_after'] = post
        api.require(p1_tail_finish_collect(api, context, runtime) == collected, 'P1 finish captured evidence changed during audit')
        p1_tail_check_tools(api, tools)
        for source in plan['files']:
            api.require(api.public_bytes(root, sources[source['source_id']]) == plan['contents'][source['path']], 'P1 finish source changed')
        ev['post_verified'] = True
        receipt['controls'] = p1_tail_finish_controls(api, suite, ev)
        receipt['target_readbacks'] = [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']]
        receipt['axioms'] = sorted({a for audit_row in audits for a in audit_row['axioms']})
        receipt.update(outcome='FRESH_KERNEL_COMPONENTS', proof_scope='COMPONENTS', exit_code=0)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError, KeyboardInterrupt) as error:
        api.write_json(output / 'FAILURE.json', {'kind': type(error).__name__, 'message': str(error), 'scope': 'PRIVATE_DIAGNOSTIC'})
        if receipt['outcome'] != 'RESOURCE_INCONCLUSIVE': receipt['outcome'] = 'RESOURCE_INCONCLUSIVE' if isinstance(error, KeyboardInterrupt) else 'FAILED'
        receipt.update(proof_scope='NONE', exit_code=1, controls=[], target_readbacks=[], axioms=[])
    api.write_json(output / 'OUTPUT_CUSTODY.json', p1_tail_finish_output_rows(api, output))
    ev['output_custody_sha256'] = api.sha((output / 'OUTPUT_CUSTODY.json').read_bytes())
    p1_save_receipt(api, receipt, output)
    p1_tail_finish_validate_receipt(api, receipt, suite, sources, root)
    return receipt


def p1_tail_finish_validate_common(api, receipt, suite, sources):
    api.keys(receipt, {'id', 'suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256', 'outcome',
        'target_readbacks', 'controls', 'stages', 'invocation', 'started_at', 'ended_at', 'exit_code', 'log_sha256', 'axioms', 'proof_scope', 'replay_evidence'})
    api.require(receipt['id'] == suite['id'] + '-replay' and receipt['suite_id'] == suite['id'] and receipt['family'] == suite['family'] and
        receipt['suite_sha256'] == api.canonical(suite) and receipt['toolchain_sha256'] == api.canonical(suite['toolchain']), 'P1 finish suite identity differs')
    api.require(receipt['source_hashes'] == p1_projection_hashes(api, suite, sources) and
        receipt['review_hashes'] == {name: p1_tail_meta['review_hashes'][name] for name in suite['review_ids']}, 'P1 finish source/review identity differs')
    p1_time(api, receipt['started_at']); p1_time(api, receipt['ended_at'])
    api.require(receipt['started_at'] <= receipt['ended_at'] and receipt['invocation'] ==
        ['replay_v5_successors.py', '--execute', '--suite', suite['id'], '--out', '{out}'], 'P1 finish invocation/interval differs')
    ev = receipt['replay_evidence']
    api.require(ev['schema'] == p1_tail_finish_meta['evidence_schema'] and ev['recipe'] == p1_tail_finish_meta['recipe'] and
        ev['mode'] == suite['replay']['mode'] and ev['descriptor_sha256'] == api.canonical(suite['replay']), 'P1 finish family binding differs')
    implementation = ev['implementation']; api.keys(implementation, {'runner_sha256', 'assets'})
    accepted = {p1_tail_finish_implementation(api)['runner_sha256']: p1_tail_clone(p1_tail_finish_asset_pins)}
    accepted.update(getattr(api, 'p1_tail_finish_accepted_predecessors', {}))
    api.require(implementation['runner_sha256'] in accepted and implementation['assets'] == accepted[implementation['runner_sha256']], 'P1 finish implementation is not an accepted immutable version')
    api.require(receipt['stages'] == [{k: r[k] for k in ('id', 'terminal', 'exit_code', 'log_sha256')} for r in ev['stage_results']] and
        receipt['log_sha256'] == api.canonical({r['id']: r['log_sha256'] for r in ev['stage_results']}), 'P1 finish public stage/log summary differs')


def p1_tail_finish_validate_receipt(api, receipt, suite, sources, root):
    try:
        plan = p1_tail_finish_validate_suite(api, suite, sources, root)
        p1_tail_finish_validate_common(api, receipt, suite, sources)
        ev = receipt['replay_evidence']
        if plan['mode'] == 'FINITE_VIEW': return p1_tail_finish_validate_view(api, receipt, suite, sources, root)
        api.keys(ev, {'schema', 'recipe', 'mode', 'descriptor_sha256', 'implementation', 'source_hashes_before', 'source_hashes_after',
            'retained_tail', 'retained_prefix', 'source_python', 'dependency_checks_before', 'dependency_checks_after', 'runtime_sha256',
            'output_custody_sha256', 'created_directories', 'copies', 'stage_results', 'finite', 'target_audits', 'audit_source_sha256',
            'retained_builds', 'reused_finite_observations', 'new_finite_processes', 'new_audit_processes', 'new_builds', 'new_wrapper_runs',
            'independent_evidence_increment', 'post_verified', 'scope_ceiling'})
        tail = ev['retained_tail']; prior = p1_tail_finish_meta['prior_tail']
        api.require(api.canonical(tail) == prior['receipt_canonical_sha256'], 'P1 finish altered the retained failed tail')
        p1_tail_validate_receipt(api, tail, p1_tail_descriptor(api), sources, root)
        api.require(tail['outcome'] == 'FAILED' and tail['proof_scope'] == 'NONE' and tail['ended_at'] <= receipt['started_at'], 'P1 finish promoted or preceded its failed parent')
        api.require(ev['retained_prefix'] == tail['replay_evidence']['stage_results'][:3] and
            [api.canonical(r) for r in ev['retained_prefix']] == prior['reused_stage_sha256'], 'P1 retained finite captures/intervals changed')
        api.require(ev['source_hashes_before'] == ev['source_hashes_after'] == receipt['source_hashes'] and
            ev['source_python'] == p1_tail_meta['source_python'] and ev['scope_ceiling'] == p1_ceiling, 'P1 finish source/interpreter/scope differs')
        dependencies = tail['replay_evidence']['dependency_checks_before']
        api.require(ev['dependency_checks_before'] == dependencies and
            (ev['dependency_checks_after'] is None or ev['dependency_checks_after'] == dependencies), 'P1 finish imported inventory binding differs')
        for key, value in {'retained_builds': 9, 'reused_finite_observations': 3, 'new_builds': 0, 'new_wrapper_runs': 0, 'independent_evidence_increment': 0}.items():
            api.require(type(ev[key]) is int and ev[key] == value, 'P1 finish process/reuse credit differs: ' + key)
        api.require(type(ev['post_verified']) is bool and ev['created_directories'] ==
            [p1_tail_finish_meta['original_driver_prerequisite']['output_relative_path']], 'P1 finish output prerequisite/postcondition differs')
        api.digest(ev['runtime_sha256']); api.digest(ev['output_custody_sha256'])
        expected_copies = {p1_copy_control: p1_meta['members']['reviewer/independent_source_controls.py']['sha256'], **{n: p1_source for n in p1_copy_codecs}}
        api.require(ev['copies'] == expected_copies, 'P1 finish copied different scientific bytes')
        stages = ev['stage_results']
        api.require(isinstance(stages, list) and len(stages) <= 2 and [r['id'] for r in stages] == ['IndependentPythonControls', '_target_audit'][:len(stages)], 'P1 finish duplicated, reordered or replayed a process')
        input_sha = api.canonical({'prior_tail_receipt_sha256': prior['receipt_sha256'], 'prior_tail_receipt_canonical_sha256': prior['receipt_canonical_sha256'],
            'original_input_binding_sha256': api.canonical({'prior': p1_tail_meta['retained_public'], 'source_python': p1_tail_meta['source_python'], 'descriptor': p1_tail_descriptor(api)['replay']}),
            'descriptor': p1_tail_finish_descriptor(api)['replay']})
        previous = receipt['started_at']; environment = None; failed = False
        for number, stage in enumerate(stages):
            api.require(not failed, 'P1 finish continued after a failed/resource stage')
            common = {'id', 'index', 'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256', 'argv', 'cwd', 'source_sha256',
                'environment_sha256', 'input_binding_sha256', 'timeout_seconds', 'outcome', 'rejecting_subprocesses'}
            api.keys(stage, common | ({'source_binding', 'required_copies', 'output_hashes', 'derivation', 'capture_sha256'} if number == 0 else {'retained_object_set_sha256'}))
            api.require(type(stage['index']) is int and stage['index'] == number + 3 and
                type(stage['rejecting_subprocesses']) is int and stage['rejecting_subprocesses'] == 0, 'P1 finish source index/rejection credit differs')
            p1_time(api, stage['started_at']); p1_time(api, stage['ended_at'])
            api.require(previous <= stage['started_at'] <= stage['ended_at'] <= receipt['ended_at'], 'P1 finish process interval differs'); previous = stage['ended_at']
            for key in ('log_sha256', 'source_sha256', 'environment_sha256', 'input_binding_sha256'): api.digest(stage[key])
            if environment is None: environment = stage['environment_sha256']
            api.require(stage['environment_sha256'] == environment and stage['input_binding_sha256'] == input_sha, 'P1 finish new-process input/environment differs')
            api.require(stage['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED', 'MISSING'} and
                ((stage['terminal'] == 'COMPLETED' and type(stage['exit_code']) is int and 0 <= stage['exit_code'] < 124) or
                (stage['terminal'] != 'COMPLETED' and stage['exit_code'] is None)), 'P1 finish terminal/exit differs')
            api.require(stage['outcome'] in {'ACCEPT', 'FAILED', 'RESOURCE_INCONCLUSIVE'}, 'P1 finish stage outcome differs')
            if stage['terminal'] != 'COMPLETED': api.require(stage['outcome'] == 'RESOURCE_INCONCLUSIVE', 'P1 finish resource terminal gained success')
            if stage['outcome'] == 'ACCEPT': api.require(stage['terminal'] == 'COMPLETED' and stage['exit_code'] == 0, 'P1 finish acceptance lacks zero exit')
            if number == 0:
                contract = plan['tail'][3]
                api.require(stage['argv'] == contract['argv'] and stage['cwd'] == '{out}/original' and stage['timeout_seconds'] == 180 and
                    stage['source_sha256'] == contract['source_binding']['source_sha256'] and stage['source_binding'] == contract['source_binding'], 'P1 finish remaining source/argv/budget differs')
                api.require(stage['required_copies'] == {'{out}/original/' + k: v for k, v in expected_copies.items()} and
                    set(stage['output_hashes']) <= {'{out}/original/' + p1_finite_rel}, 'P1 finish remaining source/report binding differs')
                for digest in stage['output_hashes'].values(): api.digest(digest)
                api.digest(stage['capture_sha256']); p1_tail_validate_derivation(api, stage['derivation'], stage['log_sha256'], stage['terminal'] == 'TIMEOUT')
            else:
                expected_source = api.sha(p1_audit_source(api, plan['audit_targets']).encode())
                api.require(stage['argv'] == ['{tool:lean}', '-j1', '{out}/generated/P1TailCheckedReadback.lean'] and stage['cwd'] == '{retained:packet}' and
                    stage['timeout_seconds'] == 300 and stage['source_sha256'] == ev['audit_source_sha256'] == expected_source and
                    stage['retained_object_set_sha256'] == api.canonical(p1_tail_meta['prior']['objects']), 'P1 finish audit source/object binding differs')
            failed = stage['outcome'] != 'ACCEPT'
        api.require(type(ev['new_finite_processes']) is int and ev['new_finite_processes'] == int(bool(stages) and stages[0]['terminal'] != 'MISSING') and
            type(ev['new_audit_processes']) is int and ev['new_audit_processes'] == int(len(stages) == 2 and stages[1]['terminal'] != 'MISSING'), 'P1 finish physical process accounting differs')
        if ev['finite'] is not None:
            p1_tail_validate_finite(api, ev['finite'])
            api.require(stages and stages[0]['outcome'] == 'ACCEPT' and stages[0]['output_hashes'] ==
                {'{out}/original/' + p1_finite_rel: ev['finite']['finite_receipt_sha256']}, 'P1 finish finite census lacks its actual completed child report')
        if ev['target_audits']:
            api.require(len(stages) == 2 and stages[1]['outcome'] == 'ACCEPT' and len(ev['target_audits']) == 41, 'P1 finish audit is incomplete')
            for audit, target in zip(ev['target_audits'], plan['audit_targets']):
                api.keys(audit, {'target_id', 'name', 'type_sha256', 'axioms', 'closure_status', 'checked_declarations', 'log_sha256'})
                api.require(audit['target_id'] == target['target_id'] and audit['name'] == target['name'] and audit['log_sha256'] == stages[1]['log_sha256'], 'P1 finish audit target association differs')
                api.require(audit['closure_status'] == 'CHECKED_SAFE' and type(audit['checked_declarations']) is int and audit['checked_declarations'] > 0 and
                    isinstance(audit['axioms'], list) and audit['axioms'] == sorted(set(audit['axioms'])) and set(audit['axioms']) <= api.AXIOMS, 'P1 finish target closure is unsafe')
                api.digest(audit['type_sha256'])
        api.require(receipt['outcome'] in {'NOT_RUN', 'FAILED', 'RESOURCE_INCONCLUSIVE', 'FRESH_KERNEL_COMPONENTS'}, 'P1 finish result scope differs')
        if any(s['outcome'] == 'RESOURCE_INCONCLUSIVE' for s in stages): api.require(receipt['outcome'] == 'RESOURCE_INCONCLUSIVE', 'P1 finish suppressed resource outcome')
        if receipt['outcome'] != 'FRESH_KERNEL_COMPONENTS':
            api.require(receipt['proof_scope'] == 'NONE' and receipt['exit_code'] in (None, 1) and receipt['controls'] == [] and
                receipt['target_readbacks'] == [] and receipt['axioms'] == [], 'P1 incomplete finish gained qualification')
            return {'suite_id': suite['id'], 'outcome': receipt['outcome'], 'scope': 'P1_FINISH_FAILED_OR_PARTIAL_ONLY'}
        api.require(receipt['proof_scope'] == 'COMPONENTS' and type(receipt['exit_code']) is int and receipt['exit_code'] == 0 and
            len(stages) == 2 and all(s['outcome'] == 'ACCEPT' for s in stages) and ev['post_verified'] is True and
            ev['dependency_checks_after'] == dependencies and ev['finite'] is not None and len(ev['target_audits']) == 41, 'P1 finish lacks required remaining controls/audit/postconditions')
        api.require(receipt['controls'] == p1_tail_finish_controls(api, suite, ev) and receipt['target_readbacks'] ==
            [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']], 'P1 finish source/target/control association differs')
        api.require(receipt['axioms'] == sorted({a for audit in ev['target_audits'] for a in audit['axioms']}), 'P1 finish axiom summary differs')
        return {'suite_id': suite['id'], 'outcome': receipt['outcome'], 'scope': 'P1_RETAINED_COMPONENTS_AND_THREE_FINITE_CAPTURES_WITH_ONE_FINITE_CHILD_AND_AUDIT'}
    except (KeyError, TypeError, AttributeError, IndexError) as error:
        raise ValueError('Malformed P1 finish receipt: ' + str(error)) from error


def p1_tail_finish_readback(api, suite, sources, root, output, tools, inputs):
    output = api.no_symlinks(output).resolve(); receipt = api.read_json(output / 'RECEIPT.json')
    p1_tail_finish_validate_receipt(api, receipt, suite, sources, root)
    api.require(api.read_json(output / 'SUITE.json') == suite, 'P1 finish stored suite differs')
    ev = receipt['replay_evidence']; custody = output / 'OUTPUT_CUSTODY.json'
    api.require(api.sha(custody.read_bytes()) == ev['output_custody_sha256'] and api.read_json(custody) ==
        p1_tail_finish_output_rows(api, output), 'P1 finish output custody changed')
    context = p1_tail_finish_retain(api, suite, sources, root, inputs, tools)
    runtime = p1_tail_finish_runtime(api, context, output, existing=True)
    record = api.read_json(output / 'RUNTIME.json')
    api.keys(record, {'event', 'environment_sha256', 'input_binding_sha256', 'replacements', 'audit_source_sha256', 'prior_tail_receipt_sha256'})
    api.require(api.sha((output / 'RUNTIME.json').read_bytes()) == ev['runtime_sha256'] and record['event'] == runtime['events'][3] and
        record['input_binding_sha256'] == runtime['input_binding_sha256'] and record['replacements'] == runtime['replacements'] and
        record['audit_source_sha256'] == api.sha(runtime['audit_source'].encode()) and
        record['prior_tail_receipt_sha256'] == p1_tail_finish_meta['prior_tail']['receipt_sha256'], 'P1 finish private runtime association differs')
    api.digest(record['environment_sha256']); runtime['environment_sha256'] = record['environment_sha256']
    evidence = api.no_symlinks(output / p1_tail_finish_meta['original_driver_prerequisite']['output_relative_path'])
    api.require(evidence.is_dir(), 'P1 finish source-owned evidence directory is missing')
    collected = p1_tail_finish_collect(api, context, runtime)
    api.require(collected['stage_results'] == ev['stage_results'][:1] and collected['finite'] == ev['finite'] and collected['copies'] == ev['copies'], 'P1 finish actual remaining-child recollection differs')
    if len(ev['stage_results']) == 2:
        api.require((output / 'generated/P1TailCheckedReadback.lean').read_bytes() == runtime['audit_source'].encode(), 'P1 finish generated audit changed')
        stage, audits = p1_tail_audit_capture(api, runtime, api.read_json(output / 'traces/audit.json'))
        api.require(stage == ev['stage_results'][1] and audits == ev['target_audits'], 'P1 finish actual target audit recollection differs')
    return receipt


def p1_tail_finish_join_finite(api, suite, sources, root, output, tools, inputs, reviews):
    api.require(set(inputs) == {'p1-prior-receipt', 'p1-prior-command', 'p1-private-parameters', 'p1-failed-tail-receipt', 'p1-failed-tail-command', 'p1-finish-receipt'}, 'P1 finish finite inputs differ')
    physical_path = api.no_symlinks(inputs['p1-finish-receipt']).resolve()
    api.require(physical_path.name == 'RECEIPT.json', 'P1 finish finite view needs an actual physical receipt')
    physical = p1_tail_finish_readback(api, p1_tail_finish_descriptor(api), sources, root, physical_path.parent, tools,
        {k: v for k, v in inputs.items() if k != 'p1-finish-receipt'})
    api.require(physical['outcome'] == 'FRESH_KERNEL_COMPONENTS', 'P1 finish finite view lacks qualified physical completion')
    output.mkdir(parents=True); receipt = p1_initial_receipt(api, suite, sources, reviews)
    joined = {'physical_receipt_sha256': api.sha(physical_path.read_bytes()), 'physical_receipt_canonical_sha256': api.canonical(physical),
        'new_processes': 0, 'new_builds': 0, 'independent_evidence_increment': 0}
    api.write_json(output / 'JOIN.json', joined)
    stage = {'id': 'p1-finish-view-join', 'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': receipt['started_at'], 'ended_at': api.utc(),
        'log_sha256': api.sha((output / 'JOIN.json').read_bytes()), 'argv': ['{builtin:p1-finish-view-join}', '{input:p1-finish-receipt}'], 'new_processes': 0}
    receipt['replay_evidence'] = {'schema': p1_tail_finish_meta['evidence_schema'], 'recipe': p1_tail_finish_meta['recipe'], 'mode': 'FINITE_VIEW',
        'descriptor_sha256': api.canonical(suite['replay']), 'implementation': p1_tail_finish_implementation(api), **joined,
        'physical_receipt': physical, 'stage_results': [stage], 'scope_ceiling': p1_ceiling}
    receipt['controls'] = p1_tail_finish_controls(api, suite, physical['replay_evidence'])
    receipt['target_readbacks'] = [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']]
    receipt.update(outcome='FINITE_ONLY', proof_scope='FINITE', exit_code=0, axioms=[])
    p1_save_receipt(api, receipt, output); p1_tail_finish_validate_receipt(api, receipt, suite, sources, root)
    return receipt


def p1_tail_finish_validate_view(api, receipt, suite, sources, root):
    ev = receipt['replay_evidence']
    api.keys(ev, {'schema', 'recipe', 'mode', 'descriptor_sha256', 'implementation', 'physical_receipt_sha256', 'physical_receipt_canonical_sha256',
        'new_processes', 'new_builds', 'independent_evidence_increment', 'physical_receipt', 'stage_results', 'scope_ceiling'})
    for key in ('new_processes', 'new_builds', 'independent_evidence_increment'):
        api.require(type(ev[key]) is int and ev[key] == 0, 'P1 finish view gained independent execution credit')
    physical = ev['physical_receipt']; api.digest(ev['physical_receipt_sha256'])
    api.require(ev['physical_receipt_canonical_sha256'] == api.canonical(physical), 'P1 finish view physical content changed')
    p1_tail_finish_validate_receipt(api, physical, p1_tail_finish_descriptor(api), sources, root)
    api.require(physical['outcome'] == 'FRESH_KERNEL_COMPONENTS' and physical['ended_at'] <= receipt['started_at'] and
        receipt['outcome'] == 'FINITE_ONLY' and receipt['proof_scope'] == 'FINITE' and type(receipt['exit_code']) is int and receipt['exit_code'] == 0 and
        receipt['axioms'] == [] and ev['scope_ceiling'] == p1_ceiling, 'P1 finish view lacks a successful correlated completion')
    api.require(len(ev['stage_results']) == 1, 'P1 finish view has extra process stages')
    stage = ev['stage_results'][0]
    api.keys(stage, {'id', 'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256', 'argv', 'new_processes'})
    api.require(stage['id'] == 'p1-finish-view-join' and stage['terminal'] == 'COMPLETED' and type(stage['exit_code']) is int and stage['exit_code'] == 0 and
        stage['argv'] == ['{builtin:p1-finish-view-join}', '{input:p1-finish-receipt}'] and type(stage['new_processes']) is int and stage['new_processes'] == 0, 'P1 finish view is not a zero-process join')
    p1_time(api, stage['started_at']); p1_time(api, stage['ended_at']); api.digest(stage['log_sha256'])
    api.require(receipt['started_at'] <= stage['started_at'] <= stage['ended_at'] <= receipt['ended_at'], 'P1 finish view interval differs')
    api.require(receipt['controls'] == p1_tail_finish_controls(api, suite, physical['replay_evidence']) and receipt['target_readbacks'] ==
        [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']], 'P1 finish view declaration/observation association differs')
    return {'suite_id': suite['id'], 'outcome': 'FINITE_ONLY', 'scope': 'P1_FINISH_CORRELATED_ZERO_PROCESS_FINITE_VIEW'}
