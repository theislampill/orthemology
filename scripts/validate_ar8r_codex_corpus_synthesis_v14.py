#!/usr/bin/env python3
"""Fail-closed validation for the bounded Codex corpus synthesis V14."""

from __future__ import annotations

from resolve_t20_v6_source import (
    digest_record_view_bytes, digest_record_view_text,
    digest_record_view_is_file,
)


import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
import stat
import urllib.parse

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SYNTHESIS_REL = pathlib.Path(
    "docs/project-closure/ar8r-v11/post-merge-proposals/codex-corpus-synthesis-v14"
)
ALLOWED_RELATIONS = {
    "IDENTICAL_UNDER_TYPED_RENAMING",
    "STRICT_SPECIALIZATION",
    "GUARDED_APPLICATION",
    "SHARED_INVARIANT",
    "SHARED_COUNTERMODEL_ARCHITECTURE",
    "FORMAL_ANALOGUE_ONLY",
    "VOCABULARY_RESEMBLANCE_ONLY",
    "ANTI_UNIFICATION_BOUNDARY",
    "UNRESOLVED",
}
ALLOWED_VERDICTS = {
    "COMMON_THEOREM_ESTABLISHED",
    "GUARDED_MULTI_LANE_APPLICATION_ESTABLISHED",
    "SHARED_INVARIANT_ESTABLISHED",
    "ANTI_UNIFICATION_BOUNDARY_ESTABLISHED",
    "PROMISING_CANDIDATE_AUDIT_INCOMPLETE",
    "FORMAL_ANALOGUE_ONLY",
    "INSUFFICIENT_EVIDENCE",
}
EXPECTED_AUTHORITY = {
    "historical_identity": "NONE",
    "general_novelty": 0,
    "owner_adoption": "PENDING",
    "repository_scientific_adoption": "NONE",
    "source_world_bridge_established": False,
    "empirical_program_run": False,
}
EXPECTED_LEAN_SHA = "73aef790f787ce11c65f4bb080d33b147d210d718862985299b14ce27c4e9efc"
EXPECTED_CHECKER_SHA = "e359606c9f16754ae5864fc5e07003f492ab50437541b5db842b622be4d8cffc"
EXPECTED_RESULTS_SHA = "8f041c4b8b65cee3bee85c06d33ee899df5f711970f1e68837366b87fe01f078"
EXPECTED_INSTANCE_CLASSES = {
    "CLIM-01": "GUARDED_APPLICATION",
    "CLIM-02": "GUARDED_APPLICATION",
    "CLIM-03": "ANTI_UNIFICATION_BOUNDARY",
    "CLIM-04": "SHARED_COUNTERMODEL_ARCHITECTURE",
    "CLIM-05": "STRICT_SPECIALIZATION",
    "CLIM-06": "STRICT_SPECIALIZATION",
    "CLIM-07": "ANTI_UNIFICATION_BOUNDARY",
    "CLIM-08": "FORMAL_ANALOGUE_ONLY",
    "CLIM-09": "GUARDED_APPLICATION",
    "CLIM-10": "ANTI_UNIFICATION_BOUNDARY",
    "CLIM-11": "GUARDED_APPLICATION",
    "CLIM-12": "ANTI_UNIFICATION_BOUNDARY",
}
EXPECTED_RELATION_CLASSES = {
    "REL-01": "STRICT_SPECIALIZATION",
    "REL-02": "SHARED_INVARIANT",
    "REL-03": "GUARDED_APPLICATION",
    "REL-04": "GUARDED_APPLICATION",
    "REL-05": "GUARDED_APPLICATION",
    "REL-06": "STRICT_SPECIALIZATION",
    "REL-07": "ANTI_UNIFICATION_BOUNDARY",
    "REL-08": "STRICT_SPECIALIZATION",
    "REL-09": "FORMAL_ANALOGUE_ONLY",
    "REL-10": "ANTI_UNIFICATION_BOUNDARY",
    "REL-11": "GUARDED_APPLICATION",
    "REL-12": "ANTI_UNIFICATION_BOUNDARY",
    "REL-13": "IDENTICAL_UNDER_TYPED_RENAMING",
    "REL-14": "IDENTICAL_UNDER_TYPED_RENAMING",
}
EXPECTED_CANDIDATE_VERDICTS = {
    "CCS-V14-C1": "COMMON_THEOREM_ESTABLISHED",
    "CCS-V14-C2": "GUARDED_MULTI_LANE_APPLICATION_ESTABLISHED",
    "CCS-V14-C3": "GUARDED_MULTI_LANE_APPLICATION_ESTABLISHED",
    "CCS-V14-C4": "GUARDED_MULTI_LANE_APPLICATION_ESTABLISHED",
    "CCS-V14-C5": "ANTI_UNIFICATION_BOUNDARY_ESTABLISHED",
}
EXPECTED_PROTOCOL_STATUSES = {
    "B1": "BLOCKED_NO_VALIDATED_CONSTRUCT_OR_RUNTIME_MAPPING",
    "B2": "BLOCKED_ON_ACTUAL_IMPLEMENTATION_MAP",
    "B3": "PREREGISTRATION_READY_FOR_REVIEW_DRAFT",
    "B4": "BLOCKED_ON_BECAUSE_OF_UPTAKE_OPERATIONALIZATION",
}
EXPECTED_RESIDUAL_STATUSES = {
    "RGH-01": "TESTABLE_PROPOSAL",
    "RGH-02": "GUARDED_APPLICATION_SUPPORTED",
    "RGH-03": "GUARDED_APPLICATION_SUPPORTED",
    "RGH-04": "COUNTERMODEL_SUPPORTED",
    "RGH-05": "PREREGISTRATION_DRAFT_ONLY",
    "RGH-06": "ANTI_UNIFICATION_BOUNDARY_ESTABLISHED",
}
EXPECTED_SEMANTIC_SOURCE_REFS = {
    "CLIM-03": ["docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R6_PROVENANCE_ROOT_INVARIANT.md"],
    "CLIM-04": [
        "docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R6_PROVENANCE_ROOT_INVARIANT.md",
        "docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml",
    ],
    "CLIM-06": ["docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R4_OBSERVATION_COBUCHI.md"],
    "REL-05": ["docs/project-closure/ar8r-v11/programs/language-translation-and-version-custody.md"],
    "REL-06": ["docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R4_OBSERVATION_COBUCHI.md"],
    "REL-10": ["docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"],
    "REL-11": ["docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"],
}
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace|Temp|Documents|Downloads|Desktop)[\\/]|"
    r"(?<![A-Za-z0-9])/(?:home|Users|root|tmp|var/tmp|private/tmp)/|"
    r"/mnt/data/|sandbox:/|file://|chatgpt\.com/(?:c|g)/|data-message-id|"
    r"screen-threadFlyOut|[\"'`]?browser(?:[_-]|\s)+session(?:[_-]|\s)+"
    r"(?:id|identifier)[\"'`]?\s*[:=]|"
    r"(?:access|refresh)[_-]?token\s*[:=]|"
    r"(?:X-Amz-(?:Signature|Credential|Security-Token)|"
    r"X-Goog-(?:Signature|Credential))\s*=|"
    r"https?://\S*[?&](?:signature|sig|token|expires)=)",
    re.IGNORECASE,
)
JSON_UNICODE_ESCAPE_PATTERN = re.compile(r"\\u([0-9A-Fa-f]{4})")
MAX_SCAN_NORMALIZATION_ROUNDS = 64


