#!/usr/bin/env python3
"""Validate the exact PMR-007 Deep A-BK snapshot and public correction ceiling."""

import argparse
import hashlib
import json
import pathlib
import re

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
RELATIVE_ROOT = pathlib.Path("docs/project-closure/ar8r-v11")
SNAPSHOT_REL = RELATIVE_ROOT / "post-merge-proposals/pmr007-deep-a-bk"
PROGRAMS_REL = RELATIVE_ROOT / "programs"
CORRECTION_REL = (
    RELATIVE_ROOT
    / "post-merge-proposals/PMR007-DEEP-BF-BK-PUBLIC-CUSTODY-CORRECTION.yaml"
)
CROSSWALK_REL = (
    RELATIVE_ROOT
    / "post-merge-proposals/PMR007-DEEP-BF-BK-PUBLIC-REPRODUCTION-CROSSWALK.yaml"
)
ADOPTION_REL = (
    RELATIVE_ROOT
    / "post-merge-proposals/PMR007-DEEP-A-BK-ADOPTION-BOUNDARY-CORRECTION.md"
)
SOURCING_REL = (
    RELATIVE_ROOT
    / "post-merge-proposals/PMR007-DEEP-BF-BK-SOURCING-CORRECTION.md"
)
EQUATION_REL = (
    RELATIVE_ROOT
    / "post-merge-proposals/PMR007-DEEP-BE-EQUATION-PRESENTATION-CORRECTION.md"
)
PROPOSAL_RECEIPT_REL = (
    RELATIVE_ROOT
    / "provenance/AR8R-PMR007-DEEP-A-BK-PROPOSAL-RECEIPT-V1.yaml"
)
EXECUTION_RECEIPT_REL = (
    RELATIVE_ROOT
    / "provenance/AR8R-PMR007-DEEP-BF-BK-EXECUTION-RECEIPT-V1.yaml"
)
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace|Temp|Documents|Downloads|Desktop)[\\/]|"
    r"(?<![A-Za-z0-9])/(?:home|Users|root|tmp|var/tmp|private/tmp)/|"
    r"/mnt/data/|sandbox:/|file://|chatgpt\.com/(?:c|g)/|data-message-id|"
    r"screen-threadFlyOut)"
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
EXPECTED_SNAPSHOT_FILES = 1186
EXPECTED_REPOSITORY_SOURCE_PAIRS = {
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/AR8R-TRANSCENDENTAL-BRIDGE-AND-RIVAL-LEDGER-V11.yaml"),
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/ar8r-r5-minimal-nonintegration-control.md"),
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/AR8R-PROPER-FUNCTION-TYPED-MATRIX-V11.yaml"),
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md"),
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/candidate-g-derivational-unification.md"),
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/uncreated-grammar-and-articulability.md"),
    ("DEEP_BG", "docs/project-closure/ar8r-v11/programs/track-t-authority-and-bridge-status.md"),
    ("DEEP_BH", "docs/project-closure/ar8r-v11/programs/AR8R-PROPER-FUNCTION-TYPED-MATRIX-V11.yaml"),
    ("DEEP_BH", "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md"),
    ("DEEP_BI", "docs/project-closure/ar8r-v11/programs/uncreated-grammar-and-articulability.md"),
    ("DEEP_BI", "docs/project-closure/ar8r-v11/programs/language-translation-and-version-custody.md"),
    ("DEEP_BI", "docs/project-closure/ar8r-v11/programs/AR8R_TRANSCENDENTAL_ORTHABILITY_AND_SOURCE_ASCENT_V2.yaml"),
}
EXPECTED_CROSSWALK_ROUNDS = {
    "DEEP_BF": {
        "public_static_custody": "COMPLETE_FOR_INCLUDED_BYTES",
        "public_execution": "UNAVAILABLE_PRIVATE_SOURCE_PDFS",
    },
    "DEEP_BG": {
        "public_static_custody": "COMPLETE_FOR_INCLUDED_BYTES",
        "public_execution": "PARTIAL_ORIGINAL_SOURCE_SIDECAR_EXCLUDED",
    },
    "DEEP_BH": {
        "public_static_custody": "COMPLETE_FOR_INCLUDED_BYTES",
        "public_execution": "PARTIAL_PRIVATE_RENDERINGS_AND_ORIGINAL_SOURCE_SIDECAR_EXCLUDED",
    },
    "DEEP_BI": {
        "public_static_custody": "COMPLETE_FOR_INCLUDED_BYTES",
        "public_execution": "PARTIAL_ORIGINAL_SOURCE_SIDECAR_EXCLUDED",
    },
    "DEEP_BJ": {
        "public_static_custody": "COMPLETE_FOR_INCLUDED_BYTES",
        "public_execution": "PARTIAL_V2_PRIMARY_GENERATOR_ABSENT",
    },
    "DEEP_BK": {
        "public_static_custody": "COMPLETE_FOR_INCLUDED_BYTES",
        "public_execution": "DISPOSABLE_COPY_REQUIRED_WRITES_RESULTS",
    },
}
EXPECTED_PATH_CLASSES = {
    "theorem": "PROPOSED_THEOREM_FILES",
    "model": "PROPOSED_COUNTERMODELS",
    "audit_repair_rereview_and_results": "VALIDATION_RECEIPTS",
    "admission_and_frozen_hashes": "PROPOSED_LEDGER_UPDATES",
    "source_and_ancestry_notes": "PROPOSED_ORIGIN_AND_ANCESTRY_UPDATES",
}
EXPECTED_FORBIDDEN_CLAIMS = {
    "SELF_CONTAINED_PUBLIC_REREVIEW_REPRODUCTION",
    "COMPLETE_PUBLIC_SAFE_AUDIT_CUSTODY",
    "EXTERNAL_MATHEMATICAL_REVIEW",
    "OWNER_ADOPTION",
    "GENERAL_NOVELTY",
    "MENISCUS",
    "NATURAL_CLOSURE",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_manifest_path(raw):
    if not isinstance(raw, str):
        return None
    relative = raw.strip()
    if relative.startswith("*"):
        relative = relative[1:]
    if not relative or "\\" in relative or re.match(r"^[A-Za-z]:", relative):
        return None
    candidate = pathlib.PurePosixPath(relative)
    if (
        candidate.is_absolute()
        or relative != candidate.as_posix()
        or any(part in {"", ".", ".."} for part in candidate.parts)
        or candidate == pathlib.PurePosixPath("SHA256SUMS")
    ):
        return None
    return candidate.as_posix()


def _safe_repository_source_path(raw):
    relative = _safe_manifest_path(raw)
    if relative is None:
        return None
    prefix = PROGRAMS_REL.as_posix() + "/"
    if not relative.startswith(prefix):
        return None
    return relative


def _load_yaml_mapping(path, label, issues):
    if not path.is_file():
        issues.append("%s is missing" % label)
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        issues.append("%s is not valid UTF-8 YAML" % label)
        return {}
    if not isinstance(value, dict):
        issues.append("%s must be a YAML mapping" % label)
        return {}
    return value


def _manifest_rows(path):
    rows = []
    row_count = 0
    malformed_rows = 0
    unsafe_paths = 0
    duplicate_paths = 0
    listed_paths = set()
    parse_issues = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row_count += 1
        parts = line.split(None, 1)
        if len(parts) != 2 or not SHA256_PATTERN.fullmatch(parts[0]):
            malformed_rows += 1
            parse_issues.append("malformed snapshot SHA256SUMS row %d" % line_number)
            continue
        digest, raw_relative = parts
        relative = _safe_manifest_path(raw_relative)
        if relative is None:
            unsafe_paths += 1
            parse_issues.append("unsafe snapshot SHA256SUMS path at line %d" % line_number)
            continue
        if relative in listed_paths:
            duplicate_paths += 1
            parse_issues.append("duplicate snapshot SHA256SUMS path at line %d" % line_number)
            continue
        listed_paths.add(relative)
        rows.append((line_number, digest, relative))
    return {
        "rows": rows,
        "row_count": row_count,
        "listed_paths": listed_paths,
        "malformed_rows": malformed_rows,
        "unsafe_paths": unsafe_paths,
        "duplicate_paths": duplicate_paths,
        "issues": parse_issues,
    }


def validate(root=ROOT):
    root = pathlib.Path(root)
    snapshot = root / SNAPSHOT_REL
    correction_path = root / CORRECTION_REL
    crosswalk_path = root / CROSSWALK_REL
    required_text_paths = [
        root / ADOPTION_REL,
        root / SOURCING_REL,
        root / EQUATION_REL,
    ]
    issues = []
    snapshot_hash_mismatches = 0
    snapshot_manifest_malformed_rows = 0
    snapshot_manifest_unsafe_paths = 0
    snapshot_manifest_duplicate_paths = 0
    manifest_path = snapshot / "SHA256SUMS"
    if not manifest_path.is_file():
        issues.append("snapshot SHA256SUMS is missing")
        manifest_rows = []
        manifest_row_count = 0
        listed_paths = set()
    else:
        manifest = _manifest_rows(manifest_path)
        manifest_rows = manifest["rows"]
        manifest_row_count = manifest["row_count"]
        listed_paths = manifest["listed_paths"]
        snapshot_manifest_malformed_rows = manifest["malformed_rows"]
        snapshot_manifest_unsafe_paths = manifest["unsafe_paths"]
        snapshot_manifest_duplicate_paths = manifest["duplicate_paths"]
        issues.extend(manifest["issues"])

    actual_paths = set()
    for path in snapshot.rglob("*"):
        relative = path.relative_to(snapshot).as_posix()
        if (path.is_file() or path.is_symlink()) and relative != "SHA256SUMS":
            actual_paths.add(relative)
    snapshot_manifest_coverage_exact = (
        manifest_row_count == EXPECTED_SNAPSHOT_FILES
        and len(listed_paths) == EXPECTED_SNAPSHOT_FILES
        and listed_paths == actual_paths
        and snapshot_manifest_malformed_rows == 0
        and snapshot_manifest_unsafe_paths == 0
        and snapshot_manifest_duplicate_paths == 0
    )
    if not snapshot_manifest_coverage_exact:
        issues.append("snapshot SHA256SUMS coverage mismatch")

    snapshot_root = snapshot.resolve()
    for line_number, expected, relative in manifest_rows:
        target = snapshot / pathlib.PurePosixPath(relative)
        target_is_safe_file = (
            target.is_file()
            and not target.is_symlink()
            and target.resolve().is_relative_to(snapshot_root)
        )
        if not target_is_safe_file or sha256(target) != expected:
            snapshot_hash_mismatches += 1
            issues.append("snapshot hash mismatch at SHA256SUMS line %d" % line_number)

    private_paths_in_snapshot = 0
    snapshot_non_utf8_files = 0
    for relative in sorted(actual_paths):
        target = snapshot / pathlib.PurePosixPath(relative)
        if target.is_symlink():
            issues.append("snapshot symlink is forbidden: %s" % relative)
            continue
        try:
            text = target.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            snapshot_non_utf8_files += 1
            issues.append("snapshot member is not UTF-8 text: %s" % relative)
            text = target.read_bytes().decode("utf-8", errors="replace")
        private_paths_in_snapshot += len(PRIVATE_PATTERN.findall(text))
    if private_paths_in_snapshot:
        issues.append("private path or browser locator leaked into public snapshot")

    repository_source_hash_mismatches = 0
    repository_source_unsafe_paths = 0
    repository_source_malformed_rows = 0
    correction = _load_yaml_mapping(
        correction_path, "public custody correction", issues
    )
    if correction.get("public_reproduction_status") != "PARTIAL_REPRODUCTION_ONLY":
        issues.append("public reproduction ceiling is missing or promoted")
    repository_sources = correction.get("repository_sources", [])
    if not isinstance(repository_sources, list):
        issues.append("repository source custody rows must be a list")
        repository_sources = []
    observed_repository_source_pairs = []
    programs_root = (root / PROGRAMS_REL).resolve()
    for index, row in enumerate(repository_sources, 1):
        if not isinstance(row, dict) or set(row) != {"round", "path", "sha256"}:
            repository_source_malformed_rows += 1
            issues.append("malformed repository source custody row %d" % index)
            continue
        relative = _safe_repository_source_path(row.get("path"))
        digest = row.get("sha256")
        round_id = row.get("round")
        if relative is None:
            repository_source_unsafe_paths += 1
            issues.append("unsafe repository source custody path at row %d" % index)
            continue
        if not isinstance(round_id, str) or not SHA256_PATTERN.fullmatch(str(digest)):
            repository_source_malformed_rows += 1
            issues.append("malformed repository source custody row %d" % index)
            continue
        observed_repository_source_pairs.append((round_id, relative))
        target = root / pathlib.PurePosixPath(relative)
        target_is_safe_file = (
            target.is_file()
            and not target.is_symlink()
            and target.resolve().is_relative_to(programs_root)
        )
        if not target_is_safe_file or sha256(target) != digest:
            repository_source_hash_mismatches += 1
            issues.append("repository source hash mismatch: %s" % relative)
    repository_source_exact_set = (
        len(repository_sources) == len(EXPECTED_REPOSITORY_SOURCE_PAIRS)
        and len(observed_repository_source_pairs) == len(EXPECTED_REPOSITORY_SOURCE_PAIRS)
        and len(set(observed_repository_source_pairs)) == len(observed_repository_source_pairs)
        and set(observed_repository_source_pairs) == EXPECTED_REPOSITORY_SOURCE_PAIRS
        and repository_source_unsafe_paths == 0
        and repository_source_malformed_rows == 0
    )
    if not repository_source_exact_set:
        issues.append("repository source custody row set mismatch")
    private_exclusions = correction.get("private_exclusions", [])
    if len(private_exclusions) != 4 or any(row.get("public_path") is not None for row in private_exclusions):
        issues.append("private-exclusion custody rows are incomplete")

    crosswalk = _load_yaml_mapping(
        crosswalk_path, "public reproduction crosswalk", issues
    )
    crosswalk_values_exact = (
        crosswalk.get("schema")
        == "ar8r-pmr007-deep-bf-bk-public-reproduction-crosswalk-v1"
        and crosswalk.get("snapshot_root") == SNAPSHOT_REL.as_posix()
        and crosswalk.get("mutation_policy") == "READ_ONLY_SOURCE_NONMUTATING_VALIDATION"
        and crosswalk.get("historical_script_policy")
        == "EXECUTE_ONLY_IN_DISPOSABLE_COPY"
        and crosswalk.get("path_classes") == EXPECTED_PATH_CLASSES
        and crosswalk.get("rounds") == EXPECTED_CROSSWALK_ROUNDS
        and crosswalk.get("public_validator")
        == "scripts/validate_pmr007_deep_bk_public_snapshot.py"
        and crosswalk.get("public_validator_result")
        == "PASS_WITH_PARTIAL_REPRODUCTION_CEILING"
        and isinstance(crosswalk.get("forbidden_claims"), list)
        and len(crosswalk.get("forbidden_claims", [])) == len(EXPECTED_FORBIDDEN_CLAIMS)
        and set(crosswalk.get("forbidden_claims", [])) == EXPECTED_FORBIDDEN_CLAIMS
    )
    if not crosswalk_values_exact:
        issues.append("crosswalk custody or provenance ceiling mismatch")

    proposal_receipt = _load_yaml_mapping(
        root / PROPOSAL_RECEIPT_REL, "Deep A-BK proposal receipt", issues
    )
    proposal_boundary = proposal_receipt.get("proposal_boundary", {})
    execution_receipt = _load_yaml_mapping(
        root / EXECUTION_RECEIPT_REL, "Deep BF-BK execution receipt", issues
    )
    execution_boundary = execution_receipt.get("execution_boundary", {})
    interpretation = execution_receipt.get("interpretation", {})
    authority_ceiling_exact = (
        isinstance(proposal_boundary, dict)
        and proposal_boundary.get("indexed_results") == 73
        and proposal_boundary.get("existing_round_11_through_20_results") == 10
        and proposal_boundary.get("deep_a_through_bk_results") == 63
        and proposal_boundary.get("historical_identity_assigned") is False
        and proposal_boundary.get("historical_theorem_origin_credit") is False
        and proposal_boundary.get("external_review") == "OPEN"
        and proposal_boundary.get("owner_adoption") == "PENDING"
        and proposal_boundary.get("repository_readiness") == "EXTERNAL_REVIEW_REQUIRED"
        and proposal_boundary.get("general_novelty_credit") == "NOT_GRANTED"
        and proposal_boundary.get("lean_source_or_kernel_claim") == "NONE"
        and proposal_boundary.get("integrated_champion") == "NONE"
        and proposal_boundary.get("meniscus") == "MENISCUS_NOT_REACHED"
        and proposal_boundary.get("natural_closure") == "NOT_REACHED"
        and isinstance(execution_boundary, dict)
        and execution_boundary.get("public_snapshot_self_contained_executable") is False
        and execution_boundary.get("independent_reproduction_from_public_snapshot")
        == "NOT_ESTABLISHED"
        and isinstance(interpretation, dict)
        and interpretation.get("external_mathematical_review") == "OPEN"
        and interpretation.get("owner_adoption") == "PENDING"
        and interpretation.get("source_world_or_metaphysical_truth_effect") == "NONE"
        and interpretation.get("general_novelty_effect") == "NONE"
        and interpretation.get("meniscus_effect") == "NONE"
        and execution_receipt.get("authority_effect") == "NONE"
    )
    if not authority_ceiling_exact:
        issues.append("proposal or execution authority ceiling mismatch")

    for required in required_text_paths:
        if not required.is_file():
            issues.append("required correction surface is missing: %s" % required.relative_to(root))
    combined_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [correction_path, crosswalk_path, *required_text_paths]
        if path.is_file()
    )
    private_paths = len(PRIVATE_PATTERN.findall(combined_text))
    if private_paths:
        issues.append("private path or browser locator leaked into public corrections")

    required_sourcing_markers = (
        "10.1016/0024-3795(93)90224-C",
        "1605.06848",
        "PMR-BH-SRC-01",
        "UNVERIFIED",
        "ELT-2",
        "10.1038/s41586-024-08548-w",
    )
    sourcing_text = (
        (root / SOURCING_REL).read_text(encoding="utf-8")
        if (root / SOURCING_REL).is_file()
        else ""
    )
    if any(marker not in sourcing_text for marker in required_sourcing_markers):
        issues.append("sourcing correction is incomplete")
    adoption_text = (
        (root / ADOPTION_REL).read_text(encoding="utf-8")
        if (root / ADOPTION_REL).is_file()
        else ""
    )
    if "PMR-007-NCBD-1" not in adoption_text or "owner adoption: PENDING" not in adoption_text:
        issues.append("Deep BK owner-decision correction is incomplete")

    return {
        "schema": "ar8r-pmr007-deep-bk-public-validation-receipt-v1",
        "result": "FAIL" if issues else "PASS_WITH_PARTIAL_REPRODUCTION_CEILING",
        "snapshot_manifest_rows": manifest_row_count,
        "snapshot_manifest_distinct_paths": len(listed_paths),
        "snapshot_actual_files": len(actual_paths),
        "snapshot_manifest_coverage_exact": snapshot_manifest_coverage_exact,
        "snapshot_manifest_duplicate_paths": snapshot_manifest_duplicate_paths,
        "snapshot_manifest_unsafe_paths": snapshot_manifest_unsafe_paths,
        "snapshot_manifest_malformed_rows": snapshot_manifest_malformed_rows,
        "snapshot_hash_mismatches": snapshot_hash_mismatches,
        "snapshot_non_utf8_files": snapshot_non_utf8_files,
        "repository_source_rows": len(repository_sources),
        "repository_source_exact_set": repository_source_exact_set,
        "repository_source_unsafe_paths": repository_source_unsafe_paths,
        "repository_source_malformed_rows": repository_source_malformed_rows,
        "repository_source_hash_mismatches": repository_source_hash_mismatches,
        "crosswalk_values_exact": crosswalk_values_exact,
        "authority_ceiling_exact": authority_ceiling_exact,
        "private_exclusion_rows": len(private_exclusions),
        "private_paths_in_public_snapshot": private_paths_in_snapshot,
        "private_paths_in_public_corrections": private_paths,
        "self_contained_public_rereview_reproduction": False,
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
