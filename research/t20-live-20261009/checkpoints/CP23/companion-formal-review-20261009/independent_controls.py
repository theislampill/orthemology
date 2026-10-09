"""Small reviewer-authored controls; no imports from the supplied companion.

Writes only its own result file beside this script. No network, subprocess,
toolchain, archive extraction, or source modification is used.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json


def components(vertices, edges):
    remaining = set(vertices)
    result = []
    while remaining:
        group = {min(remaining)}
        while True:
            enlarged = group | {v for a, b in edges for v in (a, b) if a in group or b in group}
            if enlarged == group:
                break
            group = enlarged
        result.append(sorted(group))
        remaining -= group
    return result


def main():
    # Evaluate stated semantics, rather than trusting the delivered D9 flags.
    facts = {"q"}
    part = {("q", "q")}
    attributes = {"knowledge-g", "power-g"}
    qualifiers = {("g", a) for a in attributes}
    atomic = all(p == "q" for p in facts if (p, "q") in part)
    distinct_qualifiers = any(a != b and ("g", a) in qualifiers and ("g", b) in qualifiers
                              for a in attributes for b in attributes)
    assert atomic and distinct_qualifiers

    # D2 repairs both retain the positive requisite premise P -> R.
    witness_tables = 0
    failures = [0, 0]
    for worlds in product(tuple(product((False, True), repeat=4)), repeat=3):
        cover = all(p or n0 or n1 for p, r, n0, n1 in worlds)
        positive_requires = all(not p or r for p, r, n0, n1 in worlds)
        uniform_n0 = all(p or n0 for p, r, n0, n1 in worlds)
        n0_requires = all(not n0 or r for p, r, n0, n1 in worlds)
        all_require = all((not n0 or r) and (not n1 or r) for p, r, n0, n1 in worlds)
        necessary_r = all(r for p, r, n0, n1 in worlds)
        failures[0] += positive_requires and uniform_n0 and n0_requires and not necessary_r
        failures[1] += positive_requires and cover and all_require and not necessary_r
        witness_tables += 1
    assert failures == [0, 0]

    # Complete upward closure of the stated E relation has only two target types:
    # the designated singleton {e}, and every other nonempty plurality.
    domain = tuple(range(1, 16))
    subset = lambda x, y: x & y == x
    base = lambda x, local: x == 1 or (local and x in (2, 4))
    closed = lambda x, local: any(subset(z, x) and base(z, local) for z in domain)
    partial = lambda x, local: any(subset(x, z) and closed(z, local) for z in domain)
    assert all(not (closed(x, local) and subset(x, y)) or closed(y, local)
               for x, y, local in product(domain, domain, (False, True)))
    totals = [x for x in domain if closed(x, False)]
    locals_ = [x for x in domain if closed(x, True)]
    assert totals == [1, 3, 5, 7, 9, 11, 13, 15]
    assert locals_ == [x for x in domain if x != 8]
    assert all(partial(x, local) for x, local in product(domain, (False, True)))
    # The same NEC failure in the delivered one-instance control persists.
    assert partial(2, False) and 1 != 2 and not subset(1, 2) and partial(1, False)

    # Factive-output-information refinement, proposed by the root reviewer.
    worlds = [(a, b, a ^ b) for a, b in product((0, 1), repeat=2)]
    raw_vertices = [(side, x) for side, x in product(("A", "B"), (0, 1))]
    raw_edges = [(("A", a), ("B", b)) for a, b, h in worlds]
    refined_edges = [(("A", a, h), ("B", b, h)) for a, b, h in worlds]
    refined_vertices = set(v for edge in refined_edges for v in edge)
    raw_components = components(raw_vertices, raw_edges)
    refined_components = components(refined_vertices, refined_edges)
    raw_a_determines = all(len({h for a, b, h in worlds if a == x}) == 1 for x in (0, 1))
    raw_b_determines = all(len({h for a, b, h in worlds if b == x}) == 1 for x in (0, 1))
    assert not raw_a_determines and not raw_b_determines and len(raw_components) == 1
    assert len(refined_components) == 4
    assert all(a[-1] == b[-1] for a, b in refined_edges)
    assert all(len({v[-1] for v in comp}) == 1 for comp in refined_components)

    # The finite anti-correlated law has the written covariance obstruction.
    law = {(0, 1): Fraction(1, 2), (1, 0): Fraction(1, 2)}
    means = [sum(m * s[i] for s, m in law.items()) for i in (0, 1)]
    cov = sum(m * s[0] * s[1] for s, m in law.items()) - means[0] * means[1]
    assert cov == Fraction(-1, 4)

    # A bounded conditional/conjunction diagnostic, not an explanation relation.
    intended = [(False, True), (True, True)]
    classical = list(product((False, True), repeat=2))
    r = lambda s, t: s and t
    forward_necessary = all(not s or r(s, t) for s, t in intended)
    forward_tautology = all(not s or r(s, t) for s, t in classical)
    reverse_tautology = all(not r(s, t) or s for s, t in classical)
    assert forward_necessary and not forward_tautology and reverse_tautology
    assert {r(s, t) for s, t in intended} == {False, True}

    result = {
        "passed": True,
        "scope": "Reviewer-authored bounded semantic controls, not a new checkpoint or full model campaign.",
        "D2_repair_world_tables": witness_tables,
        "D2_repair_failures": failures,
        "D2_retained_premise": "P implies R at every world",
        "D4_complete_upward_closure": {
            "total_explainers": totals,
            "local_explainers": locals_,
            "all_fifteen_facts_partially_explain_all_targets": True,
            "source_weakening_holds": True,
            "NEC_fails_at": {"x": 2, "target": [1], "y": 1},
            "distinct_target_behaviour_types_exhausted": 2,
            "all_32767_pluralities_reenumerated": False,
        },
        "D6_anticorrelated_covariance": str(cov),
        "D9_independently_evaluated_atomicity": atomic,
        "D9_independently_evaluated_distinct_attributes": distinct_qualifiers,
        "necessary_truth_padding_conditional_control": {
            "intended_worlds_S_T": intended,
            "R_formula": "S and T",
            "S_implies_R_necessary_in_intended_scope": forward_necessary,
            "S_implies_R_classical_tautology": forward_tautology,
            "R_implies_S_classical_tautology": reverse_tautology,
            "R_contingent_in_intended_scope": True,
            "requires_conjunctive_fact_admission_and_fine_grained_identity": True,
            "S_must_not_logically_entail_T": True,
            "productive_explanation_established": False,
        },
        "XOR_information_refinement": {
            "worlds_a_b_h": worlds,
            "raw_components": raw_components,
            "raw_A_determines_h": raw_a_determines,
            "raw_B_determines_h": raw_b_determines,
            "refined_components": refined_components,
            "both_refined_states_determine_h": True,
            "productive_relation_assigned": False,
            "metaphysical_possibility_authenticated": False,
        },
    }
    output = Path(__file__).with_name("INDEPENDENT_CONTROLS.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": True, "output": str(output),
                      "D2_tables": witness_tables, "XOR_refined_components": len(refined_components)}, indent=2))


if __name__ == "__main__":
    main()
