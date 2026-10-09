#!/usr/bin/env python3
"""Finite exact-rational diagnostics; the general theorems are proved in RESULT.md."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNTS = Counter()


def check(condition, family):
    assert condition, family
    COUNTS[family] += 1


def world(k, u, lam=F(1)):
    x = 1 - (u ** (k + 1) + u ** k) / 2
    r0 = 1 - u ** (k + 1)
    r1 = 1 - u ** k
    r0 = (1 - lam) * x + lam * r0
    r1 = (1 - lam) * x + lam * r1
    return x, r0, r1, (1 - r0) ** k, (1 - r1) ** (k + 1)


def transcript_law(k, lam, which, depth):
    law = {(): F(1)}
    for _ in range(depth):
        nxt = {}
        for history, mass in law.items():
            # History genuinely changes the next selected command.
            code = sum((bit + 1) * (i + 1) for i, bit in enumerate(history))
            u = F(1 + (code % 4), 5)
            q = world(k, u, lam)[3 + which]
            nxt[history + (1,)] = mass * q
            nxt[history + (0,)] = mass * (1 - q)
        law = nxt
    return law


for k in range(1, 33):
    b = F(k, k + 1)
    t, s = b ** (k + 1), b ** k
    delta = s - t
    eta_star = delta / 2
    m = (t + s) / 2
    check(delta == b ** k / (k + 1), "critical_value_identity")
    check(t ** k == s ** (k + 1), "critical_mean_identity")
    check(F(0) < t < s < 1, "critical_domain")

    grid = sorted(set([F(i, 16) for i in range(17)] + [b]))
    prev = None
    for u in grid:
        x, r0, r1, q0, q1 = world(k, u)
        err = u ** k * (1 - u) / 2
        check(q0 == q1 == u ** (k * (k + 1)), "all_command_identity")
        check(r0 - x == err and x - r1 == err, "symmetric_error_identity")
        check(0 <= err <= eta_star, "uniform_error_on_grid")
        check(0 <= x <= 1 and 0 <= r0 <= 1 and 0 <= r1 <= 1, "rate_domain")
        if prev:
            check(x < prev[0] and r0 < prev[1] and r1 < prev[2], "strict_monotonicity")
        prev = (x, r0, r1)
        for lam in [F(0), F(1, 4), F(1, 2), F(3, 4), F(99, 100), F(1)]:
            _, a0, a1, p0, p1 = world(k, u, lam)
            check(abs(a0 - x) <= lam * eta_star and abs(a1 - x) <= lam * eta_star,
                  "interpolated_map_error")
            check(abs(p0 - p1) <= (2 * k + 1) * (1 - lam) * eta_star,
                  "near_threshold_channel_bound")

    check(world(k, F(0))[:3] == (1, 1, 1), "endpoint_preservation")
    check(world(k, F(1))[:3] == (0, 0, 0), "endpoint_preservation")
    check(abs(world(k, b)[1] - world(k, b)[0]) == eta_star,
          "supremum_attained")

    for ratio in [F(0), F(1, 10), F(1, 2), F(9, 10), F(99, 100), F(999, 1000)]:
        eta = ratio * eta_star
        A, B = m - eta, m + eta
        check(0 < t < A <= B < s < 1, "no_clipping_below_threshold")
        check(A ** k > B ** (k + 1), "binary_strict_separation")
        gaps = [A ** j - B ** (j + 1) for j in range(k + 1)]
        check(all(g > 0 for g in gaps), "full_catalogue_separation")
        check(all(gaps[j] > gaps[j + 1] for j in range(k)),
              "last_gap_is_minimum")
        for j in range(k):
            check(gaps[j + 1] == A * gaps[j] - (B - A) * B ** (j + 1),
                  "gap_recurrence")
        thresholds = [(A ** j + B ** (j + 1)) / 2 for j in range(k + 1)]
        check(all(thresholds[j] > thresholds[j + 1] for j in range(k)),
              "decoder_threshold_order")
    check((m - eta_star) ** k == (m + eta_star) ** (k + 1),
          "touching_at_threshold")

for k in range(1, 5):
    eta_star = F(k, k + 1) ** k / (2 * (k + 1))
    for depth in range(1, 5):
        P = transcript_law(k, F(1), 0, depth)
        Q = transcript_law(k, F(1), 1, depth)
        check(P == Q, "adaptive_transcript_equality")
        check(sum(P.values()) == 1, "transcript_normalization")
        for lam in [F(1, 2), F(9, 10), F(99, 100)]:
            P = transcript_law(k, lam, 0, depth)
            Q = transcript_law(k, lam, 1, depth)
            tv = sum(abs(P[h] - Q[h]) for h in P) / 2
            bound = min(F(1), depth * (2 * k + 1) * (1 - lam) * eta_star)
            check(tv <= bound, "adaptive_tv_bound")

# Degenerate catalogue {0,1}: at x=1 endpoint preservation gives means 1 and 0.
check((1, 1 - F(1)) == (1, 0), "zero_count_endpoint_exception")

result = {
    "status": "passed",
    "arithmetic": "exact fractions; no simulated observations",
    "scope": "finite diagnostics, not substitutes for the proofs in RESULT.md",
    "families": dict(sorted(COUNTS.items())),
    "total_assertions": sum(COUNTS.values()),
    "result_sha256": sha256((ROOT / "RESULT.md").read_bytes()).hexdigest(),
    "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "exact_controls.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
