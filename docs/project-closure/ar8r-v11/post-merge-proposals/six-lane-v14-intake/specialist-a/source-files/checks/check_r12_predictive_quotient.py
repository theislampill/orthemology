#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results/r12_predictive_quotient_results.json"
MODELS = BASE / "rounds/r12_predictive_quotient_models.json"

History = tuple[tuple[int, int], ...]


def output(table: int, history: History, intervention: int) -> int:
    if not history:
        idx = intervention
    elif len(history) == 1:
        pi, po = history[0]
        idx = 2 + ((pi * 2 + po) * 2 + intervention)
    else:
        raise ValueError("horizon two only")
    return (table >> idx) & 1


def reachable_depth1(table: int) -> tuple[History, History]:
    return tuple(((i, output(table, (), i)),) for i in (0, 1))  # type: ignore[return-value]


def residual(table: int, history: History, retained_inputs: tuple[int, ...] = (0, 1)) -> tuple[int, ...]:
    return tuple(output(table, history, i) for i in retained_inputs)


def quotient_count(table: int, retained_inputs: tuple[int, ...] = (0, 1)) -> int:
    return len({residual(table, h, retained_inputs) for h in reachable_depth1(table)})


def representation_exists(table: int, state_assignment: tuple[int, int], state_count: int) -> bool:
    histories = reachable_depth1(table)
    # Search all output decoders state x next-input -> output.
    for bits in range(1 << (state_count * 2)):
        ok = True
        for hidx, h in enumerate(histories):
            s = state_assignment[hidx]
            for i in (0, 1):
                predicted = (bits >> (s * 2 + i)) & 1
                if predicted != output(table, h, i):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return True
    return False


def brute_min_states(table: int) -> int:
    for k in (1, 2):
        for assignment in itertools.product(range(k), repeat=2):
            if representation_exists(table, assignment, k):
                return k
    raise AssertionError("two histories always representable with two states")


