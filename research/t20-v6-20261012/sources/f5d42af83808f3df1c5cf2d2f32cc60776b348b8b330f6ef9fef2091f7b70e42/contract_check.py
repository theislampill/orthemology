"""Finite record-view application of inherited T20 D1/D2; no warrant classifier."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import hashlib
import json

SOURCE = Path(__file__).resolve().parents[1] / 'sources' / 'source_rows.json'
EXPECTED_SHA = '67f405c245093546dd26c142db7fd09eea1513b9fb853521d496bca7a70e8a62'

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def partitions(n):
    """Each set partition once as a restricted-growth block-label tuple."""
    def grow(xs, high):
        if len(xs) == n:
            yield tuple(xs)
            return
        for value in range(high + 2):
            yield from grow(xs + [value], max(high, value))
    yield from grow([0], 0)

def analyse():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA, 'source byte drift')
    data = json.loads(raw)
    records = data['records']
    require(len(records) == 7, 'seven supplied records')
    require(len({r['claim_id'] for r in records}) == 7, 'distinct claim identities')
    require(data['independent_acquisition_of_attributed_authorities'] is False, 'attribution scope')
    rows = [tuple(r['antecedents']) for r in records]
    roles = [r['role'].startswith('direct_exposition') for r in records]
    works = [r['work_id'] for r in records]
    work_names = sorted(set(works))
    # Exclusion affects only this hypothetical view. It is not source deletion,
    # falsification, revocation of authority, or a new historical judgment.
    dead = len(records)
    coarse = rows + [('excluded-from-view',)]
    voices = roles + [None]
    state_count = dead + 1
    def target(s, action):
        if s == dead or action == 'copy':
            return s
        return dead if works[s] == action else s
    def valid(blocks, include_voice, exclude):
        groups = defaultdict(list)
        for s, b in enumerate(blocks):
            groups[b].append(s)
        actions = ['copy'] + (work_names if exclude else [])
        for group in groups.values():
            first = group[0]
            for s in group[1:]:
                if coarse[s] != coarse[first]:
                    return False
                if include_voice and voices[s] != voices[first]:
                    return False
                for action in actions:
                    if blocks[target(s, action)] != blocks[target(first, action)]:
                        return False
        return True
    all_parts = list(partitions(state_count))
    require(len(all_parts) == 4140, 'Bell(8) enumeration')
    result = {'input_sha256': EXPECTED_SHA, 'record_count': 7, 'state_count': 8,
              'partitions_enumerated': len(all_parts), 'minimum_alphabets': {},
              'contracts': {}, 'negative_controls': {}}
    for name, voice, exclusion in [('content_only', False, False),
                                    ('content_and_voice', True, False),
                                    ('content_voice_and_work_exclusion', True, True)]:
        accepted = [p for p in all_parts if valid(p, voice, exclusion)]
        least_size = min(len(set(p)) for p in accepted)
        coarsest = [p for p in accepted if len(set(p)) == least_size]
        require(len(coarsest) == 1, name + ': unique coarsest partition')
        p = coarsest[0]
        by_fibre = defaultdict(set)
        for i, key in enumerate(coarse):
            by_fibre[key].add(p[i])
        minimum = max(map(len, by_fibre.values()))
        # Independent exhaustive search over encoders; excluded state has a
        # distinct retained coarse key, so its sidecar value can be fixed at 0.
        encoding_counts = {}
        for alphabet in range(1, minimum + 1):
            count = 0
            for labels in product(range(alphabet), repeat=len(records)):
                enc = list(zip(coarse, labels + (0,)))
                if valid(enc, voice, exclusion):
                    count += 1
            encoding_counts[str(alphabet)] = count
        require(encoding_counts[str(minimum)] > 0, name + ': attaining encoder')
        require(all(v == 0 for a, v in encoding_counts.items() if int(a) < minimum),
                name + ': no smaller encoder')
        result['minimum_alphabets'][name] = minimum
        result['contracts'][name] = {
            'coarsest_partition': p, 'coarsest_blocks': least_size,
            'valid_partitions': len(accepted), 'encoding_counts': encoding_counts,
            'fixed_width_bits': (minimum - 1).bit_length(),
            'fibre_block_counts': {str(k): len(v) for k, v in by_fibre.items()}}
    row_only = coarse
    row_voice = list(zip(coarse, voices))
    result['negative_controls']['row_only_loses_voice'] = not valid(row_only, True, False)
    result['negative_controls']['row_voice_loses_work_exclusion'] = not valid(row_voice, True, True)
    # Two actual MMG reporting records collide under (row, reporting voice).
    a, b = 2, 4
    require(rows[a] == rows[b] and roles[a] == roles[b] and works[a] != works[b], 'real collision')
    require(target(a, works[a]) == dead and target(b, works[a]) == b, 'discriminating operation')
    result['collision'] = {'records': [records[a]['claim_id'], records[b]['claim_id']],
                           'shared_row': rows[a], 'shared_voice': 'reported',
                           'operation': 'exclude_work(' + works[a] + ')',
                           'outcomes': ['excluded', 'retained']}
    # Source-specified missing value remains missing under every representation.
    require(rows[6] == ('M', 'M', None), 'partial record preserved')
    complete = {r for r in rows if None not in r}
    require(complete == {('M', 'M', 'G'), ('G', 'G', 'G')}, 'complete source rows')
    require({tuple(r['antecedents']) for r in records + [records[0]] if None not in r['antecedents']} == complete,
            'copy does not add source reading')
    require(all(result['negative_controls'].values()), 'negative controls')
    result['scope'] = 'Exact frozen-record view contract only; no Arabic, historical, authority, or human-warrant validation.'
    return result

if __name__ == '__main__':
    print(json.dumps(analyse(), indent=2))
