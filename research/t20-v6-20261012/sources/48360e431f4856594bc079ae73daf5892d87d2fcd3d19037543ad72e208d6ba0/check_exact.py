#!/usr/bin/env python3
"""Exact finite diagnostics; these checks do not replace the universal proof."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from random import Random
import hashlib
import json
import time
from countermodel import (FIRST_TEN, SchurMoment, WITNESS, dot, exponent_at,
                          monomial_index, midpoint_index, multiply)

ROOT = Path(__file__).resolve().parent
checks = []


def require(name, truth):
    if not truth:
        raise AssertionError(name)
    checks.append(name)


def solve(A, b):
    """Independent ordinary Gaussian elimination; no inverse-update formula."""
    rows = [list(row) + [rhs] for row, rhs in zip(A, b)]
    n = len(A)
    for k in range(n):
        pivot = next(i for i in range(k, n) if rows[i][k])
        rows[k], rows[pivot] = rows[pivot], rows[k]
        v = rows[k][k]
        rows[k] = [x / v for x in rows[k]]
        for i in range(n):
            if i != k:
                v = rows[i][k]
                rows[i] = [x - v * y for x, y in zip(rows[i], rows[k])]
    return [row[-1] for row in rows]


def ldl(A):
    """Independent exact LDL^T factorization for the positivity diagnostics."""
    n = len(A)
    L = [[Q(int(i == j)) for j in range(n)] for i in range(n)]
    D = []
    for k in range(n):
        d = A[k][k] - sum((L[k][j] ** 2 * D[j] for j in range(k)), Q(0))
        D.append(d)
        for i in range(k + 1, n):
            L[i][k] = (A[i][k] - sum((L[i][j] * L[k][j] * D[j]
                                     for j in range(k)), Q(0))) / d
    return L, D


def independent_prefix(N):
    """Separate shell enumeration, direct entries and Gaussian solves."""
    exponents = [(0, 0), (2, 1), (1, 2), (1, 1), (1, 0),
                 (0, 1), (2, 0), (0, 2), (3, 0), (0, 3)]
    degree = 4
    while len(exponents) < N:
        exponents += [(degree - b, b) for b in range(degree + 1)]
        degree += 1
    lookup = {p: i for i, p in enumerate(exponents)}
    values = [Q(1), Q(1), Q(1), Q(4)]

    def entry(i, k):
        a, b = (exponents[i][t] + exponents[k][t] for t in (0, 1))
        if a % 2 or b % 2:
            return Q(0)
        return values[lookup[(a // 2, b // 2)]]

    for k in range(4, N):
        A = [[entry(i, h) for h in range(k)] for i in range(k)]
        v = [entry(i, k) for i in range(k)]
        solution = solve(A, v)
        values.append(Q(1) + sum((a * b for a, b in zip(v, solution)), Q(0)))
    return values


def main():
    start = time.monotonic()
    for n in range(1, 20001):
        require(f"inverse_index_{n}", monomial_index(*exponent_at(n)) == n)
    for d in range(51):
        for b in range(d + 1):
            p = (d - b, b)
            require(f"index_inverse_{p}", exponent_at(monomial_index(*p)) == p)
    small_pairs = []
    for (i, p), (k, q) in combinations(enumerate(FIRST_TEN, 1), 2):
        h = midpoint_index(p, q)
        if h is not None:
            small_pairs.append({"i": i, "k": k, "midpoint_index": h})
            require(f"exceptional_pair_{i}_{k}", h < k)
    require("exactly_nine_exceptional_pairs", len(small_pairs) == 9)
    # Degree at most 25 covers 351 monomials, including the exceptional order.
    P = [exponent_at(n) for n in range(1, 352)]
    compatible = 0
    for (i, p), (k, q) in combinations(enumerate(P, 1), 2):
        h = midpoint_index(p, q)
        if h is not None:
            compatible += 1
            require(f"midpoint_prefix_{i}_{k}", h < k)
    N = 25
    independent = independent_prefix(N)
    model = SchurMoment()
    prefix_rows = []
    for n in range(1, N + 1):
        model.extend(n)
        A = model.gram(n)
        L, D = ldl(A)
        expected = [Q(4) if i == 3 else Q(1) for i in range(n)]
        require(f"LDL_pivots_{n}", D == expected)
        require(f"symmetric_{n}", all(A[i][j] == A[j][i]
                                      for i in range(n) for j in range(n)))
        require(f"reconstruct_LDL_{n}", all(
            A[i][j] == sum((L[i][k] * D[k] * L[j][k] for k in range(n)), Q(0))
            for i in range(n) for j in range(n)))
        determinant = Q(1)
        for d in D:
            determinant *= d
        require(f"determinant_{n}", determinant == (1 if n < 4 else 4))
        require(f"independent_recurrence_{n}", model.j[n - 1] == independent[n - 1])
        require(f"dyadic_{n}", model.j[n - 1].denominator & (model.j[n - 1].denominator - 1) == 0)
        if n >= 4:
            require(f"inverse_identity_{n}", all(
                sum((A[i][k] * model.B[k][j] for k in range(n)), Q(0)) == int(i == j)
                for i in range(n) for j in range(n)))
        prefix_rows.append({"index": n, "exponent": exponent_at(n),
                            "value": str(model.j[n - 1]),
                            "numerator_bits": model.j[n - 1].numerator.bit_length(),
                            "denominator_bits": model.j[n - 1].denominator.bit_length()})
    require("normalized", model.apply({(0, 0): 1}) == 1)
    require("witness_value", model.apply(WITNESS) == -1)
    require("sequence_need_not_be_monotone", model.j[11] == Q(5, 4) < model.j[10])
    rng = Random(10102026)
    A = model.gram(N)
    for trial in range(80):
        c = [Q(rng.randrange(-5, 6), rng.randrange(1, 8)) for _ in range(N)]
        p = {exponent_at(i + 1): a for i, a in enumerate(c) if a}
        value = model.apply(multiply(p, p))
        quadratic = sum((c[i] * A[i][j] * c[j]
                         for i in range(N) for j in range(N)), Q(0))
        require(f"polynomial_square_gram_identity_{trial}", value == quadratic)
        require(f"nonzero_polynomial_square_positive_{trial}", value > 0)
    # Negative controls demonstrate why changing or truncating the recurrence is unsafe.
    base = SchurMoment()
    v = [Q(0), Q(0), Q(4), Q(0)]
    w = [dot(row, v) for row in base.B]
    bad = [row + [a] for row, a in zip(base.gram(4), v)]
    bad.append(v + [dot(v, w) - 1])
    c = [-a for a in w] + [Q(1)]
    bad_value = sum((c[i] * bad[i][j] * c[j] for i in range(5) for j in range(5)), Q(0))
    require("negative_control_wrong_schur_sign", bad_value == -1)
    base.extend(10)
    # Zero-tail moment convention after j_10: Lambda((y^4-1)^2)=1-2*j_8.
    zero_tail_value = 1 - 2 * base.j[7]
    require("negative_control_zero_tail_not_positive", zero_tail_value == -163029)
    require("negative_control_wrong_witness_value", model.apply(WITNESS) != 0)
    require("negative_control_false_monotonicity", not all(
        a <= b for a, b in zip(model.j, model.j[1:])))
    # Scalar lower bound checks are only diagnostics; the global proof is in PROOF.md
    # and is separately kernel-checked in lean-support.
    for a in range(-12, 13):
        for b in range(-12, 13):
            x, y = Q(a, 4), Q(b, 4)
            f = 1 + x**4 * y**2 + x**2 * y**4 - x**2 * y**2
            require(f"scalar_grid_{a}_{b}", f >= Q(3, 4))
    (ROOT / "PREFIX_25.json").write_text(json.dumps(prefix_rows, indent=2) + "\n")
    receipt = {
        "status": "PASS_EXACT_FINITE_DIAGNOSTICS",
        "universal_claim_basis": "PROOF.md induction; finite tests are not its proof",
        "checks_passed": len(checks), "prefix_length": N,
        "independent_recurrence": "direct Gaussian solves and separate shell enumeration",
        "positivity_verification": "independent exact LDL factorization, reconstruction and pivots",
        "bounded_midpoint_pairs_checked": compatible,
        "exceptional_pairs": small_pairs, "Lambda_F": "-1",
        "negative_controls": {"wrong_schur_sign": str(bad_value),
                              "zero_tail_square": str(zero_tail_value),
                              "false_monotonicity_rejected": True},
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ["countermodel.py", "check_exact.py"]},
        "prefix_sha256": hashlib.sha256((ROOT / "PREFIX_25.json").read_bytes()).hexdigest(),
    }
    (ROOT / "EXACT_CHECK_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
