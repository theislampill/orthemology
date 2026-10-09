#!/usr/bin/env python3
"""Tiny finite S5 premise-independence control, not metaphysical possibility.

One rigid candidate g, two worlds, universal accessibility. E is existence;
C is adequate world-relative explanatory coverage. H includes necessary E
and necessary C. Enumerating H bridges checks the strong-profile restriction
only; defining H does not establish its metaphysical availability.
"""

from itertools import product
import json

W = (0, 1)
R = {(w, v) for w in W for v in W}
assert all((w, w) in R for w in W)
assert all((v, w) in R for w, v in R)
assert all((w, u) in R for w, v in R for x, u in R if x == v)


def box(values, w):
    return all(values[v] for v in W if (w, v) in R)


def diamond(values, w):
    return any(values[v] for v in W if (w, v) in R)


def globally_implies(left, right):
    return all(not left[w] or right[w] for w in W)


thin_count = 0
strong_count = 0
thin_failures = []
strong_failures = []
for E in product((False, True), repeat=2):
    N = tuple(box(E, w) for w in W)
    assert N[0] == N[1]  # de re necessary-existence predicate is invariant
    for C in product((False, True), repeat=2):
        if not globally_implies(C, N):
            continue
        thin_count += 1
        H = tuple(box(E, w) and box(C, w) for w in W)
        assert H[0] == H[1]
        target = tuple(C[w] or box(tuple(not c for c in C), w) for w in W)
        entry = {"E": E, "N": N, "C": C, "H": H,
                 "not_C_implies_box_not_C": target}
        if not all(target):
            thin_failures.append(entry)
        if globally_implies(C, H) and globally_implies(H, C):
            strong_count += 1
            if not all(target):
                strong_failures.append(entry)

witness = next(x for x in thin_failures if x["C"] == (False, True))
assert witness["E"] == (True, True)
assert witness["N"] == (True, True)
assert witness["H"] == (False, False)
assert witness["not_C_implies_box_not_C"] == (False, True)
assert diamond(witness["C"], 0)
assert not globally_implies(witness["C"], witness["H"])
assert thin_count == 7
assert len(thin_failures) == 2
assert strong_count == 5
assert not strong_failures

print(json.dumps({
    "scope": "finite logical premise-independence control only",
    "worlds": ["w0", "w1"],
    "accessibility": "universal S5",
    "candidate_domain": ["g"],
    "thin_constraint": "At every world C implies N; N is box E(g)",
    "strong_addition": "At every world C iff H; H is box E(g) and box C",
    "thin_models_checked": thin_count,
    "thin_countermodels": len(thin_failures),
    "strong_models_checked": strong_count,
    "strong_countermodels": len(strong_failures),
    "witness": witness,
    "witness_excluded_by": "C at w1 does not imply essential-coverage profile H",
    "limitation": "No claim of actual metaphysical possibility or source-theory refutation"
}, indent=2))
