#!/usr/bin/env python3
"""Finite checks for the continuation-information supplement.

No network access, source-repository mutation or physical experimentation.
Run with ordinary Python. Explicit exceptions, not removable assert statements,
implement every check. The algorithms below are deliberately small exact oracles,
not a scalable optimizer or a certification of the model premises.
"""
from __future__ import annotations

from collections import defaultdict, deque
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import inf
from pathlib import Path
from typing import Callable, Hashable, Iterable, Mapping
import argparse
import json
import platform
import sys
import traceback

class CheckFailure(RuntimeError):
    pass

def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)

def common(acceptable: Mapping[Hashable, frozenset], worlds: Iterable[Hashable]) -> frozenset:
    ws = tuple(worlds)
    if not ws:
        raise ValueError('An evidence fibre must be nonempty.')
    out = set(acceptable[ws[0]])
    for w in ws[1:]:
        out.intersection_update(acceptable[w])
    return frozenset(out)

def minimum_cover(acceptable: Mapping[Hashable, frozenset]) -> int | float:
    if not acceptable:
        raise ValueError('The situation set must be nonempty.')
    if any(not a for a in acceptable.values()):
        return inf
    candidates = sorted(set().union(*acceptable.values()), key=repr)
    for n in range(1, len(candidates) + 1):
        for ds in combinations(candidates, n):
            d = set(ds)
            if all(d.intersection(a) for a in acceptable.values()):
                return n
    raise CheckFailure('A finite union of nonempty acceptable sets did not cover.')

def minimum_partition(acceptable: Mapping[Hashable, frozenset]) -> int | float:
    """Independent oracle: partition W into cells with a common answer."""
    worlds = tuple(acceptable)
    if not worlds:
        raise ValueError('The situation set must be nonempty.')
    @lru_cache(None)
    def solve(mask: int) -> int | float:
        if mask == 0:
            return 0
        first = mask & -mask
        result = inf
        sub = mask
        while sub:
            if sub & first:
                members = [worlds[i] for i in range(len(worlds)) if sub & (1 << i)]
                if common(acceptable, members):
                    result = min(result, 1 + solve(mask ^ sub))
            sub = (sub - 1) & mask
        return result
    return solve((1 << len(worlds)) - 1)

def minimum_probe_depth(acceptable: Mapping[int, frozenset],
                        probes: tuple[tuple[int, ...], ...],
                        initial: tuple[int, ...] | None = None) -> int | float:
    """Exact nondestructive binary-probe decision depth on a finite relation."""
    if initial is None:
        initial = tuple(acceptable)
    if not initial:
        raise ValueError('Empty initial evidence is inconsistent, not success.')
    @lru_cache(None)
    def solve(ws: tuple[int, ...]) -> int | float:
        if common(acceptable, ws):
            return 0
        result = inf
        for probe in probes:
            cells: dict[int, list[int]] = defaultdict(list)
            for w in ws:
                cells[probe[w]].append(w)
            if len(cells) <= 1:
                continue
            result = min(result, 1 + max(solve(tuple(v)) for v in cells.values()))
        return result
    return solve(initial)

def partitions(items: tuple[int, ...]):
    """Enumerate set partitions exactly once, independently of acceptable sets."""
    if not items:
        yield ()
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        yield ((first,),) + p
        for j in range(len(p)):
            yield p[:j] + ((first,) + p[j],) + p[j + 1:]

Pair = tuple[Hashable, Hashable]
Belief = frozenset[Pair]
Action = Callable[[Hashable], tuple[Hashable, Hashable] | None]

def successors(belief: Belief, action: Action) -> tuple[Belief, ...] | None:
    by_observation: dict[Hashable, set[Pair]] = defaultdict(set)
    for origin, current in belief:
        result = action(current)
        if result is None:
            return None  # Uniform legality; no unmodelled informative refusal.
        nxt, observation = result
        by_observation[observation].add((origin, nxt))
    return tuple(frozenset(pairs) for _, pairs in sorted(by_observation.items(), key=lambda kv: repr(kv[0])))

def winning_rank(initial: Belief, actions: Mapping[str, Action],
                 acceptable_now: Callable[[Hashable, Hashable], frozenset],
                 max_beliefs: int = 10000) -> tuple[int | float, dict]:
    """Exact finite reachable-belief graph and least reachability fixed point."""
    if not initial:
        raise ValueError('Empty belief cannot establish a justified verdict.')
    reachable = {initial}
    queue = deque([initial])
    graph = {}
    while queue:
        b = queue.popleft()
        graph[b] = {}
        for name, action in actions.items():
            nxt = successors(b, action)
            if nxt is None:
                continue
            graph[b][name] = nxt
            for nb in nxt:
                if nb not in reachable:
                    reachable.add(nb)
                    queue.append(nb)
                    if len(reachable) > max_beliefs:
                        raise ValueError('Declared finite exploration ceiling exceeded.')
    ranks = {}
    for b in reachable:
        vals = [acceptable_now(w, x) for w, x in b]
        intersection = set(vals[0])
        for v in vals[1:]:
            intersection.intersection_update(v)
        if intersection:
            ranks[b] = 0
    rounds = 0
    while True:
        newly = {}
        for b in reachable - ranks.keys():
            possible = [1 + max(ranks[nb] for nb in bs)
                        for bs in graph[b].values() if all(nb in ranks for nb in bs)]
            if possible:
                newly[b] = min(possible)
        if not newly:
            break
        ranks.update(newly)
        rounds += 1
    return ranks.get(initial, inf), {'reachable_beliefs': len(reachable),
                                    'winning_beliefs': len(ranks), 'rank_iterations': rounds}

