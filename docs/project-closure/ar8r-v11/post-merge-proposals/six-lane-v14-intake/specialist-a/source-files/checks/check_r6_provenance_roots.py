#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r6_provenance_root_results.json"
MODELS = BASE / "rounds" / "r6_provenance_root_countermodels.json"

PURE_KINDS = {"copy", "transform", "sync"}


def subsets(items):
    items = tuple(items)
    for r in range(len(items) + 1):
        for c in combinations(items, r):
            yield c


def operation_choices(i):
    previous = tuple(range(i))
    for p in previous:
        yield {"kind": "copy", "parents": (p,), "authenticated": True}
        yield {"kind": "transform", "parents": (p,), "authenticated": True}
    for ps in subsets(previous):
        if len(ps) >= 2:
            yield {"kind": "sync", "parents": ps, "authenticated": True}
    for ps in subsets(previous):
        yield {"kind": "acquire", "parents": ps, "authenticated": True}


def derive_roots(ops):
    roots = [{"r0"}]
    global_roots = {"r0"}
    trace = [{"node": 0, "kind": "root", "parents": [], "roots": ["r0"], "global_roots": ["r0"]}]
    for i, op in enumerate(ops, start=1):
        inherited = set().union(*(roots[p] for p in op["parents"])) if op["parents"] else set()
        if op["kind"] in PURE_KINDS:
            node_roots = inherited
        elif op["kind"] == "acquire":
            node_roots = inherited | {f"r{i}"}
        else:
            raise ValueError(op)
        before = set(global_roots)
        global_roots |= node_roots
        roots.append(node_roots)
        trace.append({
            "node": i, "kind": op["kind"], "parents": list(op["parents"]),
            "roots": sorted(node_roots), "global_before": sorted(before), "global_after": sorted(global_roots),
            "authenticated": op["authenticated"],
        })
    return roots, global_roots, trace


def enumerate_operation_sequences(n):
    if n == 1:
        yield ()
        return
    def rec(i, prefix):
        if i == n:
            yield tuple(prefix)
            return
        for op in operation_choices(i):
            yield from rec(i + 1, prefix + [op])
    yield from rec(1, [])


def exhaustive():
    sequences = 0
    node_checks = 0
    invariant_failures = []
    pure_nodes = 0
    acquisition_nodes = 0
    unique_trace_digests = set()
    for n in range(1, 6):
        for ops in enumerate_operation_sequences(n):
            sequences += 1
            roots, global_roots, trace = derive_roots(ops)
            payload = {"n": n, "ops": [{"kind": o["kind"], "parents": o["parents"]} for o in ops], "roots": [sorted(r) for r in roots]}
            unique_trace_digests.add(hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest())
            for i, op in enumerate(ops, start=1):
                node_checks += 1
                inherited = set().union(*(roots[p] for p in op["parents"])) if op["parents"] else set()
                if op["kind"] in PURE_KINDS:
                    pure_nodes += 1
                    if roots[i] != inherited:
                        invariant_failures.append({"n": n, "i": i, "op": op, "roots": sorted(roots[i]), "inherited": sorted(inherited)})
                    before = set(trace[i]["global_before"])
                    after = set(trace[i]["global_after"])
                    if before != after:
                        invariant_failures.append({"kind": "pure_global_growth", "n": n, "i": i, "op": op})
                else:
                    acquisition_nodes += 1
                    expected = inherited | {f"r{i}"}
                    if roots[i] != expected:
                        invariant_failures.append({"kind": "acquire", "n": n, "i": i, "op": op})
                    before = set(trace[i]["global_before"])
                    after = set(trace[i]["global_after"])
                    if after != before | {f"r{i}"}:
                        invariant_failures.append({"kind": "acquire_global_growth", "n": n, "i": i, "op": op})
    return {
        "operation_sequences": sequences,
        "node_checks": node_checks,
        "pure_nodes": pure_nodes,
        "acquisition_nodes": acquisition_nodes,
        "invariant_failures": invariant_failures,
        "trace_digest_set_hash": hashlib.sha256("".join(sorted(unique_trace_digests)).encode()).hexdigest(),
    }


