#!/usr/bin/env python3
"""Validate the provenance-safe AR8R V8 public recovery packet."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "project-closure" / "ar8r-v8"
INDEX = PACKET / "AR8R-V8-IDENTITY-INDEX.yaml"
EXPECTED = [*(f"AR8R-T{i}" for i in range(130, 156)), "AR8R-T307",
            *(f"AR8R-T{i}" for i in range(309, 319)),
            *(f"AR8R-T{i}" for i in range(351, 355)), "AR8R-T366"]
EXACT = {*(f"AR8R-T{i}" for i in range(130, 144)), *(f"AR8R-T{i}" for i in range(351, 355))}
ALLOWED = {
    "EXACT_VERBATIM_TRANSCRIPT_RECOVERY",
    "CANONICAL_SEMANTIC_RECONSTRUCTION",
    "ROLE_PRESERVING_REPLACEMENT",
    "HISTORICAL_IDENTITY_ONLY",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> list[str]:
    issues: list[str] = []
    if not INDEX.exists():
        return [f"missing AR8R V8 identity index: {INDEX.relative_to(ROOT)}"]
    try:
        data = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"identity index unreadable: {exc}"]
    rows = data.get("identities", []) if isinstance(data, dict) else []
    ids = [row.get("historical_identity") for row in rows if isinstance(row, dict)]
    if len(rows) != 42 or set(ids) != set(EXPECTED) or len(ids) != len(set(ids)):
        issues.append("identity index must contain each of the 42 target identities exactly once")
    for row in rows:
        if not isinstance(row, dict):
            issues.append("identity index contains a non-object row"); continue
        tid = row.get("historical_identity")
        provenance = row.get("provenance_class")
        if provenance not in ALLOWED:
            issues.append(f"{tid}: invalid provenance class {provenance!r}")
        if tid in EXACT:
            if provenance != "EXACT_VERBATIM_TRANSCRIPT_RECOVERY":
                issues.append(f"{tid}: exact historical payload has wrong provenance")
            rel = row.get("payload_path")
            path = ROOT / rel if isinstance(rel, str) else None
            if path is None or not path.is_file():
                issues.append(f"{tid}: payload file missing")
            elif digest(path) != row.get("payload_sha256"):
                issues.append(f"{tid}: payload hash mismatch")
        elif row.get("original_historical_bytes_recovered") is not False:
            issues.append(f"{tid}: unavailable original bytes must remain explicitly false")
    by_id = {row.get("historical_identity"): row for row in rows if isinstance(row, dict)}
    if by_id.get("AR8R-T150", {}).get("provenance_class") != "ROLE_PRESERVING_REPLACEMENT":
        issues.append("AR8R-T150 must map only to a role-preserving replacement")
    if by_id.get("AR8R-T366", {}).get("provenance_class") != "CANONICAL_SEMANTIC_RECONSTRUCTION":
        issues.append("AR8R-T366 must remain a post hoc semantic reconstruction")
    if by_id.get("AR8R-T354", {}).get("audit_status") != "BLOCKED_FORMAL_DEFECT":
        issues.append("AR8R-T354 blocking preorder defect must remain explicit")
    unresolved = [row for row in rows if row.get("provenance_class") == "HISTORICAL_IDENTITY_ONLY"]
    if len(unresolved) != 22:
        issues.append(f"expected 22 unresolved historical identities, found {len(unresolved)}")
    if data.get("historical_ar8r_duration") != "09:41:25.405101139":
        issues.append("historical AR8R duration changed")
    return issues


def main() -> int:
    issues = validate()
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    print("AR8R V8 recovery packet: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
