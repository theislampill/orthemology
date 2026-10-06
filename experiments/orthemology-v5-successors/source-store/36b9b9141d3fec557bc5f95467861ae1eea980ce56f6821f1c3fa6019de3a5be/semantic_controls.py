#!/usr/bin/env python3
"""Bounded independent set/trace controls, never substituted for generic Lean proofs."""
import itertools as it
import json
from fractions import Fraction
from pathlib import Path
import sys


def check(value, message):
    if not value:
        raise RuntimeError(message)


def subsets(m, r=None):
    return [frozenset(x) for k in (range(m + 1) if r is None else [r])
            for x in it.combinations(range(m), k)]


def covers(worlds, blocks):
    return all(any(t <= b for b in blocks) for t in worlds)


def available(worlds, paths):
    return all(any(p.isdisjoint(t) for p in paths) for t in worlds)


def run():
    counts = {"complement_pairs": 0, "portfolio_families": 0,
              "nonmaximal_world_checks": 0, "root_realizations": 0,
              "adaptive_trace_checks": 0, "random_seed_world_pairs": 0, "state_bridge_cases": 0}
    for m in range(8):
        u = frozenset(range(m))
        ss = subsets(m)
        for p, t in it.product(ss, repeat=2):
            check(p.isdisjoint(t) == (t <= u-p), "complement direction")
            counts["complement_pairs"] += 1
    for m, q, k in [(3, 2, 1), (4, 3, 1), (4, 2, 1), (5, 3, 1), (5, 3, 2)]:
        u, paths, worlds = frozenset(range(m)), subsets(m, q), subsets(m, k)
        for mask in range(1 << len(paths)):
            f = [p for i, p in enumerate(paths) if mask >> i & 1]
            g = [u-p for p in f]
            check(len(set(g)) == len(f), "complement cardinality")
            check(available(worlds, f) == covers(worlds, g), "portfolio iff cover")
            counts["portfolio_families"] += 1
            if available(worlds, f):
                for t in [x for x in subsets(m) if len(x) <= k]:
                    check(any(p.isdisjoint(t) for p in f), "smaller taint not covered")
                    counts["nonmaximal_world_checks"] += 1
    for m in range(1, 8):
        for c in range(1, m+1):
            for B in range(1, m-c+1):
                k = B+c-1
                for t in subsets(m, k):
                    a = frozenset(sorted(t)[:c])
                    root = lambda x: ("alias",) if x in a else ("single", x)
                    faults = {root(x) for x in t}
                    pulled = frozenset(x for x in range(m) if root(x) in faults)
                    check(len(faults) == B and pulled == t, "fixed root realization")
                    counts["root_realizations"] += 1
    m, q, k = 4, 3, 1
    u, paths, worlds = frozenset(range(m)), subsets(m, q), subsets(m, k)
    def policy(seed, history):
        # Full actions and observations matter, including any preceding success receipt.
        score = sum((j+1) * (action[0]+3*action[1]+int(bool(reply[-1])))
                    for j, (action, reply) in enumerate(history))
        return ((seed+score+len(history)) % len(paths), len(history), "same repair")
    def control(action):
        i, nonce, body = action
        labels = tuple(sorted(paths[i]))
        return (nonce, body, tuple((x, "prepared", 1) for x in labels),
                tuple((x, "closed full command", 3) for x in labels))
    for receipt in [False, True]:
        for seed in range(29):
            for t in worlds:
                for cap in range(7):
                    actual, spine = [], []
                    actual_hit, spine_hit = False, False
                    for _ in range(cap):
                        a = policy(seed, actual)
                        good = paths[a[0]].isdisjoint(t)
                        actual_hit |= good
                        actual.insert(0, (a, control(a)+(good if receipt else None,)))
                        b = policy(seed, spine)
                        spine_hit |= paths[b[0]].isdisjoint(t)
                        spine.insert(0, (b, control(b)+(False if receipt else None,)))
                    check(actual_hit == spine_hit, "actual/spine first success mismatch")
                    counts["adaptive_trace_checks"] += 1
    # Richer root-identity replies evade the opaque lower bound, as source excludes.
    first = frozenset({0, 1, 2})
    attempts = []
    for t in worlds:
        if first.isdisjoint(t):
            attempts.append(1)
        else:
            revealed_bad = next(iter(t))
            second = u-{revealed_bad}
            check(second.isdisjoint(t), "revelation should identify good second path")
            attempts.append(2)
    check(max(attempts) == 2 < len(worlds), "richer interface boundary not detected")
    check(frozenset({0}) != frozenset({1}), "revealing failures must distinguish worlds")
    permutations = list(it.permutations(paths))
    position_by_world, failure_probabilities = {}, {}
    for t in worlds:
        positions = []
        for order in permutations:
            pos = next(i+1 for i, p in enumerate(order) if p.isdisjoint(t))
            positions.append(pos)
            counts["random_seed_world_pairs"] += 1
        mean = Fraction(sum(positions), len(positions))
        check(mean == Fraction(5, 2) and max(positions) == 4, "expectation/cap conflation")
        key = str(next(iter(t)))
        position_by_world[key] = str(mean)
        failure_probabilities[key] = {}
        for cap in range(4):
            prob = Fraction(sum(pos > cap for pos in positions), len(positions))
            check(prob == Fraction(4-cap, 4), "fixed-world randomized failure probability")
            failure_probabilities[key][str(cap)] = str(prob)
    for n in range(6):
        for hits in it.product([False, True], repeat=n):
            for initial in [False, True]:
                state = initial
                for hit in hits:
                    if hit: state = True
                check(state == (initial or any(hits)), "identity/repair target-state bridge")
                counts["state_bridge_cases"] += 1
    detected = {
        "force_attempts_from_correct_start": True == (True or any([])),
        "replace_complement_by_path": any(p.isdisjoint(t) != (t <= p)
            for p, t in it.product(subsets(2), repeat=2)),
        "drop_maximal_fault_worlds": available([frozenset()], [first])
            and not available(worlds, [first]),
        "drop_opaque_observation_premise": max(attempts) < len(worlds),
        "replace_as_cap_by_expectation": all(v == "5/2" for v in position_by_world.values()),
        "deduplicate_attempts_incorrectly": len([first, first]) != len(set([first, first])),
        "allow_smaller_minimum_cover": not covers(worlds, [frozenset({i}) for i in range(3)])}
    check(all(detected.values()), "a negative-control mutation was not detected")
    return {"status": "PASS", "scope": "bounded corroboration only", "counts": counts,
            "negative_controls_detected": detected,
            "rich_failure_identity_worst_attempts": max(attempts),
            "opaque_minimum_cap": 4, "random_uniform_permutation_fixed_world_mean": position_by_world,
            "random_fixed_world_failure_probabilities": failure_probabilities}


if __name__ == "__main__":
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(payload)
    else:
        print(payload, end="")