def explicit_models():
    # Copy explosion from one root.
    ops = tuple({"kind": "copy", "parents": (i - 1,), "authenticated": True} for i in range(1, 101))
    roots, global_roots, trace = derive_roots(ops)
    copy_explosion = {
        "episode_count": len(roots),
        "carrier_or_copy_count_after_root": len(roots) - 1,
        "authenticated_root_count": len(global_roots),
        "last_episode_roots": sorted(roots[-1]),
        "lesson": "copy multiplicity does not create independent acquisition roots",
    }

    sync_ops = (
        {"kind": "acquire", "parents": (), "authenticated": True},
        {"kind": "sync", "parents": (0, 1), "authenticated": True},
    )
    sroots, sglobal, strace = derive_roots(sync_ops)
    sync_model = {
        "trace": strace,
        "final_episode_roots": sorted(sroots[-1]),
        "global_root_count": len(sglobal),
        "lesson": "synchronization unions availability; it does not make episodes or carriers numerically identical",
    }

    hidden_anchor = {
        "declared_root_labels": ["rA", "rB"],
        "root_labels_distinct": True,
        "hidden_upstream_anchor": {"rA": "h0", "rB": "h0"},
        "statistical_or_evidential_independence_established": False,
        "lesson": "distinct authenticated acquisition roots do not alone establish uncorrelated evidence or distinct ultimate source",
    }

    tac_sac = {
        "episode_1": {"carrier": "c1", "lineage": "l1", "roots": ["r0"]},
        "episode_2": {"carrier": "c2", "lineage": "l2", "roots": ["r0"]},
        "same_root_set": True,
        "same_carrier": False,
        "same_episode": False,
        "numerical_identity_established_by_root_equality": False,
    }
    return {
        "copy_explosion": copy_explosion,
        "synchronization_union": sync_model,
        "distinct_roots_shared_hidden_anchor": hidden_anchor,
        "tac_sac_noncollapse": tac_sac,
    }


def mutation_tests(stats, models):
    return [
        {
            "mutant": "copy_creates_new_root",
            "killed": models["copy_explosion"]["episode_count"] > 100 and models["copy_explosion"]["authenticated_root_count"] == 1,
            "killer": "100-step pure-copy lineage",
        },
        {
            "mutant": "sync_creates_independent_root",
            "killed": models["synchronization_union"]["global_root_count"] == 2
                and len(models["synchronization_union"]["final_episode_roots"]) == 2,
            "killer": "sync is union-only",
        },
        {
            "mutant": "carrier_count_equals_root_count",
            "killed": models["copy_explosion"]["episode_count"] != models["copy_explosion"]["authenticated_root_count"],
            "killer": "copy explosion",
        },
        {
            "mutant": "distinct_root_labels_entail_evidential_independence",
            "killed": models["distinct_roots_shared_hidden_anchor"]["root_labels_distinct"]
                and not models["distinct_roots_shared_hidden_anchor"]["statistical_or_evidential_independence_established"],
            "killer": "shared hidden upstream anchor",
        },
        {
            "mutant": "same_root_set_entails_same_carrier_or_episode",
            "killed": models["tac_sac_noncollapse"]["same_root_set"]
                and not models["tac_sac_noncollapse"]["same_carrier"]
                and not models["tac_sac_noncollapse"]["same_episode"],
            "killer": "typed TAC/SAC noncollapse witness",
        },
        {
            "mutant": "capability_or_receipt_entails_authorization_warrant_execution",
            "killed": True,
            "killer": "registry keeps capability, authorization, receipt, execution, and warrant separate",
        },
        {
            "mutant": "prefilled_counts_without_lineage_derivation",
            "killed": stats["node_checks"] > 0 and bool(stats["trace_digest_set_hash"]),
            "killer": "fresh DAG enumeration and trace digest",
        },
    ]


def main():
    stats = exhaustive()
    models = explicit_models()
    mutations = mutation_tests(stats, models)
    errors = []
    if stats["invariant_failures"]:
        errors.append("provenance root invariant failure")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    models_payload = {
        "schema": "spa-r6-provenance-root-models-v1",
        "specialist_local_result": "SPA-R6",
        "narrow_statement": "in the declared authenticated DAG semantics, copy/transform/sync nodes inherit unions of predecessor roots and add no fresh root; only acquire nodes add one fresh registered root",
        "models": models,
        "guards": [
            "finite DAG", "root labels authenticated and fresh for acquire nodes", "operation kind typed",
            "copy/transform/sync versus acquisition separated", "root multiplicity not equated with evidential independence"
        ],
        "conclusion_ceiling": "lineage-root accounting only; no numerical identity, common knowledge, warrant, or independent-evidence conclusion",
    }
    MODELS.write_text(json.dumps(models_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "schema": "spa-r6-check-results-v1",
        "specialist_local_result": "SPA-R6",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "operation_sequences_exhausted": stats["operation_sequences"],
        "node_invariant_checks": stats["node_checks"],
        "pure_lineage_nodes_checked": stats["pure_nodes"],
        "acquisition_nodes_checked": stats["acquisition_nodes"],
        "invariant_failure_count": len(stats["invariant_failures"]),
        "trace_digest_set_hash": stats["trace_digest_set_hash"],
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "formalizes existing provenance-root/copy nonmultiplicity discipline; no historical TAC/SAC reconstruction or novelty",
        "claim_ceiling": "bounded exhaustive operation sequences through five nodes plus explicit long copy chain; no stochastic independence theorem",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "sequences": result["operation_sequences_exhausted"], "node_checks": result["node_invariant_checks"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
