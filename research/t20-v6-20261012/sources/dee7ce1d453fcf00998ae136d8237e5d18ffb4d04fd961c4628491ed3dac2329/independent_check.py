"""Independent bounded replay. No Lean, external optimizer, or world claims.

All local file reads are hash-bound. Only derived in-memory states are changed.
Explicit exception checks remain active with python -O. Output is JSON on stdout.
"""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 't20-closure-audit-20261011'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


checked = {}
for row in json.loads((AUDIT / 'early_foundations/SOURCE_BINDINGS.json').read_text())['sources']:
    path = ROOT / row['path']
    expected = row.get('public_sha256', row.get('sha256'))
    require(digest(path) == expected, f'Foundation binding: {path}')
    checked[row['path']] = expected
for row in json.loads((AUDIT / 'early_operations/SOURCE_BINDINGS.json').read_text()):
    path = ROOT / row['local_path']
    require(digest(path) == row['sha256'], f'Operation binding: {path}')
    checked[row['local_path']] = row['sha256']
protected = {}
for row in json.loads((AUDIT / 'early_operations/V4_TARGET_BINDINGS.json').read_text()):
    require(digest(ROOT / row['path']) == row['sha256'], f'Protected target binding: {row["path"]}')
    protected[row['path']] = row['sha256']

# Read the actual historical U01 paragraph and current source-owned disposition.
# Their classification is an attributed current record, not freshly verified Lean.
hist_sha = '2795cb401c807b28b3fc84c4f46986e9f12ac040d5b40d3a6594634a4c38b40f'
cur_sha = 'e4c4a52d9739c118328f2614d763f5dc0b5b9d476529c695e2e6f0c2404c2449'


def obj(h):
    path = ROOT / 't20-consolidation-20261011/catalogue/objects' / h[:2] / h
    require(digest(path) == h, f'Canonical object hash {h}')
    return path


historical_path, current_path = obj(hist_sha), obj(cur_sha)
historical_bytes, current_bytes = historical_path.read_bytes(), current_path.read_bytes()
body = historical_bytes.decode()
section = re.search(r'## U01 — (.*?)\n(.*?)(?=\n## U02)', body, re.S)
require(section is not None, 'U01 section exists')
title, rest = section.groups()
record = {
    'id': 'U01', 'obligation': title.strip(),
    'blocker': re.search(r'^Blocker: (.+)$', rest, re.M).group(1),
    'method': re.search(r'^Method: (.+)$', rest, re.M).group(1),
    'sources': re.findall(r'\[[^\]]+\]\(([^)]+)\)', re.search(r'^Sources: (.+)$', rest, re.M).group(1)),
}
rows = json.loads(current_bytes)['additional_dispositions']
u01s = [r for r in rows if r['id'] == 'U01']
require(len(u01s) == 1, 'Exactly one current U01 owner row')
owner = u01s[0]
require(owner['original_record'] == record, 'Current owner preserves the parsed historical record')
require(record['blocker'].startswith('No installed compiler;'), 'Historical scope is compiler absence')
require(owner['classification'] == 'HISTORICAL_KERNEL_GAP_CURRENT_MAPPED_SCOPE_SEPARATELY_DISCHARGED', 'Exact current classification')
require(owner['research_task'] is False, 'Source itself does not restart the historical task')
application = json.loads((AUDIT / 'early_foundations/BOUNDED_APPLICATION.json').read_text())
require(application['result']['historical_source_sha256'] == hist_sha, 'Application historical source identity')
require(application['result']['historical_U01'] == record, 'Application record matches independently parsed source')
require(application['result']['current_classification'] == owner['classification'], 'Application current attribution matches actual owner')

# Synthetic stale derived assertions; these are not claimed to be defects in v4.
# Each map reads its own fixed source, never the other mutable assertion field.
def repair_history(state):
    result = deepcopy(state)
    result['historical_assertion'] = {'attributed_to': hist_sha, 'record': deepcopy(record)}
    return result


