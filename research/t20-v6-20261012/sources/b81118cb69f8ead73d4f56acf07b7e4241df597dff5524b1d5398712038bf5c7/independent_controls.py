"""Independent exact controls: unnormalized joint counts and latent seed enumeration.
No imports from the author's scripts. These finite checks supplement proof review.
"""
from fractions import Fraction as F
from collections import Counter
from itertools import product
from random import Random
import json


def normalize(v):
    z = sum(v)
    if not z:
        raise ValueError('impossible conditioning event')
    return tuple(F(x) / z for x in v)


def bregman(p, q, power=2):
    phi = lambda v: sum(x ** power for x in v) / power
    return phi(p) - phi(q) - sum(qi ** (power - 1) * (pi - qi) for pi, qi in zip(p, q))


def risk(p, q, power=2):
    return sum(pi * bregman(tuple(F(i == j) for i in range(len(p))), q, power)
               for j, pi in enumerate(p))


def zero_boundary():
    cases = 0
    for n in (2, 3, 4):
        for pw in product((1, 2, 5), repeat=n):
            p = normalize(pw)
            for qw in product((1, 3), repeat=n):
                q = normalize(qw)
                edge = min(pi / qi for pi, qi in zip(p, q))
                assert edge <= 1
                for scale in (2, 7, 101):
                    eps = edge / scale
                    joint = tuple((pi - eps * qi, eps * qi) for pi, qi in zip(p, q))
                    assert all(x > 0 for row in joint for x in row)
                    assert tuple(sum(row) for row in joint) == p
                    assert normalize(tuple(row[1] for row in joint)) == q
                    assert sum(row[1] for row in joint) == eps
                    assert sum(abs(row[0] - pi) + abs(row[1]) for pi, row in zip(p, joint)) / 2 == eps
                    cases += 1
                # Strict epsilon bound is necessary for every joint cell positive.
                assert any(pi - edge * qi == 0 for pi, qi in zip(p, q))
    # At the boundary itself conditioning refuses, rather than inventing a posterior.
    try:
        normalize((0, 0, 0))
    except ValueError:
        pass
    else:
        raise AssertionError('impossible event accepted')
    # A fixed zero prior forbids positive posterior mass there under any conditioning.
    assert normalize((F(1, 3), F(0), F(1, 6)))[1] == 0
    return {'positive_models': cases, 'strict_boundary_zero_cell': True,
            'impossible_event_refused': True, 'excluded_hypotheses_not_resurrected': True}


def collider_countermodel():
    # 200 equiprobable causal seeds. This uses deterministic mechanisms, not the
    # author's product-of-probabilities model implementation.
    counts = Counter()
    for theta, bad, u, w in product(range(2), range(2), range(10), range(5)):
        y = theta if u < (5 if bad else 9) else 1 - theta
        v = theta if w < 4 else 1 - theta
        counts[(theta, bad, y, v, int(y != v))] += 1
    assert sum(counts.values()) == 200
    def post(**constraints):
        names = ('theta', 'bad', 'y', 'v', 'd')
        return normalize(tuple(sum(c for row, c in counts.items() if row[0] == t
                        and all(row[names.index(k)] == val for k, val in constraints.items()))
                               for t in range(2)))
    old = post(y=1)
    true = post(y=1, bad=1, d=1)
    coarse = post(bad=1, d=1)
    assert old == (F(3, 10), F(7, 10))
    assert true == (F(4, 5), F(1, 5))
    assert coarse == (F(1, 2), F(1, 2))
    assert post(y=1, bad=1) == post(bad=1)
    # Replacing the old joint evidence by only the marginal audit is actual
    # loss of conditional discrimination. It is not failure of algebraic Bayes.
    assert risk(true, coarse) - risk(true, true) == F(9, 100)
    return {'equiprobable_seeds': 200, 'old_theta1': old[1],
            'full_theta1': true[1], 'audit_only_theta1': coarse[1],
            'selected_event_quadratic_regret': F(9, 100)}