def check_cover_partition_equivalence() -> dict:
    cases = 0
    candidates = (0, 1, 2)
    nonempty = [frozenset(s) for n in range(1, 4) for s in combinations(candidates, n)]
    for nworlds in range(1, 5):
        for rows in product(nonempty, repeat=nworlds):
            relation = dict(enumerate(rows))
            a, b = minimum_cover(relation), minimum_partition(relation)
            require(a == b, f'Cover/partition disagreement: {relation!r}, {a}, {b}')
            cases += 1
    tri = {0: frozenset('ab'), 1: frozenset('bc'), 2: frozenset('ac')}
    require(all(common(tri, pair) for pair in combinations(tri, 2)), 'Pairwise overlap example malformed.')
    require(not common(tri, tri), 'Triple obstruction was not generated.')
    require(minimum_cover(tri) == 2, 'Triple example covering number incorrect.')
    return {'enumerated_nonempty_relations': cases, 'triple_pairwise_overlap_global_failure': True}

def check_leaf_bound() -> dict:
    finite_cases = 0
    impossible_cases = 0
    unrestricted_tight_cases = 0
    nonempty = [frozenset(s) for n in range(1, 4) for s in combinations(range(3), n)]
    for nworlds in range(1, 4):
        binary_maps = tuple(product((0, 1), repeat=nworlds))
        repertoires = [()] + [(p,) for p in binary_maps]
        repertoires += list(combinations(binary_maps, 2))
        parts = tuple(partitions(tuple(range(nworlds))))
        for rows in product(nonempty, repeat=nworlds):
            relation = dict(enumerate(rows))
            kappa = minimum_cover(relation)
            unrestricted = minimum_probe_depth(relation, binary_maps)
            expected = (int(kappa) - 1).bit_length()
            require(unrestricted == expected, 'Unrestricted binary-probe tightness failed.')
            unrestricted_tight_cases += 1
            for probes in repertoires:
                for part in parts:
                    depths = [minimum_probe_depth(relation, tuple(probes), tuple(cell)) for cell in part]
                    d = max(depths)
                    if d == inf:
                        impossible_cases += 1
                        continue
                    require(kappa <= len(part) * (2 ** int(d)), 'Fixed-target leaf-count bound failed.')
                    finite_cases += 1
    hidden = {0: frozenset({0}), 1: frozenset({1})}
    depth = minimum_probe_depth(hidden, ((0, 0),))
    require(depth == inf, 'Constant probes incorrectly resolved hidden bit.')
    require(minimum_cover(hidden) <= 2, 'Numerical capacity counterexample malformed.')
    return {'finite_record_probe_cases': finite_cases, 'unresolvable_record_probe_cases': impossible_cases,
            'unrestricted_tight_cases': unrestricted_tight_cases,
            'capacity_bound_not_sufficient_for_constant_probes': True}

def check_query_quantifiers() -> dict:
    by_k = []
    for k in range(1, 9):
        worlds = tuple(product((0, 1), repeat=k))
        query_depths = []
        for q in range(k):
            relation = {i: frozenset({w[q]}) for i, w in enumerate(worlds)}
            probe = tuple(w[q] for w in worlds)
            d = minimum_probe_depth(relation, (probe,))
            require(d == 1, f'Coordinate {q} did not require and admit exactly one probe.')
            query_depths.append(d)
        cells = [worlds]
        trace_counts = [len(cells)]
        for q in range(k):
            new_cells = []
            for cell in cells:
                for bit in (0, 1):
                    sub = tuple(w for w in cell if w[q] == bit)
                    if sub:
                        new_cells.append(sub)
            cells = new_cells
            trace_counts.append(len(cells))
        require(all(len(cell) == 1 for cell in cells), 'Sequential vector recovery did not identify all worlds.')
        require(len(cells) == 2 ** k, 'Full-vector leaf count disagrees with generated worlds.')
        require(all(any(x[q] != y[q] for q in range(k)) for x, y in combinations(worlds, 2)),
                'Different bit strings were not separated by a coordinate query.')
        by_k.append({'k': k, 'worlds': len(worlds), 'record_bits': 0,
                     'per_query_maximum_depth': max(query_depths),
                     'full_vector_generated_leaf_counts': trace_counts,
                     'family_wide_b_plus_d_ge_k_is_false': k > 1})
    return {'coordinate_families': by_k}

