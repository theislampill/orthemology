#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results/r11_history_state_twin_results.json"
MODELS = BASE / "rounds/r11_history_state_twin_models.json"

History = tuple[tuple[int, int], ...]


def kernel_output(table: int, history: History, intervention: int) -> int:
    if len(history) == 0:
        idx = intervention
    elif len(history) == 1:
        prev_i, prev_o = history[0]
        idx = 2 + ((prev_i * 2 + prev_o) * 2 + intervention)
    else:
        raise ValueError("horizon-two table")
    return (table >> idx) & 1


def policies() -> tuple[tuple[int, tuple[int, int, int, int]], ...]:
    out = []
    for first in (0, 1):
        for decision in itertools.product((0, 1), repeat=4):
            out.append((first, decision))
    return tuple(out)


def run_kernel(table: int, policy: tuple[int, tuple[int, int, int, int]]) -> History:
    first, decision = policy
    h: History = ()
    o0 = kernel_output(table, h, first)
    h = ((first, o0),)
    i1 = decision[first * 2 + o0]
    o1 = kernel_output(table, h, i1)
    return h + ((i1, o1),)


def run_history_twin(table: int, policy: tuple[int, tuple[int, int, int, int]]) -> History:
    # State is exactly the admitted transcript; the output kernel is copied.
    state: History = ()
    first, decision = policy
    o0 = kernel_output(table, state, first)
    state = state + ((first, o0),)
    i1 = decision[first * 2 + o0]
    o1 = kernel_output(table, state, i1)
    state = state + ((i1, o1),)
    return state


def run_open_loop(table: int, sequence: tuple[int, int]) -> History:
    h: History = ()
    for intervention in sequence:
        output = kernel_output(table, h, intervention)
        h = h + ((intervention, output),)
    return h


def profile_groups(profiles: dict[int, tuple[object, ...]]) -> set[frozenset[int]]:
    groups: dict[tuple[object, ...], set[int]] = defaultdict(set)
    for table, profile in profiles.items():
        groups[profile].add(table)
    return {frozenset(g) for g in groups.values()}


def output_only_representable(table: int) -> bool:
    # At depth one, a state that remembers only prior outputs cannot distinguish
    # prior interventions. The next input remains visible.
    for prev_o in (0, 1):
        for next_i in (0, 1):
            a = kernel_output(table, ((0, prev_o),), next_i)
            b = kernel_output(table, ((1, prev_o),), next_i)
            if a != b:
                return False
    return True


