#!/usr/bin/env python3
"""Selected-source CAS storage; never imports, executes, or extracts selected sources.

Contract: trusted local filesystem without concurrent hostile renames. Caller supplies
an independently reviewed exact planner result; unkeyed hashes bind consistency, not
approval or authenticity. Every source body is retained in memory after preflight.
A failed write may leave an incomplete fresh output, without a completion receipt.
"""
from __future__ import annotations
from pathlib import Path
import plan_selection as p

MAP_SCHEMA = 't20-v6-selected-source-view-map-v1'
RECEIPT_SCHEMA = 't20-v6-selected-source-materialisation-v1'
ROLES = {'authored_proof', 'authored_code', 'authored_argument', 'consumed_fixture',
         'assurance_code', 'qualified_metadata', 'licensed_dependency'}


def keys(value, required, optional=()):
    p.require(isinstance(value, dict), 'object required')
    p.require(set(required) <= set(value) <= set(required) | set(optional), 'unexpected or missing fields')


def object_path(h):
    return 'authored_objects/' + h[:2] + '/' + h


def local_path(value):
    path = Path(value).absolute()
    p.require('..' not in path.parts, 'parent traversal in local path')
    for part in (path, *path.parents):
        p.require(not part.is_symlink(), 'symlink path component')
    return path


def overlap(a, b):
    # Case-fold as well as lexical containment, for portability across filesystems.
    aa = tuple(x.casefold() for x in a.parts)
    bb = tuple(x.casefold() for x in b.parts)
    return aa[:len(bb)] == bb or bb[:len(aa)] == aa


def fresh_destination(destination, protected):
    target = local_path(destination)
    p.require(not target.exists(), 'destination already exists')
    p.require(target.parent.is_dir(), 'destination parent must already exist')
    for root in protected:
        p.require(not overlap(target, local_path(root)), 'destination overlaps preserved input')
    return target


