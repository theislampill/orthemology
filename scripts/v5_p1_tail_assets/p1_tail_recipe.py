"""Exact P1 failed-attempt continuation; no original wrapper or object producer."""

def p1_tail_clone(value):
    return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))


def p1_tail_handles(suite):
    return isinstance(suite, dict) and isinstance(suite.get('replay'), dict) and suite['replay'].get('schema') == p1_tail_meta['replay_schema']


def p1_tail_descriptor(api, mode='CONTINUATION'):
    api.require(mode in {'CONTINUATION', 'FINITE_VIEW'}, 'Unknown P1 tail view')
    physical = p1_tail_clone(p1_tail_meta['original_physical_suite'])
    suite = p1_tail_clone(physical if mode == 'CONTINUATION' else p1_tail_meta['original_finite_suite'])
    tail = []
    for index, child in enumerate(physical['replay']['children'][-4:]):
        row = p1_tail_clone(child)
        row['index'] = index
        row['argv'] = [part.replace('{tool:python}', '{tool:python-source}').replace('{archive:p1}', '{retained:packet}') for part in row['argv']]
        # Exact bytes are copied by this continuation, never attributed to a rerun wrapper.
        if row['id'] == 'IndependentPythonControls':
            row['source_binding']['derivation_id'] = 'p1-tail-control-copy'
        tail.append(row)
    suite['id'] = p1_tail_meta['physical_suite_id'] if mode == 'CONTINUATION' else p1_tail_meta['finite_suite_id']
    suite['replay'] = {'schema': p1_tail_meta['replay_schema'], 'recipe': p1_tail_meta['recipe'],
        'mode': mode, 'scope': 'COMPONENTS' if mode == 'CONTINUATION' else 'FINITE',
        'original_suite_sha256': api.canonical(physical), 'original_finite_suite_sha256': api.canonical(p1_tail_meta['original_finite_suite']),
        'prior_receipt_sha256': p1_tail_meta['prior']['receipt_sha256'],
        'prior_receipt_canonical_sha256': p1_tail_meta['prior']['receipt_canonical_sha256'],
        'prior_run_custody_sha256': p1_tail_meta['prior']['run_custody_sha256'],
        'prior_command_custody_sha256': p1_tail_meta['prior']['command_custody_sha256'],
        'files': physical['replay']['files'], 'retained_objects': p1_tail_clone(p1_tail_meta['prior']['objects']),
        'tail': tail, 'audit_targets': physical['replay']['audit_targets'],
        'source_python': p1_tail_clone(p1_tail_meta['source_python']),
        'orchestration_python': p1_tail_clone(p1_tail_meta['orchestration_python']),
        'source_readme_sha256': p1_tail_meta['source_readme_sha256'], 'source_ast_pin_sha256': p1_tail_meta['source_ast_pin_sha256'],
        'private_parameters': physical['replay']['private_parameters'], 'dependency_pins': physical['replay']['dependency_pins'],
        'budgets': p1_tail_clone(p1_tail_meta['budgets']), 'new_lean_producer_builds': 0,
        'prior_wrapper_replays': 0, 'independent_evidence_increment': 0,
        'physical_suite_id': p1_tail_meta['physical_suite_id'], 'scope_ceiling': p1_ceiling}
    return suite


def p1_tail_validate_suite(api, suite, sources, root):
    try:
        expected = p1_tail_descriptor(api, suite['replay']['mode'])
        api.require(suite == expected, 'P1 tail descriptor differs from the complete exact continuation')
        prior = p1_tail_meta['prior']
        api.require(api.canonical(p1_tail_meta['original_physical_suite']) == prior['suite_sha256'], 'P1 original descriptor pin differs')
        original = p1_validate_suite(api, p1_tail_meta['original_physical_suite'], sources, root)
        p1_validate_suite(api, p1_tail_meta['original_finite_suite'], sources, root)
        for child in suite['replay']['tail']:
            p1_source_binding(api, child['source_binding'], sources, p1_meta['members'][child['owner_path']]['sha256'])
        api.require(len(suite['replay']['audit_targets']) == 41, 'P1 tail audit census differs')
        return {**suite['replay'], 'contents': original['contents'], 'paths': original['paths'],
                'targets': {t['id']: t for t in suite['targets']}}
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError('Malformed P1 continuation descriptor: ' + str(error)) from error


def p1_tail_verify_custody(api, root, rows):
    root = api.no_symlinks(root).resolve()
    api.require(root.is_dir() and isinstance(rows, list) and rows, 'P1 retained custody is missing')
    expected = {}
    for row in rows:
        api.keys(row, {'path', 'sha256', 'bytes'})
        name = api.relative(row['path']); api.digest(row['sha256'])
        api.require(name not in expected and type(row['bytes']) is int and row['bytes'] >= 0, 'Invalid P1 retained file census')
        expected[name] = row
    seen = set()
    for path in root.rglob('*'):
        api.no_symlinks(path)
        api.require(path.is_file() or path.is_dir(), 'Nonregular retained P1 evidence')
        if path.is_file(): seen.add(path.relative_to(root).as_posix())
    api.require(seen == set(expected), 'P1 retained files missing or added')
    for name, row in expected.items():
        data = api.path_in(root, name).read_bytes()
        api.require(len(data) == row['bytes'] and api.sha(data) == row['sha256'], 'P1 retained bytes changed: ' + name)
    return api.canonical(rows)


def p1_tail_check_tools(api, tools):
    api.require(set(tools) == {'lean', 'python-source', 'mathlib'}, 'P1 tail needs exact explicit Lean, source Python and Mathlib paths')
    resolved = {}
    for name, sha256, size in [('lean', api.LEAN_SHA, None), ('python-source', p1_tail_meta['source_python']['sha256'], p1_tail_meta['source_python']['bytes'])]:
        path = api.no_symlinks(tools[name]).absolute()
        if not path.is_file(): raise api.MissingTool('P1 continuation tool is unavailable: ' + name)
        data = path.read_bytes()
        api.require(api.sha(data) == sha256 and (size is None or len(data) == size), 'P1 tail executable fingerprint differs: ' + name)
        resolved[name] = path
    resolved['mathlib'] = api.no_symlinks(tools['mathlib']).resolve()
    if not resolved['mathlib'].is_dir(): raise api.MissingTool('P1 continuation Mathlib root is missing')
    return {'paths': resolved, 'source_python': p1_tail_clone(p1_tail_meta['source_python']),
            'lean': {'version': '4.19.0', 'sha256': api.LEAN_SHA}}


