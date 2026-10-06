from pathlib import Path, PurePosixPath
import ast, contextlib, io, json, math, os, re, runpy, signal, stat, subprocess, sys, time, types, zipfile

p1_archive = 'c3088bcc0c75a84754bf70beaac5efca88264cdb53bae771e206459bdb6b6e2d'
p1_prefix = 'P1_Expression_Source_and_Acceptance/'
p1_driver = '3c6cd0c6573778acc4f81e3d1e139e9467b2147ba5ff5fd12c262f1cdfc7101e'
p1_python = 'd1483a82342508f2ec2b172b788d5b676a59eaf70ed01ae846a0f84f63a3a82a'
p1_source = 'dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
p1_pins = {'LEAN_DISTRIBUTION_PIN.json': '6f364a506b2b7bc8934b13ef50b296fd2047d9b7894a2b7f637ad44e4f8e52fb', 'MATHLIB_SOURCE_PIN.json': 'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431', 'MATHLIB_CACHE_PIN.json': '7dc08ad35391b67f1fb930b1315432ec17321dc6ecfad13b4689f32ade95d2f9'}
p1_delta = 'ad3ea6127754328f22c495c52f9570c9d42371c5a103125aceda1dd6717ccf4a'
p1_trace_names = {f'.lake/build/lib/lean/Cache/{name}.trace' for name in ['Hashing', 'IO', 'Lean', 'Main', 'Requests']}
p1_copy_control = 'control-layout/tranche9/reviews/python-runtime-refinement/controls/independent_source_controls.py'
p1_copy_codecs = ['control-layout/tranche9/baseline/components/Eighth_Literal_Runtime_Counterexamples_20261002/prcodec.py', 'control-layout/tranche9/baseline/components/Semantic_Control_Independent_Review_20261002/literal-snapshot/prcodec.py']
p1_timeout_marker = '\nTIMEOUT: NO REJECTION OR SUCCESS CREDIT\n'
p1_resource = re.compile('\\btimeout\\b|WALL_CLOCK_LIMIT|maximum number of heartbeats|maximum recursion depth|out of memory', re.I)
p1_infrastructure = re.compile('unknown module|unknown constant|unknown identifier|file not found|no such file|object file .* does not exist', re.I)

def p1_packet(api, archive, root):
    raw = p1_archive_members(api, archive, p1_archive)
    api.require(all((name.startswith(p1_prefix) for name in raw)), 'Wrong P1 archive root')
    members = {name[len(p1_prefix):]: data for name, data in raw.items()}
    root = api.no_symlinks(root).resolve()
    actual = set()
    for path in root.rglob('*'):
        api.no_symlinks(path)
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    api.require(actual == set(members), 'P1 full packet census differs')
    for name, data in members.items():
        api.require(api.path_in(root, name).read_bytes() == data, 'P1 packet member differs')
    api.require(api.sha(members['replay.py']) == p1_driver and api.sha(members['source/prcodec.py']) == p1_source, 'Wrong P1 source/driver')
    for name, pin in p1_pins.items():
        api.require(api.sha(members['dependencies/' + name]) == pin, 'P1 dependency pin differs')
    api.require(api.sha(members['dependencies/TRACE_PATH_DELTAS.json']) == p1_delta, 'P1 trace scope differs')
    return members

def p1_trace_comparison(api, raw_files, delta, prefix, reference_prefix):
    """Check only the five declared traces; never write comparison bytes."""
    api.require(type(prefix) is str and type(reference_prefix) is str and (bool(prefix) == bool(reference_prefix)), 'P1 private strings must be paired')
    api.require(set(raw_files) == set(delta['allowed_paths']) == p1_trace_names and len(delta['allowed_paths']) == 5, 'P1 trace scope must be exactly five files')
    rows = {row['path']: row for row in delta['files']}
    api.require(set(rows) == p1_trace_names and len(delta['files']) == 5, 'P1 trace declaration census differs')
    current = prefix.encode()
    reference = reference_prefix.encode()
    result = []
    for name in sorted(rows):
        row = rows[name]
        raw = raw_files[name]
        api.require(isinstance(raw, bytes) and row['replacement_count'] == 1, 'Invalid P1 trace comparison')
        exact = api.sha(raw) == row['original_pin_sha256'] and len(raw) == row['original_pin_bytes']
        count = 0
        if exact:
            derived = raw
        else:
            api.require(bool(current) and raw.count(current) == 1, 'P1 trace requires exactly one supplied prefix')
            derived = raw.replace(current, reference)
            count = 1
        api.require(api.sha(derived) == row['original_pin_sha256'] and len(derived) == row['original_pin_bytes'], 'P1 trace comparison did not recover exact pinned bytes')
        result.append({'path': name, 'source_sha256': api.sha(raw), 'source_bytes': len(raw), 'derived_sha256': api.sha(derived), 'derived_bytes': len(derived), 'pinned_sha256': row['original_pin_sha256'], 'replacement_count': count})
    return {'files': result, 'current_string_sha256': api.sha(current), 'reference_string_sha256': api.sha(reference), 'dependency_bytes_written': False, 'full_inventory_verified': False, 'scope': 'FIVE_TRACE_METADATA_COMPARISONS_ONLY'}

def p1_prepare(api, archive, root, out, lean_root, mathlib, python, trace_prefix='', pinned_trace_prefix=''):
    root = api.no_symlinks(root).resolve()
    members = p1_packet(api, archive, root)
    out = api.no_symlinks(out).absolute()
    lean_root = api.no_symlinks(lean_root).resolve()
    mathlib = api.no_symlinks(mathlib).resolve()
    python = Path(python).absolute()
    api.require(not out.exists(), 'Original P1 output must be absent')
    for path in (root, lean_root, mathlib):
        api.require(not out.is_relative_to(path) and (not path.is_relative_to(out)), 'P1 output overlaps input')
    lean = api.no_symlinks(lean_root / 'bin/lean')
    api.require(api.sha(lean.read_bytes()) == api.LEAN_SHA and api.sha(python.read_bytes()) == p1_python, 'Changed P1 tool bytes')
    definitions = {node.targets[0].id: ast.literal_eval(node.value) for node in ast.parse(members['replay.py']).body if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and (node.targets[0].id in {'MODULES', 'MUTANTS'})}
    modules = definitions['MODULES']
    mutants = definitions['MUTANTS']
    api.require(len(modules) == 9 and len(mutants) == 4, 'P1 module/mutant census differs')
    pins = {name: json.loads(members['dependencies/' + name]) for name in p1_pins}
    cache = pins['MATHLIB_CACHE_PIN.json']
    inventory = {'compiler_entries': len(pins['LEAN_DISTRIBUTION_PIN.json']['entries']), 'source_files': len(pins['MATHLIB_SOURCE_PIN.json']['files']), 'cache_entries': len(cache['entries'])}
    api.require(inventory == {'compiler_entries': 5065, 'source_files': 6816, 'cache_entries': 34230}, 'P1 full inventory contract differs')
    delta = json.loads(members['dependencies/TRACE_PATH_DELTAS.json'])
    comparison = p1_trace_comparison(api, {name: api.path_in(mathlib, name).read_bytes() for name in delta['allowed_paths']}, delta, trace_prefix, pinned_trace_prefix)
    path = ':'.join([str(out / 'build')] + [str(api.path_in(mathlib, name)) for name in cache['roots']])
    children = []
    derivations = {}
    generated = {}
    copies = [(p1_copy_control, 'reviewer/independent_source_controls.py')] + [(name, 'source/prcodec.py') for name in p1_copy_codecs]
    for name, owner in copies:
        generated[name] = members[owner]
        derivations[name] = {'kind': 'COPIED_EXACT', 'owner': owner, 'owner_sha256': api.sha(members[owner]), 'derived_sha256': api.sha(members[owner]), 'driver_sha256': p1_driver}

    def child(name, member, argv, obj=None, expected=0, finite=False):
        source = out / member if member in generated else root / member
        data = generated.get(member, members.get(member))
        children.append({'id': name, 'readonly': False, 'profile': 'PYTHON_PIPE' if finite else 'LEAN_PIPE', 'argv': argv, 'cwd': str(out), 'explicit_cwd': True, 'source_path': str(source), 'source_sha256': api.sha(data), 'object_path': str(obj) if obj else None, 'expected_exit': expected, 'positive_prerequisites': [name for _, name in modules] if expected else [], 'lean_path': path, 'lean_bin': str(lean_root / 'bin'), 'timeout': 180, 'finite': finite, 'axiom_count': 37 if name == 'P1Axioms' else 4 if name == 'ReviewerContract' else None, 'log': str(out / 'logs' / (name + '.log')), 'required_copies': {str(out / n): api.sha(data) for n, data in generated.items()} if name == 'IndependentPythonControls' else {}})
    for kind, name in modules:
        member = kind + '/' + name.replace('.', '/') + '.lean'
        obj = out / 'build' / (name.replace('.', '/') + '.olean')
        child(name, member, [str(lean), '-j1', '--root=' + str(root / kind), '-o', str(obj), str(root / member)], obj)
    for name in mutants:
        member = 'controls/' + name + '.lean'
        obj = out / 'build' / (name + '.olean')
        child(name, member, [str(lean), '-j1', '--root=' + str(root / 'controls'), '-o', str(obj), str(root / member)], obj, 1)
    for name, member in [('SourceShape', 'source_contract.py'), ('SourceContract', 'controls/test_source_contract.py'), ('PythonEdges', 'controls/check_python_edges.py')]:
        child(name, member, [str(python), '-B', str(root / member)], finite=True)
    child('IndependentPythonControls', p1_copy_control, [str(python), '-B', str(out / p1_copy_control)], finite=True)
    api.require(len(children) == 17, 'P1 original child census differs')
    replacements = [(str(root), '$PACKET'), (str(out), '$OUTPUT'), (str(lean_root), '$LEAN_ROOT'), (str(mathlib), '$MATHLIB_ROOT'), (str(python), '$PYTHON')]
    return {'events': children, 'children': children, 'event_plan_sha256': api.canonical(children), 'driver_sha256': p1_driver, 'dependency_inventory_required': inventory, 'dependency_pin_sha256': p1_pins, 'full_dependency_inventory_verified': False, 'trace_comparison': comparison, 'private_argument_kinds': {'--trace-prefix': 'PAIRED_LITERAL_STRING', '--pinned-trace-prefix': 'PAIRED_LITERAL_STRING'}, 'replacements': replacements, 'derivations': derivations, 'generated_bytes': generated, 'new_independent_custody': False, 'requires_prior_scientific_output': False, 'original_sources_changed': False, 'requires_fresh_observer': True}

def p1_validate_call(api, event, argv, args, kwargs, parent_env):
    api.require(isinstance(argv, list) and argv == event['argv'] and all((isinstance(x, str) for x in argv)) and (not args), 'P1 original argv/order differs')
    api.require(set(kwargs) == {'cwd', 'env', 'stdout', 'stderr', 'text', 'timeout'}, 'P1 original child keyword differs')
    api.require(str(Path(kwargs['cwd']).absolute()) == event['cwd'], 'P1 explicit cwd differs')
    api.require(type(kwargs['timeout']) is int and kwargs['timeout'] == 180 and (kwargs['stdout'] == subprocess.PIPE) and (kwargs['stderr'] == subprocess.STDOUT) and (kwargs['text'] is True), 'P1 child capture/budget differs')
    env = {k: v for k, v in parent_env.items() if not k.startswith(('LEAN', 'LD_'))}
    env['LEAN_PATH'] = event['lean_path']
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PATH'] = event['lean_bin'] + os.pathsep + env.get('PATH', '')
    api.require(kwargs['env'] == env, 'P1 source-derived environment differs')
    api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 actual child source changed')
    for path, digest in event['required_copies'].items():
        api.require(api.sha(api.no_symlinks(path).read_bytes()) == digest, 'P1 compatibility copy differs')
    if event['object_path'] is not None:
        api.require(not api.no_symlinks(event['object_path']).exists(), 'P1 cold object already exists')
    return True

def p1_neutralize(api, raw, replacements, timeout=False):
    api.require(isinstance(raw, bytes), 'P1 raw diagnostic must be bytes')
    expected = ['$PACKET', '$OUTPUT', '$LEAN_ROOT', '$MATHLIB_ROOT', '$PYTHON']
    api.require(len(replacements) == 5 and [r[1] for r in replacements] == expected and all((type(old) is str and old for old, _ in replacements)), 'P1 exact diagnostic substitution map differs')
    text = raw.decode('utf8', errors='replace' if timeout else 'strict')
    mapping = []
    for old, new in sorted(replacements, key=lambda row: len(row[0]), reverse=True):
        count = text.count(old)
        before = api.sha(text.encode())
        text = text.replace(old, new)
        mapping.append({'source_string_sha256': api.sha(old.encode()), 'replacement': new, 'count': count, 'before_sha256': before, 'after_sha256': api.sha(text.encode())})
    if timeout:
        text += p1_timeout_marker
    derived = text.encode()
    return {'source_sha256': api.sha(raw), 'derived_sha256': api.sha(derived), 'derived_bytes': derived, 'replacements': mapping, 'utf8_decode_errors': 'replace' if timeout else 'strict', 'source_owned_timeout_suffix': timeout, 'science_bytes_changed': False}