def validate_plan(plan):
    keys(plan, {'schema', 'state', 'audience', 'destination', 'decision_reference',
                'input_digests', 'baseline', 'objects', 'views', 'replay_blockers',
                'source_execution_selected', 'future_preflight'})
    p.require(plan['schema'] == p.SCHEMA, 'wrong plan schema')
    p.require(plan['state'] == 'PLAN_ONLY_NOT_ASSEMBLED', 'plan-only state required')
    p.require(plan['source_execution_selected'] is False, 'source execution forbidden')
    p.require(plan['audience'] in {'owner_private_handoff', 'public_repository'}, 'invalid audience')
    p.identifier(plan['decision_reference'])
    p.require('v6' in p.relative(plan['destination']).casefold(), 'v6 destination required')
    keys(plan['input_digests'], {'lookup_sha256', 'v5_index_sha256', 'exclusions_sha256'})
    for value in plan['input_digests'].values():
        p.sha(value)
    baseline = plan['baseline']
    keys(baseline, {'archive_sha256', 'policy', 'whole_archive_publication_selected'})
    p.sha(baseline['archive_sha256'])
    p.require(baseline['policy'] == 'separate_unchanged_owner_checkpoint', 'baseline policy changed')
    p.require(baseline['whole_archive_publication_selected'] is False, 'whole archive not selected')
    p.require(isinstance(plan['future_preflight'], list) and all(isinstance(x, str) for x in plan['future_preflight']), 'invalid preflight metadata')
    p.require(not p.SENSITIVE.search(p.canonical(plan).decode()), 'private linkage in public plan')
    objects = plan['objects']
    p.require(isinstance(objects, list) and objects, 'explicit object selection required')
    selected = {}
    common = {'sha256', 'action', 'reviewed_digest', 'current_path_digest', 'scope_status', 'exclusion_categories'}
    for obj in objects:
        p.require(isinstance(obj, dict), 'invalid object')
        action = obj.get('action')
        p.require(action in {'include', 'identity_only', 'omit'}, 'invalid action')
        if action == 'include':
            keys(obj, common | {'role', 'required_dependencies', 'eligibility_basis', 'bytes', 'provider'},
                 {'original_sha256', 'transformation_receipt_sha256',
                  'received_public_qualification_sha256', 'original_equivalence_status'})
        else:
            keys(obj, common | {'availability'})
            p.require(obj['availability'] in {'held_excluded', 'exact_snapshot_unavailable'}, 'invalid availability')
        h = p.sha(obj['sha256'])
        p.require(h not in selected, 'duplicate selected identity')
        selected[h] = obj
        p.sha(obj['reviewed_digest'])
        if obj['current_path_digest'] is not None:
            p.sha(obj['current_path_digest'])
        p.identifier(obj['scope_status'])
        exclusions = obj['exclusion_categories']
        p.require(isinstance(exclusions, list) and all(isinstance(x, str) for x in exclusions), 'invalid exclusions')
        if action != 'include':
            continue
        p.require(not (set(exclusions) & p.HARD_REASONS) and
                  not any(x.startswith('lookup:') or x == 'sensitive_screen_flags' for x in exclusions),
                  'excluded source cannot be delivered')
        p.require(obj['eligibility_basis'] in p.BASIS, 'independent eligibility required')
        p.require(obj['role'] in ROLES, 'admitted role required')
        p.require(type(obj['bytes']) is int and obj['bytes'] >= 0, 'invalid source size')
        deps = obj['required_dependencies']
        p.require(isinstance(deps, list) and deps == sorted({p.sha(x) for x in deps}), 'invalid dependencies')
        provider = obj['provider']
        p.require(isinstance(provider, dict), 'invalid provider')
        if provider.get('kind') == 'authored_annex_object':
            keys(provider, {'kind', 'path'})
            p.require(provider['path'] == object_path(h), 'CAS provider mismatch')
        else:
            keys(provider, {'kind', 'archive_sha256', 'member'})
            p.require(provider['kind'] == 'separate_v5_member', 'invalid provider kind')
            p.require(provider['archive_sha256'] == baseline['archive_sha256'], 'baseline identity mismatch')
            p.relative(provider['member'])
        if obj['eligibility_basis'] == 'reviewed_public_projection':
            p.require({'original_sha256', 'transformation_receipt_sha256'} <= set(obj), 'projection linkage required')
            p.require(p.sha(obj['original_sha256']) != h, 'distinct projection identity required')
            p.sha(obj['transformation_receipt_sha256'])
            p.require('received_public_qualification_sha256' not in obj and
                      'original_equivalence_status' not in obj, 'unexpected received-public linkage')
        elif obj['eligibility_basis'] == 'reviewed_received_public_version':
            p.require({'original_sha256', 'received_public_qualification_sha256',
                       'original_equivalence_status'} <= set(obj), 'received-public linkage required')
            p.require(p.sha(obj['original_sha256']) != h, 'distinct original identity required')
            p.sha(obj['received_public_qualification_sha256'])
            p.require(obj['original_equivalence_status'] == 'unverified_original_unavailable' and
                      'transformation_receipt_sha256' not in obj,
                      'received-public version cannot assert original equivalence')
        else:
            p.require(not ({'original_sha256', 'transformation_receipt_sha256',
                           'received_public_qualification_sha256', 'original_equivalence_status'} & set(obj)),
                      'unexpected projection linkage')
    included = {h: obj for h, obj in selected.items() if obj['action'] == 'include'}
    blockers = []
    for h, obj in included.items():
        for dep in obj['required_dependencies']:
            p.require(dep in selected, 'missing explicit dependency disposition')
            if dep not in included:
                blockers.append({'consumer': h, 'dependency': dep, 'reason': 'required_dependency_not_delivered'})
        if obj['eligibility_basis'] == 'reviewed_public_projection':
            p.require(obj['original_sha256'] in selected and obj['transformation_receipt_sha256'] in included, 'projection evidence not delivered')
        elif obj['eligibility_basis'] == 'reviewed_received_public_version':
            original = selected.get(obj['original_sha256'], {})
            receipt = included.get(obj['received_public_qualification_sha256'], {})
            p.require(original.get('action') == 'identity_only' and
                      original.get('availability') == 'exact_snapshot_unavailable' and
                      receipt.get('role') == 'qualified_metadata',
                      'received-public qualification or unavailable original missing')
    p.require(plan['replay_blockers'] == sorted(blockers, key=lambda x: (x['consumer'], x['dependency'])), 'replay blocker mismatch')
    views = plan['views']
    p.require(isinstance(views, list), 'invalid view list')
    folded = set()
    component_spellings = {}
    seen_identities = set()
    for view in views:
        keys(view, {'path', 'sha256'})
        name = p.relative(view['path'])
        p.require('/' in name, 'packet/member view required')
        p.identifier(name.split('/')[0])
        p.require(view['sha256'] in included, 'view identity is not included')
        parts = name.split('/')
        for depth in range(1, len(parts) + 1):
            component = '/'.join(parts[:depth])
            key = component.casefold()
            p.require(component_spellings.get(key, component) == component, 'casefold directory alias')
            component_spellings[key] = component
        low = name.casefold()
        p.require(low not in folded, 'duplicate or casefold view collision')
        folded.add(low)
        seen_identities.add(view['sha256'])
    for name in folded:
        parts = name.split('/')
        for depth in range(1, len(parts)):
            p.require('/'.join(parts[:depth]) not in folded, 'file-directory view conflict')
    p.require(seen_identities == set(included), 'every included identity needs a view')
    p.require(views == sorted(views, key=lambda v: v['path']), 'view order must be canonical')
    return included


