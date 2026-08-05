#!/usr/bin/env python3
"""Executable verification for item N1 of AR8R-FABLE-R1-NEGATIVE-RESULTS.md.

Checks, by exhaustive computation over explicitly listed finite structures:

  1. the triangle countermodel: root-sets {r1,r2},{r2,r3},{r1,r3} have
     minimum transversal tau = 2 and maximum disjoint packing nu = 1;
  2. the path countermodel: root-sets {r1,r2},{r2,r3},{r3,r4} violate the
     matroid exchange axiom for pairwise-disjointness independence, witnessed
     by J1 = {e2}, J2 = {e1, e3};
  3. the withdrawn sharp threshold is indeed false: three multi-root
     structures (one 2-root item; two disjoint 2-root items; intersecting
     {r1,r2},{r1,r3}) each satisfy BOTH exchange and tau = nu;
  4. the single-root regime is sufficient: every root-multiset over 4 roots
     with up to 4 single-root items satisfies exchange and tau = nu
     (exhaustive over that bound, not sampled);
  5. quorum arithmetic within its declared range: for 2 <= n <= 7,
     1 <= k <= n, the k-subsets of n roots have tau = n-k+1, nu = floor(n/k),
     and tau = nu iff k = 1 or k = n.

Deterministic: no randomness. Output: one JSON object; exit 0 iff all checks
pass.
"""

import json
import sys
from itertools import combinations, product


def tau(edges, universe):
    if not edges:
        return 0
    for r in range(len(universe) + 1):
        for cand in combinations(sorted(universe), r):
            cset = set(cand)
            if all(cset & e for e in edges):
                return r
    raise AssertionError("unreachable")


def nu(edges):
    best = 0

    def rec(i, used, count):
        nonlocal best
        best = max(best, count)
        if i == len(edges) or count + (len(edges) - i) <= best:
            return
        if not (edges[i] & used):
            rec(i + 1, used | edges[i], count + 1)
        rec(i + 1, used, count)

    rec(0, set(), 0)
    return best


def independent_sets(edges):
    n = len(edges)
    out = []
    for mask in range(1 << n):
        sel = [i for i in range(n) if (mask >> i) & 1]
        if all(
            not (edges[a] & edges[b])
            for ai, a in enumerate(sel)
            for b in sel[ai + 1:]
        ):
            out.append(frozenset(sel))
    return set(out)


def exchange_holds(edges):
    indep = independent_sets(edges)
    for j1 in indep:
        for j2 in indep:
            if len(j1) < len(j2) and not any(
                j1 | {e} in indep for e in j2 - j1
            ):
                return False
    return True


def main() -> int:
    results = {}

    tri = [{"r1", "r2"}, {"r2", "r3"}, {"r1", "r3"}]
    results["triangle_tau_2_nu_1"] = (
        tau(tri, {"r1", "r2", "r3"}) == 2 and nu(tri) == 1
    )

    path = [{"r1", "r2"}, {"r2", "r3"}, {"r3", "r4"}]
    indep = independent_sets(path)
    j1, j2 = frozenset({1}), frozenset({0, 2})
    results["path_exchange_fails_at_J1_J2"] = (
        j1 in indep
        and j2 in indep
        and not any(j1 | {e} in indep for e in j2 - j1)
        and not exchange_holds(path)
    )

    counterexamples = {
        "single_2root_item": [{"r1", "r2"}],
        "two_disjoint_2root_items": [{"r1", "r2"}, {"r3", "r4"}],
        "intersecting_2root_items": [{"r1", "r2"}, {"r1", "r3"}],
    }
    for name, edges in counterexamples.items():
        uni = set().union(*edges)
        results[f"threshold_false_{name}"] = (
            exchange_holds(edges) and tau(edges, uni) == nu(edges)
        )

    ok_single = True
    roots = ["r1", "r2", "r3", "r4"]
    for n_items in range(1, 5):
        for combo in product(roots, repeat=n_items):
            edges = [{r} for r in combo]
            uni = set(combo)
            if not (exchange_holds(edges) and tau(edges, uni) == nu(edges)):
                ok_single = False
    results["single_root_regime_sufficient_exhaustive"] = ok_single

    ok_quorum = True
    for n in range(2, 8):
        for k in range(1, n + 1):
            routes = [set(c) for c in combinations(range(n), k)]
            t, v = tau(routes, set(range(n))), nu(routes)
            if t != n - k + 1 or v != n // k or (t == v) != (k in (1, n)):
                ok_quorum = False
    results["quorum_range_n2_to_7"] = ok_quorum

    ok = all(results.values())
    json.dump(
        {"python_version": sys.version.split()[0], "checks": results, "pass": ok},
        sys.stdout,
        indent=2,
    )
    print()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
