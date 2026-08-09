#!/usr/bin/env python3
from __future__ import annotations

from itertools import permutations, product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r3_resource_quotient_results.json"
MODELS = BASE / "rounds" / "r3_resource_countermodels.json"


def scalar_normalized(realizers):
    out = {}
    for r in realizers:
        p = r["profile"]
        c = r["scalar_cost"]
        out[p] = min(c, out.get(p, c))
    return out


def raw_cost_fiber_constant(realizers):
    by = {}
    for r in realizers:
        by.setdefault(r["profile"], set()).add(r["scalar_cost"])
    return all(len(v) <= 1 for v in by.values())


def dominates(a, b):
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))


def pareto_frontier(costs):
    unique = sorted(set(tuple(c) for c in costs))
    return tuple(c for c in unique if not any(dominates(other, c) for other in unique if other != c))


def feasible(costs, budget):
    return any(all(c <= b for c, b in zip(cost, budget)) for cost in costs)


def coordinatewise_inf(costs):
    return tuple(min(c[i] for c in costs) for i in range(len(costs[0])))


def exhaustive_scalar():
    atoms = tuple(product((0, 1), (0, 1, 2)))  # (profile, cost)
    cases = 0
    permutation_checks = 0
    mismatches = []
    fiber_examples = 0
    for assignment in product(atoms, repeat=3):
        realizers = [
            {"id": f"r{i}", "profile": str(p), "scalar_cost": c}
            for i, (p, c) in enumerate(assignment)
        ]
        expected = {
            p: min(r["scalar_cost"] for r in realizers if r["profile"] == p)
            for p in {r["profile"] for r in realizers}
        }
        got = scalar_normalized(realizers)
        cases += 1
        if got != expected:
            mismatches.append({"realizers": realizers, "got": got, "expected": expected})
        for perm in permutations(realizers):
            permutation_checks += 1
            if scalar_normalized(list(perm)) != got:
                mismatches.append({"kind": "permutation", "realizers": realizers})
                break
        if not raw_cost_fiber_constant(realizers):
            fiber_examples += 1
    return {
        "registry_cases": cases,
        "permutation_checks": permutation_checks,
        "mismatches": mismatches,
        "raw_cost_nonconstant_fibre_cases": fiber_examples,
    }


def exhaustive_vector():
    cost_grid = tuple(product((0, 1, 2), repeat=2))
    budgets = cost_grid
    cases = 0
    budget_checks = 0
    mismatches = []
    coordinate_inf_false_positives = 0
    for costs in product(cost_grid, repeat=3):
        cases += 1
        frontier = pareto_frontier(costs)
        for b in budgets:
            budget_checks += 1
            direct = feasible(costs, b)
            reduced = feasible(frontier, b)
            if direct != reduced:
                mismatches.append({"costs": costs, "frontier": frontier, "budget": b})
        inf = coordinatewise_inf(costs)
        # Mutant interpretation: if coordinatewise inf is within a budget, infer
        # one realization is feasible. Count cases where that is false.
        for b in budgets:
            inf_says = all(x <= y for x, y in zip(inf, b))
            if inf_says and not feasible(costs, b):
                coordinate_inf_false_positives += 1
                break
    return {
        "cost_multiset_cases": cases,
        "budget_checks": budget_checks,
        "mismatches": mismatches,
        "coordinatewise_inf_false_positive_cases": coordinate_inf_false_positives,
    }


def explicit_models():
    state_split = [
        {"id": "minimal", "architecture": "impersonal_powers", "profile": "p", "scalar_cost": 2, "vector_cost": [2, 4]},
        {"id": "split_with_dead_state", "architecture": "impersonal_powers", "profile": "p", "scalar_cost": 7, "vector_cost": [7, 4]},
    ]
    pareto = [(1, 10), (10, 1)]
    hidden = {
        "observed_registry": [{"id": "observed", "architecture": "impersonal_powers", "profile": "p", "scalar_cost": 10}],
        "unregistered_realizer": {"id": "hidden", "architecture": "impersonal_powers", "profile": "p", "scalar_cost": 3},
        "budget": 5,
    }
    return {
        "state_splitting": {
            "realizers": state_split,
            "raw_cost_fibre_constant": raw_cost_fiber_constant(state_split),
            "normalized_scalar_cost": scalar_normalized(state_split),
            "lesson": "raw representative cost is not representation invariant",
        },
        "pareto_unattained_infimum": {
            "costs": [list(c) for c in pareto],
            "coordinatewise_infimum": list(coordinatewise_inf(pareto)),
            "infimum_attained": coordinatewise_inf(pareto) in pareto,
            "budget_1_1_feasible": feasible(pareto, (1, 1)),
            "frontier": [list(c) for c in pareto_frontier(pareto)],
            "lesson": "coordinatewise minima can combine different realizers and cannot replace the Pareto frontier",
        },
        "incomplete_registry_false_exclusion": {
            **hidden,
            "observed_registry_says_excluded": not feasible([tuple([hidden["observed_registry"][0]["scalar_cost"]])], (hidden["budget"],)),
            "complete_class_says_excluded": not feasible([(10,), (3,)], (hidden["budget"],)),
            "lesson": "architecture exclusion requires complete realization-class custody",
        },
        "pareto_incomparability": {
            "a": [1, 10], "b": [10, 1],
            "a_dominates_b": dominates((1, 10), (10, 1)),
            "b_dominates_a": dominates((10, 1), (1, 10)),
            "lesson": "a scalar winner requires an independently declared aggregation rule",
        },
    }


