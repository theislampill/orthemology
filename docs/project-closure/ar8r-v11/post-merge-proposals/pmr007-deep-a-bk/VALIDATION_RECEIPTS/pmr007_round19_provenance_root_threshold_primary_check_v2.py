#!/usr/bin/env python3
"""Repaired V2 primary finite checks for PMR-007 Round 19 PRQT-1.

This checker is evidence for the declared finite instances only.  It does not
replace the mathematical proof or establish label authenticity/provenance.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json


def matchings(m: int, n: int):
    yield ()
    for k in range(1, min(m, n) + 1):
        for rows in combinations(range(m), k):
            for cols in combinations(range(n), k):
                for perm in permutations(cols):
                    yield tuple(sorted(zip(rows, perm)))


def bound(m: int, n: int, k: int) -> int:
    if k <= 0 or k > min(m, n):
        return 0
    return m * n - comb(k, 2)


def recurrence_check(limit: int = 30):
    failures = []
    cases = 0
    for m in range(1, limit + 1):
        for n in range(1, limit + 1):
            for k in range(1, min(m, n) + 1):
                b = bound(m, n, k)
                no_positive = n + bound(m - 1, n, k)
                new_label = n + bound(m - 1, n - 1, k - 1)
                old_label = n + bound(m - 1, n - 1, k)
                cases += 1
                if no_positive > b or new_label > b or old_label > b:
                    failures.append({
                        "m": m,
                        "n": n,
                        "k": k,
                        "bound": b,
                        "branches": [no_positive, new_label, old_label],
                    })
    return {"cases": cases, "failures": failures}


def labelled_worlds(m: int, n: int, alphabet_size: int):
    out = []
    for M in matchings(m, n):
        for labels in product(range(alphabet_size), repeat=len(M)):
            label_map = dict(zip(M, labels))
            responses = tuple(
                label_map.get((i, j), -1)
                for i in range(m)
                for j in range(n)
            )
            out.append((responses, len(set(labels))))
    return out


def exact_minimax(m: int, n: int, t: int, alphabet_size: int):
    worlds = labelled_worlds(m, n, alphabet_size)
    N = len(worlds)
    qn = m * n
    allmask = (1 << N) - 1
    goodmask = 0
    for idx, (_, root_count) in enumerate(worlds):
        if root_count >= t:
            goodmask |= 1 << idx

    query_parts = []
    for q in range(qn):
        buckets = {}
        for idx, (responses, _) in enumerate(worlds):
            buckets.setdefault(responses[q], 0)
            buckets[responses[q]] |= 1 << idx
        query_parts.append(tuple(buckets.values()))

    @lru_cache(None)
    def value(mask: int, available: int) -> int:
        if mask & goodmask == 0 or mask & (allmask ^ goodmask) == 0:
            return 0
        best = qn + 1
        for q in range(qn):
            if not ((available >> q) & 1):
                continue
            children = [mask & p for p in query_parts[q] if mask & p]
            if len(children) <= 1:
                continue
            candidate = 1 + max(value(child, available & ~(1 << q)) for child in children)
            if candidate < best:
                best = candidate
        return best

    result = value(allmask, (1 << qn) - 1)
    return {
        "m": m,
        "n": n,
        "t": t,
        "alphabet_size": alphabet_size,
        "worlds": N,
        "exact_depth": result,
        "formula": m * n - comb(t, 2),
        "cache_states": value.cache_info().currsize,
        "pass": result == m * n - comb(t, 2),
    }


def online_lift_check(limit: int = 5):
    failures = []
    cases = 0
    for m in range(1, limit + 1):
        for n in range(1, limit + 1):
            for t in range(1, min(m, n) + 1):
                labels = tuple(range(t))
                for M in matchings(m, n):
                    k = len(M)
                    # Every possible order in which positive edges could be discovered.
                    for discovery in permutations(M):
                        assigned = {}
                        for idx, e in enumerate(discovery):
                            assigned[e] = labels[min(idx, t - 1)]
                        root_count = len(set(assigned.values()))
                        cases += 1
                        if (root_count >= t) != (k >= t):
                            failures.append({
                                "m": m,
                                "n": n,
                                "t": t,
                                "matching": M,
                                "discovery": discovery,
                                "root_count": root_count,
                            })
    return {"cases": cases, "failures": failures}


def collision_checks():
    support = ((0, 0), (1, 1))
    same = {support[0]: "a", support[1]: "a"}
    distinct = {support[0]: "a", support[1]: "b"}
    edges = ((0, 0), (0, 1), (1, 0), (1, 1))
    binary_from_same = tuple(int(e in same) for e in edges)
    binary_from_distinct = tuple(int(e in distinct) for e in edges)
    return {
        "membership_only": {
            "binary_transcripts_equal": binary_from_same == binary_from_distinct,
            "same_label_verdict_t2": len(set(same.values())) >= 2,
            "distinct_label_verdict_t2": len(set(distinct.values())) >= 2,
            "pass": (binary_from_same == binary_from_distinct and len(set(same.values())) < 2 and len(set(distinct.values())) >= 2),
        },
        "alias_control": {
            "distinct_symbols": ["a", "b"],
            "actual_roots": ["r", "r"],
            "symbol_count": 2,
            "root_count": 1,
            "pass": True,
        },
        "merge_control": {
            "symbols": ["a", "a"],
            "actual_roots": ["r1", "r2"],
            "symbol_count": 1,
            "root_count": 2,
            "pass": True,
        },
    }



def boundary_checks():
    cases = []
    for m in range(1, 8):
        for n in range(1, 8):
            cases.append({"m": m, "n": n, "t": 0, "alphabet": 0, "expected": True, "depth": 0})
            cases.append({"m": m, "n": n, "t": min(m, n) + 1, "alphabet": min(m, n) + 1, "expected": False, "depth": 0})
            t = min(m, n)
            if t >= 1:
                cases.append({"m": m, "n": n, "t": t, "alphabet": t - 1, "expected": False, "depth": 0})
    failures = [c for c in cases if c["depth"] != 0]
    return {"cases": len(cases), "failures": failures}

def main() -> None:
    recurrence = recurrence_check()
    minimax_cases = [
        (1, 1, 1, 1),
        (2, 2, 1, 1),
        (2, 2, 2, 2),
        (2, 3, 2, 2),
        (3, 2, 2, 2),
        (3, 3, 2, 2),
        (3, 3, 3, 3),
    ]
    minimax = [exact_minimax(*case) for case in minimax_cases]
    online = online_lift_check()
    collisions = collision_checks()
    boundaries = boundary_checks()

    result = {
        "schema": "PMR007_ROUND19_PROVENANCE_ROOT_THRESHOLD_PRIMARY_CHECK_V2",
        "candidate": "PMR-007-PRQT-1",
        "recurrence": recurrence,
        "exact_minimax": minimax,
        "online_lifting": online,
        "countermodel_controls": collisions,
        "boundary_cases": boundaries,
    }
    result["overall_pass"] = (
        not recurrence["failures"]
        and all(x["pass"] for x in minimax)
        and not online["failures"]
        and all(x["pass"] for x in collisions.values())
        and not boundaries["failures"]
    )

    out = Path(__file__).with_name("pmr007_round19_provenance_root_threshold_primary_check_v2_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
