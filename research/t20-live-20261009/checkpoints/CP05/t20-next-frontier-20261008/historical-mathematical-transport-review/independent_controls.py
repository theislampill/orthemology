#!/usr/bin/env python3
"""Reviewer-written exact diagnostics; author artifacts are read-only inputs."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import subprocess
import sys


@lru_cache(None)
def trees(lo, hi):
    """All full ordered binary cut trees, independently of target labels/prices."""
    if hi - lo == 1:
        return ((lo, hi, None, None, None),)
    return tuple((lo, hi, k, left, right)
                 for k in range(lo + 1, hi)
                 for left in trees(lo, k) for right in trees(k, hi))


def tree_cost(tree, labels, prices):
    lo, hi, k, left, right = tree
    if all(labels[j] == labels[lo] for j in range(lo, hi)):
        return 0
    return prices[k - 1] + max(tree_cost(left, labels, prices),
                              tree_cost(right, labels, prices))


def enumerate_optimum(labels, prices, root=None):
    return min(tree_cost(t, labels, prices) for t in trees(0, len(labels))
               if root is None or t[2] == root)


def bellman(labels, prices):
    @lru_cache(None)
    def value(lo, hi):
        if len(set(labels[lo:hi])) == 1:
            return 0
        return min(prices[k - 1] + max(value(lo, k), value(k, hi))
                   for k in range(lo + 1, hi))
    return value(0, len(labels))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def endpoint_law(count, cap, policy):
    """Fresh randomized actions, randomized stopping, randomized final reports."""
    rates = (F(0), F(1, 3), F(2, 3), F(1))
    law = defaultdict(F)

    def visit(history, mass):
        depth = len(history)
        stop = F(1) if depth == cap else (F(1, 3) if depth else F(0))
        if stop:
            # Decisions use a common, genuinely random kernel as well.
            parity = sum(bit for _, bit in history) % 2
            law[(history, parity)] += mass * stop * F(2, 3)
            law[(history, 1 - parity)] += mass * stop * F(1, 3)
        if stop == 1:
            return
        index = (depth + policy + sum(bit for _, bit in history)) % 4
        for offset, chance in ((0, F(1, 3)), (1, F(2, 3))):
            action = rates[(index + offset) % 4]
            q = (1 - action) ** count
            for bit, probability in ((1, q), (0, 1 - q)):
                if probability:
                    visit(history + ((action, bit),),
                          mass * (1 - stop) * chance * probability)

    visit((), F(1))
    assert sum(law.values()) == 1 and all(v > 0 for v in law.values())
    return law


def main():
    here = Path(__file__).resolve().parent
    author = here.parent / 'historical-mathematical-transport'
    bindings = json.loads((here / 'REVIEW_BINDINGS.json').read_text())
    for item in bindings['frozen_author_files']:
        data = (author / item['path']).read_bytes()
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    for item in bindings['compared_modern_proofs']:
        data = (here.parent / item['path']).read_bytes()
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    replay = subprocess.check_output([sys.executable, str(author / 'exact_controls.py')])
    assert replay == (author / 'CONTROL_RESULTS.json').read_bytes()

    unit_cases = weighted_cases = 0
    for size in range(1, 9):
        for labels in product((0, 1), repeat=size):
            runs = 1 + sum(a != b for a, b in zip(labels, labels[1:]))
            optimum = enumerate_optimum(labels, (1,) * (size - 1))
            assert optimum == (runs - 1).bit_length()
            unit_cases += 1
    for size in range(1, 6):
        for labels in product((0, 1), repeat=size):
            for prices in product((1, 2, 5), repeat=size - 1):
                assert enumerate_optimum(labels, prices) == bellman(labels, prices)
                weighted_cases += 1
    for size in range(1, 9):
        assert enumerate_optimum(tuple(range(size)), (1,) * (size - 1)) == (size - 1).bit_length()
    labels, prices = (0, 0, 1, 1, 0, 0), (100, 10, 1, 10, 100)
    root_costs = [enumerate_optimum(labels, prices, k) for k in range(1, 6)]
    assert root_costs == [111, 20, 11, 20, 111]

    # Exact vanishing-margin family: n=3, m=3/2, so H_(n/m)=H_2.
    margins = []
    for exponent in range(2, 18):
        eps = F(1, 2 ** exponent)
        a, b = (eps, 2 * eps), (eps, 2 * eps)
        P = [[2 * x * y - (x * y) ** 2 for y in b] for x in a]
        determinant = P[0][0] * P[1][1] - P[0][1] * P[1][0]
        assert determinant == -8 * eps ** 6 < 0
        margins.append(str(abs(determinant)))
    assert all(F(a) > F(b) for a, b in zip(margins, margins[1:]))

    linear_cases = 0
    d = (F(1, 2), F(1, 2), F(-1))
    for denominator in range(2, 20):
        for numerator in range(1, denominator):
            t = F(numerator, denominator)
            q = (t, t * t, (t + t * t) / 2)
            A = ((F(1),) * 3, q)
            T = (tuple(x * x for x in q), tuple(x * (1 - x) for x in q),
                 tuple(x * (1 - x) for x in q), tuple((1 - x) ** 2 for x in q))
            gap = t * t * (1 - t) ** 2 / 4
            assert all(dot(row, d) == 0 for row in A)
            assert tuple(dot(row, d) for row in T) == (gap, -gap, -gap, gap)
            assert all(sum(row[j] for row in T) == 1 for j in range(3))
            linear_cases += 1

    # Omitting mass retention makes the kernel paraphrase false:
    # A=0, all probability laws feasible, T is reset to a single output.
    mass_direction = (F(1), F(0))
    assert dot((0, 0), mass_direction) == 0
    assert dot((1, 1), mass_direction) == 1
    assert dot((1, 1), (1, -1)) == 0
    # Full support is sufficient, not necessary: A records mass and first-state mass.
    # On record (1,0), state 1 is impossible, but D=ker(A)=span(0,1,-1).
    restricted_direction = (F(0), F(1), F(-1))
    assert dot((1, 1, 1), restricted_direction) == 0
    assert dot((1, 0, 0), restricted_direction) == 0
    # Feasible-support guard: binary singleton marginals (0,0) force delta_00.
    # Its marginal record kernel nevertheless contains the following forbidden direction.
    boundary_direction = (F(1), F(-1), F(-1), F(1))
    boundary_A = ((1, 1, 1, 1), (0, 0, 1, 1), (0, 1, 0, 1))
    assert all(dot(row, boundary_direction) == 0 for row in boundary_A)
    assert any(boundary_direction)

    comparisons = likelihood_checks = 0
    for cap in range(1, 5):
        for policy in range(4):
            laws = {n: endpoint_law(n, cap, policy) for n in range(1, 6)}
            for n, m in combinations(laws, 2):
                assert laws[n].keys() == laws[m].keys()
                comparisons += 1
                for terminal, pn in laws[n].items():
                    ratio = F(1)
                    for action, bit in terminal[0]:
                        qn, qm = (1 - action) ** n, (1 - action) ** m
                        kn, km = (qn, qm) if bit else (1 - qn, 1 - qm)
                        assert kn > 0 and km > 0
                        ratio *= kn / km
                    assert pn / laws[m][terminal] == ratio
                    likelihood_checks += 1
    # Boundary negative control: zero versus positive count at x=1 is exactly separable.
    assert (1 - F(1)) ** 0 == 1 and (1 - F(1)) ** 1 == 0
    # Positive error is compatible with finite inference: distinguish counts 1 and 2.
    N, cutoff = 32, 12
    error_1 = sum(F(comb(N, s), 2 ** N) for s in range(cutoff))
    error_2 = sum(F(comb(N, s)) * F(1, 4) ** s * F(3, 4) ** (N - s)
                  for s in range(cutoff, N + 1))
    assert 0 < error_1 < F(1, 10) and 0 < error_2 < F(1, 10)

    balanced_support_cases = 0
    rates = (F(0), F(1, 4), F(1, 2), F(1))
    for roots in range(2, 5):
        for k in range(1, 4):
            for action in product(rates, repeat=roots):
                q0, z = F(1), F(1)
                for a in action:
                    q0 *= (1 - a) ** k
                    z *= a
                q1 = q0 * (1 - z)
                assert (q0 > 0) == (q1 > 0) and (q0 < 1) == (q1 < 1)
                balanced_support_cases += 1

    print(json.dumps({
        'status': 'PASS',
        'frozen_author_files_verified': len(bindings['frozen_author_files']),
        'compared_modern_proofs_verified': len(bindings['compared_modern_proofs']),
        'author_controls_replay': 'byte-identical',
        'unit_price_full_tree_enumeration_cases': unit_cases,
        'weighted_full_tree_vs_bellman_cases': weighted_cases,
        'full_label_identification_cases': 8,
        'heterogeneous_first_cut_costs': root_costs,
        'exact_vanishing_margin_cases': len(margins),
        'smallest_checked_determinant_magnitude': margins[-1],
        'exact_linear_channel_cases': linear_cases,
        'proposition_6_scope_negative_controls': 3,
        'adaptive_randomized_stopped_law_comparisons': comparisons,
        'exact_terminal_likelihood_ratio_checks': likelihood_checks,
        'balanced_multiroot_common_support_cases': balanced_support_cases,
        'positive_error_separation': {'samples': N, 'no_hit_threshold': cutoff,
                                      'count_1_error': str(error_1), 'count_2_error': str(error_2),
                                      'both_errors_below': '1/10'},
        'scope': 'Finite exact controls supplement the review proofs; no infinite-policy enumeration.'
    }, indent=2))


if __name__ == '__main__':
    main()