def p1_tail_retain(api, suite, sources, root, inputs, tools):
    p1_tail_validate_suite(api, suite, sources, root)
    api.require(set(inputs) == {'p1-prior-receipt', 'p1-prior-command', 'p1-private-parameters'}, 'P1 retained input bindings differ')
    prior = p1_tail_meta['prior']
    receipt_path = api.no_symlinks(inputs['p1-prior-receipt']).resolve()
    command_path = api.no_symlinks(inputs['p1-prior-command']).resolve()
    api.require(receipt_path.name == 'RECEIPT.json' and command_path.name == 'COMMAND.json', 'P1 retained record names differ')
    api.require(api.sha(receipt_path.read_bytes()) == prior['receipt_sha256'], 'P1 failed receipt bytes changed')
    api.require(api.sha(command_path.read_bytes()) == prior['command_sha256'], 'P1 original command bytes changed')
    run = receipt_path.parent
    api.require(p1_tail_verify_custody(api, run, prior['run_files']) == prior['run_custody_sha256'], 'P1 retained run census changed')
    api.require(p1_tail_verify_custody(api, command_path.parent, prior['command_files']) == prior['command_custody_sha256'], 'P1 retained command census changed')
    receipt = api.read_json(receipt_path); command = api.read_json(command_path)
    api.require(api.canonical(receipt) == prior['receipt_canonical_sha256'], 'P1 failed receipt content differs')
    p1_validate_receipt(api, receipt, p1_tail_meta['original_physical_suite'], sources, root)
    api.require(receipt['outcome'] == 'FAILED' and receipt['proof_scope'] == 'NONE' and receipt['exit_code'] == 1, 'P1 old failure was promoted')
    api.require(command['terminal'] == 'COMPLETED' and command['exit_code'] == 1 and command['formal_slots'] == 1,
                'P1 retained original command terminal differs')
    api.require(command['log_sha256'] == api.sha((command_path.parent / 'combined.log').read_bytes()), 'P1 retained command/log join differs')
    ev = receipt['replay_evidence']; job = api.read_json(run / 'P1_RUNTIME_JOB.json'); runtime = api.read_json(run / 'P1_RUNTIME_PLAN.json')
    api.require(api.sha((run / 'P1_RUNTIME_JOB.json').read_bytes()) == prior['job_sha256'] == ev['job_sha256'], 'P1 original job changed')
    api.require(api.sha((run / 'P1_RUNTIME_PLAN.json').read_bytes()) == prior['runtime_plan_sha256'] == ev['runtime_plan_sha256'], 'P1 original plan changed')
    packet = run / 'archive' / p1_prefix.rstrip('/')
    api.require(job['source_root'] == str(packet) and job['original_output'] == str(run / 'original'), 'P1 retained output association differs')
    api.require(runtime['source_root'] == str(packet), 'P1 retained source root differs')
    tools_record = p1_tail_check_tools(api, tools); resolved = tools_record['paths']
    lean_root = resolved['lean'].resolve().parent.parent
    api.require(job['lean_root'] == str(lean_root) and job['mathlib'] == str(resolved['mathlib']), 'P1 retained imported environment differs')
    private_path = api.no_symlinks(inputs['p1-private-parameters'])
    values = api.read_json(private_path); pair = p1_private_parameters(api, values, lean_root)
    api.require(values == job['private_parameters'] and pair['public'] == ev['private_parameters'], 'P1 retained private parameter binding differs')
    api.require(p1_packet_expected(api, packet) == p1_meta['packet_expected'], 'P1 retained source packet differs')
    parent = {key: ev['stage_results'][0][key] for key in ('terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256')}
    physical = p1_collect(api, runtime, run / 'original', run / 'traces', parent, (run / 'logs/original.log').read_bytes())
    mapping = [(str(packet), '{archive:p1}'), (str(run), '{out}'), (job['lean_root'], '{tool:lean-root}'),
               (job['mathlib'], '{dependency:mathlib}'), (str(lean_root / 'bin/lean'), '{tool:lean}'), (job['python'], '{tool:python}')]
    api.require(p1_symbolize(api, physical, mapping) == ev['physical'], 'P1 actual original collector differs from the retained failure')
    children = physical['children']
    api.require([c['id'] for c in children] == prior['completed_prefix'] + [prior['failed_child']] and
                [c['outcome'] for c in children] == ['ACCEPT'] * 9 + ['REJECT'] * 4 + ['FAILED'], 'P1 retained child accounting differs')
    api.require(physical['not_run'] == prior['never_started'], 'P1 old never-started inventory changed')
    objects = []
    for want, child, event in zip(prior['objects'], children[:9], runtime['children'][:9]):
        path = api.path_in(run, want['path']); source = api.path_in(run, want['source_path'])
        api.require(want['module'] == child['id'] and str(path) == event['object_path'] and str(source) == event['source_path'], 'P1 retained object/source association differs')
        api.require(api.sha(path.read_bytes()) == child['object_sha256'] == want['sha256'] and path.stat().st_size == want['bytes'], 'P1 retained object changed')
        api.require(api.sha(source.read_bytes()) == event['source_sha256'] == want['source_sha256'], 'P1 retained source changed')
        api.require(child['capture_sha256'] == want['capture_sha256'] and child['capture']['output_hashes'] == {str(path): want['sha256']}, 'P1 retained object/capture join differs')
        objects.append(p1_tail_clone(want))
    api.require(len(objects) == 9 and not ev['target_audits'] and ev['views'] is None, 'P1 retained audit or view history differs')
    return {'receipt': receipt, 'physical': physical, 'objects': objects, 'run': run, 'packet': packet, 'runtime': runtime,
        'tools': tools_record, 'private': pair, 'private_path': private_path, 'lean_root': lean_root,
        'retained_public': p1_tail_clone(p1_tail_meta['retained_public'])}


def p1_tail_finite(api, root, out, texts):
    # Source-owned original census; only the separately versioned runtime pin changes.
    api.require(set(texts) == set(p1_finite_names), 'P1 tail finite child coverage incomplete')
    def original(name):
        data = api.path_in(root, name).read_bytes()
        api.require(api.sha(data) == p1_meta['members'][name]['sha256'], 'P1 tail finite source/reference changed')
        return data
    shape = p1_json(api, texts['SourceShape'])
    api.require(api.canonical(shape) == api.canonical(p1_json(api, original('acceptance/author/SOURCE_SHAPE_RESULT.json'))), 'P1 tail source-shape census/limits changed')
    edges = p1_json(api, texts['PythonEdges'])
    api.require(api.canonical(edges) == api.canonical(p1_json(api, original('acceptance/author/PYTHON_EDGE_CONTROLS.json'))), 'P1 tail bounded Python edge cases changed')
    api.require(re.fullmatch(r'\.\.\n-+\nRan 2 tests in [0-9.]+s\n\nOK\n', texts['SourceContract'].replace('\r\n', '\n')), 'P1 tail source contract tests incomplete')
    source = original('source/prcodec.py'); script = original('reviewer/independent_source_controls.py')
    obs_path = api.path_in(out, p1_finite_rel); obs = api.read_json(obs_path)
    reference = p1_json(api, original('acceptance/evidence/INDEPENDENT_SOURCE_CONTROLS.json'))
    api.keys(obs, set(reference))
    api.require(obs['source_sha256'] == p1_source and obs['independent_literal_copy_sha256'] == p1_source and obs['script_sha256'] == api.sha(script), 'P1 tail finite literal/driver identity differs')
    for key in ('status', 'differential_cases', 'outcome_counts', 'seeded_boundary_cases', 'observed_source_lines', 'source_ast_bindings', 'limits'):
        api.require(api.canonical(obs[key]) == api.canonical(reference[key]), 'P1 tail finite census or scope changed: ' + key)
    api.require(isinstance(obs['python_version'], str) and obs['python_version'].startswith('3.12.3 '), 'P1 tail finite interpreter differs')
    api.require(isinstance(obs['created_utc'], str) and re.fullmatch(r'\d{4}-\d\d-\d\dT[0-9:.]+(?:Z|\+00:00)', obs['created_utc']), 'P1 tail finite time missing')
    tree = ast.parse(script.decode()); assignments = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'mutations' for t in n.targets)]
    api.require(len(assignments) == 1, 'P1 tail mutation table missing'); cases = ast.literal_eval(assignments[0].value)
    api.require(len(cases) == len(obs['mutation_controls']) == 18, 'P1 tail internal comparison census differs')
    mutation_hashes = []
    for (name, before, after, case), row in zip(cases, obs['mutation_controls']):
        api.keys(row, {'name', 'case', 'original', 'mutant', 'changed_source_sha256', 'detected'})
        api.require(row['name'] == name and api.canonical(row['case']) == api.canonical(case), 'P1 tail finite witness changed')
        text = source.decode(); api.require(text.count(before) == 1, 'P1 tail mutation source anchor differs')
        api.require(row['changed_source_sha256'] == api.sha(text.replace(before, after).encode()), 'P1 tail internal mutant bytes differ')
        api.require(row['detected'] is True and api.canonical(row['original']) != api.canonical(row['mutant']), 'P1 tail internal mutation undetected')
        for value in (row['original'], row['mutant']):
            api.require(isinstance(value, list) and len(value) in (3, 4) and value[0] in ('ok', 'err') and type(value[-1]) is int and value[-1] >= 0, 'Malformed P1 tail model observation')
        mutation_hashes.append(api.canonical(row))
    outside = obs['outside_domain_observations']; old_outside = reference['outside_domain_observations']
    api.require(isinstance(outside, list) and len(outside) == 11 and [x['input_repr'] for x in outside] == [x['input_repr'] for x in old_outside], 'P1 tail excluded-domain census changed')
    for row in outside:
        api.keys(row, {'input_repr', 'observation'}); api.require(isinstance(row['observation'], list) and row['observation'][0] in ('ok', 'err'), 'Invalid P1 tail excluded-domain observation')
    summary, sep, tail = texts['IndependentPythonControls'].rpartition('\nDetected mutations: ')
    api.require(sep and tail == '18\n', 'P1 tail internal mutation summary differs')
    keys = ['status', 'differential_cases', 'outcome_counts', 'seeded_boundary_cases', 'source_ast_bindings']
    api.require(api.canonical(p1_json(api, summary)) == api.canonical({k: obs[k] for k in keys}), 'P1 tail finite stdout/file join differs')
    return {'source_shape': 'IDENTITY_ONLY', 'source_contract_tests': 2, 'source_text_mutations': 5, 'edge_cases': 26,
        'edge_outside_domain': 4, 'differential_cases': 266760, 'seeded_boundary_cases': 1593,
        'internal_mutations': 18, 'internal_mutation_record_sha256': mutation_hashes, 'outside_domain': 11,
        'finite_receipt_sha256': api.sha(obs_path.read_bytes()), 'rejecting_subprocesses': 0, 'scope': 'FINITE_ONLY', 'scope_ceiling': p1_ceiling}