def repair_current(state):
    result = deepcopy(state)
    result['current_assertion'] = {
        'attributed_to': cur_sha, 'classification': owner['classification'],
        'research_task': owner['research_task'], 'scope': 'current owner record only; no kernel replay',
    }
    return result


target_history = repair_history({})['historical_assertion']
target_current = repair_current({})['current_assertion']
initials = []
for h, c in product([None, {'stale': 'compiler available historically'}, target_history],
                    [None, {'stale': 'all historical declarations discharged'}, target_current]):
    initials.append({'immutable_historical_record': deepcopy(record),
                     'source_ids': [hist_sha, cur_sha], 'unaffected': {'custody': 'retained'},
                     'historical_assertion': deepcopy(h), 'current_assertion': deepcopy(c)})
for state in initials:
    before = deepcopy(state)
    h, c = repair_history(state), repair_current(state)
    require(repair_history(h) == h, 'History idempotence')
    require(repair_current(c) == c, 'Current idempotence')
    final = repair_current(h)
    require(final == repair_history(c), 'Commutation')
    require(final['historical_assertion'] == target_history, 'Historical attribution adequate')
    require(final['current_assertion'] == target_current, 'Current attribution adequate')
    for key in ['immutable_historical_record', 'source_ids', 'unaffected']:
        require(final[key] == state[key], 'Custody and unaffected fields retained')
    require(state == before, 'Repair maps do not mutate their input')
require(historical_path.read_bytes() == historical_bytes, 'Historical bytes unchanged')
require(current_path.read_bytes() == current_bytes, 'Current owner bytes unchanged')

# Deletion control: copying a mutable, stale transcription loses commutation.
def source_correct(s):
    return {**s, 'transcription': record['blocker']}


def stale_copy(s):
    return {**s, 'claim': s['transcription']}


stale = {'transcription': 'compiler available historically', 'claim': None}
require(source_correct(stale_copy(stale)) != stale_copy(source_correct(stale)), 'Stale-copy deletion witness')

# Finite corroboration of the inherited LocalCover bridge, not general proof.
def below(rel, a, b):
    return a == b or (a, b) in rel


def local_cover(nodes, rel, g, x):
    return below(rel, g, x) and all(not below(rel, y, x) or below(rel, g, y) for y in nodes)


def connected(nodes, rel):
    seen = {nodes[0]}
    while True:
        new = seen | {y for x in seen for y in nodes if (x, y) in rel or (y, x) in rel}
        if new == seen:
            return len(seen) == len(nodes)
        seen = new


posets = connected_locally_complete = 0
for n in range(1, 5):
    nodes = list(range(n)); pairs = [(a, b) for a in nodes for b in nodes if a != b]
    for mask in range(1 << len(pairs)):
        rel = {p for i, p in enumerate(pairs) if (mask >> i) & 1}
        if not all((a, c) in rel for a, b in rel for bb, c in rel if b == bb):
            continue
        posets += 1
        covers = {x: {g for g in nodes if local_cover(nodes, rel, g, x)} for x in nodes}
        require(all(len(s) <= 1 for s in covers.values()), 'Local cover uniqueness')
        for x, y in rel:
            if covers[x] and covers[y]:
                require(covers[x] == covers[y], 'Local cover edge agreement')
        if connected(nodes, rel) and all(covers.values()):
            connected_locally_complete += 1
            common = set.intersection(*covers.values())
            require(len(common) == 1, 'Singleton gluing')
            g = next(iter(common))
            require(all(below(rel, g, x) for x in nodes), 'Least ancestor')

# Nonconverse: a stipulated constant adequacy family glues even when it has no
# warranted correspondence with the actual ancestral LocalCover relation.
nodes = [0, 1, 2]; merge = {(0, 2), (1, 2)}
arbitrary_U = {x: {0} for x in nodes}
require(connected(nodes, merge), 'Nonconverse connected field')
require(all(arbitrary_U[x] & arbitrary_U[y] for x, y in merge), 'Nonconverse edge overlap')
require(not any(local_cover(nodes, merge, g, 2) for g in nodes), 'No LocalCover at merge target')

