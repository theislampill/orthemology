"""Exact G1 source-membership metadata view of one retained author run.

The 109-member declared map is not a new measurement. The original 107-file
projection, 127-member archive inventories and all execution evidence remain
inside the unchanged prior receipt. This module never starts a process or
writes a file. The original replay descriptor remains available separately.
"""
import copy
import json

SCHEMA = 'orthemology-v5-g1-membership-metadata-v1'
OLD_SUITE = 'b6ba8c2ceb6b645ed6d1f33162eb872d87f369d2ed342b3514a771ab35895a91'
NEW_SUITE = '7a902f6333972b3a25d551aa464ea4b07cd41bfdc48e7b5601d6e0b09e7f7c04'
CATALOG = '1c04885e6a997afd24e831315a1bd313fbaef693c2d682402db0637407b55344'
PRIOR_FILE = '1b39b168f89d8b7575131a27a0697ec22b2c1d4bc333b506f1a6f3516a01b152'
PRIOR_CANONICAL = 'da3e904d18f5656add78cf079f4d7879e7f7ab06b7089a50eb03cb3800ccb46d'
MEMBERSHIP = (
    {'source_id': 's0715-913c79014b9d7f98aafe',
     'source_sha256': '76e3fa078a75460c6a347dcae9646c9c96cbc32a48cd55bcfbc6ce52ad99b849',
     'inventory_namespace': 'g1', 'inventory_member': 'mutations/PathLengthMutationControl.lean',
     'physical_child_id': 'PathLengthMutationControl', 'physical_child_index': 139,
     'observation_stage_id': 'observe-PathLengthMutationControl',
     'control_id': 'd08-g1-control-9-D08-01-check_sound'},
    {'source_id': 's0715-dbfd2596f3b7b49f66c9',
     'source_sha256': '2628c64ef41e82c87c0c35890b12767b04a2075d8b25f98eb1137c2db3aaed57',
     'inventory_namespace': 'g1', 'inventory_member': 'mutations/PathEdgesMutationControl.lean',
     'physical_child_id': 'PathEdgesMutationControl', 'physical_child_index': 141,
     'observation_stage_id': 'observe-PathEdgesMutationControl',
     'control_id': 'd08-g1-control-10-D08-01-check_sound'},
)
ACCOUNTING = {'new_processes': 0, 'new_builds': 0, 'new_audits': 0, 'new_independence': 0}
TOP_DELTA = {'suite_sha256', 'source_hashes', 'replay_evidence'}
TOP_KEYS = {'id', 'suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes',
            'toolchain_sha256', 'outcome', 'target_readbacks', 'controls', 'stages', 'invocation',
            'started_at', 'ended_at', 'exit_code', 'log_sha256', 'axioms', 'proof_scope', 'replay_evidence'}


def _original(adapter):
    family = adapter.selector_g1_load_family()
    api = family.selector_g1_adapter_view(vars(adapter))
    adapter.require(family.SELECTOR_G1_CATALOG_SHA256 == CATALOG, 'Changed G1 membership catalogue authority')
    catalog = family.selector_g1_catalog(api)
    old = catalog['families']['g1']['suite']
    adapter.require(adapter.canonical(old) == OLD_SUITE, 'Changed original G1 replay descriptor')
    return family, api, catalog, old


def original_replay_suite(*, adapter):
    """Return the unchanged executable catalogue descriptor, never this view."""
    return copy.deepcopy(_original(adapter)[3])