def joint_tensor_checks():
    rng = Random(90137)
    counts = Counter()
    # Each finite experiment has theta=3, retained history=2, report=3, audit=3.
    # Zeros include impossible outcomes, excluded prior states and support shrinkage.
    for experiment in range(420):
        n, nh, ny, na = 3, 2, 3, 3
        table = {(t, h, y, a): F(rng.choice((0, 0, 0, 1, 2, 5)))
                 for t, h, y, a in product(range(n), range(nh), range(ny), range(na))}
        if experiment % 5 == 0:
            for key in table:
                if key[0] == 2:
                    table[key] = 0
        if experiment % 7 == 0:
            for key in table:
                if key[2:] == (2, 2):
                    table[key] = 0
        counts['joint_tensors'] += 1
        for h in range(nh):
            by_theta = tuple(sum(table[t,h,y,a] for y,a in product(range(ny),range(na))) for t in range(n))
            if sum(by_theta) == 0:
                continue
            p = normalize(by_theta)
            for y in range(ny):
                y_theta = tuple(sum(table[t,h,y,a] for a in range(na)) for t in range(n))
                if sum(y_theta) == 0:
                    continue
                old = normalize(y_theta)
                gain = {power:F(0) for power in (2, 4)}
                info = {power:F(0) for power in (2, 4)}
                regret = {power:F(0) for power in (2, 4)}
                for a in range(na):
                    j = tuple(table[t,h,y,a] for t in range(n))
                    if sum(j) == 0:
                        counts['impossible_events_refused'] += 1
                        continue
                    full = normalize(j)
                    a_theta = tuple(sum(table[t,h,v,a] for v in range(ny)) for t in range(n))
                    coarse = normalize(a_theta)
                    coarse_support = [t for t in range(n) if a_theta[t] > 0]
                    p_support = [t for t in range(n) if by_theta[t] > 0]
                    # Criterion independently checked with cross products, no normalization cancellation.
                    flat_after_a = all(j[t] * a_theta[u] == j[u] * a_theta[t]
                                       for t,u in product(coarse_support, repeat=2))
                    bare_flat = all(j[t] * by_theta[u] == j[u] * by_theta[t]
                                    for t,u in product(p_support, repeat=2))
                    assert (full == coarse) == flat_after_a
                    assert (full == p) == bare_flat
                    # Directly observed history, then audit, reproduces the joint.
                    seq = tuple(j[t] / y_theta[t] if y_theta[t] else F(0) for t in range(n))
                    assert normalize(tuple(old[t] * seq[t] for t in range(n))) == full
                    # Audit-first factorization has the same result including zeros.
                    replacement = tuple(j[t] / a_theta[t] if a_theta[t] else F(0) for t in range(n))
                    assert normalize(tuple(coarse[t] * replacement[t] for t in range(n))) == full
                    assert all(full[t] == 0 for t in range(n) if p[t] == 0)
                    # Well-defined inverse-factor version: only the prior support is relevant.
                    if all(y_theta[t] for t in p_support):
                        ly = tuple(y_theta[t]/by_theta[t] if by_theta[t] else F(1) for t in range(n))
                        ma = tuple(a_theta[t]/by_theta[t] if by_theta[t] else F(0) for t in range(n))
                        assert normalize(tuple(old[t]/ly[t]*ma[t] for t in range(n))) == coarse
                        divided = normalize(tuple(old[t]/ly[t]*seq[t] for t in range(n)))
                        ds = [t for t in range(n) if divided[t] > 0]
                        assert (divided == full) == (len({ly[t] for t in ds}) == 1)
                        counts['inverse_supported_events'] += 1
                    for power in (2,4):
                        w = sum(j) / sum(y_theta)
                        gain[power] += w * (risk(full, old, power) - risk(full, coarse, power))
                        info[power] += w * bregman(full, old, power)
                        regret[power] += w * bregman(full, coarse, power)
                        assert risk(full, coarse, power) - risk(full, full, power) == bregman(full, coarse, power)
                        assert bregman(full, coarse, power) >= 0
                        assert (bregman(full, coarse, power) == 0) == (full == coarse)
                    counts['positive_observation_events'] += 1
                    counts['audit_deletion_exact_events'] += int(full == coarse)
                    counts['bare_deletion_exact_events'] += int(full == p)
                    counts['prior_support_restricted_events'] += int(len(p_support) < n)
                for power in (2,4):
                    assert gain[power] == info[power] - regret[power]
                    counts['conditional_score_identities'] += 1
    # A zero factor erases prior support and cannot be inverted from posterior alone.
    p1, p2, L = (F(1,3),F(2,3)), (F(2,3),F(1,3)), (1,0)
    assert normalize(tuple(pi*li for pi,li in zip(p1,L))) == normalize(tuple(pi*li for pi,li in zip(p2,L)))
    assert p1 != p2
    counts['zero_factor_noninvertibility_witness'] = 1
    return dict(counts)


if __name__ == '__main__':
    print(json.dumps({'status':'PASS', 'arithmetic':'exact Fraction',
                      'zero_audit_boundary':zero_boundary(),
                      'independent_causal_model':collider_countermodel(),
                      'joint_tensor_controls':joint_tensor_checks(),
                      'scope':'Finite controls supplement written general proofs; no empirical or source-warrant validation.'},
                     indent=2, default=str))
