#!/usr/bin/env python3
"""Validate the bounded Deep BW-CJ semantic custody reissue."""

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
AR8R_REL = pathlib.Path("docs/project-closure/ar8r-v11")
REISSUE_REL = AR8R_REL / "post-merge-proposals/pmr007-deep-bw-cj-semantic-reissue"
SOURCE_REL = REISSUE_REL / "source-files"
SOURCE_MANIFEST_REL = REISSUE_REL / "SOURCE_SHA256SUMS"
PROVENANCE_RECEIPT_REL = AR8R_REL / "provenance/AR8R-PMR007-DEEP-BW-CJ-CUSTODY-REISSUE-V1.yaml"
BV_VALIDATOR_REL = pathlib.Path("scripts/validate_pmr007_deep_bv_semantic_reissue.py")
EXPECTED_SOURCE_MANIFEST_SHA256 = "5a96a38980643ec5f56d3306ef2fb6b14ef607afb07036d5902b720916cf8d3d"
EXPECTED_V2_CHECKER_SHA256 = "0d83924960c9710e16834e4d382979ba655f93e9a7f475d378eb0c6ba948a68e"
EXPECTED_V2_RESULT_SHA256 = "c370d5a3eefa3bb557cde0cf620522a19f87387653dc24efb0c3b8a454072e0a"
EXPECTED_V3_CHECKER_SHA256 = "28def256cce9031cab7b86d2208eacd911a4625278db3db7638066c1ab8c5252"
EXPECTED_V3_RESULT_SHA256 = "e92dd6dcd1b221a016bc53419e2e10582265e48ab7d1328d34ed6b9a679c1090"
EXPECTED_IDS = [
    "PMR-007-TCIS-1", "PMR-007-MBAC-1", "PMR-007-SWAC-1", "PMR-007-BAXE-1",
    "PMR-007-RCIG-1", "PMR-007-CRFW-1", "PMR-007-CSQF-1", "PMR-007-NOPF-1",
    "PMR-007-CDPS-1", "PMR-007-ABIC-1", "PMR-007-SICM-1", "PMR-007-OIOT-1",
    "PMR-007-SCSI-1", "PMR-007-FSGW-1",
]
EXPECTED_ROUNDS = ["BW", "BX", "BY", "BZ", "CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ"]
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace|Temp|Documents|Downloads|Desktop)[\\/]|"
    r"(?<![A-Za-z0-9])/(?:home|Users|root|tmp|var/tmp|private/tmp)/|"
    r"/mnt/data/|sandbox:/|file://|chatgpt\.com/(?:c|g)/|data-message-id|"
    r"screen-threadFlyOut)"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_mapping(path, label, issues):
    if not path.is_file():
        issues.append(f"{label} is missing")
        return {}
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        issues.append(f"{label} is not valid UTF-8 YAML")
        return {}
    if not isinstance(document, dict):
        issues.append(f"{label} must be a mapping")
        return {}
    return document


def parse_source_manifest(path, issues):
    if not path.is_file():
        issues.append("semantic-reissue SOURCE_SHA256SUMS is missing")
        return {}, False
    exact_digest = sha256(path) == EXPECTED_SOURCE_MANIFEST_SHA256
    observed = {}
    malformed = False
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        lines = []
        malformed = True
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            malformed = True
            continue
        relative = parts[1]
        prefix = "source-files/"
        if not relative.startswith(prefix) or relative in observed:
            malformed = True
            continue
        observed[relative[len(prefix):]] = parts[0]
    exact = exact_digest and not malformed and len(observed) == 40
    if not exact:
        issues.append("semantic-reissue SOURCE_SHA256SUMS mismatch")
    return observed, exact


