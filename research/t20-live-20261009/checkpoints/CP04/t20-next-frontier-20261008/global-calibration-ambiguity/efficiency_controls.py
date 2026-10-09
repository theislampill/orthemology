#!/usr/bin/env python3
"""Exact rational controls for the separately scoped efficiency appendix."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNTS = Counter()


def check(value, name):
    assert value, name
    COUNTS[name] += 1


def clipped(k, u, eta):
    x = 1 - (u ** (k + 1) + u ** k) / 2
    d = u ** k * (1 - u) / 2
    r0, r1 = x + min(d, eta), x - min(d, eta)
    return x, d, r0, r1, (1 - r0) ** k, (1 - r1) ** (k + 1)


def adaptive(k, eta, which, depth):
    law = {(): F(1)}
    for _ in range(depth):
        nxt = {}
        for hist, mass in law.items():
            u = F(1 + (sum((i + 1) * (bit + 1) for i, bit in enumerate(hist)) % 4), 5)
            q = clipped(k, u, eta)[4 + which]
            nxt[hist + (1,)] = mass * q
            nxt[hist + (0,)] = mass * (1 - q)
        law = nxt
    return law


for k in range(1, 33):
    b = F(k, k + 1)
    eta_star = b ** k / (2 * (k + 1))
    grid = sorted(set([F(i, 16) for i in range(17)] + [b]))
    for eta_ratio in [F(0), F(1, 10), F(1, 2), F(9, 10), F(1), F(11, 10)]:
        eta = eta_ratio * eta_star
        previous = None
        for u in grid:
            x, d, r0, r1, q0, q1 = clipped(k, u, eta)
            check(d <= x / (2 * k + 1), "linear_envelope")
            check(u ** k * (k + 1 - k * u) <= 1, "envelope_polynomial")
            check(0 <= r1 <= x <= r0 <= 1, "clipped_rate_range")
            check(max(abs(r0 - x), abs(r1 - x)) <= eta, "clipped_error_band")
            check(r0 == min(1 - u ** (k + 1), x + eta), "min_map_identity")
            check(r1 == max(1 - u ** k, x - eta), "max_map_identity")
            if previous:
                check(r0 < previous[0] and r1 < previous[1], "strict_clipped_monotonicity")
            previous = (r0, r1)
            if d <= eta:
                check(q0 == q1, "inactive_region_exact_equality")
            else:
                check(x > (2 * k + 1) * eta, "active_command_barrier")
                check(0 <= x - eta <= x + eta <= 1, "active_rate_domain")
                qstar = u ** (k * (k + 1))
                check(q0 >= qstar >= q1, "active_common_mean_sandwich")
                check(0 <= q0 - q1 <= q0 == (1 - x - eta) ** k, "active_tv_envelope")
                check(q0 <= (1 - 2 * (k + 1) * eta) ** k, "rational_rare_event_envelope")
        check(clipped(k, F(0), eta)[2:4] == (1, 1), "clipped_endpoints")
        check(clipped(k, F(1), eta)[2:4] == (0, 0), "clipped_endpoints")

for k in range(1, 5):
    eta_star = F(k, k + 1) ** k / (2 * (k + 1))
    for ratio in [F(0), F(1, 10), F(1, 2), F(9, 10), F(1)]:
        eta = ratio * eta_star
        rational_envelope = (1 - 2 * (k + 1) * eta) ** k
        for depth in range(1, 5):
            P, Q = adaptive(k, eta, 0, depth), adaptive(k, eta, 1, depth)
            check(sum(P.values()) == sum(Q.values()) == 1, "adaptive_normalization")
            tv = sum(abs(P[h] - Q[h]) for h in P) / 2
            check(tv <= min(1, depth * rational_envelope), "adaptive_rare_event_tv")

for M in range(2, 65):
    for ratio in [F(0), F(1, 10), F(1, 2), F(9, 10), F(1)]:
        eta = ratio / (16 * M)
        x = max(F(1, M), 8 * M * eta)
        A, B = 1 - x - eta, 1 - x + eta
        g = A ** (M - 1) - B ** M
        check(F(1, M) <= x <= F(1, 2) and eta <= x / (8 * M), "upper_command_domain")
        check(0 < A <= B < 1 and B >= F(1, 2), "upper_no_clipping")
        z = 2 * eta / B
        check(0 <= z < 1 and (1 - z) ** (M - 1) >= 1 - (M - 1) * z,
              "bernoulli_inequality")
        bracket = x - eta - 2 * (M - 1) * eta / B
        check(bracket >= x - (4 * M - 3) * eta >= x / 2, "upper_gap_bracket")
        check(g >= B ** (M - 1) * bracket >= x * B ** (M - 1) / 2,
              "upper_gap_lower_bound")
        check(g >= x * (1 - x) ** (M - 1) / 2 > 0, "rational_positive_gap")
        check(x <= F(1, M) + 8 * M * eta, "simplified_budget_command")
        check(all(A ** j - B ** (j + 1) >= g for j in range(M)),
              "full_catalogue_gap_control")

result = {
    "status": "passed",
    "arithmetic": "exact fractions; exponential inequalities proved in the appendix",
    "families": dict(sorted(COUNTS.items())),
    "total_assertions": sum(COUNTS.values()),
    "appendix_sha256": sha256((ROOT / "POLYNOMIAL_EFFICIENCY_APPENDIX.md").read_bytes()).hexdigest(),
    "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT / "results" / "efficiency_controls.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