def p1_classify_stage(api, plan, event, capture, raw, original_log, original_row, accepted_positive_ids):
    api.require(capture['argv'] == event['argv'] and capture['cwd'] == event['cwd'] and (capture['log_sha256'] == api.sha(raw)), 'P1 actual child capture differs')
    terminal = capture['terminal']
    code = capture['exit_code']
    api.require(terminal in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED'}, 'Unknown P1 child terminal')
    api.require(type(code) is int and 0 <= code < 124 if terminal == 'COMPLETED' else code is None, 'Invalid P1 captured child exit')
    if terminal == 'INTERRUPTED':
        api.require(original_row is None and original_log is None, 'P1 interrupted returned process needs an actual return-code capture extension')
        return {'outcome': 'RESOURCE_INCONCLUSIVE', 'semantic_outcome': None, 'evidence_scope': 'CAPTURE_ONLY', 'rejecting_subprocesses': 0, 'qualification': 'REQUIRES_SOURCE_OWNED_FULL_COLLECTOR', 'mutation_census_credit': None, 'derivation': None}
    derivation = p1_neutralize(api, raw, plan['replacements'], terminal == 'TIMEOUT')
    api.require(original_log == derivation['derived_bytes'], 'P1 source-owned diagnostic derivation differs')
    if terminal == 'TIMEOUT':
        api.require(original_row is None, 'P1 timeout must not manufacture an original command row')
    else:
        row = original_row
        api.require(isinstance(row, dict), 'Missing P1 original command row')
        neutral_argv = [p1_neutralize(api, x.encode(), plan['replacements'])['derived_bytes'].decode() for x in event['argv']]
        api.require(row['command'] == neutral_argv, 'P1 original neutral command differs')
        api.require(row['name'] == event['id'] and row['expectation'] == ('REJECT' if event['expected_exit'] else 'ACCEPT') and (type(row['exit_code']) is int) and (row['exit_code'] == code), 'P1 original child identity/exit differs')
        api.require(row['source_sha256'] == event['source_sha256'] and row['raw_diagnostic_sha256'] == api.sha(raw) and (row['path_neutral_log_sha256'] == api.sha(original_log)), 'P1 original source/log hashes differ')
        api.require(row['diagnostic_path_substitution_only'] is True and type(row['wall_limit_seconds']) is int and (row['wall_limit_seconds'] == 180), 'P1 original capture contract differs')
        api.require(type(row['elapsed_seconds']) in (int, float) and math.isfinite(row['elapsed_seconds']) and (row['elapsed_seconds'] >= 0), 'P1 elapsed time invalid')
    text = original_log.decode()
    resource = terminal != 'COMPLETED' or p1_resource.search(text) is not None
    obj = event['object_path']
    object_hash = None
    if resource:
        outcome = 'RESOURCE_INCONCLUSIVE'
    elif event['expected_exit'] == 1:
        matched = code == 1 and "error: tactic 'rfl' failed" in text and (p1_infrastructure.search(text) is None)
        if matched:
            api.require(set(event['positive_prerequisites']) <= set(accepted_positive_ids), 'P1 rejection lacks positive prerequisites')
            api.require(not api.no_symlinks(obj).exists(), 'P1 rejected mutant emitted an object')
        outcome = 'REJECT' if matched else 'FAILED'
    else:
        outcome = 'ACCEPT' if code == 0 and 'error:' not in text and ('sorryAx' not in text) and ("declaration uses 'sorry'" not in text) else 'FAILED'
        if outcome == 'ACCEPT' and obj is not None:
            object_hash = api.sha(api.no_symlinks(obj).read_bytes())
    return {'outcome': outcome, 'semantic_outcome': 'REJECT' if outcome == 'REJECT' else None, 'evidence_scope': 'FINITE_ONLY' if event['finite'] else 'SOURCE_CHILD_ONLY_NOT_QUALIFICATION', 'proof_scope': 'NONE', 'rejecting_subprocesses': 1 if outcome == 'REJECT' else 0, 'mutation_census_credit': None, 'qualification': 'REQUIRES_SOURCE_OWNED_FULL_COLLECTOR', 'object_sha256': object_hash, 'axiom_readbacks_required': event['axiom_count'], 'derivation': {k: v for k, v in derivation.items() if k != 'derived_bytes'}}

def p1_view_membership(api, plan):
    formal = [row for row in plan['children'] if not row['finite']]
    finite = [row for row in plan['children'] if row['finite']]
    api.require(len(formal) == 13 and len(finite) == 4 and (len({row['id'] for row in plan['children']}) == 17), 'P1 view child partition differs')
    return {'physical_runs': 1, 'formal': {'child_ids': [r['id'] for r in formal], 'object_count': 9}, 'finite': {'child_ids': [r['id'] for r in finite], 'object_count': 0}, 'proofs_from_view_join': 0, 'join_requires': 'SAME_CAPTURE_PARENT_AND_ORIGINAL_RECEIPT_SOURCE_TOOLCHAIN_DEPENDENCY_FINGERPRINTS'}

# Exact P1 family branch. Integration and scientific execution require owner release.
p1_schema = 'orthemology-v5-p1-replay-v1'
p1_evidence_schema = 'orthemology-v5-p1-evidence-v1'
p1_recipe = 't09-p1-original-v1'
p1_reference_owner = '31b8bec9737020d4db458406bf36202519249d53aab0e98657a103258284bf13'
p1_reference_prefix_sha = '8914341a79b1396f569f19ab2b47dc2b2d09d7bd015b7aa25c6ed5bc82f30978'
p1_ceiling = 'Expression algorithm-model correspondence only; frontend/CPython/host, parser/statement/full runner remain residual. No P2/P3 work.'
p1_copy_statement = 'Two byte-identical output-only copies of the bound input; no new independent provenance claim'
p1_finite_rel = 'control-layout/tranche9/reviews/python-runtime-refinement/evidence/INDEPENDENT_SOURCE_CONTROLS.json'
p1_public_paths = [m['path'] for m in p1_meta['modules']] + [
    'source_contract.py', 'controls/test_source_contract.py', 'controls/check_python_edges.py',
    'reviewer/independent_source_controls.py', 'source/prcodec.py', 'spec/SOURCE_AST_PINS.json']
p1_finite_names = ['SourceShape', 'SourceContract', 'PythonEdges', 'IndependentPythonControls']
p1_positive_names = [m['name'] for m in p1_meta['modules'] if not m['negative']]
p1_negative_names = [m['name'] for m in p1_meta['modules'] if m['negative']]
p1_child_names = p1_positive_names + p1_negative_names + p1_finite_names
p1_resource = re.compile(r'\btimeout\b|timed out|WALL_CLOCK_LIMIT|WALL_TIMEOUT|RESOURCE_LIMIT|maximum number of heartbeats|maximum recursion depth|out of memory', re.I)
p1_infrastructure = re.compile(r'unknown module|unknown constant|unknown identifier|file not found|no such file|failed to (?:load|read)|cannot load|object file .* does not exist', re.I)


def p1_api():
    # importlib users are not required to register a module in sys.modules.
    return types.SimpleNamespace(**globals())


def p1_archive_members(api, path, expected):
    data = api.no_symlinks(path).read_bytes(); api.require(api.sha(data) == expected, 'Changed original P1 archive')
    members = {}; folded = set()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for info in archive.infolist():
            api.relative(info.filename)
            api.require(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in {0, stat.S_IFREG}, 'Nonregular P1 archive member')
            api.require(info.filename not in members and info.filename.casefold() not in folded, 'Duplicate P1 archive member')
            folded.add(info.filename.casefold()); members[info.filename] = archive.read(info)
    return members


def p1_private_parameters(api, values, lean_root):
    api.keys(values, {'trace_prefix', 'pinned_trace_prefix'})
    a, b = values['trace_prefix'], values['pinned_trace_prefix']
    api.require(type(a) is str and type(b) is str and bool(a) == bool(b), 'P1 private trace strings must be paired')
    api.require(all(len(x.encode()) <= 4096 and not any(c in x for c in '\x00\r\n') for x in (a, b)), 'Invalid P1 private string')
    if a:
        api.require(a == str(Path(lean_root).resolve()) + '/', 'P1 current prefix is not the verified distribution root')
        api.require(api.sha(b.encode()) == p1_reference_prefix_sha, 'P1 reference prefix is not source-derived')
    return {'values': dict(values), 'public': {'kind': 'PAIRED_PRIVATE_TRACE_STRINGS',
            'current_sha256': api.sha(a.encode()), 'reference_sha256': api.sha(b.encode()),
            'reference_owner_sha256': p1_reference_owner, 'reference_derivation': 'LEAN_LITERAL_PARENT_PARENT_WITH_TRAILING_SLASH',
            'dependency_bytes_written': False}}


def p1_source_binding(api, binding, sources, expected_hash):
    api.require(isinstance(binding, dict), 'P1 source binding must be an object')
    kind = binding.get('kind')
    fields = {'ORIGINAL_SOURCE': {'kind', 'source_id', 'source_sha256'},
        'ARCHIVE_MEMBER': {'kind', 'archive_source_id', 'archive_sha256', 'member', 'source_sha256'},
        'GENERATED_BY_ORIGINAL': {'kind', 'source_id', 'source_sha256', 'generated_sha256', 'derivation_id'},
        'TOOL_PROBE': {'kind', 'tool_name', 'executable_sha256', 'driver_sha256'}}
    api.require(kind in fields, 'Unknown P1 source binding variant'); api.keys(binding, fields[kind])
    if kind == 'TOOL_PROBE':
        api.require(binding['tool_name'] in {'lean', 'python'} and binding['driver_sha256'] == p1_driver, 'Wrong P1 tool probe owner')
        api.require(binding['executable_sha256'] == (api.LEAN_SHA if binding['tool_name'] == 'lean' else p1_python), 'Wrong P1 tool probe executable')
    else:
        api.require(binding['source_sha256'] == expected_hash, 'Wrong P1 source binding hash')
        if kind == 'ARCHIVE_MEMBER':
            api.relative(binding['member']); owner = sources.get(binding['archive_source_id'])
            api.require(owner and owner['original_sha256'] == binding['archive_sha256'], 'Wrong P1 archive owner')
        else:
            owner = sources.get(binding['source_id']); api.require(owner and owner['original_sha256'] == expected_hash, 'Wrong P1 source owner')
            if kind == 'GENERATED_BY_ORIGINAL':
                api.identifier(binding['derivation_id']); api.require(binding['generated_sha256'] == expected_hash, 'P1 compatibility copy is not exact')
    return dict(binding)


def p1_choose_source(api, sources, expected, public=True):
    choices = [r for r in sources.values() if r.get('original_sha256') == expected and
               (not public or (r.get('projection') == 'EXACT' and r.get('public_sha256') == expected))]
    api.require(choices, 'Missing exact P1 source identity')
    return sorted(choices, key=lambda r: r['id'])[0]['id']


def p1_target_declaration(api, data, target):
    local = target['name'].rsplit('.', 1)[-1]
    match = re.search(r'\btheorem ' + re.escape(local) + r'\b[\s\S]*?(?=\s:=)', data.decode('utf8'))
    api.require(match and api.sha(match.group().encode()) == target['target_sha256'], 'P1 theorem declaration changed')
    return match.group()


def p1_descriptor(api, sources, source_root, mode='PHYSICAL'):
    api.require(mode in {'PHYSICAL', 'FINITE_VIEW'}, 'Unknown P1 view')
    root = api.no_symlinks(source_root)
    for path in p1_public_paths:
        data = api.path_in(root, path).read_bytes()
        api.require(api.sha(data) == p1_meta['members'][path]['sha256'], 'P1 descriptor source drift')
    files = [{'path': path, 'source_id': p1_choose_source(api, sources, p1_meta['members'][path]['sha256'])} for path in p1_public_paths]
    by_path = {r['path']: r['source_id'] for r in files}
    archive_id = p1_choose_source(api, sources, p1_archive, False); driver_id = p1_choose_source(api, sources, p1_driver, False)
    targets = []; audit_targets = []
    for t in p1_meta['targets']:
        tid = 'p1-' + t['name']; decl = p1_target_declaration(api, api.path_in(root, t['path']).read_bytes(), t)
        audit_targets.append({'target_id': tid, 'module': t['module'], 'name': t['name'], 'source_id': by_path[t['path']]})
        targets.append({'id': tid, 'source_id': by_path[t['path']], 'declaration': decl, 'target_sha256': t['target_sha256'], 'domain': 'REFERENCE_EXECUTION', 'calculus': 'OTHER'})
    children = p1_child_contract(api, by_path, archive_id)
    controls = [{'id': 'p1-' + c['id'], 'source_id': c['source_binding'].get('source_id', by_path[c['owner_path']]),
        'target_id': targets[0]['id'], 'role': 'MUTATION_REJECTION' if c['expected_exit_code'] else 'POSITIVE',
        'expected_outcome': 'REJECT' if c['expected_exit_code'] else 'ACCEPT',
        'expected_outcome_sha256': api.sha(('REJECT' if c['expected_exit_code'] else 'ACCEPT').encode())} for c in children]
    if mode == 'FINITE_VIEW':
        targets = [{'id': 'p1-eval-expr-source', 'source_id': by_path['source/prcodec.py'], 'declaration': p1_meta['finite_declaration'],
            'target_sha256': p1_meta['finite_target_sha256'], 'domain': 'SOURCE_TEXT', 'calculus': 'NONE'}]
        controls = [{**c, 'target_id': targets[0]['id']} for c in controls if c['id'][3:] in p1_finite_names]
    replay = {'schema': p1_schema, 'recipe': p1_recipe, 'scope': 'COMPONENTS' if mode == 'PHYSICAL' else 'FINITE', 'mode': mode,
       'files': files, 'archive_source_id': archive_id, 'driver_source_id': driver_id,
       'private_parameters': [{'name': 'trace_prefix', 'kind': 'PRIVATE_STRING', 'derivation': 'VERIFIED_LEAN_DISTRIBUTION_ROOT_WITH_TRAILING_SLASH'},
           {'name': 'pinned_trace_prefix', 'kind': 'PRIVATE_STRING', 'derivation': 'SOURCE_LITERAL_PARENT_PARENT_WITH_TRAILING_SLASH', 'owner_sha256': p1_reference_owner, 'value_sha256': p1_reference_prefix_sha}],
       'argument_meanings': {'--lean-root': 'LEAN_DISTRIBUTION_ROOT', '--mathlib-root': 'MATHLIB_ROOT', '--output': 'FRESH_OUTPUT_DIRECTORY',
           '--trace-prefix': 'PAIRED_PRIVATE_STRING', '--pinned-trace-prefix': 'PAIRED_PRIVATE_STRING'},
       'source_argv': ['{tool:python}', '-B', '{driver:p1}', '--lean-root', '{tool:lean-root}', '--mathlib-root', '{dependency:mathlib}',
           '--output', '{out}/original', '--trace-prefix', '{private:trace_prefix}', '--pinned-trace-prefix', '{private:pinned_trace_prefix}'],
       'launch_cwd': '{archive:p1}', 'module_order': p1_positive_names, 'modules': p1_meta['modules'],
       'official_imports': p1_meta['official_imports'], 'audit_targets': audit_targets, 'children': children,
       'tools': [p1_meta['python']], 'dependency_pins': p1_pins, 'parent_timeout_seconds': 7200, 'child_timeout_seconds': 180,
       'audit_timeout_seconds': 300, 'scope_ceiling': p1_ceiling, 'physical_suite_id': 'd08-p1'}
    return {'id': 'd08-p1' if mode == 'PHYSICAL' else 'd08-p1-reference', 'family': 't09-expression-machine' if mode == 'PHYSICAL' else 't09-expression-source',
       'result_families': ['t09-expression-machine', 't09-expression-source'] if mode == 'PHYSICAL' else ['t09-expression-source'],
       'origin_archive_sha256': p1_archive, 'source_ids': [r['source_id'] for r in files], 'review_ids': [],
       'targets': targets, 'controls': controls, 'toolchain': p1_meta['toolchain'], 'replay': replay}


def p1_child_contract(api, paths, archive_id):
    rows = []
    pairs = [(m['name'], m['path'], m['negative']) for m in p1_meta['modules']]
    pairs += list(zip(p1_finite_names, ['source_contract.py', 'controls/test_source_contract.py', 'controls/check_python_edges.py', 'reviewer/independent_source_controls.py'], [False] * 4))
    for index, (name, path, negative) in enumerate(pairs):
        h = p1_meta['members'][path]['sha256']; finite = name in p1_finite_names
        binding = {'kind': 'ORIGINAL_SOURCE', 'source_id': paths[path], 'source_sha256': h}
        src = '{archive:p1}/' + path
        if name == 'IndependentPythonControls':
            src = '{out}/original/' + p1_copy_control
            binding = {'kind': 'GENERATED_BY_ORIGINAL', 'source_id': paths[path], 'source_sha256': h, 'generated_sha256': h, 'derivation_id': 'p1-control-copy'}
        obj = None if finite else 'original/build/' + name.replace('.', '/') + '.olean'
        argv = ['{tool:python}', '-B', src] if finite else ['{tool:lean}', '-j1', '--root={archive:p1}/' + path.split('/')[0], '-o', '{out}/' + obj, src]
        rows.append({'id': name, 'index': index, 'owner_path': path, 'source_binding': binding, 'argv': argv,
            'cwd': '{out}/original', 'expected_exit_code': 1 if negative else 0, 'timeout_seconds': 180,
            'positive_prerequisites': p1_positive_names if negative else [], 'object_path': obj,
            'log': 'original/logs/' + name + '.log', 'scope': 'FINITE_ONLY' if finite else 'FORMAL_COMPONENT',
            'axiom_count': 37 if name == 'P1Axioms' else 4 if name == 'ReviewerContract' else None})
    return rows


def p1_validate_suite(api, suite, sources, root):
    try:
        api.keys(suite, {'id', 'family', 'result_families', 'origin_archive_sha256', 'source_ids', 'review_ids', 'targets', 'controls', 'toolchain', 'replay'})
        replay = suite['replay']; mode = replay['mode']; api.require(mode in {'PHYSICAL', 'FINITE_VIEW'}, 'Unknown P1 mode')
        files = replay['files']; api.require(isinstance(files, list) and [r['path'] for r in files] == p1_public_paths, 'Incomplete P1 source census')
        contents = {}; paths = {}; ids = set()
        for row in files:
            api.keys(row, {'path', 'source_id'}); sid = row['source_id']; api.identifier(sid)
            api.require(sid not in ids, 'P1 duplicate source identity'); ids.add(sid)
            source = sources[sid]; data = api.public_bytes(root, source)
            api.require(source['projection'] == 'EXACT' and api.sha(data) == p1_meta['members'][row['path']]['sha256'], 'P1 source bytes/projection differ')
            contents[row['path']] = data; paths[row['path']] = sid
        api.require(suite['source_ids'] == [x['source_id'] for x in files], 'P1 suite/projection inventory differs')
        for field, expected in [('archive_source_id', p1_archive), ('driver_source_id', p1_driver)]:
            owner = sources[replay[field]]; api.require(owner['original_sha256'] == expected, 'P1 custody identity changed')
        driver = sources[replay['driver_source_id']]
        api.require(driver['origin_archive_sha256'] == p1_archive and driver['member_chain'][-1] == p1_prefix + 'replay.py', 'P1 driver member changed')
        # Reconstruct exact permitted descriptors from immutable code-owned source data.
        expected = p1_descriptor_from_contents(api, sources, contents, mode, paths, replay['archive_source_id'], replay['driver_source_id'])
        api.require(replay == expected['replay'], 'P1 descriptor differs from complete exact recipe')
        for field in ('id', 'family', 'result_families', 'origin_archive_sha256', 'toolchain', 'targets', 'controls'):
            api.require(suite[field] == expected[field], 'P1 suite field changed: ' + field)
        api.string_list(suite['review_ids'])
        for child in replay['children']:
            p1_source_binding(api, child['source_binding'], sources, p1_meta['members'][child['owner_path']]['sha256'])
        accepted = set(); negative = set(p1_negative_names)
        for module in p1_meta['modules']:
            actual = api.imports(contents[module['path']].decode()); api.require(actual == module['imports'], 'P1 original imports changed')
            custom = set(actual) & set(p1_child_names)
            api.require(not (custom & negative), 'P1 negative source contaminates accepted closure')
            if not module['negative']:
                api.require(custom <= accepted, 'P1 module order is incomplete'); accepted.add(module['name'])
            api.require(set(actual) - set(p1_child_names) <= {x['module'] for x in p1_meta['official_imports']}, 'Undeclared P1 official import')
        return {**replay, 'contents': contents, 'paths': paths, 'targets': {t['id']: t for t in suite['targets']}}
    except (KeyError, TypeError, AttributeError, UnicodeError) as exc:
        raise ValueError('Malformed P1 descriptor or source: ' + str(exc)) from exc


def p1_descriptor_from_contents(api, sources, contents, mode, paths, archive_id, driver_id):
    # A bounded virtual read-only source root avoids materialising producer files.
    class Reader:
        def __init__(self, name=''): self.name = name
        def read_bytes(self): return contents[self.name]
    class Facade:
        def __getattr__(self, name): return getattr(api, name)
        def no_symlinks(self, path): return path
        def path_in(self, root, name): return Reader(name)
    facade = Facade()
    selected={sid:sources[sid] for sid in set(paths.values())|{archive_id,driver_id}}
    expected = p1_descriptor(facade, selected, Reader(), mode)
    api.require({r['path']: r['source_id'] for r in expected['replay']['files']} == paths, 'P1 source aliases differ from canonical owner selection')
    api.require(expected['replay']['archive_source_id'] == archive_id and expected['replay']['driver_source_id'] == driver_id, 'P1 custody owner alias differs')
    return expected


def p1_inventory(api, base, pin, trace_comparison=None):
    base = api.no_symlinks(base).resolve(); api.require(base.is_dir(), 'Missing P1 dependency root')
    api.require(isinstance(pin, dict) and isinstance(pin.get('roots'), list) and isinstance(pin.get('entries'), list), 'Invalid P1 dependency manifest')
    rows = {}; seen = set(); allowed = trace_comparison or {}
    for row in pin['entries']:
        rel = api.relative(row['path']); api.require(rel not in rows, 'Duplicate P1 dependency entry'); rows[rel] = row
    for name in pin['roots']:
        api.require(isinstance(name, str), 'Invalid P1 inventory root')
        directory = base if name == '' else api.path_in(base, name)
        api.require(directory.is_dir() and not directory.is_symlink(), 'Missing P1 inventory directory')
        for path in ([directory] if name else []) + list(directory.rglob('*')): seen.add(path.relative_to(base).as_posix())
    api.require(seen == set(rows), 'P1 dependency inventory missing/extra entries')
    changed = []; facts = []
    for rel, row in rows.items():
        path = base / rel; kind = row['kind']
        # Ancestors may not be symlinks; a source-declared leaf symlink is checked exactly.
        api.no_symlinks(path.parent)
        if kind == 'directory': api.require(path.is_dir() and not path.is_symlink(), 'P1 dependency directory drift')
        elif kind == 'symlink':
            api.require(path.is_symlink() and os.readlink(path) == row['target'] and path.exists() and path.resolve().is_relative_to(base), 'P1 dependency symlink drift')
        else:
            api.require(kind == 'file' and path.is_file() and not path.is_symlink(), 'P1 nonregular dependency')
            data = path.read_bytes(); exact = api.sha(data) == row['sha256'] and len(data) == row.get('bytes', row.get('size'))
            if not exact:
                match = allowed.get(rel)
                api.require(match and match['source_sha256'] == api.sha(data) and match['source_bytes'] == len(data)
                    and match['derived_sha256'] == row['sha256'] and match['derived_bytes'] == row.get('bytes', row.get('size')), 'P1 dependency identity mismatch')
                changed.append(rel)
            facts.append({'path': rel, 'sha256': api.sha(data), 'bytes': len(data)})
    return {'entries': len(rows), 'exact_except_trace_paths': sorted(changed), 'actual_files_sha256': api.canonical(facts)}


def p1_verify_dependencies(api, source_root, lean_root, mathlib, pair):
    manifests = {}
    for name, h in p1_pins.items():
        path = api.path_in(source_root, 'dependencies/' + name); api.require(api.sha(path.read_bytes()) == h, 'P1 pin manifest changed')
        manifests[name] = api.read_json(path)
    delta = api.read_json(api.path_in(source_root, 'dependencies/TRACE_PATH_DELTAS.json'))
    api.require(api.sha(api.path_in(source_root, 'dependencies/TRACE_PATH_DELTAS.json').read_bytes()) == p1_delta, 'P1 trace delta changed')
    compare = p1_trace_comparison(api, {n: api.path_in(mathlib, n).read_bytes() for n in p1_trace_names}, delta,
        pair['values']['trace_prefix'], pair['values']['pinned_trace_prefix'])
    l = p1_inventory(api, lean_root, manifests['LEAN_DISTRIBUTION_PIN.json'])
    c = p1_inventory(api, mathlib, manifests['MATHLIB_CACHE_PIN.json'], {x['path']: x for x in compare['files']})
    source_rows = manifests['MATHLIB_SOURCE_PIN.json']['files']; seen = set(); facts = []
    for row in source_rows:
        name = api.relative(row['path']); api.require(name not in seen, 'Duplicate P1 Mathlib source'); seen.add(name)
        data = api.path_in(mathlib, name).read_bytes()
        api.require(len(data) == row['size'] and api.sha(data) == row['sha256'], 'P1 Mathlib source identity mismatch')
        facts.append({'path': name, 'sha256': api.sha(data), 'bytes': len(data)})
    api.require((l['entries'], len(source_rows), c['entries']) == (5065, 6816, 34230), 'Incomplete P1 full inventory')
    expected = {'lean_distribution': {k: l[k] for k in ('entries', 'exact_except_trace_paths')},
        'mathlib_cache': {k: c[k] for k in ('entries', 'exact_except_trace_paths')}, 'source_records': 6816,
        'pin_manifests': p1_pins, 'official_precompiled_cache_trusted': True, 'proof_dependencies_rebuilt': False}
    return {'original_expected': expected, 'compiler_inventory_sha256': l['actual_files_sha256'],
        'cache_inventory_sha256': c['actual_files_sha256'], 'source_inventory_sha256': api.canonical(facts),
        'comparison': compare, 'full_inventory_verified': True, 'dependency_bytes_written': False}


def p1_packet_expected(api, root):
    root=api.no_symlinks(root)
    seen=set()
    for path in root.rglob('*'):
        api.no_symlinks(path)
        if path.is_file():seen.add(path.relative_to(root).as_posix())
    api.require(seen==set(p1_meta['members']),'P1 packet postcheck census changed')
    data = {n: api.path_in(root, n).read_bytes() for n in p1_meta['members']}
    for n, b in data.items(): api.require(api.sha(b) == p1_meta['members'][n]['sha256'] and len(b) == p1_meta['members'][n]['bytes'], 'P1 packet identity drift')
    manifest = json.loads(data['PUBLIC_MANIFEST.json']); source = json.loads(data['bindings/ACCEPTED_SOURCE_MANIFEST.json']); review = json.loads(data['bindings/ACCEPTED_REVIEW_MANIFEST.json'])
    return {'public_manifest_sha256': api.sha(data['PUBLIC_MANIFEST.json']),
        'accepted_source_manifest_sha256': 'd0177de1ebeb8de4ff71898dbccc729ca420c70a50c307f1bacccd6d2c38d43d',
        'accepted_review_receipt_sha256': 'c55e4f5ae6dba9ce0f517c2b6ab242fdfbad7e4f8951e856cb7487e7fd1c15a0',
        'public_files': len(manifest['files']), 'original_source_payloads': len(source['files']), 'original_review_payloads': len(review['files'])}


def p1_capture_run(api, original_run, plan, trace, parent_env):
    position = 0; trace = api.no_symlinks(trace)
    def invoke(argv, *args, **kwargs):
        nonlocal position
        api.require(position < len(plan['children']), 'Extra P1 original child')
        event = plan['children'][position]; p1_validate_call(api, event, argv, args, kwargs, parent_env)
        input_hash = None
        if plan.get('preflight') is not None:
            input_path = api.path_in(event['cwd'], 'INPUT_RECEIPT.json')
            api.require(api.read_json(input_path) == plan['preflight']['input_expected'], 'P1 original input preflight differs')
            input_hash = api.sha(input_path.read_bytes())
        index = position; position += 1; record_path = api.path_in(trace, f'{index:04}.json')
        api.require(not record_path.exists(), 'P1 capture collision')
        record = {'index': index, 'argv': list(argv), 'cwd': str(Path(kwargs['cwd']).absolute()), 'started_at': api.utc(), 'ended_at': None,
            'terminal': 'RUNNING', 'exit_code': None, 'returned_exit_code': None, 'returned': False, 'log_sha256': None,
            'source_sha256': event['source_sha256'], 'output_hashes': {}, 'input_receipt_sha256': input_hash}
        api.write_json(record_path, record)
        def finish(raw, terminal, returned=False, code=None):
            raw = raw.encode('utf8') if isinstance(raw, str) else raw
            api.require(isinstance(raw, bytes), 'P1 capture omitted diagnostic bytes')
            log = api.path_in(trace, f'{index:04}.log'); api.require(not log.exists(), 'P1 raw log collision'); log.write_bytes(raw)
            outputs = {}
            if event['object_path']:
                obj = api.no_symlinks(event['object_path'])
                if obj.is_file(): outputs[str(obj)] = api.sha(obj.read_bytes())
            api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'P1 child changed source')
            record.update(ended_at=api.utc(), terminal=terminal, exit_code=code if terminal == 'COMPLETED' else None,
                returned_exit_code=code if returned else None, returned=returned, log_sha256=api.sha(raw), output_hashes=outputs)
            api.write_json(record_path, record)
        try:
            result = original_run(argv, **kwargs)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            finish(getattr(error, 'stdout', None) or b'', 'TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'INTERRUPTED')
            raise
        except BaseException:
            finish(b'', 'INTERRUPTED'); raise
        api.require(type(result.returncode) is int and isinstance(result.stdout, str), 'Invalid P1 original subprocess result')
        finish(result.stdout, 'COMPLETED' if 0 <= result.returncode < 124 else 'INTERRUPTED', True, result.returncode)
        return result
    return invoke


def p1_check_driver(api, driver, arguments, plan):
    api.require(sys.flags.optimize == 0, 'P1 original driver refuses optimized execution')
    api.require(api.sha(api.no_symlinks(driver).read_bytes()) == p1_driver, 'Unreviewed P1 original driver')
    api.require(arguments == plan['source_arguments'], 'P1 source-facing arguments changed')
    api.require([x['id'] for x in plan['children']] == p1_child_names and plan.get('preflight'), 'P1 tracing lacks complete original plan')


def p1_run_original(api, driver, arguments, plan, trace, runner=None):
    p1_check_driver(api, driver, arguments, plan)
    trace = api.no_symlinks(trace); api.require(not trace.exists(), 'P1 trace must be absent'); trace.mkdir(parents=True)
    old_run = subprocess.run; old_argv = sys.argv; old_path = sys.path[:]; old_cwd = Path.cwd(); old_bytecode = sys.dont_write_bytecode
    try:
        subprocess.run = p1_capture_run(api, old_run, plan, trace, dict(os.environ))
        sys.argv = [str(driver), *arguments]; sys.path[0] = str(Path(driver).parent); sys.dont_write_bytecode = True
        os.chdir(Path(driver).parent)
        (runner or runpy.run_path)(str(driver), run_name='__main__')
    finally:
        subprocess.run = old_run; sys.argv = old_argv; sys.path[:] = old_path; sys.dont_write_bytecode = old_bytecode; os.chdir(old_cwd)
    return 0


def p1_classify(api, plan, event, capture, raw, original_log, original_row, positives):
    api.require(capture['argv'] == event['argv'] and capture['cwd'] == event['cwd'] and capture['source_sha256'] == event['source_sha256'], 'P1 child capture identity mismatch')
    api.require(capture['log_sha256'] == api.sha(raw) and type(capture['returned']) is bool, 'P1 raw capture mismatch')
    terminal = capture['terminal']; code = capture['returned_exit_code']
    api.require(terminal in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED'}, 'P1 child has no terminal capture')
    api.require((capture['returned'] and type(code) is int) or (not capture['returned'] and code is None), 'P1 actual return-code provenance mismatch')
    api.require(capture['exit_code'] == (code if terminal == 'COMPLETED' else None), 'P1 semantic/raw return-code mismatch')
    if terminal == 'COMPLETED': api.require(capture['returned'] and 0 <= code < 124, 'Invalid P1 completed child')
    if terminal == 'TIMEOUT': api.require(not capture['returned'], 'P1 timeout cannot have returned status')
    derivation = None
    if capture['returned'] or terminal == 'TIMEOUT':
        clean = p1_neutralize(api, raw, plan['replacements'], terminal == 'TIMEOUT')
        api.require(original_log == clean['derived_bytes'], 'P1 raw-to-neutral log derivation mismatch')
        derivation = {k: v for k, v in clean.items() if k != 'derived_bytes'}
    else: api.require(original_log is None, 'Unreturned P1 child unexpectedly has an original log')
    if capture['returned']:
        api.require(isinstance(original_row, dict), 'P1 returned child omitted original command row')
        api.keys(original_row, {'name','expectation','exit_code','elapsed_seconds','command','source_sha256','raw_diagnostic_sha256','path_neutral_log_sha256','diagnostic_path_substitution_only','wall_limit_seconds'})
        expected = {'name': event['id'], 'expectation': 'REJECT' if event['expected_exit'] else 'ACCEPT', 'exit_code': code,
            'command': [p1_neutralize(api, x.encode(), plan['replacements'])['derived_bytes'].decode() for x in event['argv']],
            'source_sha256': event['source_sha256'], 'raw_diagnostic_sha256': api.sha(raw), 'path_neutral_log_sha256': api.sha(original_log),
            'diagnostic_path_substitution_only': True, 'wall_limit_seconds': 180}
        for k, value in expected.items(): api.require(type(original_row[k]) is type(value) and original_row[k] == value, 'P1 original command binding mismatch: ' + k)
        elapsed = original_row['elapsed_seconds']; api.require(type(elapsed) in {int, float} and math.isfinite(elapsed) and elapsed >= 0, 'Invalid P1 elapsed time')
    else: api.require(original_row is None, 'P1 unreturned child cannot have a fabricated original row')
    text = raw.decode('utf8', errors='replace'); outcome = 'FAILED'; obj_hash = None
    if terminal != 'COMPLETED' or p1_resource.search(text): outcome = 'RESOURCE_INCONCLUSIVE'
    elif event['expected_exit']:
        if code == 1 and "error: tactic 'rfl' failed" in text and not p1_infrastructure.search(text):
            api.require(set(event['positive_prerequisites']) <= positives, 'P1 intended rejection lacks nine prior positives')
            api.require(not api.no_symlinks(event['object_path']).exists(), 'P1 rejected mutant emitted an object'); outcome = 'REJECT'
    elif code == 0 and not any(x in text for x in ('error:', 'sorryAx', "declaration uses 'sorry'")):
        if event['object_path']:
            obj = api.no_symlinks(event['object_path']); obj_hash = api.sha(obj.read_bytes())
            api.require(capture['output_hashes'] == {str(obj): obj_hash}, 'P1 captured/current object differs')
        else: api.require(capture['output_hashes'] == {}, 'Finite P1 child gained an object')
        outcome = 'ACCEPT'
    return {'id': event['id'], 'outcome': outcome, 'semantic_outcome': outcome if outcome in {'ACCEPT', 'REJECT'} else None,
        'rejecting_subprocesses': int(outcome == 'REJECT'), 'scope': 'FINITE_ONLY' if event['finite'] else 'FORMAL_COMPONENT',
        'object_sha256': obj_hash, 'derivation': derivation, 'mutation_census_credit': None}


def p1_audit_source(api, targets):
    api.require(isinstance(targets, list) and targets, 'P1 safe audit has no targets')
    for row in targets: api.lean_name(row['name']); api.lean_name(row['module'])
    suffix = api.canonical([{k: row[k] for k in ('target_id', 'module', 'name')} for row in targets])[:16]
    namespace = 'P1FreshCheckedAudit_' + suffix
    api.require(not any(t['name'].startswith(namespace + '.') for t in targets), 'P1 audit namespace collision')
    return api._audit_source(targets).replace('V5SuccessorCheckedAudit', namespace)


def p1_json(api, text):
    def pairs(rows):
        obj = {}
        for key, value in rows:
            api.require(key not in obj, 'Duplicate P1 JSON key'); obj[key] = value
        return obj
    def bad(value): raise ValueError('Nonfinite P1 JSON')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad)


def p1_finite(api, root, out, texts):
    api.require(set(texts) == set(p1_finite_names), 'P1 finite child coverage incomplete')
    def original(name):
        data = api.path_in(root, name).read_bytes()
        api.require(api.sha(data) == p1_meta['members'][name]['sha256'], 'P1 finite source/reference changed')
        return data
    shape = p1_json(api, texts['SourceShape'])
    api.require(api.canonical(shape) == api.canonical(p1_json(api, original('acceptance/author/SOURCE_SHAPE_RESULT.json'))), 'P1 source-shape census/limits changed')
    edges = p1_json(api, texts['PythonEdges'])
    api.require(api.canonical(edges) == api.canonical(p1_json(api, original('acceptance/author/PYTHON_EDGE_CONTROLS.json'))), 'P1 bounded Python edge cases changed')
    api.require(re.fullmatch(r'\.\.\n-+\nRan 2 tests in [0-9.]+s\n\nOK\n', texts['SourceContract'].replace('\r\n', '\n')), 'P1 source contract tests incomplete')
    source = original('source/prcodec.py'); script = original('reviewer/independent_source_controls.py')
    obs_path = api.path_in(out, p1_finite_rel); obs = api.read_json(obs_path)
    reference = p1_json(api, original('acceptance/evidence/INDEPENDENT_SOURCE_CONTROLS.json'))
    api.keys(obs, set(reference))
    api.require(obs['source_sha256'] == p1_source and obs['independent_literal_copy_sha256'] == p1_source and obs['script_sha256'] == api.sha(script), 'P1 finite literal/driver identity differs')
    for key in ('status', 'differential_cases', 'outcome_counts', 'seeded_boundary_cases', 'observed_source_lines', 'source_ast_bindings', 'limits'):
        api.require(api.canonical(obs[key]) == api.canonical(reference[key]), 'P1 finite census or scope changed: ' + key)
    api.require(isinstance(obs['python_version'], str) and obs['python_version'].startswith('3.11.9 '), 'P1 finite interpreter differs')
    api.require(isinstance(obs['created_utc'], str) and re.fullmatch(r'\d{4}-\d\d-\d\dT[0-9:.]+(?:Z|\+00:00)', obs['created_utc']), 'P1 finite time missing')
    tree = ast.parse(script.decode()); assignments = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'mutations' for t in n.targets)]
    api.require(len(assignments) == 1, 'P1 mutation table missing'); cases = ast.literal_eval(assignments[0].value)
    api.require(len(cases) == len(obs['mutation_controls']) == 18, 'P1 internal comparison census differs')
    mutation_hashes = []
    for (name, before, after, case), row in zip(cases, obs['mutation_controls']):
        api.keys(row, {'name', 'case', 'original', 'mutant', 'changed_source_sha256', 'detected'})
        api.require(row['name'] == name and api.canonical(row['case']) == api.canonical(case), 'P1 finite witness changed')
        text = source.decode(); api.require(text.count(before) == 1, 'P1 mutation source anchor differs')
        api.require(row['changed_source_sha256'] == api.sha(text.replace(before, after).encode()), 'P1 internal mutant bytes differ')
        api.require(row['detected'] is True and api.canonical(row['original']) != api.canonical(row['mutant']), 'P1 internal mutation undetected')
        for value in (row['original'], row['mutant']):
            api.require(isinstance(value, list) and len(value) in (3, 4) and value[0] in ('ok', 'err') and type(value[-1]) is int and value[-1] >= 0, 'Malformed P1 model observation')
        mutation_hashes.append(api.canonical(row))
    outside = obs['outside_domain_observations']; old_outside = reference['outside_domain_observations']
    api.require(isinstance(outside, list) and len(outside) == 11 and [x['input_repr'] for x in outside] == [x['input_repr'] for x in old_outside], 'P1 excluded-domain census changed')
    for row in outside:
        api.keys(row, {'input_repr', 'observation'}); api.require(isinstance(row['observation'], list) and row['observation'][0] in ('ok', 'err'), 'Invalid P1 excluded-domain observation')
    summary, sep, tail = texts['IndependentPythonControls'].rpartition('\nDetected mutations: ')
    api.require(sep and tail == '18\n', 'P1 internal mutation summary differs')
    keys = ['status', 'differential_cases', 'outcome_counts', 'seeded_boundary_cases', 'source_ast_bindings']
    api.require(api.canonical(p1_json(api, summary)) == api.canonical({k: obs[k] for k in keys}), 'P1 finite stdout/file join differs')
    return {'source_shape': 'IDENTITY_ONLY', 'source_contract_tests': 2, 'source_text_mutations': 5, 'edge_cases': 26,
        'edge_outside_domain': 4, 'differential_cases': 266760, 'seeded_boundary_cases': 1593,
        'internal_mutations': 18, 'internal_mutation_record_sha256': mutation_hashes, 'outside_domain': 11,
        'finite_receipt_sha256': api.sha(obs_path.read_bytes()), 'rejecting_subprocesses': 0, 'scope': 'FINITE_ONLY',
        'scope_ceiling': p1_ceiling}