def normalized_scan_variants(text: str) -> tuple[list[str], bool]:
    """Return bounded fixed-point variants for privacy and authority scanning.

    The public surface can contain JSON slash/Unicode escapes and nested percent
    encoding.  Scan both the serialized bytes and each decoded representation.
    Inputs that do not stabilize within the bound fail closed.
    """
    variants: list[str] = []
    seen: set[str] = set()
    candidate = text
    for _ in range(MAX_SCAN_NORMALIZATION_ROUNDS + 1):
        if candidate not in seen:
            variants.append(candidate)
            seen.add(candidate)
        transformed = candidate.replace(r"\/", "/")
        transformed = JSON_UNICODE_ESCAPE_PATTERN.sub(
            lambda match: chr(int(match.group(1), 16)), transformed
        )
        transformed = urllib.parse.unquote(transformed)
        if transformed not in seen:
            variants.append(transformed)
            seen.add(transformed)
        if transformed == candidate:
            return variants, False
        candidate = transformed
    return variants, True


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(digest_record_view_bytes(path)).hexdigest()




def load_yaml(path: pathlib.Path, issues: list[str]):
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        issues.append(f"YAML parse failure: {path.name}: {type(exc).__name__}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"YAML root is not a mapping: {path.name}")
        return {}
    return value


def load_json(path: pathlib.Path, issues: list[str]):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        issues.append(f"JSON parse failure: {path.name}: {type(exc).__name__}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"JSON root is not a mapping: {path.name}")
        return {}
    return value


def current_public_paths(synthesis: pathlib.Path, issues: list[str]) -> list[pathlib.Path]:
    """Enumerate physical current text without recovering retired history.

    Refuse unsafe or unreadable traversal instead of silently omitting files.
    This is a current-source scan, not historical membership authentication.
    """
    paths = []
    try:
        for ancestor in [*reversed(synthesis.absolute().parents), synthesis.absolute()]:
            if not stat.S_ISDIR(ancestor.lstat().st_mode):
                issues.append("unsafe current synthesis root")
                return []
    except OSError:
        issues.append("unreadable current synthesis root")
        return []

    def unreadable(error):
        issues.append("unreadable current synthesis directory")

    for directory, directories, files in os.walk(synthesis, followlinks=False, onerror=unreadable):
        base = pathlib.Path(directory)
        for name in list(directories):
            path = base / name
            try:
                safe = stat.S_ISDIR(path.lstat().st_mode)
            except OSError:
                safe = False
            if not safe:
                directories.remove(name)
                issues.append(f"unsafe current synthesis member: {path.relative_to(synthesis)}")
        for name in files:
            path = base / name
            try:
                safe = stat.S_ISREG(path.lstat().st_mode)
            except OSError:
                safe = False
            if not safe:
                issues.append(f"unsafe current synthesis member: {path.relative_to(synthesis)}")
            else:
                paths.append(path)
    return sorted(paths)


def validate(root=ROOT, synthesis_override=None):
    root = pathlib.Path(root)
    synthesis = pathlib.Path(synthesis_override) if synthesis_override else root / SYNTHESIS_REL
    issues: list[str] = []
    public_paths = current_public_paths(synthesis, issues)
    if issues:
        return {
            "schema": "ar8r-codex-current-synthesis-validation-v2",
            "result": "FAIL",
            "historical_audit_chain": "NOT_RUN",
            "historical_package_authentication": "NOT_RUN",
            "issues": issues,
        }

    instance_map = load_yaml(synthesis / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml", issues)
    relation_map = load_yaml(synthesis / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml", issues)
    formalization = load_yaml(synthesis / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml", issues)
    countermodels_data = load_yaml(synthesis / "AR8R-CODEX-COUNTERMODELS-V14.yaml", issues)
    verdict = load_yaml(synthesis / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml", issues)
    residuals_data = load_yaml(synthesis / "AR8R-CODEX-RESIDUAL-GUIDED-HYPOTHESIS-LEDGER-V14.yaml", issues)

    instances = instance_map.get("instances", [])
    instance_ids = [row.get("id") for row in instances if isinstance(row, dict)]
    if instance_ids != list(EXPECTED_INSTANCE_CLASSES):
        issues.append("typed instance exact identity/order mismatch")
    required_instance_fields = {
        "domain_objects", "target_query", "observation_or_transport", "fibres",
        "load_bearing_distinction", "sufficiency_condition", "restoring_resource",
        "authorization_and_version_guards", "failure_witness", "downstream_uses",
        "source_refs", "custody_class", "formalization_status", "relation_class",
        "source_world_bridge_established", "nonclaims",
    }
    for row in instances:
        if not isinstance(row, dict) or not required_instance_fields.issubset(row):
            issues.append("typed instance missing required fields")
            continue
        if row.get("relation_class") not in ALLOWED_RELATIONS:
            issues.append(f"unknown instance relation class: {row.get('id')}")
        if row.get("relation_class") != EXPECTED_INSTANCE_CLASSES.get(row.get("id")):
            issues.append(f"instance relation class drift: {row.get('id')}")
        if row.get("source_world_bridge_established") is not False or not row.get("nonclaims"):
            issues.append(f"instance bridge/nonclaim boundary mismatch: {row.get('id')}")
        references = row.get("source_refs", [])
        if row.get("id") in EXPECTED_SEMANTIC_SOURCE_REFS and references != EXPECTED_SEMANTIC_SOURCE_REFS[row.get("id")]:
            issues.append(f"instance semantic source contract drift: {row.get('id')}")
        for reference in references:
            pure = pathlib.PurePosixPath(reference)
            if pure.is_absolute() or ".." in pure.parts or "\\" in reference:
                issues.append(f"non-normalized instance source reference: {row.get('id')}: {reference}")
            if not digest_record_view_is_file(root / reference):
                issues.append(f"unresolved instance source reference: {row.get('id')}: {reference}")

    if instance_map.get("authority") != {
        "historical_identity": "NONE",
        "repository_scientific_adoption": "NONE",
        "owner_adoption": "PENDING",
        "general_novelty": 0,
    }:
        issues.append("cross-lane instance authority drift or promotion")

    relations = relation_map.get("relations", [])
    relation_ids = [row.get("id") for row in relations if isinstance(row, dict)]
    if relation_ids != list(EXPECTED_RELATION_CLASSES):
        issues.append("theorem-family exact identity/order mismatch")
    for row in relations:
        if not isinstance(row, dict) or row.get("relation") not in ALLOWED_RELATIONS:
            issues.append(f"unknown theorem-family relation: {row.get('id') if isinstance(row, dict) else None}")
            continue
        if row.get("novelty_effect") != 0 or not row.get("source_refs"):
            issues.append(f"relation ancestry or novelty boundary mismatch: {row.get('id')}")
        if row.get("relation") != EXPECTED_RELATION_CLASSES.get(row.get("id")):
            issues.append(f"theorem-family relation class drift: {row.get('id')}")
        references = row.get("source_refs", [])
        if row.get("id") in EXPECTED_SEMANTIC_SOURCE_REFS and references != EXPECTED_SEMANTIC_SOURCE_REFS[row.get("id")]:
            issues.append(f"relation semantic source contract drift: {row.get('id')}")
        for reference in references:
            pure = pathlib.PurePosixPath(reference)
            if pure.is_absolute() or ".." in pure.parts or "\\" in reference:
                issues.append(f"non-normalized relation source reference: {row.get('id')}: {reference}")
            if not digest_record_view_is_file(root / reference):
                issues.append(f"unresolved relation source reference: {row.get('id')}: {reference}")
    theorem_ancestry_bounded = any(
        row.get("source") == "AR-T1"
        and row.get("target") == "AR8R-T294"
        and row.get("relation") == "STRICT_SPECIALIZATION"
        for row in relations if isinstance(row, dict)
    ) and any(
        row.get("source") == "AR-T1"
        and row.get("target") == "CCS-V14-C1"
        and row.get("relation") == "SHARED_INVARIANT"
        for row in relations if isinstance(row, dict)
    )
    if not theorem_ancestry_bounded:
        issues.append("AR-T1 / AR8R-T294 ancestry ceiling drift")

    candidates = formalization.get("candidates", [])
    candidate_ids = [row.get("id") for row in candidates if isinstance(row, dict)]
    if candidate_ids != list(EXPECTED_CANDIDATE_VERDICTS):
        issues.append("candidate exact identity/order mismatch")
    for row in candidates:
        if not isinstance(row, dict):
            issues.append("candidate is not a mapping")
            continue
        if row.get("verdict") not in ALLOWED_VERDICTS:
            issues.append(f"unknown candidate verdict: {row.get('id')}")
        if row.get("verdict") != EXPECTED_CANDIDATE_VERDICTS.get(row.get("id")):
            issues.append(f"candidate verdict drift: {row.get('id')}")
        if not row.get("nonclaims") or not row.get("earliest_internal_ancestor"):
            issues.append(f"candidate ancestry/nonclaim boundary missing: {row.get('id')}")
        if row.get("earliest_internal_ancestor") != "PRIOR-ART::FIBRE_FACTORIZATION" or row.get("internal_specialization") != "AR-T1":
            issues.append(f"candidate generic/internal ancestry drift: {row.get('id')}")
        if row.get("historical_identity") != "NONE" or row.get("novelty") != 0:
            issues.append(f"candidate historical identity or novelty promoted: {row.get('id')}")

    protocols = formalization.get("empirical_protocols", [])
    protocol_ids = [row.get("id") for row in protocols if isinstance(row, dict)]
    protocol_readiness_fail_closed = (
        len(protocols) == 4
        and protocol_ids == list(EXPECTED_PROTOCOL_STATUSES)
        and all(row.get("status") == EXPECTED_PROTOCOL_STATUSES[row.get("id")] for row in protocols)
        and all(row.get("status") != "READY_TO_RUN" for row in protocols)
        and all(row.get("experiment_executed") is False for row in protocols)
        and next((row for row in protocols if row.get("id") == "B3"), {}).get("status")
        == "PREREGISTRATION_READY_FOR_REVIEW_DRAFT"
    )
    if not protocol_readiness_fail_closed:
        issues.append("empirical protocol readiness or execution promoted")
    if formalization.get("authority") != {
        "repository_scientific_adoption": "NONE",
        "owner_adoption": "PENDING",
        "empirical_program_run": False,
    }:
        issues.append("formalization authority drift or promotion")

    countermodels = countermodels_data.get("countermodels", [])
    countermodel_ids = [row.get("id") for row in countermodels if isinstance(row, dict)]
    expected_countermodels = [f"CM-{index:02d}" for index in range(1, 12)]
    if countermodel_ids != expected_countermodels:
        issues.append("countermodel exact identity/order mismatch")
    if any(not row.get("witness") or not row.get("conclusion") for row in countermodels if isinstance(row, dict)):
        issues.append("countermodel witness or conclusion missing")
    if countermodels_data.get("authority") != {
        "scope": "DECLARED_MODELS_ONLY",
        "general_novelty": 0,
        "owner_adoption": "PENDING",
    }:
        issues.append("countermodel authority drift or promotion")

    residuals = residuals_data.get("hypotheses", [])
    residual_ids = [row.get("id") for row in residuals if isinstance(row, dict)]
    if residual_ids != list(EXPECTED_RESIDUAL_STATUSES):
        issues.append("residual-hypothesis exact identity/order mismatch")
    for row in residuals:
        if row.get("status") != EXPECTED_RESIDUAL_STATUSES.get(row.get("id")):
            issues.append(f"residual-hypothesis status drift: {row.get('id')}")
    if residuals_data.get("authority_ceiling") != {
        "hypotheses_are_historical_evidence": False,
        "general_novelty": 0,
        "owner_adoption": "PENDING",
    }:
        issues.append("residual-hypothesis authority drift or promotion")

    authority = verdict.get("authority", {})
    authority_ceiling_exact = authority == EXPECTED_AUTHORITY
    if not authority_ceiling_exact:
        issues.append("authority ceiling drift or promotion")
    program = verdict.get("program_status", {})
    if program != {
        "integrated_champion": "NONE",
        "meniscus": "MENISCUS_NOT_REACHED",
        "natural_closure": "NOT_REACHED",
    }:
        issues.append("champion, meniscus, or closure promotion")
    if verdict.get("preserved_controls") != {
        "AR8R-T354": "BLOCKED_FORMAL_DEFECT",
        "TAC_SAC_HISTORICAL_DEFINITIONS": "UNAVAILABLE_UNDEFINED",
    }:
        issues.append("T354 or TAC/SAC preserved-control drift")
    if verdict.get("verdicts", {}).get("common_theorem_identity") != "PRIOR-ART::FIBRE_FACTORIZATION":
        issues.append("generic fibre theorem identity/ancestry drift")
    if verdict.get("verdicts", {}).get("internal_boolean_nonempty_specialization") != "AR-T1":
        issues.append("AR-T1 specialization relation drift")

    lean_source = synthesis / "lean/CodexFibreSynthesis.lean"
    lean_receipt = load_json(synthesis / "lean/LEAN_RECEIPT.json", issues)
    lean_receipt_exact = (
        digest_record_view_is_file(lean_source)
        and sha256(lean_source) == EXPECTED_LEAN_SHA
        and lean_receipt.get("source_sha256") == EXPECTED_LEAN_SHA
        and lean_receipt.get("standalone_parse_elaboration_kernel") == "PASS"
        and lean_receipt.get("project_build_run") is False
        and lean_receipt.get("historical_identity") == "NONE"
        and lean_receipt.get("general_novelty") == 0
        and lean_receipt.get("repository_scientific_adoption") == "NONE"
        and lean_receipt.get("owner_adoption") == "PENDING"
    )
    if not lean_receipt_exact:
        issues.append("Lean source or receipt drift")

    checker = synthesis / "checks/codex_fibre_synthesis_check.py"
    results_path = synthesis / "checks/codex_fibre_synthesis_check_results.json"
    results = load_json(results_path, issues)
    checker_receipt_exact = (
        digest_record_view_is_file(checker)
        and digest_record_view_is_file(results_path)
        and sha256(checker) == EXPECTED_CHECKER_SHA
        and sha256(results_path) == EXPECTED_RESULTS_SHA
        and results.get("status") == "PASS"
        and results.get("full_codomain_cases") == 1544
        and results.get("full_codomain_failures") == 0
        and results.get("pair_guard_cases") == 179
        and results.get("pair_guard_failures") == 0
        and results.get("joint_refinement_cases") == 179
        and results.get("joint_refinement_failures") == 0
        and results.get("empty_off_range_countermodel", {}).get("full_decoder_exists") is False
    )
    if not checker_receipt_exact:
        issues.append("finite checker source or result drift")

    private_path_findings = 0
    all_public_text = []
    for path in public_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(f"non-UTF-8 synthesis member: {path.relative_to(synthesis)}")
            continue
        except OSError:
            issues.append(f"unreadable synthesis member: {path.relative_to(synthesis)}")
            continue
        privacy_variants, normalization_exhausted = normalized_scan_variants(text)
        all_public_text.extend(privacy_variants)
        if normalization_exhausted:
            private_path_findings += 1
        private_path_findings += sum(
            len(PRIVATE_PATTERN.findall(variant)) for variant in privacy_variants
        )
    if private_path_findings:
        issues.append(
            "private path, browser locator, signed URL, or token-like text leaked into synthesis"
        )
    joined_public_text = "\n".join(all_public_text)
    authority_assignment_ceiling = {
        "HISTORICAL_IDENTITY": ("NONE", "HISTORICAL_IDENTITY"),
        "GENERAL_NOVELTY": ("0", "GENERAL_NOVELTY"),
        "REPOSITORY_SCIENTIFIC_ADOPTION": ("NONE", "SCIENTIFIC_ADOPTION"),
        "OWNER_ADOPTION": ("PENDING", "OWNER_ADOPTION"),
        "SOURCE_WORLD_BRIDGE_ESTABLISHED": ("FALSE", "SOURCE_WORLD_TRUE"),
        "EMPIRICAL_RESULT": ("NO_EXPERIMENT_EXECUTED", "EMPIRICAL_RESULT"),
        "INTEGRATED_CHAMPION": ("NONE", "INTEGRATED_CHAMPION"),
        "MENISCUS": ("MENISCUS_NOT_REACHED", "MENISCUS_REACHED"),
        "NATURAL_CLOSURE": ("NOT_REACHED", "NATURAL_CLOSURE_REACHED"),
        "T354": ("BLOCKED_FORMAL_DEFECT", "T354_PROMOTION"),
        "TAC_SAC": ("UNAVAILABLE_UNDEFINED", "TAC_SAC_DEFINITION"),
    }
    authority_key_pattern = "|".join(
        re.escape(key).replace("_", r"(?:[_-]|\s)+")
        for key in authority_assignment_ceiling
    )
    authority_gap = r"(?:\s|/\*.*?\*/|<!--.*?-->|\#[^\r\n]*(?:\r?\n|$))*"
    authority_assignment = re.compile(
        rf"(?<![A-Za-z0-9])[\"'`]?(?P<key>{authority_key_pattern})[\"'`]?"
        rf"{authority_gap}[:=]{authority_gap}"
        rf"(?P<value>[\"'][^\"'\r\n]*[\"']|[^,\r\n}}\]]+)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in authority_assignment.finditer(joined_public_text):
        normalized_key = re.sub(r"(?:[_-]|\s)+", "_", match.group("key")).upper()
        raw_value = match.group("value").strip()
        if not raw_value.startswith(("\"", "'")):
            raw_value = re.sub(r"\s+#.*$", "", raw_value).strip()
        raw_value = raw_value.strip("\"'`")
        normalized_value = re.sub(r"[_ -]+", "_", raw_value).upper()
        ceiling = authority_assignment_ceiling.get(normalized_key)
        if ceiling is not None and normalized_value != ceiling[0]:
            issues.append(f"prose or machine authority promotion: {ceiling[1]}")
    forbidden_promotions = {
        "MENISCUS_REACHED": r"(?<!NOT_)\bMENISCUS_REACHED\b",
        "NATURAL_CLOSURE_REACHED": r"\bnatural_closure\s*:\s*REACHED\b",
        "SOURCE_WORLD_TRUE": r"\bsource_world_bridge_established\s*:\s*true\b",
        "HISTORICAL_IDENTITY": r"\bhistorical_identity\s*:\s*AR8R[-_]",
        "NECESSARY_BEING": r"[\"']?necessary[_ -]+being[_ -]+established[\"']?\s*:\s*true\b",
        "ONE_PERSONAL_BEARER": r"[\"']?one[_ -]+personal[_ -]+bearer[_ -]+established[\"']?\s*:\s*true\b",
        "PERSONALITY": r"[\"']?personality[_ -]+established[\"']?\s*:\s*true\b",
        "WISDOM": r"[\"']?wisdom[_ -]+established[\"']?\s*:\s*true\b",
        "SPEECH": r"[\"']?speech[_ -]+established[\"']?\s*:\s*true\b",
        "REVELATION": r"[\"']?revelation[_ -]+established[\"']?\s*:\s*true\b",
        "ALLAH": r"[\"']?allah[_ -]+identification[_ -]+established[\"']?\s*:\s*true\b",
        "EMPIRICAL_RUN": r"[\"']?empirical[_ -]+program[_ -]+run[\"']?\s*:\s*true\b",
    }
    for label, pattern in forbidden_promotions.items():
        if re.search(pattern, joined_public_text, re.IGNORECASE):
            issues.append(f"prose or machine authority promotion: {label}")

    return {
        "schema": "ar8r-codex-current-synthesis-validation-v2",
        "result": "FAIL" if issues else "PASS_CURRENT_SYNTHESIS_CONTRACTS",
        "instance_count": len(instances),
        "candidate_count": len(candidates),
        "countermodel_count": len(countermodels),
        "protocol_count": len(protocols),
        "private_path_findings": private_path_findings,
        "authority_ceiling_exact": authority_ceiling_exact,
        "theorem_ancestry_bounded": theorem_ancestry_bounded,
        "lean_receipt_exact": lean_receipt_exact,
        "checker_receipt_exact": checker_receipt_exact,
        "historical_audit_chain": "NOT_RUN",
        "historical_package_authentication": "NOT_RUN",
        "protocol_readiness_fail_closed": protocol_readiness_fail_closed,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args()
    receipt = validate(args.root)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["result"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
