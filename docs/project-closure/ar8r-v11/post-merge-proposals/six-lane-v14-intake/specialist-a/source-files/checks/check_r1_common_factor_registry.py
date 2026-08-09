#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import inspect
import itertools
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parents[1]
REG_PATH = BASE / "registry" / "architecture_factor_registry.yaml"
MAP_PATH = BASE / "registry" / "complete_experiment_profile_map.json"
MANIFEST_PATH = BASE / "coverage" / "declared_family_manifest.yaml"
COVERAGE_PATH = BASE / "coverage" / "total_coverage_map.yaml"
SCHEMA_PATH = BASE / "contracts" / "common_intervention_contract.schema.json"
OUT = BASE / "results" / "r1_common_factor_registry_results.json"

FORBIDDEN = {
    "architecture", "target_coordinate", "personal", "impersonal", "plural",
    "intentional_uptake", "one_bearer", "source_world_truth"
}


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def canonical_cell(assignment: dict[str, str]) -> str:
    raw = json.dumps(assignment, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()[:20]


def validate_registry(reg: dict[str, Any], profile_map: dict[str, Any], manifest: dict[str, Any], coverage: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    factors = reg.get("factors", [])
    factor_ids = [f.get("id") for f in factors]
    if len(factor_ids) != len(set(factor_ids)):
        errors.append("duplicate factor id")
    if not factor_ids:
        errors.append("empty factor list")

    for factor in factors:
        values = factor.get("values")
        if not isinstance(values, list) or not values or any(isinstance(v, (dict, list)) for v in values):
            errors.append(f"factor {factor.get('id')} lacks finite atomic values")
        if factor.get("id") == "resource_band" and factor.get("unbounded", False):
            errors.append("finite resource factor marked unbounded")

    expected_arches = set(reg.get("declared_scope", {}).get("architectures", []))
    got_arches = {a.get("id") for a in reg.get("architectures", [])}
    if got_arches != expected_arches:
        errors.append(f"architecture set mismatch expected={sorted(expected_arches)} got={sorted(got_arches)}")

    ftypes = {f["id"]: f["abstract_type"] for f in factors}
    for arch in reg.get("architectures", []):
        fmap = arch.get("factor_map", {})
        if set(fmap) != set(factor_ids):
            errors.append(f"architecture {arch.get('id')} factor map not total")
        for fid, item in fmap.items():
            if fid in ftypes and item.get("implementation_type") != ftypes[fid]:
                errors.append(f"architecture {arch.get('id')} type mismatch at {fid}")
            for key in ("implementation_version", "authorization_guard", "resource_guard", "decoder_contract", "status"):
                if not item.get(key):
                    errors.append(f"architecture {arch.get('id')} missing {key} at {fid}")

    finite = reg.get("contracts", {}).get("finite", {})
    if not finite.get("input_alphabets_finite") or not finite.get("output_alphabets_finite"):
        errors.append("finite alphabet guards not asserted")
    if finite.get("continuous_or_unbounded_fields_allowed"):
        errors.append("finite contract permits continuous/unbounded fields")
    if not isinstance(finite.get("horizon"), int) or finite.get("horizon", 0) < 1:
        errors.append("finite horizon missing")

    measurable = reg.get("contracts", {}).get("measurable", {})
    required_meas = (
        "input_measurable_space_locator", "output_measurable_space_locator",
        "kernel_measurability_receipt", "decoder_measurability_receipt",
        "adaptive_policy_measurability_receipt", "target_blindness_receipt",
        "machine_verified",
    )
    for key in required_meas:
        if key not in measurable:
            errors.append(f"measurable contract missing {key}")
    if measurable.get("status") != "SCHEMA_ONLY_REQUIRES_EXTERNAL_PROOF_RECEIPTS":
        errors.append("measurable contract overclaims status")
    if measurable.get("machine_verified") is not False:
        errors.append("measurable contract must remain unverified")

    decoder = reg.get("common_decoder", {})
    outputs = set(decoder.get("output_fields", []))
    if outputs & FORBIDDEN:
        errors.append(f"decoder leaks forbidden fields {sorted(outputs & FORBIDDEN)}")
    if set(decoder.get("forbidden_input_fields", [])) != FORBIDDEN:
        errors.append("decoder forbidden-field registry drift")

    policy = reg.get("policy_registry", {})
    allowed = set(policy.get("allowed_inputs", []))
    forbidden = set(policy.get("forbidden_inputs", []))
    if allowed & (FORBIDDEN | forbidden):
        errors.append("policy allowed inputs leak forbidden coordinate")
    if not isinstance(policy.get("horizon"), int):
        errors.append("policy horizon missing")

    # Complete factorial map is derived, not trusted by its count field.
    value_lists = [f["values"] for f in factors]
    expected_assignments = [dict(zip(factor_ids, vals)) for vals in itertools.product(*value_lists)]
    expected_cells = {canonical_cell(a): a for a in expected_assignments}
    actual_cells = profile_map.get("cells", [])
    actual_ids = [c.get("cell_id") for c in actual_cells]
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("duplicate cell id")
    actual_by_id = {c.get("cell_id"): c.get("assignment") for c in actual_cells}
    if actual_by_id != expected_cells:
        errors.append("profile map is not the exact complete factorial")
    if profile_map.get("actual_cell_count") != len(actual_cells):
        errors.append("profile map stored count mismatch")
    if profile_map.get("expected_cell_count") != len(expected_cells):
        errors.append("profile map expected count mismatch")

    expected_families = {row["id"] for row in manifest.get("families", [])}
    rows = coverage.get("rows", [])
    covered = [row.get("family_id") for row in rows]
    if set(covered) != expected_families or len(covered) != len(set(covered)):
        errors.append("coverage map is not total and one-to-one over declared manifest")
    valid_buckets = {"included_neutral_factor", "derived_analysis", "external_anchor_required", "outside_declared_neutral_class"}
    for row in rows:
        if row.get("bucket") not in valid_buckets:
            errors.append(f"invalid coverage bucket for {row.get('family_id')}")
        fids = row.get("factor_ids", [])
        if "all" not in fids and not set(fids).issubset(set(factor_ids)):
            errors.append(f"unknown factor in coverage row {row.get('family_id')}")
        if not row.get("reason"):
            errors.append(f"unreasoned coverage row {row.get('family_id')}")

    return errors


def raw_run(arch: str, cell: dict[str, str]) -> dict[str, Any]:
    # The decoder receives no architecture label. Architecture only selects the
    # constructed fixture implementation that emits these common raw fields.
    content_bit = 0 if cell["content"] == "alpha" else 1
    encoded = int(cell["form"] == "encoded")
    conflict = int(cell["target_truth_relation"] == "conflict")
    cut = int(cell["causal_mode"] == "cut")
    fresh = int(cell["challenge_nonce"] == "fresh")
    over = int(cell["resource_band"] == "over_budget")
    stale = int(cell["authority_version"] == "revoked_or_stale")
    copy = int(cell["provenance_operation"] == "pure_copy")

    if arch == "unified_personal":
        action = content_bit ^ conflict ^ (cut & encoded)
        timeout = bool(over and fresh and cut)
        latency = "high" if over or encoded else "low"
    elif arch == "impersonal_powers":
        action = content_bit ^ conflict ^ (fresh & stale)
        timeout = bool(over and fresh)
        latency = "high" if over else "low"
    elif arch == "plural":
        action = content_bit ^ conflict ^ (cut & copy)
        timeout = bool(over and cut)
        latency = "high" if over or cut else "low"
    else:
        raise ValueError(arch)

    trajectory_basis = {
        "a": action,
        "c": cut,
        "f": fresh,
        "o": over,
        "s": stale,
        "x": copy,
        "timeout": timeout,
    }
    return {
        "action_bit": action,
        "certificate_match": not bool(conflict),
        "authority_handling": "reject" if stale else "accept",
        "root_count_bin": "one" if copy else "two_or_more",
        "latency_bin": latency,
        "timeout": timeout,
        "trajectory_payload": trajectory_basis,
        "canonical_content": cell["content"],
    }


def common_decoder(raw: dict[str, Any]) -> dict[str, Any]:
    # This function intentionally has no target/architecture argument.
    payload = json.dumps(raw["trajectory_payload"], sort_keys=True, separators=(",", ":"))
    return {
        "action_bit": raw["action_bit"],
        "certificate_match": raw["certificate_match"],
        "authority_handling": raw["authority_handling"],
        "root_count_bin": raw["root_count_bin"],
        "latency_bin": raw["latency_bin"],
        "timeout": raw["timeout"],
        "trajectory_digest": hashlib.sha256(payload.encode()).hexdigest()[:16],
    }


def simulate_profiles(reg: dict[str, Any], profile_map: dict[str, Any]) -> dict[str, Any]:
    profiles: dict[str, list[dict[str, Any]]] = {}
    for arch in reg["declared_scope"]["architectures"]:
        profiles[arch] = [common_decoder(raw_run(arch, cell["assignment"])) for cell in profile_map["cells"]]
    digests = {
        arch: hashlib.sha256(json.dumps(p, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        for arch, p in profiles.items()
    }
    pairs = []
    arches = sorted(profiles)
    for i, a in enumerate(arches):
        for b in arches[i+1:]:
            differing = sum(x != y for x, y in zip(profiles[a], profiles[b]))
            pairs.append({"a": a, "b": b, "differing_cells": differing, "same_complete_profile": differing == 0})
    return {
        "profile_digests": digests,
        "pairwise_profile_comparison": pairs,
        "interpretation_ceiling": "constructed fixture discrimination only; not architecture implementation or metaphysical identification",
    }


def mutation_tests(reg: dict[str, Any], pmap: dict[str, Any], manifest: dict[str, Any], coverage: dict[str, Any]) -> list[dict[str, Any]]:
    tests: list[tuple[str, Any]] = []

    x = copy.deepcopy(reg)
    del x["architectures"][0]["factor_map"][x["factors"][0]["id"]]
    tests.append(("missing_factor_map", (x, pmap, manifest, coverage)))

    x = copy.deepcopy(reg)
    x["common_decoder"]["output_fields"].append("architecture")
    tests.append(("decoder_target_leak", (x, pmap, manifest, coverage)))

    x = copy.deepcopy(reg)
    for f in x["factors"]:
        if f["id"] == "resource_band":
            f["unbounded"] = True
    tests.append(("unbounded_resource_in_finite_contract", (x, pmap, manifest, coverage)))

    x = copy.deepcopy(reg)
    x["policy_registry"]["allowed_inputs"].append("target_coordinate")
    tests.append(("policy_target_leak", (x, pmap, manifest, coverage)))

    x = copy.deepcopy(reg)
    del x["contracts"]["measurable"]["decoder_measurability_receipt"]
    tests.append(("missing_measurable_decoder_receipt", (x, pmap, manifest, coverage)))

    xmap = copy.deepcopy(pmap)
    xmap["cells"] = xmap["cells"][:-1]
    xmap["actual_cell_count"] -= 1
    tests.append(("deleted_factorial_cell", (reg, xmap, manifest, coverage)))

    xcov = copy.deepcopy(coverage)
    xcov["rows"] = xcov["rows"][:-1]
    tests.append(("incomplete_family_coverage", (reg, pmap, manifest, xcov)))

    results = []
    for name, args in tests:
        errs = validate_registry(*args)
        results.append({"mutant": name, "killed": bool(errs), "errors": errs})
    return results


def main() -> None:
    reg = load_yaml(REG_PATH)
    pmap = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    manifest = load_yaml(MANIFEST_PATH)
    coverage = load_yaml(COVERAGE_PATH)
    errors = validate_registry(reg, pmap, manifest, coverage)

    # Validate a canonical finite contract instance against the public schema.
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    contract_instance = {
        "contract_kind": "finite",
        "target_blind": True,
        "decoder": reg["common_decoder"],
        "policy": reg["policy_registry"],
        "architecture_maps": reg["architectures"],
        "scope_ceiling": reg["declared_scope"]["implementation_ceiling"],
    }
    schema_errors = [e.message for e in Draft202012Validator(schema).iter_errors(contract_instance)]
    errors.extend(f"schema: {x}" for x in schema_errors)

    decoder_source = inspect.getsource(common_decoder)
    decoder_source_leaks = sorted(word for word in FORBIDDEN if word in decoder_source and word not in {"architecture"})
    # The source comment mentions architecture, but the function signature/body cannot access it.
    signature_target_blind = list(inspect.signature(common_decoder).parameters) == ["raw"]
    if not signature_target_blind:
        errors.append("common decoder signature not target-blind")

    mutations = mutation_tests(reg, pmap, manifest, coverage)
    all_killed = all(m["killed"] for m in mutations)
    if not all_killed:
        errors.append("one or more registry mutants survived")

    result = {
        "schema": "spa-r1-check-results-v1",
        "specialist_local_result": "SPA-R1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "derived_counts": {
            "factor_count": len(reg["factors"]),
            "architecture_witness_count": len(reg["architectures"]),
            "factorial_cell_count": len(pmap["cells"]),
            "declared_family_count": len(manifest["families"]),
            "coverage_row_count": len(coverage["rows"]),
        },
        "decoder_signature_target_blind": signature_target_blind,
        "decoder_source_forbidden_tokens_excluding_comment_only_architecture": decoder_source_leaks,
        "constructed_profile_analysis": simulate_profiles(reg, pmap),
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "registry and coverage synthesis only; no theorem origin or novelty; Deep BV finite factorization remains T294 up to renaming",
        "claim_ceiling": "typed finite registry and exhaustive declared-signature fixture; no real architecture implementation; measurable contract unverified",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "counts": result["derived_counts"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
