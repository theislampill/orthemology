"""Exact selector continuation checks and no-follow negative-fixture custody.

This module executes no producer, compiler or audit. Main owns reviewed runner
registration and must verify this immutable helper before injecting that set.
"""
from datetime import datetime
import json
import os
from pathlib import Path
import stat

SC_SCHEMA = 'orthemology-v5-selector-audit-continuation-v1'
SC_REVIEWED_EXECUTORS = frozenset()
SC_SUITE = '5b16a846fde6ac4f761f5fe4d40e3440d407664250ed16fb8763f1f99bd8814c'
SC_PRIOR_RAW = '276bb08759ed1017a86778543d8686c297f00488c75dd2fb640d6e7be1e5d9bc'
SC_PRIOR = 'fda30bda7479f312186780bb7c8ff042a4b731919fbe68317403db8efd0e02dc'
SC_FAILURE = 'c5e0260fc6ebc44910e34390b5307186fdcea913b851c15f8b15ecaca3218b6f'
SC_PARENT_CUSTODY = '5770c0a212291c94b3c92499c81f6dd64fadbdfcf40403d0d7a6ec0e764949ca'
SC_COLLECTION = '8b28f7b24eb3c84f7d2848308f13226500aab8b5a6760174b4a0d6e41c108ab8'
SC_CUSTODY = 'b1cc8692f4734d078eabb61cff402d3b5f61b17ce70933c651cc625353f9329e'
SC_AUDITOR = '17406b6357d193b1f7423526278cc55946fe0589b9af5aa0e69a839ff4e3e511'
SC_PROJECT = '09bc20e0c75fa5e5be272d54166f156bd13abf14d6d359c2ddab1b87d7ef687b'
SC_CORE_REUSE = '514695a5595a8f69d41e69edf4d8cbaecac37431ca86016a9f50b4da0011f756'
SC_OLD_RUNNER = 'ab06a34e10487b396cf83b3e07eba135ad821dab1e91b25cad0780e1b444a8f0'
SC_LINK = 'original/original-census-controls/evidence/replay-guard-fixtures/symlink/unexpected-link'
SC_SIBLING = SC_LINK.rsplit('/', 1)[0] + '/Fixture.olean'
SC_CONTROL = 'original/original-census-controls/check_replay_guards.py'
SC_ARCHIVE_CONTROL = 'archives/selector-archive/Ninth_Selector_Family_Source_Acceptance_v1/controls/check_original_replay_guards.py'
SC_DRIVER = 'archives/selector-archive/Ninth_Selector_Family_Source_Acceptance_v1/replay.py'
SC_CONTROL_SHA = '70f00b8ea97851e72057b89da66b6e1dea7f30c774ea75e5dabc4ebc3c89de0b'
SC_DRIVER_SHA = 'a02ac9ee8c6108bd247c64c8a5fdfd66741dfdc24370600b90fe1ae15c2c6946'
SC_SIBLING_SHA = 'cfc170388f4b9e80522008420b49a20e7dbb6d50ed6708598c848841e5b1cff6'
SC_STAGE_KEYS = set('id argv cwd budget_seconds started_at ended_at terminal exit_code log_sha256 output_hashes'.split())
SC_COMMON = set('descriptor_sha256 closure_sha256 source_hashes_before source_hashes_after import_fingerprints tool_fingerprints dependency_checks driver_hashes'.split())
SC_RECEIPT_KEYS = set('id suite_id family suite_sha256 source_hashes review_hashes toolchain_sha256 outcome target_readbacks controls stages invocation started_at ended_at exit_code log_sha256 axioms proof_scope replay_evidence'.split())
SC_EVIDENCE_KEYS = SC_COMMON | set('schema runner_sha256 continuation_module_sha256 cache_policy stage_results target_audits output_hashes prior retained_custody retained_collection retained_inputs fresh_audit accounting'.split())
SC_ACCOUNTING = {'reused_selector_physical_runs': 1, 'reused_selector_children': 45, 'reused_selector_objects': 15,
    'reused_qualified_core_objects': 167, 'new_source_owned_physical_runs': 0, 'new_child_compilations': 0,
    'new_custom_objects': 0, 'new_target_audit_processes': 1, 'independent_evidence_increment': 0}


