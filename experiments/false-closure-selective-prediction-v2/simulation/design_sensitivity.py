#!/usr/bin/env python3
"""FCSP-2 PRE-RUN design sensitivity — SYNTHETIC ASSUMPTIONS, NOT PILOT EVIDENCE.

Unit-aligned with the analysis (audit B4 repair): simulates ITEM-level paired
contrasts (40 substantive items, single deterministic repeat) under labeled
synthetic effect assumptions, using the same arm-swap permutation test the
analysis runs. This fixes the design's sensitivity BEFORE any run; no
post-hoc power computation exists in this packet.
"""
import random

N_ITEMS = 40
ASSUMED_BASE_FC = 0.35     # synthetic assumption
ASSUMED_TREAT_FC = 0.20    # synthetic assumption (effect 0.15 > MIE 0.10)
ALPHA = 0.05
SIMS = 400
PERMS = 2000


def one_sim(rng):
    diffs = []
    for _ in range(N_ITEMS):
        b = 1.0 if rng.random() < ASSUMED_BASE_FC else 0.0
        t = 1.0 if rng.random() < ASSUMED_TREAT_FC else 0.0
        diffs.append(t - b)
    obs = abs(sum(diffs) / len(diffs))
    hits = 0
    for _ in range(PERMS):
        s = abs(sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs))
        if s >= obs - 1e-12:
            hits += 1
    return (hits / PERMS) < ALPHA


def main():
    rng = random.Random(20260732)
    wins = sum(one_sim(rng) for _ in range(SIMS))
    print("SYNTHETIC design sensitivity (item-level, single repeat): %.3f at assumed "
          "%.2f -> %.2f (%d sims). NOT PILOT EVIDENCE."
          % (wins / SIMS, ASSUMED_BASE_FC, ASSUMED_TREAT_FC, SIMS))


if __name__ == "__main__":
    main()
