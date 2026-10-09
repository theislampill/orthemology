#!/usr/bin/env python3
"""Independent state-table checks of the graph-restricted continuation transfer.
The BFS operates on full truth tables. It never uses the mask-transition rule.
The comparator computes connected supersets independently.
"""
from collections import deque
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json


def character(n, mask):
    return tuple((-1) ** ((x & mask).bit_count() % 2) for x in range(1 << n))


def state_gate(x, i, j):
    # The actual bit operation is x_i <- x_i xor x_j.
    return x ^ ((1 << i) if x & (1 << j) else 0)


def pullback(table, i, j):
    return tuple(table[state_gate(x, i, j)] for x in range(len(table)))


def truth_table_distances(n, edges):
    gates = tuple(edges) + tuple((j, i) for i, j in edges)
    d = {character(n, 1 << i): 0 for i in range(n)}
    q = deque(d)
    while q:
        f = q.popleft()
        for i, j in gates:
            g = pullback(f, i, j)
            if g not in d:
                d[g] = d[f] + 1
                q.append(g)
    return {s: d.get(character(n, s)) for s in range(1, 1 << n)}


def connected(n, edges, subset):
    if not subset:
        return False
    root = (subset & -subset).bit_length() - 1
    seen = {root}
    while True:
        old = set(seen)
        for i, j in edges:
            if (subset >> i) & 1 and (subset >> j) & 1:
                if i in seen:
                    seen.add(j)
                if j in seen:
                    seen.add(i)
        if seen == old:
            return len(seen) == subset.bit_count()


def steiner_cost(n, edges, s):
    costs = [2 * t.bit_count() - s.bit_count() - 1
             for t in range(1, 1 << n)
             if s & t == s and connected(n, edges, t)]
    return min(costs, default=None)


def expect(law, f):
    return sum((p * q for p, q in zip(law, f)), Fraction())


def main():
    graphs = pairs = gate_equations = 0
    for n in range(1, 5):
        possible = tuple(combinations(range(n), 2))
        for emask in range(1 << len(possible)):
            edges = tuple(e for k, e in enumerate(possible) if (emask >> k) & 1)
            d = truth_table_distances(n, edges)
            for s in range(1, 1 << n):
                assert d[s] == steiner_cost(n, edges, s), (n, edges, s, d[s])
                pairs += 1
            graphs += 1
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                for s in range(1 << n):
                    got = pullback(character(n, s), i, j)
                    target = s ^ (1 << j) if s & (1 << i) else s
                    assert got == character(n, target)
                    gate_equations += 1

    n = 4
    path = ((0, 1), (1, 2), (2, 3))
    d = truth_table_distances(n, path)
    ranks = [1 + sum(c is not None and c <= h for c in d.values()) for h in range(6)]
    assert ranks == [5, 8, 10, 13, 15, 16]
    endpoint = (1 << 0) | (1 << 3)
    assert d[15] == 3 and d[endpoint] == 5
    # Actual full physical circuits, as opposed to mask traces.
    for mask, circuit in [(15, [(2, 3), (1, 2), (0, 1)]),
                          (endpoint, [(0, 1), (1, 2), (2, 3), (1, 2), (0, 1)])]:
        for x in range(16):
            y = x
            for i, j in circuit:
                y = state_gate(y, i, j)
            assert (-1) ** (y & 1) == character(4, mask)[x]

    parity = character(4, endpoint)
    plus = tuple(Fraction(1 + p, 16) for p in parity)
    minus = tuple(Fraction(1 - p, 16) for p in parity)
    assert sum(plus) == sum(minus) == 1
    assert all(p >= 0 for p in plus + minus)
    retained = [s for s, c in d.items() if c is not None and c <= 3]
    for s in [0] + retained:
        assert expect(plus, character(4, s)) == expect(minus, character(4, s))
    event = tuple(Fraction(1 - p, 2) for p in parity)
    assert expect(plus, event) == 0 and expect(minus, event) == 1
    # In contrast, proper-marginal-only and full-degree-cutoff mutations fail.
    assert endpoint not in retained and 15 in retained
    assert d[endpoint] != endpoint.bit_count() - 1

    disconnected = ((0, 1), (2, 3))
    dd = truth_table_distances(4, disconnected)
    assert 1 + sum(v is not None for v in dd.values()) == 7
    assert dd[15] is None

    results = {
        'status': 'PASS', 'truth_table_graphs': graphs,
        'nonempty_graph_mask_comparisons': pairs,
        'pointwise_gate_character_identities': gate_equations,
        'path4_augmented_ranks': ranks,
        'path4_first_full_parity_horizon': d[15],
        'path4_first_endpoint_pair_horizon': d[endpoint],
        'path4_horizon3_retained_masks': retained,
        'separating_pair': {'normalised_nonnegative': True,
            'all_horizon3_moments_equal': True,
            'later_endpoint_event_probabilities': [0, 1],
            'minimax_error': '1/2'},
        'two_disconnected_edges_augmented_saturated_rank': 7,
        'negative_controls': ['complete-graph formula rejected on path endpoints',
            'downward-closed moment family rejected',
            'connected-graph saturation rejected on disconnected graph'],
        'scope': 'Exact finite checks; general theorem separately proved in Lean and prose.'}
    dest = Path(__file__).with_name('CONTROL_RESULTS.json')
    dest.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
