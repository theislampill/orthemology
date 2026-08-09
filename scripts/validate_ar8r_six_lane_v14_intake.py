#!/usr/bin/env python3
"""Validate immutable six-lane V14 proposal custody and correction overlays."""

from __future__ import annotations

import argparse
import hashlib
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
INTAKE_REL = pathlib.Path(
    "docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake"
)
PACKAGES = {
    "central": {
        "manifest": "SHA256SUMS",
        "manifest_sha256": "161bba2290408e313d08fa19e38adaec2b4c54ae36be2c37662a9398248ede81",
        "files": 178,
    },
    "specialist-a": {
        "manifest": "SHA256SUMS",
        "manifest_sha256": "f19fb30506f0d91cd0ababbe48c2f39ab0d075d5ae9b683fdf87717e26cf371f",
        "files": 77,
    },
    "specialist-b": {
        "manifest": "MANIFEST.sha256",
        "manifest_sha256": "a3e32a6f8986fb9196c21e4ed9bb7d1be05b80050a063c201d9e71bbcbbd78dd",
        "files": 29,
    },
}
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace|Temp|Documents|Downloads|Desktop)[\\/]|"
    r"(?<![A-Za-z0-9])/(?:home|Users|root|tmp|var/tmp|private/tmp)/|"
    r"/mnt/data/|sandbox:/|file://|chatgpt\.com/(?:c|g)/|data-message-id|"
    r"screen-threadFlyOut|screen-threadFlyOut|(?:access|refresh)[_-]?token\s*[:=])",
    re.IGNORECASE,
)

EXPECTED_EXTERNAL_EVIDENCE_FILES = {
    "AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml",
    "AR8R-SIX-LANE-V14-SOURCING-CORRECTION.md",
}
EXPECTED_B1_B4_PROTOCOLS = [
    "noetic restoration and proper function",
    "intentional uptake and personality",
    "source-recipient causal landing",
    "truth-connected norm and because-of uptake",
]
EXPECTED_AUTHORITY_CEILING = {
    "historical_identity": "NONE",
    "repository_scientific_adoption": "NONE",
    "owner_adoption": "PENDING",
    "external_review": "OPEN",
    "general_novelty": 0,
    "empirical_program_run": False,
    "source_world_bridge_established": False,
    "integrated_champion": "NONE",
    "meniscus": "MENISCUS_NOT_REACHED",
    "natural_closure": "NOT_REACHED",
}