def p1_tail_runtime(api, context, output, *, existing=False):
    output = api.no_symlinks(output).resolve()
    api.require(existing or not output.exists(), 'P1 tail output must be absent')
    packet = context['packet']; lean_root = context['lean_root']; tools = context['tools']['paths']
    copies = {p1_copy_control: api.path_in(packet, 'reviewer/independent_source_controls.py').read_bytes(),
              **{name: api.path_in(packet, 'source/prcodec.py').read_bytes() for name in p1_copy_codecs}}
    cache = api.read_json(packet / 'dependencies/MATHLIB_CACHE_PIN.json')
    roots = cache['roots']
    expected = ['.lake/build/lib/lean'] + ['.lake/packages/' + name + '/.lake/build/lib/lean' for name in ['LeanSearchClient', 'Qq', 'aesop', 'batteries', 'importGraph', 'plausible', 'proofwidgets']]
    api.require(roots == expected, 'P1 tail declared eight-library order changed')
    lean_path = os.pathsep.join([str(context['run'] / 'original/build')] + [str(api.path_in(tools['mathlib'], name)) for name in roots])
    env = {k: v for k, v in api._clean_environment().items() if not k.startswith(('LEAN', 'LD_'))}
    env.update(LEAN_PATH=lean_path, PYTHONDONTWRITEBYTECODE='1', PATH=str(lean_root / 'bin') + os.pathsep + env.get('PATH', ''))
    descriptor = p1_tail_descriptor(api)['replay']; events = []
    replacements = [[str(packet), '$PACKET'], [str(output / 'original'), '$OUTPUT'], [str(lean_root), '$LEAN_ROOT'],
                    [str(tools['mathlib']), '$MATHLIB_ROOT'], [str(tools['python-source']), '$PYTHON']]
    for contract in descriptor['tail']:
        source = output / 'original' / p1_copy_control if contract['id'] == 'IndependentPythonControls' else packet / contract['owner_path']
        events.append({'id': contract['id'], 'index': contract['index'], 'argv': [str(tools['python-source']), '-B', str(source)],
            'cwd': str(output / 'original'), 'source_path': str(source), 'source_sha256': contract['source_binding']['source_sha256'],
            'source_binding': contract['source_binding'], 'timeout_seconds': 180, 'symbolic_argv': contract['argv'],
            'required_copies': {str(output / 'original' / name): api.sha(data) for name, data in copies.items()} if contract['id'] == 'IndependentPythonControls' else {}})
    mapping = [(str(packet), '{retained:packet}'), (str(context['run']), '{retained:run}'), (str(output), '{out}'),
        (str(lean_root), '{tool:lean-root}'), (str(tools['mathlib']), '{dependency:mathlib}'),
        (str(tools['lean']), '{tool:lean}'), (str(tools['python-source']), '{tool:python-source}')]
    return {'events': events, 'env': env, 'environment_sha256': api.canonical(env), 'copies': copies,
        'replacements': replacements, 'mapping': mapping, 'audit_source': p1_audit_source(api, descriptor['audit_targets']),
        'input_binding_sha256': api.canonical({'prior': context['retained_public'], 'source_python': p1_tail_meta['source_python'], 'descriptor': descriptor}),
        'output': output, 'packet': packet, 'retained_run': context['run']}


def p1_tail_outcome(api, result, raw):
    api.require(result['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED', 'MISSING'}, 'Unknown P1 tail terminal')
    api.require((result['terminal'] == 'COMPLETED' and type(result['exit_code']) is int and 0 <= result['exit_code'] < 124) or
                (result['terminal'] != 'COMPLETED' and result['exit_code'] is None), 'Invalid P1 tail terminal/exit')
    if result['terminal'] != 'COMPLETED' or p1_resource.search(raw.decode('utf8', errors='replace')):
        return 'RESOURCE_INCONCLUSIVE'
    return 'ACCEPT' if result['exit_code'] == 0 and not p1_infrastructure.search(raw.decode('utf8', errors='replace')) else 'FAILED'


def p1_tail_implementation(api):
    return {'runner_sha256': api.sha(Path(api.__file__).read_bytes()), 'assets': p1_tail_clone(p1_tail_asset_pins)}


def p1_tail_initial(api, suite, sources, reviews):
    receipt = p1_initial_receipt(api, suite, sources, reviews)
    receipt['replay_evidence'] = {'schema': p1_tail_meta['evidence_schema'], 'recipe': p1_tail_meta['recipe'], 'mode': suite['replay']['mode'],
        'descriptor_sha256': api.canonical(suite['replay']), 'implementation': p1_tail_implementation(api),
        'source_hashes_before': dict(receipt['source_hashes']), 'source_hashes_after': dict(receipt['source_hashes']),
        'retained': None, 'source_python': p1_tail_clone(p1_tail_meta['source_python']), 'private_parameters': None,
        'dependency_checks_before': None, 'dependency_checks_after': None, 'runtime_sha256': None, 'stage_results': [],
        'copies': {}, 'finite': None, 'target_audits': [], 'audit_source_sha256': None, 'output_custody_sha256': None,
        'retained_builds': 0, 'new_builds': 0, 'new_wrapper_runs': 0, 'new_finite_processes': 0, 'new_audit_processes': 0,
        'independent_evidence_increment': 0, 'post_verified': False, 'scope_ceiling': p1_ceiling}
    return receipt


def p1_tail_capture(api, runtime, event, result, raw):
    api.keys(result, {'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256'})
    api.require(result['log_sha256'] == api.sha(raw), 'P1 tail process/raw log identity differs')
    p1_tail_outcome(api, result, raw)
    p1_time(api, result['started_at']); p1_time(api, result['ended_at'])
    api.require(result['started_at'] <= result['ended_at'], 'P1 tail capture interval reversed')
    api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 tail source changed during child')
    for name, digest in event['required_copies'].items():
        api.require(api.sha(api.no_symlinks(name).read_bytes()) == digest, 'P1 tail output copy changed')
    outputs = {}
    if event['id'] == 'IndependentPythonControls':
        path = runtime['output'] / 'original' / p1_finite_rel
        if path.exists(): outputs[str(path)] = api.sha(api.no_symlinks(path).read_bytes())
    derived = p1_neutralize(api, raw, runtime['replacements'], result['terminal'] == 'TIMEOUT')
    neutral = runtime['output'] / 'original/logs' / (event['id'] + '.log')
    neutral.parent.mkdir(parents=True, exist_ok=True); neutral.write_bytes(derived['derived_bytes'])
    return {'id': event['id'], 'index': event['index'], **result, 'argv': event['argv'], 'cwd': event['cwd'],
        'source_sha256': event['source_sha256'], 'source_binding': event['source_binding'], 'environment_sha256': runtime['environment_sha256'],
        'input_binding_sha256': runtime['input_binding_sha256'], 'required_copies': event['required_copies'], 'output_hashes': outputs,
        'derivation': {k: v for k, v in derived.items() if k != 'derived_bytes'}}


