#!/usr/bin/env python3
"""Independent bounded determinant replay; universal proof lives in REVIEW.md.

Unlike the author's inverse updates or Gaussian-solve replay, construct diagonals
by multilinearity of the determinant and compute it by fraction-free elimination.
The author module is imported only after this reference sequence is built.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse
import hashlib
import importlib.util
import json
import time

HERE = Path(__file__).resolve().parent
counts = Counter()

def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] += 1


def enumerated(degree):
    # Set enumeration with explicit exceptional permutation, no triangular formula.
    low = [(0, 0), (2, 1), (1, 2), (1, 1), (1, 0),
           (0, 1), (2, 0), (0, 2), (3, 0), (0, 3)]
    shell = sorted(((a, b) for a in range(degree + 1)
                    for b in range(degree + 1) if 4 <= a + b <= degree),
                   key=lambda p: (sum(p), p[1]))
    return low + shell


def determinant(matrix):
    """Bareiss elimination, with rational exact arithmetic and row pivoting."""
    if not matrix:
        return Q(1)
    a = [list(row) for row in matrix]
    previous = Q(1)
    sign = Q(1)
    for k in range(len(a) - 1):
        pivots = [r for r in range(k, len(a)) if a[r][k]]
        if not pivots:
            return Q(0)
        r = pivots[0]
        if r != k:
            a[k], a[r] = a[r], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                a[i][j] = (pivot * a[i][j] - a[i][k] * a[k][j]) / previous
        for i in range(k + 1, len(a)):
            a[i][k] = Q(0)
        previous = pivot
    return sign * a[-1][-1]


def reference(N):
    E = enumerated(N)
    lookup = {p: i for i, p in enumerate(E)}
    moments = [Q(1), Q(1), Q(1), Q(4)]

    def entry(i, j):
        a, b = (E[i][t] + E[j][t] for t in (0, 1))
        if a % 2 or b % 2:
            return Q(0)
        h = lookup[a // 2, b // 2]
        check('moment_entry_available', h < len(moments))
        if i != j:
            check('offdiagonal_uses_earlier_index', h < max(i, j))
        else:
            check('diagonal_uses_own_index', h == i)
        return moments[h]

    for n in range(5, N + 1):
        # Temporarily set the new diagonal to zero. Its determinant is affine
        # in that diagonal, with coefficient det(previous leading block)=4.
        moments.append(Q(0))
        A = [[entry(i, j) for j in range(n)] for i in range(n)]
        coefficient = determinant([row[:-1] for row in A[:-1]])
        check('previous_determinant_four', coefficient == 4)
        d0 = determinant(A)
        moments[-1] = (4 - d0) / coefficient
        A[-1][-1] = moments[-1]
        check('constructed_determinant_four', determinant(A) == 4)
    return E[:N], moments


def polynomial_product(p, q):
    out = {}
    for (a, b), c in p.items():
        for (d, e), f in q.items():
            out[a + d, b + e] = out.get((a + d, b + e), Q(0)) + c * f
    return {k: v for k, v in out.items() if v}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=Path, default=HERE / 'frozen-target')
    args = parser.parse_args()
    target = args.target.resolve()
    N = 25
    E, ref = reference(N)
    spec = importlib.util.spec_from_file_location('reviewed_countermodel', target / 'countermodel.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    model = module.SchurMoment()
    saved_prefixes = []
    for n in range(1, N + 1):
        model.extend(n)
        check('reference_diagonal_matches', model.j[n - 1] == ref[n - 1])
        check('prefix_stability', all(model.j[:len(v)] == v for v in saved_prefixes))
        saved_prefixes.append(list(model.j))
        check('dyadic_moment', model.j[n - 1].denominator.bit_count() == 1)
        A = model.gram(n)
        check('leading_minor_positive', determinant(A) == (1 if n < 4 else 4))
        check('gram_symmetry', all(A[i][j] == A[j][i] for i in range(n) for j in range(n)))
        if n >= 4:
            check('dyadic_inverse', all(x.denominator.bit_count() == 1 for row in model.B for x in row))
            check('right_inverse_identity', all(sum(A[i][k] * model.B[k][j] for k in range(n)) == Q(i == j)
                    for i in range(n) for j in range(n)))
            check('left_inverse_identity', all(sum(model.B[i][k] * A[k][j] for k in range(n)) == Q(i == j)
                    for i in range(n) for j in range(n)))
    check('seed_gram_exact', model.gram(4) == [[Q(4 if i == 3 else 1) if i == j else Q(0)
                                             for j in range(4)] for i in range(4)])
    check('first_twelve_values', ref[:12] == list(map(Q, [1,1,1,4,17,17,290,81515,81798,6644043123,479723268580926])) + [Q(5,4)])
    broad = enumerated(100)
    for n, e in enumerate(broad, 1):
        check('direct_enumeration_matches_index', module.monomial_index(*e) == n)
        check('direct_enumeration_matches_inverse', module.exponent_at(n) == e)
    # Integer-only indexing is checked at extreme indices; this is still finite.
    for power in range(1, 101):
        for shift in (-1, 0, 1):
            n = 10 ** power + shift
            check('large_index_roundtrip', module.monomial_index(*module.exponent_at(n)) == n)
    bounded = enumerated(30)
    lookup = {e: i for i, e in enumerate(bounded, 1)}
    exceptional = []
    for (i, p), (j, q) in combinations(enumerate(bounded, 1), 2):
        sums = tuple(a + b for a, b in zip(p, q))
        if all(s % 2 == 0 for s in sums):
            h = lookup[tuple(s // 2 for s in sums)]
            check('midpoint_precedence', h < j)
            if i <= 10 and j <= 10:
                exceptional.append([i, j, h])
    check('exceptional_pairs_exact', exceptional == [[1,7,5],[1,8,6],[2,6,4],[2,10,3],[3,5,4],[3,9,2],[5,9,7],[6,10,8],[7,8,4]])
    # Independently multiply and evaluate sparse polynomials using the reference
    # sequence, never the author's polynomial multiplication helper.
    ref_lookup = {e: i for i, e in enumerate(E)}
    def evaluate(poly, seq=ref, zero_tail=False):
        total = Q(0)
        for (a, b), c in poly.items():
            if a % 2 or b % 2:
                continue
            h = ref_lookup[a // 2, b // 2]
            if zero_tail and h >= len(seq):
                continue
            total += c * seq[h]
        return total
    for shift in range(50):
        p = {e: Q(((i + 2) * (shift + 1)) % 11 - 5, (i + shift) % 5 + 1)
             for i, e in enumerate(E) if (i + shift) % 3}
        p = {e: c for e, c in p.items() if c}
        squared = polynomial_product(p, p)
        value = evaluate(squared)
        check('independent_square_positive', value > 0)
        check('independent_square_matches_api', model.apply(squared) == value)
    witness = {(0,0):Q(1),(4,2):Q(1),(2,4):Q(1),(2,2):Q(-1)}
    check('normalization', model.moment(0,0) == 1)
    check('independent_witness_negative', evaluate(witness) == -1 == model.apply(witness))
    for a in range(15):
        for b in range(15):
            if a % 2 or b % 2:
                check('odd_moments_zero', model.moment(a, b) == 0)
    # Controls for essential proof obligations.
    altered = E[:10]
    altered[4], altered[9] = altered[9], altered[4]
    bad_lookup = {e: i for i, e in enumerate(altered, 1)}
    bad_order_midpoint = bad_lookup[(1,0)]
    check('negative_control_order_detected', bad_order_midpoint == 10 > max(bad_lookup[(0,0)], bad_lookup[(2,0)]))
    test_square = polynomial_product({(1,0):Q(1),(1,2):Q(-4)}, {(1,0):Q(1),(1,2):Q(-4)})
    zero_schur = ref.copy(); zero_schur[4] = Q(16)
    negative_schur = ref.copy(); negative_schur[4] = Q(15)
    check('negative_control_zero_schur', evaluate(test_square, zero_schur) == 0)
    check('negative_control_negative_schur', evaluate(test_square, negative_schur) == -1)
    check('negative_control_monotonicity', ref[11] == Q(5,4) < ref[10])
    zero_tail_square = polynomial_product({(0,4):Q(1),(0,0):Q(-1)}, {(0,4):Q(1),(0,0):Q(-1)})
    check('negative_control_zero_tail', evaluate(zero_tail_square, ref[:10], True) == -163029)
    # A one-entry perturbation is rejected by determinant completion.
    perturbed = model.gram(12)
    perturbed[-1][-1] += Q(1,4)
    check('negative_control_diagonal_perturbation', determinant(perturbed) == 5 and determinant(perturbed) != 4)
    receipt = {
        'status':'PASS_INDEPENDENT_BOUNDED_DETERMINANT_REPLAY',
        'proof_limit':'Finite checks do not establish universal existence or positivity; REVIEW.md supplies independent mathematical review.',
        'method':'Direct determinant-affine diagonal construction with Bareiss elimination; independent shell enumeration and polynomial multiplication.',
        'prefix_length':N, 'checks':sum(counts.values()), 'groups':dict(counts),
        'midpoint_degree_bound':30,'index_degree_bound':100,'extreme_indices_up_to':'10^100+1',
        'first_twelve':list(map(str,ref[:12])),
        'Lambda_F':str(evaluate(witness)),
        'negative_controls':{'bad_exceptional_order':'future midpoint index 10 from endpoints 1,7',
          'zero_Schur_square':'0','negative_Schur_square':'-1','zero_tail_square':'-163029',
          'false_monotonicity':'479723268580926 > 5/4','diagonal_perturbation_det':'5 != 4'},
        'target_sha256':{name:hashlib.sha256((target/name).read_bytes()).hexdigest() for name in ('PROOF.md','countermodel.py','check_exact.py')},
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds':round(time.monotonic()-started,3)
    }
    print(json.dumps(receipt,indent=2))
    (HERE/'INDEPENDENT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__ == '__main__':
    main()