def p1_time(api, value):
    api.require(isinstance(value, str) and value.endswith('Z'), 'Missing P1 measured UTC time')
    from datetime import datetime
    parsed = datetime.fromisoformat(value[:-1] + '+00:00')
    return parsed


def p1_collect(api, plan, output, trace, parent, parent_log):
    api.require([x['id'] for x in plan['children']] == p1_child_names and plan.get('preflight'), 'P1 whole collector lacks complete source plan')
    output = api.no_symlinks(output); trace = api.no_symlinks(trace)
    api.require(parent.get('log_sha256') == api.sha(parent_log), 'P1 parent log capture changed')
    p1_time(api, parent['started_at']); p1_time(api, parent['ended_at'])
    api.require(parent['started_at'] <= parent['ended_at'], 'P1 parent interval reversed')
    command_path = output / 'COMMANDS.json'; rows = api.read_json(command_path) if command_path.is_file() else []
    api.require(isinstance(rows, list) and [r['name'] for r in rows] == p1_child_names[:len(rows)], 'P1 original command order/census differs')
    captures = sorted(trace.glob('*.json')) if trace.is_dir() else []
    api.require(len(captures) <= 17 and [p.name for p in captures] == [f'{i:04}.json' for i in range(len(captures))], 'P1 physical capture census/order differs')
    expected_trace = {f'{i:04}{suffix}' for i in range(len(captures)) for suffix in ('.json', '.log')}
    if trace.is_dir(): api.require({p.name for p in trace.iterdir()} == expected_trace, 'P1 extra/missing raw trace artifact')
    positives = set(); children = []; finite_texts = {}; returned_count = 0; previous_end = parent['started_at']; resource = parent['terminal'] != 'COMPLETED'
    for index, cap_path in enumerate(captures):
        cap = api.read_json(api.no_symlinks(cap_path)); event = plan['children'][index]
        api.keys(cap, {'index','argv','cwd','started_at','ended_at','terminal','exit_code','returned_exit_code','returned','log_sha256','source_sha256','output_hashes','input_receipt_sha256'})
        api.require(type(cap['index']) is int and cap['index'] == index, 'P1 physical child index changed')
        p1_time(api, cap['started_at']); p1_time(api, cap['ended_at'])
        api.require(previous_end <= cap['started_at'] <= cap['ended_at'] <= parent['ended_at'], 'P1 physical child interval outside parent/order'); previous_end = cap['ended_at']
        raw = api.no_symlinks(cap_path.with_suffix('.log')).read_bytes()
        original = rows[returned_count] if cap['returned'] and returned_count < len(rows) else None
        if cap['returned']: returned_count += 1
        log_path = api.no_symlinks(event['log']); log = log_path.read_bytes() if log_path.is_file() else None
        result = p1_classify(api, plan, event, cap, raw, log, original, positives)
        input_path = output / 'INPUT_RECEIPT.json'
        api.require(cap['input_receipt_sha256'] == api.sha(api.no_symlinks(input_path).read_bytes()), 'P1 captured input receipt changed')
        if result['outcome'] == 'ACCEPT':
            positives.add(event['id'])
            if event['finite']: finite_texts[event['id']] = log.decode('utf8')
            if event['axiom_count']:
                expected = [x['name'] for x in p1_meta['targets'] if (x['module'] == 'ReviewerContract') == (event['id'] == 'ReviewerContract')]
                api.require(len(expected) == event['axiom_count'], 'P1 axiom source inventory differs')
                api.check_original_readbacks(log.decode('utf8'), expected)
        resource = resource or result['outcome'] == 'RESOURCE_INCONCLUSIVE'
        children.append({**result, 'index': index, 'capture': cap, 'capture_sha256': api.sha(cap_path.read_bytes()),
            'original_row_sha256': api.canonical(original) if original is not None else None,
            'original_log_sha256': api.sha(log) if log is not None else None})
    api.require(returned_count == len(rows), 'P1 uncaptured original command row')
    outcome = 'RESOURCE_INCONCLUSIVE' if resource else 'FAILED'
    terminal_path = output / 'REPLAY_RECEIPT.json'; terminal = api.read_json(terminal_path) if terminal_path.is_file() else None
    record = {'schema': 'P1-WHOLE-COLLECTOR-1', 'outcome': outcome, 'children': children, 'not_run': p1_child_names[len(children):],
        'original_terminal_sha256': api.sha(terminal_path.read_bytes()) if terminal is not None else None,
        'input_receipt_sha256': api.sha((output / 'INPUT_RECEIPT.json').read_bytes()) if (output / 'INPUT_RECEIPT.json').is_file() else None,
        'commands_sha256': api.sha(command_path.read_bytes()) if command_path.is_file() else None,
        'trace_sha256': api._file_hashes(trace) if trace.exists() else None, 'parent': parent,
        'preflight': plan['preflight'], 'objects': {}, 'finite': None, 'copies': {}, 'scope_ceiling': p1_ceiling}
    if resource: return record
    if parent['terminal'] != 'COMPLETED' or parent['exit_code'] != 0 or len(children) != 17 or any(c['outcome'] not in {'ACCEPT','REJECT'} for c in children): return record
    api.require(terminal is not None and plan['preflight']['dependencies']['full_inventory_verified'] is True, 'P1 success lacks terminal or full inventories')
    input_value = api.read_json(output / 'INPUT_RECEIPT.json')
    api.require(input_value == plan['preflight']['input_expected'], 'P1 original/full input inventory join differs')
    expected_fields = set('status finished_utc public_manifest_sha256 accepted_source_manifest_sha256 accepted_review_receipt_sha256 public_files original_source_payloads original_review_payloads dependencies compiled_scientific_modules fresh_observer_dependency public_axiom_checks reviewer_universal_consumers author_lean_controls reviewer_lean_controls rejected_machine_mutations python_differential_cases python_seeded_boundary_cases python_behavior_mutants new_resource_inconclusive_runs author_custom_objects_reused no_input_tree_mutation control_layout_literal_copies scope commands_sha256 objects'.split())
    api.keys(terminal, expected_fields)
    expected = {**{k: v for k, v in input_value.items() if k != 'status'}, 'status': 'PASS_PORTABLE_P1_REPLAY',
        'compiled_scientific_modules': 4, 'fresh_observer_dependency': True, 'public_axiom_checks': 37, 'reviewer_universal_consumers': 4,
        'author_lean_controls': 21, 'reviewer_lean_controls': 28, 'rejected_machine_mutations': 4, 'python_differential_cases': 266760,
        'python_seeded_boundary_cases': 1593, 'python_behavior_mutants': 18, 'new_resource_inconclusive_runs': False,
        'author_custom_objects_reused': False, 'no_input_tree_mutation': True, 'control_layout_literal_copies': p1_copy_statement,
        'scope': p1_ceiling, 'commands_sha256': record['commands_sha256']}
    for key, value in expected.items(): api.require(api.canonical(terminal[key]) == api.canonical(value), 'P1 terminal contract changed: ' + key)
    from datetime import datetime
    finished = datetime.fromisoformat(terminal['finished_utc'].replace('Z','+00:00'))
    api.require(p1_time(api, parent['started_at']) <= finished <= p1_time(api, parent['ended_at']), 'P1 terminal time outside measured run')
    build = api.no_symlinks(output / 'build'); actual = {}
    for path in build.rglob('*'):
        api.no_symlinks(path)
        api.require(path.is_dir() or path.is_file(), 'Nonregular P1 build artifact')
        if path.is_file(): api.require(path.suffix == '.olean', 'Unexpected P1 compiler byproduct'); actual[path.relative_to(build).as_posix()] = api.sha(path.read_bytes())
    expected_objects = {name.replace('.','/')+'.olean' for name in p1_positive_names}
    api.require(set(actual) == expected_objects, 'P1 nine-object census differs')
    api.require(terminal['objects'] == [{'path': path, 'sha256': actual[path]} for path in sorted(actual)], 'P1 original/current object receipt differs')
    for c, event in zip(children, plan['children']):
        if event['object_path'] and c['outcome'] == 'ACCEPT': api.require(actual[Path(event['object_path']).relative_to(build).as_posix()] == c['object_sha256'], 'P1 object changed after child')
    copies = {}
    for relative, data in plan['generated_bytes'].items():
        api.require(api.path_in(output, relative).read_bytes() == data, 'P1 output-only copy changed'); copies[relative] = api.sha(data)
    finite = p1_finite(api, Path(plan['source_root']), output, finite_texts)
    created=datetime.fromisoformat(api.read_json(output/p1_finite_rel)['created_utc'].replace('Z','+00:00'))
    finite_capture=children[-1]['capture']
    api.require(p1_time(api,finite_capture['started_at'])<=created<=p1_time(api,finite_capture['ended_at']),'P1 finite report is outside its measured original child')
    summary = p1_json(api, parent_log)
    api.require(summary == {k: terminal[k] for k in ['status','public_manifest_sha256','compiled_scientific_modules','public_axiom_checks','rejected_machine_mutations']}, 'P1 parent stdout/terminal mismatch')
    record.update(outcome='ORIGINAL_COMPLETE_PENDING_SAFE_AUDIT', objects=actual, finite=finite, copies=copies)
    return record


