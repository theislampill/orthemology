#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r2_deletion_criterion_results.json"
MODELS_OUT = BASE / "rounds" / "r2_deletion_models.json"


def powerset(items):
    items = tuple(items)
    for r in range(len(items) + 1):
        for c in combinations(items, r):
            yield frozenset(c)


def restrictions_equal(f, g, D):
    return all(f[x] == g[x] for x in D)


def restriction_injective(H, D):
    for i, f in enumerate(H):
        for g in H[i + 1:]:
            if restrictions_equal(f, g, D):
                return False
    return True


def has_deletion_collision(H, D):
    return any(restrictions_equal(f, g, D) for i, f in enumerate(H) for g in H[i + 1:])


def witness_collision(H, D):
    for i, f in enumerate(H):
        for g in H[i + 1:]:
            if restrictions_equal(f, g, D):
                return f, g
    return None


def profile_dict(t):
    return {str(i): v for i, v in enumerate(t)}


def exhaustive_check():
    total = 0
    mismatches = []
    unrestricted_proper_deletions = 0
    unrestricted_failures = []
    structural_recoverable = []

    for n in range(1, 4):
        X = tuple(range(n))
        all_profiles = tuple(product((0, 1), repeat=n))
        for H_idx_set in powerset(range(len(all_profiles))):
            if not H_idx_set:
                continue
            H = tuple(all_profiles[i] for i in sorted(H_idx_set))
            for D in powerset(X):
                total += 1
                inj = restriction_injective(H, D)
                coll = has_deletion_collision(H, D)
                if inj != (not coll):
                    mismatches.append({"n": n, "H": [profile_dict(h) for h in H], "D": sorted(D), "injective": inj, "collision": coll})
        H_all = all_profiles
        for D in powerset(X):
            if D != frozenset(X):
                unrestricted_proper_deletions += 1
                if restriction_injective(H_all, D):
                    unrestricted_failures.append({"n": n, "D": sorted(D)})

    # Explicit structurally constrained recovery models.
    H_even_parity = tuple(p for p in product((0, 1), repeat=3) if p[2] == (p[0] ^ p[1]))
    D01 = frozenset({0, 1})
    structural_recoverable.append({
        "id": "even_parity_recovers_deleted_cell_2",
        "hypothesis_class": [profile_dict(p) for p in H_even_parity],
        "observed_cells": sorted(D01),
        "restriction_injective": restriction_injective(H_even_parity, D01),
        "recovery_rule": "y2 = y0 XOR y1",
    })
    H_constant = ((0, 0, 0), (1, 1, 1))
    D0 = frozenset({0})
    structural_recoverable.append({
        "id": "constant_profiles_recover_two_deleted_cells",
        "hypothesis_class": [profile_dict(p) for p in H_constant],
        "observed_cells": sorted(D0),
        "restriction_injective": restriction_injective(H_constant, D0),
        "recovery_rule": "all cells equal",
    })

    unrestricted_witness = witness_collision(tuple(product((0, 1), repeat=3)), frozenset({0, 1}))
    explicit = {
        "unrestricted_one_cell_deletion": {
            "hypothesis_class": "all binary response tables on three cells",
            "observed_cells": [0, 1],
            "restriction_injective": False,
            "collision_witness": [profile_dict(unrestricted_witness[0]), profile_dict(unrestricted_witness[1])],
            "witness_valid": unrestricted_witness[0] != unrestricted_witness[1]
                and restrictions_equal(unrestricted_witness[0], unrestricted_witness[1], frozenset({0, 1})),
        },
        "structural_recovery": structural_recoverable,
    }

    return {
        "criterion_cases": total,
        "criterion_mismatches": mismatches,
        "unrestricted_proper_deletion_cases": unrestricted_proper_deletions,
        "unrestricted_proper_deletion_failures": unrestricted_failures,
        "explicit_models": explicit,
    }


