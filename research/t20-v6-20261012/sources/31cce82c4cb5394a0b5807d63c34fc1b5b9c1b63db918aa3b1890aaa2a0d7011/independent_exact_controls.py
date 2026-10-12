"""Independently authored rational spot checks for the Pro-to-Dot delta.

Scope: finite controls for the explicit audit/Euler/rational formulas.
Not a formal proof, a Lean replay, or a test of any existing T20 integrator.
"""
from fractions import Fraction as F
from itertools import product


def normalise(values):
    values = list(values)
    assert all(v >= 0 for v in values) and sum(values) > 0
    return tuple(v / sum(values) for v in values)


def audit(w, r):
    assert all(v > 0 for v in r)
    return normalise(a * b for a, b in zip(w, r))


def euler(w, fit, h):
    average = sum(a * c for a, c in zip(w, fit))
    return tuple(a + h * a * (c - average) for a, c in zip(w, fit))


def reciprocal(w, potential, h):
    baseline = min(potential)
    factors = [1 / (1 + h * (v - baseline)) for v in potential]
    return audit(w, factors)


def energy(w, potential):
    return sum(x * v for x, v in zip(w, potential))


def check():
    w = (F(1, 2), F(1, 2))
    r = (F(1), F(2))
    fit = (F(0), F(1))
    h = F(1, 2)
    after = audit(euler(w, fit, h), r)
    before = euler(audit(w, r), fit, h)
    assert after == (F(3, 13), F(10, 13)), after
    assert before == (F(2, 9), F(7, 9)), before
    assert abs(after[0] - before[0]) == F(1, 117)
    assert abs(after[1] - before[1]) == F(1, 117)
    print('Exact Euler/audit defect: 1/117 — PASS')

    tests = 0
    for ws in product((1, 2, 3), repeat=3):
        ww = normalise(map(F, ws))
        for ps in product((0, 1, 4), repeat=3):
            pp = tuple(map(F, ps))
            for step in (F(0), F(1, 10), F(3, 2)):
                out = reciprocal(ww, pp, step)
                assert all(x > 0 for x in out)
                assert sum(out) == 1
                assert energy(out, pp) <= energy(ww, pp)
                assert reciprocal(ww, tuple(x + 7 for x in pp), step) == out
                for rr in ((1, 1, 1), (1, 2, 3), (4, 1, 2)):
                    factors = tuple(F(x) for x in rr)
                    assert audit(out, factors) == reciprocal(audit(ww, factors), pp, step)
                    tests += 1
    print('Reciprocal positivity, descent, shift, covariance:', tests, 'exact checks — PASS')

    # Sharp posterior TV control for likelihood ratio range [1,4].
    prior = (F(2, 3), F(1, 3))
    posterior = audit(prior, (F(1), F(4)))
    assert posterior == (F(1, 3), F(2, 3))
    tv = sum(abs(x - y) for x, y in zip(prior, posterior)) / 2
    assert tv == F(1, 3)
    print('Sharp relative-likelihood TV example: 1/3 — PASS')
    print('All new exact spot checks passed.')


if __name__ == '__main__':
    check()