def make_map(plan, plan_hash, included):
    return {'schema': MAP_SCHEMA, 'plan_sha256': plan_hash,
            'objects': [{'sha256': h, 'bytes': obj['bytes'], 'path': object_path(h)}
                        for h, obj in sorted(included.items())],
            'views': plan['views']}


def make_receipt(plan_hash, view_map):
    return {'schema': RECEIPT_SCHEMA, 'state': 'MATERIALISED_SOURCE_ONLY',
            'plan_sha256': plan_hash, 'view_map_sha256': p.digest(p.canonical(view_map)),
            'object_count': len(view_map['objects']), 'view_count': len(view_map['views']),
            'total_unique_bytes': sum(obj['bytes'] for obj in view_map['objects']),
            'source_execution_selected': False}


def write_exclusive(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(data)

def validate_received_public_bodies(included, bodies):
    for h, obj in included.items():
        if obj['eligibility_basis'] == 'reviewed_received_public_version':
            p.validate_received_public_receipt(
                bodies[obj['received_public_qualification_sha256']], h, obj['original_sha256'])


def materialise(result, destination, protected_roots, workspace):
    """Preflight and copy an exact reviewed plan to a fresh, disjoint CAS directory."""
    keys(result, {'public_plan', 'plan_sha256', 'private_resolution'})
    # Snapshot JSON-shaped inputs; callers cannot mutate our metadata while writing.
    result = p.parse(p.canonical(result))
    plan = result['public_plan']
    plan_hash = p.sha(result['plan_sha256'])
    p.require(p.digest(p.canonical(plan)) == plan_hash, 'plan digest mismatch')
    included = validate_plan(plan)
    workspace = local_path(workspace)
    p.require(workspace.is_dir(), 'workspace must exist')
    resolutions = result['private_resolution']
    p.require(isinstance(resolutions, list), 'invalid private resolution')
    paths = {}
    for resolution in resolutions:
        keys(resolution, {'sha256', 'source_path', 'proposed_operation', 'provider'})
        h = p.sha(resolution['sha256'])
        p.require(h in included and h not in paths, 'private resolver identity mismatch')
        p.require(resolution['proposed_operation'] == 'resolve_exact_bytes_only', 'invalid resolution operation')
        p.require(resolution['provider'] == included[h]['provider'], 'resolver provider mismatch')
        p.require(isinstance(resolution['source_path'], str) and resolution['source_path'], 'source path required')
        paths[h] = local_path(workspace / resolution['source_path'])
    p.require(set(paths) == set(included), 'private resolver set mismatch')
    p.require(isinstance(protected_roots, (list, tuple)), 'explicit protected roots required')
    target = fresh_destination(destination, [*protected_roots, *paths.values()])
    bodies = {}
    for h, path in sorted(paths.items()):
        data = p.checked_read(path, h)
        p.require(len(data) == included[h]['bytes'], 'source size mismatch')
        bodies[h] = data
    validate_received_public_bodies(included, bodies)
    view_map = make_map(plan, plan_hash, included)
    receipt = make_receipt(plan_hash, view_map)
    target.mkdir()
    for h, data in bodies.items():
        write_exclusive(target / object_path(h), data)
    write_exclusive(target / 'PUBLIC_PLAN.json', p.canonical(plan))
    write_exclusive(target / 'VIEW_MAP.json', p.canonical(view_map))
    # Completion marker is last; failures above cannot appear complete.
    write_exclusive(target / 'MATERIALISATION.json', p.canonical(receipt))
    return receipt


def read_metadata(package, name):
    path = local_path(package / name)
    p.require(path.is_file(), 'missing package metadata: ' + name)
    raw = path.read_bytes()
    value = p.parse(raw)
    p.require(raw == p.canonical(value), 'noncanonical package metadata: ' + name)
    return value


def reconstruct_views(package, destination):
    """Verify a complete CAS package and copy only its selected views to a sibling.

    Returns a deterministic in-memory receipt. The output directory contains only
    selected paths, so no receipt filename can collide with a selected source path.
    """
    package = local_path(package)
    p.require(package.is_dir(), 'package directory required')
    target = fresh_destination(destination, [package])
    p.require(target.parent == package.parent, 'view destination must be a fresh sibling')
    plan = read_metadata(package, 'PUBLIC_PLAN.json')
    included = validate_plan(plan)
    plan_hash = p.digest(p.canonical(plan))
    view_map = read_metadata(package, 'VIEW_MAP.json')
    expected_map = make_map(plan, plan_hash, included)
    p.require(p.canonical(view_map) == p.canonical(expected_map), 'view map does not match selected plan')
    receipt = read_metadata(package, 'MATERIALISATION.json')
    p.require(p.canonical(receipt) == p.canonical(make_receipt(plan_hash, expected_map)), 'materialisation receipt mismatch')
    expected_paths = set()
    for obj in expected_map['objects']:
        path = Path(obj['path'])
        expected_paths.update([path, *path.parents][:-1])
    store = local_path(package / 'authored_objects')
    actual_paths = set()
    if store.exists():
        p.require(store.is_dir(), 'source store must be a directory')
        actual_paths.add(store.relative_to(package))
        for path in store.rglob('*'):
            local_path(path)
            actual_paths.add(path.relative_to(package))
    p.require(actual_paths == expected_paths, 'source store inventory mismatch')
    bodies = {}
    for obj in expected_map['objects']:
        h = obj['sha256']
        data = p.checked_read(package / obj['path'], h)
        p.require(len(data) == obj['bytes'], 'stored source size mismatch')
        bodies[h] = data
    validate_received_public_bodies(included, bodies)
    target.mkdir()
    for view in expected_map['views']:
        write_exclusive(target / view['path'], bodies[view['sha256']])
    return {'schema': 't20-v6-selected-source-reconstruction-v1',
            'state': 'RECONSTRUCTED_SOURCE_ONLY', 'plan_sha256': plan_hash,
            'view_map_sha256': receipt['view_map_sha256'],
            'view_count': len(expected_map['views']), 'source_execution_selected': False}
