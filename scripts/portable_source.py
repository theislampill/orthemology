"""Private portable-wrapper helpers proposed against the frozen D03 adapter.

These helpers have no command-line entry point and do not admit a public recipe.
Only an already-reviewed caller may install the tracer around an original run.
No proof qualification or shared-view receipt is produced by this module.
"""
from pathlib import Path
from io import BytesIO
import ast
import json
import re
import stat
import subprocess
import zipfile

REVIEW_ARCHIVE_SHA = 'a7dac7ac8fe8e867b4581ebcd2757067371985eb728a66fc83720e33389c8f9b'
PORTABLE_WRAPPER_SHA = '3f2bcdbac6726d5924aa193b250a43c91474bca3f1cd1a22568f760f224169a3'
DERIVED_LITERAL_SHA = '38b5486e26fcd245a92e3e7d1673c9ce06c8c7d293973ab565a2a79ba841237b'
PYTHON_SHA = 'd1483a82342508f2ec2b172b788d5b676a59eaf70ed01ae846a0f84f63a3a82a'
FILES = {
    'REVIEW_MANIFEST.json': '94b983318333e8bd79f08ba2e43f72add2f561629b3b54b05a37faed42d70abf',
    'replay_review.py': '210480b01a6a14f8458541ccb34d782f7bf87536aaf11df4751aff62addb5da4',
    'replay_literal_independent.py': '20619379878a206a38f88fbb193fed7fb1ec8f494137aa806b2d04e382fcd6c6',
    'snapshot/verify_dependency_identity.py': '7deeab885edfa67829f733766a1d8e9f08439157dec5bd54f05681371ed0e10e',
    'snapshot/DEPENDENCY_PINS.json': '9eaffaa788991447cf64938183de0e982b467d333dd9a369f11c0c99a0be595c',
    'snapshot/SOURCE_MANIFEST.json': '8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c',
    'literal-snapshot/SOURCE_MANIFEST.json': '81d7bec2f6bf584d62f5cac7aa32773870dcff4ca33d8d53d5c84cec765f63e4',
    'literal-snapshot/check_literal_native.py': '15ad3c3ef916810047f18dad43e465b6194276e0272f98063bfe3d63862a1b95',
    'literal-snapshot/prcodec.py': 'dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c',
}
RESOURCE = re.compile(r'\btimeout\b|WALL_TIMEOUT|RESOURCE_LIMIT|maximum number of heartbeats|maximum recursion depth|out of memory', re.I)
INFRASTRUCTURE = re.compile(r'unknown module|unknown constant|unknown identifier|no such file|file not found|failed to read file|object file .* does not exist', re.I)
MISMATCH = ('error: application type mismatch', 'η ≤ ε : Prop', 'η ≤ ε / 2 : Prop')


def _archive_members(api, archive):
    data = api.no_symlinks(archive).read_bytes()
    api.require(api.sha(data) == REVIEW_ARCHIVE_SHA, 'Original review archive identity differs')
    with zipfile.ZipFile(BytesIO(data)) as source:
        infos = source.infolist()
        names = [item.filename for item in infos]
        api.require(len(names) == len(set(names)) == 737, 'Original review archive census differs')
        for item in infos:
            api.relative(item.filename)
            mode = item.external_attr >> 16
            api.require(not item.is_dir() and not (stat.S_ISLNK(mode) or stat.S_ISCHR(mode) or stat.S_ISBLK(mode)), 'Nonregular review archive member')
            api.require(not item.filename.endswith(('.olean', '.ilean', '.pyc', '.o', '.a')), 'Compiled original custom input')
        members = {name: source.read(name) for name in names}
    for name, expected in FILES.items():
        api.require(api.sha(members[name]) == expected, 'Reviewed helper or manifest differs: ' + name)
    manifest = json.loads(members['REVIEW_MANIFEST.json'])
    records = manifest['files']
    api.require(len({row['path'] for row in records}) == len(records), 'Repeated original manifest member')
    api.require({row['path'] for row in records} | {'REVIEW_MANIFEST.json', 'REVIEW_MANIFEST.sha256'} == set(members), 'Review manifest/member census differs')
    for row in records:
        data = members[row['path']]
        api.require(type(row['bytes']) is int and len(data) == row['bytes'] and api.sha(data) == row['sha256'], 'Original review source bytes differ')
    api.require(members['REVIEW_MANIFEST.sha256'].decode().split()[0] == FILES['REVIEW_MANIFEST.json'], 'Review checksum declaration differs')
    return members


