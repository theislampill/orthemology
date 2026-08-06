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
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace)[\\/]|/mnt/data/|sandbox:/|file://|"
    r"chatgpt\.com/(?:c|g)/|data-message-id|screen-threadFlyOut)"
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
EXPECTED_SNAPSHOT_FILES = 1186


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_manifest_path(raw):
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

    actual_paths = {
        path.relative_to(snapshot).as_posix()
        for path in snapshot.rglob("*")
        if (path.is_file() or path.is_symlink()) and path.name != "SHA256SUMS"
    }
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
    if not correction_path.is_file():
        issues.append("public custody correction is missing")
        correction = {}
    else:
        correction = yaml.safe_load(correction_path.read_text(encoding="utf-8"))
    if correction.get("public_reproduction_status") != "PARTIAL_REPRODUCTION_ONLY":
        issues.append("public reproduction ceiling is missing or promoted")
    for row in correction.get("repository_sources", []):
        target = root / pathlib.PurePosixPath(row["path"])
        if not target.is_file() or sha256(target) != row["sha256"]:
            repository_source_hash_mismatches += 1
            issues.append("repository source hash mismatch: %s" % row["path"])
    private_exclusions = correction.get("private_exclusions", [])
    if len(private_exclusions) != 4 or any(row.get("public_path") is not None for row in private_exclusions):
        issues.append("private-exclusion custody rows are incomplete")

    if not crosswalk_path.is_file():
        issues.append("public reproduction crosswalk is missing")
        crosswalk = {}
    else:
        crosswalk = yaml.safe_load(crosswalk_path.read_text(encoding="utf-8"))
    if crosswalk.get("public_validator_result") != "PASS_WITH_PARTIAL_REPRODUCTION_CEILING":
        issues.append("crosswalk public ceiling is missing or promoted")
    expected_rounds = {"DEEP_BF", "DEEP_BG", "DEEP_BH", "DEEP_BI", "DEEP_BJ", "DEEP_BK"}
    if set(crosswalk.get("rounds", {})) != expected_rounds:
        issues.append("crosswalk BF-BK round coverage is incomplete")

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
        "repository_source_rows": len(correction.get("repository_sources", [])),
        "repository_source_hash_mismatches": repository_source_hash_mismatches,
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
