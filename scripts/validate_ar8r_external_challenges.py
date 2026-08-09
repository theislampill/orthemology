#!/usr/bin/env python3
"""Validate bounded, nonauthoritative AR8R external challenge custody."""

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


ROOT = pathlib.Path(__file__).resolve().parents[1]
CHALLENGES_REL = pathlib.Path("docs/project-closure/ar8r-v11/post-merge-proposals/external-challenges")
EXPECTED_MANIFEST_HASHES = {
    "challenger-a-common-intervention": "6e758db5a84c6681b2aac6778a8b15f4c8dea0c6ed406f52b84c778adc081981",
    "challenger-b-formal-ancestry": "124cac3847e46e939744bd18c4a3c6d885f34989df22b0df21e22ee854ac8000",
}
EXPECTED_SOURCE_COUNTS = {
    "challenger-a-common-intervention": 1,
    "challenger-b-formal-ancestry": 12,
}
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace|Temp|Documents|Downloads|Desktop)[\\/]|"
    r"(?<![A-Za-z0-9])/(?:home|Users|root|tmp|var/tmp|private/tmp)/|"
    r"/mnt/data/|sandbox:/|file://|chatgpt\.com/(?:c|g)/|data-message-id|"
    r"screen-threadFlyOut)"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(path, expected_digest, issues):
    if not path.is_file() or sha256(path) != expected_digest:
        issues.append(f"challenge source manifest mismatch: {path.parent.name}")
        return {}, False
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
        prefix = "source-files/"
        if not parts[1].startswith(prefix):
            malformed = True
            continue
        relative = parts[1][len(prefix):]
        if relative in observed:
            malformed = True
        observed[relative] = parts[0]
    if malformed:
        issues.append(f"challenge source manifest is malformed: {path.parent.name}")
    return observed, not malformed


