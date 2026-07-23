#!/usr/bin/env python3
"""Pure structured validator for the Task 9 argument map."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "companion" / "DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml"
SOURCE_STATUS_PATH = ROOT / "references" / "source-status.yaml"
MAX_ISSUES = 100

CLAIM_ROLES = {
    "primary-text-verified",
    "secondary-reconstruction",
    "cross-source-synthesis",
    "orthemological-extension",
    "computational-analogy",
    "creed-internal-inference",
}
REFERENCE_ROLES = {
    "primary-text",
    "secondary-scholarship",
    "comparative",
    "rival",
    "lexical-reference",
}
NODE_FIELDS = {
    "id",
    "order",
    "label",
    "scope",
    "premises",
    "inference_type",
    "bridge_status",
    "bridge_premise_refs",
    "conclusion",
    "dependencies",
    "claim_role",
    "source_status_refs",
    "evidence_access_status",
    "reference_roles",
    "strongest_objection",
    "rival_exit",
    "warrant_basis",
}
RIVAL_FAMILIES = {
    "selected-function-naturalism",
    "modal-primitivism",
    "platonism-structural-realism",
    "brute-contingency",
    "aseity-bootstrapping",
    "euthyphro-fittingness",
    "impersonal-ground",
}
WARRANT_BASES = {
    "stated-premises-and-inference",
    "revelation-and-declared-creed-internal-inference",
}
COPIED_CUSTODY_FIELDS = {
    "citation",
    "citation_locator",
    "edition",
    "translation",
    "repository_extraction",
    "locator",
}
SPEECH_CREATED = {
    "SPEECH-BEARER-01",
    "SPEECH-BEARER-02",
    "SPEECH-BEARER-03",
    "SPEECH-BEARER-04",
    "SPEECH-BEARER-07",
}


def _add(issues: list[str], message: str) -> None:
    if len(issues) < MAX_ISSUES:
        issues.append(message)


def _source_rows(registry: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(registry, dict) or not isinstance(registry.get("claims"), list):
        return {}
    return {
        row["id"]: row
        for row in registry["claims"]
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }


def _texts(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_texts(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_texts(item) for item in value)
    return value if isinstance(value, str) else ""


def validate_mapping(data: Any, source_registry: Any) -> list[str]:
    """Return bounded diagnostics for arbitrary already-loaded inputs."""
    issues: list[str] = []
    if not isinstance(data, dict):
        return ["argument map must be a mapping"]
    if data.get("schema") != "orthemology-dynamic-orthability-argument-map-v2":
        _add(issues, "schema must be orthemology-dynamic-orthability-argument-map-v2")
    if data.get("operative_noetic_frame") != "athari-taymiyyan":
        _add(issues, "operative_noetic_frame must declare athari-taymiyyan")

    policy = data.get("cross_framework_policy")
    if not isinstance(policy, dict):
        _add(issues, "cross_framework_policy must be a mapping")
    elif (
        policy.get("meaning") != "dialectical-accessibility-and-rival-routing"
        or policy.get("warrant_role") != "presentation-only"
        or policy.get("objective_criteria_assessable") is not True
        or policy.get("school_label_is_warrant") is not False
        or policy.get("source_identity_is_warrant") is not False
    ):
        _add(
            issues,
            "cross-framework scope must mean dialectical accessibility, not a neutral tribunal",
        )

    wisdom = data.get("common_premise_fittingness_to_wisdom")
    if not isinstance(wisdom, dict) or wisdom.get("status") not in {
        "held",
        "conditional",
        "removed",
    }:
        _add(issues, "common-premise fittingness-to-Wisdom bridge must remain held")

    if data.get("divine_formal_object_policy") != "Allah-is-never-an-internal-formal-object":
        _add(issues, "Allah must never be represented as an internal formal object")

    fitrah = data.get("fitrah_boundary")
    if (
        not isinstance(fitrah, dict)
        or fitrah.get("representation") != "qualitative-defeasible-multidimensional"
        or not isinstance(fitrah.get("not"), list)
        or not {
            "scalar",
            "coordinate",
            "algorithm",
            "guaranteed-attractor",
            "discourse-readable-soul-state",
            "metaortheme",
        }.issubset(set(fitrah.get("not", [])))
    ):
        _add(issues, "fiṭrah must remain qualitative, defeasible, and multidimensional")

    proper = data.get("proper_function_boundary")
    if (
        not isinstance(proper, dict)
        or proper.get("historical_attribution") != "modern-comparative-reconstruction"
        or proper.get("inferential_reach") != "does-not-by-itself-prove-a-Designer"
    ):
        _add(issues, "proper functionalism is modern comparison, not Ibn Taymiyya's theory")

    rabb = data.get("rabb_lexical_crosswalk")
    required_layers = {
        "token": "orthemma",
        "candidate_senses": "orthemes",
        "interpretive_rules": "metaorthemes",
        "context_binding": "metaorthemma",
        "disambiguation": "orthing",
    }
    if not isinstance(rabb, dict):
        _add(issues, "Rabb lexical crosswalk must be a mapping")
    else:
        if rabb.get("lexical_range_semantics") != "candidate-senses-selected-by-context":
            _add(issues, "Rabb lexical range cannot conjunctively entail all senses")
        if rabb.get("theological_reach") != "none-from-etymology-alone":
            _add(issues, "Rabb lexical evidence cannot prove theology or Wisdom")
        layers = rabb.get("layers")
        if not isinstance(layers, dict):
            _add(issues, "Rabb layers must be a mapping")
        else:
            for key, expected in required_layers.items():
                if layers.get(key) != expected:
                    _add(issues, f"Rabb layer {key} must map to {expected}")
        if rabb.get("creaturely_completion") != "remains-dependent-not-self-sufficient":
            _add(issues, "Rabb crosswalk cannot imply creaturely self-sufficiency")

    speech_boundary = data.get("speech_boundary")
    if (
        not isinstance(speech_boundary, dict)
        or speech_boundary.get("capacity_entails_actual_speech") is not False
        or speech_boundary.get("actual_speech_requires")
        != "revelational-school-internal-dependency"
    ):
        _add(issues, "capacity for disclosure must not entail actual divine Speech")

    bearers = data.get("speech_bearers")
    if not isinstance(bearers, list) or len(bearers) != 7:
        _add(issues, "exactly seven Speech bearers are required")
    else:
        ids: set[str] = set()
        for bearer in bearers:
            if not isinstance(bearer, dict):
                _add(issues, "Speech bearer must be a mapping")
                continue
            bearer_id = bearer.get("id")
            if not isinstance(bearer_id, str) or bearer_id in ids:
                _add(issues, "seven Speech bearers require distinct stable ids")
                continue
            ids.add(bearer_id)
            created_status = bearer.get("created_status")
            if bearer_id in SPEECH_CREATED and created_status != "created":
                _add(issues, f"created bearer {bearer_id} must remain created")
            if bearer_id == "SPEECH-BEARER-05" and created_status != "uncreated-divine-attribute-act":
                _add(issues, "Allah's act of speaking must remain distinct")
            if bearer_id == "SPEECH-BEARER-06" and created_status != "uncreated-divine-speech":
                _add(issues, "revealed Arabic wording must remain Allah's Speech")

    routes = data.get("rival_routes")
    if not isinstance(routes, dict):
        for family in sorted(RIVAL_FAMILIES):
            _add(issues, f"missing rival route {family}")
    else:
        for family in sorted(RIVAL_FAMILIES - set(routes)):
            _add(issues, f"missing rival route {family}")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        _add(issues, "nodes must be a non-empty list")
        return issues

    source_rows = _source_rows(source_registry)
    node_ids = {
        node.get("id")
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    claim_ids: set[str] = set()
    for raw_node in nodes:
        if not isinstance(raw_node, dict):
            continue
        raw_premises = raw_node.get("premises")
        if isinstance(raw_premises, list):
            claim_ids.update(
                item["id"]
                for item in raw_premises
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            )
        raw_conclusion = raw_node.get("conclusion")
        if isinstance(raw_conclusion, dict) and isinstance(raw_conclusion.get("id"), str):
            claim_ids.add(raw_conclusion["id"])
    seen: set[str] = set()
    for index, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            _add(issues, f"node {index} must be a mapping")
            continue
        node_id = node.get("id", f"node-{index}")
        for field in sorted(NODE_FIELDS - set(node)):
            _add(issues, f"{node_id}: missing field {field}")
        for field in sorted(COPIED_CUSTODY_FIELDS & set(node)):
            _add(
                issues,
                f"{node_id}: copied source-custody field {field} is prohibited; resolve it from the registry owner",
            )
        if node_id in seen:
            _add(issues, f"duplicate node id {node_id}")
        elif isinstance(node_id, str):
            seen.add(node_id)
        if node.get("order") != index:
            _add(issues, f"{node_id}: order must equal canonical position {index}")
        if not isinstance(node_id, str) or not re.fullmatch(r"ARG-\d{2}", node_id):
            _add(issues, f"{node_id}: id must be stable ARG-NN")

        premises = node.get("premises")
        if not isinstance(premises, list) or not premises:
            _add(issues, f"{node_id}: premises must be a non-empty list")
        else:
            for premise in premises:
                if not isinstance(premise, dict) or not isinstance(premise.get("id"), str) or not isinstance(premise.get("text"), str):
                    _add(issues, f"{node_id}: malformed premise")
        conclusion = node.get("conclusion")
        if not isinstance(conclusion, dict) or not isinstance(conclusion.get("id"), str) or not isinstance(conclusion.get("text"), str):
            _add(issues, f"{node_id}: malformed conclusion")

        dependencies = node.get("dependencies")
        if not isinstance(dependencies, list):
            _add(issues, f"{node_id}: dependencies must be a list")
        else:
            for dependency in dependencies:
                if dependency not in node_ids:
                    _add(issues, f"{node_id}: dangling dependency {dependency}")
                elif dependency == node_id:
                    _add(issues, f"{node_id}: self dependency")
        bridge_refs = node.get("bridge_premise_refs")
        if not isinstance(bridge_refs, list):
            _add(issues, f"{node_id}: bridge_premise_refs must be a list")
        else:
            for bridge_ref in bridge_refs:
                if bridge_ref not in claim_ids:
                    _add(issues, f"{node_id}: dangling bridge_premise_ref {bridge_ref}")

        role = node.get("claim_role")
        if role not in CLAIM_ROLES:
            _add(issues, f"{node_id}: invalid claim_role {role}")
        if index >= 4 and role == "computational-analogy":
            _add(issues, f"{node_id}: upper node cannot use computational-analogy")
        if node.get("warrant_basis") not in WARRANT_BASES:
            _add(issues, f"{node_id}: invalid warrant_basis")
        objection = node.get("strongest_objection")
        if (
            not isinstance(objection, dict)
            or not isinstance(objection.get("id"), str)
            or not isinstance(objection.get("status"), str)
            or not isinstance(objection.get("text"), str)
        ):
            _add(issues, f"{node_id}: strongest_objection must be a typed mapping")
        rival = node.get("rival_exit")
        if (
            not isinstance(rival, dict)
            or not isinstance(rival.get("id"), str)
            or not isinstance(rival.get("disposition"), str)
            or not isinstance(rival.get("joint"), str)
        ):
            _add(issues, f"{node_id}: rival_exit must be a typed mapping")

        refs = node.get("source_status_refs")
        access = node.get("evidence_access_status")
        ref_roles = node.get("reference_roles")
        if not isinstance(refs, list):
            _add(issues, f"{node_id}: source_status_refs must be a list")
            refs = []
        if not isinstance(access, dict):
            _add(issues, f"{node_id}: evidence_access_status must be a mapping")
            access = {}
        if not isinstance(ref_roles, dict):
            _add(issues, f"{node_id}: reference_roles must be a mapping")
            ref_roles = {}
        if set(ref_roles) != set(refs):
            _add(issues, f"{node_id}: reference_roles keys must equal source_status_refs")
        if set(access) != set(refs):
            _add(issues, f"{node_id}: evidence_access_status keys must equal source_status_refs")
        for ref in refs:
            row = source_rows.get(ref)
            if row is None:
                _add(issues, f"{node_id}: unresolved source_status_ref {ref}")
                continue
            if access.get(ref) != row.get("status"):
                _add(issues, f"{node_id}: evidence access drift for {ref}")
            if ref_roles.get(ref) not in REFERENCE_ROLES:
                _add(issues, f"{node_id}: invalid reference role for {ref}")

        text = _texts(node).lower()
        if "gradient exists" in text or "objective differentiable correction gradient" in text:
            _add(issues, f"{node_id}: literal objective gradient is prohibited")
        if "guaranteed to converge" in text or "guaranteed convergence" in text:
            _add(issues, f"{node_id}: guaranteed convergence is prohibited")
        if "created arabic wording" in text:
            _add(issues, f"{node_id}: unsafe created Arabic wording is prohibited")
        if "already personal" in text or "already intelligent" in text:
            _add(issues, f"{node_id}: premise assumes its conclusion")
        if index >= 4 and ("osm-supported" in text or "daee-result" in text or "empirical proof" in text):
            _add(issues, f"{node_id}: upper node cannot be validated by OSM/DAEE")

    by_id = {node.get("id"): node for node in nodes if isinstance(node, dict)}
    norm = by_id.get("ARG-04")
    if isinstance(norm, dict):
        dependencies = norm.get("dependencies")
        bridges = norm.get("bridge_premise_refs")
        if (
            not isinstance(dependencies, list)
            or "ARG-02" not in dependencies
            or not isinstance(bridges, list)
            or "ARG-04-P2" not in bridges
        ):
            _add(issues, "ARG-04: normativity bridge must be separate from empirical learnability")

    actual = by_id.get("ARG-12")
    if isinstance(actual, dict):
        if (
            actual.get("bridge_status") != "revelational"
            or actual.get("scope") != "athari-taymiyyan-operative"
            or actual.get("claim_role") != "creed-internal-inference"
        ):
            _add(issues, "actual Speech requires revelational Athari dependency")
    athari_wisdom = by_id.get("ARG-10")
    if isinstance(athari_wisdom, dict):
        if athari_wisdom.get("bridge_status") not in {
            "held",
            "conditional",
            "held-pending-source-custody",
        }:
            _add(issues, "Athari Wisdom route cannot exceed its verified source custody")
        if (
            not athari_wisdom.get("source_status_refs")
            and "remain held"
            not in str(athari_wisdom.get("conclusion", {}).get("text", "")).lower()
        ):
            _add(issues, "Athari Wisdom source assertion must remain held without verified sources")

    return issues[:MAX_ISSUES]


def main() -> int:
    try:
        data = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8"))
        registry = yaml.safe_load(SOURCE_STATUS_PATH.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"[FAIL] argument map parse: {exc}")
        return 1
    issues = validate_mapping(data, registry)
    if issues:
        for issue in issues:
            print(f"[FAIL] {issue}")
        print(f"Argument-map validation failed: {len(issues)} issue(s)")
        return 1
    print(f"[PASS] structured argument map: {len(data['nodes'])} nodes")
    print("[PASS] source references, roles, and evidence access agree")
    print("[PASS] dialectical, metaphysical, Rabb, fiṭrah, and Speech firewalls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
