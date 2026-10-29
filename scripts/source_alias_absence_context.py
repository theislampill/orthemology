"""Receive the public nine-route change and retained Round19 conflict context."""
from pathlib import Path
from source_alias_absence_population import public_consumers, require


def derive_context(repo, classes):
    repo = Path(repo).resolve()
    snapshot, _ = public_consumers(repo)
    # This existing product predicate authenticates its original public Git
    # object and requires exactly nine textual path substitutions, with every
    # other byte unchanged. It also checks the current index binding.
    snapshot.pmr007_rounds_formalization_navigation(repo, indexed=True)
    current = snapshot.load_yaml(repo / snapshot.PMR007_ROUNDS_FORMALIZATION)
    by_retained = {r['canonical']: r['alias'] for r in classes if r['cohort'] == '98'}
    changes = []
    prefix = 'docs/project-closure/ar8r-v11/'
    for row in current['results']:
        retained = prefix + row['source_path']
        if retained in by_retained:
            changes.append({'result_id': row['result_id'], 'original': by_retained[retained], 'retained': retained})
    require(len(changes) == 9, 'Nine original public formalization routes are required')
    excluded = snapshot.PMR007_ROUNDS_PREFIX + '/' + snapshot.PMR007_ROUNDS_CONTEXT_MEMBER
    locator = excluded + '#exact-internal-ancestor'
    crosswalk = snapshot.load_yaml(snapshot.FAMILY_CROSSWALK)
    def dictionaries(value):
        if isinstance(value, dict):
            yield value
            for child in value.values(): yield from dictionaries(child)
        elif isinstance(value, list):
            for child in value: yield from dictionaries(child)
    rows = [row for row in dictionaries(crosswalk) if locator in row.get('basis_locators', [])]
    require(len(rows) == 1 and rows[0]['classification_status'] == 'UNRESOLVED_PUBLIC_OWNER_CONFLICT'
            and rows[0]['v5_family'] is None
            and rows[0]['candidate_v5_families'] == ['FAMILY-FIBRE', 'FAMILY-HIGHER']
            and rows[0]['relation'] == 'REDUCTION_OR_EXTENSION_NOT_IDENTITY',
            'Original Round19 public conflict changed')
    require(excluded not in {r['alias'] for r in classes} and (repo / excluded).is_file(),
            'Required contextual original is selected or absent')
    return {'changed_formalization_fields': changes, 'excluded_locator': locator,
            'excluded_conflict_row': rows[0]}