def p1_views(api, physical, target_audits):
    api.require(physical.get('outcome') == 'ORIGINAL_COMPLETE_PENDING_SAFE_AUDIT', 'P1 views lack complete physical original run')
    api.require([x['id'] for x in physical['children']] == p1_child_names, 'P1 views omit physical children')
    api.require(len(target_audits) == 41 and {r['name'] for r in target_audits} == {t['name'] for t in p1_meta['targets']}, 'P1 views require all 41 fresh targets')
    for row in target_audits:
        api.require(row['closure_status'] == 'CHECKED_SAFE' and type(row['checked_declarations']) is int and row['checked_declarations'] > 0, 'P1 view has unsafe target closure')
        api.require(set(row['axioms']) <= api.AXIOMS, 'P1 view has unapproved axiom'); api.digest(row['type_sha256'])
    api.require(len(physical['objects']) == 9 and physical['finite']['internal_mutations'] == 18, 'P1 view census incomplete')
    shared = {k: physical[k] for k in ('trace_sha256','original_terminal_sha256','input_receipt_sha256','commands_sha256')}
    return {'formal': {**shared, 'child_ids': p1_child_names[:13], 'object_count': 9, 'proof_scope': 'COMPONENTS', 'safe_targets': 41},
        'finite': {**shared, 'child_ids': p1_finite_names, 'object_count': 0, 'proof_scope': 'FINITE', 'internal_comparisons': 18},
        'physical_runs': 1, 'view_join_new_builds': 0, 'independent_evidence_increment': 0, 'scope_ceiling': p1_ceiling}