def _module_order(api, members, namespace, target, count):
    prefix = 'snapshot/' + namespace + '/src/'
    by_name = {name[len(prefix):-5].replace('/', '.'): name for name in members if name.startswith(prefix) and name.endswith('.lean')}
    order = []; seen = set()
    def visit(name, trail):
        api.require(name not in trail, 'Original import cycle')
        if name in seen: return
        for imported in api.imports(members[by_name[name]].decode()):
            if imported in by_name: visit(imported, trail | {name})
            else: api.require(imported.startswith(('Mathlib', 'Lean', 'Std', 'Init')), 'Unreviewed official import')
        seen.add(name); order.append((name, by_name[name]))
    visit(target, set())
    api.require(len(order) == len(by_name) == count, 'Original closure census differs')
    return order


def build_plan(api, archive, out, lean, mathlib, python):
    """Read exact original bytes; produce an internal ordered process plan."""
    members = _archive_members(api, archive)
    out = api.no_symlinks(out).absolute()
    lean = api.no_symlinks(lean).resolve(); mathlib = api.no_symlinks(mathlib).resolve()
    # Match the accepted tool verifier: preserve the explicit interpreter path
    # (including a venv symlink) after checking the actual executable bytes.
    # The original finite child uses sys.executable with that exact spelling.
    python = Path(python).absolute()
    api.require(python.is_file() and api.sha(python.read_bytes()) == PYTHON_SHA, 'Wrong pinned Python executable')
    api.require(lean.is_file() and api.sha(lean.read_bytes()) == api.LEAN_SHA, 'Wrong pinned Lean executable')
    snapshot = out / 'review-source'
    libs = [mathlib / '.lake/build/lib/lean'] + sorted((mathlib / '.lake/packages').glob('*/.lake/build/lib/lean'))
    suffix = [str(path) for path in libs]
    events = []; children = []
    def readonly(argv, text):
        events.append({'readonly': True, 'argv': [str(x) for x in argv], 'text': text})
    def dependencies():
        for package in json.loads(members['snapshot/DEPENDENCY_PINS.json'])['packages']:
            path = mathlib if package['name'] == 'mathlib' else mathlib / '.lake/packages' / package['name']
            for tail, text in [(['rev-parse', 'HEAD'], True), (['status', '--porcelain', '--untracked-files=all'], True), (['ls-files', '-z'], False)]:
                readonly(['git', '-C', path, *tail], text)
    def child(namespace, label, member, root_member, obj=None, timeout=180, negative=False):
        source = snapshot / member
        object_path = out / obj if obj else None
        argv = [str(lean), '-j1', '--root=' + str(snapshot / root_member)]
        if object_path: argv += ['-o', str(object_path)]
        argv.append(str(source))
        prefixes = [out / 'core' / namespace / 'build'] if namespace != 'literal' else [out / 'literal/build', out / 'core/runtime/build']
        event = {'readonly': False, 'id': namespace + '/' + label, 'argv': argv,
                 'cwd': str(snapshot), 'timeout': timeout, 'source_path': str(source),
                 'source_sha256': api.sha(members[member]), 'member': member,
                 'object_path': str(object_path) if object_path else None,
                 'lean_path': ':'.join([str(x) for x in prefixes] + suffix),
                 'expected_exit': 1 if negative else 0,
                 'original_log': ('core/' + namespace if namespace != 'literal' else 'literal') + '/logs/' + label + '.log',
                 'timeout_marker': '\nWALL_TIMEOUT_180\n' if namespace != 'literal' else '\nRESOURCE_LIMIT\n'}
        events.append(event); children.append(event)
    readonly([lean, '--version'], True); dependencies()
    for name, member in _module_order(api, members, 'runtime', 'ExactRuntimeCounterexample', 167):
        child('runtime', name, member, 'snapshot/runtime/src', 'core/runtime/build/' + name.replace('.', '/') + '.olean')
    for name in ('EveryNewAxiom', 'ExactStatementReview', 'NegativeProofIndependence'):
        child('runtime', name, name + '.lean', '')
    for name, member in _module_order(api, members, 'cost', 'ActualExponentialMoments', 146):
        child('cost', name, member, 'snapshot/cost/src', 'core/cost/build/' + name.replace('.', '/') + '.olean')
    child('cost', 'CostReadback', 'snapshot/readbacks/CostReadback.lean', 'snapshot/readbacks')
    child('cost', 'ExactInheritedCostMutant', 'snapshot/cost/mutation/ActualExponentialMoments.lean', 'snapshot/cost/mutation', negative=True)
    dependencies()
    for name in ('LiteralSelectorObstruction', 'LiteralSelectorFamily', 'LiteralRuntimeCounterexample'):
        child('literal', name, 'literal-snapshot/src/' + name + '.lean', 'literal-snapshot/src', 'literal/build/' + name + '.olean')
    for name in ('EveryLiteralAxiom', 'LiteralEndpointReview'):
        child('literal', name, name + '.lean', '')
    child('literal', 'SelectorNumeralReadback', 'literal-snapshot/readbacks/SelectorNumeralReadback.lean', 'literal-snapshot/readbacks', timeout=30)
    child('literal', 'LiteralCodeReadback', 'literal-snapshot/readbacks/LiteralCodeReadback.lean', 'literal-snapshot/readbacks', timeout=120)
    member = 'literal-snapshot/check_literal_native.py'
    event = {'readonly': False, 'id': 'literal/native',
             'argv': [str(python), str(snapshot / member), '--readback', str(out / 'literal/logs/LiteralCodeReadback.log'),
                      '--codec', str(snapshot / 'literal-snapshot/prcodec.py'), '--out', str(out / 'literal/NATIVE_RESULT.json')],
             'cwd': str(snapshot), 'timeout': 90, 'source_path': str(snapshot / member),
             'source_sha256': api.sha(members[member]), 'member': member,
             'object_path': None, 'lean_path': None, 'expected_exit': 0,
             'original_log': 'literal/logs/native.log', 'timeout_marker': None}
    events.append(event); children.append(event)
    literal = members['replay_literal_independent.py'].decode()
    # Obtain the archived path-bearing statement from the already hash-pinned
    # source. Keep its private locator out of this reusable proposal's bytes.
    dependency_assignments = [node for node in ast.walk(ast.parse(literal))
                              if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                              isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'dependency']
    api.require(len(dependency_assignments) == 1, 'Literal dependency derivation is ambiguous')
    archived_dependency_call = ast.get_source_segment(literal, dependency_assignments[0])
    changes = [("cr['status']=='PASS_CORE_WITH_EXPLICIT_AUXILIARY_LIMITATIONS'",
                "cr['status'] in ['PASS_CORE_WITH_EXPLICIT_AUXILIARY_LIMITATIONS','PASS_INDEPENDENT_REVIEW_CHECKS']"),
               (archived_dependency_call, 'dependency=d.verify_dependencies(MATH,ARCHIVE,pins)')]
    for before, after in changes:
        api.require(literal.count(before) == 1, 'Literal driver derivation is ambiguous')
        literal = literal.replace(before, after)
    ast.parse(literal)
    api.require(api.sha(literal.encode()) == DERIVED_LITERAL_SHA, 'Literal driver derivation differs')
    api.require(len(children) == 326 and len(events) == 381, 'Portable original process census differs')
    return {'members': members, 'children': children, 'events': events,
            'archive_sha256': REVIEW_ARCHIVE_SHA, 'derived_literal_sha256': DERIVED_LITERAL_SHA,
            'event_plan_sha256': api.canonical(events)}


