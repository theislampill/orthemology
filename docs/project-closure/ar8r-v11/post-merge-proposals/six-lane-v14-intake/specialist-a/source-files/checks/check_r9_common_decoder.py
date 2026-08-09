#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results/r9_common_decoder_results.json"
MODELS = BASE / "rounds/r9_common_decoder_models.json"

ArchMap = tuple[tuple[int, int], ...]  # ((observation,target), ...) per architecture


def fibre_consistent(arches: tuple[ArchMap, ...]) -> bool:
    seen: dict[int, int] = {}
    for arch in arches:
        for obs, target in arch:
            if obs in seen and seen[obs] != target:
                return False
            seen[obs] = target
    return True


def decoder_exists(arches: tuple[ArchMap, ...]) -> bool:
    for decoder in itertools.product((0, 1), repeat=2):
        if all(decoder[obs] == target for arch in arches for obs, target in arch):
            return True
    return False


def local_decoders_exist(arches: tuple[ArchMap, ...]) -> bool:
    return all(decoder_exists((arch,)) for arch in arches)


def output_histogram(arch: ArchMap) -> tuple[int, int]:
    return (sum(target == 0 for _, target in arch), sum(target == 1 for _, target in arch))


def exhaustive() -> dict[str, object]:
    point_maps = []
    for obs in itertools.product((0, 1), repeat=2):
        for target in itertools.product((0, 1), repeat=2):
            point_maps.append(tuple(zip(obs, target)))

    cases = 0
    mismatch = 0
    local_only = 0
    histogram_collision = 0
    architecture_permutation_checks = 0
    architecture_permutation_failures = 0
    counterexamples = []

    for arches in itertools.product(point_maps, repeat=3):
        cases += 1
        condition = fibre_consistent(arches)
        brute = decoder_exists(arches)
        mismatch += int(condition != brute)
        if local_decoders_exist(arches) and not brute:
            local_only += 1
            if len(counterexamples) < 16:
                counterexamples.append(arches)
        if len({output_histogram(a) for a in arches}) == 1 and not brute:
            histogram_collision += 1
        baseline = condition
        for perm in itertools.permutations(range(3)):
            architecture_permutation_checks += 1
            architecture_permutation_failures += int(fibre_consistent(tuple(arches[i] for i in perm)) != baseline)

    return {
        "cases": cases,
        "criterion_mismatch_count": mismatch,
        "local_decoder_but_no_common_decoder_count": local_only,
        "same_target_histogram_but_no_common_decoder_count": histogram_collision,
        "architecture_permutation_checks": architecture_permutation_checks,
        "architecture_permutation_failure_count": architecture_permutation_failures,
        "counterexamples": counterexamples,
    }


def explicit_models() -> dict[str, object]:
    local_only = (
        ((0, 0),),
        ((0, 1),),
        ((1, 0),),
    )
    positive = (
        ((0, 0), (1, 1)),
        ((0, 0),),
        ((1, 1),),
    )
    hidden_architecture_decoder = {
        "description": "a decoder permitted to inspect the architecture tag can return conflicting targets at the same observation; that is not a common decoder",
        "forbidden_decoder": "d(architecture, observation)",
        "required_decoder": "d(observation)",
    }
    return {
        "local_decoders_without_common": local_only,
        "positive_common_decoder": positive,
        "architecture_tag_leak": hidden_architecture_decoder,
    }


def mutation_tests(stats: dict[str, object], models: dict[str, object]) -> list[dict[str, object]]:
    local_only = tuple(tuple(tuple(p) for p in arch) for arch in models["local_decoders_without_common"])
    positive = tuple(tuple(tuple(p) for p in arch) for arch in models["positive_common_decoder"])
    return [
        {
            "mutant": "architecture_specific_decoders_imply_one_common_decoder",
            "killed": local_decoders_exist(local_only) and not decoder_exists(local_only),
            "killer": "cross-architecture same-observation conflicting-target witness",
        },
        {
            "mutant": "same_target_histograms_imply_common_decoder",
            "killed": int(stats["same_target_histogram_but_no_common_decoder_count"]) > 0,
            "killer": "histograms discard observation-target alignment",
        },
        {
            "mutant": "decoder_may_read_architecture_tag",
            "killed": not decoder_exists(local_only),
            "killer": "decoder signature is d(observation), not d(architecture, observation)",
        },
        {
            "mutant": "within_architecture_fibre_constancy_is_enough",
            "killed": local_decoders_exist(local_only) and not fibre_consistent(local_only),
            "killer": "coproduct-domain fibre crosses architecture tags",
        },
        {
            "mutant": "architecture_order_changes_common_decodability",
            "killed": int(stats["architecture_permutation_failure_count"]) == 0 and int(stats["architecture_permutation_checks"]) > 0,
            "killer": "exhaustive architecture-order permutations",
        },
        {
            "mutant": "prefilled_common_decoder_counter",
            "killed": int(stats["cases"]) == 4096 and int(stats["criterion_mismatch_count"]) == 0,
            "killer": "fresh enumeration of all three-architecture two-point binary maps",
        },
        {
            "mutant": "common_decoder_proves_architecture_coordinate",
            "killed": decoder_exists(positive),
            "killer": "the decoder reconstructs only the frozen target, not metaphysical architecture or source truth",
        },
    ]


def main() -> None:
    stats = exhaustive()
    models = explicit_models()
    mutations = mutation_tests(stats, models)
    errors = []
    if stats["criterion_mismatch_count"]:
        errors.append("fibre criterion disagrees with decoder search")
    if stats["architecture_permutation_failure_count"]:
        errors.append("architecture permutation changed result")
    if not stats["local_decoder_but_no_common_decoder_count"]:
        errors.append("local/common decoder separation not witnessed")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    model_payload = {
        "schema": "spa-r9-common-decoder-models-v1",
        "specialist_local_result": "SPA-R9",
        "typed_object": "finite tagged disjoint union of architecture-specific domains with a shared observation alphabet and target alphabet",
        "criterion": "one target-blind decoder d:Y->Q exists iff equal observations anywhere in the tagged union always carry equal targets",
        "construction": "map each observed y to its unique consistent target; choose any default on unobserved y",
        "models": models,
        "guards": [
            "common observation semantics", "one frozen decoder signature", "architecture tag unavailable to decoder",
            "target used for evaluation only", "finite alphabets in executable checker"
        ],
        "conclusion_ceiling": "common reconstruction of the frozen finite target only",
    }
    MODELS.write_text(json.dumps(model_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(json.dumps(models, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r9-check-results-v1",
        "specialist_local_result": "SPA-R9",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "declared_signature_cases": stats["cases"],
        "criterion_mismatch_count": stats["criterion_mismatch_count"],
        "local_decoder_but_no_common_decoder_count": stats["local_decoder_but_no_common_decoder_count"],
        "same_target_histogram_but_no_common_decoder_count": stats["same_target_histogram_but_no_common_decoder_count"],
        "architecture_permutation_checks": stats["architecture_permutation_checks"],
        "architecture_permutation_failure_count": stats["architecture_permutation_failure_count"],
        "model_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(bool(m["killed"]) for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "exact specialization of the existing finite fibre-factorization criterion on a tagged disjoint union; no new theorem identity or novelty",
        "claim_ceiling": "finite common decoder for the frozen target; no actual architecture implementation, source-world transfer, or metaphysical identification",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["declared_signature_cases"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