def _sc_time(value):
    if not isinstance(value, str) or not value.endswith('Z'):
        raise ValueError('Selector continuation time must be UTC')
    return datetime.fromisoformat(value[:-1] + '+00:00')


def _sc_custody_binding():
    return {'schema': 'selector-negative-fixture-nofollow-custody-v1', 'before_sha256': SC_CUSTODY, 'after_sha256': SC_CUSTODY,
        'link': {'path': SC_LINK, 'literal_target': 'Fixture.olean', 'kind': 'SYMLINK_NOT_FOLLOWED'},
        'sibling': {'path': SC_SIBLING, 'sha256': SC_SIBLING_SHA, 'bytes': 62},
        'source': {'archive_sha256': 'e2c40bb8b2612db8898cdea0db2c984c91edaa15122dd23cbfb16f33d3e98255',
                   'archive_control': SC_ARCHIVE_CONTROL, 'copied_control': SC_CONTROL, 'control_sha256': SC_CONTROL_SHA,
                   'archive_driver': SC_DRIVER, 'driver_sha256': SC_DRIVER_SHA},
        'credit': 'NEGATIVE_CENSUS_FIXTURE_ONLY_NO_PROOF_IMPORT'}


def selector_custody(root, *, api):
    """Hash regular files; read only the literal of the one source-bound link.

    POSIX directory descriptors and O_NOFOLLOW protect every traversal/open.
    This inventory is custody data, never an accepted proof or import root.
    The receipt validator separately pins the complete resulting inventory.
    """
    api.require(os.name == 'posix' and hasattr(os, 'O_NOFOLLOW'), 'No-follow custody requires the qualified POSIX environment')
    root = Path(root)
    api.require(root.is_absolute() and '..' not in root.parts, 'Custody root must be absolute without traversal')
    rows = {}; modes = {}; flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    def walk(directory, prefix):
        with os.scandir(directory) as entries:
            names = sorted(entry.name for entry in entries)
        for name in names:
            key = prefix + name; before = os.stat(name, dir_fd=directory, follow_symlinks=False)
            if stat.S_ISLNK(before.st_mode):
                api.require(key == SC_LINK, 'Unexpected symlink in selector custody')
                target = os.readlink(name, dir_fd=directory)
                api.require(target == 'Fixture.olean', 'Changed negative-fixture link literal')
                rows[key] = {'kind': 'SYMLINK_NOT_FOLLOWED', 'literal_target': target}
            elif stat.S_ISDIR(before.st_mode):
                child = os.open(name, flags, dir_fd=directory)
                try:
                    current = os.fstat(child)
                    api.require((current.st_dev, current.st_ino) == (before.st_dev, before.st_ino), 'Custody directory changed while opening')
                    rows[key] = {'kind': 'DIRECTORY'}; walk(child, key + '/')
                finally:
                    os.close(child)
            elif stat.S_ISREG(before.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
                with os.fdopen(child, 'rb') as stream:
                    current = os.fstat(stream.fileno())
                    api.require(stat.S_ISREG(current.st_mode) and (current.st_dev, current.st_ino) == (before.st_dev, before.st_ino), 'Custody file changed while opening')
                    raw = stream.read(); after = os.fstat(stream.fileno())
                api.require((before.st_mode, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
                            (after.st_mode, after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'Custody file changed while reading')
                rows[key] = {'kind': 'REGULAR_FILE', 'sha256': api.sha(raw), 'bytes': len(raw)}; modes[key] = after.st_mode
            else:
                raise ValueError('Nonregular selector custody entry')
            final = os.stat(name, dir_fd=directory, follow_symlinks=False)
            api.require((final.st_dev, final.st_ino, final.st_mode) == (before.st_dev, before.st_ino, before.st_mode), 'Custody entry replaced during read')
    descriptor = None
    try:
        descriptor = os.open('/', flags)
        for part in root.parts[1:]:
            following = os.open(part, flags, dir_fd=descriptor); os.close(descriptor); descriptor = following
        walk(descriptor, '')
        api.require(rows.get(SC_LINK) == {'kind': 'SYMLINK_NOT_FOLLOWED', 'literal_target': 'Fixture.olean'}, 'Expected negative fixture link is absent')
        api.require(rows.get(SC_SIBLING) == {'kind': 'REGULAR_FILE', 'sha256': SC_SIBLING_SHA, 'bytes': 62}
                    and modes[SC_SIBLING] & 0o111 == 0, 'Negative fixture sibling differs or is executable')
        for path, digest in ((SC_CONTROL, SC_CONTROL_SHA), (SC_ARCHIVE_CONTROL, SC_CONTROL_SHA), (SC_DRIVER, SC_DRIVER_SHA)):
            api.require(rows.get(path, {}).get('kind') == 'REGULAR_FILE' and rows[path]['sha256'] == digest, 'Changed source-owned fixture producer')
        return rows
    except (OSError, KeyError, TypeError) as error:
        raise ValueError('Selector no-follow custody failed') from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _sc_prior(evidence, suite, sources, root, api, family, plan):
    binding = evidence['prior']; api.keys(binding, {'receipt', 'receipt_sha256', 'receipt_canonical_sha256', 'receipt_bytes', 'failure_sha256', 'parent_custody_acceptance_sha256'})
    api.require(binding['receipt_sha256'] == SC_PRIOR_RAW and binding['receipt_canonical_sha256'] == SC_PRIOR
                and type(binding['receipt_bytes']) is int and binding['receipt_bytes'] == 1756047
                and binding['failure_sha256'] == SC_FAILURE
                and binding['parent_custody_acceptance_sha256'] == SC_PARENT_CUSTODY, 'Changed exact selector prior anchors')
    prior = binding['receipt']; api.keys(prior, SC_RECEIPT_KEYS)
    api.require(api.canonical(prior) == SC_PRIOR and prior['outcome'] == 'FAILED' and prior['proof_scope'] == 'NONE', 'Changed failed selector history')
    old = prior['replay_evidence']
    api.require(old['runner_sha256'] == SC_OLD_RUNNER and old['schema'] == 'orthemology-v5-replay-evidence-v2', 'Changed original selector runner/schema')
    # This is the only receipt sent to the ordinary branch: unchanged FAILED.
    api.validate_receipt(prior, suite, sources, root)
    stages = api.indexed(old['stage_results'])
    api.require(list(stages) == ['_prerequisites', *plan['stages'], '_target_audit'], 'Changed original stage inventory')
    for sid, row in stages.items():
        ran = sid in {'_prerequisites', 'original-selector'}
        api.require((row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and row['exit_code'] == 0) if ran else
                    (row['terminal'] == 'SKIPPED' and row['exit_code'] is None and row['log_sha256'] == api.sha(b'')), 'Ineligible prior stage')
        api.require(row['output_hashes'] == {}, 'Changed incomplete output-directory census')
    api.require(all(old[k] == [] for k in ('child_observations', 'control_diagnostics', 'target_audits'))
                and prior['controls'] == prior['target_readbacks'] == prior['axioms'] == [], 'Partial prior projection is not eligible')
    core = old['dependency_reuse']; cat = family.selector_g1_catalog(api)
    api.require(api.canonical(core) == SC_CORE_REUSE, 'Changed qualified core dependency')
    identity = family.selector_g1_dependency_identity(api, 'selector', core['identity']['receipt'], cat['core_suite'], sources, root)
    api.require(identity == core['identity'], 'Qualified core identity differs')
    family.selector_g1_validate_reuse(api, 'selector', core, cat['core_suite'])
    return prior, old


def _sc_fresh(receipt, evidence, prior, api):
    stages = api.indexed(evidence['stage_results'])
    api.require(list(stages) == ['_prerequisites', '_target_audit'], 'Selector continuation reruns original work')
    start, end = _sc_time(receipt['started_at']), _sc_time(receipt['ended_at'])
    api.require(_sc_time(prior['ended_at']) < start <= end, 'Old/reversed selector continuation interval')
    previous = start
    for sid, row in stages.items():
        api.keys(row, SC_STAGE_KEYS)
        argv = ['{builtin:prerequisites}'] if sid == '_prerequisites' else ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean']
        api.require(row['argv'] == argv and row['cwd'] == '.' and type(row['budget_seconds']) is int
                    and row['budget_seconds'] == (30 if sid == '_prerequisites' else 300), 'Changed selector fresh stage recipe')
        rs, re = _sc_time(row['started_at']), _sc_time(row['ended_at'])
        api.require(previous <= rs <= re <= end, 'Invalid fresh stage interval'); previous = re
        api.require(row['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED'}, 'Fresh audit process missing')
        if row['terminal'] == 'COMPLETED':
            api.require(type(row['exit_code']) is int and 0 <= row['exit_code'] < 124, 'Invalid fresh exit')
        else:
            api.require(row['exit_code'] is None, 'Resource failure received concrete rejection credit')
        api.digest(row['log_sha256']); api.require(row['output_hashes'] == {}, 'New custom object claimed')
    api.require(stages['_prerequisites']['terminal'] == 'COMPLETED' and stages['_prerequisites']['exit_code'] == 0, 'Fresh prerequisites absent')
    api.require(receipt['stages'] == [{k: row[k] for k in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in stages.values()]
                and receipt['log_sha256'] == api.canonical({sid: row['log_sha256'] for sid, row in stages.items()}), 'Fresh/top-level logs disagree')
    return stages


def _sc_collection(receipt, evidence, prior, old, plan, fresh, suite, api):
    retained = evidence['retained_collection']
    api.keys(retained, {'parser_id', 'collector_runner_sha256', 'observed_at', 'collection', 'stage_results', 'child_observations', 'control_diagnostics'})
    api.require(retained['parser_id'] == 'selector-exact-source-collector-v1' and retained['collector_runner_sha256'] == evidence['runner_sha256'], 'Wrong selector collector attribution')
    collection = retained['collection']
    api.require(api.canonical(collection) == SC_COLLECTION, 'Changed complete retained collection')
    api.require(collection['physical_children'] == old['driver_invocations'][0]['physical_children']
                and collection['output_hashes'] == old['output_hashes'], 'Changed producer or retained objects')
    parsed, audit_start = _sc_time(retained['observed_at']), _sc_time(fresh['_target_audit']['started_at'])
    api.require(_sc_time(fresh['_prerequisites']['ended_at']) <= parsed <= audit_start, 'Collection is not a fresh pre-audit observation')
    rows = api.indexed(retained['stage_results']); observations = api.indexed(retained['child_observations'], 'stage_id')
    declared = {sid: row for sid, row in plan['stages'].items() if sid != 'original-selector'}
    api.require(list(rows) == list(observations) == list(declared), 'Missing, duplicate or reordered observation projection')
    raw = api.indexed(collection['child_observations'], 'source_child_id')
    controls, diagnostics = [], []; expected_controls = api.indexed(suite['controls'])
    previous = parsed
    for sid, spec in declared.items():
        stage = rows[sid]; api.keys(stage, SC_STAGE_KEYS); child = raw[spec['argv'][2]]
        api.require(stage['argv'] == spec['argv'] and stage['cwd'] == spec['cwd']
                    and type(stage['budget_seconds']) is int and stage['budget_seconds'] == spec['timeout_seconds']
                    and stage['terminal'] == child['terminal'] and type(stage['exit_code']) is int
                    and stage['exit_code'] == child['exit_code'] and stage['log_sha256'] == child['log_sha256']
                    and stage['output_hashes'] == {}, 'Collection projected a different execution')
        rs, re = _sc_time(stage['started_at']), _sc_time(stage['ended_at'])
        when = _sc_time(observations[sid]['observed_at'])
        api.require(previous <= rs <= when <= re <= audit_start, 'Observation timing replaced physical execution'); previous = re
        expected = {**child, 'stage_id': sid, 'parent_stage_id': 'original-selector', 'physical_run_sha256': collection['trace_sha256'],
                    'parent_log_sha256': old['driver_invocations'][0]['parent_log_sha256'], 'observed_at': observations[sid]['observed_at']}
        api.require(api.canonical(observations[sid]) == api.canonical(expected), 'Changed source/physical/finite observation binding')
        for cid in spec['control_ids']:
            control = expected_controls[cid]
            api.require(child['actual_outcome'] == control['expected_outcome'], 'Source-owned control not observed')
            controls.append({k: control[k] for k in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
                'actual_outcome': child['actual_outcome'], 'actual_outcome_sha256': api.sha(child['actual_outcome'].encode()),
                'terminal': child['terminal'], 'exit_code': child['exit_code'], 'log_sha256': child['log_sha256']})
            diagnostics.append({'control_id': cid, 'stage_id': sid, 'prerequisite_stage_ids': spec['depends_on'],
                'expected': spec['expected_diagnostics'], 'observed_log_sha256': child['log_sha256'], 'match': 'MATCHED'})
    api.require(api.canonical(receipt['controls']) == api.canonical(controls)
                and api.canonical(retained['control_diagnostics']) == api.canonical(diagnostics), 'Control outcome/role/diagnostic not source-bound')
    return collection


def _sc_validate(receipt, suite, sources, root, api):
    json.dumps(receipt, allow_nan=False); api.keys(receipt, SC_RECEIPT_KEYS)
    api.require(suite['id'] == 'd06-selector' and api.canonical(suite) == SC_SUITE, 'Wrong exact selector suite')
    family = api.selector_g1_load_family(); plan = family.selector_g1_validate_suite(api, suite, sources, root)
    evidence = receipt['replay_evidence']; api.keys(evidence, SC_EVIDENCE_KEYS)
    api.require(evidence['schema'] == SC_SCHEMA and evidence['cache_policy'] == 'RETAINED_SELECTOR_AND_QUALIFIED_CORE_FRESH_TARGET_AUDIT_ONLY', 'Wrong selector continuation schema/policy')
    api.require(evidence['runner_sha256'] == api.sha(Path(api.__file__).read_bytes()) or evidence['runner_sha256'] in SC_REVIEWED_EXECUTORS, 'Unreviewed selector continuation runner')
    api.require(evidence['continuation_module_sha256'] == api.sha(Path(__file__).read_bytes()), 'Changed immutable continuation helper')
    prior, old = _sc_prior(evidence, suite, sources, root, api, family, plan)
    api.require(isinstance(receipt['id'], str) and receipt['id'].startswith('d06-selector-audit-continuation-')
                and len(receipt['id']) > len('d06-selector-audit-continuation-'), 'Continuation needs a new identity')
    api.require(receipt['invocation'] == ['replay_v5_successors.py', '--selector-audit-continuation', '--suite', 'd06-selector', '--prior', '{prior}', '--out', '{out}'], 'Wrong audit-only selector invocation')
    for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256'):
        api.require(api.canonical(receipt[key]) == api.canonical(prior[key]), 'Changed selector source/review/target/toolchain identity')
    for key in SC_COMMON:
        api.require(api.canonical(evidence[key]) == api.canonical(old[key]), 'Changed tool/source/import/dependency identity')
    fresh = _sc_fresh(receipt, evidence, prior, api)
    collection = _sc_collection(receipt, evidence, prior, old, plan, fresh, suite, api)
    api.require(api.canonical(evidence['retained_custody']) == api.canonical(_sc_custody_binding()), 'Changed no-follow negative-fixture custody')
    expected_inputs = {'project_before_sha256': SC_PROJECT, 'project_after_sha256': SC_PROJECT,
        'source_inventory_before': old['source_inventory_before'], 'source_inventory_after': old['source_inventory_before'],
        'objects_before': collection['output_hashes'], 'objects_after': collection['output_hashes'],
        'core_reuse_before_sha256': SC_CORE_REUSE, 'core_reuse_after_sha256': SC_CORE_REUSE,
        'official_caches_before': old['official_caches_before'], 'official_caches_after': old['official_caches_before']}
    api.require(api.canonical(evidence['retained_inputs']) == api.canonical(expected_inputs), 'Retained source/object/core/cache identity changed')
    api.require(api.canonical(evidence['accounting']) == api.canonical(SC_ACCOUNTING), 'Invented new producer/compiler/independence credit')
    audit = evidence['fresh_audit']
    api.keys(audit, set('recipe generated_source_sha256 resolved_invocation_sha256 argv_provenance library_roots traversal_bound distinct_declaration_accounting fresh_custom_objects'.split()))
    api.digest(audit['resolved_invocation_sha256'])
    expected_audit = {'recipe': 'selector-retained-closure-audit-v1', 'generated_source_sha256': SC_AUDITOR,
        'resolved_invocation_sha256': audit['resolved_invocation_sha256'], 'argv_provenance': 'RESOLVED_FROM_BOUND_INPUTS',
        'library_roots': ['{prior}/original/build', '{qualified-core}/original/runtime/build', '{pinned-official-caches}'],
        'traversal_bound': 1000000, 'distinct_declaration_accounting': 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED', 'fresh_custom_objects': 0}
    api.require(api.canonical(audit) == api.canonical(expected_audit)
                and api.sha(family.selector_g1_audit_source(api, list(plan['targets'].values())).encode()) == SC_AUDITOR, 'Changed audited roots/source or falsely fresh objects')
    api.require(evidence['output_hashes'] == {'generated/V5SuccessorReadback.lean': SC_AUDITOR}, 'Wrong new audit outputs')
    run = fresh['_target_audit']; successful = receipt['outcome'] == 'QUALIFIED_DECLARED_SUITE'
    if not successful:
        expected = 'FAILED' if run['terminal'] == 'COMPLETED' else 'RESOURCE_INCONCLUSIVE'
        api.require(receipt['outcome'] == expected and receipt['proof_scope'] == 'NONE'
                    and type(receipt['exit_code']) is int and receipt['exit_code'] == 1
                    and (run['terminal'] != 'COMPLETED' or run['exit_code'] > 0)
                    and receipt['target_readbacks'] == receipt['axioms'] == evidence['target_audits'] == [], 'Failed audit acquired qualification or partial target credit')
    else:
        api.require(receipt['proof_scope'] == 'DECLARED_SUITE' and type(receipt['exit_code']) is int and receipt['exit_code'] == 0
                    and run['terminal'] == 'COMPLETED' and run['exit_code'] == 0, 'Selector audit did not succeed')
        audits = api.indexed(evidence['target_audits'], 'target_id'); axes = set()
        api.require(set(audits) == set(plan['targets']), 'All seven exact safe targets required')
        for tid, row in audits.items():
            api.keys(row, set('target_id name type_sha256 axioms closure_status checked_declarations stage_id log_sha256'.split()))
            api.require(row['name'] == plan['targets'][tid]['name'] and row['closure_status'] == 'CHECKED_SAFE'
                        and type(row['checked_declarations']) is int and row['checked_declarations'] > 0
                        and row['stage_id'] == '_target_audit' and row['log_sha256'] == run['log_sha256'], 'Wrong target/closure/log association')
            api.digest(row['type_sha256'])
            api.require(isinstance(row['axioms'], list) and len(set(row['axioms'])) == len(row['axioms']) and set(row['axioms']) <= api.AXIOMS, 'Unapproved target axiom')
            axes.update(row['axioms'])
        expected = [{'target_id': row['id'], 'source_id': row['source_id'], 'target_sha256': row['target_sha256'], 'outcome': 'CHECKED'} for row in suite['targets']]
        api.require(receipt['target_readbacks'] == expected and receipt['axioms'] == sorted(axes), 'Wrong source-bound target summary')
    return {'suite_id': 'd06-selector', 'outcome': receipt['outcome'], 'scope': 'EXACT_RETAINED_SELECTOR_AND_MISSING_AUDIT_ENVELOPE_ONLY'}


def validate_selector_continuation(receipt, suite, sources, root, *, api):
    try:
        return _sc_validate(receipt, suite, sources, root, api)
    except (KeyError, TypeError, IndexError, OverflowError) as error:
        raise ValueError('Malformed selector continuation envelope') from error
