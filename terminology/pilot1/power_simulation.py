#!/usr/bin/env python3
"""Simulation-based power for the crossed random-effects terminology design.

ALL PARAMETERS BELOW ARE SYNTHETIC PLACEHOLDERS (marked PLACEHOLDER). They are
NOT pilot estimates — no pilot has run — and any output produced with them is a
demonstration of the machinery, never a power claim. Replace the PLACEHOLDER
block with estimated components after Pilot 0/1, bump PARAMS_VERSION, and
record the change in the deviation ledger of the packet that consumes it.

Usage: python power_simulation.py [--sims 500] [--n-items 12] [--n-raters 3]
       [--n-runs 4] [--effect-pp 15]
"""
import argparse
import math
import random

PARAMS_VERSION = "0-PLACEHOLDER"

# --- PLACEHOLDER variance components (logit scale), clearly synthetic ---
PLACEHOLDER = {
    "baseline_rate_armB": 0.55,   # PLACEHOLDER: primary-endpoint rate under Arm B
    "sd_item": 0.60,              # PLACEHOLDER
    "sd_rater": 0.25,             # PLACEHOLDER
    "sd_run": 0.40,               # PLACEHOLDER
}


def logit(p):
    return math.log(p / (1 - p))


def inv_logit(x):
    return 1 / (1 + math.exp(-x))


def simulate_once(rng, n_items, n_raters, n_runs, effect_pp):
    p0 = PLACEHOLDER["baseline_rate_armB"]
    beta = logit(min(0.99, p0 + effect_pp / 100)) - logit(p0)
    items = [rng.gauss(0, PLACEHOLDER["sd_item"]) for _ in range(n_items)]
    raters = [rng.gauss(0, PLACEHOLDER["sd_rater"]) for _ in range(n_raters)]
    cells = []
    for arm_effect, arm in ((0.0, "B"), (beta, "C")):
        for i, it in enumerate(items):
            for r in range(n_runs):
                run_e = rng.gauss(0, PLACEHOLDER["sd_run"])
                eta = logit(p0) + arm_effect + it + run_e
                # rater majority over binary scores
                votes = [int(rng.random() < inv_logit(eta + ra)) for ra in raters]
                cells.append((arm, sum(votes) > len(votes) / 2))
    # crude arm-difference z-test on cell successes (stand-in for the mixed model;
    # the real analysis is the mixed model in the spec — this is a power *screen*)
    b = [s for a, s in cells if a == "B"]
    c = [s for a, s in cells if a == "C"]
    pb, pc, n = sum(b) / len(b), sum(c) / len(c), len(b)
    pooled = (sum(b) + sum(c)) / (2 * n)
    se = math.sqrt(2 * pooled * (1 - pooled) / n) or 1e-9
    z = (pc - pb) / se
    return z > 1.96


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=500)
    ap.add_argument("--n-items", type=int, default=12)
    ap.add_argument("--n-raters", type=int, default=3)
    ap.add_argument("--n-runs", type=int, default=4)
    ap.add_argument("--effect-pp", type=float, default=15.0)
    args = ap.parse_args()
    rng = random.Random(1)
    hits = sum(simulate_once(rng, args.n_items, args.n_raters, args.n_runs, args.effect_pp)
               for _ in range(args.sims))
    print("PARAMS_VERSION:", PARAMS_VERSION, "(SYNTHETIC PLACEHOLDERS — not a power claim)")
    print("simulated power at +%.0f pp with %d items x %d runs: %.2f"
          % (args.effect_pp, args.n_items, args.n_runs, hits / args.sims))


if __name__ == "__main__":
    main()
