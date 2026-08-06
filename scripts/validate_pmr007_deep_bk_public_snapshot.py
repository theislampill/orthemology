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
    r"(?:[A-Za-z]:[\\/](?:Users|workspace)[\\/]|/mnt/data/|sandbox:/|chatgpt\.com/c/)"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest_rows(path):
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        digest, relative = line.split(None, 1)
        rows.append((line_number, digest, relative.strip()))
    return rows


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
    manifest_path = snapshot / "SHA256SUMS"
    if not manifest_path.is_file():
        issues.append("snapshot SHA256SUMS is missing")
        manifest_rows = []
    else:
        manifest_rows = _manifest_rows(manifest_path)
    for line_number, expected, relative in manifest_rows:
        target = snapshot / pathlib.PurePosixPath(relative)
        if not target.is_file() or sha256(target) != expected:
            snapshot_hash_mismatches += 1
            issues.append("snapshot hash mismatch at SHA256SUMS line %d" % line_number)

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
        "snapshot_manifest_rows": len(manifest_rows),
        "snapshot_hash_mismatches": snapshot_hash_mismatches,
        "repository_source_rows": len(correction.get("repository_sources", [])),
        "repository_source_hash_mismatches": repository_source_hash_mismatches,
        "private_exclusion_rows": len(private_exclusions),
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