def p1_tail_partial_semantics(api, packet, name, texts):
    if name in {'SourceShape', 'PythonEdges'}:
        path = 'acceptance/author/' + ('SOURCE_SHAPE_RESULT.json' if name == 'SourceShape' else 'PYTHON_EDGE_CONTROLS.json')
        api.require(api.canonical(p1_json(api, texts[name])) == api.canonical(p1_json(api, api.path_in(packet, path).read_bytes())), 'P1 tail finite source census differs')
    if name == 'SourceContract':
        api.require(re.fullmatch(r'\.\.\n-+\nRan 2 tests in [0-9.]+s\n\nOK\n', texts[name].replace('\r\n', '\n')), 'P1 tail two original source-contract tests did not pass')


def p1_tail_collect(api, runtime):
    output = runtime['output']; trace = api.no_symlinks(output / 'traces')
    captures = sorted(p for p in trace.glob('*.json') if p.name != 'audit.json')
    api.require(len(captures) <= 4 and [p.name for p in captures] == [f'{i:04}.json' for i in range(len(captures))], 'P1 tail capture inventory/order differs')
    api.require({p.name for p in trace.iterdir()} <= {f'{i:04}{suffix}' for i in range(len(captures)) for suffix in ('.json', '.log')} | {'audit.json', 'audit.log'}, 'Unexpected P1 tail trace artifact')
    stages = []; texts = {}; finite = None; previous = p1_tail_meta['retained_public']['ended_at']; stopped = False
    for index, path in enumerate(captures):
        api.require(not stopped, 'P1 tail ran after a failed/resource child')
        cap = api.read_json(api.no_symlinks(path)); event = runtime['events'][index]
        api.keys(cap, {'id', 'index', 'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256', 'argv', 'cwd', 'source_sha256',
            'source_binding', 'environment_sha256', 'input_binding_sha256', 'required_copies', 'output_hashes', 'derivation'})
        for key in ('id', 'index', 'argv', 'cwd', 'source_sha256', 'source_binding', 'required_copies'):
            api.require(cap[key] == event[key], 'P1 tail actual command/source contract differs: ' + key)
        api.require(cap['environment_sha256'] == runtime['environment_sha256'] and cap['input_binding_sha256'] == runtime['input_binding_sha256'], 'P1 tail environment/input association differs')
        p1_time(api, cap['started_at']); p1_time(api, cap['ended_at'])
        api.require(previous <= cap['started_at'] <= cap['ended_at'], 'P1 tail children overlap or precede retained work'); previous = cap['ended_at']
        raw = api.no_symlinks(path.with_suffix('.log')).read_bytes()
        api.require(api.sha(raw) == cap['log_sha256'], 'P1 tail raw log changed')
        neutral = api.no_symlinks(output / 'original/logs' / (event['id'] + '.log')).read_bytes()
        derivation = p1_neutralize(api, raw, runtime['replacements'], cap['terminal'] == 'TIMEOUT')
        api.require(derivation['derived_bytes'] == neutral and cap['derivation'] == {k: v for k, v in derivation.items() if k != 'derived_bytes'}, 'P1 tail exact raw/neutral derivation differs')
        api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 tail input bytes changed')
        for name, digest in cap['required_copies'].items(): api.require(api.sha(api.no_symlinks(name).read_bytes()) == digest, 'P1 tail copy custody changed')
        wanted_outputs = {}
        if event['id'] == 'IndependentPythonControls' and (output / 'original' / p1_finite_rel).exists():
            wanted_outputs[str(output / 'original' / p1_finite_rel)] = api.sha(api.no_symlinks(output / 'original' / p1_finite_rel).read_bytes())
        api.require(cap['output_hashes'] == wanted_outputs, 'P1 finite report output/capture join differs')
        outcome = p1_tail_outcome(api, cap, raw)
        if outcome == 'ACCEPT':
            texts[event['id']] = neutral.decode('utf8')
            try:
                p1_tail_partial_semantics(api, runtime['packet'], event['id'], texts)
                if index == 3:
                    finite = p1_tail_finite(api, runtime['packet'], output / 'original', texts)
                    created = api.read_json(output / 'original' / p1_finite_rel)['created_utc']
                    from datetime import datetime
                    stamp = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    api.require(p1_time(api, cap['started_at']) <= stamp <= p1_time(api, cap['ended_at']), 'P1 finite report is outside its actual child interval')
            except (ValueError, KeyError, TypeError, UnicodeError):
                outcome = 'FAILED'; finite = None
        stopped = outcome != 'ACCEPT'
        public = p1_symbolize(api, cap, runtime['mapping'])
        stages.append({**public, 'outcome': outcome, 'capture_sha256': api.sha(path.read_bytes()),
            'timeout_seconds': 180, 'rejecting_subprocesses': 0})
    copies = {}
    for name, data in runtime['copies'].items():
        api.require(api.path_in(output / 'original', name).read_bytes() == data, 'P1 continuation copy changed')
        copies[name] = api.sha(data)
    outcome = stages[-1]['outcome'] if stopped else 'COMPLETE' if len(stages) == 4 and finite is not None else 'INCOMPLETE'
    return {'stage_results': stages, 'finite': finite, 'copies': copies, 'outcome': outcome}


def p1_tail_audit_capture(api, runtime, result):
    output = runtime['output']; raw = api.no_symlinks(output / 'traces/audit.log').read_bytes()
    api.require(result['log_sha256'] == api.sha(raw), 'P1 tail audit raw log changed')
    outcome = p1_tail_outcome(api, result, raw)
    targets = p1_tail_meta['original_physical_suite']['replay']['audit_targets']; audits = []
    if outcome == 'ACCEPT':
        try:
            values = api.parse_readbacks(raw.decode(), targets)
            audits = [{'target_id': tid, **value, 'log_sha256': result['log_sha256']} for tid, value in values.items()]
        except (ValueError, UnicodeError): outcome = 'FAILED'
    row = {'id': '_target_audit', 'index': 4, **result, 'argv': ['{tool:lean}', '-j1', '{out}/generated/P1TailCheckedReadback.lean'],
        'cwd': '{retained:packet}', 'source_sha256': api.sha(runtime['audit_source'].encode()), 'environment_sha256': runtime['environment_sha256'],
        'input_binding_sha256': runtime['input_binding_sha256'], 'timeout_seconds': 300, 'outcome': outcome, 'rejecting_subprocesses': 0,
        'retained_object_set_sha256': api.canonical(p1_tail_meta['prior']['objects'])}
    return row, audits


def p1_tail_controls(api, suite, ev):
    by_name = {c['id']: {'outcome': c['outcome'], **c['capture']} for c in ev['retained']['physical_children'][:13]}
    by_name.update({r['id']: r for r in ev['stage_results'][:4]})
    rows = []
    for control in suite['controls']:
        child = by_name[control['id'][3:]]
        rows.append({k: control[k] for k in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
            'actual_outcome': child['outcome'], 'actual_outcome_sha256': api.sha(child['outcome'].encode()),
            'terminal': child['terminal'], 'exit_code': child['exit_code'], 'log_sha256': child['log_sha256']})
    return rows


