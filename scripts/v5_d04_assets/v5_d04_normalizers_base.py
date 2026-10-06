from pathlib import Path, PurePosixPath
import ast, hashlib, json, re

LEAN_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'

MATHLIB = 'c44e0c8ee63ca166450922a373c7409c5d26b00b'

AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}

INFRA = re.compile(r'unknown module|unknown constant|unknown identifier|unknown namespace|no such file|file not found|failed to read file|object file|timed out|out of memory|maximum (?:recursion|heartbeats)|deterministic timeout', re.I)


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_at(root, relative):
    require(isinstance(relative, str) and relative and '\\' not in relative, 'Invalid output/source locator')
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and all(p not in {'', '.', '..'} for p in pure.parts), 'Escaping output/source locator')
    root = Path(root).absolute()
    path = root / relative
    require(not root.is_symlink() and not any(p.is_symlink() for p in [path, *path.parents]), 'Symlink source/output')
    require(path.resolve().is_relative_to(root.resolve()) and path.is_file(), 'Missing source/output file: ' + relative)
    return path


def read_json(root, relative):
    def pairs(items):
        data = {}
        for key, value in items:
            require(key not in data, 'Duplicate JSON key')
            data[key] = value
        return data
    def invalid(value):
        raise ValueError('Nonfinite JSON value')
    return json.loads(file_at(root, relative).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_constant=invalid)


def log_data(root, relative):
    data = file_at(root, relative).read_bytes()
    return data.decode('utf-8'), sha(data)


def positive(root, name, relative, code, *, recorded_sha=None):
    require(type(code) is int and code == 0, 'Positive child did not exit 0: ' + name)
    text, fingerprint = log_data(root, relative)
    require('sorryAx' not in text, 'Proof hole in positive child: ' + name)
    if recorded_sha is not None:
        require(recorded_sha == fingerprint, 'Child log digest changed: ' + name)
    return {'id': name, 'terminal': 'COMPLETED', 'exit_code': code, 'log_sha256': fingerprint,
            'log_relative_path': relative, 'outcome': 'ACCEPT'}


def rejected(root, name, relative, code, literals):
    require(type(code) is int and code == 1, 'Expected source-prescribed semantic exit 1: ' + name)
    text, fingerprint = log_data(root, relative)
    require(all(literal in text for literal in literals), 'Missing intended diagnostic: ' + name)
    require(not INFRA.search(text), 'Infrastructure/resource failure is not rejection: ' + name)
    return {'id': name, 'terminal': 'COMPLETED', 'exit_code': code, 'log_sha256': fingerprint,
            'log_relative_path': relative, 'outcome': 'REJECT',
            'diagnostics': [{'literal': x, 'sha256': sha(x.encode())} for x in literals]}


def audit_log(root, relative, expected):
    text, fingerprint = log_data(root, relative)
    rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)
    no_axioms = re.findall(r"'([^']+)' does not depend on any axioms", text)
    require(len(rows) + len(no_axioms) == expected, 'Incomplete original axiom readbacks')
    require(len({n for n, _ in rows} | set(no_axioms)) == expected, 'Duplicate original axiom target')
    for _, raw in rows:
        require({x.strip() for x in raw.split(',') if x.strip()} <= AXIOMS, 'Unapproved original audit axiom')
    return {'log_sha256': fingerprint, 'declaration_count': expected,
            'scope': 'ORIGINAL_AXIOM_READBACK_ONLY_ADAPTER_CHECKED_CLOSURE_IS_SEPARATE'}


def source_hashes(root, expected):
    actual = {}
    for name, fingerprint in expected.items():
        require(isinstance(fingerprint, str) and re.fullmatch('[a-f0-9]{64}', fingerprint), 'Malformed source digest')
        actual[name] = sha(file_at(root, name).read_bytes())
        require(actual[name] == fingerprint, 'Original source changed: ' + name)
    return actual


