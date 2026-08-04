#!/usr/bin/env python3
"""Validate the provenance-safe AR8R V8 public recovery packet."""
from __future__ import annotations

import hashlib
import re
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
V11 = ROOT / "docs" / "project-closure" / "ar8r-v11"
CONNES = V11 / "provenance" / "AR8R-CONNES-RIGIDITY-DISPUTE-RECEIPT-V11.yaml"
OSW15 = V11 / "governance" / "ORTHEMOLOGICAL-SPECIFICATION-WARRANT-OSW-15.yaml"
PRIVATE_PDF_NAME = "C2680D5A-8FAE-11F1-A320-F5FC2CA0B584.pdf"


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
    if CONNES.is_file() and OSW15.is_file():
        connes = yaml.safe_load(CONNES.read_text(encoding="utf-8"))
        expected_dispositions = (
            "NIELSEN_CHALLENGE_REJECTED__SPECIALIST_SETTLEMENT_OPEN",
            "DOES_NOT_REFUTE_EXACT_PUBLIC_OPENAI_OBJECT",
            "REJECTED_AS_PROOF__FATAL_GAPS",
        )
        actual_dispositions = (
            connes.get("openai_result", {}).get("disposition"),
            connes.get("nielsen_critique", {}).get("disposition"),
            connes.get("nielsen_positive_proof", {}).get("disposition"),
        )
        if actual_dispositions != expected_dispositions:
            issues.append("V11 Connes dispute dispositions were collapsed or promoted")
        if connes.get("overall_disposition") != "UNRESOLVED_PENDING_OPERATOR_ALGEBRA_SPECIALIST_REVIEW":
            issues.append("V11 Connes dispute overall status was promoted")
        osw = yaml.safe_load(OSW15.read_text(encoding="utf-8"))
        if len(osw.get("coordinates", [])) != 15:
            issues.append("V11 OSW-15 coordinate coverage changed")
        forbidden = re.compile(r"(?:[A-Za-z]:\\|/mnt/data/|sandbox:|file://|data-message-id|screen-threadFlyOut)", re.I)
        for path in V11.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if PRIVATE_PDF_NAME.lower() in text.lower():
                issues.append(f"private PDF filename entered V11 public tree: {path.relative_to(ROOT)}")
            if forbidden.search(text):
                issues.append(f"private locator entered V11 public tree: {path.relative_to(ROOT)}")
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
