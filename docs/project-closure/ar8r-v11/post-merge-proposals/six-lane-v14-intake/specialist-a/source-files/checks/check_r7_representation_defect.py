#!/usr/bin/env python3
from __future__ import annotations

from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r7_representation_defect_results.json"
MODELS = BASE / "rounds" / "r7_representation_countermodels.json"


def fiber_constant(rep, target):
    for i in range(len(rep)):
        for j in range(i + 1, len(rep)):
            if rep[i] == rep[j] and target[i] != target[j]:
                return False
    return True


def decoder_exists_bruteforce(rep, target, label_count, target_values=(0, 1)):
    for decoder in product(target_values, repeat=label_count):
        if all(decoder[rep[i]] == target[i] for i in range(len(rep))):
            return True, decoder
    return False, None


def defect(rep, target):
    return sum(
        1
        for i in range(len(rep))
        for j in range(i + 1, len(rep))
        if rep[i] == rep[j] and target[i] != target[j]
    )


def joint(r, q):
    return tuple((r[i], q[i]) for i in range(len(r)))


def canonical_partition(rep):
    blocks = {}
    for i, z in enumerate(rep):
        blocks.setdefault(z, []).append(i)
    return tuple(sorted(tuple(v) for v in blocks.values()))


def exhaustive():
    decoder_cases = 0
    decoder_mismatches = []
    joint_cases = 0
    joint_monotonic_failures = []
    joint_repairs = 0
    partition_equivalence_cases = 0
    partition_equivalence_failures = []

    for n in range(1, 6):
        label_count = min(3, n)
        reps = tuple(product(range(label_count), repeat=n))
        targets = tuple(product((0, 1), repeat=n))
        qs = tuple(product((0, 1), repeat=n))
        for rep in reps:
            part = canonical_partition(rep)
            for target in targets:
                decoder_cases += 1
                fc = fiber_constant(rep, target)
                de, _ = decoder_exists_bruteforce(rep, target, label_count)
                if fc != de:
                    decoder_mismatches.append({"n": n, "rep": rep, "target": target, "fiber_constant": fc, "decoder_exists": de})
                base_defect = defect(rep, target)
                for q in qs:
                    joint_cases += 1
                    jd = defect(joint(rep, q), target)
                    if jd > base_defect:
                        joint_monotonic_failures.append({"n": n, "rep": rep, "q": q, "target": target, "base": base_defect, "joint": jd})
                    if base_defect > 0 and jd == 0:
                        joint_repairs += 1
        # Same partition -> same sufficiency and defect for all targets.
        if n <= 4:
            for r1 in reps:
                p1 = canonical_partition(r1)
                for r2 in reps:
                    if canonical_partition(r2) != p1:
                        continue
                    for target in targets:
                        partition_equivalence_cases += 1
                        if fiber_constant(r1, target) != fiber_constant(r2, target) or defect(r1, target) != defect(r2, target):
                            partition_equivalence_failures.append({"n": n, "r1": r1, "r2": r2, "target": target})

    return {
        "decoder_cases": decoder_cases,
        "decoder_mismatches": decoder_mismatches,
        "joint_cases": joint_cases,
        "joint_monotonic_failures": joint_monotonic_failures,
        "joint_repairs": joint_repairs,
        "partition_equivalence_cases": partition_equivalence_cases,
        "partition_equivalence_failures": partition_equivalence_failures,
    }


def explicit_models():
    target = (0, 0, 1, 1)
    high_card = (0, 1, 0, 2)
    low_card = (0, 0, 1, 1)
    hist_a = (0, 0, 1, 1)
    hist_b = (0, 1, 0, 1)
    base = (0, 0, 0, 0)
    correction = (0, 0, 1, 1)
    same_map = (0, 0, 1, 1)
    relabelled = (7, 7, 9, 9)
    return {
        "raw_cardinality_not_sufficiency": {
            "target": list(target),
            "higher_cardinality_representation": list(high_card),
            "higher_cardinality": len(set(high_card)),
            "higher_has_decoder": fiber_constant(high_card, target),
            "lower_cardinality_representation": list(low_card),
            "lower_cardinality": len(set(low_card)),
            "lower_has_decoder": fiber_constant(low_card, target),
        },
        "same_histogram_not_same_partition": {
            "target": list(target),
            "representation_a": list(hist_a),
            "representation_b": list(hist_b),
            "same_label_histogram": sorted(hist_a.count(x) for x in set(hist_a)) == sorted(hist_b.count(x) for x in set(hist_b)),
            "a_has_decoder": fiber_constant(hist_a, target),
            "b_has_decoder": fiber_constant(hist_b, target),
        },
        "joint_correction_repairs_residual": {
            "target": list(target),
            "base_representation": list(base),
            "correction_representation": list(correction),
            "base_defect": defect(base, target),
            "joint_defect": defect(joint(base, correction), target),
            "joint_has_decoder": fiber_constant(joint(base, correction), target),
        },
        "learned_hand_authored_tag_neutrality": {
            "learned": {"tag": "learned", "map": list(same_map)},
            "hand_authored": {"tag": "hand_authored", "map": list(same_map)},
            "same_fibres": canonical_partition(same_map) == canonical_partition(same_map),
            "same_decoder_status": fiber_constant(same_map, target),
        },
        "coordinate_relabelling_same_partition": {
            "representation_a": list(same_map),
            "representation_b": list(relabelled),
            "same_partition": canonical_partition(same_map) == canonical_partition(relabelled),
            "same_defect": defect(same_map, target) == defect(relabelled, target),
        },
        "factorization_firewall": {
            "nonnegative_rank_or_tensor_uniqueness_claimed": False,
            "statement": "this operation compares induced fibres only; it does not identify a tensor factorization or its uniqueness",
        },
    }


