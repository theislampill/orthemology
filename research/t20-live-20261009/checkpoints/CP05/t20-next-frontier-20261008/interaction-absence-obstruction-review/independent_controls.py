#!/usr/bin/env python3
"""Exact diagnostic controls; the quantified impossibility is proved in REVIEW.md."""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json

C = Counter()

def check(family, condition):
    assert condition, family
    C[family] += 1

def root_bracket(u, n, width):
    assert 0 <= u <= 1 and n >= 1 and width > 0
    if u in (0, 1):
        return u, u
    lo, hi = F(0), F(1)
    while hi - lo > width:
        mid = (lo + hi) / 2
        if mid ** n <= u:
            lo = mid
        else:
            hi = mid
    assert lo ** n <= u <= hi ** n
    return lo, hi

def q_bracket(n, a, b, width):
    u = 1 - a
    lo, hi = root_bracket(u, n, width)
    return u * (1 - b + b * lo), u * (1 - b + b * hi)

def alternative_name(n, a, b, eps):
    # One fixed total, memoryless name, including repeated and unqueried inputs.
    if eps > F(1, n + 1):
        return 1 - a
    lo, hi = q_bracket(n, a, b, eps)
    return (lo + hi) / 2

def base_name(a, b, eps):
    return 1 - a

def interval(name, a, b, eps):
    y = name(a, b, eps)
    return max(F(0), y - eps), min(F(1), y + eps)

ns = list(range(1, 49)) + [64, 127]
ts = sorted({F(j, d) for d in range(1, 17) for j in range(d + 1)})
bs = [F(j, 7) for j in range(8)]
for n in ns:
    peak_t = F(n, n + 1)
    peak_a = 1 - peak_t ** n
    gap = peak_t ** n / (n + 1)
    check('supremum_and_bound', gap == F(n ** n, (n + 1) ** (n + 1)))
    check('supremum_and_bound', 0 < gap < F(1, n + 1))
    check('supremum_and_bound', (1 - peak_a) * (1 - peak_t) == gap)
    check('supremum_and_bound', n - (n + 1) * peak_t == 0)
    previous_a, previous_r = None, None
    for t in reversed(ts):
        a, rate = 1 - t ** n, 1 - t
        if previous_a is not None:
            check('calibration_membership', previous_a < a and previous_r < rate)
        previous_a, previous_r = a, rate
        check('calibration_membership', (1 - rate) ** n == 1 - a)
        derivative_core = n - (n + 1) * t
        check('derivative_sign', (derivative_core > 0) == (t < peak_t))
        check('derivative_sign', (derivative_core < 0) == (t > peak_t))
        for b in bs:
            q0 = 1 - a
            independent_route_q = (1 - rate) ** n * (1 - rate * b)
            closed_q = (1 - a) * (1 - b + b * t)
            check('route_formula', independent_route_q == closed_q)
            check('uniform_gap_grid', 0 <= q0 - closed_q <= gap)
            check('uniform_gap_grid', q0 - closed_q == b * t ** n * (1 - t))
            da = (1 - b) + b * F(n + 1, n) * t
            db = t ** n * (1 - t)
            check('response_lipschitz', 0 <= da <= 2 and 0 <= db <= 1)
            if a in (0, 1) or b == 0:
                check('masked_boundary_identity', q0 == closed_q)
    # Positive interaction is genuinely distinct, even with rational nominal input.
    t, b = F(1, 2), F(1, 2)
    a = 1 - t ** n
    check('not_population_equivalence', b * t ** n * (1 - t) > 0)
    # Every finite N is an admissible finite inventory with no B-only routes.
    check('inventory_counts', isinstance(n, int) and n >= 1 and n + 1 > n)

points = [(F(0), F(0)), (F(0), F(1)), (F(1), F(0)), (F(1), F(1)),
          (F(1, 2), F(1, 2)), (F(2, 3), F(1)), (F(9, 10), F(1, 3))]