def validate_call(api, event, argv, positional, kwargs):
    """Validate actual original subprocess arguments, without changing them."""
    api.require(isinstance(argv, list) and all(isinstance(x, str) for x in argv) and argv == event['argv'] and not positional,
                'Original portable command/order differs')
    if event['readonly']:
        allowed = {'stdout', 'check', 'timeout'} | ({'text'} if event['text'] else set())
        api.require(set(kwargs) <= allowed and kwargs.get('stdout') == subprocess.PIPE and kwargs.get('check') is True and
                    kwargs.get('timeout') is None and (kwargs.get('text') is True if event['text'] else 'text' not in kwargs),
                    'Unreviewed read-only subprocess keyword')
        return
    expected = {'cwd', 'stdout', 'stderr', 'text', 'timeout'} | ({'env'} if event['lean_path'] is not None else set())
    api.require(set(kwargs) == expected, 'Original portable subprocess keyword set differs')
    api.require(str(kwargs['cwd']) == event['cwd'], 'Original portable cwd differs')
    api.require(type(kwargs['timeout']) is int and kwargs['timeout'] == event['timeout'], 'Original portable child budget differs')
    api.require(kwargs['stdout'] == subprocess.PIPE and kwargs['stderr'] == subprocess.STDOUT and kwargs['text'] is True, 'Original portable capture mode differs')
    if event['lean_path'] is not None:
        env = kwargs['env']
        api.require(isinstance(env, dict) and env.get('LEAN_PATH') == event['lean_path'] and
                    {key for key in env if key.startswith('LEAN_')} == {'LEAN_PATH'}, 'Original isolated environment differs')
    api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes()) == event['source_sha256'], 'Original child source changed')
    if event['object_path']:
        api.require(not api.no_symlinks(event['object_path']).exists(), 'Original child output already exists')