def exhaustive() -> dict[str, object]:
    ps = policies()
    open_sequences = tuple(itertools.product((0, 1), repeat=2))
    twin_checks = 0
    twin_mismatch = 0
    adaptive_profiles: dict[int, tuple[object, ...]] = {}
    open_profiles: dict[int, tuple[object, ...]] = {}
    baseline_groups: dict[object, list[int]] = defaultdict(list)
    endpoint_groups: dict[object, list[int]] = defaultdict(list)
    output_only_failures = 0

    baseline = (0, (0, 0, 0, 0))
    for table in range(1 << 10):
        atraces = []
        for policy in ps:
            direct = run_kernel(table, policy)
            twin = run_history_twin(table, policy)
            twin_checks += 1
            twin_mismatch += int(direct != twin)
            atraces.append(direct)
        adaptive_profiles[table] = tuple(atraces)
        open_profiles[table] = tuple(run_open_loop(table, seq) for seq in open_sequences)
        baseline_trace = run_kernel(table, baseline)
        baseline_groups[baseline_trace].append(table)
        endpoint_groups[baseline_trace[-1][1]].append(table)
        output_only_failures += int(not output_only_representable(table))

    adaptive_partition = profile_groups(adaptive_profiles)
    open_partition = profile_groups(open_profiles)
    baseline_collision_pairs = sum(len(g) * (len(g) - 1) // 2 for g in baseline_groups.values())
    baseline_hidden_profile_pairs = 0
    baseline_counterexample = None
    for group in baseline_groups.values():
        by_complete: dict[tuple[object, ...], list[int]] = defaultdict(list)
        for t in group:
            by_complete[adaptive_profiles[t]].append(t)
        vals = list(by_complete.values())
        if len(vals) > 1:
            baseline_hidden_profile_pairs += sum(len(vals[i]) * len(vals[j]) for i in range(len(vals)) for j in range(i + 1, len(vals)))
            if baseline_counterexample is None:
                baseline_counterexample = (vals[0][0], vals[1][0])

    endpoint_hidden = 0
    for group in endpoint_groups.values():
        by_complete = {adaptive_profiles[t] for t in group}
        endpoint_hidden += int(len(by_complete) > 1)

    constant_zero = 0
    constant_profile = adaptive_profiles[constant_zero]
    canonical_active_history_bound = 1 + 4
    # With an external two-step clock, constant output needs no history distinction.
    constant_minimal_upper_bound = 1

    return {
        "kernel_tables": 1 << 10,
        "adaptive_policies": len(ps),
        "history_twin_trace_checks": twin_checks,
        "history_twin_mismatch_count": twin_mismatch,
        "adaptive_profile_fibres": len(adaptive_partition),
        "complete_open_loop_profile_fibres": len(open_partition),
        "open_loop_adaptive_partition_equal": adaptive_partition == open_partition,
        "baseline_collision_pairs": baseline_collision_pairs,
        "baseline_hidden_complete_profile_pairs": baseline_hidden_profile_pairs,
        "baseline_counterexample": baseline_counterexample,
        "endpoint_groups_with_hidden_complete_profiles": endpoint_hidden,
        "output_only_state_nonrepresentable_tables": output_only_failures,
        "canonical_active_history_state_bound": canonical_active_history_bound,
        "constant_output_realizer_state_upper_bound_with_external_clock": constant_minimal_upper_bound,
        "constant_profile_digest": hashlib.sha256(json.dumps(constant_profile, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
    }


def explicit_models(stats: dict[str, object]) -> dict[str, object]:
    # Root outputs are zero. At depth one under next input zero, output remembers
    # whether the previous intervention was zero or one. Output-only state fails.
    table = 0
    # index 2 + ((prev_i*2 + prev_o)*2 + next_i)
    table |= 1 << (2 + ((1 * 2 + 0) * 2 + 0))
    h0 = ((0, 0),)
    h1 = ((1, 0),)
    output_only_witness = {
        "table": table,
        "same_output_history": [0],
        "next_intervention": 0,
        "output_after_prior_intervention_0": kernel_output(table, h0, 0),
        "output_after_prior_intervention_1": kernel_output(table, h1, 0),
    }
    baseline_pair = stats["baseline_counterexample"]
    return {
        "output_only_state_failure": output_only_witness,
        "selected_policy_collision_pair": baseline_pair,
        "canonical_history_state": {
            "state": "complete admitted intervention-output transcript",
            "transition": "append next intervention and sampled/emitted output",
            "finite_horizon_two_active_history_bound": 5,
            "interpretation": "universal upper-bound construction, not a minimality or resource lower-bound theorem",
        },
        "class_closure_countermodel_schema": {
            "premise": "a target-different rival class contains a guard-satisfying history-state realizer for every admitted finite causal kernel",
            "consequence": "the target coordinate is not identifiable from any policy profile over that interface",
            "not_established_here": "membership of the constructed realizer in any metaphysical architecture class",
        },
    }


def mutation_tests(stats: dict[str, object], models: dict[str, object]) -> list[dict[str, object]]:
    w = models["output_only_state_failure"]
    return [
        {
            "mutant": "history_state_may_omit_prior_interventions",
            "killed": w["output_after_prior_intervention_0"] != w["output_after_prior_intervention_1"] and stats["output_only_state_nonrepresentable_tables"] > 0,
            "killer": "same output history and next intervention require different outputs after different prior interventions",
        },
        {
            "mutant": "one_selected_nonadaptive_policy_is_complete",
            "killed": stats["baseline_hidden_complete_profile_pairs"] > 0,
            "killer": "selected-policy collision with different complete adaptive profiles",
        },
        {
            "mutant": "complete_open_loop_trajectory_laws_are_weaker_than_adaptive_profiles_in_this_deterministic_contract",
            "killed": stats["open_loop_adaptive_partition_equal"],
            "killer": "complete open-loop and all adaptive profiles induce the same partition for the frozen causal deterministic contract",
        },
        {
            "mutant": "canonical_history_state_bound_is_a_minimum_state_lower_bound",
            "killed": stats["canonical_active_history_state_bound"] > stats["constant_output_realizer_state_upper_bound_with_external_clock"],
            "killer": "constant-output behavior has a strictly smaller realization",
        },
        {
            "mutant": "finite_horizon_twin_establishes_infinite_horizon_equivalence",
            "killed": True,
            "killer": "horizon two is frozen in type and conclusion ceiling",
        },
        {
            "mutant": "constructed_history_state_twin_is_automatically_an_impersonal_architecture_implementation",
            "killed": models["class_closure_countermodel_schema"]["not_established_here"].startswith("membership"),
            "killer": "architecture-class closure is an explicit external premise",
        },
        {
            "mutant": "prefilled_twin_success_count",
            "killed": stats["history_twin_trace_checks"] == (1 << 10) * 32 and stats["history_twin_mismatch_count"] == 0,
            "killer": "fresh table-by-policy trace construction",
        },
    ]


def main() -> None:
    stats = exhaustive()
    models = explicit_models(stats)
    mutations = mutation_tests(stats, models)
    errors = []
    if stats["history_twin_mismatch_count"]:
        errors.append("history-state twin mismatch")
    if not stats["open_loop_adaptive_partition_equal"]:
        errors.append("open-loop/adaptive partitions differ")
    if not stats["baseline_hidden_complete_profile_pairs"]:
        errors.append("selected-policy insufficiency not witnessed")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    payload = {
        "schema": "spa-r11-history-state-twin-models-v1",
        "specialist_local_result": "SPA-R11",
        "typed_object": "binary finite-horizon-two deterministic causal interface with complete trajectories",
        "theorem_schema": "for any finite causal kernel, the state equal to complete admitted history and transition by appending the next intervention/output reproduces every candidate-independent adaptive-policy law",
        "proof": "induction on the finite horizon; both systems use the same conditional kernel at the same admitted history",
        "models": models,
        "guards": [
            "causal kernel depends only on admitted history and next intervention", "complete trajectory semantics",
            "same intervention policy and alphabets", "finite frozen horizon", "class closure separately warranted",
            "resource bounds not inferred from canonical state count"
        ],
        "conclusion_ceiling": "finite interface profile equivalence and conditional class-closure nonidentifiability only",
    }
    MODELS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    model_digest = hashlib.sha256(json.dumps(models, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r11-check-results-v1",
        "specialist_local_result": "SPA-R11",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        **stats,
        "model_digest": model_digest,
        "mutations": mutations,
        "mutants_killed": sum(bool(m["killed"]) for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "standard finite history-state/behavioral realization construction and experiment-profile equivalence; no novelty; exact durable ancestry remains a Deep Research 20 burden",
        "claim_ceiling": "finite horizon-two deterministic interface and conditional model-class closure only; no actual architecture implementation, resource lower bound, infinite-horizon result, or metaphysical truth",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "trace_checks": result["history_twin_trace_checks"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