def p1_tail_output_rows(api, output):
    allowed = {'SUITE.json', 'RUNTIME.json', 'FAILURE.json', 'generated/P1TailCheckedReadback.lean', 'traces/audit.json', 'traces/audit.log',
        'original/' + p1_finite_rel} | {'original/' + name for name in [p1_copy_control, *p1_copy_codecs]} | {
        'original/logs/' + name + '.log' for name in p1_finite_names} | {'traces/' + f'{i:04}' + suffix for i in range(4) for suffix in ('.json', '.log')}
    rows = []
    for path in sorted(output.rglob('*')):
        api.no_symlinks(path)
        api.require(path.is_dir() or path.is_file(), 'P1 tail output contains nonregular evidence')
        if path.is_file() and path.relative_to(output).as_posix() not in {'RECEIPT.json', 'OUTPUT_CUSTODY.json'}:
            api.require(path.relative_to(output).as_posix() in allowed, 'P1 tail has an unprescribed output file')
            api.require(path.suffix not in {'.olean', '.ilean', '.pyc'}, 'P1 tail must not produce or copy Lean objects or Python cache')
            data = path.read_bytes(); rows.append({'path': path.relative_to(output).as_posix(), 'sha256': api.sha(data), 'bytes': len(data)})
    return rows


def p1_tail_execute_suite(api, suite, sources, root, output, tools, inputs, scope=None, reviews=None):
    plan = p1_tail_validate_suite(api, suite, sources, root)
    api.require(scope is None or scope == plan['scope'], 'P1 tail execution scope differs')
    api.require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'P1 tail scientific reviews are missing')
    output = api.no_symlinks(output).resolve(); api.require(not output.exists(), 'P1 continuation output must be absent')
    for path in [root, *tools.values(), *inputs.values()]:
        resolved = Path(path).resolve(); api.require(not output.is_relative_to(resolved) and not resolved.is_relative_to(output), 'P1 tail output overlaps input')
    for name in ('p1-prior-receipt', 'p1-prior-command', 'p1-tail-receipt'):
        if name in inputs:
            retained_root = Path(inputs[name]).resolve().parent
            api.require(not output.is_relative_to(retained_root) and not retained_root.is_relative_to(output), 'P1 tail output overlaps retained evidence root')
    if plan['mode'] == 'FINITE_VIEW': return p1_tail_join_finite(api, suite, sources, root, output, tools, inputs, reviews)
    # Source execution remains on 3.12; this orchestration must stay on the reviewed 3.11.9.
    import sys
    api.require(sys.version_info[:3] == (3, 11, 9) and api.sha(Path(sys.executable).read_bytes()) == p1_tail_meta['orchestration_python']['sha256'], 'P1 tail orchestration interpreter changed')
    context = p1_tail_retain(api, suite, sources, root, inputs, tools)
    runtime = p1_tail_runtime(api, context, output)
    dependencies = p1_verify_dependencies(api, context['packet'], context['lean_root'], context['tools']['paths']['mathlib'], context['private'])
    api.require(dependencies == context['receipt']['replay_evidence']['dependency_checks'], 'P1 retained transitive compiler/source/cache closure changed')
    output.mkdir(parents=True); (output / 'traces').mkdir(); (output / 'original').mkdir()
    api.write_json(output / 'SUITE.json', suite)
    record = {'events': runtime['events'], 'environment_sha256': runtime['environment_sha256'], 'input_binding_sha256': runtime['input_binding_sha256'],
        'replacements': runtime['replacements'], 'audit_source_sha256': api.sha(runtime['audit_source'].encode()),
        'retained_receipt_sha256': p1_tail_meta['prior']['receipt_sha256']}
    api.write_json(output / 'RUNTIME.json', record)
    for name, data in runtime['copies'].items():
        target = api.path_in(output / 'original', name); target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    receipt = p1_tail_initial(api, suite, sources, reviews); ev = receipt['replay_evidence']
    ev.update(retained=context['retained_public'], retained_builds=9, private_parameters=context['private']['public'],
        dependency_checks_before=dependencies, runtime_sha256=api.sha((output / 'RUNTIME.json').read_bytes()))
    p1_save_receipt(api, receipt, output)
    try:
        for event in runtime['events']:
            api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 tail source changed before child')
            log = output / 'traces' / (f"{event['index']:04}.log")
            result = api.run_process(event['argv'], Path(event['cwd']), runtime['env'], log, 180)
            capture = p1_tail_capture(api, runtime, event, result, log.read_bytes())
            api.write_json(log.with_suffix('.json'), capture)
            collected = p1_tail_collect(api, runtime)
            ev['stage_results'] = p1_tail_clone(collected['stage_results']); ev['copies'] = collected['copies']; ev['finite'] = collected['finite']
            ev['new_finite_processes'] = sum(c['terminal'] != 'MISSING' for c in ev['stage_results'])
            if collected['outcome'] in {'FAILED', 'RESOURCE_INCONCLUSIVE'}:
                receipt['outcome'] = collected['outcome']; raise ValueError('P1 tail child did not meet its complete source contract')
            p1_save_receipt(api, receipt, output)
        api.require(collected['outcome'] == 'COMPLETE', 'P1 tail finite census incomplete')
        generated = output / 'generated'; generated.mkdir()
        audit = generated / 'P1TailCheckedReadback.lean'; audit.write_text(runtime['audit_source'], encoding='utf8')
        ev['audit_source_sha256'] = api.sha(audit.read_bytes())
        result = api.run_process([context['tools']['paths']['lean'], '-j1', audit], context['packet'], runtime['env'], output / 'traces/audit.log', 300)
        api.write_json(output / 'traces/audit.json', result)
        audit_row, target_audits = p1_tail_audit_capture(api, runtime, result)
        ev['stage_results'].append(audit_row); ev['new_audit_processes'] = int(result['terminal'] != 'MISSING'); ev['target_audits'] = target_audits
        if audit_row['outcome'] != 'ACCEPT':
            receipt['outcome'] = audit_row['outcome']; raise ValueError('P1 continuation safe target audit did not complete')
        api.require(api.path_in(output, 'generated/P1TailCheckedReadback.lean').read_bytes() == runtime['audit_source'].encode(), 'P1 generated audit source changed')
        again = p1_tail_retain(api, suite, sources, root, inputs, tools)
        api.require(again['retained_public'] == context['retained_public'], 'P1 retained custody changed during continuation')
        post = p1_verify_dependencies(api, context['packet'], context['lean_root'], context['tools']['paths']['mathlib'], context['private'])
        api.require(post == dependencies, 'P1 transitive imported closure changed during continuation')
        ev['dependency_checks_after'] = post
        repeated = p1_tail_collect(api, runtime)
        api.require(repeated == collected, 'P1 tail source/capture/finite evidence changed during audit')
        p1_tail_check_tools(api, tools)
        for row in plan['files']:
            api.require(api.public_bytes(root, sources[row['source_id']]) == plan['contents'][row['path']], 'P1 published source changed during continuation')
        ev['post_verified'] = True
        receipt['controls'] = p1_tail_controls(api, suite, ev)
        receipt['target_readbacks'] = [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']]
        receipt['axioms'] = sorted({a for row in target_audits for a in row['axioms']})
        receipt.update(outcome='FRESH_KERNEL_COMPONENTS', proof_scope='COMPONENTS', exit_code=0)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError, KeyboardInterrupt) as error:
        api.write_json(output / 'FAILURE.json', {'kind': type(error).__name__, 'message': str(error), 'scope': 'PRIVATE_DIAGNOSTIC'})
        if receipt['outcome'] != 'RESOURCE_INCONCLUSIVE': receipt['outcome'] = 'RESOURCE_INCONCLUSIVE' if isinstance(error, KeyboardInterrupt) else 'FAILED'
        receipt.update(proof_scope='NONE', exit_code=1, controls=[], target_readbacks=[], axioms=[])
    rows = p1_tail_output_rows(api, output); api.write_json(output / 'OUTPUT_CUSTODY.json', rows)
    ev['output_custody_sha256'] = api.sha((output / 'OUTPUT_CUSTODY.json').read_bytes())
    p1_save_receipt(api, receipt, output)
    p1_tail_validate_receipt(api, receipt, suite, sources, root)
    return receipt


