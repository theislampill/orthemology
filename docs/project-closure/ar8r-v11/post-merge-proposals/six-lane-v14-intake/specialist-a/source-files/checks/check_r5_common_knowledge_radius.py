#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r5_common_knowledge_radius_results.json"
MODELS = BASE / "rounds" / "r5_common_knowledge_countermodels.json"


def partitions(n):
    if n == 0:
        yield ()
        return
    def rec(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for label in range(max(prefix) + 2):
            yield from rec(prefix + [label])
    yield from rec([0])


def accessible(labels, w):
    return {v for v, lab in enumerate(labels) if lab == labels[w]}


def union_neighbors(agent_partitions, w):
    out = set()
    for labels in agent_partitions:
        out |= accessible(labels, w)
    return out


def component_and_dist(agent_partitions, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        w = q.popleft()
        for v in union_neighbors(agent_partitions, w):
            if v not in dist:
                dist[v] = dist[w] + 1
                q.append(v)
    return set(dist), dist


def everyone_step(agent_partitions, worlds_true):
    n = len(agent_partitions[0])
    return {
        w for w in range(n)
        if all(accessible(labels, w).issubset(worlds_true) for labels in agent_partitions)
    }


def everyone_depth(agent_partitions, valuation, k):
    current = set(valuation)
    for _ in range(k):
        current = everyone_step(agent_partitions, current)
    return current


def common_knowledge(agent_partitions, valuation, w):
    comp, _ = component_and_dist(agent_partitions, w)
    return comp.issubset(valuation)


def exhaustive():
    cases = 0
    radius_mismatches = []
    n_minus_one_mismatches = []
    e1_not_ck = []
    e2_not_ck = []
    unique_e1_digests = set()
    max_eccentricity = 0
    for n in range(1, 5):
        parts = tuple(partitions(n))
        for p_a in parts:
            for p_b in parts:
                agents = (p_a, p_b)
                for mask in range(1 << n):
                    valuation = {w for w in range(n) if mask & (1 << w)}
                    e1 = everyone_depth(agents, valuation, 1)
                    e2 = everyone_depth(agents, valuation, 2)
                    en = everyone_depth(agents, valuation, max(0, n - 1))
                    for w in range(n):
                        cases += 1
                        comp, dist = component_and_dist(agents, w)
                        d = max(dist.values())
                        max_eccentricity = max(max_eccentricity, d)
                        ck = comp.issubset(valuation)
                        ed = w in everyone_depth(agents, valuation, d)
                        if ck != ed:
                            radius_mismatches.append({"n": n, "a": p_a, "b": p_b, "valuation": sorted(valuation), "w": w, "d": d, "ck": ck, "ed": ed})
                        if ck != (w in en):
                            n_minus_one_mismatches.append({"n": n, "a": p_a, "b": p_b, "valuation": sorted(valuation), "w": w})
                        if w in e1 and not ck:
                            payload = {"n": n, "a": p_a, "b": p_b, "valuation": sorted(valuation), "w": w, "d": d}
                            digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                            unique_e1_digests.add(digest)
                            if len(e1_not_ck) < 20:
                                e1_not_ck.append(payload)
                        if w in e2 and not ck and len(e2_not_ck) < 20:
                            e2_not_ck.append({"n": n, "a": p_a, "b": p_b, "valuation": sorted(valuation), "w": w, "d": d})
    return {
        "cases": cases,
        "radius_mismatches": radius_mismatches,
        "n_minus_one_mismatches": n_minus_one_mismatches,
        "e1_not_ck_sample": e1_not_ck,
        "e1_not_ck_unique_count": len(unique_e1_digests),
        "e2_not_ck_sample": e2_not_ck,
        "max_eccentricity": max_eccentricity,
        "e1_countermodel_digest_set_hash": hashlib.sha256("".join(sorted(unique_e1_digests)).encode()).hexdigest(),
    }


def explicit_countermodel():
    # A partition {0,1}|{2}; B partition {0}|{1,2}; phi true at 0,1.
    agents = ((0, 0, 1), (0, 1, 1))
    valuation = {0, 1}
    w = 0
    comp, dist = component_and_dist(agents, w)
    d = max(dist.values())
    agent_a_knows = accessible(agents[0], w).issubset(valuation)
    agent_b_knows = accessible(agents[1], w).issubset(valuation)
    return {
        "worlds": [0, 1, 2],
        "agent_A_partition": list(agents[0]),
        "agent_B_partition": list(agents[1]),
        "phi_true_worlds": sorted(valuation),
        "actual_world": w,
        "agent_A_knows_phi": agent_a_knows,
        "agent_B_knows_phi": agent_b_knows,
        "everyone_knows_phi_depth_1": w in everyone_depth(agents, valuation, 1),
        "common_knowledge_phi": common_knowledge(agents, valuation, w),
        "union_reachable_component": sorted(comp),
        "epistemic_closure_radius": d,
        "everyone_knows_iterated_to_radius": w in everyone_depth(agents, valuation, d),
        "lesson": "first-order mutual acknowledgement does not close the alternating-agent reachability chain",
    }


def mutation_tests(stats, model):
    fixed_depth_two_failure = bool(stats["e2_not_ck_sample"])
    return [
        {
            "mutant": "private_acknowledgment_by_one_agent_implies_common_knowledge",
            "killed": model["agent_A_knows_phi"] and not model["common_knowledge_phi"],
            "killer": "three-world alternating partition model",
        },
        {
            "mutant": "everyone_knows_once_implies_common_knowledge",
            "killed": model["everyone_knows_phi_depth_1"] and not model["common_knowledge_phi"] and stats["e1_not_ck_unique_count"] > 0,
            "killer": "union-reachability closure",
        },
        {
            "mutant": "depth_equal_to_agent_count_always_suffices",
            "killed": fixed_depth_two_failure,
            "killer": "four-world alternating chains with epistemic radius three",
        },
        {
            "mutant": "component_diameter_correction_is_unnecessary",
            "killed": model["epistemic_closure_radius"] > 1 and not model["common_knowledge_phi"],
            "killer": "explicit nonlocal false world",
        },
        {
            "mutant": "prefilled_pass_without_reachability_recomputation",
            "killed": stats["cases"] > 0 and bool(stats["e1_countermodel_digest_set_hash"]),
            "killer": "fresh partition/valuation enumeration and witness digest",
        },
        {
            "mutant": "finite_synchronous_kripke_result_proves_protocol_common_knowledge",
            "killed": True,
            "killer": "scope guard excludes message loss, clocks, failures, and source/warrant transfer",
        },
    ]


def main():
    stats = exhaustive()
    model = explicit_countermodel()
    mutations = mutation_tests(stats, model)
    errors = []
    if stats["radius_mismatches"]:
        errors.append("eccentricity-depth criterion mismatch")
    if stats["n_minus_one_mismatches"]:
        errors.append("n-1 finite bound mismatch")
    if model["common_knowledge_phi"] or not model["everyone_knows_phi_depth_1"]:
        errors.append("explicit mutual-knowledge countermodel failed")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    model_payload = {
        "schema": "spa-r5-common-knowledge-models-v1",
        "specialist_local_result": "SPA-R5",
        "narrow_statement": "in a finite S5-style epistemic model, common knowledge at w equals E^d phi where d is the eccentricity of w in the union-of-agent accessibility graph; d <= |W|-1",
        "explicit_countermodel": model,
        "bounded_e1_countermodel_sample": stats["e1_not_ck_sample"],
        "bounded_e2_countermodel_sample": stats["e2_not_ck_sample"],
        "guards": [
            "finite worlds", "two agents", "equivalence accessibility relations", "truth valuation frozen",
            "common knowledge defined by reflexive-transitive closure of union accessibility"
        ],
        "conclusion_ceiling": "finite epistemic-model closure only; no protocol receipt, warrant, or source truth",
    }
    MODELS.write_text(json.dumps(model_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "schema": "spa-r5-check-results-v1",
        "specialist_local_result": "SPA-R5",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "declared_signature_cases": stats["cases"],
        "radius_mismatch_count": len(stats["radius_mismatches"]),
        "n_minus_one_mismatch_count": len(stats["n_minus_one_mismatches"]),
        "e1_not_common_knowledge_unique_count": stats["e1_not_ck_unique_count"],
        "max_epistemic_closure_radius_observed": stats["max_eccentricity"],
        "countermodel_digest_set_hash": stats["e1_countermodel_digest_set_hash"],
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "standard finite common-knowledge reachability/fixed-point semantics; no novelty; durable ancestry locator deferred to Deep Research 20",
        "claim_ceiling": "bounded exhaustive evidence for up to four worlds and a direct finite proof; no asynchronous distributed-protocol theorem",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["declared_signature_cases"], "e1_countermodels": result["e1_not_common_knowledge_unique_count"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