def trace_calls(api, original_run, trace, plan):
    """Installable callback; callers must bind the exact reviewed parent first."""
    api.require(api.canonical(plan['events']) == plan['event_plan_sha256'], 'Changed source-owned event plan')
    captured_run = api.traced_run(original_run, trace)
    position = 0
    def invoke(argv, *args, **kwargs):
        nonlocal position
        api.require(position < len(plan['events']), 'Extra original portable command/order')
        event = plan['events'][position]
        validate_call(api, event, argv, args, kwargs)
        position += 1
        return original_run(argv, **kwargs) if event['readonly'] else captured_run(argv, **kwargs)
    def require_complete():
        api.require(position == len(plan['events']), 'Original process plan is incomplete')
        rows = read_capture(api, plan, trace)
        api.require(len(rows) == len(plan['children']), 'Original child capture is incomplete')
        return {'events': position, 'science_children': len(rows)}
    invoke.require_complete = require_complete
    return invoke


def _check_captured(api, event, captured, captured_log):
    api.require(captured['argv'] == event['argv'] and captured['cwd'] == event['cwd'], 'Captured child command/cwd differs')
    api.require(api.sha(captured_log) == captured['log_sha256'], 'Captured child log differs')
    code = captured['exit_code']; terminal = captured['terminal']
    api.require(terminal in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED'}, 'Unknown captured child terminal')
    api.require((type(code) is int and 0 <= code < 124) if terminal == 'COMPLETED' else code is None, 'Invalid captured child exit')


def read_capture(api, plan, trace):
    """Read an exact terminal prefix; an incomplete prefix is not completion."""
    api.require(api.canonical(plan['events']) == plan['event_plan_sha256'] and
                [e for e in plan['events'] if not e['readonly']] == plan['children'], 'Changed source-owned event plan')
    trace = api.no_symlinks(trace)
    records = sorted(trace.glob('*.json'))
    api.require(len(records) <= len(plan['children']), 'Extra child capture census')
    expected = {f'{i:04}.json' for i in range(len(records))} | {f'{i:04}.log' for i in range(len(records))}
    api.require({p.name for p in trace.iterdir()} == expected, 'Incomplete or extra capture file census')
    rows = []
    for i, path in enumerate(records):
        row = api.read_json(api.no_symlinks(path))
        api.require(type(row['index']) is int and row['index'] == i, 'Captured child index differs')
        api.require(isinstance(row['started_at'], str) and isinstance(row['ended_at'], str), 'Nonterminal child capture')
        data = api.no_symlinks(path.with_suffix('.log')).read_bytes()
        _check_captured(api, plan['children'][i], row, data)
        rows.append(row)
    return rows


def classify_child(api, event, original, captured, original_log, captured_log):
    """Classify a captured source-owned child; never produce qualification."""
    native = event['id'] == 'literal/native'
    _check_captured(api, event, captured, captured_log)
    code = captured['exit_code']; terminal = captured['terminal']
    if original is not None:
        if native:
            api.require(original['native_command'] == captured['argv'] and original['native_log_sha256'] == api.sha(original_log), 'Original finite command/log differs')
        else:
            api.require(original['source_sha256'] == event['source_sha256'] and original['command'] == captured['argv'], 'Original child source/command differs')
            prior_code = original['exit_code']
            api.require(prior_code is None or type(prior_code) is int, 'Invalid original child exit')
            agreement = prior_code == code if terminal != 'INTERRUPTED' else (prior_code is None or prior_code < 0 or prior_code >= 124)
            api.require(agreement and original['log_sha256'] == api.sha(original_log), 'Original child exit/log contradicts capture')
    else:
        # The literal producer persists native_command only after all final
        # assertions. A captured failed native process can lack that row.
        api.require(native, 'Missing original child row')
    augmentation = None
    if original_log is not None:
        if terminal == 'TIMEOUT' and event['timeout_marker'] is not None:
            augmentation = event['timeout_marker']
            api.require(original_log == captured_log + augmentation.encode(), 'Original timeout log has unreviewed augmentation')
        else:
            api.require(original_log == captured_log, 'Original log differs from actual captured stdout')
    else:
        api.require(native and terminal != 'COMPLETED', 'Missing original child log')
    text = (original_log if original_log is not None else captured_log).decode('utf8')
    resource_match = RESOURCE.search(text)
    resource = terminal != 'COMPLETED' or resource_match is not None
    if not native and original is not None and 'resource_diagnostic' in original:
        expected_flag = bool(re.search(r'timeout|maximum number of heartbeats|WALL_TIMEOUT', text, re.I))
        api.require(original['resource_diagnostic'] is expected_flag, 'Original resource flag contradicts log')
    mismatch = event['id'] == 'cost/ExactInheritedCostMutant' and all(literal in text for literal in MISMATCH)
    if resource:
        outcome = 'RESOURCE_INCONCLUSIVE'
    elif event['expected_exit'] == 1:
        outcome = 'REJECT' if code == 1 and mismatch and INFRASTRUCTURE.search(text) is None else 'FAILED'
    else:
        clean = code == 0 and 'error:' not in text and not re.search(r'\b(sorry|admit)\b|sorryAx|declaration uses', text)
        outcome = 'ACCEPT' if clean else 'FAILED'
    return {'source_child_id': event['id'], 'source_sha256': event['source_sha256'],
            'scope': 'SOURCE_CHILD_ONLY_NOT_QUALIFICATION', 'terminal': terminal, 'exit_code': code,
            'outcome': outcome, 'semantic_outcome': outcome if outcome in {'ACCEPT', 'REJECT'} else None,
            'captured_log_sha256': captured['log_sha256'],
            'original_log_sha256': api.sha(original_log) if original_log is not None else None,
            'original_row_present': original is not None,
            'source_log_augmentation': augmentation,
            'concrete_application_mismatch': mismatch,
            'mismatch_precedes_resource': bool(mismatch and resource_match is not None and text.index(MISMATCH[0]) < resource_match.start()),
            'unchanged_theorem_refuted': False}