def p1_tail_validate_derivation(api, value, raw_sha, timed_out):
    api.keys(value, {'source_sha256', 'derived_sha256', 'replacements', 'utf8_decode_errors', 'source_owned_timeout_suffix', 'science_bytes_changed'})
    api.require(value['source_sha256'] == raw_sha and value['source_owned_timeout_suffix'] is timed_out and value['science_bytes_changed'] is False and
        value['utf8_decode_errors'] == ('replace' if timed_out else 'strict'), 'P1 tail raw/neutral interpretation differs')
    api.digest(value['derived_sha256'])
    rows = value['replacements']; api.require(isinstance(rows, list) and len(rows) == 5 and {r['replacement'] for r in rows} == {'$PACKET', '$OUTPUT', '$LEAN_ROOT', '$MATHLIB_ROOT', '$PYTHON'}, 'P1 tail neutralization map differs')
    previous = None
    for row in rows:
        api.keys(row, {'source_string_sha256', 'replacement', 'count', 'before_sha256', 'after_sha256'})
        for field in ('source_string_sha256', 'before_sha256', 'after_sha256'): api.digest(row[field])
        api.require(type(row['count']) is int and row['count'] >= 0, 'P1 tail replacement count differs')
        if previous is not None: api.require(previous == row['before_sha256'], 'P1 tail neutralization chain differs')
        if row['count'] == 0: api.require(row['before_sha256'] == row['after_sha256'], 'P1 tail zero-count substitution changed bytes')
        previous = row['after_sha256']
    if not timed_out:
        api.require(rows[0]['before_sha256'] == raw_sha and previous == value['derived_sha256'], 'P1 tail raw/neutral hash chain differs')


def p1_tail_validate_finite(api, finite):
    api.keys(finite, {'source_shape', 'source_contract_tests', 'source_text_mutations', 'edge_cases', 'edge_outside_domain', 'differential_cases',
        'seeded_boundary_cases', 'internal_mutations', 'internal_mutation_record_sha256', 'outside_domain', 'finite_receipt_sha256', 'rejecting_subprocesses', 'scope', 'scope_ceiling'})
    api.require(finite['source_shape'] == 'IDENTITY_ONLY' and finite['scope'] == 'FINITE_ONLY' and finite['scope_ceiling'] == p1_ceiling, 'P1 tail finite scope inflated')
    for key, value in {'source_contract_tests': 2, 'source_text_mutations': 5, 'edge_cases': 26, 'edge_outside_domain': 4,
        'differential_cases': 266760, 'seeded_boundary_cases': 1593, 'internal_mutations': 18, 'outside_domain': 11, 'rejecting_subprocesses': 0}.items():
        api.require(type(finite[key]) is int and finite[key] == value, 'P1 tail finite census differs: ' + key)
    api.require(isinstance(finite['internal_mutation_record_sha256'], list) and len(finite['internal_mutation_record_sha256']) == 18, 'P1 tail internal comparison records incomplete')
    for digest in finite['internal_mutation_record_sha256']: api.digest(digest)
    api.digest(finite['finite_receipt_sha256'])


def p1_tail_validate_common(api, receipt, suite, sources):
    api.keys(receipt, {'id', 'suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256', 'outcome',
        'target_readbacks', 'controls', 'stages', 'invocation', 'started_at', 'ended_at', 'exit_code', 'log_sha256', 'axioms', 'proof_scope', 'replay_evidence'})
    api.require(receipt['id'] == suite['id'] + '-replay' and receipt['suite_id'] == suite['id'] and receipt['family'] == suite['family'] and
        receipt['suite_sha256'] == api.canonical(suite) and receipt['toolchain_sha256'] == api.canonical(suite['toolchain']), 'P1 continuation suite identity differs')
    api.require(receipt['source_hashes'] == p1_projection_hashes(api, suite, sources), 'P1 tail source identity differs')
    api.require(receipt['review_hashes'] == {name: p1_tail_meta['review_hashes'][name] for name in suite['review_ids']}, 'P1 tail exact inherited scientific reviews differ')
    for value in receipt['review_hashes'].values(): api.digest(value)
    p1_time(api, receipt['started_at']); p1_time(api, receipt['ended_at'])
    api.require(receipt['started_at'] <= receipt['ended_at'] and receipt['invocation'] == ['replay_v5_successors.py', '--execute', '--suite', suite['id'], '--out', '{out}'], 'P1 tail invocation/interval differs')
    ev = receipt['replay_evidence']
    api.require(ev['schema'] == p1_tail_meta['evidence_schema'] and ev['recipe'] == p1_tail_meta['recipe'] and ev['mode'] == suite['replay']['mode'] and
        ev['descriptor_sha256'] == api.canonical(suite['replay']), 'P1 continuation family binding differs')
    implementation = ev['implementation']; api.keys(implementation, {'runner_sha256', 'assets'})
    # Compatibility additions are code-owned in the main adapter, outside these immutable assets.
    accepted = {p1_tail_implementation(api)['runner_sha256']: p1_tail_clone(p1_tail_asset_pins)}
    accepted.update(getattr(api, 'p1_tail_accepted_predecessors', {}))
    api.require(implementation['runner_sha256'] in accepted and implementation['assets'] == accepted[implementation['runner_sha256']], 'P1 tail implementation is not an admitted immutable version')
    api.require(receipt['stages'] == [{k: r[k] for k in ('id', 'terminal', 'exit_code', 'log_sha256')} for r in ev['stage_results']] and
        receipt['log_sha256'] == api.canonical({r['id']: r['log_sha256'] for r in ev['stage_results']}), 'P1 tail public stage/log summary differs')