def _suite(suite, sources, root, adapter):
    family, api, catalog, old = _original(adapter)
    adapter.require(adapter.canonical(suite) == NEW_SUITE, 'Unknown G1 membership metadata descriptor')
    expected = copy.deepcopy(old)
    expected['source_ids'].extend(row['source_id'] for row in MEMBERSHIP)
    adapter.require(adapter.canonical(expected) == NEW_SUITE and suite == expected,
                    'G1 membership correction is not the exact two-source suffix')
    plan = family.selector_g1_validate_suite(api, old, sources, root)
    for row in MEMBERSHIP:
        sid = row['source_id']
        adapter.require(adapter.canonical(sources[sid]) == adapter.canonical(catalog['sources'][sid]),
                        'Changed G1 membership source ownership')
        data = adapter.public_bytes(root, sources[sid])
        adapter.require(adapter.sha(data) == row['source_sha256'] == sources[sid]['original_sha256'],
                        'Changed archive-consumed G1 control bytes')
    # Keep the old projected contents/files intact. This annotation is not an
    # execution plan; the public project/execute entry points refuse this view.
    plan['metadata_only'] = True
    plan['membership_source_hashes'] = {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']}
    return plan, family, api, catalog, old


def validate_suite(suite, sources, root, *, adapter):
    try:
        return _suite(suite, sources, root, adapter)[0]
    except (KeyError, TypeError, AttributeError, IndexError, OverflowError) as error:
        raise ValueError('Malformed G1 membership descriptor: ' + str(error)) from error


def _associations(prior, catalog, adapter):
    evidence = prior['replay_evidence']
    adapter.require(len(evidence['driver_invocations']) == 1, 'G1 metadata view requires one retained producer')
    invocation = evidence['driver_invocations'][0]
    physical = invocation['physical_children']
    observations = adapter.indexed(evidence['child_observations'], 'stage_id')
    controls = adapter.indexed(prior['controls'])
    contract = adapter.indexed(catalog['families']['g1']['contract']['stages'])
    results = adapter.indexed(evidence['original_collection']['original_result']['runs'], 'label')
    for member in MEMBERSHIP:
        sid, digest, name = member['source_id'], member['source_sha256'], member['physical_child_id']
        binding = {'kind': 'ORIGINAL_SOURCE', 'source_id': sid, 'source_sha256': digest}
        for field in ['source_inventory_before', 'source_inventory_after']:
            inventory = evidence[field][member['inventory_namespace']]
            adapter.require(len(inventory) == 127 and inventory[member['inventory_member']] == digest,
                            'Control is absent from the measured original archive inventory')
        spec = contract[name]
        adapter.require(spec['source']['source_id'] == sid and spec['source']['sha256'] == digest
                        and spec['source']['path'] == '{root:g1}/' + member['inventory_member']
                        and spec['generated_source'] is None and spec['expected_exit_code'] == 1
                        and spec['role'] == 'MUTATION_REJECTION', 'Changed original archive control contract')
        child = physical[member['physical_child_index']]
        observation = observations[member['observation_stage_id']]
        control = controls[member['control_id']]
        result = results[name]
        adapter.require(child['index'] == member['physical_child_index'] and child['id'] == name
                        and child['source_binding'] == binding and child['argv'] == spec['expected_argv']
                        and child['terminal'] == 'COMPLETED' and type(child['exit_code']) is int
                        and child['exit_code'] == 1 and child['credit'] == 'REJECT'
                        and child['output_hashes'] == {}, 'Wrong original source-bound rejection child')
        adapter.require(observation['physical_child_id'] == name and observation['source_child_id'] == name
                        and observation['source_binding'] == binding and observation['terminal'] == 'COMPLETED'
                        and observation['exit_code'] == 1 and observation['actual_outcome'] == 'REJECT'
                        and observation['physical_run_sha256'] == invocation['trace_sha256']
                        and observation['physical_record_sha256'] == adapter.canonical(child),
                        'Changed original control observation association')
        adapter.require(control['source_id'] == sid and control['target_id'] == 'D08-01-check_sound'
                        and control['role'] == 'MUTATION_REJECTION' and control['actual_outcome'] == 'REJECT'
                        and control['terminal'] == 'COMPLETED' and control['exit_code'] == 1,
                        'Changed original control role or terminal')
        adapter.require(result['source_sha256'] == digest and result['expected_exit'] == result['exit_code'] == 1
                        and observation['original_record_sha256'] == adapter.canonical(result)
                        and child['log_sha256'] == observation['log_sha256'] == control['log_sha256'] == result['log_sha256'],
                        'Changed source-owned result or control log association')
    return copy.deepcopy(list(MEMBERSHIP))


def _receipt(receipt, suite, sources, root, adapter):
    adapter.keys(receipt, TOP_KEYS)
    evidence = receipt['replay_evidence']
    adapter.keys(evidence, {'schema', 'provenance', 'prior', 'membership', 'accounting'})
    adapter.require(evidence['schema'] == SCHEMA and evidence['provenance'] == 'RETAINED_ORIGINAL_EXECUTION',
                    'Unknown G1 membership provenance')
    binding = evidence['prior']
    adapter.keys(binding, {'receipt_file_sha256', 'receipt_canonical_sha256', 'suite_sha256', 'catalog_sha256', 'receipt'})
    adapter.require(binding['receipt_file_sha256'] == PRIOR_FILE and binding['receipt_canonical_sha256'] == PRIOR_CANONICAL
                    and binding['suite_sha256'] == OLD_SUITE and binding['catalog_sha256'] == CATALOG,
                    'Unreviewed retained G1 receipt or catalogue')
    prior = binding['receipt']
    adapter.require(adapter.canonical(prior) == PRIOR_CANONICAL, 'Original G1 receipt was altered')
    adapter.keys(evidence['accounting'], set(ACCOUNTING))
    adapter.require(all(type(value) is int and value == 0 for value in evidence['accounting'].values()),
                    'Membership correction cannot add process, build, audit or independence credit')
    adapter.require(adapter.canonical(evidence['membership']) == adapter.canonical(list(MEMBERSHIP)),
                    'Unknown G1 source-membership association')
    plan, family, api, catalog, old = _suite(suite, sources, root, adapter)
    family.selector_g1_validate_receipt(api, prior, old, sources, root)
    adapter.require(prior['outcome'] == 'QUALIFIED_DECLARED_SUITE' and prior['proof_scope'] == 'DECLARED_SUITE',
                    'Metadata cannot promote an unsuccessful original execution')
    adapter.require(evidence['membership'] == _associations(prior, catalog, adapter), 'G1 membership evidence differs')
    adapter.require(receipt['suite_sha256'] == NEW_SUITE and receipt['source_hashes'] == plan['membership_source_hashes'],
                    'Derived G1 membership map differs')
    adapter.require(adapter.canonical({k: v for k, v in receipt.items() if k not in TOP_DELTA}) ==
                    adapter.canonical({k: v for k, v in prior.items() if k not in TOP_DELTA}),
                    'G1 metadata changed retained execution fields')
    return {'suite_id': 'd08-g1', 'outcome': prior['outcome'], 'provenance': 'RETAINED_ORIGINAL_EXECUTION',
            'accounting': dict(ACCOUNTING)}


def validate_receipt(receipt, suite, sources, root, *, adapter):
    try:
        return _receipt(receipt, suite, sources, root, adapter)
    except (KeyError, TypeError, AttributeError, IndexError, OverflowError) as error:
        raise ValueError('Malformed G1 membership receipt: ' + str(error)) from error


def derive(raw, suite, sources, root, *, adapter):
    """Produce the metadata view in memory from the exact retained raw bytes."""
    adapter.require(isinstance(raw, bytes) and adapter.sha(raw) == PRIOR_FILE, 'Changed retained G1 receipt bytes')
    def pairs(items):
        result = {}
        for key, value in items:
            adapter.require(key not in result, 'Duplicate retained G1 JSON key')
            result[key] = value
        return result
    prior = json.loads(raw, object_pairs_hook=pairs)
    result = copy.deepcopy(prior)
    result['suite_sha256'] = NEW_SUITE
    result['source_hashes'] = dict(prior['source_hashes'])
    result['source_hashes'].update({row['source_id']: row['source_sha256'] for row in MEMBERSHIP})
    result['replay_evidence'] = {
        'schema': SCHEMA, 'provenance': 'RETAINED_ORIGINAL_EXECUTION',
        'prior': {'receipt_file_sha256': PRIOR_FILE, 'receipt_canonical_sha256': PRIOR_CANONICAL,
                  'suite_sha256': OLD_SUITE, 'catalog_sha256': CATALOG, 'receipt': prior},
        'membership': copy.deepcopy(list(MEMBERSHIP)), 'accounting': dict(ACCOUNTING),
    }
    validate_receipt(result, suite, sources, root, adapter=adapter)
    return result
