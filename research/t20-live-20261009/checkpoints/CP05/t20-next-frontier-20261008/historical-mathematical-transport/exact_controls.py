#!/usr/bin/env python3
"""Exact finite diagnostics for historical mathematical transport. No network or writes."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import hashlib
import json


def optimal(labels, prices):
    @lru_cache(None)
    def solve(lo, hi):
        if len(set(labels[lo:hi])) == 1:
            return 0
        return min(prices[k - 1] + max(solve(lo, k), solve(k, hi))
                   for k in range(lo + 1, hi))
    return solve(0, len(labels))


def count_runs(labels):
    return 1 + sum(a != b for a, b in zip(labels, labels[1:]))


def ceil_log2(n):
    return (n - 1).bit_length()


def channel_rows(q):
    return [tuple(z * z for z in q),
            tuple(z * (1 - z) for z in q),
            tuple(z * (1 - z) for z in q),
            tuple((1 - z) ** 2 for z in q)]


def dot(v, w):
    return sum(a * b for a, b in zip(v, w))


def det3(rows):
    a, b, c = rows
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def adaptive_law(count, max_depth, policy_index):
    """Finite randomized adaptive policies, with seed visible in full transcript."""
    rates = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
    out = {}

    def visit(seed, history, mass):
        depth = len(history)
        bits = [bit for _, bit in history]
        early = depth > 0 and ((seed + policy_index) % 3 == 0) and bits[-1] == 1
        if depth == max_depth or early:
            out[(seed, history)] = mass
            return
        index = (seed + 2 * depth + sum((k + 1) * bit for k, bit in enumerate(bits))
                 + policy_index * (depth + 1)) % len(rates)
        x = rates[index]
        q = (1 - x) ** count
        for bit, chance in ((1, q), (0, 1 - q)):
            if chance:
                visit(seed, history + ((x, bit),), mass * chance)

    for seed in range(4):
        visit(seed, (), F(1, 4))
    assert sum(out.values()) == 1
    assert all(p > 0 for p in out.values())
    return out


def main():
    boolean_cases = 0
    for size in range(1, 11):
        for labels in product((0, 1), repeat=size):
            observed = optimal(labels, (1,) * (size - 1))
            assert observed == ceil_log2(count_runs(labels)), (labels, observed)
            boolean_cases += 1

    labels = (0, 0, 1, 1, 0, 0)
    prices = (100, 10, 1, 10, 100)
    assert optimal(labels, prices) == 11
    first_cut_costs = [prices[k - 1] + max(optimal(labels[:k], prices[:k - 1]),
                                         optimal(labels[k:], prices[k:]))
                       for k in range(1, len(labels))]
    assert first_cut_costs == [111, 20, 11, 20, 111]

    d = (F(1, 2), F(1, 2), F(-1))
    linear_cases = 0
    for denominator in range(2, 18):
        for numerator in range(1, denominator):
            t = F(numerator, denominator)
            q = (t, t * t, (t + t * t) / 2)
            assert dot((1, 1, 1), d) == 0 and dot(q, d) == 0
            diff = tuple(dot(row, d) for row in channel_rows(q))
            gap = t * t * (1 - t) ** 2 / 4
            assert diff == (gap, -gap, -gap, gap) and gap > 0
            assert det3(((F(1),) * 3, q, channel_rows(q)[0])) != 0
            linear_cases += 1
    q = (F(1, 2), F(1, 4), F(3, 8))
    assert det3(((F(1),) * 3, q, channel_rows(q)[0])) == F(1, 256)
    assert dot(channel_rows(q)[0], d) == F(1, 64)

    pointwise_checks = 0
    for n, m in combinations(range(1, 9), 2):
        for denominator in range(1, 18):
            for numerator in range(denominator + 1):
                x = F(numerator, denominator)
                qn, qm = (1 - x) ** n, (1 - x) ** m
                assert (qn > 0) == (qm > 0)
                assert (qn < 1) == (qm < 1)
                pointwise_checks += 1

    adaptive_checks = 0
    for max_depth in range(1, 7):
        for policy_index in range(4):
            laws = [adaptive_law(j, max_depth, policy_index) for j in range(1, 9)]
            for p, qlaw in combinations(laws, 2):
                assert set(p) == set(qlaw)
                adaptive_checks += 1

    here = Path(__file__).resolve().parent
    bindings = json.loads((here / 'SOURCE_BINDINGS.json').read_text())
    for item in bindings['local_compared_proofs']:
        data = (here.parent / item['path']).read_bytes()
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']

    print(json.dumps({
        'status': 'PASS',
        'unit_price_boolean_catalogues': boolean_cases,
        'heterogeneous_price_optimum': 11,
        'heterogeneous_first_cut_costs': first_cut_costs,
        'rational_linear_channel_cases': linear_cases,
        'channel_gap_at_half': '1/64',
        'augmented_record_determinant_at_half': '1/256',
        'pointwise_common_support_checks': pointwise_checks,
        'adaptive_stopped_transcript_support_comparisons': adaptive_checks,
        'bound_current_proofs_verified': len(bindings['local_compared_proofs']),
        'scope': 'Finite exact diagnostics only; general results rely on written proofs.'
    }, indent=2))


if __name__ == '__main__':
    main()
