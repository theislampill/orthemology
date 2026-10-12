#!/usr/bin/env python3
"""Exact rational certificates for two finite transport countermodels.

This checks the displayed upper and matching moment-dual lower certificates;
it does not claim independent proof of the inherited general theorems.
No packages, network, historical data, or floating-point arithmetic are used.
"""
from fractions import Fraction as F
import json


def dot(a, b):
    return sum((F(x) * F(y) for x, y in zip(a, b)), F(0))


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    pivot_row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for i in range(len(a)):
            if i != pivot_row:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def certificate(basis, target, coefficients, left, right):
    """A retained linear approximant and equal-moment laws certify equality."""
    assert len(left) == len(right) == len(target)
    for law in (left, right):
        assert sum(law) == 1 and all(p >= 0 for p in law)
    assert all(dot(left, row) == dot(right, row) for row in basis)
    approximation = [
        sum((F(c) * F(row[i]) for c, row in zip(coefficients, basis)), F(0))
        for i in range(len(target))
    ]
    upper = max(abs(F(f) - g) for f, g in zip(target, approximation))
    lower = abs(dot(left, target) - dot(right, target)) / 2
    assert upper == lower
    return str(upper)


def main():
    # Model A: raw r is injective; its retained first moment is insufficient.
    states_a = (-1, 0, 1)
    ones_a = (1, 1, 1)
    f_a = (1, 0, 1)
    v_a = [ones_a, states_a]
    p_a = (F(1, 2), F(0), F(1, 2))
    p_prime_a = (F(0), F(1), F(0))
    assert len(set(states_a)) == 3
    assert tuple(x * x for x in states_a) == f_a
    assert rank(v_a) == 2 and rank(v_a + [f_a]) == 3
    defect_a = certificate(v_a, f_a, (F(1, 2), 0), p_a, p_prime_a)
    assert defect_a == "1/2"

    # Model B: exact authors differ, but wording is constant on the same fibre.
    q_b = (("author_alpha", "wording_W"), ("author_beta", "wording_W"))
    r_b = (0, 0)
    ones_b = (1, 1)
    authorship_claim = (1, 0)
    wording_claim = (1, 1)
    v_b = [ones_b]
    p_b, p_prime_b = (F(1), F(0)), (F(0), F(1))
    assert r_b[0] == r_b[1] and q_b[0] != q_b[1]
    assert q_b[0][1] == q_b[1][1]
    author_defect = certificate(v_b, authorship_claim, (F(1, 2),), p_b, p_prime_b)
    wording_defect = certificate(v_b, wording_claim, (1,), p_b, p_prime_b)
    assert author_defect == "1/2" and wording_defect == "0"

    # One action, one certain observation, identity kernel: K f = f.
    identity = ((1, 0), (0, 1))
    for f in (ones_b, authorship_claim, wording_claim):
        assert tuple(dot(row, f) for row in identity) == f
    c_unrelated = [ones_b, wording_claim]
    c_author = [ones_b, authorship_claim]
    augmentation_unrelated = rank(v_b + c_unrelated) - rank(v_b)
    augmentation_author = rank(v_b + c_author) - rank(v_b)
    assert augmentation_unrelated == 0 and augmentation_author == 1

    # A separate stipulated prior, with no extra information from constant r.
    prior = (F(99, 100), F(1, 100))
    posterior_author_probability = dot(prior, authorship_claim)
    bayes_01_risk = min(prior)
    randomized_minimax_01_risk = max(F(1, 2), 1 - F(1, 2))
    deterministic_minimax_01_risk = 1
    assert posterior_author_probability == F(99, 100)
    assert bayes_01_risk == F(1, 100)
    assert randomized_minimax_01_risk == F(1, 2)

    result = {
        "status": "all exact assertions passed",
        "model_A": {
            "raw_f_recoverable": True,
            "moment_defect": defect_a,
            "equal_retained_first_moment": str(dot(p_a, states_a)),
            "target_expectations": [str(dot(p_a, f_a)), str(dot(p_prime_a, f_a))],
        },
        "model_B": {
            "combined_target_raw_recoverable": False,
            "authorship_defect": author_defect,
            "wording_defect": wording_defect,
            "identity_dynamics_augmentation_unrelated_contract": augmentation_unrelated,
            "identity_dynamics_augmentation_author_contract": augmentation_author,
            "stipulated_posterior_author_probability": str(posterior_author_probability),
            "bayes_01_risk": str(bayes_01_risk),
            "randomized_minimax_01_risk": str(randomized_minimax_01_risk),
            "deterministic_minimax_01_risk": deterministic_minimax_01_risk,
        },
        "scope": "Two synthetic finite models; no historical or philosophical warrant claim.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