def check_calibration_continuation() -> dict:
    worlds = tuple(product((0, 1), repeat=3))  # b,c,k
    fibres: dict[tuple, list] = defaultdict(list)
    for b, c, k in worlds:
        y = c ^ k
        fibres[(b, y)].append((b, c, k))
        require((y ^ k) == c, 'Retained polarity did not decode.')
        reference = 0 ^ k
        require((y ^ reference) == c, 'Reference reacquisition did not decode.')
    ambiguous = sum(len({w[1] for w in cell}) > 1 for cell in fibres.values())
    require(ambiguous == len(fibres), 'Not all no-calibration fibres exhibit the intended ambiguity.')
    sequence_checks = 0
    for length in range(7):
        for inputs in product((0, 1), repeat=length):
            for initial in (0, 1):
                for cut in range(length + 1):
                    source = initial
                    for a in inputs[:cut]:
                        source ^= a
                    destination = source  # Exact stipulated handover, not a physical experiment.
                    for a in inputs[cut:]:
                        destination ^= a
                    reference = initial
                    for a in inputs:
                        reference ^= a
                    require(destination == reference, 'Parity continuation failed at generated cut.')
                    sequence_checks += 1
    return {'worlds': len(worlds), 'ambiguous_postmigration_sensor_fibres': ambiguous,
            'generated_parity_sequence_cut_checks': sequence_checks,
            'retained_calibration_and_reference_reacquisition_both_decode': True}

def check_destructive_labels_and_resources() -> dict:
    labels = {'p': 0, 'q': 0, 'r': 1}
    table_a = {'p': 't1', 'q': 't0', 'r': 't0', 't0': 't0', 't1': 't1'}
    table_b = {'p': 't0', 'q': 't1', 'r': 't0', 't0': 't0', 't1': 't1'}
    obs = {'t0': 0, 't1': 1}
    actions = {name: (lambda x, table=table: (table[x], obs[table[x]]))
               for name, table in [('a', table_a), ('b', table_b)]}
    initial = frozenset((w, w) for w in labels)
    rank, data = winning_rank(initial, actions, lambda w, x: frozenset({labels[w]}))
    require(rank == inf, 'Destructive experiment falsely yielded a global sound strategy.')
    for pair in combinations(labels, 2):
        require(any(obs[t[pair[0]]] != obs[t[pair[1]]] for t in (table_a, table_b)),
                'The pairwise distinguishability premise was not generated.')

    resource_initial = frozenset((w, (w, 1)) for w in (0, 1))
    good = lambda w, x: frozenset({w}) if x[1] == 1 else frozenset()
    destructive = {'measure': lambda x: ((x[0], 0), x[0])}
    retained_resource = {'measure': lambda x: (x, x[0])}
    dr, dd = winning_rank(resource_initial, destructive, good)
    nr, nd = winning_rank(resource_initial, retained_resource, good)
    require(dr == inf, 'Consumed battery was incorrectly treated as terminally executable.')
    require(nr == 1, 'Non-destructive probe should decide in exactly one step.')
    return {'pairwise_distinguishable_but_no_global_strategy': data,
            'destructive_resource_model': dd, 'resource_preserving_model': nd,
            'resource_preserving_initial_rank': nr}

def check_iterator_representation_invariance() -> dict:
    """A direct semantic regression requirement, not an attribution to an unread helper."""
    relation = {0: frozenset('ab'), 1: frozenset('bc'), 2: frozenset('ac')}
    checks = 0
    for n in range(1, 4):
        for subset in combinations(relation, n):
            expected = common(relation, subset)
            for representation in (list(subset), set(subset), iter(subset), (x for x in subset)):
                require(common(relation, representation) == expected,
                        'One-shot iterable changed the common-answer calculation.')
                checks += 1
    try:
        common(relation, iter(()))
    except ValueError:
        empty_rejected = True
    else:
        empty_rejected = False
    require(empty_rejected, 'Empty evidence was not rejected.')
    return {'container_and_single_pass_iterable_checks': checks, 'empty_evidence_rejected': True,
            'scope': 'This tests the new helper only. It does not claim to repair the frontier support helper.'}

def run(output: Path) -> dict:
    if not __debug__:
        raise RuntimeError('Run ordinary Python; assertion-disabled execution is not accepted as this receipt.')
    groups = [check_cover_partition_equivalence, check_leaf_bound, check_query_quantifiers,
              check_calibration_continuation, check_destructive_labels_and_resources,
              check_iterator_representation_invariance]
    report = {'status': 'PASS', 'python': sys.version, 'platform': platform.platform(),
              'ordinary_python': __debug__, 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Synthetic finite models only; no empirical, source-completeness, novelty or adoption claim.',
              'checks': []}
    for group in groups:
        try:
            detail = group()
            report['checks'].append({'name': group.__name__, 'status': 'PASS', 'result': detail})
        except Exception as exc:
            report['status'] = 'FAIL'
            report['checks'].append({'name': group.__name__, 'status': 'FAIL', 'error': repr(exc),
                                     'traceback': traceback.format_exc()})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('continuation_information_results.json'))
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result['status'] == 'PASS' else 1)