def load_bv_validator(root, issues):
    path = root / BV_VALIDATOR_REL
    if not path.is_file():
        issues.append("Deep BL-BV validator is missing")
        return None
    spec = importlib.util.spec_from_file_location("pmr007_bv_validator_for_bw_cj", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def v1_false_pass_detected(source):
    checker = source / "PROPOSAL/checks/post_bv_consolidated_recheck.py"
    try:
        text = checker.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return (
        '"matched_twins":20000' in text
        and 'ci["matched_twins"]+=' not in text
        and '"personal_impersonal_twins":20000' in text
        and 'cj["personal_impersonal_twins"]+=' not in text
    )


def rerun_checker(reissue, issues):
    checker = reissue / "intake-review/checks/post_bv_consolidated_recheck_v3.py"
    supplied_result = reissue / "intake-review/checks/post_bv_consolidated_recheck_v3_results.json"
    v2_checker = reissue / "intake-review/checks/post_bv_consolidated_recheck_v2.py"
    if not checker.is_file() or not supplied_result.is_file() or not v2_checker.is_file():
        issues.append("repaired V3 checker or result is missing")
        return False, False, False, 0
    if sha256(checker) != EXPECTED_V3_CHECKER_SHA256 or sha256(supplied_result) != EXPECTED_V3_RESULT_SHA256:
        issues.append("repaired V3 checker or result hash mismatch")
        return False, False, False, 0
    try:
        supplied = json.loads(supplied_result.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        issues.append("supplied consolidated checker result is invalid")
        return False, False, False, 0

    with tempfile.TemporaryDirectory() as temporary:
        temporary = pathlib.Path(temporary)
        copied_checker = temporary / checker.name
        copied_result = temporary / supplied_result.name
        shutil.copy2(checker, copied_checker)
        shutil.copy2(v2_checker, temporary / v2_checker.name)
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        completed = subprocess.run(
            [sys.executable, str(copied_checker)],
            cwd=temporary,
            env=environment,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if completed.returncode != 0 or not copied_result.is_file():
            issues.append("consolidated checker did not reproduce successfully")
            return False, False, False, 0
        try:
            reproduced = json.loads(copied_result.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            issues.append("reproduced consolidated checker result is invalid")
            return False, False, False, 0
        byte_match = copied_result.read_bytes() == supplied_result.read_bytes()

    semantic_match = reproduced == supplied
    results = reproduced.get("results", {}) if isinstance(reproduced, dict) else {}
    pass_count = sum(row.get("pass") is True for row in results.values() if isinstance(row, dict))
    ci = results.get("CI", {})
    cj = results.get("CJ", {})
    reproduced_ok = (
        reproduced.get("overall_pass") is True
        and reproduced.get("schema") == "pmr007-post-bv-consolidated-recheck-v3"
        and reproduced.get("v2_ci_cj_disposition") == "REJECTED_TAUTOLOGICAL_REPETITION_NOT_INDEPENDENT_EVIDENCE"
        and reproduced.get("authority") == "BOUNDED_FINITE_SIGNATURE_WITNESSES_ONLY"
        and list(results) == EXPECTED_ROUNDS
        and pass_count == 14
        and ci.get("authority") == "EXHAUSTIVE_DECLARED_FINITE_SIGNATURE_WITNESS_NOT_ARCHITECTURE_IMPLEMENTATION"
        and ci.get("declared_profiles") == 15625
        and ci.get("exhaustive_target_fibre_witnesses") == 15625
        and ci.get("witness_failures") == 0
        and ci.get("target_leak_false_positives") == 0
        and ci.get("profile_change_false_positives") == 0
        and ci.get("same_target_false_positives") == 0
        and ci.get("predicate_mutation_receipt", {}).get("all_declared_mutants_killed") is True
        and cj.get("authority") == "EXHAUSTIVE_ELIGIBLE_FINITE_SIGNATURE_WITNESS_NOT_ARCHITECTURE_IMPLEMENTATION"
        and cj.get("declared_profiles") == 6561
        and cj.get("eligible_profiles") == 72
        and cj.get("eligibility_recheck_failures") == 0
        and cj.get("exhaustive_personal_impersonal_witnesses") == 72
        and cj.get("witness_failures") == 0
        and cj.get("target_leak_false_positives") == 0
        and cj.get("profile_change_false_positives") == 0
        and cj.get("same_target_false_positives") == 0
        and cj.get("predicate_mutation_receipt", {}).get("all_declared_mutants_killed") is True
    )
    if not semantic_match:
        issues.append("reproduced checker object does not match supplied result")
    if not byte_match:
        issues.append("reproduced V3 checker bytes do not match supplied deterministic result")
    if not reproduced_ok:
        issues.append("consolidated checker did not pass all fourteen bounded checks")
    return reproduced_ok, semantic_match, byte_match, pass_count


def validate(root=ROOT, reissue_override=None, provenance_override=None):
    root = pathlib.Path(root)
    reissue = pathlib.Path(reissue_override) if reissue_override else root / REISSUE_REL
    source = reissue / "source-files"
    manifest_path = reissue / "SOURCE_SHA256SUMS"
    provenance_path = pathlib.Path(provenance_override) if provenance_override else root / PROVENANCE_RECEIPT_REL
    issues = []
    expected_hashes, source_manifest_exact = parse_source_manifest(manifest_path, issues)

    actual_paths = set()
    private_path_findings = 0
    structured_parse_errors = 0
    source_hash_mismatches = 0
    if source.is_dir():
        actual_paths = {
            path.relative_to(source).as_posix()
            for path in source.rglob("*")
            if path.is_file() or path.is_symlink()
        }
    else:
        issues.append("semantic-reissue source directory is missing")
    source_coverage_exact = actual_paths == set(expected_hashes)
    if not source_coverage_exact:
        issues.append("semantic-reissue source coverage mismatch")

    for relative in sorted(actual_paths):
        target = source / pathlib.PurePosixPath(relative)
        if target.is_symlink():
            issues.append(f"semantic-reissue symlink is forbidden: {relative}")
            continue
        try:
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            issues.append(f"semantic-reissue member is not readable UTF-8: {relative}")
            continue
        private_path_findings += len(PRIVATE_PATTERN.findall(text))
        if relative.endswith((".yaml", ".yml")):
            try:
                yaml.safe_load(text)
            except yaml.YAMLError:
                structured_parse_errors += 1
        elif relative.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError:
                structured_parse_errors += 1
        expected = expected_hashes.get(relative)
        if expected is None or sha256(target) != expected:
            source_hash_mismatches += 1
    if private_path_findings:
        issues.append("private path or browser locator leaked into semantic reissue")
    if structured_parse_errors:
        issues.append("semantic-reissue structured file parse failure")
    if source_hash_mismatches:
        issues.append("semantic-reissue source hash mismatch")

    provenance = load_mapping(provenance_path, "Deep BW-CJ custody receipt", issues)
    source_reissue = provenance.get("source_reissue", {})
    repository_copy = provenance.get("repository_copy", {})
    boundary = provenance.get("proposal_boundary", {})
    recheck = provenance.get("independent_intake_recheck", {})
    integration = provenance.get("integration", {})
    authority_ceiling_exact = (
        provenance.get("schema") == "ar8r-pmr007-deep-bw-cj-custody-reissue-v1"
        and source_reissue.get("sha256") == "215be89bdca4a33d4272182b2eb21d956290691ac148b1c8df92db9fde96a4af"
        and source_reissue.get("bytes") == 61145
        and source_reissue.get("archive_members") == 40
        and all(source_reissue.get(field) == 0 for field in (
            "unsafe_paths", "duplicate_paths", "crc_failures", "byte_mismatches", "structured_parse_errors"
        ))
        and source_reissue.get("round_trip_restoration") == "PASS"
        and repository_copy.get("source_files") == 40
        and repository_copy.get("source_files_copied_byte_exact_from_reissue") is True
        and repository_copy.get("original_ephemeral_deep_bw_cj_bytes_claimed") is False
        and boundary.get("result_count") == 14
        and boundary.get("range") == "Deep BW through Deep CJ"
        and boundary.get("identities") == EXPECTED_IDS
        and boundary.get("original_ephemeral_files") == "UNAVAILABLE"
        and boundary.get("semantic_reissue_only") is True
        and boundary.get("historical_identity") == "NONE"
        and boundary.get("owner_adoption") == "PENDING"
        and boundary.get("external_review") == "OPEN"
        and boundary.get("repository_scientific_adoption") == "NONE"
        and boundary.get("general_mathematical_novelty") == 0
        and boundary.get("lean_parse_elaboration_kernel") == "NOT_RUN"
        and boundary.get("integrated_champion") == "NONE"
        and boundary.get("meniscus") == "MENISCUS_NOT_REACHED"
        and boundary.get("natural_closure") == "NOT_REACHED"
        and boundary.get("historical_duration_effect") == "NONE"
        and boundary.get("theorem_origin_authority_effect") == "NONE"
        and recheck.get("v1_parsed_result_reproduced") is True
        and recheck.get("v1_disposition") == "REJECTED_FALSE_PASS_CI_CJ"
        and recheck.get("v1_defects") == [
            "CI_TWIN_COUNTER_PREFILLED_BODY_NOT_EXECUTED",
            "CJ_TWIN_COUNTER_PREFILLED_BODY_NOT_EXECUTED",
            "PLATFORM_NATIVE_NEWLINE_OUTPUT_DRIFT",
        ]
        and recheck.get("v2_checker_sha256") == EXPECTED_V2_CHECKER_SHA256
        and recheck.get("v2_result_sha256") == EXPECTED_V2_RESULT_SHA256
        and recheck.get("v2_executed_on_intake") is True
        and recheck.get("v2_parsed_result_reproduces_exactly") is True
        and recheck.get("v2_disposition") == "REJECTED_TAUTOLOGICAL_REPETITION_NOT_INDEPENDENT_EVIDENCE"
        and recheck.get("v3_checker_sha256") == EXPECTED_V3_CHECKER_SHA256
        and recheck.get("v3_result_sha256") == EXPECTED_V3_RESULT_SHA256
        and recheck.get("v3_executed_on_intake") is True
        and recheck.get("v3_parsed_result_reproduces_exactly") is True
        and recheck.get("declared_finite_checks") == 14
        and recheck.get("finite_checks_passed") == 14
        and recheck.get("ci_exhaustive_signature_witnesses") == 15625
        and recheck.get("ci_negative_controls_executed") == 46875
        and recheck.get("cj_eligible_signature_witnesses") == 72
        and recheck.get("cj_negative_controls_executed") == 216
        and recheck.get("predicate_mutant_families_killed_per_round") == 3
        and recheck.get("authority_ceiling") == "CONSTRUCTED_FINITE_SIGNATURE_WITNESSES_ONLY"
        and recheck.get("scientific_disposition") == {
            "BW_THROUGH_CH": "GAP_PENDING_PER_RESULT_INDEPENDENT_REVIEW",
            "CI": "GAP_CONDITIONAL_COUNTERMODEL_ARCHITECTURE_IMPLEMENTATION_UNVERIFIED",
            "CJ": "GAP_CONDITIONAL_COUNTERMODEL_ARCHITECTURE_IMPLEMENTATION_UNVERIFIED",
        }
        and integration.get("base_sha") == "a8142c3caf103ee46a2cd759c3d319b1e29b40da"
        and integration.get("private_archive_committed") is False
        and integration.get("source_pdf_bytes_committed") is False
        and integration.get("raw_chat_or_activity_committed") is False
    )
    if not authority_ceiling_exact:
        issues.append("semantic-reissue authority ceiling mismatch")

    index = load_mapping(source / "PROPOSAL/ledgers/RESULT_INDEX.yaml", "Deep BW-CJ result index", issues)
    results = index.get("results", []) if isinstance(index, dict) else []
    indexed_results = len(results) if isinstance(results, list) else 0
    result_index_exact = (
        isinstance(results, list)
        and [row.get("round") for row in results] == EXPECTED_ROUNDS
        and [row.get("identity") for row in results] == EXPECTED_IDS
        and index.get("custody_class") == "SEMANTIC_REISSUE_OR_REGENERATED_CUSTODY_COPY"
        and all(row.get("historical_identity") == "NONE" for row in results)
        and all(row.get("general_mathematical_novelty") == 0 for row in results)
        and all(row.get("owner_adoption") == "PENDING" for row in results)
        and all(row.get("external_review") == "OPEN" for row in results)
        and all(row.get("repository_adoption") == "NONE" for row in results)
        and all(row.get("custody_exact_original_bytes") is False for row in results)
    )
    if not result_index_exact:
        issues.append("Deep BW-CJ result-index identity or custody mismatch")

    v3_checker_reproduced = False
    v3_result_semantic_match = False
    v3_result_byte_match = False
    checker_pass_count = 0
    if source_coverage_exact and source_hash_mismatches == 0 and structured_parse_errors == 0:
        v3_checker_reproduced, v3_result_semantic_match, v3_result_byte_match, checker_pass_count = rerun_checker(reissue, issues)
    else:
        issues.append("checker reproduction skipped because source custody failed")

    detected_v1_false_pass = v1_false_pass_detected(source)
    if not detected_v1_false_pass:
        issues.append("known V1 CI/CJ false-pass structure is not preserved or detected")

    bv_validator = load_bv_validator(root, issues)
    if bv_validator is None:
        deep_bv_baseline_unchanged = False
    else:
        bv_receipt = bv_validator.validate(root)
        deep_bv_baseline_unchanged = (
            bv_receipt.get("result") == "PASS_WITH_SEMANTIC_REISSUE_CEILING"
            and bv_receipt.get("source_hash_mismatches") == 0
            and bv_receipt.get("source_manifest_exact") is True
        )
    if not deep_bv_baseline_unchanged:
        issues.append("Deep BL-BV semantic baseline changed or failed validation")

    return {
        "schema": "ar8r-pmr007-deep-bw-cj-semantic-reissue-validation-v1",
        "result": "FAIL" if issues else "PASS_WITH_SEMANTIC_REISSUE_CEILING",
        "source_files": len(actual_paths),
        "source_coverage_exact": source_coverage_exact,
        "source_hash_mismatches": source_hash_mismatches,
        "source_manifest_exact": source_manifest_exact,
        "structured_parse_errors": structured_parse_errors,
        "private_path_findings": private_path_findings,
        "indexed_results": indexed_results,
        "result_index_exact": result_index_exact,
        "authority_ceiling_exact": authority_ceiling_exact,
        "deep_bv_baseline_unchanged": deep_bv_baseline_unchanged,
        "v3_checker_reproduced": v3_checker_reproduced,
        "v3_result_semantic_match": v3_result_semantic_match,
        "v3_result_byte_match": v3_result_byte_match,
        "checker_pass_count": checker_pass_count,
        "v1_false_pass_detected": detected_v1_false_pass,
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