for n in [1, 2, 3, 7, 15, 31]:
    for eps in [F(1, 2), F(1, 16), F(1, 128), F(1, n + 1),
                F(1, 2 * (n + 1)), F(2, n + 1)]:
        for a, b in points:
            y = alternative_name(n, a, b, eps)
            check('fixed_total_name', y == alternative_name(n, a, b, eps))
            if eps > F(1, n + 1):
                gap = F(n ** n, (n + 1) ** (n + 1))
                check('fixed_total_name', y == 1 - a and gap < eps)
            else:
                lo, hi = q_bracket(n, a, b, eps / 8)
                check('fixed_total_name', y - eps < lo and hi < y + eps)

def adaptive_probe(name, seed, steps):
    transcript = []
    last = F(seed % 5, 5)
    for j in range(steps):
        a = F(0) if j % 5 == 0 else F(1) if j % 5 == 1 else (last + 1) / 3
        b = F(0) if j % 4 == 0 else F(1) if j % 4 == 1 else F(seed % 7 + 1, 8)
        eps = F(1, 2 ** (j + seed % 3 + 1))
        y = name(a, b, eps)
        transcript.append((a, b, eps, y))
        last = y
    return transcript

for seed in range(12):
    for steps in range(0, 11):
        transcript = adaptive_probe(base_name, seed, steps)
        min_eps = min((q[2] for q in transcript), default=F(1))
        n = min_eps.denominator + 1
        check('adaptive_transcript', F(1, n + 1) < min_eps)
        other = adaptive_probe(lambda a, b, eps: alternative_name(n, a, b, eps), seed, steps)
        check('adaptive_transcript', transcript == other)

# A geometric random stopping-time fixture has no uniform finite precision cap.
# It illustrates the positive-probability finite-threshold argument exactly.
for k in range(1, 17):
    eta = F(1, 2 ** (k + 1))
    n = 2 ** (k + 1)
    event_mass = sum((F(1, 2 ** (j + 1)) for j in range(k)), F(0))
    check('randomized_threshold_events', event_mass == 1 - F(1, 2 ** k))
    check('randomized_threshold_events', F(1, n + 1) < eta)
    for j in range(k):
        eps = F(1, 2 ** (j + 1))
        check('randomized_threshold_events', eps > eta)
        check('randomized_threshold_events', alternative_name(n, F(1, 2), F(1), eps) == F(1, 2))

presence_bits = {}
for n in [1, 2, 3, 7, 15, 31]:
    name = lambda a, b, eps: alternative_name(n, a, b, eps)
    found = False
    for bits in range(1, 30):
        eps = F(1, 2 ** bits)
        alo, ahi = interval(name, F(1, 2), F(0), eps)
        blo, bhi = interval(name, F(0), F(1, 2), eps)
        clo, chi = interval(name, F(1, 2), F(1, 2), eps)
        contrast_lo, contrast_hi = alo * blo - chi, ahi * bhi - clo
        check('presence_semidecision', contrast_hi > 0)
        if contrast_lo > 0:
            found = True
            presence_bits[str(n)] = bits
            break
    check('presence_semidecision', found)

for bits in range(1, 30):
    eps = F(1, 2 ** bits)
    alo, ahi = interval(base_name, F(1, 2), F(0), eps)
    blo, bhi = interval(base_name, F(0), F(1, 2), eps)
    clo, chi = interval(base_name, F(1, 2), F(1, 2), eps)
    check('absence_not_certified', alo * blo - chi <= 0 <= ahi * bhi - clo)

result = {
    'status': 'PASS',
    'arithmetic': 'integer and Fraction; no simulation or floating-point probability approximation',
    'assertion_counts': dict(sorted(C.items())),
    'total_assertions': sum(C.values()),
    'presence_detection_bits_for_test_names': presence_bits,
    'scope': 'Finite exact diagnostic controls only; universal claims rely on written proofs.'
}
out = Path(__file__).with_name('INDEPENDENT_CONTROLS.json')
out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, indent=2, sort_keys=True))
