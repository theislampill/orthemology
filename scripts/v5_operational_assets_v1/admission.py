import copy
import datetime as _operational_datetime
APPROVED_DECLARED_SUITES.update({'D05-T08-COMMON-ORIGINAL': 'e74f0ed69e1b74cd9d08cd7d0be2964f5b74ab5435a70095dd093f6b7389a1b3', 'D05-T08-BATCH-ORIGINAL': '4ddf91239b4abdf2be6e71458540c78ae35a3fe1034d6277672ed8421027c51a', 'D05-T08-SHARED-ORIGINAL': '98ea2e2ccce36d4d42b7d64a9877a7627fca1779b4f2bf8ca887ed96aa37c46e', 'D05-T08-CONTROLLER-ORIGINAL': 'be8d9d0b77ede1ac13f7bff5bf776ad2f5af36eefdf2b0d16807b1061077fac4', 'D07-T09-CONTROLLER-ORIGINAL': '29ce6f0c7205c4d652a6dda398541733289499bb7b1358e0529a3d31d5732b45', 'D07-T09-TRANSPORT-ORIGINAL': '3c35b9ea992f6a2a84a71287df50a82382675d56fdd8a0620b86b6fa0b70e642'})
OPERATIONAL_RECIPES = {v["recipe"] for v in _OPERATIONAL_DATA["packets"].values()}

def operational_precheck(suite, sources):
    """Exact source and full descriptor admission, including component ceilings."""
    known = suite.get('id') in _OPERATIONAL_DATA['suites']
    recipes = {row.get('recipe') for row in suite.get('replay', {}).get('drivers', [])}
    if not known and not recipes & OPERATIONAL_RECIPES:
        return
    require(known, 'Operational recipe has a foreign suite identity')
    require(canonical(suite) == _OPERATIONAL_DATA['suites'][suite['id']]['canonical_sha256'],
            'Changed complete operational descriptor or scope')
    for sid, expected in _OPERATIONAL_DATA['source_bindings'][suite['id']].items():
        require(sid in sources and {key: sources[sid].get(key) for key in expected} == expected,
                'Changed operational original/public source binding')


def operational_validate_driver(driver, source):
    owner = next(value for value in _OPERATIONAL_DATA['packets'].values() if value['recipe'] == driver['recipe'])
    require(driver['sha256'] == owner['driver']['sha256'] and driver['argument_meanings'] == owner['argument_meanings'],
            'Changed exact operational driver or typed arguments')
    require(source['projection'] == 'CUSTODY_ONLY' and source['public_sha256'] is None and
            source['original_sha256'] == owner['driver']['sha256'] and
            source['original_bytes'] == owner['driver']['bytes'] and
            source['member_chain'] == owner['driver']['member_chain'] and
            source['origin_archive_sha256'] == owner['driver']['parent_archive_sha256'],
            'Changed original operational driver custody')


def operational_validate_package(suite, sources, plan):
    if suite['id'] not in _OPERATIONAL_DATA['suites']:
        return
    packet = _OPERATIONAL_DATA['suites'][suite['id']]['packet']
    owner = _OPERATIONAL_DATA['packets'][packet]
    plan['operational_packet'] = packet
    plan['operational_helpers'] = owner['helper_ids']
    plan['operational_suite_id'] = suite['id']
    plan['operational_sources'] = {sid: sources[sid] for sid in _OPERATIONAL_DATA['source_bindings'][suite['id']]}
    plan['operational_expected_stages'] = indexed(_OPERATIONAL_DATA['descriptors'][suite['id']]['replay']['stages'])


def operational_validate_argv(stage, plan):
    require(stage == plan['operational_expected_stages'].get(stage['id']),
            'Changed original operational stage, control, helper, or argument vector')


def operational_diagnostic(stage, diagnostic, plan):
    if 'operational_packet' not in plan:
        return False
    return diagnostic in plan['operational_expected_stages'][stage['id']]['expected_diagnostics']


def operational_physical_specs(packet):
    require(packet in _OPERATIONAL_DATA['execution_plans'], 'Unreviewed operational call plan')
    return copy.deepcopy(_OPERATIONAL_DATA['execution_plans'][packet]['physical'])


def operational_validate_source_binding(packet, child, binding):
    rows = {row['id']: row for row in operational_physical_specs(packet)}
    require(child in rows and binding == rows[child]['source_binding'], 'Changed exact operational child source binding')


def operational_check_helper(helper_id, text, output, mappings):
    require(helper_id in _OPERATIONAL_DATA['helpers'], 'Unreviewed operational helper')
    owner = _OPERATIONAL_DATA['helpers'][helper_id]
    if owner['kind'] == 'unittest':
        check_unittest_log(text, owner['unittest_names'])
        require(re.search(r'Ran ' + str(owner['required_count']) + r' tests? in ', text) is not None,
                'Original helper test count differs')
        return
    if owner['kind'] == 'json-checks':
        value = read_json(path_in(output, 'wrapper-checks/common-boundary.json'))
        require(json.loads(text) == value and value['status'] == 'PASS', 'Original boundary helper lacks terminal JSON')
        require(value['checks'] == _OPERATIONAL_DATA['common_boundary_checks'], 'Original boundary check inventory differs')
        require(value['public_manifest_sha256'] == _OPERATIONAL_DATA['direct']['t08-common']['input_files']['PUBLIC_MANIFEST.json']['sha256'],
                'Boundary helper checked another source manifest')
        require(value['mutations'] == 'Disposable reviewer-owned fixtures only; extracted package and dependencies unchanged.',
                'Boundary helper scope changed')
        return
    require(owner['kind'] == 'json-probes', 'Unknown helper result contract')
    directory = path_in(output, 'wrapper-checks/controller-environment')
    value = read_json(directory / 'RECEIPT.json')
    require(json.loads(text) == value and value['status'] == 'PASS_BOUNDED_COMPILER_ENVIRONMENT_CHECKS', 'Original environment helper lacks terminal JSON')
    require(value['wrapper_sha256'] == _OPERATIONAL_DATA['packets']['t08-controller']['driver']['sha256'] and
            value['test_source_sha256'] == owner['source']['sha256'], 'Environment helper source binding differs')
    require(value['tested_loader_keys'] == ['LD_PRELOAD', 'LD_LIBRARY_PATH', 'LD_AUDIT', 'LD_DEBUG', 'LD_PROFILE', 'LD_TRACE_LOADED_OBJECTS', 'LD_FUTURE_UNKNOWN_TEST'] and
            value['input_mapping_unchanged'] is True and value['ordinary_variables_retained'] is True and
            value['legacy_two_name_policy_rejected_in_memory'] is True and type(value['main_runner_stage_call_sites']) is int and
            value['main_runner_stage_call_sites'] == 3, 'Environment helper contract is incomplete')
    require([row['stage'] for row in value['stages']] == ['version', 'compile', 'axiom_audit'], 'Environment helper omitted/reordered actual probes')
    for row in value['stages']:
        received = json.loads((directory / (row['stage'] + '.log')).read_text())
        require(type(row['exit_code']) is int and row['exit_code'] == 0 and row['received'] == received and received == {
            'loader_keys': [], 'ordinary': {'PROBE_ORDINARY': 'ordinary-retained', 'KEEP_LD_NAME': 'retained',
                'LDX_NOT_PREFIX': 'retained', 'LEAN_PATH': '/generated/build:/pinned/cache', 'PROBE_STAGE': row['stage']}},
                'Actual environment probe differed from its receipt')


class _OperationalAPI:
    def __getattr__(self, name):
        return globals()[name]
_operational_api = _OperationalAPI()