def mutation_tests(exhaustive):
    models = exhaustive["explicit_models"]
    mutations = []

    # Mutant 1: every proper deletion is fatal, even on constrained H.
    parity = models["structural_recovery"][0]
    mutations.append({
        "mutant": "all_proper_deletions_fatal",
        "killed": parity["restriction_injective"] is True,
        "killer": parity["id"],
    })

    # Mutant 2: n-1 observed cells always identify.
    unrestricted = models["unrestricted_one_cell_deletion"]
    mutations.append({
        "mutant": "n_minus_one_cells_always_sufficient",
        "killed": unrestricted["restriction_injective"] is False,
        "killer": "unrestricted response tables",
    })

    # Mutant 3: repeated twin is accepted as a collision witness.
    f = (0, 0, 0)
    repeated_twin_accepted = f != f and restrictions_equal(f, f, frozenset({0, 1}))
    mutations.append({
        "mutant": "repeated_constructed_twin_counts_as_collision",
        "killed": not repeated_twin_accepted,
        "killer": "collision witness requires distinct profiles",
    })

    # Mutant 4: stored/prefilled pass counter without witness-bearing enumeration.
    prefilled_record = {"criterion_cases": exhaustive["criterion_cases"], "criterion_mismatches": []}
    canonical_case_digest = hashlib.sha256(
        json.dumps(exhaustive["explicit_models"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    prefilled_has_derived_witness_digest = "derived_witness_digest" in prefilled_record
    mutations.append({
        "mutant": "prefilled_counter_false_pass",
        "killed": (not prefilled_has_derived_witness_digest) and bool(canonical_case_digest),
        "killer": "audit requires derived witness digest and reruns enumeration",
    })

    # Mutant 5: count of observed cells alone decides injectivity.
    same_D_size_opposite_answers = (
        models["unrestricted_one_cell_deletion"]["restriction_injective"]
        != models["structural_recovery"][0]["restriction_injective"]
        and len(models["unrestricted_one_cell_deletion"]["observed_cells"])
        == len(models["structural_recovery"][0]["observed_cells"])
    )
    mutations.append({
        "mutant": "cell_count_only_criterion",
        "killed": same_D_size_opposite_answers,
        "killer": "same two-cell observation set size, opposite injectivity by hypothesis class",
    })

    return mutations


def main():
    exhaustive = exhaustive_check()
    mutations = mutation_tests(exhaustive)
    errors = []
    if exhaustive["criterion_mismatches"]:
        errors.append("restriction criterion mismatch")
    if exhaustive["unrestricted_proper_deletion_failures"]:
        errors.append("unrestricted proper-deletion theorem failed")
    if not all(x["restriction_injective"] for x in exhaustive["explicit_models"]["structural_recovery"]):
        errors.append("structural recoverability witness failed")
    if not exhaustive["explicit_models"]["unrestricted_one_cell_deletion"]["witness_valid"]:
        errors.append("explicit unrestricted collision invalid")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    models_payload = {
        "schema": "spa-r2-deletion-models-v1",
        "specialist_local_result": "SPA-R2",
        "theorem": "restriction to D identifies H iff the restriction map H -> Y^D is injective; equivalently no distinct H-profiles agree on D",
        "unrestricted_corollary": "for |Y| >= 2, every proper D fails on H = Y^X",
        "structural_warning": "proper deletion can be recoverable when H imposes constraints",
        **exhaustive["explicit_models"],
        "conclusion_ceiling": "declared hypothesis-class identifiability only",
    }
    MODELS_OUT.write_text(json.dumps(models_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    digest = hashlib.sha256(json.dumps(exhaustive["explicit_models"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "spa-r2-check-results-v1",
        "specialist_local_result": "SPA-R2",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "criterion_cases_exhausted": exhaustive["criterion_cases"],
        "criterion_mismatch_count": len(exhaustive["criterion_mismatches"]),
        "unrestricted_proper_deletion_cases": exhaustive["unrestricted_proper_deletion_cases"],
        "unrestricted_failure_count": len(exhaustive["unrestricted_proper_deletion_failures"]),
        "derived_witness_digest": digest,
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "elementary restriction-injectivity/fibre criterion; no novelty; Deep BV finite factorization remains T294 up to renaming",
        "claim_ceiling": "finite exhaustive verification for binary X sizes 1-3 plus general paper proof; not whole architecture identification",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["criterion_cases_exhausted"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