def p1_projection_hashes(api, suite, sources):
    return {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']}


def p1_symbolize(api, value, mappings):
    if isinstance(value, dict): return {p1_symbolize(api, k, mappings): p1_symbolize(api, v, mappings) for k, v in value.items()}
    if isinstance(value, list): return [p1_symbolize(api, x, mappings) for x in value]
    if isinstance(value, str):
        for old, new in sorted(mappings, key=lambda p: len(p[0]), reverse=True): value = value.replace(old, new)
    return value


def p1_initial_receipt(api, suite, sources, reviews):
    now = api.utc(); hashes = p1_projection_hashes(api, suite, sources)
    return {'id': suite['id']+'-replay', 'suite_id': suite['id'], 'family': suite['family'], 'suite_sha256': api.canonical(suite),
        'source_hashes': hashes, 'review_hashes': {r: reviews[r]['review_sha256'] for r in suite['review_ids']},
        'toolchain_sha256': api.canonical(suite['toolchain']), 'outcome': 'NOT_RUN', 'target_readbacks': [], 'controls': [], 'stages': [],
        'invocation': ['replay_v5_successors.py','--execute','--suite',suite['id'],'--out','{out}'],
        'started_at': now, 'ended_at': now, 'exit_code': None, 'log_sha256': api.canonical({}), 'axioms': [], 'proof_scope': 'NONE',
        'replay_evidence': {'schema': p1_evidence_schema, 'recipe': p1_recipe, 'descriptor_sha256': api.canonical(suite['replay']),
            'runner_sha256': api.sha(Path(api.__file__).read_bytes()), 'source_hashes_before': hashes, 'source_hashes_after': dict(hashes),
            'driver_sha256': p1_driver, 'archive_sha256': p1_archive, 'tool_fingerprints': {}, 'dependency_checks': None,
            'private_parameters': None, 'job_sha256': None, 'runtime_plan_sha256': None, 'stage_results': [], 'physical': None, 'physical_children': [],
            'target_audits': [], 'audit_source_sha256': None, 'physical_audit': None, 'views': None, 'physical_receipt_sha256': None,
            'physical_execution_count': 0, 'new_builds': 0, 'independent_evidence_increment': 0, 'scope_ceiling': p1_ceiling}}


def p1_save_receipt(api, receipt, output):
    ev = receipt['replay_evidence']; receipt['stages'] = [{k: r[k] for k in ('id','terminal','exit_code','log_sha256')} for r in ev['stage_results']]
    receipt['log_sha256'] = api.canonical({r['id']: r['log_sha256'] for r in ev['stage_results']})
    receipt['ended_at'] = api.utc(); api.write_json(output/'RECEIPT.json', receipt)


def p1_project_suite(api, suite, sources, root, output):
    plan = p1_validate_suite(api, suite, sources, root); output = api.no_symlinks(output).resolve()
    api.require(not output.exists() and not output.is_relative_to(Path(root).resolve()), 'P1 projection requires fresh external output')
    output.mkdir(parents=True); project = output/'project'; project.mkdir()
    for name, data in plan['contents'].items():
        p = api.path_in(project,name); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
    api.write_json(output/'PLAN.json', {'suite_sha256': api.canonical(suite), 'recipe':p1_recipe, 'status':'PROJECTED_NOT_EXECUTED'})
    return {'project':str(project),'output':str(output)}


def p1_trace_entry(api, arguments):
    api.require(len(arguments) == 2, 'Malformed internal P1 trace invocation')
    path = api.no_symlinks(arguments[0]); api.require(api.sha(path.read_bytes()) == arguments[1], 'P1 private runtime job changed')
    job = api.read_json(path)
    api.keys(job, {'schema','archive','source_root','original_output','lean_root','mathlib','python','private_parameters','preflight'})
    api.require(job['schema'] == 'P1-PRIVATE-RUNTIME-JOB-1', 'Unknown P1 private runtime job')
    api.require(str(Path(sys.executable).absolute()) == job['python'], 'P1 trace interpreter spelling differs from original argv')
    pair = p1_private_parameters(api, job['private_parameters'], job['lean_root'])
    plan = p1_prepare(api, job['archive'], job['source_root'], job['original_output'], job['lean_root'], job['mathlib'], job['python'],
        pair['values']['trace_prefix'], pair['values']['pinned_trace_prefix'])
    plan.update(preflight=job['preflight'], source_root=job['source_root'])
    arguments = ['--lean-root',job['lean_root'],'--mathlib-root',job['mathlib'],'--output',job['original_output'],
        '--trace-prefix',pair['values']['trace_prefix'],'--pinned-trace-prefix',pair['values']['pinned_trace_prefix']]
    plan['source_arguments'] = arguments
    return p1_run_original(api, Path(job['source_root'])/'replay.py', arguments, plan, path.parent/'traces', runner=None)


def p1_check_tools(api, tools, output):
    api.require(set(tools) == {'lean','python','mathlib'}, 'P1 needs exactly explicit Lean, Python and Mathlib paths')
    found = {}; fingerprints = {}; env = api._clean_environment()
    for name, expected, version in [('lean',api.LEAN_SHA,'4.19.0'),('python',p1_python,'3.11.9')]:
        path = Path(tools[name]).absolute()
        if not path.is_file(): raise api.MissingTool('P1 executable is unavailable: '+name)
        api.require(api.sha(path.read_bytes()) == expected, 'P1 executable fingerprint differs')
        log = output/'logs'/('tool-'+name+'.log'); run = api.run_process([path,'--version'],output,env,log,30)
        text = log.read_text()
        api.require(run['terminal']=='COMPLETED' and run['exit_code']==0 and re.search(r'(?<![0-9.])'+re.escape(version)+r'(?![0-9.])',text), 'P1 tool version readback failed')
        if name=='lean': api.require('6caaee842e94' in text and 'x86_64-unknown-linux-gnu' in text, 'P1 official compiler build differs')
        found[name] = path
        fingerprints[name] = {'source_binding': {'kind':'TOOL_PROBE','tool_name':name,'executable_sha256':expected,'driver_sha256':p1_driver},
            'version':version,'version_log_sha256':run['log_sha256']}
    mathlib=api.no_symlinks(tools['mathlib']).resolve()
    if not mathlib.is_dir(): raise api.MissingTool('P1 Mathlib root is unavailable')
    found['mathlib']=mathlib
    return found,fingerprints,env


def p1_execute_suite(api, suite, sources, root, output, tools, inputs, scope=None, reviews=None):
    output = api.no_symlinks(output).resolve()
    api.require(not output.exists(), 'P1 output must be absent; retain previous run')
    plan = p1_validate_suite(api,suite,sources,root)
    api.require(scope is None or scope==plan['scope'], 'P1 execution scope differs from descriptor')
    api.require(isinstance(reviews,dict) and set(suite['review_ids'])<=set(reviews), 'P1 source review identities missing')
    for path in [root,*tools.values(),*inputs.values()]:
        resolved=Path(path).resolve();api.require(not output.is_relative_to(resolved) and not resolved.is_relative_to(output), 'P1 output overlaps an input')
    if plan['mode']=='FINITE_VIEW': return p1_join_finite(api,suite,sources,root,output,inputs,reviews)
    api.require(set(inputs)=={'p1-archive','p1-private-parameters'}, 'P1 external input bindings differ')
    output.mkdir(parents=True);(output/'logs').mkdir()
    api.write_json(output/'SUITE.json',suite)
    receipt=p1_initial_receipt(api,suite,sources,reviews);ev=receipt['replay_evidence'];p1_save_receipt(api,receipt,output)
    try:
        archive=api.no_symlinks(inputs['p1-archive']);api.require(api.sha(archive.read_bytes())==p1_archive,'P1 archive changed')
        extraction=output/'archive'; api.extract_source_zip(archive,extraction);source_root=extraction/p1_prefix.rstrip('/')
        api.require({p.relative_to(source_root).as_posix() for p in source_root.rglob('*') if p.is_file()}==set(p1_meta['members']),'P1 packet file census differs')
        resolved,fingerprints,env=p1_check_tools(api,tools,output);ev['tool_fingerprints']=fingerprints
        lean_root=resolved['lean'].resolve().parent.parent;mathlib=resolved['mathlib']
        private_file=api.no_symlinks(inputs['p1-private-parameters']);values=api.read_json(private_file)
        pair=p1_private_parameters(api,values,lean_root);ev['private_parameters']=pair['public']
        dependencies=p1_verify_dependencies(api,source_root,lean_root,mathlib,pair);ev['dependency_checks']=dependencies
        packet=p1_packet_expected(api,source_root)
        preflight={'input_expected':{'status':'PASS_PACKET_AND_DEPENDENCIES',**packet,'dependencies':dependencies['original_expected']},'dependencies':dependencies}
        runtime=p1_prepare(api,archive,source_root,output/'original',lean_root,mathlib,resolved['python'],values['trace_prefix'],values['pinned_trace_prefix'])
        runtime.update(preflight=preflight,source_root=str(source_root))
        job={'schema':'P1-PRIVATE-RUNTIME-JOB-1','archive':str(archive),'source_root':str(source_root),'original_output':str(output/'original'),
            'lean_root':str(lean_root),'mathlib':str(mathlib),'python':str(resolved['python']),'private_parameters':values,'preflight':preflight}
        job_path=output/'P1_RUNTIME_JOB.json';api.write_json(job_path,job);ev['job_sha256']=api.sha(job_path.read_bytes())
        # This private snapshot supports read-only receipt joins. It is never a descriptor or permission source.
        serial_plan={k:v for k,v in runtime.items() if k!='generated_bytes'}
        api.write_json(output/'P1_RUNTIME_PLAN.json',serial_plan)
        ev['runtime_plan_sha256']=api.sha((output/'P1_RUNTIME_PLAN.json').read_bytes())
        log=output/'logs/original.log';launch=[resolved['python'],'-B',Path(api.__file__).resolve(),'--trace-p1-original',job_path,ev['job_sha256']]
        ev['physical_execution_count']=1
        parent=api.run_process(launch,source_root,env,log,plan['parent_timeout_seconds'])
        if parent['terminal']!='COMPLETED': receipt.update(outcome='RESOURCE_INCONCLUSIVE',exit_code=1)
        ev['stage_results'].append({'id':'p1-original',**parent,'argv':['{tool:python}','-B','{adapter}','--trace-p1-original','{out}/P1_RUNTIME_JOB.json',ev['job_sha256']],
            'source_argv':plan['source_argv'],'cwd':'{archive:p1}','timeout_seconds':7200})
        physical=p1_collect(api,runtime,output/'original',output/'traces',parent,log.read_bytes())
        mapping=[(str(source_root),'{archive:p1}'),(str(output),'{out}'),(str(lean_root),'{tool:lean-root}'),(str(mathlib),'{dependency:mathlib}'),
            (str(lean_root/'bin/lean'),'{tool:lean}'),(str(resolved['python']),'{tool:python}')]
        # Source readback/public command spellings stay exact; no log/science bytes are rewritten.
        public=p1_symbolize(api,physical,mapping);ev['physical']=public;ev['physical_children']=public['children']
        if physical['outcome']=='RESOURCE_INCONCLUSIVE': receipt.update(outcome='RESOURCE_INCONCLUSIVE',exit_code=1);raise ValueError('P1 original resource-inconclusive')
        api.require(physical['outcome']=='ORIGINAL_COMPLETE_PENDING_SAFE_AUDIT','P1 original did not complete its entire source contract')
        ev['new_builds']=9
        targets=plan['audit_targets'];generated=output/'generated';generated.mkdir();audit=generated/'P1CheckedReadback.lean'
        audit.write_text(p1_audit_source(api,targets),encoding='utf8');ev['audit_source_sha256']=api.sha(audit.read_bytes())
        cache=api.read_json(source_root/'dependencies/MATHLIB_CACHE_PIN.json')
        audit_env=dict(env);audit_env['LEAN_PATH']=os.pathsep.join([str(output/'original/build')]+[str(mathlib/p) for p in cache['roots']])
        audit_log=output/'logs/target-audit.log';audit_run=api.run_process([resolved['lean'],'-j1',audit],source_root,audit_env,audit_log,300)
        ev['stage_results'].append({'id':'_target_audit',**audit_run,'argv':['{tool:lean}','-j1','{out}/generated/P1CheckedReadback.lean'],
            'source_argv':None,'cwd':'{archive:p1}','timeout_seconds':300})
        ev['physical_audit']=ev['stage_results'][-1]
        if audit_run['terminal']!='COMPLETED' or p1_resource.search(audit_log.read_text(errors='replace')):
            receipt.update(outcome='RESOURCE_INCONCLUSIVE',exit_code=1);raise ValueError('P1 target audit resource-inconclusive')
        api.require(audit_run['exit_code']==0,'P1 target closure audit failed')
        audited=api.parse_readbacks(audit_log.read_text(),targets)
        ev['target_audits']=[{'target_id':tid,**value,'log_sha256':audit_run['log_sha256']} for tid,value in audited.items()]
        ev['views']=p1_views(api,public,ev['target_audits'])
        # Re-read the current exact packet, dependency inventories and original products after audit.
        api.require(p1_packet_expected(api,source_root)==packet,'P1 packet changed during execution')
        api.require(p1_verify_dependencies(api,source_root,lean_root,mathlib,pair)==dependencies,'P1 dependency changed during execution')
        again=p1_collect(api,runtime,output/'original',output/'traces',parent,log.read_bytes())
        api.require(again==physical,'P1 original evidence changed during audit')
        api.require(api.sha(archive.read_bytes())==p1_archive and api.read_json(private_file)==values,'P1 external inputs changed')
        for name in ('lean','python'):api.require(api.sha(resolved[name].read_bytes())==fingerprints[name]['source_binding']['executable_sha256'],'P1 tool changed')
        ev['source_hashes_after']=p1_projection_hashes(api,suite,sources)
        for row in plan['files']:api.require(api.public_bytes(root,sources[row['source_id']])==plan['contents'][row['path']],'P1 public source changed')
        children={c['id']:c for c in public['children']}
        for control in suite['controls']:
            child=children[control['id'][3:]];cap=child['capture']
            receipt['controls'].append({k:control[k] for k in ('id','source_id','target_id','role','expected_outcome_sha256')}|{
                'actual_outcome':child['outcome'],'actual_outcome_sha256':api.sha(child['outcome'].encode()),'terminal':cap['terminal'],'exit_code':cap['exit_code'],'log_sha256':cap['log_sha256']})
        receipt['target_readbacks']=[{'target_id':t['id'],'source_id':t['source_id'],'target_sha256':t['target_sha256'],'outcome':'CHECKED'} for t in suite['targets']]
        receipt['axioms']=sorted({a for row in ev['target_audits'] for a in row['axioms']})
        receipt.update(outcome='FRESH_KERNEL_COMPONENTS',proof_scope='COMPONENTS',exit_code=0)
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        api.write_json(output/'FAILURE.json',{'kind':type(error).__name__,'message':str(error),'scope':'PRIVATE_DIAGNOSTIC'})
        if receipt['outcome']!='RESOURCE_INCONCLUSIVE': receipt.update(outcome='BLOCKED_TOOLCHAIN' if isinstance(error,api.MissingTool) else 'FAILED',exit_code=2 if isinstance(error,api.MissingTool) else 1)
        receipt['proof_scope']='NONE'
        # Raw children and incomplete captures remain in the private output even if collection fails.
    p1_save_receipt(api,receipt,output);p1_validate_receipt(api,receipt,suite,sources,root);return receipt


def p1_validate_receipt(api, receipt, suite, sources, root):
    plan=p1_validate_suite(api,suite,sources,root)
    try:
        api.keys(receipt,{'id','suite_id','family','suite_sha256','source_hashes','review_hashes','toolchain_sha256','outcome','target_readbacks','controls','stages','invocation','started_at','ended_at','exit_code','log_sha256','axioms','proof_scope','replay_evidence'})
        ev=receipt['replay_evidence']
        fields={'schema','recipe','descriptor_sha256','runner_sha256','source_hashes_before','source_hashes_after','driver_sha256','archive_sha256','tool_fingerprints','dependency_checks','private_parameters','job_sha256','runtime_plan_sha256','stage_results','physical','physical_children','target_audits','audit_source_sha256','physical_audit','views','physical_receipt_sha256','physical_execution_count','new_builds','independent_evidence_increment','scope_ceiling'}
        api.keys(ev,fields);api.require(ev['schema']==p1_evidence_schema and ev['recipe']==p1_recipe and ev['scope_ceiling']==p1_ceiling,'Unknown P1 receipt contract')
        api.require(receipt['suite_id']==suite['id'] and receipt['family']==suite['family'] and receipt['suite_sha256']==api.canonical(suite),'P1 receipt belongs to another suite')
        api.require(receipt['toolchain_sha256']==api.canonical(suite['toolchain']) and ev['descriptor_sha256']==api.canonical(suite['replay']),'P1 descriptor/toolchain receipt differs')
        hashes=p1_projection_hashes(api,suite,sources)
        api.require(receipt['source_hashes']==ev['source_hashes_before']==ev['source_hashes_after']==hashes,'P1 source receipt changed')
        api.require(set(receipt['review_hashes'])==set(suite['review_ids']),'P1 review identity inventory differs')
        for h in receipt['review_hashes'].values():api.digest(h)
        api.require(ev['driver_sha256']==p1_driver and ev['archive_sha256']==p1_archive and type(ev['independent_evidence_increment']) is int and ev['independent_evidence_increment']==0,'P1 original identity or independence changed')
        api.require(type(ev['physical_execution_count']) is int and ev['physical_execution_count'] in (0,1) and type(ev['new_builds']) is int and 0<=ev['new_builds']<=9,'P1 physical counts are not measured integers')
        api.digest(ev['runner_sha256']);p1_time(api,receipt['started_at']);p1_time(api,receipt['ended_at'])
        api.require(receipt['started_at']<=receipt['ended_at'],'P1 receipt interval reversed')
        api.require(receipt['invocation']==['replay_v5_successors.py','--execute','--suite',suite['id'],'--out','{out}'],'P1 receipt invocation changed')
        stages=ev['stage_results'];api.require(isinstance(stages,list) and [r['id'] for r in stages] in [[],['p1-original'],['p1-original','_target_audit'],['p1-view-join']],'P1 stage ledger differs')
        for row in stages:
            api.keys(row,{'id','terminal','exit_code','started_at','ended_at','log_sha256','argv','source_argv','cwd','timeout_seconds'})
            api.digest(row['log_sha256']);p1_time(api,row['started_at']);p1_time(api,row['ended_at'])
            api.require(receipt['started_at']<=row['started_at']<=row['ended_at']<=receipt['ended_at'],'P1 stage interval differs')
            api.require(row['terminal'] in {'COMPLETED','TIMEOUT','INTERRUPTED','MISSING'},'Unknown P1 terminal')
            api.require((row['terminal']=='COMPLETED' and type(row['exit_code']) is int and 0<=row['exit_code']<124) or (row['terminal']!='COMPLETED' and row['exit_code'] is None),'Invalid P1 stage exit')
            contracts={'p1-original':(['{tool:python}','-B','{adapter}','--trace-p1-original','{out}/P1_RUNTIME_JOB.json',ev['job_sha256']],plan['source_argv'],'{archive:p1}',7200),
                '_target_audit':(['{tool:lean}','-j1','{out}/generated/P1CheckedReadback.lean'],None,'{archive:p1}',300),
                'p1-view-join':(['{builtin:p1-view-join}','{input:p1-physical-receipt}'],None,'.',30)}
            api.require((row['argv'],row['source_argv'],row['cwd'],row['timeout_seconds'])==contracts[row['id']],'P1 actual parent/audit/join invocation differs')
        api.require(receipt['stages']==[{k:r[k] for k in ('id','terminal','exit_code','log_sha256')} for r in stages],'P1 top-level stage summary differs')
        api.require(receipt['log_sha256']==api.canonical({r['id']:r['log_sha256'] for r in stages}),'P1 stage log identity differs')
        success=receipt['outcome'] in {'FRESH_KERNEL_COMPONENTS','FINITE_ONLY'}
        api.require(receipt['outcome'] in {'NOT_RUN','FAILED','RESOURCE_INCONCLUSIVE','BLOCKED_TOOLCHAIN','BLOCKED_EXTERNAL_INPUT','FRESH_KERNEL_COMPONENTS','FINITE_ONLY'},'Unknown P1 outcome')
        if not success:
            api.require(receipt['proof_scope']=='NONE' and receipt['exit_code'] in (None,1,2),'P1 failure gained proof credit')
            api.require(not receipt['target_readbacks'] and not receipt['controls'],'P1 failure cannot carry qualified target/control rows')
            return {'suite_id':suite['id'],'outcome':receipt['outcome'],'scope':'P1_FAILED_OR_PARTIAL_ATTEMPT_ONLY'}
        api.require(receipt['exit_code']==0 and receipt['proof_scope']==plan['scope'],'P1 successful view scope differs')
        for k in ('job_sha256','runtime_plan_sha256','audit_source_sha256'):api.digest(ev[k])
        api.require(ev['audit_source_sha256']==api.sha(p1_audit_source(api,plan['audit_targets']).encode()),'P1 independent target audit source changed')
        private=ev['private_parameters'];api.keys(private,{'kind','current_sha256','reference_sha256','reference_owner_sha256','reference_derivation','dependency_bytes_written'})
        api.require(private['kind']=='PAIRED_PRIVATE_TRACE_STRINGS' and private['reference_owner_sha256']==p1_reference_owner and private['reference_derivation']=='LEAN_LITERAL_PARENT_PARENT_WITH_TRAILING_SLASH' and private['dependency_bytes_written'] is False,'P1 private argument derivation changed')
        api.digest(private['current_sha256']);api.digest(private['reference_sha256'])
        empty=api.sha(b'');api.require((private['current_sha256']==empty and private['reference_sha256']==empty) or (private['current_sha256']!=empty and private['reference_sha256']==p1_reference_prefix_sha),'P1 private arguments are unpaired/not source-derived')
        physical=ev['physical'];api.require(isinstance(physical,dict),'Missing P1 physical evidence')
        api.keys(physical,{'schema','outcome','children','not_run','original_terminal_sha256','input_receipt_sha256','commands_sha256','trace_sha256','parent','preflight','objects','finite','copies','scope_ceiling'})
        api.require(physical['schema']=='P1-WHOLE-COLLECTOR-1' and physical['scope_ceiling']==p1_ceiling and physical['outcome']=='ORIGINAL_COMPLETE_PENDING_SAFE_AUDIT' and physical['not_run']==[],'Incomplete P1 whole physical collector')
        for field in ('original_terminal_sha256','input_receipt_sha256','commands_sha256','trace_sha256'):api.digest(physical[field])
        api.require(ev['physical_children']==physical['children'] and [c['id'] for c in physical['children']]==p1_child_names,'P1 physical child inventory differs')
        api.require(physical['preflight']['dependencies']==ev['dependency_checks'] and ev['dependency_checks']['full_inventory_verified'] is True and ev['dependency_checks']['dependency_bytes_written'] is False,'P1 full dependency inventory receipt missing')
        dep=ev['dependency_checks'];api.keys(dep,{'original_expected','compiler_inventory_sha256','cache_inventory_sha256','source_inventory_sha256','comparison','full_inventory_verified','dependency_bytes_written'})
        api.keys(physical['preflight'],{'input_expected','dependencies'})
        api.require(physical['preflight']['input_expected']=={'status':'PASS_PACKET_AND_DEPENDENCIES',**p1_meta['packet_expected'],'dependencies':dep['original_expected']},'P1 input/packet/full-inventory association differs')
        for field in ('compiler_inventory_sha256','cache_inventory_sha256','source_inventory_sha256'):api.digest(dep[field])
        expected=dep['original_expected'];api.require(expected['lean_distribution']['entries']==5065 and expected['mathlib_cache']['entries']==34230 and expected['source_records']==6816 and expected['pin_manifests']==p1_pins and expected['official_precompiled_cache_trusted'] is True and expected['proof_dependencies_rebuilt'] is False,'P1 dependency counts/policy changed')
        api.keys(expected,{'lean_distribution','mathlib_cache','source_records','pin_manifests','official_precompiled_cache_trusted','proof_dependencies_rebuilt'})
        for kind in ('lean_distribution','mathlib_cache'):api.keys(expected[kind],{'entries','exact_except_trace_paths'})
        api.require(expected['lean_distribution']['exact_except_trace_paths']==[],'P1 compiler inventory cannot relocate proof bytes')
        comparison=dep['comparison'];api.keys(comparison,{'files','current_string_sha256','reference_string_sha256','dependency_bytes_written','full_inventory_verified','scope'})
        api.require(comparison['current_string_sha256']==private['current_sha256'] and comparison['reference_string_sha256']==private['reference_sha256'] and comparison['dependency_bytes_written'] is False and comparison['full_inventory_verified'] is False and comparison['scope']=='FIVE_TRACE_METADATA_COMPARISONS_ONLY','P1 trace metadata comparison scope changed')
        pins={r['path']:r for r in p1_meta['trace_pins']};api.require([r['path'] for r in comparison['files']]==sorted(pins),'P1 trace comparison inventory differs')
        changed=[]
        for row in comparison['files']:
            api.keys(row,{'path','source_sha256','source_bytes','derived_sha256','derived_bytes','pinned_sha256','replacement_count'});pin=pins[row['path']]
            api.require(row['derived_sha256']==row['pinned_sha256']==pin['original_pin_sha256'] and row['derived_bytes']==pin['original_pin_bytes'],'P1 trace comparison missed original pin')
            api.require(type(row['source_bytes']) is int and row['source_bytes']>=0 and type(row['replacement_count']) is int and row['replacement_count'] in (0,1),'Invalid P1 trace replacement census');api.digest(row['source_sha256'])
            if row['replacement_count']:changed.append(row['path'])
            else:api.require(row['source_sha256']==row['derived_sha256'] and row['source_bytes']==row['derived_bytes'],'P1 zero-replacement comparison changed bytes')
        api.require(expected['mathlib_cache']['exact_except_trace_paths']==changed,'P1 cache/trace comparison join differs')
        api.require(set(ev['tool_fingerprints'])=={'lean','python'},'P1 tool check inventory differs')
        for name,row in ev['tool_fingerprints'].items():
            api.keys(row,{'source_binding','version','version_log_sha256'});p1_source_binding(api,row['source_binding'],sources,None)
            api.require(row['version']==('4.19.0' if name=='lean' else '3.11.9'),'P1 tool version differs');api.digest(row['version_log_sha256'])
        previous=physical['parent']['started_at'];accepted=set();objects={};by_child={}
        for expected,child in zip(plan['children'],physical['children']):
            api.keys(child,{'id','outcome','semantic_outcome','rejecting_subprocesses','scope','object_sha256','derivation','mutation_census_credit','index','capture','capture_sha256','original_row_sha256','original_log_sha256'})
            cap=child['capture'];api.keys(cap,{'index','argv','cwd','started_at','ended_at','terminal','exit_code','returned_exit_code','returned','log_sha256','source_sha256','output_hashes','input_receipt_sha256'})
            api.require(child['index']==cap['index']==expected['index'] and cap['argv']==expected['argv'] and cap['cwd']==expected['cwd'],'P1 actual child invocation differs')
            api.require(cap['source_sha256']==expected['source_binding']['source_sha256'] and cap['input_receipt_sha256']==physical['input_receipt_sha256'],'P1 child/source/input association differs')
            api.require(cap['terminal']=='COMPLETED' and cap['returned'] is True and type(cap['exit_code']) is int and cap['exit_code']==cap['returned_exit_code']==expected['expected_exit_code'],'P1 actual child terminal differs')
            p1_time(api,cap['started_at']);p1_time(api,cap['ended_at']);api.require(previous<=cap['started_at']<=cap['ended_at']<=physical['parent']['ended_at'],'P1 serial child timing differs');previous=cap['ended_at']
            outcome='REJECT' if expected['expected_exit_code'] else 'ACCEPT'
            api.require(child['outcome']==child['semantic_outcome']==outcome and child['rejecting_subprocesses']==int(outcome=='REJECT') and child['scope']==expected['scope'] and child['mutation_census_credit'] is None,'P1 child semantic scope changed')
            api.require(set(expected['positive_prerequisites'])<=accepted,'P1 rejection precedes all nine positives')
            if outcome=='ACCEPT':accepted.add(child['id'])
            for field in ('capture_sha256','original_row_sha256','original_log_sha256'):api.digest(child[field])
            api.digest(cap['log_sha256']);derivation=child['derivation'];api.require(derivation['source_sha256']==cap['log_sha256'] and derivation['derived_sha256']==child['original_log_sha256'] and derivation['science_bytes_changed'] is False and derivation['source_owned_timeout_suffix'] is False,'P1 raw/neutral log association changed')
            if expected['object_path'] and outcome=='ACCEPT':
                api.digest(child['object_sha256']);key='{out}/'+expected['object_path'];api.require(cap['output_hashes']=={key:child['object_sha256']},'P1 child object binding changed')
                objects[expected['object_path'].removeprefix('original/build/')]=child['object_sha256']
            else:api.require(cap['output_hashes']=={} and child['object_sha256'] is None,'P1 rejection/finite observation gained object credit')
            by_child[child['id']]=child
        api.require(objects==physical['objects'] and len(objects)==9,'P1 physical object census changed')
        api.require(physical['copies']=={p1_copy_control:p1_meta['members']['reviewer/independent_source_controls.py']['sha256'],**{name:p1_source for name in p1_copy_codecs}},'P1 exact compatibility-copy census changed')
        finite=physical['finite'];api.require(finite['internal_mutations']==18 and len(finite['internal_mutation_record_sha256'])==18 and finite['rejecting_subprocesses']==0 and finite['scope']=='FINITE_ONLY' and finite['scope_ceiling']==p1_ceiling,'P1 internal comparisons gained process/proof credit')
        api.keys(finite,{'source_shape','source_contract_tests','source_text_mutations','edge_cases','edge_outside_domain','differential_cases','seeded_boundary_cases','internal_mutations','internal_mutation_record_sha256','outside_domain','finite_receipt_sha256','rejecting_subprocesses','scope','scope_ceiling'})
        for key,want in {'source_contract_tests':2,'source_text_mutations':5,'edge_cases':26,'edge_outside_domain':4,'differential_cases':266760,'seeded_boundary_cases':1593,'internal_mutations':18,'outside_domain':11,'rejecting_subprocesses':0}.items():
            api.require(type(finite[key]) is int and finite[key]==want,'P1 finite source-owned census changed')
        api.require(finite['source_shape']=='IDENTITY_ONLY','P1 shape check became semantic proof');api.digest(finite['finite_receipt_sha256'])
        for h in finite['internal_mutation_record_sha256']:api.digest(h)
        api.require(ev['views']==p1_views(api,physical,ev['target_audits']),'P1 views do not join the same run')
        audit=ev['physical_audit'];api.keys(audit,{'id','terminal','exit_code','started_at','ended_at','log_sha256','argv','source_argv','cwd','timeout_seconds'})
        api.require(audit['id']=='_target_audit' and audit['terminal']=='COMPLETED' and type(audit['exit_code']) is int and audit['exit_code']==0 and
            (audit['argv'],audit['source_argv'],audit['cwd'],audit['timeout_seconds'])==(['{tool:lean}','-j1','{out}/generated/P1CheckedReadback.lean'],None,'{archive:p1}',300),'P1 physical audit invocation differs')
        p1_time(api,audit['started_at']);p1_time(api,audit['ended_at']);api.digest(audit['log_sha256'])
        api.require(physical['parent']['ended_at']<=audit['started_at']<=audit['ended_at']<=receipt['ended_at'],'P1 safe audit did not follow the physical run')
        api.require(len(ev['target_audits'])==len(plan['audit_targets']),'P1 target audit census differs')
        for actual,expected in zip(ev['target_audits'],plan['audit_targets']):
            api.keys(actual,{'target_id','name','type_sha256','axioms','closure_status','checked_declarations','log_sha256'})
            api.require(actual['target_id']==expected['target_id'] and actual['name']==expected['name'] and actual['log_sha256']==audit['log_sha256'],'P1 target audit/log/owner association differs')
        api.require(receipt['axioms']==sorted({a for row in ev['target_audits'] for a in row['axioms']}),'P1 target axiom summary differs')
        api.require(receipt['target_readbacks']==[{'target_id':t['id'],'source_id':t['source_id'],'target_sha256':t['target_sha256'],'outcome':'CHECKED'} for t in suite['targets']],'P1 target source bindings differ')
        api.require(len(receipt['controls'])==len(suite['controls']),'P1 complete control inventory missing')
        for actual,expected in zip(receipt['controls'],suite['controls']):
            child=by_child[expected['id'][3:]];cap=child['capture']
            want={k:expected[k] for k in ('id','source_id','target_id','role','expected_outcome_sha256')}|{'actual_outcome':child['outcome'],'actual_outcome_sha256':api.sha(child['outcome'].encode()),'terminal':cap['terminal'],'exit_code':cap['exit_code'],'log_sha256':cap['log_sha256']}
            api.require(actual==want,'P1 control/physical child association differs')
        if plan['mode']=='PHYSICAL':
            api.require(receipt['outcome']=='FRESH_KERNEL_COMPONENTS' and ev['physical_execution_count']==1 and ev['new_builds']==9 and ev['physical_receipt_sha256'] is None,'P1 physical execution credit changed')
            api.require([r['id'] for r in stages]==['p1-original','_target_audit'] and all(r['terminal']=='COMPLETED' and r['exit_code']==0 for r in stages),'P1 physical/audit stages incomplete')
            api.require(physical['parent']=={k:stages[0][k] for k in ('terminal','exit_code','started_at','ended_at','log_sha256')},'P1 physical parent association changed')
            api.require(ev['physical_audit']==stages[1],'P1 target audit stage differs from physical audit')
        else:
            api.require(receipt['outcome']=='FINITE_ONLY' and ev['physical_execution_count']==0 and ev['new_builds']==0 and [r['id'] for r in stages]==['p1-view-join'],'P1 finite view re-executed or gained proof credit')
            api.digest(ev['physical_receipt_sha256'])
        return {'suite_id':suite['id'],'outcome':receipt['outcome'],'scope':'SOURCE_BOUND_P1_PHYSICAL_OR_ZERO_BUILD_VIEW'}
    except (KeyError,TypeError,AttributeError) as exc:raise ValueError('Malformed P1 receipt: '+str(exc)) from exc


def p1_join_finite(api,suite,sources,root,output,inputs,reviews):
    api.require(set(inputs)=={'p1-physical-receipt'},'P1 finite view requires one exact existing physical receipt')
    output=api.no_symlinks(output).resolve();api.require(not output.exists(),'P1 view output must be absent')
    source_receipt=api.no_symlinks(inputs['p1-physical-receipt']);prior_output=source_receipt.parent
    api.require(source_receipt.name=='RECEIPT.json' and not output.is_relative_to(prior_output),'P1 finite join location differs')
    physical_receipt=api.read_json(source_receipt);prior_suite=api.read_json(api.path_in(prior_output,'SUITE.json'))
    api.require(prior_suite['replay']['mode']=='PHYSICAL','P1 view cannot join another view')
    p1_validate_receipt(api,physical_receipt,prior_suite,sources,root)
    api.require(physical_receipt['outcome']=='FRESH_KERNEL_COMPONENTS','P1 finite view requires complete successful original and safe audit')
    ev=physical_receipt['replay_evidence'];job_path=api.path_in(prior_output,'P1_RUNTIME_JOB.json');plan_path=api.path_in(prior_output,'P1_RUNTIME_PLAN.json')
    api.require(api.sha(job_path.read_bytes())==ev['job_sha256'] and api.sha(plan_path.read_bytes())==ev['runtime_plan_sha256'],'P1 original runtime metadata changed')
    job=api.read_json(job_path);runtime=api.read_json(plan_path);source_root=api.no_symlinks(job['source_root'])
    api.require(Path(job['original_output'])==prior_output/'original' and source_root==prior_output/'archive'/p1_prefix.rstrip('/'),'P1 original output/packet root moved')
    p1_packet_expected(api,source_root)
    runtime['generated_bytes']={p1_copy_control:api.path_in(source_root,'reviewer/independent_source_controls.py').read_bytes(),
        **{p:api.path_in(source_root,'source/prcodec.py').read_bytes() for p in p1_copy_codecs}}
    original_stage=ev['stage_results'][0];parent={k:original_stage[k] for k in ('terminal','exit_code','started_at','ended_at','log_sha256')}
    record=p1_collect(api,runtime,prior_output/'original',prior_output/'traces',parent,api.path_in(prior_output,'logs/original.log').read_bytes())
    mapping=[(str(source_root),'{archive:p1}'),(str(prior_output),'{out}'),(job['lean_root'],'{tool:lean-root}'),(job['mathlib'],'{dependency:mathlib}'),
        (str(Path(job['lean_root'])/'bin/lean'),'{tool:lean}'),(job['python'],'{tool:python}')]
    api.require(p1_symbolize(api,record,mapping)==ev['physical'],'P1 view differs from current original capture/products')
    audit=api.path_in(prior_output,'generated/P1CheckedReadback.lean');audit_log=api.path_in(prior_output,'logs/target-audit.log')
    api.require(api.sha(audit.read_bytes())==ev['audit_source_sha256'] and audit.read_text()==p1_audit_source(api,prior_suite['replay']['audit_targets']),'P1 fresh target audit source changed')
    api.require(api.sha(audit_log.read_bytes())==ev['stage_results'][1]['log_sha256'],'P1 fresh target log changed')
    audits=api.parse_readbacks(audit_log.read_text(),prior_suite['replay']['audit_targets'])
    api.require([{'target_id':tid,**value,'log_sha256':api.sha(audit_log.read_bytes())} for tid,value in audits.items()]==ev['target_audits'],'P1 safe audit join differs')
    # All operations above are reads; the view starts no process and produces no object.
    started=api.utc();output.mkdir(parents=True);(output/'logs').mkdir();api.write_json(output/'SUITE.json',suite)
    receipt=p1_initial_receipt(api,suite,sources,reviews);view=receipt['replay_evidence']
    for key in ('driver_sha256','archive_sha256','tool_fingerprints','dependency_checks','private_parameters','job_sha256','runtime_plan_sha256','physical','physical_children','target_audits','audit_source_sha256','physical_audit','views'):
        view[key]=ev[key]
    view['physical_receipt_sha256']=api.sha(source_receipt.read_bytes());view['physical_execution_count']=0;view['new_builds']=0
    log=output/'logs/view-join.log';log.write_text('P1 finite view joined the exact original receipt, current capture, objects, copies and safe audit; zero new processes or builds.\n')
    view['stage_results']=[{'id':'p1-view-join','argv':['{builtin:p1-view-join}','{input:p1-physical-receipt}'],'source_argv':None,'cwd':'.','timeout_seconds':30,
        'terminal':'COMPLETED','exit_code':0,'started_at':receipt['started_at'],'ended_at':api.utc(),'log_sha256':api.sha(log.read_bytes())}]
    receipt['controls']=[{**c,'target_id':suite['targets'][0]['id']} for c in physical_receipt['controls'] if c['id'][3:] in p1_finite_names]
    receipt['target_readbacks']=[{'target_id':t['id'],'source_id':t['source_id'],'target_sha256':t['target_sha256'],'outcome':'CHECKED'} for t in suite['targets']]
    receipt['axioms']=physical_receipt['axioms'];receipt.update(outcome='FINITE_ONLY',proof_scope='FINITE',exit_code=0)
    p1_save_receipt(api,receipt,output);p1_validate_receipt(api,receipt,suite,sources,root);return receipt