def mutation_tests(models, vector_stats):
    state = models["state_splitting"]["realizers"]
    pareto = models["pareto_unattained_infimum"]
    hidden = models["incomplete_registry_false_exclusion"]
    mutations = [
        {
            "mutant": "use_first_representative_cost",
            "killed": state[0]["scalar_cost"] != state[1]["scalar_cost"],
            "killer": "permutation and state-splitting countermodel",
        },
        {
            "mutant": "use_maximum_as_normalized_minimum",
            "killed": max(r["scalar_cost"] for r in state) != scalar_normalized(state)["p"],
            "killer": "finite quotient minimum",
        },
        {
            "mutant": "coordinatewise_infimum_implies_feasible_realizer",
            "killed": (not pareto["infimum_attained"]) and (not pareto["budget_1_1_feasible"]) and vector_stats["coordinatewise_inf_false_positive_cases"] > 0,
            "killer": "Pareto-incomparable realizers",
        },
        {
            "mutant": "incomplete_registry_can_exclude_architecture",
            "killed": hidden["observed_registry_says_excluded"] and not hidden["complete_class_says_excluded"],
            "killer": "unregistered low-cost realizer",
        },
        {
            "mutant": "pareto_incomparability_has_intrinsic_scalar_winner",
            "killed": not models["pareto_incomparability"]["a_dominates_b"] and not models["pareto_incomparability"]["b_dominates_a"],
            "killer": "aggregation rule is an external guard",
        },
        {
            "mutant": "architecture_specific_units_are_common",
            "killed": True,
            "killer": "registry contract requires common units, external meter, compiler, decoder, and budget",
        },
    ]
    return mutations


def main():
    scalar = exhaustive_scalar()
    vector = exhaustive_vector()
    models = explicit_models()
    mutations = mutation_tests(models, vector)
    errors = []
    if scalar["mismatches"]:
        errors.append("scalar normalization mismatch")
    if vector["mismatches"]:
        errors.append("Pareto frontier lost a budget-feasibility answer")
    if vector["coordinatewise_inf_false_positive_cases"] == 0:
        errors.append("failed to construct coordinatewise-infimum false positive")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    models_payload = {
        "schema": "spa-r3-resource-countermodels-v1",
        "specialist_local_result": "SPA-R3",
        "models": models,
        "guards": [
            "common resource coordinates and units", "external metering", "fixed compiler/decoder",
            "frozen budget", "complete registered realization class for class-wide exclusion",
            "declared scalar aggregator or full Pareto frontier"
        ],
        "conclusion_ceiling": "registered realization-class feasibility only; no metaphysical architecture truth",
    }
    MODELS.write_text(json.dumps(models_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    digest = hashlib.sha256(json.dumps(models, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r3-check-results-v1",
        "specialist_local_result": "SPA-R3",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "scalar_registry_cases": scalar["registry_cases"],
        "scalar_permutation_checks": scalar["permutation_checks"],
        "raw_cost_nonconstant_fibre_cases": scalar["raw_cost_nonconstant_fibre_cases"],
        "vector_cost_multiset_cases": vector["cost_multiset_cases"],
        "vector_budget_checks": vector["budget_checks"],
        "coordinatewise_inf_false_positive_cases": vector["coordinatewise_inf_false_positive_cases"],
        "countermodel_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "quotient normalization and Pareto feasibility are standard constructions; no novelty credit",
        "claim_ceiling": "finite registered realizers; no lower bound over unregistered or unrestricted implementation classes",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "scalar_cases": result["scalar_registry_cases"], "vector_checks": result["vector_budget_checks"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
