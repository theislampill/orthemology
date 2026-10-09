#!/usr/bin/env python3
"""Two finite illustrations of the symmetry addendum, not a frame census."""

from itertools import product
import json

W = (0, 1)


def box(R, values, w):
    return all(values[v] for v in W if (w, v) in R)


def diamond(R, values, w):
    return any(values[v] for v in W if (w, v) in R)


def premises(R, C, S):
    return all((not C[w] or S[w]) and
               (not S[w] or box(R, C, w)) for w in W)


def conclusion(R, C):
    return all(not diamond(R, C, w) or C[w] for w in W)


def properties(R):
    return {
        "reflexive": all((w, w) in R for w in W),
        "symmetric": all((v, w) in R for w, v in R),
        "transitive": all((w, u) in R for w, v in R
                          for x, u in R if x == v),
    }


# A symmetric frame that is neither reflexive nor transitive.
R_symmetric = {(0, 1), (1, 0)}
assert properties(R_symmetric) == {
    "reflexive": False, "symmetric": True, "transitive": False}
valuations_checked = 0
satisfying_premises = 0
counterexamples = 0
for C in product((False, True), repeat=2):
    for S in product((False, True), repeat=2):
        valuations_checked += 1
        if premises(R_symmetric, C, S):
            satisfying_premises += 1
            counterexamples += int(not conclusion(R_symmetric, C))
assert valuations_checked == 16
assert satisfying_premises == 2
assert counterexamples == 0

# A reflexive, transitive countermodel; every world has a successor.
R_directed = {(0, 0), (0, 1), (1, 1)}
C_directed = (False, True)
S_directed = (False, True)
assert properties(R_directed) == {
    "reflexive": True, "symmetric": False, "transitive": True}
assert all(any((w, v) in R_directed for v in W) for w in W)
assert premises(R_directed, C_directed, S_directed)
assert not conclusion(R_directed, C_directed)
assert not C_directed[0] and diamond(R_directed, C_directed, 0)

print(json.dumps({
    "scope": "local transport after admitted explanatory premises",
    "premises": ["globally C implies S", "globally S implies box C"],
    "conclusion": "diamond C implies C, equivalently not C implies box not C",
    "symmetric_example": {
        "relation": sorted(R_symmetric),
        "properties": properties(R_symmetric),
        "valuations_checked": valuations_checked,
        "satisfying_premises": satisfying_premises,
        "counterexamples": counterexamples,
    },
    "directed_countermodel": {
        "relation": sorted(R_directed),
        "properties": properties(R_directed),
        "C": C_directed,
        "S": S_directed,
        "global_premises_hold": True,
        "not_C_and_diamond_C_at_w0": True,
        "empty_successor_sets": False,
    },
    "limitation": "No full frame characterization or metaphysical-possibility claim"
}, indent=2))