def rerun_challenger_b(source, issues):
    script = source / "deep_bv_challenger_countermodels.py"
    supplied_result = source / "deep_bv_challenger_results.json"
    try:
        supplied = json.loads(supplied_result.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        issues.append("Challenger B supplied finite-check result is invalid")
        return False
    with tempfile.TemporaryDirectory() as temporary:
        temporary = pathlib.Path(temporary)
        for item in source.iterdir():
            if item.is_file():
                shutil.copy2(item, temporary / item.name)
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        completed = subprocess.run(
            [sys.executable, str(temporary / script.name)],
            cwd=temporary,
            env=environment,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if completed.returncode != 0:
            issues.append("Challenger B finite checker failed to execute")
            return False
        try:
            reproduced = json.loads((temporary / supplied_result.name).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            issues.append("Challenger B reproduced result is invalid")
            return False
    check = reproduced.get("exhaustive_check", {})
    exact = (
        reproduced == supplied
        and check.get("total_map_pairs_checked") == 87317
        and check.get("attained_range_equivalence_pass") is True
        and check.get("full_codom_equivalence_pass_under_nonempty_target") is True
        and len(reproduced.get("countermodels", [])) == 14
    )
    if not exact:
        issues.append("Challenger B finite checker did not reproduce its bounded result")
    return exact


def validate(root=ROOT, challenges_override=None):
    root = pathlib.Path(root)
    challenges = pathlib.Path(challenges_override) if challenges_override else root / CHALLENGES_REL
    issues = []
    source_hash_mismatches = 0
    private_path_findings = 0
    counts = {}

    for name, expected_manifest_digest in EXPECTED_MANIFEST_HASHES.items():
        challenge = challenges / name
        source = challenge / "source-files"
        expected, manifest_valid = parse_manifest(challenge / "SOURCE_SHA256SUMS", expected_manifest_digest, issues)
        actual = {
            path.relative_to(source).as_posix()
            for path in source.rglob("*")
            if path.is_file() or path.is_symlink()
        } if source.is_dir() else set()
        counts[name] = len(actual)
        if not manifest_valid or actual != set(expected) or len(actual) != EXPECTED_SOURCE_COUNTS[name]:
            issues.append(f"challenge source coverage mismatch: {name}")
        for relative in sorted(actual):
            target = source / pathlib.PurePosixPath(relative)
            if target.is_symlink():
                issues.append(f"challenge symlink is forbidden: {name}/{relative}")
                continue
            try:
                text = target.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                issues.append(f"challenge member is not UTF-8: {name}/{relative}")
                continue
            private_path_findings += len(PRIVATE_PATTERN.findall(text))
            if expected.get(relative) != sha256(target):
                source_hash_mismatches += 1

    for path in challenges.rglob("*"):
        if not path.is_file() or "source-files" in path.parts:
            continue
        try:
            private_path_findings += len(PRIVATE_PATTERN.findall(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            issues.append(f"challenge review member is not UTF-8: {path.relative_to(challenges).as_posix()}")
    if private_path_findings:
        issues.append("private path or browser locator leaked into external challenge custody")
    if source_hash_mismatches:
        issues.append("external challenge source hash mismatch")

    challenger_b = challenges / "challenger-b-formal-ancestry"
    challenger_b_finite_checker_reproduced = False
    if source_hash_mismatches == 0 and private_path_findings == 0:
        challenger_b_finite_checker_reproduced = rerun_challenger_b(challenger_b / "source-files", issues)

    original_lean = challenger_b / "source-files/DeepBVCommonInterventionCriterion.lean"
    try:
        original_text = original_lean.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        original_text = ""
    challenger_b_original_lean_failure_recorded = (
        "spec : CommonInterventionSpec\n" in original_text
        and "  syntax : Syntax" in original_text
        and sha256(original_lean) == "62663384281c23ff599d0e4bef14c81b9e6f29a4732ed609760b71520adedfe4"
    ) if original_lean.is_file() else False
    if not challenger_b_original_lean_failure_recorded:
        issues.append("Challenger B original Lean failure surface is not preserved")

    repaired = challenger_b / "intake-review/DeepBVCommonInterventionCriterion.repaired.lean"
    receipt_path = challenger_b / "intake-review/LEAN_INTAKE_RECEIPT.json"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        receipt = {}
    challenger_b_repaired_lean_receipt_exact = (
        repaired.is_file()
        and sha256(repaired) == "7b666912629790cb01cbfe8bfcde829238ade5f31bf776728e2f1d911b9fedd3"
        and receipt.get("source_draft_status") == "PARSE_ELABORATION_FAILED"
        and receipt.get("repaired_draft_sha256") == sha256(repaired)
        and receipt.get("lean_version") == "4.32.2"
        and receipt.get("standalone_parse_elaboration_kernel") == "PASS"
        and receipt.get("project_build") == "NOT_RUN_NOT_APPLICABLE_TO_EXTERNAL_CHALLENGE"
        and receipt.get("owner_adoption") == "PENDING"
        and receipt.get("repository_scientific_adoption") == "NONE"
        and receipt.get("general_novelty") == 0
    )
    if not challenger_b_repaired_lean_receipt_exact:
        issues.append("Challenger B repaired Lean receipt mismatch")

    return {
        "schema": "ar8r-external-challenge-custody-validation-v1",
        "result": "FAIL" if issues else "PASS_NONAUTHORITATIVE_CHALLENGE_CUSTODY",
        "challenger_a_source_files": counts.get("challenger-a-common-intervention", 0),
        "challenger_b_source_files": counts.get("challenger-b-formal-ancestry", 0),
        "source_hash_mismatches": source_hash_mismatches,
        "private_path_findings": private_path_findings,
        "challenger_b_finite_checker_reproduced": challenger_b_finite_checker_reproduced,
        "challenger_b_original_lean_failure_recorded": challenger_b_original_lean_failure_recorded,
        "challenger_b_repaired_lean_receipt_exact": challenger_b_repaired_lean_receipt_exact,
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