def p1_tail_validate_receipt(api, receipt, suite, sources, root):
    try:
        plan = p1_tail_validate_suite(api, suite, sources, root)
        p1_tail_validate_common(api, receipt, suite, sources)
        ev = receipt['replay_evidence']
        if plan['mode'] == 'FINITE_VIEW': return p1_tail_validate_view(api, receipt, suite, sources, root)
        api.keys(ev, {'schema', 'recipe', 'mode', 'descriptor_sha256', 'implementation', 'source_hashes_before', 'source_hashes_after', 'retained',
            'source_python', 'private_parameters', 'dependency_checks_before', 'dependency_checks_after', 'runtime_sha256', 'stage_results',
            'copies', 'finite', 'target_audits', 'audit_source_sha256', 'output_custody_sha256', 'retained_builds', 'new_builds', 'new_wrapper_runs',
            'new_finite_processes', 'new_audit_processes', 'independent_evidence_increment', 'post_verified', 'scope_ceiling'})
        api.require(ev['source_hashes_before'] == ev['source_hashes_after'] == receipt['source_hashes'] and ev['source_python'] == p1_tail_meta['source_python'], 'P1 tail source or interpreter binding differs')
        api.require(ev['scope_ceiling'] == p1_ceiling and type(ev['post_verified']) is bool, 'P1 tail scope/postcondition differs')
        for name in ('new_builds', 'new_wrapper_runs', 'independent_evidence_increment'):
            api.require(type(ev[name]) is int and ev[name] == 0, 'P1 continuation gained new producer/independence credit')
        api.require(ev['retained'] == p1_tail_meta['retained_public'] and type(ev['retained_builds']) is int and ev['retained_builds'] == 9, 'P1 original failed record or retained products changed')
        api.require(ev['private_parameters'] == ev['retained']['private_parameters'] and ev['dependency_checks_before'] == ev['retained']['dependency_checks'], 'P1 retained imported closure/private derivation differs')
        api.require(ev['dependency_checks_after'] is None or ev['dependency_checks_after'] == ev['dependency_checks_before'], 'P1 post-run compiler/source/cache inventory differs')
        api.digest(ev['runtime_sha256']); api.digest(ev['output_custody_sha256'])
        stages = ev['stage_results']; wanted = p1_finite_names + ['_target_audit']
        api.require(isinstance(stages, list) and len(stages) <= 5 and [r['id'] for r in stages] == wanted[:len(stages)], 'P1 tail ledger omitted, duplicated or reordered a stage')
        previous = receipt['started_at']; env_sha = None; failed = False
        input_sha = api.canonical({'prior': ev['retained'], 'source_python': p1_tail_meta['source_python'], 'descriptor': p1_tail_descriptor(api)['replay']})
        for index, row in enumerate(stages):
            api.require(not failed, 'P1 tail continued after a failed/resource stage')
            common = {'id', 'index', 'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256', 'argv', 'cwd', 'source_sha256',
                'environment_sha256', 'input_binding_sha256', 'timeout_seconds', 'outcome', 'rejecting_subprocesses'}
            api.keys(row, common | ({'source_binding', 'required_copies', 'output_hashes', 'derivation', 'capture_sha256'} if index < 4 else {'retained_object_set_sha256'}))
            api.require(type(row['index']) is int and row['index'] == index and type(row['rejecting_subprocesses']) is int and row['rejecting_subprocesses'] == 0, 'P1 tail index or subprocess-rejection credit changed')
            p1_time(api, row['started_at']); p1_time(api, row['ended_at'])
            api.require(previous <= row['started_at'] <= row['ended_at'] <= receipt['ended_at'], 'P1 tail stage interval/order differs'); previous = row['ended_at']
            api.require(ev['retained']['ended_at'] <= row['started_at'], 'P1 continuation precedes retained attempt')
            for field in ('log_sha256', 'source_sha256', 'environment_sha256', 'input_binding_sha256'): api.digest(row[field])
            if env_sha is None: env_sha = row['environment_sha256']
            api.require(row['environment_sha256'] == env_sha and row['input_binding_sha256'] == input_sha, 'P1 tail stages use different input/environment bindings')
            api.require(row['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED', 'MISSING'}, 'Unknown P1 tail terminal')
            api.require((row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and 0 <= row['exit_code'] < 124) or
                (row['terminal'] != 'COMPLETED' and row['exit_code'] is None), 'P1 tail terminal/exit mismatch')
            api.require(row['outcome'] in {'ACCEPT', 'FAILED', 'RESOURCE_INCONCLUSIVE'}, 'Unknown P1 tail outcome')
            if row['terminal'] != 'COMPLETED': api.require(row['outcome'] == 'RESOURCE_INCONCLUSIVE', 'P1 resource terminal gained success/rejection credit')
            if row['outcome'] == 'ACCEPT': api.require(row['terminal'] == 'COMPLETED' and row['exit_code'] == 0, 'P1 tail accepted without expected exit')
            if index < 4:
                contract = plan['tail'][index]
                api.require(row['argv'] == contract['argv'] and row['cwd'] == '{out}/original' and row['timeout_seconds'] == 180 and
                    row['source_sha256'] == contract['source_binding']['source_sha256'] and row['source_binding'] == contract['source_binding'], 'P1 tail source/argv/budget differs')
                copies = {'{out}/original/' + name: digest for name, digest in ev['copies'].items()} if index == 3 else {}
                api.require(row['required_copies'] == copies, 'P1 tail actual compatibility copies differ')
                api.digest(row['capture_sha256']); p1_tail_validate_derivation(api, row['derivation'], row['log_sha256'], row['terminal'] == 'TIMEOUT')
                api.require(set(row['output_hashes']) <= ({'{out}/original/' + p1_finite_rel} if index == 3 else set()), 'P1 tail child gained unapproved output')
                for h in row['output_hashes'].values(): api.digest(h)
            else:
                expected_source = api.sha(p1_audit_source(api, plan['audit_targets']).encode())
                api.require(row['argv'] == ['{tool:lean}', '-j1', '{out}/generated/P1TailCheckedReadback.lean'] and row['cwd'] == '{retained:packet}' and
                    row['timeout_seconds'] == 300 and row['source_sha256'] == ev['audit_source_sha256'] == expected_source and
                    row['retained_object_set_sha256'] == api.canonical(p1_tail_meta['prior']['objects']), 'P1 tail safe audit source/objects differ')
            failed = row['outcome'] != 'ACCEPT'
        api.require(type(ev['new_finite_processes']) is int and ev['new_finite_processes'] == sum(r['terminal'] != 'MISSING' for r in stages[:4]) and
            type(ev['new_audit_processes']) is int and ev['new_audit_processes'] == int(len(stages) == 5 and stages[-1]['terminal'] != 'MISSING'), 'P1 tail process accounting differs')
        expected_copies = {p1_copy_control: p1_meta['members']['reviewer/independent_source_controls.py']['sha256'], **{n: p1_source for n in p1_copy_codecs}}
        api.require(ev['copies'] == expected_copies or (not stages and ev['copies'] == {}), 'P1 tail exact output-only copy census differs')
        if ev['finite'] is not None:
            p1_tail_validate_finite(api, ev['finite'])
            api.require(len(stages) >= 4 and stages[3]['outcome'] == 'ACCEPT' and stages[3]['output_hashes'] == {'{out}/original/' + p1_finite_rel: ev['finite']['finite_receipt_sha256']}, 'P1 finite report is not bound to its completed child')
        if ev['target_audits']:
            api.require(len(stages) == 5 and stages[4]['outcome'] == 'ACCEPT' and len(ev['target_audits']) == 41, 'P1 tail safe audit incomplete')
            for row, target in zip(ev['target_audits'], plan['audit_targets']):
                api.keys(row, {'target_id', 'name', 'type_sha256', 'axioms', 'closure_status', 'checked_declarations', 'log_sha256'})
                api.require(row['target_id'] == target['target_id'] and row['name'] == target['name'] and row['log_sha256'] == stages[4]['log_sha256'], 'P1 target/source/audit association differs')
                api.require(row['closure_status'] == 'CHECKED_SAFE' and type(row['checked_declarations']) is int and row['checked_declarations'] > 0 and
                    isinstance(row['axioms'], list) and row['axioms'] == sorted(set(row['axioms'])) and set(row['axioms']) <= api.AXIOMS, 'P1 target closure or axiom footprint is unsafe')
                api.digest(row['type_sha256'])
        api.require(receipt['outcome'] in {'NOT_RUN', 'FAILED', 'RESOURCE_INCONCLUSIVE', 'FRESH_KERNEL_COMPONENTS'}, 'P1 tail outcome differs')
        if any(r['outcome'] == 'RESOURCE_INCONCLUSIVE' for r in stages): api.require(receipt['outcome'] == 'RESOURCE_INCONCLUSIVE', 'P1 tail resource outcome was suppressed')
        if receipt['outcome'] != 'FRESH_KERNEL_COMPONENTS':
            api.require(receipt['proof_scope'] == 'NONE' and receipt['exit_code'] in (None, 1) and receipt['controls'] == [] and receipt['target_readbacks'] == [] and receipt['axioms'] == [], 'P1 incomplete continuation gained qualification')
            return {'suite_id': suite['id'], 'outcome': receipt['outcome'], 'scope': 'P1_TAIL_FAILED_OR_PARTIAL_ONLY'}
        api.require(receipt['proof_scope'] == 'COMPONENTS' and type(receipt['exit_code']) is int and receipt['exit_code'] == 0 and
            len(stages) == 5 and all(s['outcome'] == 'ACCEPT' for s in stages) and ev['post_verified'] is True and
            ev['dependency_checks_after'] == ev['dependency_checks_before'] and ev['finite'] is not None and len(ev['target_audits']) == 41, 'P1 tail completion lacks all finite/audit/postconditions')
        api.require(receipt['controls'] == p1_tail_controls(api, suite, ev), 'P1 controls do not join retained versus new observations')
        api.require(receipt['target_readbacks'] == [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']], 'P1 target declaration bindings differ')
        api.require(receipt['axioms'] == sorted({a for row in ev['target_audits'] for a in row['axioms']}), 'P1 target axiom summary differs')
        return {'suite_id': suite['id'], 'outcome': receipt['outcome'], 'scope': 'RETAINED_P1_COMPONENTS_WITH_FRESH_FINITE_TAIL_AND_SAFE_AUDIT'}
    except (KeyError, TypeError, AttributeError, IndexError) as error:
        raise ValueError('Malformed P1 tail receipt: ' + str(error)) from error


def p1_tail_readback(api, suite, sources, root, output, tools, inputs):
    output = api.no_symlinks(output).resolve(); receipt = api.read_json(output / 'RECEIPT.json')
    p1_tail_validate_receipt(api, receipt, suite, sources, root)
    api.require(api.read_json(output / 'SUITE.json') == suite, 'P1 tail stored suite changed')
    ev = receipt['replay_evidence']; custody_path = output / 'OUTPUT_CUSTODY.json'
    api.require(api.sha(custody_path.read_bytes()) == ev['output_custody_sha256'] and api.read_json(custody_path) == p1_tail_output_rows(api, output), 'P1 tail output custody changed')
    context = p1_tail_retain(api, suite, sources, root, inputs, tools)
    runtime = p1_tail_runtime(api, context, output, existing=True)
    record = api.read_json(output / 'RUNTIME.json')
    api.require(api.sha((output / 'RUNTIME.json').read_bytes()) == ev['runtime_sha256'], 'P1 tail private runtime changed')
    api.keys(record, {'events', 'environment_sha256', 'input_binding_sha256', 'replacements', 'audit_source_sha256', 'retained_receipt_sha256'})
    api.require(record['events'] == runtime['events'] and record['input_binding_sha256'] == runtime['input_binding_sha256'] and
        record['replacements'] == runtime['replacements'] and record['audit_source_sha256'] == api.sha(runtime['audit_source'].encode()) and
        record['retained_receipt_sha256'] == p1_tail_meta['prior']['receipt_sha256'], 'P1 tail actual private source/argv association changed')
    # Ambient environment may change after execution; its captured digest remains custody-bound.
    api.digest(record['environment_sha256']); runtime['environment_sha256'] = record['environment_sha256']
    collected = p1_tail_collect(api, runtime)
    api.require(collected['stage_results'] == ev['stage_results'][:4] and collected['finite'] == ev['finite'] and collected['copies'] == ev['copies'], 'P1 tail whole capture/source/finite recollection differs')
    if len(ev['stage_results']) == 5:
        api.require((output / 'generated/P1TailCheckedReadback.lean').read_bytes() == runtime['audit_source'].encode(), 'P1 tail generated audit changed')
        row, audits = p1_tail_audit_capture(api, runtime, api.read_json(output / 'traces/audit.json'))
        api.require(row == ev['stage_results'][4] and audits == ev['target_audits'], 'P1 tail exact target audit recollection differs')
    return receipt


def p1_tail_join_finite(api, suite, sources, root, output, tools, inputs, reviews):
    api.require(set(inputs) == {'p1-prior-receipt', 'p1-prior-command', 'p1-private-parameters', 'p1-tail-receipt'}, 'P1 correlated view inputs differ')
    physical_path = api.no_symlinks(inputs['p1-tail-receipt']).resolve()
    api.require(physical_path.name == 'RECEIPT.json', 'P1 correlated view needs an actual continuation receipt')
    physical_suite = p1_tail_descriptor(api)
    physical = p1_tail_readback(api, physical_suite, sources, root, physical_path.parent, tools, {k: v for k, v in inputs.items() if k != 'p1-tail-receipt'})
    api.require(physical['outcome'] == 'FRESH_KERNEL_COMPONENTS', 'P1 correlated view lacks a complete qualified continuation')
    output.mkdir(parents=True); receipt = p1_initial_receipt(api, suite, sources, reviews)
    joined = {'physical_receipt_sha256': api.sha(physical_path.read_bytes()), 'physical_receipt_canonical_sha256': api.canonical(physical),
        'new_processes': 0, 'new_builds': 0, 'independent_evidence_increment': 0}
    api.write_json(output / 'JOIN.json', joined)
    stage = {'id': 'p1-tail-view-join', 'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': receipt['started_at'], 'ended_at': api.utc(),
        'log_sha256': api.sha((output / 'JOIN.json').read_bytes()), 'argv': ['{builtin:p1-tail-view-join}', '{input:p1-tail-receipt}'], 'new_processes': 0}
    ev = {'schema': p1_tail_meta['evidence_schema'], 'recipe': p1_tail_meta['recipe'], 'mode': 'FINITE_VIEW',
        'descriptor_sha256': api.canonical(suite['replay']), 'implementation': p1_tail_implementation(api),
        **joined, 'physical_receipt': physical, 'stage_results': [stage], 'scope_ceiling': p1_ceiling}
    receipt['replay_evidence'] = ev
    receipt['controls'] = p1_tail_controls(api, suite, physical['replay_evidence'])
    receipt['target_readbacks'] = [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']]
    receipt.update(outcome='FINITE_ONLY', proof_scope='FINITE', exit_code=0, axioms=[])
    p1_save_receipt(api, receipt, output); p1_tail_validate_receipt(api, receipt, suite, sources, root)
    return receipt


def p1_tail_validate_view(api, receipt, suite, sources, root):
    ev = receipt['replay_evidence']
    api.keys(ev, {'schema', 'recipe', 'mode', 'descriptor_sha256', 'implementation', 'physical_receipt_sha256', 'physical_receipt_canonical_sha256',
        'new_processes', 'new_builds', 'independent_evidence_increment', 'physical_receipt', 'stage_results', 'scope_ceiling'})
    for name in ('new_processes', 'new_builds', 'independent_evidence_increment'):
        api.require(type(ev[name]) is int and ev[name] == 0, 'P1 finite view gained independent execution/build credit')
    api.require(ev['scope_ceiling'] == p1_ceiling and receipt['outcome'] == 'FINITE_ONLY' and receipt['proof_scope'] == 'FINITE' and
        type(receipt['exit_code']) is int and receipt['exit_code'] == 0 and receipt['axioms'] == [], 'P1 finite view proof scope inflated')
    api.digest(ev['physical_receipt_sha256'])
    physical = ev['physical_receipt']; api.require(ev['physical_receipt_canonical_sha256'] == api.canonical(physical), 'P1 correlated physical content changed')
    p1_tail_validate_receipt(api, physical, p1_tail_descriptor(api), sources, root)
    api.require(physical['outcome'] == 'FRESH_KERNEL_COMPONENTS' and physical['ended_at'] <= receipt['started_at'], 'P1 finite view lacks prior successful audit')
    api.require(len(ev['stage_results']) == 1, 'P1 finite view has extra stages')
    row = ev['stage_results'][0]; api.keys(row, {'id', 'terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256', 'argv', 'new_processes'})
    api.require(row['id'] == 'p1-tail-view-join' and row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and row['exit_code'] == 0 and
        row['argv'] == ['{builtin:p1-tail-view-join}', '{input:p1-tail-receipt}'] and type(row['new_processes']) is int and row['new_processes'] == 0, 'P1 finite view is not a zero-process join')
    p1_time(api, row['started_at']); p1_time(api, row['ended_at']); api.digest(row['log_sha256'])
    api.require(receipt['started_at'] <= row['started_at'] <= row['ended_at'] <= receipt['ended_at'], 'P1 finite view interval differs')
    api.require(receipt['controls'] == p1_tail_controls(api, suite, physical['replay_evidence']), 'P1 finite controls came from another observation')
    api.require(receipt['target_readbacks'] == [{'target_id': t['id'], 'source_id': t['source_id'], 'target_sha256': t['target_sha256'], 'outcome': 'CHECKED'} for t in suite['targets']], 'P1 finite source target binding differs')
    return {'suite_id': suite['id'], 'outcome': 'FINITE_ONLY', 'scope': 'P1_SAME_CONTINUATION_ZERO_PROCESS_FINITE_VIEW'}