def dynamic(recipe, source_root, output):
    receipt = read_json(output, 'REPLAY_RECEIPT.json')
    require(receipt['status'] == 'PASS_AUTHOR_ISOLATED_REPLAY', 'Incomplete original dynamic receipt')
    require('version 4.19.0,' in receipt['lean_version'], 'Wrong original compiler readback')
    base = recipe == 't07-dynamic-base'
    names = ['finite', 'covering', 'lean_interlock', 'lean_covering'] if base else ['finite', 'core_lean', 'cover_lean', 'attribution_lean']
    require([s['step'] for s in receipt['steps']] == names, 'Missing/reordered dynamic child')
    stages = [positive(output, row['step'], row['log'], row['exit_code'], recorded_sha=row['log_sha256' if base else 'sha256']) for row in receipt['steps']]
    expected_source_names = (['dynamic_interlock.py','verify_dynamic.py','verify_covering.py','DynamicInterlock.lean','CoveringCore.lean','COVERING_WITNESSES.json'] if base else
                             ['verify_attribution.py','UnknownRootAttribution.lean','dependencies/DynamicInterlock.lean','dependencies/CoveringCore.lean'])
    require(set(receipt['source_sha256']) == set(expected_source_names), 'Incomplete dynamic source inventory')
    inputs = source_hashes(Path(source_root)/'base-v2' if base else source_root, receipt['source_sha256'])
    if base:
        finite = read_json(output, 'FINITE_CHECK_RESULTS.json'); covering = read_json(output, 'COVERING_CHECK_RESULTS.json')
        require(receipt['results'] == {'FINITE_CHECK_RESULTS.json':finite, 'COVERING_CHECK_RESULTS.json':covering}, 'Embedded finite result differs')
        require(finite['status'] == 'PASS_FINITE_DECLARED_CONTROLS', 'Incomplete finite dynamic controls')
        require(covering['status'] == 'PASS_COVERING_WITNESSES_AND_FINITE_AUXILIARIES' and covering['four_edge_graph_cases'] == 15 and covering['labelled_failure_deletion_cap_B1_n4'] == 2, 'Incomplete finite covering controls')
        traces = read_json(output, 'DELETION_TRACES.json')
        adverse = {'cached_votes':'UNSAFE', 'mutable_payload':'UNSAFE', 'current_authorization_deleted':'UNSAFE',
                   'common_downstream_writer':'UNSAFE', 'common_selector_omitted':'SAFE_BUT_NEVER_RESTORED',
                   'two_B_plus_one_failed_candidate':'UNSAFE', 'immediate_external_revocation':'UNSAFE',
                   'instantaneous_budget_failed_candidate':'FAILS_LIFETIME_PREMISE',
                   'perpetual_version_change_prefix':'SAFE_NONPERSISTENT_PREFIX',
                   'too_small_cancellation_certificate':'LATE_WRITE_AFTER_FALSE_CANCELLATION'}
        for name, expected in adverse.items():
            require(traces[name]['expected'] == expected and traces[name]['history'], 'Missing finite adverse trace: ' + name)
        require(finite['counts']['deletion_and_matched_control_traces'] == len(traces), 'Incomplete matched-control trace inventory')
        counters = {'finite_counts':finite['counts'], 'finite_adverse_outcomes':adverse, 'finite_matched_trace_count':len(traces), 'covering':covering}
    else:
        finite = read_json(output, 'ATTRIBUTION_CHECK_RESULTS.json')
        require(finite['status'] == 'PASS_FINITE_FIXED_MAP_CONTROLS' and receipt['finite_results'] == finite, 'Incomplete finite fixed-map controls')
        require(finite['source_sha256'] == inputs['verify_attribution.py'], 'Finite helper identity changed')
        traces = read_json(output, 'ATTRIBUTION_COUNTEREXAMPLES.json')
        require(set(traces) == {'five_labels_four_gate_liveness_failure','five_labels_stale_landing','two_cancel_labels_not_two_roots','forced_alias_bridge'}, 'Missing fixed-map counterexample')
        require(traces['five_labels_stale_landing']['old_path_can_land_after_effective_revoke'] is True, 'Lost stale-landing counterexample')
        require(traces['two_cancel_labels_not_two_roots']['closure_not_warranted'] is True, 'Lost root-identity counterexample')
        require(traces['forced_alias_bridge']['not_safe_against_B1'] is True, 'Lost forced-bridge boundary')
        counters = {'finite_counts':finite['counts'], 'finite_counterexamples':traces}
    return stages, counters, inputs