def contains_ready_to_run(value) -> bool:
    if isinstance(value, dict):
        return any(contains_ready_to_run(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_ready_to_run(item) for item in value)
    return value == "READY_TO_RUN"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(path: pathlib.Path, expected_digest: str, issues: list[str]):
    expected: dict[str, str] = {}
    if not path.is_file() or sha256(path) != expected_digest:
        issues.append(f"source manifest mismatch: {path}")
        return expected
    malformed = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split(None, 1)
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            malformed = True
            continue
        relative = parts[1].removeprefix("./").replace("\\", "/")
        if relative.startswith("/") or ".." in pathlib.PurePosixPath(relative).parts:
            malformed = True
            continue
        if relative in expected:
            malformed = True
        expected[relative] = parts[0]
    if malformed:
        issues.append(f"source manifest malformed: {path}")
    return expected


def parse_structured(root: pathlib.Path, issues: list[str]):
    parsed = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.suffix.lower() == ".json":
                json.loads(path.read_text(encoding="utf-8"))
                parsed += 1
            elif path.suffix.lower() in {".yaml", ".yml"}:
                yaml.safe_load(path.read_text(encoding="utf-8"))
                parsed += 1
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
            issues.append(f"structured parse failure: {path}: {type(exc).__name__}")
    return parsed


def rerun_specialist_a(source: pathlib.Path, issues: list[str]) -> bool:
    with tempfile.TemporaryDirectory() as temporary:
        work = pathlib.Path(temporary) / "specialist-a"
        shutil.copytree(source, work)
        for result in (work / "results").glob("*.json"):
            result.unlink()
        fresh = work / "audit/FRESH_REREVIEW.json"
        if fresh.exists():
            fresh.unlink()
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        commands = [
            [sys.executable, "checks/run_all_checks.py"],
            [sys.executable, "audit/fresh_rereview.py"],
        ]
        for command in commands:
            completed = subprocess.run(
                command,
                cwd=work,
                env=environment,
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            if completed.returncode != 0:
                issues.append(f"Specialist A executable replay failed: {' '.join(command)}")
                return False

        exact = True
        expected_results = sorted(
            path for path in (source / "results").glob("r*_results.json")
        )
        for expected in expected_results:
            observed = work / "results" / expected.name
            try:
                if json.loads(observed.read_text(encoding="utf-8")) != json.loads(
                    expected.read_text(encoding="utf-8")
                ):
                    exact = False
            except (OSError, json.JSONDecodeError):
                exact = False
        expected_fresh = source / "audit/FRESH_REREVIEW.json"
        observed_fresh = work / "audit/FRESH_REREVIEW.json"
        try:
            fresh_exact = json.loads(observed_fresh.read_text(encoding="utf-8")) == json.loads(
                expected_fresh.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            fresh_exact = False
        if not fresh_exact:
            exact = False
        try:
            aggregate = json.loads((work / "results/all_checks_results.json").read_text(encoding="utf-8"))
            rereview = json.loads(observed_fresh.read_text(encoding="utf-8"))
            exact = exact and aggregate.get("status") == "PASS"
            exact = exact and aggregate.get("rounds_passed") == 12
            exact = exact and rereview.get("status") == "PASS"
        except (OSError, json.JSONDecodeError):
            exact = False
        if not exact:
            issues.append("Specialist A finite checker/rereview replay did not reproduce")
        return exact


def validate(root=ROOT, intake_override=None):
    root = pathlib.Path(root)
    intake = pathlib.Path(intake_override) if intake_override else root / INTAKE_REL
    issues: list[str] = []
    counts: dict[str, int] = {}
    source_hash_mismatches = 0
    private_path_findings = 0

    for lane, contract in PACKAGES.items():
        source = intake / lane / "source-files"
        manifest = source / contract["manifest"]
        expected = parse_manifest(manifest, contract["manifest_sha256"], issues)
        actual_paths = {
            path.relative_to(source).as_posix()
            for path in source.rglob("*")
            if path.is_file() or path.is_symlink()
        } if source.is_dir() else set()
        counts[lane] = len(actual_paths)
        expected_paths = set(expected) | {contract["manifest"]}
        if actual_paths != expected_paths or len(actual_paths) != contract["files"]:
            issues.append(f"source coverage mismatch: {lane}")
        for relative in sorted(actual_paths):
            target = source / pathlib.PurePosixPath(relative)
            if target.is_symlink():
                issues.append(f"symlink forbidden in source custody: {lane}/{relative}")
                continue
            if relative != contract["manifest"] and expected.get(relative) != sha256(target):
                source_hash_mismatches += 1

    if source_hash_mismatches:
        issues.append("source hash mismatch")

    for path in intake.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(f"non-UTF-8 public intake member: {path.relative_to(intake)}")
            continue
        private_path_findings += len(PRIVATE_PATTERN.findall(text))
    if private_path_findings:
        issues.append("private path, browser locator, or token-like text leaked into intake")

    structured_files_parsed = parse_structured(intake, issues)

    try:
        ledger = yaml.safe_load((intake / "AR8R-SIX-LANE-V14-INTEGRATION-LEDGER.yaml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        ledger = {}
    lanes = ledger.get("lanes", []) if isinstance(ledger, dict) else []
    lane_count = len(lanes)
    if lane_count != 6 or len({row.get("id") for row in lanes}) != 6:
        issues.append("six-lane integration ledger coverage mismatch")
    if any(row.get("owner_adoption") != "PENDING" for row in lanes):
        issues.append("owner-adoption promotion in six-lane ledger")
    program = ledger.get("program_status", {}) if isinstance(ledger, dict) else {}
    if program.get("repository_scientific_adoption") != "NONE":
        issues.append("repository scientific adoption promotion")
    if program.get("owner_adoption") != "PENDING":
        issues.append("program-level owner-adoption promotion")
    if program.get("integrated_champion") != "NONE":
        issues.append("integrated-champion promotion")
    if program.get("meniscus") != "MENISCUS_NOT_REACHED" or program.get("natural_closure") != "NOT_REACHED":
        issues.append("meniscus or closure promotion")

    a_receipt_path = intake / "specialist-a/intake-review/LEAN_INTAKE_RECEIPT.json"
    b_receipt_path = intake / "specialist-b/intake-review/LEAN_INTAKE_RECEIPT.json"
    try:
        a_receipt = json.loads(a_receipt_path.read_text(encoding="utf-8"))
        b_receipt = json.loads(b_receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        a_receipt, b_receipt = {}, {}

    a_source = intake / "specialist-a/source-files/lean"
    a_review = intake / "specialist-a/intake-review/lean"
    specialist_a_original_lean_failures_recorded = (
        sha256(a_source / "DeletionCriterion.lean") == "1140cc3f56d743000ebf94ee3c84ecc6727d2a5fa7e4dbc352d0af98675b2caa"
        and sha256(a_source / "ObservationUniformity.lean") == "555e88086b3c6345331ff5801928940217606bbb02cb0866db56b5b05645f70e"
        and [row.get("status") for row in a_receipt.get("originals", [])] == ["PARSE_FAILED", "PARSE_FAILED"]
    )
    expected_a_repairs = {
        (
            "intake-review/lean/DeletionCriterion.repaired.lean",
            "8825df59e9ba945d61ec5db752087bf677f1d0fdd1f82cdb556b84732c8b2873",
            "PASS",
        ),
        (
            "intake-review/lean/ObservationUniformity.repaired.lean",
            "b46453b7f11f4593e3caf4e96cd2f48ad02af9df345586b720a7e9cf70f73324",
            "PASS",
        ),
    }
    actual_a_repairs = [
        (
            row.get("path"),
            row.get("sha256"),
            row.get("standalone_parse_elaboration_kernel"),
        )
        for row in a_receipt.get("repairs", [])
        if isinstance(row, dict)
    ]
    specialist_a_repaired_lean_receipts_exact = (
        sha256(a_review / "DeletionCriterion.repaired.lean") == "8825df59e9ba945d61ec5db752087bf677f1d0fdd1f82cdb556b84732c8b2873"
        and sha256(a_review / "ObservationUniformity.repaired.lean") == "b46453b7f11f4593e3caf4e96cd2f48ad02af9df345586b720a7e9cf70f73324"
        and len(actual_a_repairs) == len(expected_a_repairs)
        and set(actual_a_repairs) == expected_a_repairs
        and a_receipt.get("repository_scientific_adoption") == "NONE"
        and a_receipt.get("owner_adoption") == "PENDING"
    )
    if not specialist_a_original_lean_failures_recorded:
        issues.append("Specialist A original Lean failures not preserved")
    if not specialist_a_repaired_lean_receipts_exact:
        issues.append("Specialist A repaired Lean receipt mismatch")

    b_source = intake / "specialist-b/source-files/SpecialistBBridgeSignatures.lean"
    b_repaired = intake / "specialist-b/intake-review/lean/SpecialistBBridgeSignatures.repaired.lean"
    specialist_b_original_lean_failure_recorded = (
        sha256(b_source) == "e18b1e03b970b4d355008eb64ba3f502a23e9c36797ecb009d6487e923c97015"
        and b_receipt.get("original", {}).get("status") == "PARSE_ELABORATION_FAILED"
    )
    specialist_b_repaired_lean_receipt_exact = (
        sha256(b_repaired) == "3602e4d29ebb57e8b01e78acf57dc49712373af59509bcfe193c93ba302f20d1"
        and b_receipt.get("repair", {}).get("standalone_parse_elaboration_kernel") == "PASS"
        and b_receipt.get("repository_scientific_adoption") == "NONE"
        and b_receipt.get("owner_adoption") == "PENDING"
    )
    if not specialist_b_original_lean_failure_recorded:
        issues.append("Specialist B original Lean failure not preserved")
    if not specialist_b_repaired_lean_receipt_exact:
        issues.append("Specialist B repaired Lean receipt mismatch")

    evidence_path = intake / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
    try:
        evidence = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        evidence = {}

    external_evidence_root = intake / "external-evidence"
    external_evidence_files = {
        path.relative_to(external_evidence_root).as_posix()
        for path in external_evidence_root.rglob("*")
        if path.is_file()
    } if external_evidence_root.is_dir() else set()
    reports = evidence.get("reports", []) if isinstance(evidence, dict) else []
    report_copy_flags_exact = (
        len(reports) == 3
        and {row.get("lane") for row in reports if isinstance(row, dict)}
        == {"DEEP_RESEARCH_20", "DEEP_RESEARCH_21", "DEEP_RESEARCH_22"}
        and all(row.get("public_bytes_copied") is False for row in reports if isinstance(row, dict))
    )
    private_reports_excluded = (
        report_copy_flags_exact
        and external_evidence_files == EXPECTED_EXTERNAL_EVIDENCE_FILES
    )
    if not private_reports_excluded:
        issues.append("private Deep Research report bytes or copy flags entered public intake")

    authority_ceiling = evidence.get("authority_ceiling", {}) if isinstance(evidence, dict) else {}
    authority_ceiling_exact = authority_ceiling == EXPECTED_AUTHORITY_CEILING
    if not authority_ceiling_exact:
        issues.append("Deep Research authority ceiling drift or promotion")
    theological = {row.get("id"): row for row in evidence.get("theological_and_metaphysical_sources", [])}
    speech = theological.get("DR21-SPEECH-VOICE", {})
    deep_research_locator_corrections_exact = (
        speech.get("locator") == "volume 12, pages 98 and 409 in the checked Islamweb digital rendering"
        and speech.get("prior_locator_12_98") == "CONFIRMED_PARALLEL_LOCUS"
        and theological.get("DR21-QIYAS-AL-AWLA", {}).get("locator")
        == "volume 7 pages 362-363 in the checked digital rendering"
    )
    if not deep_research_locator_corrections_exact:
        issues.append("Deep Research source-locator correction mismatch")

    protocols = {row.get("id"): row for row in evidence.get("empirical_and_protocol_intake", [])}
    tensor = protocols.get("DR22-TENSOR-ARM-ONTOLOGY", {})
    tensor_program = (root / "docs/project-closure/ar8r-v11/programs/tensor-and-bitter-lesson.md").read_text(encoding="utf-8")
    tensor_arm_specification_blocked = (
        tensor.get("representation_candidates_in_current_charter") == 6
        and tensor.get("legacy_gate_description") == "120 observations and five arms"
        and tensor.get("status") == "BLOCKED_SPECIFICATION_AMBIGUITY"
        and "BLOCKED_SPECIFICATION_AMBIGUITY" in tensor_program
    )
    if not tensor_arm_specification_blocked:
        issues.append("tensor representation-arm ambiguity not fail-closed")

    readiness = evidence.get("protocol_readiness", {}) if isinstance(evidence, dict) else {}
    deep_research_22_readiness_fail_closed = (
        readiness.get("ready_to_run_count") == 0
        and readiness.get("empirical_validation_claimed") is False
        and not contains_ready_to_run(evidence)
    )
    if not deep_research_22_readiness_fail_closed:
        issues.append("Deep Research 22 protocol readiness promoted without evidence")

    coverage = protocols.get("DR22-B1-B4-COVERAGE-GAP", {})
    deep_research_22_b1_b4_gap_explicit = (
        coverage.get("status") == "NOT_ANSWERED_BY_CURRENT_REPORT"
        and coverage.get("required_protocols") == EXPECTED_B1_B4_PROTOCOLS
    )
    if not deep_research_22_b1_b4_gap_explicit:
        issues.append("Deep Research 22 B1-B4 coverage gap is not explicit")

    specialist_a_checks_reproduced = False
    if intake_override is None and source_hash_mismatches == 0:
        specialist_a_checks_reproduced = rerun_specialist_a(
            intake / "specialist-a/source-files", issues
        )

    return {
        "schema": "ar8r-six-lane-v14-intake-validation-v1",
        "result": "FAIL" if issues else "PASS_PROPOSAL_CUSTODY_AND_BOUNDED_SOURCE_INTAKE",
        "lane_count": lane_count,
        "source_file_counts": counts,
        "source_hash_mismatches": source_hash_mismatches,
        "private_path_findings": private_path_findings,
        "structured_files_parsed": structured_files_parsed,
        "private_reports_excluded": private_reports_excluded,
        "authority_ceiling_exact": authority_ceiling_exact,
        "specialist_a_checks_reproduced": specialist_a_checks_reproduced,
        "specialist_a_original_lean_failures_recorded": specialist_a_original_lean_failures_recorded,
        "specialist_a_repaired_lean_receipts_exact": specialist_a_repaired_lean_receipts_exact,
        "specialist_b_original_lean_failure_recorded": specialist_b_original_lean_failure_recorded,
        "specialist_b_repaired_lean_receipt_exact": specialist_b_repaired_lean_receipt_exact,
        "deep_research_locator_corrections_exact": deep_research_locator_corrections_exact,
        "tensor_arm_specification_blocked": tensor_arm_specification_blocked,
        "deep_research_22_readiness_fail_closed": deep_research_22_readiness_fail_closed,
        "deep_research_22_b1_b4_gap_explicit": deep_research_22_b1_b4_gap_explicit,
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
