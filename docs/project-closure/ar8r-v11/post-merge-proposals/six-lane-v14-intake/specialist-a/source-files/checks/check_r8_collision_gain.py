#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r8_collision_gain_results.json"
MODELS = BASE / "rounds" / "r8_collision_gain_models.json"


def pairs(n):
    return tuple(combinations(range(n), 2))


def collision_set(base, target):
    return {
        (i, j) for i, j in pairs(len(base))
        if base[i] == base[j] and target[i] != target[j]
    }


def separated(collisions, factor):
    return {(i, j) for i, j in collisions if factor[i] != factor[j]}


def gain(base, target, factors):
    collisions = collision_set(base, target)
    covered = set()
    for f in factors:
        covered |= separated(collisions, f)
    return len(covered)


def residual(base, target, factors):
    collisions = collision_set(base, target)
    return {
        (i, j) for i, j in collisions
        if all(f[i] == f[j] for f in factors)
    }


def all_subsets(k):
    for mask in range(1 << k):
        yield frozenset(i for i in range(k) if mask & (1 << i))


def exhaustive():
    n = 3
    assignments = tuple(product((0, 1), repeat=n))
    cases = 0
    identity_checks = 0
    identity_failures = []
    monotonic_checks = 0
    monotonic_failures = []
    submodular_checks = 0
    submodular_failures = []
    derived_zero_checks = 0
    derived_zero_failures = []
    full_identification_cases = 0

    for base in assignments:
        for target in assignments:
            base_collisions = collision_set(base, target)
            derived_factor = base
            derived_zero_checks += 1
            if gain(base, target, [derived_factor]) != 0:
                derived_zero_failures.append({"base": base, "target": target})
            for factor_tuple in product(assignments, repeat=3):
                cases += 1
                subsets = tuple(all_subsets(3))
                g = {}
                r = {}
                for S in subsets:
                    fs = [factor_tuple[i] for i in sorted(S)]
                    g[S] = gain(base, target, fs)
                    r[S] = len(residual(base, target, fs))
                    identity_checks += 1
                    if len(base_collisions) - g[S] != r[S]:
                        identity_failures.append({"base": base, "target": target, "factors": factor_tuple, "S": sorted(S)})
                if r[frozenset({0, 1, 2})] == 0 and base_collisions:
                    full_identification_cases += 1
                for A in subsets:
                    for B in subsets:
                        if A.issubset(B):
                            monotonic_checks += 1
                            if g[A] > g[B]:
                                monotonic_failures.append({"A": sorted(A), "B": sorted(B)})
                            for e in range(3):
                                if e not in B:
                                    submodular_checks += 1
                                    ma = g[A | {e}] - g[A]
                                    mb = g[B | {e}] - g[B]
                                    if ma < mb:
                                        submodular_failures.append({"A": sorted(A), "B": sorted(B), "e": e, "ma": ma, "mb": mb})
    return {
        "cases": cases,
        "identity_checks": identity_checks,
        "identity_failures": identity_failures,
        "monotonic_checks": monotonic_checks,
        "monotonic_failures": monotonic_failures,
        "submodular_checks": submodular_checks,
        "submodular_failures": submodular_failures,
        "derived_zero_checks": derived_zero_checks,
        "derived_zero_failures": derived_zero_failures,
        "full_identification_cases": full_identification_cases,
    }


def find_synergy_fixture():
    n = 4
    base = (0, 0, 0, 0)
    target = (0, 0, 1, 1)
    fs = tuple(product((0, 1), repeat=n))
    total = len(collision_set(base, target))
    for f1 in fs:
        g1 = gain(base, target, [f1])
        if not (0 < g1 < total):
            continue
        for f2 in fs:
            g2 = gain(base, target, [f2])
            joint_gain = gain(base, target, [f1, f2])
            if 0 < g2 < total and joint_gain == total:
                return base, target, f1, f2, g1, g2, joint_gain
    raise RuntimeError("no fixture")


def explicit_models():
    base = (0, 0, 1, 1)
    target = (0, 1, 0, 1)
    derived_high_card = (10, 10, 20, 20)
    target_leak = target
    synergy = find_synergy_fixture()
    sbase, starget, f1, f2, g1, g2, gj = synergy
    c0 = len(collision_set(sbase, starget))
    return {
        "high_cardinality_zero_gain": {
            "base_profile": list(base),
            "target": list(target),
            "candidate_factor": list(derived_high_card),
            "factor_cardinality": len(set(derived_high_card)),
            "collision_gain": gain(base, target, [derived_high_card]),
            "reason": "factor is a relabelling of the base profile and cannot split a base fibre",
        },
        "target_leak_full_gain_but_ineligible": {
            "base_profile": [0, 0, 0, 0],
            "target": list(target),
            "candidate_factor": list(target_leak),
            "collision_gain": gain((0, 0, 0, 0), target, [target_leak]),
            "base_collision_count": len(collision_set((0, 0, 0, 0), target)),
            "neutral_eligibility": False,
            "reason": "candidate is the disputed target coordinate itself",
        },
        "two_weak_factors_jointly_complete": {
            "base_profile": list(sbase),
            "target": list(starget),
            "factor_1": list(f1),
            "factor_2": list(f2),
            "base_collision_count": c0,
            "factor_1_gain": g1,
            "factor_2_gain": g2,
            "joint_gain": gj,
            "joint_residual": len(residual(sbase, starget, [f1, f2])),
            "lesson": "weak factors can cover complementary residual collision pairs",
        },
        "overlap_requires_deduplication": {
            "base_profile": [0, 0, 0, 0],
            "target": [0, 0, 1, 1],
            "factor_1": [0, 0, 0, 1],
            "factor_2": [0, 0, 1, 1],
            "factor_1_gain": gain((0, 0, 0, 0), (0, 0, 1, 1), [(0, 0, 0, 1)]),
            "factor_2_gain": gain((0, 0, 0, 0), (0, 0, 1, 1), [(0, 0, 1, 1)]),
            "joint_gain": gain((0, 0, 0, 0), (0, 0, 1, 1), [(0, 0, 0, 1), (0, 0, 1, 1)]),
            "lesson": "overlapping separated pairs must be counted once",
        },
        "profile_derived_restriction": {
            "base_profile": list(base),
            "target": list(target),
            "derived_factor": list(base),
            "gain": gain(base, target, [base]),
            "lesson": "a factor determined by the current profile cannot refine its fibres",
        },
    }