# Exact operational erasure calculation and timing controls.
roots = tuple(range(8)); faults = list(combinations(roots, 3)); menus = list(combinations(roots, 2))
require(len(faults) == 56 and len(menus) == 28, 'Finite census')
shared = {C: F(sum(set(T) <= set(C) for T in menus), len(menus)) for C in faults}
require(set(shared.values()) == {F(3, 28)}, 'Shared risk for every static fault set')
rows = [[F(sum(T[m] == i for T in menus), 28) for i in roots] for m in range(2)]
require(rows[0] == [F(7-i, 28) for i in roots] and rows[1] == [F(i, 28) for i in roots], 'Exact sorted decoder marginals')
require(all(sum(row) == 1 for row in rows), 'Decoder normalization')
risks = {C: min(sum(row[i] for i in C) for row in rows) for C in faults}
require(all(v == F(min(sum(C), 21-sum(C)), 28) for C, v in risks.items()), 'Exact closed risk formula')
require(max(risks.values()) == F(5, 14), 'Exact erased risk, not merely an inequality')
require(risks[(0, 3, 7)] == F(5, 14), 'Explicit maximizing witness')
require(max(risks.values()) - F(3, 28) == F(1, 4), 'Exact risk increase')
blocks = [set(range(4)), set(range(4, 8))]
partition = max(min(F(len(set(C) & B), 4) for B in blocks) for C in faults)
require(partition == F(1, 4), 'Fixed partition performance, not arbitrary-codebook lower proof')
require(all(any(set(T) <= set(C) for C in faults) for T in menus), 'Unchanged exposed menu has loss one')
require({sum(F(1, 8) for _ in C) for C in faults} == {F(3, 8)}, 'Uniform private row after message')
require(all(any(i in C for C in faults) for i in roots), 'Every exposed root can be corrupted')
random_order_rows = [[F(sum(i in T for T in menus), 56) for i in roots] for _ in range(2)]
require(random_order_rows == [[F(1, 8)] * 8] * 2, 'Random order erasure yields two uniform rows')
require(max(min(sum(row[i] for i in C) for row in random_order_rows) for C in faults) == F(3, 8), 'Erasure depends on label convention')

for path, expected in checked.items():
    require(digest(ROOT / path) == expected, f'Source unchanged after checks: {path}')
for path, expected in protected.items():
    require(digest(ROOT / path) == expected, f'Protected target unchanged after checks: {path}')

print(json.dumps({
    'status': 'PASS',
    'scope': 'Fresh source-bound attribution repair and finite reference controls; no kernel, external theorem, deployment or metaphysical certification',
    'source_paths_hash_checked': len(checked),
    'protected_v4_paths_hash_checked_unchanged': len(protected),
    'u01': {'historical_sha256': hist_sha, 'current_owner_sha256': cur_sha,
            'states_tested': len(initials), 'source_record_equal': True,
            'maps_idempotent_commuting': True, 'source_bytes_unchanged': True,
            'stale_copy_noncommutation_detected': True,
            'classification_authority': 'Read from bound owner; not a new substantive kernel verification'},
    'local_cover': {'labelled_strict_posets_n1_through_n4': posets,
                    'connected_locally_complete_posets': connected_locally_complete,
                    'nonconverse': {'ancestry': sorted(merge), 'all_U': [0], 'target_without_cover': 2},
                    'limit': 'Finite corroboration and one nonconverse witness; general theorem inherited and statically read'},
    'operational': {'fault_sets': 56, 'menus': 28, 'shared_static': '3/28',
                    'sorted_erasure': '5/14', 'witness': [0, 3, 7], 'increase': '1/4',
                    'partition_attainment': '1/4', 'random_order_erasure': '3/8',
                    'unchanged_menu_after_seed': '1', 'uniform_after_message': '3/8', 'exposed_root': '1',
                    'limit': 'Global private-codebook optimality and schedule lower bounds come from inherited ordinary proofs, not finite enumeration'}
}, indent=2))
