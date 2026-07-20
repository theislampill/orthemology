#!/usr/bin/env python3
"""FCSP-1 power simulation — SYNTHETIC ASSUMPTIONS, NOT PILOT EVIDENCE.

Simulates the paired-item permutation test of analyze_fcsp.py under explicitly
synthetic effect assumptions to estimate power at the packet's item count and
repeat structure. Every number below is an assumption, labeled as such; none
derives from any run, pilot, or private record.
"""
import random

N_ITEMS = 32            # substantive items (F1-F8)
REPEATS = 5
ASSUMED_BASELINE_FC = 0.35   # synthetic assumption
ASSUMED_TREATMENT_FC = 0.20  # synthetic assumption (effect 0.15 > MIE 0.10)
ALPHA = 0.05
SIMS = 400
PERMS = 2000


def one_sim(rng):
    diffs = []
    for _ in range(N_ITEMS):
        b = sum(rng.random() < ASSUMED_BASELINE_FC for _ in range(REPEATS)) / REPEATS
        t = sum(rng.random() < ASSUMED_TREATMENT_FC for _ in range(REPEATS)) / REPEATS
        diffs.append(t - b)
    obs = abs(sum(diffs) / len(diffs))
    hits = 0
    for _ in range(PERMS):
        s = abs(sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs))
        if s >= obs - 1e-12:
            hits += 1
    return (hits / PERMS) < ALPHA


def main():
    rng = random.Random(20260727)
    wins = sum(one_sim(rng) for _ in range(SIMS))
    print("SYNTHETIC power estimate at assumed effect %.2f -> %.2f: %.3f (%d sims)"
          % (ASSUMED_BASELINE_FC, ASSUMED_TREATMENT_FC, wins / SIMS, SIMS))
    print("NOT PILOT EVIDENCE — assumptions are synthetic and labeled.")


if __name__ == "__main__":
    main()