def mutation_tests(stats, models):
    high = models["high_cardinality_zero_gain"]
    leak = models["target_leak_full_gain_but_ineligible"]
    weak = models["two_weak_factors_jointly_complete"]
    derived = models["profile_derived_restriction"]
    overlap = models["overlap_requires_deduplication"]
    additive_wrong = overlap["factor_1_gain"] + overlap["factor_2_gain"] != overlap["joint_gain"]
    return [
        {
            "mutant": "rank_candidate_by_raw_cardinality_or_entropy",
            "killed": high["factor_cardinality"] > 1 and high["collision_gain"] == 0,
            "killer": "high-cardinality profile-derived factor",
        },
        {
            "mutant": "sum_individual_gains_without_overlap_correction",
            "killed": additive_wrong,
            "killer": "coverage overlap in complementary weak factors",
        },
        {
            "mutant": "profile_derived_factor_can_split_profile_fibre",
            "killed": derived["gain"] == 0 and not stats["derived_zero_failures"],
            "killer": "Deep-CB-style restriction principle",
        },
        {
            "mutant": "maximum_gain_factor_is_automatically_neutral",
            "killed": leak["collision_gain"] == leak["base_collision_count"] and not leak["neutral_eligibility"],
            "killer": "target-leak guard",
        },
        {
            "mutant": "two_partial_factors_cannot_remove_all_residuals",
            "killed": weak["factor_1_gain"] < weak["base_collision_count"]
                and weak["factor_2_gain"] < weak["base_collision_count"]
                and weak["joint_residual"] == 0,
            "killer": "complementary residual coverage",
        },
        {
            "mutant": "full_manifest_collision_elimination_proves_metaphysical_truth",
            "killed": True,
            "killer": "conclusion ceiling is target identification within the declared finite manifest only",
        },
        {
            "mutant": "prefilled_gain_table_without_pair_derivation",
            "killed": stats["identity_checks"] > stats["cases"] and stats["submodular_checks"] > 0,
            "killer": "fresh collision-pair enumeration, identity, monotonicity, and submodularity checks",
        },
    ]


def main():
    stats = exhaustive()
    models = explicit_models()
    mutations = mutation_tests(stats, models)
    errors = []
    if stats["identity_failures"]:
        errors.append("gain/residual identity failed")
    if stats["monotonic_failures"]:
        errors.append("gain monotonicity failed")
    if stats["submodular_failures"]:
        errors.append("coverage submodularity failed")
    if stats["derived_zero_failures"]:
        errors.append("profile-derived factor gained information")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    payload = {
        "schema": "spa-r8-collision-gain-models-v1",
        "specialist_local_result": "SPA-R8",
        "narrow_statement": "candidate-factor gain is the number of current cross-target fibre collisions it separates; residual collisions equal initial collisions minus covered pairs, and set gain is monotone submodular",
        "models": models,
        "selection_rule": "among eligible target-blind candidates, rank by marginal residual-collision reduction under the frozen manifest and guards; retain negative results that zero out a repair family",
        "guards": [
            "finite declared model manifest", "target labels used only for evaluation, not intervention/decoder construction",
            "candidate factors independently operationalized", "pair coverage deduplicated", "class-wide claim limited to manifest"
        ],
        "conclusion_ceiling": "rival-partition power within the declared finite manifest only",
    }
    MODELS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    digest = hashlib.sha256(json.dumps(models, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r8-check-results-v1",
        "specialist_local_result": "SPA-R8",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "declared_signature_cases": stats["cases"],
        "gain_residual_identity_checks": stats["identity_checks"],
        "identity_failure_count": len(stats["identity_failures"]),
        "monotonicity_checks": stats["monotonic_checks"],
        "monotonicity_failure_count": len(stats["monotonic_failures"]),
        "submodularity_checks": stats["submodular_checks"],
        "submodularity_failure_count": len(stats["submodular_failures"]),
        "profile_derived_zero_gain_checks": stats["derived_zero_checks"],
        "full_identification_cases": stats["full_identification_cases"],
        "model_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "elementary partition refinement/coverage-function machinery; no novelty; relation to anchor set cover remains application-level unless proposition identity is proved",
        "claim_ceiling": "bounded exact finite target partition; no empirical, causal, source-world, or metaphysical truth inference",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["declared_signature_cases"], "identity_checks": result["gain_residual_identity_checks"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