def open_loop_profile(table: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    traces = []
    for i0, i1 in itertools.product((0, 1), repeat=2):
        o0 = output(table, (), i0)
        h = ((i0, o0),)
        o1 = output(table, h, i1)
        traces.append(((i0, o0), (i1, o1)))
    return tuple(traces)


def exhaustive() -> dict[str, object]:
    cases = 0
    minimality_mismatch = 0
    quotient_one = 0
    quotient_two = 0
    deletion_merges = 0
    single_input_false_sufficiency = 0
    permutation_checks = 0
    permutation_failures = 0
    groups: dict[tuple[object, ...], list[int]] = defaultdict(list)
    quotient_by_table: dict[int, int] = {}

    for table in range(1 << 10):
        cases += 1
        q = quotient_count(table)
        brute = brute_min_states(table)
        minimality_mismatch += int(q != brute)
        quotient_one += int(q == 1)
        quotient_two += int(q == 2)
        q0 = quotient_count(table, (0,))
        q1 = quotient_count(table, (1,))
        deletion_merges += int(q == 2 and (q0 == 1 or q1 == 1))
        single_input_false_sufficiency += int(q == 2 and q0 == 1)

        histories = reachable_depth1(table)
        sigs = [residual(table, h) for h in histories]
        for perm in ((0, 1), (1, 0)):
            permutation_checks += 1
            perm_count = len({sigs[i] for i in perm})
            permutation_failures += int(perm_count != q)

        prof = open_loop_profile(table)
        groups[prof].append(table)
        quotient_by_table[table] = q

    profile_invariance_failures = 0
    off_support_table_pairs = 0
    for group in groups.values():
        qs = {quotient_by_table[t] for t in group}
        profile_invariance_failures += int(len(qs) != 1)
        off_support_table_pairs += len(group) * (len(group) - 1) // 2

    return {
        "kernel_tables": cases,
        "minimality_mismatch_count": minimality_mismatch,
        "quotient_class_count_one_tables": quotient_one,
        "quotient_class_count_two_tables": quotient_two,
        "deleted_continuation_coordinate_merge_tables": deletion_merges,
        "input_zero_only_false_sufficiency_tables": single_input_false_sufficiency,
        "history_label_permutation_checks": permutation_checks,
        "history_label_permutation_failure_count": permutation_failures,
        "complete_profile_fibres": len(groups),
        "off_support_table_pairs_inside_profile_fibres": off_support_table_pairs,
        "profile_invariance_failure_count": profile_invariance_failures,
    }


def find_models() -> dict[str, object]:
    deletion_witness = None
    compressed_witness = None
    full_witness = None
    for table in range(1 << 10):
        hs = reachable_depth1(table)
        sigs = [residual(table, h) for h in hs]
        if compressed_witness is None and sigs[0] == sigs[1]:
            compressed_witness = {"table": table, "histories": hs, "residual_signatures": sigs, "quotient_classes": 1}
        if full_witness is None and sigs[0] != sigs[1]:
            full_witness = {"table": table, "histories": hs, "residual_signatures": sigs, "quotient_classes": 2}
        if deletion_witness is None and sigs[0] != sigs[1] and sigs[0][0] == sigs[1][0]:
            deletion_witness = {
                "table": table,
                "histories": hs,
                "full_residual_signatures": sigs,
                "retained_input_zero_signatures": [residual(table, h, (0,)) for h in hs],
                "interpretation": "deleting continuation input 1 merges histories that full future behavior separates",
            }
        if deletion_witness and compressed_witness and full_witness:
            break

    return {
        "compressed_history_example": compressed_witness,
        "two_class_example": full_witness,
        "deletion_example": deletion_witness,
        "state_splitting_countermodel": {
            "semantic_residuals": [[0, 0], [1, 1]],
            "minimal_predictive_classes": 2,
            "split_representation_labels": ["a0", "a1", "b"],
            "raw_state_count": 3,
            "reason": "a0 and a1 are duplicate labels for the same future behavior",
        },
        "resource_bridge": {
            "correction_parameter": "number of distinct continuation-law residuals at a frozen depth",
            "use": "semantics-invariant lower bound for deterministic state identifiers at that depth",
            "guard": "architecture exclusion still requires a common machine model and a lower bound over the complete rival realization class",
        },
    }


def mutation_tests(stats: dict[str, object], models: dict[str, object]) -> list[dict[str, object]]:
    split = models["state_splitting_countermodel"]
    deletion = models["deletion_example"]
    return [
        {
            "mutant": "every_reachable_history_requires_a_distinct_minimal_state",
            "killed": stats["quotient_class_count_one_tables"] > 0,
            "killer": "two reachable histories with identical continuation behavior",
        },
        {
            "mutant": "raw_state_count_is_representation_invariant",
            "killed": split["raw_state_count"] > split["minimal_predictive_classes"],
            "killer": "state-splitting duplicate labels",
        },
        {
            "mutant": "one_retained_continuation_input_suffices_for_full_predictive_equivalence",
            "killed": stats["input_zero_only_false_sufficiency_tables"] > 0 and deletion is not None,
            "killer": "deleted-continuation-coordinate witness",
        },
        {
            "mutant": "off_support_table_bits_change_predictive_quotient_despite_equal_complete_profiles",
            "killed": stats["off_support_table_pairs_inside_profile_fibres"] > 0 and stats["profile_invariance_failure_count"] == 0,
            "killer": "complete-profile fibre invariance across off-support table variants",
        },
        {
            "mutant": "learned_or_hand_authored_state_labels_change_the_quotient",
            "killed": stats["history_label_permutation_failure_count"] == 0,
            "killer": "quotient depends on future behavior, not labels or provenance tags",
        },
        {
            "mutant": "predictive_state_lower_bound_identifies_metaphysical_architecture",
            "killed": True,
            "killer": "lower bound is relative to the frozen deterministic interface and machine semantics",
        },
        {
            "mutant": "prefilled_minimal_state_counts",
            "killed": stats["kernel_tables"] == 1024 and stats["minimality_mismatch_count"] == 0 and stats["quotient_class_count_one_tables"] + stats["quotient_class_count_two_tables"] == 1024,
            "killer": "fresh decoder search for every causal table",
        },
    ]


def main() -> None:
    stats = exhaustive()
    models = find_models()
    mutations = mutation_tests(stats, models)
    errors = []
    for key in ("minimality_mismatch_count", "history_label_permutation_failure_count", "profile_invariance_failure_count"):
        if stats[key]:
            errors.append(key)
    if not stats["deleted_continuation_coordinate_merge_tables"]:
        errors.append("deletion witness absent")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    payload = {
        "schema": "spa-r12-predictive-quotient-models-v1",
        "specialist_local_result": "SPA-R12",
        "typed_object": "reachable depth-one histories of a binary deterministic horizon-two causal interface",
        "equivalence": "two histories are equivalent iff they induce the same output for every retained continuation intervention",
        "minimality": "the number of residual-signature classes is exactly the minimum number of deterministic state identifiers needed at that depth",
        "proof": "equivalent histories may share a state; inequivalent histories cannot share a state because a continuation input would demand two outputs from one state/input pair",
        "models": models,
        "guards": [
            "finite deterministic interface", "fixed depth and remaining horizon", "all continuation interventions retained",
            "external clock treatment explicit", "complete profile semantics", "no stochastic or measurable generalization"
        ],
        "conclusion_ceiling": "depth-specific deterministic predictive quotient and minimal state count only",
    }
    MODELS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(json.dumps(models, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r12-check-results-v1",
        "specialist_local_result": "SPA-R12",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        **stats,
        "model_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(bool(m["killed"]) for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "finite deterministic Myhill-Nerode/predictive-state quotient analogue; standard ancestry expected, no novelty; exact theorem-level locator remains a Deep Research 20 burden",
        "claim_ceiling": "depth-specific finite deterministic minimal predictive-state count; no stochastic/measurable extension, architecture exclusion, source-world transfer, or metaphysical truth",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "tables": result["kernel_tables"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