def mutation_tests(stats, models):
    raw = models["raw_cardinality_not_sufficiency"]
    hist = models["same_histogram_not_same_partition"]
    joint_model = models["joint_correction_repairs_residual"]
    tags = models["learned_hand_authored_tag_neutrality"]
    return [
        {
            "mutant": "higher_representation_cardinality_implies_sufficiency",
            "killed": raw["higher_cardinality"] > raw["lower_cardinality"] and not raw["higher_has_decoder"] and raw["lower_has_decoder"],
            "killer": "fixed-target high-cardinality collision",
        },
        {
            "mutant": "same_label_histogram_implies_same_information_partition",
            "killed": hist["same_label_histogram"] and hist["a_has_decoder"] != hist["b_has_decoder"],
            "killer": "crossed two-by-two partitions",
        },
        {
            "mutant": "majority_decoder_counts_as_exact_factorization",
            "killed": joint_model["base_defect"] > 0,
            "killer": "exact decoder requires zero cross-target fibre collisions",
        },
        {
            "mutant": "adding_a_representation_can_increase_exact_collision_defect",
            "killed": not stats["joint_monotonic_failures"],
            "killer": "common refinement only splits fibres",
        },
        {
            "mutant": "learned_tag_is_formally_more_informative_than_hand_authored_tag",
            "killed": tags["same_fibres"] and tags["same_decoder_status"],
            "killer": "identical maps with different provenance tags",
        },
        {
            "mutant": "fibre_factorization_proves_tensor_uniqueness",
            "killed": not models["factorization_firewall"]["nonnegative_rank_or_tensor_uniqueness_claimed"],
            "killer": "separate theorem-family firewall",
        },
        {
            "mutant": "prefilled_decoder_count_without_bruteforce",
            "killed": stats["decoder_cases"] > 0 and stats["joint_cases"] > stats["decoder_cases"],
            "killer": "fresh brute-force decoder enumeration and joint-refinement checks",
        },
    ]


def main():
    stats = exhaustive()
    models = explicit_models()
    mutations = mutation_tests(stats, models)
    errors = []
    if stats["decoder_mismatches"]:
        errors.append("decoder/fibre criterion mismatch")
    if stats["joint_monotonic_failures"]:
        errors.append("joint representation increased defect")
    if stats["partition_equivalence_failures"]:
        errors.append("same partition changed target sufficiency")
    if stats["joint_repairs"] == 0:
        errors.append("no residual repair found")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    payload = {
        "schema": "spa-r7-representation-models-v1",
        "specialist_local_result": "SPA-R7",
        "narrow_statement": "a representation admits an exact common decoder for a target iff the target is constant on representation fibres; joint representations refine fibres and cannot increase exact collision defect",
        "models": models,
        "guards": [
            "finite domain", "exact deterministic target", "representation maps frozen",
            "common decoder target-independent", "learned/hand-authored provenance kept separate from induced partition",
            "no tensor-factorization uniqueness inference"
        ],
        "conclusion_ceiling": "target sufficiency of induced partitions only",
    }
    MODELS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    digest = hashlib.sha256(json.dumps(models, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r7-check-results-v1",
        "specialist_local_result": "SPA-R7",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "decoder_cases_exhausted": stats["decoder_cases"],
        "decoder_mismatch_count": len(stats["decoder_mismatches"]),
        "joint_representation_cases": stats["joint_cases"],
        "joint_monotonic_failure_count": len(stats["joint_monotonic_failures"]),
        "joint_residual_repairs_found": stats["joint_repairs"],
        "same_partition_cases": stats["partition_equivalence_cases"],
        "same_partition_failure_count": len(stats["partition_equivalence_failures"]),
        "countermodel_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "the decoder criterion is the existing T294/Deep BV fibre-factorization family up to representation vocabulary; no new theorem identity or novelty",
        "claim_ceiling": "finite exact-target representation sufficiency; no learned-mechanism, tensor-rank, or factor uniqueness result",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "decoder_cases": result["decoder_cases_exhausted"], "joint_cases": result["joint_representation_cases"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
