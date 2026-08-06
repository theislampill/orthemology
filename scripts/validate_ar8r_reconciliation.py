#!/usr/bin/env python3
"""Validate the bounded AR8R V11 campaign-reconciliation packet."""

from __future__ import annotations

import sys
import csv
import hashlib
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "project-closure" / "ar8r-v11"
CATALOG = PACKET / "AR8R-V11-EVIDENCE-CATALOG.yaml"
LEDGER = PACKET / "AR8R-V11-RECONCILIATION-LEDGER.yaml"
FIXTURE = PACKET / "governance" / "FALSE-ZERO-NEGATIVE-FIXTURE.yaml"
PROJECTION = PACKET / "governance" / "CURRENT-CAMPAIGN-PROJECTION.yaml"
ORIGIN_V5 = PACKET / "provenance" / "AR8R-CANONICAL-THEOREM-ORIGIN-REGISTRY-V5-PUBLIC-SANITIZED.yaml"
ORIGIN_V6 = PACKET / "provenance" / "AR8R-CANONICAL-THEOREM-ORIGIN-REGISTRY-V6.yaml"
RECOVERY_OVERLAY = PACKET / "provenance" / "AR8R-TARGET-IDENTITY-RECOVERY-OVERLAY-V8.yaml"
SOURCE_UNIVERSE = PACKET / "provenance" / "AR8R-SOURCE-UNIVERSE-RECEIPT-V1.yaml"
SOURCE_UNIVERSE_V2 = PACKET / "provenance" / "AR8R-SOURCE-UNIVERSE-RECEIPT-V2.yaml"
HISTORICAL_COLLISION_RECEIPT = PACKET / "provenance" / "AR8R-HISTORICAL-ID-COLLISION-RECEIPT-P236-P242-V1.yaml"
HISTORICAL_COLLISION_PAYLOAD = PACKET / "theorems" / "historical-collision-recoveries" / "AR8R-HR-P236P242-T236-v1-payload.md"
POST_MERGE_CATALOG = PACKET / "AR8R-V11-POST-MERGE-EVIDENCE-CATALOG.yaml"
THREAD_CUSTODY = PACKET / "provenance" / "AR8R-POST-MERGE-THREAD-CUSTODY-RECEIPT-V1.yaml"
LINK_DRIFT = PACKET / "provenance" / "AR8R-POST-MERGE-LINK-DRIFT-SUMMARY-V1.yaml"
PMR007_RECEIPT = PACKET / "provenance" / "AR8R-PMR007-ROUNDS11-20-PROPOSAL-RECEIPT.yaml"
PMR007_PROPOSAL = PACKET / "post-merge-proposals" / "pmr007-rounds11-20"
PMR007_CORRECTION = PACKET / "post-merge-proposals" / "PMR007-ROUNDS11-20-ADOPTION-BOUNDARY-CORRECTION.md"
PMR007_DEEP_RECEIPT = PACKET / "provenance" / "AR8R-PMR007-DEEP-A-AP-PROPOSAL-RECEIPT-V1.yaml"
PMR007_DEEP_EXECUTION = PACKET / "provenance" / "AR8R-PMR007-DEEP-A-AP-EXECUTION-RECEIPT-V1.yaml"
PMR007_DEEP_PROPOSAL = PACKET / "post-merge-proposals" / "pmr007-deep-a-ap"
PMR007_DEEP_CORRECTION = PACKET / "post-merge-proposals" / "PMR007-DEEP-A-AP-ADOPTION-BOUNDARY-CORRECTION.md"
VISIBLE_SOURCE_MANIFEST = PACKET / "provenance" / "AR8R-POST-MERGE-VISIBLE-FILE-CARD-MANIFEST-V1.yaml"
FILE_CARD_ARCHIVE_CONFLICTS = PACKET / "provenance" / "AR8R-POST-MERGE-FILE-CARD-ARCHIVE-CONFLICTS-V1.yaml"
SOURCE_RECEIPTS = (
    PACKET / "provenance" / "AR8R-FULL-PROGRAM-REENTRY-V2-SOURCE-RECEIPT.yaml",
    PACKET / "provenance" / "AR8R-POST-MERGE-PMR001-SOURCE-RECEIPT.yaml",
    PACKET / "provenance" / "AR8R-POST-MERGE-PMR002-006-SOURCE-RECEIPT.yaml",
)

PROGRAMS = PACKET / "programs"
PROVENANCE = PACKET / "provenance"
FORMALIZATION = PACKET / "formalization"
DEFERRED_EXACT = PROGRAMS / "deferred-candidate-source" / "exact"
DEEP_CONTEXT_RECEIPT = PROVENANCE / "AR8R-DEEP-CONTEXT-SOURCE-RECEIPT-V11.yaml"
A_TO_N = PROGRAMS / "AR8R-THREE-TRACK-A-TO-N-ARCHITECTURE-V11.yaml"
BRIDGE_LEDGER = PROGRAMS / "AR8R-TRANSCENDENTAL-BRIDGE-AND-RIVAL-LEDGER-V11.yaml"
PROPER_FUNCTION_MATRIX = PROGRAMS / "AR8R-PROPER-FUNCTION-TYPED-MATRIX-V11.yaml"
ONTOLOGY_MATRIX = PROGRAMS / "AR8R-ONTOLOGY-AND-REPRESENTATION-ALTERNATIVES-MATRIX-V11.yaml"
TAC_REGISTRY = PROGRAMS / "AR8R-TAC-SAC-TYPED-COORDINATE-AND-COUNTERMODEL-REGISTRY-V11.yaml"
PMR_MAP = FORMALIZATION / "AR8R-PMR007-TEN-RESULT-FORMALIZATION-MAP-V11.yaml"
LEAN_QUEUE = FORMALIZATION / "AR8R-V11-LEAN-FORMALIZATION-QUEUE.yaml"
TEN_CONFLICT = PROVENANCE / "AR8R-TEN-ADVANCES-STATIC-CONFLICT-RECEIPT-V11.yaml"
FAMILY_CROSSWALK = PROVENANCE / "AR8R-THEOREM-FAMILY-RELATION-CROSSWALK-V11.yaml"
CONNES_RECEIPT = PROVENANCE / "AR8R-CONNES-RIGIDITY-DISPUTE-RECEIPT-V11.yaml"
LEAN_V6 = PROVENANCE / "AR8R-LEAN-STATUS-MAP-V6.yaml"
LEAN_V7 = PROVENANCE / "AR8R-LEAN-STATUS-MAP-V7.yaml"
OSW15 = PACKET / "governance" / "ORTHEMOLOGICAL-SPECIFICATION-WARRANT-OSW-15.yaml"
SURFACE_CUSTODY = PROGRAMS / "program-surface-and-correction-custody.yaml"
FLYWHEEL = PROGRAMS / "AR8R-RESEARCH-FLYWHEEL-CROSSWALK-V1.yaml"
MILESTONE_CHARTER = PROGRAMS / "AR8R-ORTHEMOLOGY-MENISCUS-MILESTONE-ARCHITECTURE-V1.md"
MILESTONES = PROGRAMS / "AR8R-ORTHEMOLOGY-MENISCUS-MILESTONES-V1.yaml"
OSM_PROGRAM_CROSSWALK = PROGRAMS / "AR8R-OSM-LEARNING-TRAJECTORY-CONVERGENCE-CROSSWALK-V12.yaml"
OSM_PROGRAM_NOTE = PROGRAMS / "AR8R-OSM-LEARNING-TRAJECTORY-CONVERGENCE-CROSSWALK-V12.md"
FABLE_OSM_PROMPT = PROGRAMS / "AR8R-FABLE-OSM-CONVERGENCE-RESEARCH-PROMPT-V1.md"
FABLE_INTEGRATED_PROMPT = PROGRAMS / "AR8R-FABLE-INTEGRATED-ORTHEMOLOGY-MENISCUS-RESEARCH-PROMPT-V2.md"
FABLE_INTEGRATED_PROMPT_SHA256 = "0588405a041ea825e958089354508f2fe4ee7c4e586afe56cb0f42cded46c8f2"
COMPATIBILITY_OVERLAY = PROGRAMS / "AR8R-FULL-PROGRAM-REENTRY-COMPATIBILITY-RESOLUTION-V11.yaml"
ASCENT_V2 = PROGRAMS / "AR8R_TRANSCENDENTAL_ORTHABILITY_AND_SOURCE_ASCENT_V2.yaml"
TWO_THREAD_RECEIPT = PROVENANCE / "AR8R-TWO-THREAD-SYNTHESIS-RECEIPT-V11.yaml"
CURRENT_STATE = ROOT / "docs" / "current-state.yaml"
GITIGNORE = ROOT / ".gitignore"

EXPECTED_DEFERRED_SOURCE: dict[str, tuple[int, str]] = {
    "candidate-e/000045__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__ARGUMENT.md": (7630, "17fcba74e46f016ffe8c4d84c5248f4692e03052ac30dd3df1789f62a94cc14a"),
    "candidate-e/000046__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__CHAMPION_CHALLENGER_HISTORY.md": (270, "d9054bb7c6e755b665c1de0e2270c7cf36e1cb7ce15eb66d3a85b3394085d937"),
    "candidate-e/000047__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__COUNTERMODELS.md": (4833, "ecccc524f85cb02834ec8bf0fe602d183f1e26fe348e58a7f3776da80b20b845"),
    "candidate-e/000048__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__FORMAL_RECONSTRUCTION.md": (5378, "774d241695b4e8df5865008918d4e601a2e26f6d9c31bea034b3351c14b810c3"),
    "candidate-e/000049__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__HISTORY__ARGUMENT_WAVE1.md": (1027, "639811260d6bdca6ddbef3c5a33b14fb35bbab475ed83a1d9fbb1c99c9bd4f33"),
    "candidate-e/000050__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__HISTORY__FORMAL_RECONSTRUCTION_WAVE1.md": (708, "59d4d899019c71d64e4a24fc51b6ec902d3c032506f596f4707cdf8f33e1d3c2"),
    "candidate-e/000051__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__INDEPENDENT_AUDIT.md": (563, "895b1d65c37af6661c8fe8b3f8a020053e12c7b40d34750b7b3544001c06d19b"),
    "candidate-e/000052__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__NOVELTY_AUDIT.md": (2841, "34be7fd80c8f97ab348859291b412a7fc0a59e6fce418b1de289b2a9014c468e"),
    "candidate-e/000053__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__PREMISE_DEFENSES.md": (4164, "f62deeaa161d3584356bfdfdae70a3a9d308318b3f2609d9af8f7d945cade468"),
    "candidate-e/000054__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__RIVAL_REPAIRS.md": (2804, "0e0e8e7031119eec0ecc53d104e864f90f02d91086cf793c78a1ebbc4bf03101"),
    "candidate-e/000055__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__E-orthability-fittingness__SOURCE_LINEAGE.md": (3156, "840079607e2ad257aab11b29863167b1cf279b1f66bd6dbe9aecaae9f124f7da"),
    "candidate-g/000065__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__ARGUMENT.md": (3694, "cb6021b4a7a1363ba77ece8e1c8e9d6d9a1b923ec9a27ed6bd14fccb2f822f7f"),
    "candidate-g/000066__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__CHAMPION_CHALLENGER_HISTORY.md": (389, "266465cf71ce357b28139f92dc4b31fb7f8466693158cd3b163fae9789383154"),
    "candidate-g/000067__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__COUNTERMODELS.md": (2042, "8ee0b2350c20d29e017723496ead010bae3cfd064daf58435bd4526f0dfb922c"),
    "candidate-g/000068__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__DERIVATIONAL_UNIFICATION_PARITY_THEOREM.md": (5832, "781eb3cba34cc9c79b077d417abb9eb0c83c5274e234922ff895560521c637e6"),
    "candidate-g/000069__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__FORMAL_RECONSTRUCTION.md": (2492, "6b3828ec336a3c2ce442232b4b1fc4c8a00920b481485f82573a569a59c50930"),
    "candidate-g/000070__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__INDEPENDENT_AUDIT.md": (64, "910e43e7547caf7988080201b652350c03cb8144bbc9566758e08cd708385326"),
    "candidate-g/000071__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__NOVELTY_AUDIT.md": (1128, "1cb9a1b6b745835fb82e475e4e58367040a61891418a40658f828523f5f95754"),
    "candidate-g/000072__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__PREMISE_DEFENSES.md": (3464, "a5c0de7f2e4cad97f81c5558c13a52143f3a9f90d815070646d17f8ae31ff8df"),
    "candidate-g/000073__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__RIVAL_REPAIRS.md": (2068, "3ff52bd174ec90b341bc675351528e8370b8765065389e6e0d738104beb286e8"),
    "candidate-g/000074__ar7-reopened-audit-continuation__payload__ar7-complete__CANDIDATES__G-unity-agency-wisdom__SOURCE_LINEAGE.md": (209, "b57b4aaac8addd1b3f58c4ccf5a03c8b57c735b280f2dec890af97d0e1da2a9d"),
    "integration/A_TO_N_COMPREHENSIVE_INTEGRATION_MAP.yaml": (24015, "cc1eefd4db0af89f5f948ccfffb0a8f15b8d12468d23c3a4cf5e4eb2f05c34c8"),
    "integration/THREE_TRACK_PROGRAM_MAP.md": (1809, "14774f2ecf57dc3d78ee2ef5ab3d514ffaa29d8059f2926131b581b94b4ac62a"),
    "integration/THREE_TRACK_TYPED_DEPENDENCY_GRAPH.yaml": (3583, "09a38d7482a64bc49b112a0d82bd0f1bebff9647eb65bc36e1a49f82cec7fd4a"),
}

EXPECTED_PMR007 = {
    "PMR-007-MLT-1",
    "PMR-007-SMRB-1",
    "PMR-007-FRLA-1",
    "PMR-007-COB-1",
    "PMR-007-TRC-1",
    "PMR-007-VCT-1",
    "PMR-007-RSD-1",
    "PMR-007-ORTC-V4",
    "PMR-007-PRQT-1",
    "PMR-007-PRRC-1",
}

EXPECTED_PMR007_DEEP = {
    "PMR-007-NFG-1", "PMR-007-DURP-1", "PMR-007-ICR-1", "PMR-007-UGEN-1",
    "PMR-007-TNAC-1", "PMR-007-FPF-1", "PMR-007-CBA-1", "PMR-007-UAP-1",
    "PMR-007-OAS-1", "PMR-007-UCA-1", "PMR-007-WFB-1", "PMR-007-SDL-1",
    "PMR-007-ETRP-1", "PMR-007-ANH-1", "PMR-007-GUPP-1", "PMR-007-TRPF-1",
    "PMR-007-FEAG-1", "PMR-007-R5CU-1", "PMR-007-SCRF-1", "PMR-007-MACC-1",
    "PMR-007-TRPD-1", "PMR-007-SWPC-1", "PMR-007-TIPC-1", "PMR-007-TKAA-1",
    "PMR-007-PFSA-1", "PMR-007-COWC-1", "PMR-007-CGIP-1", "PMR-007-FSPW-1",
    "PMR-007-SRVN-1", "PMR-007-RSMF-1", "PMR-007-IHDU-1", "PMR-007-NRID-1",
    "PMR-007-R5NR-1", "PMR-007-SDIG-1", "PMR-007-NMIB-1", "PMR-007-CIOB-1",
    "PMR-007-SAMC-1", "PMR-007-EGAC-1", "PMR-007-SRIN-1", "PMR-007-ABPD-1",
    "PMR-007-RPDS-1", "PMR-007-SWRI-1",
}

EXPECTED_MILESTONE_STATUSES = {
    **{f"M{i}": "ACTIVE_RESEARCH_PROGRAM" for i in (4, 5, 6, 8, 9, 10, 11, 13, 18)},
    **{f"M{i}": "PARTIALLY_IMPLEMENTED" for i in (1, 2, 3, 7, 12, 14, 16)},
    "M15": "BLOCKED_ON_EMPIRICAL_EVIDENCE",
    "M17": "BLOCKED_ON_SPECIALIST_REVIEW",
}
EXPECTED_MENISCUS_REQUIREMENTS = {
    "MEN-1": {"M1", "M3", "M4", "M5", "M6", "M12", "M14"},
    "MEN-2": {"M4", "M5", "M6", "M8", "M9", "M13"},
    "MEN-3": {"M3", "M7", "M8", "M9", "M10", "M15"},
    "MEN-4": {"M1", "M7", "M8", "M9", "M13", "M14"},
    "MEN-5": {"M2", "M12", "M13", "M14", "M17"},
    "MEN-6": {"M5", "M7", "M8", "M9", "M14"},
    "MEN-7": {"M1", "M2", "M10", "M11", "M12", "M13", "M17"},
    "MEN-8": {"M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M14"},
    "MEN-9": {"M1", "M3", "M6", "M8", "M12", "M15", "M18"},
}
EXPECTED_MILESTONE_SOURCE_CLASSES = {
    "CURRENT_PUBLIC_ORTHEMOLOGY_MAIN",
    "EXACT_HISTORICAL_AR8R_EVIDENCE",
    "POST_MERGE_PMR_PROPOSAL",
    "NEW_V11_ANALYSIS",
    "OWNER_SYNTHETIC_NOETIC_DRAFT",
    "DAEE_CURRENT_MAIN",
    "DAEE_DRAFT_PR_8",
    "DAEE_DRAFT_PR_9",
    "EXTERNAL_MATHEMATICS",
    "UNRESOLVED_OR_MISSING_EVIDENCE",
}

OPEN_TOKENS = (
    "OPEN",
    "PENDING",
    "PARTIAL",
    "CONTRADICTORY",
    "BLOCKED",
    "UNAUDITED",
    "REPAIR_REQUIRED",
)
TERMINAL_SUMMARY_STATES = {"MENISCUS_REACHED", "NATURAL_CLOSURE"}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


V11_TERMINAL_MAP_FIELDS = {
    "AR8R-V11-ATTACHMENT-ROW-DISPOSITION-MAP-V1.csv": [
        "row_id", "item_kind", "expansion_status", "has_href", "disposition",
    ],
    "AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv": [
        "row_id", "surface", "kind", "sha256", "bytes", "source_status", "disposition",
    ],
    "AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv": [
        "archive_sequence", "sha256", "bytes", "member_count", "integrity_status", "disposition",
    ],
    "AR8R-V11-ARCHIVE-MEMBER-HASH-DISPOSITION-MAP-V1.csv": [
        "member_sha256", "occurrence_count", "member_bytes", "disposition",
    ],
}

V11_GENERATED_SOURCE_UNIVERSE_NAMES = set(V11_TERMINAL_MAP_FIELDS) | {
    "AR8R-SOURCE-UNIVERSE-RECEIPT-V2.yaml",
}


def _is_lower_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _is_positive_decimal(value: Any) -> bool:
    return isinstance(value, str) and value.isdigit() and int(value) > 0


def public_hash_evidence() -> tuple[set[str], set[str]]:
    """Return exact public file hashes and hashes mentioned outside V11 generated maps."""
    exact: set[str] = set()
    mentioned: set[str] = set()
    text_suffixes = {".csv", ".json", ".jsonl", ".md", ".py", ".sha256", ".txt", ".yaml", ".yml"}
    tracked = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.split(b"\0")
    for raw_path in tracked:
        if not raw_path:
            continue
        path = ROOT / raw_path.decode("utf-8")
        if not path.is_file() or path.name in V11_GENERATED_SOURCE_UNIVERSE_NAMES:
            continue
        data = path.read_bytes()
        exact.add(hashlib.sha256(data).hexdigest())
        if path.suffix.lower() in text_suffixes:
            text = data.decode("utf-8", errors="ignore").lower()
            mentioned.update(re.findall(r"\b[0-9a-f]{64}\b", text))
    return exact, mentioned


def validate_v11_terminal_map_rows(
    name: str,
    fieldnames: list[str] | None,
    rows: list[dict[str, str]],
    *,
    public_exact_hashes: set[str] | None = None,
    public_mentioned_hashes: set[str] | None = None,
) -> list[str]:
    """Validate privacy-safe V11 terminal maps as typed, fail-closed records."""
    issues: list[str] = []
    expected_fields = V11_TERMINAL_MAP_FIELDS.get(name)
    if expected_fields is None:
        return [f"unexpected-v11-terminal-map:{name}"]
    if fieldnames != expected_fields:
        issues.append(f"v11-terminal-map-header-mismatch:{name}")

    if name == "AR8R-V11-ATTACHMENT-ROW-DISPOSITION-MAP-V1.csv":
        if [row.get("row_id") for row in rows] != [str(index) for index in range(1, 1008)]:
            issues.append("v11-attachment-row-sequence-mismatch")
        expected_counts = {"CARD": 152, "LINK": 3, "BUTTON": 852}
        if Counter(row.get("item_kind") for row in rows) != expected_counts:
            issues.append("v11-attachment-kind-count-mismatch")
        if any(row.get("expansion_status") != "EXPANDED" for row in rows):
            issues.append("v11-attachment-expansion-status-mismatch")
        if Counter(row.get("has_href") for row in rows) != {"False": 1004, "True": 3}:
            issues.append("v11-attachment-href-count-mismatch")
        if any(
            row.get("disposition") != "PRIVATE_UI_INVENTORY_ROW_ACCOUNTED_NO_PUBLIC_BODY_IMPORT"
            for row in rows
        ):
            issues.append("v11-attachment-disposition-mismatch")

    elif name == "AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv":
        if [row.get("row_id") for row in rows] != [str(index) for index in range(1, 188)]:
            issues.append("v11-download-row-sequence-mismatch")
        if Counter(row.get("surface") for row in rows) != {"FILE_CARD": 161, "RESPONSE_LEVEL_BUTTON_CONTROL": 26}:
            issues.append("v11-download-surface-count-mismatch")
        if Counter(row.get("kind") for row in rows) != {"DOWNLOAD": 159, "USER_UPLOAD": 2, "BUTTON_CONTROL_DOWNLOAD": 26}:
            issues.append("v11-download-kind-count-mismatch")
        expected_status_counts = {
            "DOWNLOADED_AND_HASHED": 178,
            "DOWNLOAD_FAILED": 6,
            "DOWNLOAD_FAILED_RETRY": 1,
            "HISTORICAL_LINK_UNAVAILABLE": 1,
            "VIEWER_OPENED_NO_SUPPORTED_DOWNLOAD": 1,
        }
        if Counter(row.get("source_status") for row in rows) != expected_status_counts:
            issues.append("v11-download-source-status-count-mismatch")
        expected_disposition_counts = {
            "EXACT_PUBLIC_BYTES_PRESENT": 137,
            "PRIVATE_CUSTODY_OR_VERIFICATION_RECEIPT_NO_PUBLIC_IMPORT": 9,
            "SUPERSEDED_FAILED_ATTEMPT_MATCHED_TO_LATER_SUCCESS": 7,
            "PUBLIC_HASH_RECEIPTED_NO_DUPLICATE_IMPORT": 13,
            "PUBLIC_SAFE_SOURCE_SUMMARIZED_NOT_IMPORTED": 4,
            "SUPERSEDED_OR_REJECTED_PROPOSAL_NOT_IMPORTED": 3,
            "HISTORICAL_LINK_UNAVAILABLE_WITH_PRIVATE_BOUNDARY_EVIDENCE": 1,
            "VIEWER_OPENED_NO_SUPPORTED_DOWNLOAD": 1,
            "CHECKSUM_SIDECAR_HASH_ONLY_NO_PUBLIC_IMPORT": 11,
            "SUPERSEDED_BOUNDARY_CHECKPOINT_PRIVATE_NO_PUBLIC_IMPORT": 1,
        }
        if Counter(row.get("disposition") for row in rows) != expected_disposition_counts:
            issues.append("v11-download-disposition-count-mismatch")
        no_byte_pairs = {
            "DOWNLOAD_FAILED": "SUPERSEDED_FAILED_ATTEMPT_MATCHED_TO_LATER_SUCCESS",
            "DOWNLOAD_FAILED_RETRY": "SUPERSEDED_FAILED_ATTEMPT_MATCHED_TO_LATER_SUCCESS",
            "HISTORICAL_LINK_UNAVAILABLE": "HISTORICAL_LINK_UNAVAILABLE_WITH_PRIVATE_BOUNDARY_EVIDENCE",
            "VIEWER_OPENED_NO_SUPPORTED_DOWNLOAD": "VIEWER_OPENED_NO_SUPPORTED_DOWNLOAD",
        }
        for index, row in enumerate(rows, 1):
            status = row.get("source_status")
            digest = row.get("sha256")
            size = row.get("bytes")
            if status == "DOWNLOADED_AND_HASHED":
                if not _is_lower_sha256(digest) or not _is_positive_decimal(size):
                    issues.append(f"v11-download-hash-or-size-malformed:{index}")
            else:
                if digest or size or row.get("disposition") != no_byte_pairs.get(status):
                    issues.append(f"v11-download-access-boundary-incoherent:{index}")
            disposition = row.get("disposition")
            if disposition == "EXACT_PUBLIC_BYTES_PRESENT" and public_exact_hashes is not None and digest not in public_exact_hashes:
                issues.append(f"v11-download-public-bytes-absent:{index}")
            if disposition == "PUBLIC_HASH_RECEIPTED_NO_DUPLICATE_IMPORT" and public_mentioned_hashes is not None and digest not in public_mentioned_hashes:
                issues.append(f"v11-download-public-receipt-absent:{index}")

    elif name == "AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv":
        if [row.get("archive_sequence") for row in rows] != [str(index) for index in range(1, 11)]:
            issues.append("v11-archive-sequence-mismatch")
        if Counter(row.get("disposition") for row in rows) != {
            "PUBLIC_HASH_RECEIPTED_PRIVATE_ARCHIVE_NOT_IMPORTED": 9,
            "SUPERSEDED_BOUNDARY_CHECKPOINT_PRIVATE_NO_PUBLIC_IMPORT": 1,
        }:
            issues.append("v11-archive-disposition-count-mismatch")
        for index, row in enumerate(rows, 1):
            if not _is_lower_sha256(row.get("sha256")):
                issues.append(f"v11-archive-hash-malformed:{index}")
            if not _is_positive_decimal(row.get("bytes")) or not _is_positive_decimal(row.get("member_count")):
                issues.append(f"v11-archive-count-or-size-malformed:{index}")
            if row.get("integrity_status") != "PASS":
                issues.append(f"v11-archive-integrity-regression:{index}")
            if (
                row.get("disposition") == "PUBLIC_HASH_RECEIPTED_PRIVATE_ARCHIVE_NOT_IMPORTED"
                and public_mentioned_hashes is not None
                and row.get("sha256") not in public_mentioned_hashes
            ):
                issues.append(f"v11-archive-public-receipt-absent:{index}")
        if sum(int(row["member_count"]) for row in rows if _is_positive_decimal(row.get("member_count"))) != 957:
            issues.append("v11-archive-member-total-mismatch")

    elif name == "AR8R-V11-ARCHIVE-MEMBER-HASH-DISPOSITION-MAP-V1.csv":
        hashes = [row.get("member_sha256") for row in rows]
        if any(not _is_lower_sha256(digest) for digest in hashes):
            issues.append("v11-archive-member-hash-malformed")
        if hashes != sorted(set(hashes)):
            issues.append("v11-archive-member-hash-order-or-uniqueness-mismatch")
        if Counter(row.get("disposition") for row in rows) != {
            "EXACT_PUBLIC_BYTES_PRESENT": 173,
            "PRIVATE_OR_DUPLICATE_OR_UNSELECTED_ARCHIVE_MEMBER_NO_PUBLIC_IMPORT": 284,
            "PUBLIC_HASH_RECEIPTED_NO_DUPLICATE_IMPORT": 49,
        }:
            issues.append("v11-archive-member-disposition-count-mismatch")
        for index, row in enumerate(rows, 1):
            if not _is_positive_decimal(row.get("occurrence_count")) or not _is_positive_decimal(row.get("member_bytes")):
                issues.append(f"v11-archive-member-count-or-size-malformed:{index}")
            digest = row.get("member_sha256")
            disposition = row.get("disposition")
            if disposition == "EXACT_PUBLIC_BYTES_PRESENT" and public_exact_hashes is not None and digest not in public_exact_hashes:
                issues.append(f"v11-archive-member-public-bytes-absent:{index}")
            if disposition == "PUBLIC_HASH_RECEIPTED_NO_DUPLICATE_IMPORT" and public_mentioned_hashes is not None and digest not in public_mentioned_hashes:
                issues.append(f"v11-archive-member-public-receipt-absent:{index}")
        if sum(int(row["occurrence_count"]) for row in rows if _is_positive_decimal(row.get("occurrence_count"))) != 957:
            issues.append("v11-archive-member-occurrence-total-mismatch")

    return list(dict.fromkeys(issues))


def validate_integrated_fable_prompt(text: str) -> list[str]:
    issues: list[str] = []
    required = (
        "FABLE_LOCAL_START.md",
        "FABLE_LOCAL_SOURCES/s41586-024-08548-w.md",
        "git check-ignore",
        "Never add either path with `git add -f`",
        "AR8R-HR-P236P242-T236-v1",
        "two rival candidate cores",
        "proper functionalism",
        "nominalism, conceptualism, property dualism",
        "TAC, SAC, Tachikoma",
        "uncreated-grammar constraints",
        "guarded Necessary-Being ascent",
        "Lean formalization",
        "fable/ar8r-convergence-research-v1",
        "Never push to\n`main`",
        "natural campaign closure: NOT_REACHED",
    )
    if any(token not in text for token in required):
        issues.append("integrated-fable-prompt-guard-missing")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != FABLE_INTEGRATED_PROMPT_SHA256:
        issues.append("integrated-fable-prompt-hash-mismatch")
    return issues


def status_is_open(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    upper = value.upper()
    return any(token in upper for token in OPEN_TOKENS)


def lower_level_open_records(document: dict[str, Any]) -> list[str]:
    open_records: list[str] = []
    ledgers = document.get("ledgers", {})
    if not isinstance(ledgers, dict):
        return ["malformed-ledgers"]
    for family, records in ledgers.items():
        if not isinstance(records, list):
            open_records.append(f"{family}:malformed")
            continue
        for record in records:
            if not isinstance(record, dict):
                open_records.append(f"{family}:malformed-record")
                continue
            if status_is_open(record.get("status")):
                open_records.append(f"{family}:{record.get('id', '?')}")
            pending = record.get("pending_burdens", [])
            if isinstance(pending, list):
                open_records.extend(f"{family}:{record.get('id', '?')}:{burden}" for burden in pending)
    return open_records


def validate_campaign_state(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-campaign-document"]
    summary = document.get("summary", {})
    if not isinstance(summary, dict):
        return ["malformed-summary"]

    issues: list[str] = []
    open_records = lower_level_open_records(document)
    reported = summary.get("reported_open_burden_count")
    closed_claim = (
        summary.get("campaign_status") in TERMINAL_SUMMARY_STATES
        or summary.get("natural_closure") is True
        or reported == 0
    )
    if closed_claim and open_records:
        issues.append("summary-overrides-open-lower-level-records")
    if not isinstance(reported, int) or reported != len(open_records):
        issues.append("open-burden-count-mismatch")

    champion = summary.get("integrated_champion")
    candidates = document.get("ledgers", {}).get("candidates", [])
    if champion and isinstance(candidates, list):
        selected = next(
            (
                item
                for item in candidates
                if isinstance(item, dict) and item.get("id") == champion
            ),
            None,
        )
        if selected and selected.get("pending_burdens"):
            issues.append("champion-has-pending-burdens")
    return list(dict.fromkeys(issues))


def validate_post_merge_catalog(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-post-merge-catalog"]
    issues: list[str] = []
    rows = document.get("pmr007_proposals", [])
    if not isinstance(rows, list):
        return ["malformed-pmr007-proposals"]
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    if len(ids) != len(rows) or len(ids) != len(set(ids)) or set(ids) != EXPECTED_PMR007:
        issues.append("pmr007-result-coverage-mismatch")
    for row in rows:
        if not isinstance(row, dict):
            issues.append("malformed-pmr007-proposal-row")
            continue
        if row.get("status") != "ADMITTED_POST_MERGE_SCOPED_RESULT":
            issues.append(f"pmr007-proposal-status-mismatch:{row.get('id', '?')}")

    boundary = document.get("pmr007_common_boundary", {})
    expected_boundary = {
        "provenance_class": "NEW_POST_MERGE_SCOPED_RESULT",
        "historical_identity": "NONE",
        "owner_adoption": "PENDING",
        "external_review": "OPEN",
        "repository_readiness": "EXTERNAL_REVIEW_REQUIRED",
        "historical_theorem_origin_credit": "NONE",
    }
    if not isinstance(boundary, dict):
        issues.append("malformed-pmr007-common-boundary")
    else:
        for key, expected in expected_boundary.items():
            if boundary.get(key) != expected:
                issues.append(f"pmr007-boundary-mismatch:{key}")

    source_packets = document.get("source_packets", [])
    deep_source = next(
        (
            row for row in source_packets
            if isinstance(row, dict) and row.get("id") == "PMR007_DEEP_A_THROUGH_AP"
        ),
        None,
    ) if isinstance(source_packets, list) else None
    expected_source = {
        "exact_archive_members": 831,
        "indexed_results": 52,
        "deep_results": 42,
        "disposition": "EXACT_SANITIZED_PROPOSAL_SNAPSHOT_EXTERNAL_REVIEW_AND_OWNER_ADOPTION_REQUIRED",
        "receipt": "provenance/AR8R-PMR007-DEEP-A-AP-PROPOSAL-RECEIPT-V1.yaml",
        "execution_receipt": "provenance/AR8R-PMR007-DEEP-A-AP-EXECUTION-RECEIPT-V1.yaml",
    }
    if not isinstance(deep_source, dict):
        issues.append("pmr007-deep-catalog-source-missing")
    else:
        for key, expected in expected_source.items():
            if deep_source.get(key) != expected:
                issues.append(f"pmr007-deep-catalog-source-mismatch:{key}")

    deep_boundary = document.get("pmr007_deep_a_through_ap_snapshot", {})
    expected_deep_boundary = {
        "path": "post-merge-proposals/pmr007-deep-a-ap",
        "result_index": "post-merge-proposals/pmr007-deep-a-ap/PROPOSED_RESULT_INDEX.yaml",
        "indexed_results": 52,
        "deep_a_through_ap_results": 42,
        "exact_archive_members": 831,
        "historical_identity": "NONE",
        "owner_adoption": "PENDING",
        "external_review": "OPEN",
        "repository_readiness": "EXTERNAL_REVIEW_REQUIRED",
        "general_novelty_credit": "NOT_GRANTED",
        "duplicate_credit_effect": "NONE",
        "integrated_champion": "NONE",
        "meniscus": "MENISCUS_NOT_REACHED",
        "natural_closure": "NOT_REACHED",
        "executable_reproduction": "PARTIAL_WITH_PRECISE_SOURCE_AND_SIDECAR_BOUNDARIES",
    }
    if not isinstance(deep_boundary, dict):
        issues.append("malformed-pmr007-deep-catalog-boundary")
    else:
        for key, expected in expected_deep_boundary.items():
            if deep_boundary.get(key) != expected:
                issues.append(f"pmr007-deep-catalog-boundary-mismatch:{key}")
    return issues


def validate_post_merge_thread_custody(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-post-merge-thread-custody"]
    issues: list[str] = []
    counts = document.get("capture_counts", {})
    expected_counts = {
        "conversation_turn_slots": 30,
        "populated_messages": 24,
        "worked_for_controls": 9,
        "activity_panels_captured": 8,
        "activity_panels_unavailable_with_evidence": 1,
        "total_downloads_hashed": 178,
        "archive_instances_tested": 10,
        "archive_member_rows_hashed": 957,
        "historical_link_drift_incidents": 6,
    }
    if not isinstance(counts, dict):
        issues.append("malformed-post-merge-thread-custody-counts")
    else:
        for key, expected in expected_counts.items():
            if counts.get(key) != expected:
                issues.append(f"post-merge-thread-custody-count-mismatch:{key}")

    expected_privacy_fields = {
        "private_transcript_committed",
        "raw_activity_committed",
        "browser_dom_or_screenshots_committed",
        "message_or_session_identifiers_committed",
        "signed_urls_committed",
        "bulk_private_archives_committed",
    }
    privacy = document.get("privacy_boundary")
    if not isinstance(privacy, dict) or set(privacy) != expected_privacy_fields:
        issues.append("post-merge-privacy-boundary-fields-missing")
    elif any(privacy[key] is not False for key in expected_privacy_fields):
        issues.append("post-merge-private-corpus-publication-violation")
    if document.get("conversation_mutated") is not False or document.get("messages_sent") != 0:
        issues.append("post-merge-conversation-mutation-boundary-mismatch")
    if document.get("github_mutated_by_harvest") is not False:
        issues.append("post-merge-harvest-github-boundary-mismatch")
    return issues


def validate_link_drift(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-historical-link-drift-summary"]
    issues: list[str] = []
    rows = document.get("incidents", [])
    expected_ids = {f"HLCD-V11-{index:03d}" for index in range(1, 7)}
    if document.get("classification") != "HISTORICAL_LINK_CONTENT_DRIFT":
        issues.append("historical-link-drift-classification-mismatch")
    if document.get("incident_count") != 6 or not isinstance(rows, list) or len(rows) != 6:
        issues.append("historical-link-drift-count-mismatch")
        return issues
    ids = {row.get("id") for row in rows if isinstance(row, dict)}
    if ids != expected_ids:
        issues.append("historical-link-drift-id-coverage-mismatch")
    sha_re = re.compile(r"^[0-9a-f]{64}$")
    for row in rows:
        if not isinstance(row, dict):
            issues.append("historical-link-drift-row-incomplete")
            continue
        common = {"id", "response_turn", "control", "expected_archive_sha256", "returned_boundary"}
        returned_keys = {
            key for key in ("returned_verifier_archive_sha256", "returned_sidecar_archive_sha256")
            if key in row
        }
        if not common.issubset(row) or len(returned_keys) != 1:
            issues.append("historical-link-drift-row-incomplete")
            continue
        returned = row[next(iter(returned_keys))]
        expected = row["expected_archive_sha256"]
        if not sha_re.fullmatch(str(expected)) or not sha_re.fullmatch(str(returned)):
            issues.append("historical-link-drift-hash-malformed")
        elif expected == returned:
            issues.append("historical-link-drift-nondrift-row")
        if row.get("response_turn") not in {20, 30} or row.get("returned_boundary") not in {"ROUND16", "ROUND18"}:
            issues.append("historical-link-drift-boundary-mismatch")
    interpretation = document.get("interpretation", {})
    if (
        not isinstance(interpretation, dict)
        or interpretation.get("archive_controls_resolved_to_reported_historical_boundaries") is not True
        or interpretation.get("drift_invalidates_downloaded_archive_bytes") is not False
        or interpretation.get("mutable_link_labels_are_hash_authority") is not False
    ):
        issues.append("historical-link-drift-interpretation-mismatch")
    return list(dict.fromkeys(issues))


def validate_pmr007_correction(text: str) -> list[str]:
    issues: list[str] = []
    if not all(identity in text for identity in EXPECTED_PMR007):
        issues.append("pmr007-correction-result-coverage-mismatch")
    required_rejection = (
        "Round 14 V1 remains a blocked formal defect. Round 18 V1 and V3 and "
        "Round 20 V1 remain rejected evidence."
    )
    if required_rejection not in text:
        issues.append("pmr007-correction-rejected-version-boundary-missing")
    forbidden = (
        r"round\s*20\s*v1[^\n]{0,100}\b(?:current|adopted)\b[^\n]{0,100}\b(?:theorem|result)\b",
        r"owner[_ ]adoption\s*:\s*(?:adopted|complete|pass)",
        r"external[_ ]review\s*:\s*(?:closed|complete|pass)",
    )
    if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in forbidden):
        issues.append("pmr007-correction-contradictory-promotion")
    return issues


def validate_pmr007_deep_proposal(index: Any, receipt: Any, correction: str) -> list[str]:
    """Keep the Deep A-AP snapshot exact and proposal-only."""
    issues: list[str] = []
    if not isinstance(index, dict) or not isinstance(receipt, dict):
        return ["malformed-pmr007-deep-proposal-owner"]

    results = index.get("results", [])
    items = index.get("items", [])
    if not isinstance(results, list) or not isinstance(items, list):
        return ["malformed-pmr007-deep-result-index"]
    rows = results + items
    identities = [row.get("pmr_identity") for row in rows if isinstance(row, dict)]
    if len(rows) != 52 or len(identities) != 52 or len(set(identities)) != 52:
        issues.append("pmr007-deep-result-index-count-mismatch")

    deep_rows = [row for row in rows if isinstance(row, dict) and str(row.get("round", "")).startswith("DEEP_")]
    deep_ids = {row.get("pmr_identity") for row in deep_rows}
    if len(deep_rows) != 42 or deep_ids != EXPECTED_PMR007_DEEP:
        issues.append("pmr007-deep-result-coverage-mismatch")
    for row in deep_rows:
        identity = row.get("pmr_identity", "?")
        if row.get("historical_identity_relation") != "NONE":
            issues.append(f"pmr007-deep-historical-identity-promoted:{identity}")
        if row.get("external_review_status") != "OPEN":
            issues.append(f"pmr007-deep-external-review-closed:{identity}")
        if "PENDING" not in str(row.get("owner_adoption_status", "")):
            issues.append(f"pmr007-deep-owner-adoption-promoted:{identity}")
        if "ZERO" not in str(row.get("origin_and_novelty_ceiling", "")):
            issues.append(f"pmr007-deep-novelty-promoted:{identity}")

    source = receipt.get("source_archive", {})
    repository_copy = receipt.get("repository_copy", {})
    overlap = receipt.get("overlap_with_existing_main", {})
    expected_source = {
        "sha256": "80c1679744374f20740dbb9817bb333fb9ae7f399d166afb39d28d23c3fc9d59",
        "archive_members": 831,
        "internal_sha256sums_entries": 830,
        "integrity": "PASS",
        "private_data_exclusion": "PASS",
    }
    if not isinstance(source, dict) or any(source.get(key) != value for key, value in expected_source.items()):
        issues.append("pmr007-deep-source-archive-receipt-mismatch")
    if not isinstance(repository_copy, dict) or repository_copy.get("exact_archive_members") != 831 or repository_copy.get("source_bytes_modified") is not False:
        issues.append("pmr007-deep-repository-copy-boundary-mismatch")
    if not isinstance(overlap, dict) or overlap.get("byte_duplicate_members") != 99 or overlap.get("duplicate_credit_effect") != "NONE":
        issues.append("pmr007-deep-overlap-credit-boundary-mismatch")

    required_correction = (
        "No proposal in this snapshot is adopted repository theory.",
        "No historical identity is assigned.",
        "No general novelty credit is granted.",
        "No integrated champion, meniscus, or natural closure is established.",
        "No Lean source, build, or kernel check is claimed by this repository import.",
        "99 byte-identical members",
    )
    if not all(phrase in correction for phrase in required_correction):
        issues.append("pmr007-deep-correction-boundary-missing")
    forbidden = (
        r"owner[_ ]adoption\s*:\s*(?:adopted|complete|pass)",
        r"external[_ ]review\s*:\s*(?:closed|complete|pass)",
        r"(?:meniscus|natural[_ ]closure)\s*:\s*(?:reached|complete|pass)",
    )
    if any(re.search(pattern, correction, flags=re.IGNORECASE) for pattern in forbidden):
        issues.append("pmr007-deep-correction-contradictory-promotion")
    return list(dict.fromkeys(issues))


def validate_pmr007_deep_execution(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-pmr007-deep-execution-receipt"]
    issues: list[str] = []
    broad = document.get("broad_disposable_run", {})
    isolated = document.get("isolated_rereview_run", {})
    expected_broad = {"scripts_discovered": 73, "exit_zero": 52, "exit_nonzero": 21}
    expected_isolated = {"scripts_discovered": 34, "exit_zero": 15, "exit_nonzero": 19}
    if not isinstance(broad, dict) or any(broad.get(key) != value for key, value in expected_broad.items()):
        issues.append("pmr007-deep-broad-execution-count-mismatch")
    if not isinstance(isolated, dict) or any(isolated.get(key) != value for key, value in expected_isolated.items()):
        issues.append("pmr007-deep-rereview-execution-count-mismatch")
    expected_evidence_status = "INTEGRATOR_REPORTED_NOT_INDEPENDENTLY_REPRODUCED"
    if document.get("verification_class") != expected_evidence_status:
        issues.append("pmr007-deep-execution-verification-class-overclaim")
    for label, run in (("broad", broad), ("rereview", isolated)):
        if not isinstance(run, dict):
            continue
        if run.get("evidence_status") != expected_evidence_status:
            issues.append(f"pmr007-deep-{label}-execution-evidence-overclaim")
        if run.get("public_per_script_ledger_present") is not False:
            issues.append(f"pmr007-deep-{label}-ledger-boundary-mismatch")
        if run.get("deterministic_compatibility_layout_recipe_present") is not False:
            issues.append(f"pmr007-deep-{label}-recipe-boundary-mismatch")
    boundary = document.get("execution_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("sanitized_snapshot_self_contained_executable") is not False:
        issues.append("pmr007-deep-execution-self-contained-overclaim")
    if document.get("authority_effect") != "NONE":
        issues.append("pmr007-deep-execution-authority-promoted")
    canonical = document.get("canonical_deep_x_through_ap_checks", [])
    expected_statuses = {
        "PMR-007-CGIP-1": "INTEGRATOR_REPORTED_PRIMARY_AND_DISTINCT_REREVIEW_REPRODUCED",
        "PMR-007-ABPD-1": "INTEGRATOR_REPORTED_PRIMARY_AND_DISTINCT_REREVIEW_REPRODUCED",
        "PMR-007-RPDS-1": "INTEGRATOR_REPORTED_PRIMARY_REPRODUCED_DISTINCT_REREVIEW_SOURCE_BOUND",
        "PMR-007-SWRI-1": "INTEGRATOR_REPORTED_PRIMARY_AND_DISTINCT_REREVIEW_REPRODUCED",
    }
    actual_statuses = {
        row.get("identity"): row.get("status")
        for row in canonical
        if isinstance(row, dict)
    } if isinstance(canonical, list) else {}
    if actual_statuses != expected_statuses:
        issues.append("pmr007-deep-canonical-execution-status-mismatch")
    interpretation = document.get("interpretation", {})
    if not isinstance(interpretation, dict) or interpretation.get("independent_reproduction_from_public_snapshot") != "NOT_ESTABLISHED":
        issues.append("pmr007-deep-independent-reproduction-overclaim")
    return issues


def validate_visible_source_manifest(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-visible-file-card-manifest"]
    issues: list[str] = []
    if document.get("source_surface") != "VISIBLE_FILE_CARD_BYTES":
        issues.append("visible-file-card-source-surface-mismatch")
    if document.get("companion_archive_precedence") != "NONE_WHEN_BYTES_CONFLICT":
        issues.append("visible-file-card-precedence-mismatch")
    expected = {
        "FULL_PROGRAM_REENTRY_V2": ("programs/full-program-reentry-v2-source", 22),
        "PMR001": ("post-merge-pmr001-source", 27),
        "PMR002_THROUGH_PMR006": ("post-merge-pmr002-006-source", 12),
    }
    groups = document.get("groups", [])
    if not isinstance(groups, list):
        return issues + ["malformed-visible-file-card-groups"]
    by_id = {group.get("id"): group for group in groups if isinstance(group, dict)}
    if len(by_id) != len(groups) or set(by_id) != set(expected):
        issues.append("visible-file-card-group-coverage-mismatch")
        return issues
    for group_id, (directory, expected_count) in expected.items():
        group = by_id[group_id]
        files = group.get("files", [])
        if group.get("directory") != directory or group.get("file_count") != expected_count:
            issues.append(f"visible-file-card-group-metadata-mismatch:{group_id}")
        if not isinstance(files, list) or len(files) != expected_count:
            issues.append(f"visible-file-card-row-count-mismatch:{group_id}")
            continue
        paths = [row.get("path") for row in files if isinstance(row, dict)]
        if len(paths) != len(files) or len(paths) != len(set(paths)):
            issues.append(f"visible-file-card-path-coverage-mismatch:{group_id}")
            continue
        actual_paths = {
            path.relative_to(PACKET).as_posix()
            for path in (PACKET / directory).rglob("*")
            if path.is_file()
        }
        if set(paths) != actual_paths:
            issues.append(f"visible-file-card-path-coverage-mismatch:{group_id}")
        for row in files:
            if not isinstance(row, dict):
                issues.append("visible-file-card-row-malformed")
                continue
            target = PACKET / row.get("path", "")
            if not target.is_file() or row.get("bytes") != target.stat().st_size:
                issues.append("visible-file-card-member-size-mismatch")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != row.get("sha256"):
                issues.append("visible-file-card-member-hash-mismatch")
    return list(dict.fromkeys(issues))


def validate_file_card_archive_conflicts(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-file-card-archive-conflicts"]
    issues: list[str] = []
    groups = document.get("groups", [])
    if not isinstance(groups, list) or len(groups) != 3:
        return ["file-card-archive-conflict-group-count-mismatch"]
    conflict_rows = sum(len(group.get("byte_conflicts", [])) for group in groups if isinstance(group, dict))
    absent_rows = sum(len(group.get("selected_files_absent_by_same_basename_from_archive", [])) for group in groups if isinstance(group, dict))
    multiple_rows = sum(len(group.get("multiple_same_basename_archive_members", [])) for group in groups if isinstance(group, dict))
    summary = document.get("summary", {})
    if (
        not isinstance(summary, dict)
        or summary.get("byte_conflict_rows") != 8
        or summary.get("archive_absence_rows") != 6
        or summary.get("multiple_basename_rows") != 4
        or conflict_rows != 8
        or absent_rows != 6
        or multiple_rows != 4
    ):
        issues.append("file-card-archive-conflict-count-mismatch")
    if summary.get("authority_resolution") != "VISIBLE_FILE_CARD_BYTES_SELECTED_ARCHIVE_VARIANTS_UNRESOLVED":
        issues.append("file-card-archive-conflict-authority-mismatch")
    sha_re = re.compile(r"^[0-9a-f]{64}$")
    for group in groups:
        if not isinstance(group, dict) or not sha_re.fullmatch(str(group.get("companion_archive_sha256", ""))):
            issues.append("file-card-archive-group-malformed")
            continue
        for row in group.get("byte_conflicts", []):
            selected = row.get("selected_sha256") if isinstance(row, dict) else None
            archived = row.get("archive_member_sha256") if isinstance(row, dict) else None
            if not sha_re.fullmatch(str(selected)) or not sha_re.fullmatch(str(archived)) or selected == archived:
                issues.append("file-card-archive-conflict-row-malformed")
        for row in group.get("selected_files_absent_by_same_basename_from_archive", []):
            if not isinstance(row, dict) or not row.get("filename") or not sha_re.fullmatch(str(row.get("selected_sha256", ""))):
                issues.append("file-card-archive-absence-row-malformed")
        for row in group.get("multiple_same_basename_archive_members", []):
            members = row.get("archive_members", []) if isinstance(row, dict) else []
            if not row.get("at_least_one_archive_member_matches_selected") or len(members) < 2:
                issues.append("file-card-archive-multiple-row-malformed")
    return list(dict.fromkeys(issues))


def validate_source_receipt(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["malformed-post-merge-source-receipt"]
    issues: list[str] = []
    if "source_archive" in document or not isinstance(document.get("companion_archive"), dict):
        issues.append("post-merge-source-receipt-archive-role-mismatch")
    archive = document.get("companion_archive", {})
    sha_re = re.compile(r"^[0-9a-f]{64}$")
    if (
        not archive.get("filename")
        or not sha_re.fullmatch(str(archive.get("sha256", "")))
        or not isinstance(archive.get("bytes"), int)
        or archive.get("bytes", 0) <= 0
        or not isinstance(archive.get("archive_members"), int)
        or archive.get("archive_members", 0) <= 0
        or archive.get("integrity") != "PASS"
    ):
        issues.append("post-merge-source-receipt-companion-archive-malformed")

    selection = document.get("repository_selection", {})
    if not isinstance(selection, dict):
        issues.append("post-merge-source-receipt-selection-malformed")
    else:
        if selection.get("source_surface") != "VISIBLE_FILE_CARD_BYTES":
            issues.append("post-merge-source-receipt-surface-mismatch")
        if selection.get("selection_manifest") != "AR8R-POST-MERGE-VISIBLE-FILE-CARD-MANIFEST-V1.yaml":
            issues.append("post-merge-source-receipt-manifest-mismatch")
        if selection.get("source_bytes_modified") is not False:
            issues.append("post-merge-source-receipt-byte-modification-mismatch")
        if not isinstance(selection.get("exact_public_safe_files"), int) or selection.get("exact_public_safe_files", 0) <= 0:
            issues.append("post-merge-source-receipt-file-count-malformed")

    relation = document.get("archive_relation", {})
    if not isinstance(relation, dict):
        issues.append("post-merge-source-receipt-archive-relation-malformed")
    else:
        if relation.get("precedence") != "VISIBLE_FILE_CARD_VERSION_SELECTED_ARCHIVE_VARIANTS_UNRESOLVED":
            issues.append("post-merge-source-receipt-precedence-mismatch")
        if relation.get("conflict_owner") != "AR8R-POST-MERGE-FILE-CARD-ARCHIVE-CONFLICTS-V1.yaml":
            issues.append("post-merge-source-receipt-conflict-owner-mismatch")
    return list(dict.fromkeys(issues))


def _ids_exact(rows: Any, key: str, expected: set[str]) -> bool:
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        return False
    values = [row.get(key) for row in rows]
    return len(values) == len(expected) and len(values) == len(set(values)) and set(values) == expected


def validate_deferred_exact_source(root: Path = DEFERRED_EXACT) -> list[str]:
    issues: list[str] = []
    if not root.is_dir():
        return ["deferred-exact-source-missing"]
    actual = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }
    if set(actual) != set(EXPECTED_DEFERRED_SOURCE):
        issues.append("deferred-exact-source-allowlist-mismatch")
    if len(actual) != 24 or sum(path.stat().st_size for path in actual.values()) != 84163:
        issues.append("deferred-exact-source-total-mismatch")
    expected_groups = {"candidate-e": (11, 33374), "candidate-g": (10, 21382), "integration": (3, 29407)}
    for group, (count, size) in expected_groups.items():
        members = [path for rel, path in actual.items() if rel.startswith(f"{group}/")]
        if len(members) != count or sum(path.stat().st_size for path in members) != size:
            issues.append(f"deferred-exact-source-group-mismatch:{group}")
    for relative, (expected_size, expected_hash) in EXPECTED_DEFERRED_SOURCE.items():
        path = actual.get(relative)
        if path is None:
            continue
        if path.stat().st_size != expected_size:
            issues.append(f"deferred-exact-source-size-mismatch:{relative}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            issues.append(f"deferred-exact-source-hash-mismatch:{relative}")
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    rule = "docs/project-closure/ar8r-v11/programs/deferred-candidate-source/exact/** -text"
    if attributes.count(rule) != 1:
        issues.append("deferred-exact-source-gitattributes-rule-mismatch")
    return list(dict.fromkeys(issues))


def validate_a_to_n_architecture(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["a-to-n-malformed"]
    issues: list[str] = []
    rows = document.get("candidates")
    if not _ids_exact(rows, "candidate", set("ABCDEFGHIJKLMN")):
        issues.append("a-to-n-candidate-coverage-mismatch")
        rows = rows if isinstance(rows, list) else []
    required = {
        "title", "track", "source_class", "truth_status", "proof_status", "source_status",
        "novelty_status", "significance_status", "dependencies", "live_rival", "remaining_burden",
        "current_adoption", "current_public_owner", "what_it_does_not_establish", "forbidden_promotions",
        "current_status_boundary", "historical_evidence",
    }
    exact_map = load_yaml(DEFERRED_EXACT / "integration" / "A_TO_N_COMPREHENSIVE_INTEGRATION_MAP.yaml")
    exact_rows = {
        row.get("candidate"): row
        for row in exact_map.get("entries", [])
        if isinstance(row, dict) and row.get("candidate") in set("ABCDEFGHIJKLMN")
    }
    historical_fields = {
        "truth_status", "proof_status", "source_status", "novelty_status", "significance_status",
        "terminal_or_nonterminal_status", "dependency_on_another_candidate",
    }
    expected_dependencies = {
        "A": {("NONE", "NOT_APPLICABLE")},
        "B": {("A", "STRICT_DEPENDENCY")},
        "C": {("B", "STRICT_DEPENDENCY"), ("D", "STRICT_DEPENDENCY")},
        "D": {("B", "STRICT_DEPENDENCY")},
        "E": {("A", "STRICT_DEPENDENCY")},
        "F": {("NONE", "NOT_APPLICABLE")},
        "G": {("B", "STRICT_DEPENDENCY")},
        "H": {("A", "STRICT_DEPENDENCY"), ("F", "STRICT_DEPENDENCY")},
        "I": {("NONE", "NOT_APPLICABLE")},
        "J": {("E", "STRICT_DEPENDENCY"), ("M", "NON_STRICT_ARCHITECTURE_CROSSWALK")},
        "K": {("NONE", "NOT_APPLICABLE")},
        "L": {("J", "NON_STRICT_ARCHITECTURE_CROSSWALK"), ("M", "NON_STRICT_ARCHITECTURE_CROSSWALK")},
        "M": {("J", "NON_STRICT_ARCHITECTURE_CROSSWALK"), ("L", "NON_STRICT_ARCHITECTURE_CROSSWALK")},
        "N": {
            ("E", "NON_STRICT_ARCHITECTURE_CROSSWALK"),
            ("J", "NON_STRICT_ARCHITECTURE_CROSSWALK"),
            ("L", "NON_STRICT_ARCHITECTURE_CROSSWALK"),
            ("M", "NON_STRICT_ARCHITECTURE_CROSSWALK"),
            ("PRIMARY_TEXTS_AND_SCHOOL_PREMISES", "STRICT_DEPENDENCY"),
        },
    }
    expected_current_adoption = {
        **{candidate: "NOT_ADOPTED" for candidate in "ABCDFHIJKLM"},
        "E": "DEFERRED_INSUFFICIENT_AUDIT",
        "G": "DEFERRED_INSUFFICIENT_AUDIT",
        "N": "REOPENED_SCHOOL_INTERNAL_ARCHITECTURE",
    }
    dependency_required = {
        "target", "target_kind", "relation", "edge_type", "strictness", "source_locator",
        "source_class", "adoption_boundary", "current_status",
    }
    by_candidate: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not required.issubset(row):
            issues.append(f"a-to-n-required-fields-missing:{row.get('candidate', '?') if isinstance(row, dict) else '?'}")
            continue
        candidate = row.get("candidate")
        by_candidate[candidate] = row
        if row.get("current_adoption") != expected_current_adoption.get(candidate):
            issues.append(f"a-to-n-current-adoption-mismatch:{candidate}")
        if candidate in {"E", "G"} and row.get("current_adoption") != "DEFERRED_INSUFFICIENT_AUDIT":
            issues.append(f"a-to-n-deferred-candidate-promoted:{candidate}")
        if candidate == "N" and row.get("current_adoption") != "REOPENED_SCHOOL_INTERNAL_ARCHITECTURE":
            issues.append("candidate-n-status-promoted")

        historical = row.get("historical_evidence")
        predecessor = exact_rows.get(candidate)
        if not isinstance(historical, dict) or predecessor is None:
            issues.append(f"a-to-n-historical-evidence-missing:{candidate}")
        else:
            for field in historical_fields:
                if historical.get(field) != predecessor.get(field):
                    issues.append(f"a-to-n-historical-evidence-drift:{candidate}:{field}")
            if historical.get("source_locator") != "deferred-candidate-source/exact/integration/A_TO_N_COMPREHENSIVE_INTEGRATION_MAP.yaml":
                issues.append(f"a-to-n-historical-source-locator-mismatch:{candidate}")
            if historical.get("source_class") != "EXACT_RECOVERED_PREDECESSOR_MAP":
                issues.append(f"a-to-n-historical-source-class-mismatch:{candidate}")
            if "NO_AUTOMATIC" not in str(historical.get("evidence_effect", "")) and candidate not in {"E", "G", "N"}:
                issues.append(f"a-to-n-historical-current-boundary-missing:{candidate}")
        if not isinstance(row.get("current_status_boundary"), str) or not row["current_status_boundary"]:
            issues.append(f"a-to-n-current-status-boundary-missing:{candidate}")

        dependencies = row.get("dependencies")
        if not isinstance(dependencies, list) or not dependencies:
            issues.append(f"a-to-n-dependencies-missing:{candidate}")
            continue
        observed: list[tuple[str, str]] = []
        observed_targets: list[str] = []
        for dependency in dependencies:
            if not isinstance(dependency, dict) or set(dependency) != dependency_required:
                issues.append(f"a-to-n-dependency-schema-mismatch:{candidate}")
                continue
            target = dependency.get("target")
            strictness = dependency.get("strictness")
            observed.append((target, strictness))
            observed_targets.append(target)
            if any(not isinstance(dependency.get(field), str) or not dependency.get(field) for field in dependency_required):
                issues.append(f"a-to-n-dependency-empty-field:{candidate}:{target}")
            if dependency.get("source_locator") != "deferred-candidate-source/exact/integration/A_TO_N_COMPREHENSIVE_INTEGRATION_MAP.yaml" or dependency.get("source_class") != "EXACT_RECOVERED_PREDECESSOR_MAP":
                issues.append(f"a-to-n-dependency-provenance-mismatch:{candidate}:{target}")
            if target == "NONE":
                if dependency.get("target_kind") != "NONE" or strictness != "NOT_APPLICABLE" or len(dependencies) != 1:
                    issues.append(f"a-to-n-explicit-none-malformed:{candidate}")
            elif target == "PRIMARY_TEXTS_AND_SCHOOL_PREMISES":
                if candidate != "N" or dependency.get("target_kind") != "SOURCE_REQUIREMENT" or strictness != "STRICT_DEPENDENCY":
                    issues.append(f"a-to-n-source-requirement-malformed:{candidate}")
            elif target not in set("ABCDEFGHIJKLMN") or dependency.get("target_kind") != "CANDIDATE":
                issues.append(f"a-to-n-dependency-reference-invalid:{candidate}:{target}")
        if len(observed_targets) != len(set(observed_targets)):
            issues.append(f"a-to-n-dependency-target-duplicate:{candidate}")
        if set(observed) != expected_dependencies.get(candidate, set()) or len(observed) != len(expected_dependencies.get(candidate, set())):
            issues.append(f"a-to-n-dependency-shape-mismatch:{candidate}")

    strict_graph = {
        candidate: [
            dependency["target"]
            for dependency in row.get("dependencies", [])
            if isinstance(dependency, dict)
            and dependency.get("strictness") == "STRICT_DEPENDENCY"
            and dependency.get("target_kind") == "CANDIDATE"
        ]
        for candidate, row in by_candidate.items()
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(candidate: str) -> bool:
        if candidate in visiting:
            return True
        if candidate in visited:
            return False
        visiting.add(candidate)
        if any(visit(target) for target in strict_graph.get(candidate, [])):
            return True
        visiting.remove(candidate)
        visited.add(candidate)
        return False

    if any(visit(candidate) for candidate in strict_graph if candidate not in visited):
        issues.append("a-to-n-strict-dependency-cycle")
    policy = document.get("dependency_policy", {})
    if policy.get("strict_candidate_graph") != "ACYCLIC" or policy.get("current_effect") != "Dependency evidence is recorded without adopting a candidate, proof edge, champion, meniscus, or closure claim.":
        issues.append("a-to-n-dependency-policy-mismatch")
    expected_edges = {
        "M theorem -> source fidelity", "M theorem -> divine personality",
        "N source claim -> neutral school-independent entailment",
        "T scoped anti-bootstrapping -> one Necessary Being",
        "functional integration -> one bearer", "query optimality -> proper function or Wisdom",
    }
    if set(document.get("forbidden_directed_edges", [])) != expected_edges:
        issues.append("a-to-n-nonmigration-edge-mismatch")
    closure = document.get("closure_state", {})
    if closure.get("integrated_champion") != "NO_INTEGRATED_CHAMPION":
        issues.append("a-to-n-champion-promoted")
    if closure.get("meniscus") != "MENISCUS_NOT_REACHED":
        issues.append("a-to-n-meniscus-promoted")
    if closure.get("natural_closure") != "NATURAL_CLOSURE_NOT_REACHED":
        issues.append("a-to-n-closure-promoted")
    return list(dict.fromkeys(issues))


def validate_bridge_ledger(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["bridge-ledger-malformed"]
    issues: list[str] = []
    if not _ids_exact(document.get("bridges"), "id", {f"B{i}" for i in range(17)}):
        issues.append("bridge-ledger-b-coverage-mismatch")
    if not _ids_exact(document.get("hard_premises"), "id", {f"H{i}" for i in range(17)}):
        issues.append("bridge-ledger-h-coverage-mismatch")
    if not _ids_exact(document.get("soft_considerations"), "id", {f"S{i}" for i in range(8)}):
        issues.append("bridge-ledger-s-coverage-mismatch")
    required = {"antecedent", "consequent", "hard_premise_ids", "soft_consideration_ids", "live_countermodels", "source_class", "source_locator", "status", "remaining_burden"}
    for row in document.get("bridges", []) if isinstance(document.get("bridges"), list) else []:
        if not isinstance(row, dict) or not required.issubset(row):
            issues.append(f"bridge-ledger-required-fields-missing:{row.get('id', '?') if isinstance(row, dict) else '?'}")
        elif not row.get("hard_premise_ids") or not row.get("live_countermodels"):
            issues.append(f"bridge-ledger-load-bearing-field-empty:{row.get('id')}")
    public = document.get("public_statuses", {})
    expected = {
        "same_token_same_respect": "SAME_TOKEN_SAME_RESPECT_THEORY_ADEQUACY_NO_GO_ESTABLISHED",
        "world_directed_extension": "WORLD_DIRECTED_EXTENSION_CONDITIONAL_ON_RB",
        "global_underived_modal_order": "GLOBAL_UNDERIVED_MODAL_ORDER_NOT_ESTABLISHED",
        "necessary_being": "NECESSARY_BEING_NOT_DEDUCTIVELY_ESTABLISHED",
        "r5": "UNDEFEATED", "candidate_e": "DEFERRED_INSUFFICIENT_AUDIT", "candidate_g": "DEFERRED_INSUFFICIENT_AUDIT",
    }
    if not isinstance(public, dict) or any(public.get(k) != v for k, v in expected.items()):
        issues.append("bridge-ledger-public-status-mismatch")
    closure = document.get("closure_state", {})
    if closure.get("meniscus") != "MENISCUS_NOT_REACHED":
        issues.append("bridge-ledger-meniscus-promoted")
    if closure.get("integrated_champion") != "NO_INTEGRATED_CHAMPION":
        issues.append("bridge-ledger-champion-promoted")
    if closure.get("natural_closure") != "NATURAL_CLOSURE_NOT_REACHED":
        issues.append("bridge-ledger-closure-promoted")
    return list(dict.fromkeys(issues))


def validate_typed_matrices(proper: Any, ontology: Any, tac: Any) -> list[str]:
    issues: list[str] = []
    proper_ids = {"frequency", "causal_role", "organizational_autopoietic", "selected_effect", "design", "learned_objective", "success_surface", "teleological_norm", "plantinga_epistemic_proper_function", "fitrah_oriented"}
    ontology_ids = {"nominalism_class", "resemblance_trope", "conceptualism_internal_realism", "real_pattern", "immanent_sparse_property_realism", "platonism_transcendent", "powers_brute", "property_dualism", "distributed_plural", "fixed_point_coherentist", "deistic_source_relative"}
    if not isinstance(proper, dict) or not _ids_exact(proper.get("accounts"), "id", proper_ids):
        issues.append("proper-function-account-coverage-mismatch")
    else:
        required = {"function_fixing_relation", "strongest_licensed_interpretation", "evidence_needed", "countermodel", "forbidden_promotion", "source_class", "source_locator", "adoption_status"}
        if any(not required.issubset(row) for row in proper["accounts"]):
            issues.append("proper-function-required-fields-missing")
    if not isinstance(ontology, dict) or not _ids_exact(ontology.get("alternatives"), "id", ontology_ids):
        issues.append("ontology-alternative-coverage-mismatch")
    else:
        required = {"interpretation", "compatibility_with_current_evidence", "missing_discriminator", "countermodel_role", "source_class", "historical_presence", "current_owner", "adoption_status"}
        if any(not required.issubset(row) for row in ontology["alternatives"]):
            issues.append("ontology-required-fields-missing")
        dualism = next(row for row in ontology["alternatives"] if row.get("id") == "property_dualism")
        if dualism.get("source_class") != "NEW_V11" or dualism.get("historical_presence") != "NONE_FOUND":
            issues.append("property-dualism-provenance-promoted")
        for rival_id in ("nominalism_class", "conceptualism_internal_realism"):
            rival = next(row for row in ontology["alternatives"] if row.get("id") == rival_id)
            if rival.get("adoption_status") != "LIVE_RIVAL_NOT_ADOPTED":
                issues.append(f"ontology-live-rival-promoted:{rival_id}")
            if rival.get("historical_presence") != "NONE_AS_HISTORICAL_FINDING_LIVE_CURRENT_RIVAL":
                issues.append(f"ontology-rival-backdated:{rival_id}")
    if not isinstance(tac, dict) or not _ids_exact(tac.get("countermodels"), "id", {f"CM{i:02d}" for i in range(1, 33)}):
        issues.append("tac-countermodel-coverage-mismatch")
    else:
        expected_coordinates = {
            "registered_type", "numerical_identity", "state_profile", "function_profile", "output_value", "episode_occurrence", "carrier", "lineage_root",
            "coherent_lineage_transport", "copy_relation", "provenance_root", "copy_count", "evidential_independence", "path_label", "visible_profile",
            "independent_convergence", "receipt", "proposition_truth", "warrant", "applicability", "adoption", "agreement", "understanding", "authorization",
            "execution", "writeback", "private_acknowledgment", "common_knowledge", "shared_vocabulary", "shared_schema", "full_local_grammar",
            "occurrence_meaning", "causal_lineage", "grammar_kernel", "referent", "mentality", "agency", "translation_query_preservation",
            "full_semantic_preservation", "full_grammatical_preservation", "token_type", "source_provenance", "translation_truth", "artifact_bytes",
            "version_eligibility", "proof_skeleton", "theorem_identity", "origin_credit", "novelty_credit", "distributed_realization", "common_bearer",
            "coordinated_realization", "composite_attribution", "reliable_success", "proper_function", "articulability", "convergence", "speech_capacity",
            "speech_occurrence", "name_authorization", "revealed_content", "underived_order", "necessary_being", "created_linguistic_expression",
            "uncreated_grammar", "divine_speech",
        }
        coordinates = tac.get("coordinate_registry")
        if not _ids_exact(coordinates, "id", expected_coordinates):
            issues.append("tac-coordinate-coverage-mismatch")
            coordinates = coordinates if isinstance(coordinates, list) else []
        coordinate_required = {"id", "domain", "value_space", "equality_criterion", "relevant_projections", "forbidden_collapses"}
        projection_ids: list[str] = []
        for coordinate in coordinates:
            coordinate_id = coordinate.get("id", "?") if isinstance(coordinate, dict) else "?"
            if not isinstance(coordinate, dict) or set(coordinate) != coordinate_required:
                issues.append(f"tac-coordinate-schema-mismatch:{coordinate_id}")
                continue
            if any(not coordinate.get(field) for field in ("domain", "value_space", "equality_criterion")):
                issues.append(f"tac-coordinate-empty-definition:{coordinate_id}")
            collapses = coordinate.get("forbidden_collapses")
            if not isinstance(collapses, list) or not collapses or len(collapses) != len(set(collapses)):
                issues.append(f"tac-forbidden-collapse-malformed:{coordinate_id}")
            else:
                for target in collapses:
                    if target == coordinate_id or target not in expected_coordinates:
                        issues.append(f"tac-forbidden-collapse-reference-invalid:{coordinate_id}:{target}")
            projections = coordinate.get("relevant_projections")
            if not isinstance(projections, list) or not projections:
                issues.append(f"tac-projection-missing:{coordinate_id}")
                continue
            for projection in projections:
                if not isinstance(projection, dict) or set(projection) != {"id", "domain", "codomain", "rule"}:
                    issues.append(f"tac-projection-schema-mismatch:{coordinate_id}")
                    continue
                projection_ids.append(projection.get("id"))
                if any(not isinstance(projection.get(field), str) or not projection.get(field) for field in ("id", "domain", "codomain", "rule")):
                    issues.append(f"tac-projection-empty-field:{coordinate_id}")
                if projection.get("codomain") != coordinate_id:
                    issues.append(f"tac-projection-codomain-mismatch:{coordinate_id}:{projection.get('id')}")
        if len(projection_ids) != len(set(projection_ids)):
            issues.append("tac-projection-id-duplicate")

        required = {
            "id", "compared_coordinates", "objects_or_carriers", "relations_or_valuations", "coordinates_fixed",
            "coordinates_varied", "failed_implication", "failure_reason", "exact_public_locator",
        }
        witness_signatures: list[str] = []
        failed_implications: list[str] = []
        failure_reasons: list[str] = []
        for row in tac["countermodels"]:
            countermodel_id = row.get("id", "?") if isinstance(row, dict) else "?"
            if not isinstance(row, dict) or set(row) != required:
                issues.append(f"tac-countermodel-schema-mismatch:{countermodel_id}")
                continue
            compared = row.get("compared_coordinates")
            if not isinstance(compared, list) or len(compared) < 2 or len(compared) != len(set(compared)):
                issues.append(f"tac-compared-coordinates-malformed:{countermodel_id}")
                compared = []
            for coordinate_id in compared:
                if coordinate_id not in expected_coordinates:
                    issues.append(f"tac-countermodel-coordinate-undeclared:{countermodel_id}:{coordinate_id}")
            for field in ("objects_or_carriers", "relations_or_valuations", "coordinates_fixed", "coordinates_varied"):
                if not isinstance(row.get(field), dict) or not row[field]:
                    issues.append(f"tac-countermodel-witness-empty:{countermodel_id}:{field}")
            objects = row.get("objects_or_carriers", {})
            if not isinstance(objects.get("objects"), list) or not objects.get("objects"):
                issues.append(f"tac-countermodel-object-set-empty:{countermodel_id}")
            fixed = set(row.get("coordinates_fixed", {}))
            varied = set(row.get("coordinates_varied", {}))
            if not fixed or not varied or fixed & varied or not (fixed | varied).issubset(set(compared)):
                issues.append(f"tac-countermodel-fixed-varied-malformed:{countermodel_id}")
            for field in ("failed_implication", "failure_reason", "exact_public_locator"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    issues.append(f"tac-countermodel-text-missing:{countermodel_id}:{field}")
            if row.get("exact_public_locator") != "tac-sac-identity-and-independence.md":
                issues.append(f"tac-countermodel-locator-mismatch:{countermodel_id}")
            if any(token in yaml.safe_dump(row, sort_keys=True) for token in ("finite model separates them", "declared projections held equal", "inherited placeholder")):
                issues.append(f"tac-countermodel-generic-placeholder:{countermodel_id}")
            witness_signatures.append(yaml.safe_dump({key: row.get(key) for key in ("objects_or_carriers", "relations_or_valuations", "coordinates_fixed", "coordinates_varied")}, sort_keys=True))
            failed_implications.append(row.get("failed_implication"))
            failure_reasons.append(row.get("failure_reason"))
        if len(witness_signatures) != len(set(witness_signatures)):
            issues.append("tac-countermodel-witness-duplicate")
        if len(failed_implications) != len(set(failed_implications)) or len(failure_reasons) != len(set(failure_reasons)):
            issues.append("tac-countermodel-explanation-duplicate")
    if isinstance(tac, dict):
        firewall = tac.get("historical_firewall", {})
        contract = tac.get("countermodel_contract", {})
        if tac.get("source_class") != "NEW_V11" or tac.get("historical_packet_status") != "UNAVAILABLE" or tac.get("historical_identity_assignment") != "NONE":
            issues.append("tac-historical-packet-promoted")
        if firewall.get("coordinate_semantics") != "NEW_V11_ONLY_NOT_RECOVERED_HISTORICAL_DEFINITIONS" or firewall.get("tac_sac_term_adoption") != "NOT_AUTHORIZED" or firewall.get("exact_source_status") != "EXACT_TAC_SAC_PACKET_UNAVAILABLE":
            issues.append("tac-historical-firewall-mismatch")
        expected_contract = {
            "model_class": "FINITE_NEW_V11_NONIMPLICATION_WITNESS",
            "historical_identity": "NONE",
            "novelty_credit": 0,
            "external_review_status": "NOT_ASSIGNED",
            "owner_adoption_status": "NOT_ASSIGNED",
        }
        if not isinstance(contract, dict) or any(contract.get(key) != value for key, value in expected_contract.items()):
            issues.append("tac-countermodel-contract-promoted")
    return list(dict.fromkeys(issues))


def validate_formalization_owners(pmr: Any, queue: Any, ten: Any, family: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(pmr, dict) or not _ids_exact(pmr.get("results"), "result_id", EXPECTED_PMR007):
        issues.append("pmr-formalization-result-coverage-mismatch")
    else:
        required = {"round_version", "source_path", "status", "pure_declaration", "application_declaration", "pure_dependencies", "wrapper_dependencies", "executable_evidence_paths", "proof_scope", "countermodel_guards", "source_present", "parse_status", "elaboration_status", "kernel_status", "axiom_status", "external_review_status", "owner_adoption_status", "historical_identity", "novelty_ceiling", "blockers"}
        for row in pmr["results"]:
            if not required.issubset(row):
                issues.append(f"pmr-formalization-required-fields-missing:{row.get('result_id', '?')}")
                continue
            if row.get("status") != "ADMITTED_POST_MERGE_SCOPED_RESULT" or row.get("owner_adoption_status") != "PENDING" or row.get("historical_identity") != "NONE":
                issues.append("pmr-result-owner-adoption-promoted")
            if row.get("parse_status") != "NOT_PERFORMED" or row.get("elaboration_status") != "NOT_PERFORMED" or row.get("kernel_status") != "NOT_PERFORMED":
                issues.append(f"pmr-formalization-status-promoted:{row.get('result_id')}")
        by_id = {row["result_id"]: row for row in pmr["results"]}
        if "PMR-007-FRLA-1" in by_id["PMR-007-COB-1"].get("pure_dependencies", []):
            issues.append("pure-cob-depends-on-frla")
        if "PMR-007-PRQT-1" in by_id["PMR-007-PRRC-1"].get("pure_dependencies", []):
            issues.append("pure-prrc-depends-on-prqt")
    if not isinstance(queue, dict) or not _ids_exact(queue.get("queue"), "id", {"Q0", *{f"Q1{c}" for c in "abcdefghi"}}):
        issues.append("lean-queue-coverage-mismatch")
    elif any(queue.get("status_axes", {}).get(key) != "NOT_PERFORMED" for key in ("parse", "elaboration", "kernel", "axiom_report")) or queue.get("status_axes", {}).get("machine_check_claim") != "NONE":
        issues.append("lean-queue-status-promoted")
    if not isinstance(ten, dict) or ten.get("Comparator_sorry_count") != "CONFLICTING_38_42":
        issues.append("ten-advances-conflict-token-mismatch")
    else:
        if {row.get("reported_count") for row in ten.get("count_locators", []) if isinstance(row, dict)} != {38, 42}:
            issues.append("ten-advances-count-locator-mismatch")
        static = ten.get("static_scope", {})
        if any(static.get(key) not in {"NOT_PERFORMED", "NOT_RUN"} for key in ("local_lean_build", "parse", "elaboration", "kernel", "print_axioms", "comparator_execution")):
            issues.append("ten-advances-build-status-promoted")
    expected_counts = {"active_identifiers": 382, "known_identity_classes": 381, "payload_resolved_active_records": 340, "proposition_origins": 339, "focused_exact_relations": 74, "high_level_families": 10, "active_records_without_exact_relation": 327}
    if not isinstance(family, dict) or any(family.get("counts", {}).get(k) != v for k, v in expected_counts.items()):
        issues.append("theorem-family-count-mismatch")
    elif family.get("sole_proved_identity_merge") != "AR8R-T322_TO_AR8R-T319" or not _ids_exact(family.get("relation_rows"), "relation_id", {f"V5-REL-{i:03d}" for i in range(1, 75)}):
        issues.append("theorem-family-relation-coverage-mismatch")
    elif family.get("no_new_identity_merges") is not True:
        issues.append("theorem-family-identity-promoted")
    if isinstance(family, dict):
        broad_families = family.get("broad_families", {})
        expected_family_ids = {
            "FAMILY-FIBRE",
            "FAMILY-HIGHER",
            "FAMILY-ROUTE",
            "FAMILY-CAUSAL",
            "FAMILY-DYNAMIC",
            "FAMILY-ORIGIN",
            "FAMILY-GROUND",
            "FAMILY-SOURCE",
            "FAMILY-ATTRIBUTE",
            "FAMILY-RIVAL",
        }
        if set(broad_families) != expected_family_ids or any(
            not isinstance(description, str) or not description.strip()
            for description in broad_families.values()
        ):
            issues.append("theorem-family-broad-family-coverage-mismatch")

        expected_later_rows = {
            ("AR8R-T227", "AR8R-T299", "PMR-007-FRLA-1", "PMR-007-ORTC-V4", "AR8R-T366"): {
                "later_labels": ["AR8R-T227", "AR8R-T299", "PMR-007-FRLA-1", "PMR-007-ORTC-V4", "AR8R-T366"],
                "v5_family": "FAMILY-FIBRE",
                "relation": "SHARED_FAMILY_NO_PROPOSITION_IDENTITY",
            },
            ("AR8R-T228", "PMR-007-COB-1"): {
                "later_labels": ["AR8R-T228", "PMR-007-COB-1"],
                "v5_family": "FAMILY-DYNAMIC",
                "relation": "SHARED_FIXED_POINT_MACHINERY_NO_IDENTITY",
            },
            ("PMR-007-MLT-1", "PMR-007-SMRB-1", "PMR-007-RSD-1"): {
                "later_labels": ["PMR-007-MLT-1", "PMR-007-SMRB-1", "PMR-007-RSD-1"],
                "v5_family": "FAMILY-ROUTE",
                "relation": "SHARED_TRANSPORT_INFRASTRUCTURE_DISTINCT_RESULTS",
            },
            ("Candidate 1", "PMR-007-PRQT-1"): {
                "later_labels": ["Candidate 1", "PMR-007-PRQT-1"],
                "v5_family": None,
                "candidate_v5_families": ["FAMILY-FIBRE", "FAMILY-HIGHER"],
                "classification_status": "UNRESOLVED_PUBLIC_OWNER_CONFLICT",
                "basis_locators": [
                    "docs/project-closure/ar8r-v11/theorems/candidate-1-hidden-matching-threshold.md#typed-setting",
                    "docs/project-closure/ar8r-v11/programs/full-program-reentry-v2-source/AR8R_FULL_PROGRAM_REENTRY_MAP_V2.md#S09",
                    "docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-rounds11-20/PROPOSED_ORIGIN_AND_ANCESTRY_UPDATES/PMR-007_FRONTIER_ROUND19_PRIOR_ART_AND_FAMILY_NOTE.md#exact-internal-ancestor",
                ],
                "relation": "REDUCTION_OR_EXTENSION_NOT_IDENTITY",
            },
            ("AR8R-T351", "AR8R-T352", "PMR-007-PRRC-1"): {
                "later_labels": ["AR8R-T351", "AR8R-T352", "PMR-007-PRRC-1"],
                "v5_family": "FAMILY-ROUTE",
                "relation": "WRAPPER_OR_DEPENDENCY_NOT_IDENTITY",
            },
            ("AR8R-HR-P236P242-T236-v1",): {
                "later_labels": ["AR8R-HR-P236P242-T236-v1"],
                "v5_family": None,
                "candidate_v5_families": ["FAMILY-DYNAMIC", "FAMILY-SOURCE"],
                "classification_status": "HISTORICAL_IDENTIFIER_COLLISION_NO_CANONICAL_MERGE",
                "basis_locators": [
                    "docs/project-closure/ar8r-v11/provenance/AR8R-HISTORICAL-ID-COLLISION-RECEIPT-P236-P242-V1.yaml",
                    "docs/project-closure/ar8r-v11/theorems/historical-collision-recoveries/AR8R-HR-P236P242-T236-v1-payload.md",
                ],
                "relation": "COLLISION_SAFE_RECOVERY_DIRECT_COROLLARY_NO_IDENTITY",
            },
        }
        later_rows = family.get("later_label_crosswalk", [])
        actual_later_rows = {
            tuple(row.get("later_labels", [])): row
            for row in later_rows
            if isinstance(row, dict)
        }
        if len(actual_later_rows) != len(later_rows) or set(actual_later_rows) != set(expected_later_rows):
            issues.append("theorem-family-later-crosswalk-coverage-mismatch")
        for labels, expected_row in expected_later_rows.items():
            if actual_later_rows.get(labels) != expected_row:
                issues.append(f"theorem-family-later-crosswalk-mismatch:{'|'.join(labels)}")
    return list(dict.fromkeys(issues))


def validate_connes_and_osw(receipt: Any, osw: Any, lean_v7: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(receipt, dict):
        return ["connes-receipt-malformed"]
    dispositions = {
        receipt.get("openai_result", {}).get("disposition"),
        receipt.get("nielsen_critique", {}).get("disposition"),
        receipt.get("nielsen_positive_proof", {}).get("disposition"),
    }
    expected = {
        "NIELSEN_CHALLENGE_REJECTED__SPECIALIST_SETTLEMENT_OPEN",
        "DOES_NOT_REFUTE_EXACT_PUBLIC_OPENAI_OBJECT",
        "REJECTED_AS_PROOF__FATAL_GAPS",
    }
    if dispositions != expected:
        issues.append("connes-disposition-separation-mismatch")
    if receipt.get("overall_disposition") != "UNRESOLVED_PENDING_OPERATOR_ALGEBRA_SPECIALIST_REVIEW":
        issues.append("connes-overall-disposition-promoted")
    if not _ids_exact(receipt.get("blocking_defects"), "id", {f"N-{i:02d}" for i in range(1, 15)}):
        issues.append("connes-blocking-defect-coverage-mismatch")
    else:
        n11 = next(row for row in receipt["blocking_defects"] if row.get("id") == "N-11")
        expected_n11 = "The positive Lean appendix assumes classification, eliminations, injectivity, and surjectivity burdens."
        if set(n11) != {"id", "finding"} or not isinstance(n11.get("finding"), str):
            issues.append("connes-n11-shape-mismatch")
        elif n11["finding"] != expected_n11:
            issues.append("connes-n11-finding-mismatch")
    if any(value != 0 for value in receipt.get("zero_credit_boundary", {}).values()):
        issues.append("connes-credit-promoted")
    source = receipt.get("public_openai_source", {})
    if source.get("commit") != "94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6" or source.get("sha256") != "31f6c419f341ee6aa5b03bc15800a9d8ee2c654c344aab90bdef0639353ccc91":
        issues.append("connes-public-source-custody-mismatch")
    if receipt.get("private_source", {}).get("classification") != "PRIVATE_EXCLUDED_HASH_ONLY" or receipt.get("private_source", {}).get("repository_copy") is not False:
        issues.append("connes-private-source-boundary-mismatch")
    if len(receipt.get("primary_sources", [])) != 5:
        issues.append("connes-primary-source-coverage-mismatch")
    expected_coordinates = {"source_claim", "source_object", "formal_claim", "formal_object", "interpretation_map", "hypothesis_correspondence", "conclusion_correspondence", "scope_boundary", "transport_witness", "falsifiers", "axiom_inventory", "build_receipt", "kernel_receipt", "mathematical_review", "custody"}
    if not isinstance(osw, dict) or not _ids_exact(osw.get("coordinates"), "id", expected_coordinates):
        issues.append("osw15-coordinate-coverage-mismatch")
    elif osw.get("relationship_to_osw11") != "REFINEMENT_PRESERVING_ALL_PRIOR_BURDENS":
        issues.append("osw15-refinement-boundary-mismatch")
    if not isinstance(lean_v7, dict):
        issues.append("lean-v7-malformed")
    else:
        connes = lean_v7.get("connes_rigidity", {})
        if connes.get("exact_source_sha256") != "31f6c419f341ee6aa5b03bc15800a9d8ee2c654c344aab90bdef0639353ccc91":
            issues.append("lean-v7-connes-source-mismatch")
        for key in ("build_status", "parse_status", "elaboration_status", "kernel_status", "axiom_report_status", "independent_operator_algebra_review"):
            if connes.get(key) != "NOT_PERFORMED":
                issues.append(f"lean-v7-connes-status-promoted:{key}")
        if connes.get("intended_theorem_status") != "UNRESOLVED_PENDING_OPERATOR_ALGEBRA_SPECIALIST_REVIEW":
            issues.append("lean-v7-connes-theorem-promoted")
    if LEAN_V6.is_file() and hashlib.sha256(LEAN_V6.read_bytes()).hexdigest() != "2b087f71563f45eee99643ba1b9a54e1d4a6371636cf8dc83de21c45b35d5774":
        issues.append("lean-v6-prior-snapshot-changed")
    elif LEAN_V6.is_file() and isinstance(lean_v7, dict):
        prior = load_yaml(LEAN_V6)
        for key, value in prior.items():
            if key != "schema" and lean_v7.get(key) != value:
                issues.append(f"lean-v7-did-not-preserve-v6-field:{key}")
    return list(dict.fromkeys(issues))


def validate_milestone_architecture(document: Any, root: Path = ROOT) -> list[str]:
    """Validate the non-adoptive Task 7A milestone projection fail-closed."""
    if not isinstance(document, dict):
        return ["milestone-architecture-malformed"]
    issues: list[str] = []
    expected_milestones = set(EXPECTED_MILESTONE_STATUSES)
    milestone_rows = document.get("milestones")
    if not _ids_exact(milestone_rows, "milestone_id", expected_milestones):
        issues.append("milestone-id-coverage-mismatch")
        milestone_rows = milestone_rows if isinstance(milestone_rows, list) else []

    required_milestone_fields = {
        "milestone_id", "title", "status", "authority_class", "purpose", "existing_assets",
        "repository_paths", "artifact_ids", "open_burdens", "candidate_theorems",
        "candidate_invariants", "candidate_impossibility_results", "formalization_targets",
        "empirical_targets", "source_requirements", "specialist_review_requirements",
        "dependencies", "downstream_consumers", "meniscus_candidates", "nonclaims",
        "adoption_status",
    }
    by_milestone: dict[str, dict[str, Any]] = {}
    for row in milestone_rows:
        if not isinstance(row, dict):
            issues.append("milestone-row-malformed")
            continue
        milestone_id = str(row.get("milestone_id", "?"))
        if not required_milestone_fields.issubset(row):
            issues.append(f"milestone-required-fields-missing:{milestone_id}")
        if milestone_id in EXPECTED_MILESTONE_STATUSES and row.get("status") != EXPECTED_MILESTONE_STATUSES[milestone_id]:
            issues.append(f"milestone-initial-status-mismatch:{milestone_id}")
        if row.get("authority_class") != "OWNER_SUPPLIED_RESEARCH_PROGRAM_CHARTER":
            issues.append(f"milestone-authority-mismatch:{milestone_id}")
        if row.get("adoption_status") != "PROPOSAL_ONLY_UNTIL_REVIEWED":
            issues.append(f"milestone-adoption-promoted:{milestone_id}")
        if row.get("status") in {"COMPLETED", "ADOPTED", "MENISCUS_REACHED"} and not row.get("completion_evidence"):
            issues.append(f"milestone-completion-without-evidence:{milestone_id}")
        for reference in [*row.get("dependencies", []), *row.get("downstream_consumers", [])]:
            if reference not in expected_milestones:
                issues.append(f"milestone-unknown-reference:{milestone_id}:{reference}")
            if reference == milestone_id:
                issues.append(f"milestone-self-dependency:{milestone_id}")
        for candidate in row.get("meniscus_candidates", []):
            if candidate not in EXPECTED_MENISCUS_REQUIREMENTS:
                issues.append(f"milestone-unknown-candidate-reference:{milestone_id}:{candidate}")
        if milestone_id in expected_milestones:
            by_milestone[milestone_id] = row

    dependency_graph = {
        milestone_id: [dep for dep in row.get("dependencies", []) if dep in expected_milestones]
        for milestone_id, row in by_milestone.items()
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(dependency) for dependency in dependency_graph.get(node, [])):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    if any(visit(node) for node in dependency_graph if node not in visited):
        issues.append("milestone-strict-dependency-cycle")

    candidate_rows = document.get("meniscus_candidates")
    if not _ids_exact(candidate_rows, "candidate_id", set(EXPECTED_MENISCUS_REQUIREMENTS)):
        issues.append("meniscus-candidate-id-coverage-mismatch")
        candidate_rows = candidate_rows if isinstance(candidate_rows, list) else []
    required_candidate_fields = {
        "candidate_id", "title", "status", "authority_class", "adoption_status",
        "evidence_classes", "roadmap_only_credit", "open_burdens", "nonclaims",
        "proposed_target", "required_milestones", "break_condition",
    }
    for row in candidate_rows:
        if not isinstance(row, dict):
            issues.append("meniscus-candidate-row-malformed")
            continue
        candidate_id = str(row.get("candidate_id", "?"))
        if not required_candidate_fields.issubset(row):
            issues.append(f"meniscus-candidate-required-fields-missing:{candidate_id}")
            continue
        if set(row.get("required_milestones", [])) != EXPECTED_MENISCUS_REQUIREMENTS.get(candidate_id, set()):
            issues.append(f"meniscus-candidate-requirements-mismatch:{candidate_id}")
        evidence_classes = set(row.get("evidence_classes", []))
        if row.get("adoption_status") != "NOT_ADOPTED" or row.get("status") != "PROPOSAL_ONLY":
            if not evidence_classes or evidence_classes <= {"OWNER_PROGRAM_CHARTER"}:
                issues.append(f"meniscus-roadmap-only-promotion:{candidate_id}")
            else:
                issues.append(f"meniscus-candidate-adoption-promoted:{candidate_id}")
        if row.get("roadmap_only_credit") != 0:
            issues.append(f"meniscus-roadmap-credit-nonzero:{candidate_id}")

    crosswalk = document.get("artifact_crosswalk")
    if not isinstance(crosswalk, list) or not crosswalk:
        issues.append("milestone-artifact-crosswalk-missing")
        crosswalk = []
    crosswalk_ids = [row.get("artifact_id") for row in crosswalk if isinstance(row, dict)]
    if len(crosswalk_ids) != len(crosswalk) or len(crosswalk_ids) != len(set(crosswalk_ids)):
        issues.append("milestone-artifact-crosswalk-id-duplicate-or-missing")
    required_crosswalk_fields = {"artifact_id", "source_class", "authority", "path_kind", "path", "status"}
    for row in crosswalk:
        if not isinstance(row, dict) or not required_crosswalk_fields.issubset(row):
            issues.append(f"milestone-crosswalk-required-fields-missing:{row.get('artifact_id', '?') if isinstance(row, dict) else '?'}")
            continue
        artifact_id = str(row["artifact_id"])
        if row.get("source_class") not in EXPECTED_MILESTONE_SOURCE_CLASSES:
            issues.append(f"milestone-crosswalk-source-class-invalid:{artifact_id}")
        if row.get("path_kind") == "REPOSITORY":
            target = root / str(row.get("path", ""))
            if not target.is_file():
                issues.append(f"milestone-crosswalk-target-missing:{artifact_id}")
        if row.get("source_class") in {"DAEE_DRAFT_PR_8", "DAEE_DRAFT_PR_9"}:
            if row.get("authority") != "DRAFT_EXTERNAL_IMPLEMENTATION_EVIDENCE" or "NOT_MERGED_MAIN" not in str(row.get("status")):
                issues.append(f"daee-draft-authority-promoted:{artifact_id}")
    if set(document.get("source_classes", [])) != EXPECTED_MILESTONE_SOURCE_CLASSES:
        issues.append("milestone-source-class-coverage-mismatch")
    artifact_id_set = set(crosswalk_ids)
    for row in milestone_rows:
        if not isinstance(row, dict):
            continue
        for artifact_id in row.get("artifact_ids", []):
            if artifact_id not in artifact_id_set:
                issues.append(f"milestone-artifact-reference-missing:{row.get('milestone_id', '?')}:{artifact_id}")

    if not _ids_exact(document.get("dependency_phases"), "phase_id", {f"PHASE-{i}" for i in range(1, 7)}):
        issues.append("milestone-phase-coverage-mismatch")
    else:
        for phase in document["dependency_phases"]:
            for milestone_id in phase.get("milestone_ids", []):
                if milestone_id not in expected_milestones:
                    issues.append(f"milestone-phase-unknown-milestone:{phase['phase_id']}:{milestone_id}")
            for candidate_id in phase.get("candidate_ids", []):
                if candidate_id not in EXPECTED_MENISCUS_REQUIREMENTS:
                    issues.append(f"milestone-phase-unknown-candidate:{phase['phase_id']}:{candidate_id}")
    flywheels = document.get("flywheels")
    if not isinstance(flywheels, list) or len(flywheels) != 5 or len({row.get("flywheel_id") for row in flywheels if isinstance(row, dict)}) != 5:
        issues.append("milestone-flywheel-coverage-mismatch")
    for row in flywheels if isinstance(flywheels, list) else []:
        if not isinstance(row, dict) or not {"flywheel_id", "milestone_ids", "sequence", "nonclaim"}.issubset(row):
            issues.append("milestone-flywheel-required-fields-missing")
            continue
        for milestone_id in row.get("milestone_ids", []):
            if milestone_id not in expected_milestones:
                issues.append(f"milestone-flywheel-unknown-milestone:{row.get('flywheel_id')}:{milestone_id}")
    formalization_loop = document.get("formalization_loop", {})
    if formalization_loop.get("loop_id") != "FORMALIZATION-FLYWHEEL" or not formalization_loop.get("nonclaim"):
        issues.append("milestone-formalization-loop-mismatch")

    fusha = next((row for row in crosswalk if isinstance(row, dict) and row.get("artifact_id") == "FUSHA-QAMUS-BOUNDARY"), {})
    if fusha.get("implementation_status") != "NOT_ESTABLISHED" or fusha.get("pinned_snapshot") != "NONE" or fusha.get("bulk_data_copied") is not False:
        issues.append("fusha-qamus-live-state-overclaim")
    controls = document.get("control_invariants", {})
    expected_controls = {
        ("t354", "formal_status"): "BLOCKED_FORMAL_DEFECT",
        ("t299", "exact_version_custody"): "PRESERVED",
        ("ten_advances", "comparator_count"): "CONFLICTING_38_42",
        ("lean", "kernel"): "NOT_PERFORMED",
        ("tac_sac", "historical_packet_status"): "UNAVAILABLE",
        ("candidate_e", "status"): "DEFERRED_INSUFFICIENT_AUDIT",
        ("candidate_g", "status"): "DEFERRED_INSUFFICIENT_AUDIT",
        ("property_dualism", "source_class"): "NEW_V11_ANALYSIS",
        ("nominalism", "status"): "LIVE_RIVAL_NOT_ADOPTED",
        ("conceptualism", "status"): "LIVE_RIVAL_NOT_ADOPTED",
    }
    for (section, key), expected in expected_controls.items():
        if controls.get(section, {}).get(key) != expected:
            issues.append(f"milestone-control-drift:{section}:{key}")
    closure = document.get("closure_state", {})
    if closure.get("milestone_architecture") != "RECORDED_AS_OWNER_PROGRAM_CHARTER":
        issues.append("milestone-architecture-disposition-mismatch")
    if closure.get("integrated_champion") != "NO_INTEGRATED_CHAMPION":
        issues.append("milestone-architecture-champion-promoted")
    if closure.get("meniscus") != "MENISCUS_NOT_REACHED":
        issues.append("milestone-architecture-meniscus-promoted")
    if closure.get("natural_closure") != "NATURAL_CLOSURE_NOT_REACHED":
        issues.append("milestone-architecture-closure-promoted")

    if not MILESTONE_CHARTER.is_file():
        issues.append("milestone-charter-missing")
    else:
        if MILESTONE_CHARTER.stat().st_size != 76682:
            issues.append("milestone-charter-size-mismatch")
        if hashlib.sha256(MILESTONE_CHARTER.read_bytes()).hexdigest() != "f4245d44e79e50c9fbef9173ee22e50795a08b02c027059d4abbae2aef15a0c8":
            issues.append("milestone-charter-hash-mismatch")
    attributes = (root / ".gitattributes").read_text(encoding="utf-8").splitlines()
    charter_rule = "docs/project-closure/ar8r-v11/programs/AR8R-ORTHEMOLOGY-MENISCUS-MILESTONE-ARCHITECTURE-V1.md -text"
    if attributes.count(charter_rule) != 1:
        issues.append("milestone-charter-gitattributes-rule-mismatch")
    return list(dict.fromkeys(issues))


def validate_task7a_owner_integration() -> list[str]:
    """Require pointer-only integration without changing Task 7 accounting."""
    issues: list[str] = []
    catalog = load_yaml(CATALOG)
    ledger = load_yaml(LEDGER)
    a_to_n = load_yaml(A_TO_N)
    flywheel = load_yaml(FLYWHEEL)
    surface = load_yaml(SURFACE_CUSTODY)
    compatibility = load_yaml(COMPATIBILITY_OVERLAY)
    proper = load_yaml(PROPER_FUNCTION_MATRIX)
    ontology = load_yaml(ONTOLOGY_MATRIX)
    bridge = load_yaml(BRIDGE_LEDGER)
    ascent = load_yaml(ASCENT_V2)
    queue = load_yaml(LEAN_QUEUE)
    lean = load_yaml(LEAN_V7)
    campaign = load_yaml(PROJECTION)
    state = load_yaml(CURRENT_STATE)

    evidence = catalog.get("v11_task7a_owner_program_charter", {}) if isinstance(catalog, dict) else {}
    if evidence.get("charter", {}).get("sha256") != "f4245d44e79e50c9fbef9173ee22e50795a08b02c027059d4abbae2aef15a0c8" or evidence.get("charter", {}).get("bytes") != 76682:
        issues.append("task7a-evidence-charter-custody-mismatch")
    if evidence.get("projection", {}).get("milestone_count") != 18 or evidence.get("projection", {}).get("meniscus_candidate_count") != 9:
        issues.append("task7a-evidence-projection-count-mismatch")
    if evidence.get("adoption_effect") != "NONE" or evidence.get("task7_public_owner_count_effect") != 0:
        issues.append("task7a-evidence-adoption-or-task7-count-promoted")
    if len(catalog.get("v11_task7_public_owners", {}).get("owners", [])) != 22:
        issues.append("task7a-changed-task7-owner-count")

    decision = ledger.get("v11_task7a_milestone_architecture_decision", {}) if isinstance(ledger, dict) else {}
    if decision.get("completion_count") != 0 or decision.get("adopted_candidate_count") != 0 or decision.get("task7_decision_count_effect") != 0:
        issues.append("task7a-ledger-scientific-or-task7-count-promoted")
    task7 = ledger.get("v11_task6_and_pdf_addendum_decisions", {}) if isinstance(ledger, dict) else {}
    if task7.get("totals") != {"INTEGRATE": 26, "PROPOSAL_ONLY": 8, "DEFERRED": 6, "BLOCKED": 9, "PRIVATE_EXCLUDED": 4, "TOTAL": 53}:
        issues.append("task7a-changed-task7-decision-count")

    pointer = a_to_n.get("milestone_architecture", {}) if isinstance(a_to_n, dict) else {}
    if pointer.get("owner") != MILESTONES.name or pointer.get("effect") != "POINTER_ONLY_NO_CANDIDATE_OR_TRACK_PROMOTION":
        issues.append("task7a-a-to-n-pointer-mismatch")
    nodes = flywheel.get("nodes", {}) if isinstance(flywheel, dict) else {}
    projection = flywheel.get("milestone_projection", {}) if isinstance(flywheel, dict) else {}
    if nodes.get("milestone_architecture", {}).get("owner") != MILESTONES.name or projection.get("milestone_count") != 18 or projection.get("adoption_effect") != "NONE":
        issues.append("task7a-flywheel-pointer-mismatch")

    corrections = surface.get("supplied_corrections", []) if isinstance(surface, dict) else []
    charter_rows = [row for row in corrections if isinstance(row, dict) and row.get("name") == MILESTONE_CHARTER.name]
    if len(charter_rows) != 1 or charter_rows[0].get("sha256") != "f4245d44e79e50c9fbef9173ee22e50795a08b02c027059d4abbae2aef15a0c8" or charter_rows[0].get("adoption_effect") != "NONE":
        issues.append("task7a-surface-custody-pointer-mismatch")
    resolutions = compatibility.get("resolutions", []) if isinstance(compatibility, dict) else []
    milestone_resolution = [row for row in resolutions if isinstance(row, dict) and row.get("target_family") == "ORTHEMOLOGY_MENISCUS_MILESTONE_ARCHITECTURE"]
    if len(milestone_resolution) != 1 or milestone_resolution[0].get("immutable_source_files_modified") is not False:
        issues.append("task7a-compatibility-overlay-mismatch")

    for name, document, expected_milestones in (
        ("proper-function", proper, {"M10", "M11"}),
        ("ontology", ontology, {"M10", "M11", "M13"}),
        ("bridge", bridge, {"M10", "M11", "M12", "M13", "M17"}),
    ):
        crosswalk = document.get("milestone_crosswalk", {}) if isinstance(document, dict) else {}
        if crosswalk.get("owner") != MILESTONES.name or set(crosswalk.get("milestones", [])) != expected_milestones or "POINTER_ONLY" not in str(crosswalk.get("effect")):
            issues.append(f"task7a-{name}-crosswalk-mismatch")
    if ascent.get("linked_owners", {}).get("milestone_architecture") != MILESTONES.name:
        issues.append("task7a-ascent-pointer-mismatch")

    formal = queue.get("milestone_formalization_crosswalk", {}) if isinstance(queue, dict) else {}
    if formal.get("status") != "TARGET_QUEUE_ONLY" or set(formal.get("meniscus_candidates", [])) != set(EXPECTED_MENISCUS_REQUIREMENTS):
        issues.append("task7a-formalization-queue-pointer-mismatch")
    if any(queue.get("status_axes", {}).get(key) != "NOT_PERFORMED" for key in ("parse", "elaboration", "kernel", "axiom_report")) or queue.get("status_axes", {}).get("machine_check_claim") != "NONE":
        issues.append("task7a-formalization-status-promoted")
    lean_pointer = lean.get("milestone_architecture_projection", {}) if isinstance(lean, dict) else {}
    if lean_pointer.get("role") != "FORMALIZATION_TARGET_POINTER_ONLY" or any(lean_pointer.get(key) != "NONE" for key in ("source_inventory_effect", "parse_effect", "elaboration_effect", "kernel_effect", "machine_check_claim")):
        issues.append("task7a-lean-v7-pointer-mismatch")

    campaign_pointer = campaign.get("program_charter_pointer", {}) if isinstance(campaign, dict) else {}
    burden_rows = sum(len(rows) for rows in campaign.get("ledgers", {}).values() if isinstance(rows, list)) if isinstance(campaign, dict) else 0
    if campaign.get("summary", {}).get("reported_open_burden_count") != 8 or burden_rows != 8 or campaign_pointer.get("counted_open_burden_effect") != 0:
        issues.append("task7a-campaign-eight-burden-scope-drift")

    task7a = state.get("authored", {}).get("ar8r_v11_task7a", {}) if isinstance(state, dict) else {}
    expected_state = {
        "charter_sha256": "f4245d44e79e50c9fbef9173ee22e50795a08b02c027059d4abbae2aef15a0c8",
        "charter_bytes": 76682,
        "milestone_count": 18,
        "meniscus_candidate_count": 9,
        "completed_milestones": 0,
        "adopted_meniscus_candidates": 0,
        "daee_pr8_status": "OPEN_DRAFT_NOT_MERGED_MAIN",
        "daee_pr9_status": "OPEN_DRAFT_NOT_MERGED_MAIN",
        "fusha_qamus_implementation_status": "NOT_ESTABLISHED",
        "integrated_champion": "NO_INTEGRATED_CHAMPION",
        "meniscus": "MENISCUS_NOT_REACHED",
        "natural_closure": "NATURAL_CLOSURE_NOT_REACHED",
    }
    if any(task7a.get(key) != value for key, value in expected_state.items()):
        issues.append("task7a-current-state-mismatch")

    for readme in (PROGRAMS / "README.md", PACKET / "README.md"):
        text = readme.read_text(encoding="utf-8")
        if MILESTONE_CHARTER.name not in text or MILESTONES.name not in text:
            issues.append(f"task7a-navigation-missing:{readme.relative_to(ROOT)}")
    return list(dict.fromkeys(issues))


def validate_task7_ledgers_and_crosswalks(catalog: Any, ledger: Any, surface: Any, flywheel: Any, two_thread: Any) -> list[str]:
    issues: list[str] = []
    owners = catalog.get("v11_task7_public_owners", {}).get("owners", []) if isinstance(catalog, dict) else []
    if not isinstance(owners, list) or len(owners) != 22:
        issues.append("task7-public-owner-catalog-coverage-mismatch")
    else:
        for row in owners:
            if not isinstance(row, dict) or set(row) != {"path", "source_class", "authority", "adoption_effect"}:
                issues.append("task7-public-owner-catalog-schema-mismatch")
                continue
            if not (PACKET / row["path"]).is_file():
                issues.append(f"task7-public-owner-missing:{row['path']}")
    decisions = ledger.get("v11_task6_and_pdf_addendum_decisions", {}) if isinstance(ledger, dict) else {}
    expected_sets = {
        "integrate": {f"I{i:02d}" for i in range(1, 27)},
        "proposal_only": {f"P{i:02d}" for i in range(1, 9)},
        "deferred": {f"D{i:02d}" for i in range(1, 7)},
        "blocked": {f"B{i:02d}" for i in range(1, 10)},
        "private_excluded": {f"X{i:02d}" for i in range(1, 5)},
    }
    for key, expected in expected_sets.items():
        if not _ids_exact(decisions.get(key), "id", expected):
            issues.append(f"task7-decision-coverage-mismatch:{key}")
    if decisions.get("totals") != {"INTEGRATE": 26, "PROPOSAL_ONLY": 8, "DEFERRED": 6, "BLOCKED": 9, "PRIVATE_EXCLUDED": 4, "TOTAL": 53}:
        issues.append("task7-decision-total-mismatch")
    if not isinstance(surface, dict):
        issues.append("surface-custody-malformed")
    else:
        epochs = {row.get("epoch"): row for row in surface.get("surface_registry_epochs", []) if isinstance(row, dict)}
        if epochs.get("EARLIER_UNAVAILABLE_EPOCH", {}).get("status") != "UNAVAILABLE":
            issues.append("surface-earlier-unavailable-epoch-erased")
        if epochs.get("LATER_VISIBLE_FILE_CARD_SELECTION_EPOCH", {}).get("status") != "EXACT_88_SURFACE_SELECTION_AVAILABLE":
            issues.append("surface-later-selection-epoch-missing")
        if not epochs.get("LATER_VISIBLE_FILE_CARD_SELECTION_EPOCH", {}).get("archive_conflict_owner"):
            issues.append("surface-archive-conflict-owner-erased")
    if not isinstance(flywheel, dict):
        issues.append("flywheel-malformed")
    else:
        allowed = {"supports", "constrains"}
        default_kind = flywheel.get("edge_kind_default")
        nodes = flywheel.get("nodes", {})
        if not isinstance(nodes, dict) or not nodes:
            issues.append("flywheel-nodes-malformed")
            nodes = {}
        else:
            for node_id, node in nodes.items():
                if not isinstance(node, dict) or not isinstance(node.get("owner"), str) or not node["owner"].strip():
                    issues.append(f"flywheel-node-owner-malformed:{node_id}")
                    continue
                owner = Path(node["owner"])
                owner_path = (PROGRAMS / owner).resolve()
                try:
                    owner_path.relative_to(PACKET.resolve())
                except ValueError:
                    issues.append(f"flywheel-node-owner-outside-packet:{node_id}:{node['owner']}")
                    continue
                if not owner_path.is_file():
                    issues.append(f"flywheel-node-owner-missing:{node_id}:{node['owner']}")
        seen_endpoints: set[tuple[str, str]] = set()
        edges = flywheel.get("edges", [])
        if not isinstance(edges, list) or not edges:
            issues.append("flywheel-edges-malformed")
            edges = []
        for index, row in enumerate(edges, 1):
            if not isinstance(row, dict):
                issues.append(f"flywheel-edge-malformed:{index}")
                continue
            if row.get("kind", default_kind) not in allowed:
                issues.append(f"flywheel-edge-kind-invalid:{index}")
            source = row.get("from")
            target = row.get("to")
            if source not in nodes:
                issues.append(f"flywheel-edge-source-unknown:{index}:{source}")
            if target not in nodes:
                issues.append(f"flywheel-edge-target-unknown:{index}:{target}")
            if isinstance(source, str) and isinstance(target, str):
                endpoint = (source, target)
                if endpoint in seen_endpoints:
                    issues.append(f"flywheel-edge-duplicate-endpoint:{source}:{target}")
                seen_endpoints.add(endpoint)
            contribution_raw = row.get("contribution")
            nontransfer_raw = row.get("nontransfer")
            if not isinstance(contribution_raw, str) or not contribution_raw.strip():
                issues.append(f"flywheel-edge-contribution-missing:{index}")
            if not isinstance(nontransfer_raw, str) or not nontransfer_raw.strip():
                issues.append(f"flywheel-edge-nontransfer-missing:{index}")
            contribution = str(contribution_raw or "").lower()
            if any(re.search(rf"\b{verb}\b", contribution) for verb in ("proves", "adopts", "promotes", "closes")):
                issues.append(f"flywheel-promotion-verb:{index}")
    if not isinstance(two_thread, dict):
        issues.append("two-thread-receipt-malformed")
    else:
        allowed_top = {"schema", "privacy_contract", "artifacts", "capture_counts", "lane_evidence_usable", "forbidden_fields", "historical_availability_effect"}
        if set(two_thread) != allowed_top:
            issues.append("two-thread-receipt-field-allowlist-mismatch")
        for row in two_thread.get("artifacts", []):
            digest = row.get("sha256") if isinstance(row, dict) else None
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                issues.append("two-thread-receipt-hash-malformed")
    return list(dict.fromkeys(issues))


def validate_osm_program_integration(crosswalk: Any, milestones: Any, flywheel: Any, catalog: Any) -> list[str]:
    """Validate the V12 OSM program crosswalk and its exact anti-transfer gates."""
    issues: list[str] = []
    expected_hash = "0d097cba7bbb25a949e2bf95af28b5a2259bd8d60b0e5fac5a74cdf7d05aa814"
    expected_doi = "10.1038/s41586-024-08548-w"
    if not isinstance(crosswalk, dict):
        return ["osm-program-crosswalk-malformed"]

    source = crosswalk.get("source", {})
    authority = crosswalk.get("authority", {})
    if source.get("source_id") != "LAT-1" or str(source.get("doi")) != expected_doi:
        issues.append("osm-program-source-identity-mismatch")
    if source.get("access_copy_sha256") != expected_hash or source.get("access_copy_bytes") != 137824:
        issues.append("osm-program-source-custody-mismatch")
    if source.get("access_copy_role") != "EVIDENCE_CUSTODY_ONLY" or source.get("repository_copy") is not False:
        issues.append("osm-program-local-copy-boundary-mismatch")
    if source.get("underlying_experiment_reproduced") is not False or source.get("official_code_reproduced") is not False:
        issues.append("osm-program-reproduction-overclaim")
    if authority != {
        "governing_decisions": [
            "docs/decisions/0015-latent-state-observation-and-representation-boundary.md",
            "docs/decisions/0024-dynamic-orthing-and-representation-learning.md",
        ],
        "classification": "EXTERNAL_EXEMPLIFICATION_AND_CONSTRAINT",
        "adoption_effect": "NONE",
        "theorem_effect": "NONE",
        "novelty_effect": "NONE",
        "empirical_validation_effect": "NONE",
    }:
        issues.append("osm-program-authority-promoted-or-drifted")

    source_status = load_yaml(ROOT / "references" / "source-status.yaml")
    lat1 = next((row for row in source_status.get("claims", []) if isinstance(row, dict) and row.get("id") == "LAT-1"), {})
    custody = lat1.get("task8_custody", {}) if isinstance(lat1, dict) else {}
    if str(lat1.get("doi")) != expected_doi or str(custody.get("access_copy_sha256", "")).lower() != expected_hash:
        issues.append("osm-program-lat1-authority-mismatch")

    expected_source_constraints = [
        {
            "id": "OSM-SRC-01",
            "claim_kind": "SOURCE_REPORTED",
            "claim": "Sequential context can separate latent task states that share an immediate sensory observation.",
            "scope": "REPORTED_2ACDC_CSCG_AND_CA1_SETTING",
        },
        {
            "id": "OSM-SRC-02",
            "claim_kind": "SOURCE_REPORTED",
            "claim": "Several tested models can reach related terminal representational criteria while differing in learning trajectory.",
            "scope": "AMONG_TESTED_MODELS_UNDER_REPORTED_EVALUATION",
        },
        {
            "id": "OSM-SRC-03",
            "claim_kind": "SOURCE_REPORTED",
            "claim": "High next-input prediction performance can occur without the global representation geometry measured in the study.",
            "scope": "REPORTED_MODEL_SETTINGS_AND_OBJECTIVES",
        },
        {
            "id": "OSM-SRC-04",
            "claim_kind": "SOURCE_REPORTED",
            "claim": "Architecture and learning objective influence the terminal representation produced by the tested models.",
            "scope": "REPORTED_MODEL_SETTINGS_ONLY",
        },
        {
            "id": "OSM-SRC-05",
            "claim_kind": "SOURCE_REPORTED",
            "claim": "Novel-cue and stretched-track observations are consistent with bounded reuse, shift, reset, or rebinding alternatives.",
            "scope": "THREE_MICE_AND_REPORTED_ALTERATION_TESTS",
        },
    ]
    actual_source_constraints = crosswalk.get("source_reported_constraints")
    if actual_source_constraints != expected_source_constraints:
        issues.append("osm-program-source-constraint-collection-mismatch")
        expected_by_id = {row["id"]: row for row in expected_source_constraints}
        actual_by_id = {
            row.get("id"): row
            for row in actual_source_constraints or []
            if isinstance(row, dict)
        }
        drifted = sorted(
            source_id
            for source_id in set(expected_by_id) | set(actual_by_id)
            if actual_by_id.get(source_id) != expected_by_id.get(source_id)
        )
        issues.extend(f"osm-program-source-constraint-drift:{source_id}" for source_id in drifted)
    source_ids = [row.get("id") for row in actual_source_constraints or [] if isinstance(row, dict)]
    if len(source_ids) != len(set(source_ids)):
        issues.append("osm-program-source-constraint-duplicate-id")

    expected_syntheses = [
        {
            "id": "OSM-SYN-01",
            "claim_kind": "PROJECT_SYNTHESIS",
            "claim": "Endpoint agreement and performance agreement do not by themselves determine pathway adequacy, learning trajectory, or mechanism identity.",
            "status": "BOUNDED_ORTHEMOLOGY_SYNTHESIS",
        },
        {
            "id": "OSM-SYN-02",
            "claim_kind": "PROJECT_SYNTHESIS",
            "claim": "Observation, world state, model latent state, posterior, neural response, representation geometry, and orthemic profile require separate typed owners.",
            "status": "EXISTING_OBJECT_SEPARATION_RESTATED",
        },
        {
            "id": "OSM-SYN-03",
            "claim_kind": "PROJECT_SYNTHESIS",
            "claim": "Longitudinal intermediate states can discriminate candidates that a terminal-only comparison leaves open.",
            "status": "RESEARCH_METHOD_CONSTRAINT",
        },
        {
            "id": "OSM-SYN-04",
            "claim_kind": "PROJECT_SYNTHESIS",
            "claim": "A cross-domain convergence claim requires an explicit correspondence stronger than vocabulary or diagrammatic similarity.",
            "status": "PROGRAM_GOVERNANCE_CONSTRAINT",
        },
    ]
    actual_syntheses = crosswalk.get("project_syntheses")
    if actual_syntheses != expected_syntheses:
        issues.append("osm-program-synthesis-collection-mismatch")
        expected_by_id = {row["id"]: row for row in expected_syntheses}
        actual_by_id = {
            row.get("id"): row
            for row in actual_syntheses or []
            if isinstance(row, dict)
        }
        drifted = sorted(
            synthesis_id
            for synthesis_id in set(expected_by_id) | set(actual_by_id)
            if actual_by_id.get(synthesis_id) != expected_by_id.get(synthesis_id)
        )
        issues.extend(f"osm-program-synthesis-drift:{synthesis_id}" for synthesis_id in drifted)
    synthesis_ids = [row.get("id") for row in actual_syntheses or [] if isinstance(row, dict)]
    if len(synthesis_ids) != len(set(synthesis_ids)):
        issues.append("osm-program-synthesis-duplicate-id")

    expected_milestone_rows = [
        {
            "milestone_id": "M2",
            "relation": "EXTERNAL_CASE_CONSTRAINS_METHOD",
            "contribution": "Endpoint-only verification can miss trajectory and mechanism differences.",
            "nontransfer": "The study does not establish general specification warrant or theorem-intent fidelity.",
        },
        {
            "milestone_id": "M3",
            "relation": "DIRECT_BOUNDED_PROGRAM_INPUT",
            "contribution": "Observation aliasing, latent-state inference, learner updates, geometry, and task alterations instantiate the existing dynamic object distinctions.",
            "nontransfer": "Model latent states and neural representations do not become orthemes or worldly states.",
        },
        {
            "milestone_id": "M8",
            "relation": "BOUNDARY_ONLY",
            "contribution": "Supplies a concrete warning against collapsing observations, latent representations, and carriers.",
            "nontransfer": "Mouse CA1 findings do not establish a human noetic architecture, soul carrier, deformation, or restoration model.",
        },
        {
            "milestone_id": "M10",
            "relation": "BOUNDARY_ONLY",
            "contribution": "Separates operational success and terminal representation from the process that produced them.",
            "nontransfer": "Task efficiency supplies no normative proper-function, warrant, teleology, or design premise.",
        },
        {
            "milestone_id": "M11",
            "relation": "NO_EVIDENTIAL_SUPPORT",
            "contribution": "Defines an explicit empirical-to-metaphysical firewall.",
            "nontransfer": "The paper supplies no premise for transcendental orthability, Necessary Being, unity, agency, attributes, Speech, or revelation.",
        },
        {
            "milestone_id": "M12",
            "relation": "DIRECT_BOUNDED_PROGRAM_INPUT",
            "contribution": "Provides a worked source-to-method-to-model-to-representation crosswalk with distinct authority levels.",
            "nontransfer": "Article, code, model fit, representation geometry, and world truth are not interchangeable.",
        },
        {
            "milestone_id": "M13",
            "relation": "METHOD_TRANSFER_TARGET",
            "contribution": "Supplies a candidate test case for classifying endpoint-trajectory discrimination as reduction, guarded transfer, analogy, or nonidentity.",
            "nontransfer": "A reused proof pattern or vocabulary earns no new theorem or novelty credit.",
        },
        {
            "milestone_id": "M14",
            "relation": "FORMALIZATION_TARGET_ONLY",
            "contribution": "Suggests typed trace, quotient, and candidate-discrimination definitions for later formal work.",
            "nontransfer": "The paper contains no Lean theorem, proof object, parse, elaboration, kernel, or axiom receipt.",
        },
        {
            "milestone_id": "M15",
            "relation": "DIRECT_BOUNDED_PROGRAM_INPUT",
            "contribution": "Motivates longitudinal, intervention-sensitive, and held-out trajectory tests in addition to endpoint metrics.",
            "nontransfer": "The repository has not run a biological study or validated Orthemology empirically.",
        },
    ]
    expected_milestones = {row["milestone_id"] for row in expected_milestone_rows}
    rows = crosswalk.get("milestone_crosswalk", [])
    if not _ids_exact(rows, "milestone_id", expected_milestones):
        issues.append("osm-program-milestone-coverage-mismatch")
        rows = rows if isinstance(rows, list) else []
    by_milestone = {row.get("milestone_id"): row for row in rows if isinstance(row, dict)}
    expected_by_milestone = {row["milestone_id"]: row for row in expected_milestone_rows}
    for milestone_id in sorted(expected_milestones):
        if by_milestone.get(milestone_id) != expected_by_milestone[milestone_id]:
            issues.append(f"osm-program-milestone-row-drift:{milestone_id}")

    expected_qualifiers = {
        "EXACT_REDUCTION",
        "SHARED_FORMAL_MODEL_WITH_TYPED_INTERPRETATION_MAPS",
        "SHARED_INVARIANT_WITH_DOMAIN_SPECIFIC_SEMANTICS",
        "GUARDED_TRANSFER_THEOREM",
        "COMMON_COUNTERMODEL_ARCHITECTURE_UNDER_MATCHED_ASSUMPTIONS",
    }
    gate = crosswalk.get("formal_convergence_gate", {})
    if gate.get("status") != "REQUIRED_NOT_SATISFIED_BY_THIS_SOURCE" or set(gate.get("qualifying_relations", [])) != expected_qualifiers:
        issues.append("osm-program-convergence-gate-mismatch")
    if "SHARED_VOCABULARY" not in set(gate.get("rejected_shortcuts", [])):
        issues.append("osm-program-vocabulary-shortcut-not-rejected")

    required_forbidden = {
        "LATENT_STATE_EQUALS_ORTHEME",
        "CSCG_FIT_PROVES_BIOLOGICAL_MECHANISM",
        "TASK_PERFORMANCE_PROVES_PROPER_FUNCTION_OR_WARRANT",
        "MOUSE_CA1_PROVES_HUMAN_NOETIC_STRUCTURE",
        "ADAPTATION_EQUALS_RESTORATION",
        "NEUROSCIENCE_SUPPORTS_TRANSCENDENTAL_OR_THEOLOGICAL_ASCENT",
        "PAPER_CONTAINS_LEAN_PROOF",
        "SOURCE_ESTABLISHES_ORTHEMOLOGY_VALIDATION",
    }
    if not required_forbidden.issubset(set(crosswalk.get("forbidden_transfers", []))):
        issues.append("osm-program-forbidden-transfer-coverage-mismatch")
    effect = crosswalk.get("repository_effect", {})
    if effect.get("milestone_status_changed") is not False or effect.get("theorem_added") is not False or effect.get("empirical_result_added") is not False:
        issues.append("osm-program-repository-effect-promoted")
    if effect.get("fable_review_status") != "REQUIRED_NOT_YET_PERFORMED":
        issues.append("osm-program-fable-review-status-mismatch")
    if crosswalk.get("closure_state") != {
        "integrated_champion": "NO_INTEGRATED_CHAMPION",
        "meniscus": "MENISCUS_NOT_REACHED",
        "natural_closure": "NATURAL_CLOSURE_NOT_REACHED",
    }:
        issues.append("osm-program-closure-promoted")

    artifact_id = "OSM-LEARNING-TRAJECTORY-V12"
    artifact_rows = milestones.get("artifact_crosswalk", []) if isinstance(milestones, dict) else []
    artifact = next((row for row in artifact_rows if isinstance(row, dict) and row.get("artifact_id") == artifact_id), {})
    expected_artifact = {
        "artifact_id": artifact_id,
        "source_class": "CURRENT_PUBLIC_ORTHEMOLOGY_MAIN",
        "authority": "EXTERNAL_EXEMPLIFICATION_AND_CONSTRAINT",
        "path_kind": "REPOSITORY",
        "path": OSM_PROGRAM_CROSSWALK.relative_to(ROOT).as_posix(),
        "status": "CURRENT_PROGRAM_CROSSWALK_NO_THEOREM_OR_VALIDATION_CREDIT",
    }
    if artifact != expected_artifact:
        issues.append("osm-program-artifact-owner-mismatch")
    attached = {
        row.get("milestone_id")
        for row in milestones.get("milestones", []) if isinstance(milestones, dict) and isinstance(row, dict)
        and artifact_id in row.get("artifact_ids", [])
    }
    if attached != {"M2", "M3", "M12", "M13", "M15"}:
        issues.append("osm-program-artifact-milestone-scope-mismatch")

    nodes = flywheel.get("nodes", {}) if isinstance(flywheel, dict) else {}
    if nodes.get("osm_learning_trajectory", {}).get("owner") != OSM_PROGRAM_CROSSWALK.name:
        issues.append("osm-program-flywheel-node-missing")
    expected_crosswalk_edges = [
        {
            "edge_id": "OSM-FW-01",
            "from": "source_custody",
            "to": "osm_learning_trajectory",
            "contribution": "Exact article identity, methods, model scope, code provenance, and access-copy custody bound every downstream use.",
            "nontransfer": "Custody does not reproduce the experiment or prove the interpretation.",
        },
        {
            "edge_id": "OSM-FW-02",
            "from": "osm_learning_trajectory",
            "to": "representation_prh",
            "contribution": "Endpoint and trajectory must remain separate in causal and representation comparisons.",
            "nontransfer": "Better trajectory fit does not identify a biological mechanism or causal equivalence.",
        },
        {
            "edge_id": "OSM-FW-03",
            "from": "osm_learning_trajectory",
            "to": "proper_function_e",
            "contribution": "Performance and terminal geometry can leave process adequacy underdetermined.",
            "nontransfer": "Operational success does not establish proper function, objective warrant, or Wisdom.",
        },
        {
            "edge_id": "OSM-FW-04",
            "from": "osm_learning_trajectory",
            "to": "restoration",
            "contribution": "Longitudinal traces and interventions can distinguish pathways hidden by terminal labels.",
            "nontransfer": "Task learning and representational adaptation are not human or noetic restoration.",
        },
        {
            "edge_id": "OSM-FW-05",
            "from": "osm_learning_trajectory",
            "to": "tensor_search",
            "contribution": "Architecture, objective, and trajectory comparison sharpen held-out rival-model protocols.",
            "nontransfer": "A winner among tested settings is not a universal mechanism or ontology result.",
        },
    ]
    actual_crosswalk_edges = crosswalk.get("flywheel_contributions")
    if actual_crosswalk_edges != expected_crosswalk_edges:
        issues.append("osm-program-crosswalk-flywheel-collection-mismatch")
        expected_by_id = {row["edge_id"]: row for row in expected_crosswalk_edges}
        actual_by_id = {
            row.get("edge_id"): row
            for row in actual_crosswalk_edges or []
            if isinstance(row, dict)
        }
        drifted = sorted(
            edge_id
            for edge_id in set(expected_by_id) | set(actual_by_id)
            if actual_by_id.get(edge_id) != expected_by_id.get(edge_id)
        )
        issues.extend(f"osm-program-crosswalk-flywheel-drift:{edge_id}" for edge_id in drifted)
    crosswalk_edge_ids = [row.get("edge_id") for row in actual_crosswalk_edges or [] if isinstance(row, dict)]
    if len(crosswalk_edge_ids) != len(set(crosswalk_edge_ids)):
        issues.append("osm-program-crosswalk-flywheel-duplicate-id")

    expected_main_edges = [
        {
            "kind": "supports",
            "from": "source_custody",
            "to": "osm_learning_trajectory",
            "contribution": "exact article identity methods model scope code provenance and access-copy custody",
            "nontransfer": "custody does not reproduce the experiment or prove the interpretation",
        },
        {
            "kind": "supports",
            "from": "osm_learning_trajectory",
            "to": "representation_prh",
            "contribution": "endpoint and trajectory remain separate in causal and representation comparisons",
            "nontransfer": "better trajectory fit does not identify a biological mechanism or causal equivalence",
        },
        {
            "kind": "constrains",
            "from": "osm_learning_trajectory",
            "to": "proper_function_e",
            "contribution": "performance and terminal geometry can leave process adequacy underdetermined",
            "nontransfer": "operational success does not establish proper function objective warrant or Wisdom",
        },
        {
            "kind": "constrains",
            "from": "osm_learning_trajectory",
            "to": "restoration",
            "contribution": "longitudinal traces and interventions can distinguish pathways hidden by terminal labels",
            "nontransfer": "task learning and representational adaptation are not human or noetic restoration",
        },
        {
            "kind": "supports",
            "from": "osm_learning_trajectory",
            "to": "tensor_search",
            "contribution": "architecture objective and trajectory comparison sharpen held-out rival-model protocols",
            "nontransfer": "a winner among tested settings is not a universal mechanism or ontology result",
        },
    ]
    actual_main_edges = [
        row
        for row in flywheel.get("edges", []) if isinstance(flywheel, dict) and isinstance(row, dict)
        and (row.get("from") == "osm_learning_trajectory" or row.get("to") == "osm_learning_trajectory")
    ]
    if actual_main_edges != expected_main_edges:
        issues.append("osm-program-main-flywheel-collection-mismatch")
    expected_main_by_key = {(row["from"], row["to"]): row for row in expected_main_edges}
    actual_main_by_key = {(row.get("from"), row.get("to")): row for row in actual_main_edges}
    actual_main_keys = [(row.get("from"), row.get("to")) for row in actual_main_edges]
    if len(actual_main_keys) != len(set(actual_main_keys)):
        issues.append("osm-program-main-flywheel-duplicate-endpoint")
    for edge_key in sorted(set(expected_main_by_key) | set(actual_main_by_key)):
        if actual_main_by_key.get(edge_key) != expected_main_by_key.get(edge_key):
            issues.append(f"osm-program-main-flywheel-edge-drift:{edge_key[0]}:{edge_key[1]}")

    catalog_rows = catalog.get("items", []) if isinstance(catalog, dict) else []
    catalog_row = next((row for row in catalog_rows if isinstance(row, dict) and row.get("item_id") == artifact_id), {})
    expected_catalog_row = {
        "item_id": artifact_id,
        "title": "OSM learning-trajectory convergence crosswalk",
        "source_surface": "CURRENT_PUBLIC_ORTHEMOLOGY_MAIN",
        "evidence_class": "PROGRAM_OR_BURDEN_RECORD",
        "privacy_class": "PUBLIC_SAFE",
        "recommended_disposition": "PUBLIC_INTEGRATE",
        "public_locator": "DOI 10.1038/s41586-024-08548-w and source-status row LAT-1",
        "repository_relevance": "Reconnects the already integrated endpoint-versus-trajectory and latent-state source to the V11 milestone and flywheel owners without transferring empirical, normative, human, metaphysical, theorem, or meniscus credit.",
        "owner_path": OSM_PROGRAM_CROSSWALK.relative_to(ROOT).as_posix(),
        "source_access_copy_sha256": expected_hash,
        "source_access_copy_bytes": 137824,
        "campaign_epoch": "V12_PROGRAM_INTEGRATION",
    }
    if catalog_row != expected_catalog_row:
        issues.append("osm-program-evidence-catalog-mismatch")

    prompt = FABLE_OSM_PROMPT.read_text(encoding="utf-8") if FABLE_OSM_PROMPT.is_file() else ""
    prompt_tokens = (
        "fable/ar8r-convergence-research-v1",
        "Never push directly to `main`",
        "Do not transfer neuroscience evidence into metaphysics or theology",
        "Never commit it",
        "git fetch origin --prune",
        "stop unless its exact head",
    )
    if any(token not in prompt for token in prompt_tokens):
        issues.append("osm-program-fable-prompt-guard-missing")
    integrated_prompt = FABLE_INTEGRATED_PROMPT.read_text(encoding="utf-8") if FABLE_INTEGRATED_PROMPT.is_file() else ""
    issues.extend(validate_integrated_fable_prompt(integrated_prompt))
    ignore_lines = {
        line.strip()
        for line in GITIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if not {"FABLE_LOCAL_START.md", "FABLE_LOCAL_SOURCES/"}.issubset(ignore_lines):
        issues.append("integrated-fable-local-input-ignore-contract-missing")
    if not OSM_PROGRAM_NOTE.is_file():
        issues.append("osm-program-human-readable-owner-missing")
    return list(dict.fromkeys(issues))


def validate_task7_public_privacy() -> list[str]:
    issues: list[str] = []
    private_pdf = "C2680D5A-8FAE-11F1-A320-F5FC2CA0B584.pdf"
    private_pattern = re.compile(r"(?:[A-Za-z]:\\|/mnt/data/|sandbox:|file://|data-message-id|screen-threadFlyOut|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b)", re.I)
    paths = [
        DEEP_CONTEXT_RECEIPT, A_TO_N, BRIDGE_LEDGER, PROPER_FUNCTION_MATRIX, ONTOLOGY_MATRIX,
        TAC_REGISTRY, PMR_MAP, LEAN_QUEUE, TEN_CONFLICT, FAMILY_CROSSWALK, CONNES_RECEIPT,
        LEAN_V7, OSW15, TWO_THREAD_RECEIPT, MILESTONE_CHARTER, MILESTONES,
        COMPATIBILITY_OVERLAY, ASCENT_V2, SURFACE_CUSTODY, FLYWHEEL, PROJECTION,
        OSM_PROGRAM_CROSSWALK, OSM_PROGRAM_NOTE, FABLE_OSM_PROMPT, FABLE_INTEGRATED_PROMPT,
    ]
    paths.extend(path for path in DEFERRED_EXACT.rglob("*") if path.is_file())
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if private_pdf.lower() in text.lower():
            issues.append(f"task7-private-pdf-name:{path.relative_to(ROOT)}")
        if private_pattern.search(text):
            issues.append(f"task7-private-locator:{path.relative_to(ROOT)}")
    return list(dict.fromkeys(issues))


def validate_packet() -> list[str]:
    issues: list[str] = []
    for path in (
        CATALOG,
        LEDGER,
        FIXTURE,
        PROJECTION,
        ORIGIN_V5,
        ORIGIN_V6,
        RECOVERY_OVERLAY,
        SOURCE_UNIVERSE,
        SOURCE_UNIVERSE_V2,
        HISTORICAL_COLLISION_RECEIPT,
        HISTORICAL_COLLISION_PAYLOAD,
        POST_MERGE_CATALOG,
        THREAD_CUSTODY,
        LINK_DRIFT,
        PMR007_RECEIPT,
        PMR007_CORRECTION,
        PMR007_DEEP_RECEIPT,
        PMR007_DEEP_EXECUTION,
        PMR007_DEEP_CORRECTION,
        VISIBLE_SOURCE_MANIFEST,
        FILE_CARD_ARCHIVE_CONFLICTS,
        DEEP_CONTEXT_RECEIPT,
        A_TO_N,
        BRIDGE_LEDGER,
        PROPER_FUNCTION_MATRIX,
        ONTOLOGY_MATRIX,
        TAC_REGISTRY,
        PMR_MAP,
        LEAN_QUEUE,
        TEN_CONFLICT,
        FAMILY_CROSSWALK,
        CONNES_RECEIPT,
        LEAN_V7,
        OSW15,
        SURFACE_CUSTODY,
        FLYWHEEL,
        TWO_THREAD_RECEIPT,
        MILESTONE_CHARTER,
        MILESTONES,
        FABLE_INTEGRATED_PROMPT,
        COMPATIBILITY_OVERLAY,
        ASCENT_V2,
        CURRENT_STATE,
        *SOURCE_RECEIPTS,
    ):
        if not path.is_file():
            issues.append(f"missing-file:{path.relative_to(ROOT)}")
    if issues:
        return issues

    catalog = load_yaml(CATALOG)
    ledger = load_yaml(LEDGER)
    if not isinstance(catalog, dict) or not isinstance(ledger, dict):
        return ["malformed-catalog-or-ledger"]

    items = catalog.get("items", [])
    rows = ledger.get("items", [])
    if not isinstance(items, list) or not isinstance(rows, list):
        return ["malformed-catalog-or-ledger-items"]

    item_ids = [item.get("item_id") for item in items if isinstance(item, dict)]
    row_ids = [row.get("item_id") for row in rows if isinstance(row, dict)]
    if len(item_ids) != len(set(item_ids)):
        issues.append("duplicate-catalog-item-id")
    if len(row_ids) != len(set(row_ids)):
        issues.append("duplicate-ledger-item-id")
    if set(item_ids) != set(row_ids):
        issues.append("catalog-ledger-coverage-mismatch")
    if len(item_ids) < 128:
        issues.append("claim-level-catalog-regressed")

    downloads = [
        item for item in items
        if isinstance(item, dict) and item.get("source_surface") == "V8_DOWNLOADED_FILE"
    ]
    if len(downloads) != 65:
        issues.append("download-coverage-mismatch")

    for item in items:
        if not isinstance(item, dict):
            issues.append("malformed-catalog-row")
            continue
        privacy = item.get("privacy_class")
        disposition = item.get("recommended_disposition")
        if privacy == "PRIVATE_EXCLUDED" and disposition in {"PUBLIC_INTEGRATE", "PUBLIC_SUMMARY"}:
            issues.append(f"private-publication-violation:{item.get('item_id')}")
        if disposition == "SUPERSEDED_EXACT_VERSION" and item.get("current_authority") is True:
            issues.append(f"superseded-current-authority:{item.get('item_id')}")
        if item.get("campaign_epoch") == "LATER_PMR_CHARTER" and item.get("source_surface") != "SUPPLIED_LATER_PMR_ADDENDUM":
            issues.append(f"later-pmr-epoch-source-mismatch:{item.get('item_id')}")

    independent_by_hash: dict[str, list[str]] = {}
    for item in items:
        if not isinstance(item, dict) or not item.get("independent_evidence_credit"):
            continue
        digest = item.get("sha256")
        if digest:
            independent_by_hash.setdefault(digest, []).append(item.get("item_id", "?"))
    for digest, credited in independent_by_hash.items():
        if len(credited) > 1:
            issues.append(f"duplicate-byte-independent-credit:{digest}")

    dispositions = Counter(
        row.get("disposition") for row in rows if isinstance(row, dict)
    )
    if dispositions.get(None):
        issues.append("missing-terminal-disposition")
    allowed_publication_states = {
        "INTEGRATED",
        "MATERIALIZED_PUBLIC_PROPOSAL_NOT_ADOPTED",
        "DEFERRED",
        "BLOCKED",
        "EXCLUDED",
    }
    for row in rows:
        if not isinstance(row, dict):
            continue
        publication_state = row.get("publication_state")
        if publication_state not in allowed_publication_states:
            issues.append(f"invalid-publication-state:{row.get('item_id')}:{publication_state}")
        if publication_state == "MATERIALIZED_PUBLIC_PROPOSAL_NOT_ADOPTED":
            owner = ROOT / row.get("owner_path", "")
            if not owner.exists():
                issues.append(f"materialized-proposal-owner-missing:{row.get('item_id')}")

    fixture = load_yaml(FIXTURE)
    fixture_issues = validate_campaign_state(fixture)
    expected = fixture.get("expected_issue_codes", []) if isinstance(fixture, dict) else []
    for code in expected:
        if code not in fixture_issues:
            issues.append(f"negative-fixture-not-detected:{code}")
    if not fixture_issues:
        issues.append("negative-fixture-unexpectedly-valid")

    projection = load_yaml(PROJECTION)
    projection_issues = validate_campaign_state(projection)
    for code in projection_issues:
        issues.append(f"current-campaign-projection:{code}")
    if isinstance(projection, dict):
        for records in projection.get("ledgers", {}).values():
            if not isinstance(records, list):
                continue
            for record in records:
                if not isinstance(record, dict):
                    continue
                owner = record.get("owner_path")
                if not owner or not (PACKET / owner).is_file():
                    issues.append(f"missing-campaign-owner:{record.get('id', '?')}")

    origin_v5 = load_yaml(ORIGIN_V5)
    origin_v6 = load_yaml(ORIGIN_V6)
    overlay = load_yaml(RECOVERY_OVERLAY)
    if len(origin_v5.get("theorems", [])) != 514:
        issues.append("v5-origin-row-loss")
    if origin_v5.get("counts", {}).get("raw_active_ar8r_theorem_records") != 382:
        issues.append("v5-active-count-mismatch")
    if origin_v5.get("counts", {}).get("focused_exact_relation_edges") != 74:
        issues.append("v5-relation-edge-count-mismatch")
    if origin_v5.get("public_sanitization", {}).get("redacted_absolute_path_occurrences") != 2:
        issues.append("v5-public-sanitization-mismatch")
    if origin_v6.get("base_registry", {}).get("all_registry_records") != 514:
        issues.append("v6-base-row-count-mismatch")
    if overlay.get("counts", {}).get("target_identities") != 42:
        issues.append("v8-overlay-target-count-mismatch")

    universe = load_yaml(SOURCE_UNIVERSE)
    expected_universes = {
        "V7_MESSAGE_INDEX": 95,
        "V7_ACTIVITY_INDEX": 44,
        "V7_ATTACHMENT_INDEX": 1127,
        "V8_ATTACHMENT_FINAL_CLASSIFICATION": 1127,
        "V8_FIRST_PARTY_ATTACHMENT_UNIVERSE": 464,
        "V8_ACTIVITY_ASSESSMENT": 1490,
        "V8_ACTIVITY_FILE_REFERENCES": 17293,
        "V8_DOWNLOADED_FILES": 65,
    }
    actual_universes = {row.get("surface"): row.get("rows") for row in universe.get("source_universes", []) if isinstance(row, dict)}
    for surface, count in expected_universes.items():
        if actual_universes.get(surface) != count:
            issues.append(f"source-universe-count-mismatch:{surface}")
    for mapping in universe.get("closure_maps", []):
        path = PACKET / "provenance" / mapping.get("path", "")
        if not path.is_file():
            issues.append(f"missing-closure-map:{mapping.get('path')}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != mapping.get("sha256"):
            issues.append(f"closure-map-hash-mismatch:{mapping.get('path')}")
        with path.open(encoding="utf-8", newline="") as handle:
            rows = sum(1 for _ in csv.reader(handle)) - 1
        if rows != mapping.get("rows"):
            issues.append(f"closure-map-row-count-mismatch:{mapping.get('path')}")

    universe_v2 = load_yaml(SOURCE_UNIVERSE_V2)
    expected_v11_ledgers = {
        "V11_ATTACHMENT_INDEX": ("a236e9d40b2ed376953e7fce0d384224509a6567ac2549840b4bb3c764424b57", 1007),
        "V11_DOWNLOAD_AND_ARCHIVE_LEDGER_CSV": ("d1aa7644474123e2ae54c2cc46ea1bba9e7a40bde42447cd9c51dd75d69ba332", 187),
        "V11_DOWNLOAD_AND_ARCHIVE_LEDGER_JSONL": ("89caf73dcf7644acd0cd14b71a5b97ce872ac92361a171a5f9f6928ee91e0f06", 161),
        "V11_ARCHIVE_INTEGRITY_AND_EXTRACTION_LEDGER": ("35f8312da49dd8ab5d198755a17a5b0101543e4cb1a099439458a7f36b6300a7", 10),
        "V11_ARCHIVE_MEMBER_HASH_LEDGER": ("9c034a9d65a9cb6c6c5a9890ae3fb15eb850372dcca821f88845b65a428769ad", 957),
    }
    actual_v11_ledgers = {
        row.get("surface"): (row.get("sha256"), row.get("rows"))
        for row in universe_v2.get("immutable_v11_source_ledgers", [])
        if isinstance(row, dict)
    }
    for surface, expected in expected_v11_ledgers.items():
        if actual_v11_ledgers.get(surface) != expected:
            issues.append(f"v11-source-ledger-receipt-mismatch:{surface}")

    expected_v11_maps = {
        "AR8R-V11-ATTACHMENT-ROW-DISPOSITION-MAP-V1.csv": 1007,
        "AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv": 187,
        "AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv": 10,
        "AR8R-V11-ARCHIVE-MEMBER-HASH-DISPOSITION-MAP-V1.csv": 506,
    }
    public_exact_hashes, public_mentioned_hashes = public_hash_evidence()
    mapped_paths: dict[str, Path] = {}
    for mapping in universe_v2.get("terminal_maps", []):
        if not isinstance(mapping, dict):
            continue
        name = mapping.get("path", "")
        path = SOURCE_UNIVERSE_V2.parent / name
        mapped_paths[name] = path
        if name not in expected_v11_maps:
            issues.append(f"unexpected-v11-terminal-map:{name}")
            continue
        if not path.is_file():
            issues.append(f"missing-v11-terminal-map:{name}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != mapping.get("sha256"):
            issues.append(f"v11-terminal-map-hash-mismatch:{name}")
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            mapped_rows = list(reader)
            fieldnames = reader.fieldnames
        if len(mapped_rows) != expected_v11_maps[name] or mapping.get("rows") != len(mapped_rows):
            issues.append(f"v11-terminal-map-row-count-mismatch:{name}")
        issues.extend(
            validate_v11_terminal_map_rows(
                name,
                fieldnames,
                mapped_rows,
                public_exact_hashes=public_exact_hashes,
                public_mentioned_hashes=public_mentioned_hashes,
            )
        )
    if set(mapped_paths) != set(expected_v11_maps):
        issues.append("v11-terminal-map-set-mismatch")

    download_map = mapped_paths.get("AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv")
    if download_map and download_map.is_file():
        with download_map.open(encoding="utf-8", newline="") as handle:
            download_map_rows = list(csv.DictReader(handle))
        distinct_hashes = {row["sha256"] for row in download_map_rows if row.get("sha256")}
        if len(distinct_hashes) != 157:
            issues.append("v11-download-distinct-hash-count-mismatch")
        if sum(not bool(row.get("sha256")) for row in download_map_rows) != 9:
            issues.append("v11-download-unhashed-boundary-count-mismatch")
        if any(row.get("disposition") == "PRIVATE_OR_DUPLICATE_OR_UNSELECTED_SOURCE_NO_PUBLIC_IMPORT" for row in download_map_rows):
            issues.append("v11-download-source-left-generically-unclassified")

    archive_map = mapped_paths.get("AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv")
    if archive_map and archive_map.is_file():
        with archive_map.open(encoding="utf-8", newline="") as handle:
            archive_rows = list(csv.DictReader(handle))
        archive5 = [row for row in archive_rows if row.get("archive_sequence") == "5"]
        if len(archive5) != 1 or archive5[0].get("sha256") != "141deffc4323225e549149ba35b6d2ae55007242459bfb513957420b189a78e8":
            issues.append("v11-archive5-custody-mismatch")
        elif archive5[0].get("disposition") != "SUPERSEDED_BOUNDARY_CHECKPOINT_PRIVATE_NO_PUBLIC_IMPORT":
            issues.append("v11-archive5-disposition-mismatch")
        if any(row.get("integrity_status") != "PASS" for row in archive_rows):
            issues.append("v11-archive-integrity-regression")

    dual_relations = universe_v2.get("dual_hash_relations", [])
    if len(dual_relations) != 1 or not isinstance(dual_relations[0], dict):
        issues.append("v11-dual-hash-relation-missing")
    else:
        relation = dual_relations[0]
        summary_path = (SOURCE_UNIVERSE_V2.parent / relation.get("public_summary_path", "")).resolve()
        try:
            summary_path.relative_to(ROOT.resolve())
        except ValueError:
            issues.append("v11-dual-hash-summary-path-escape")
        if not summary_path.is_file():
            issues.append("v11-dual-hash-summary-missing")
        else:
            if hashlib.sha256(summary_path.read_bytes()).hexdigest() != relation.get("public_summary_sha256"):
                issues.append("v11-dual-hash-summary-mismatch")
            if summary_path.stat().st_size != relation.get("public_summary_bytes"):
                issues.append("v11-dual-hash-summary-size-mismatch")
        if relation.get("source_exact_sha256") != "31fa5b249ede9a5cd7ee180c175f432fdd29c2d94d43321de95a0ecc40b08d9e":
            issues.append("v11-dual-hash-source-mismatch")
        if relation.get("identity_claim") != "SUMMARY_IS_NOT_EXACT_SOURCE_BYTES":
            issues.append("v11-dual-hash-identity-boundary-missing")

    collision = load_yaml(HISTORICAL_COLLISION_RECEIPT)
    expected_collision_hash = "6e5f8fde52bd69c4c8e678b0ab7f0e2d5345ff4cf261cf143a7ecbb3c64835c5"
    if not HISTORICAL_COLLISION_PAYLOAD.is_file():
        issues.append("historical-collision-payload-missing")
    else:
        if HISTORICAL_COLLISION_PAYLOAD.stat().st_size != 1408:
            issues.append("historical-collision-payload-size-mismatch")
        if hashlib.sha256(HISTORICAL_COLLISION_PAYLOAD.read_bytes()).hexdigest() != expected_collision_hash:
            issues.append("historical-collision-payload-hash-mismatch")
    if hashlib.sha256(ORIGIN_V5.read_bytes()).hexdigest() != "52b1df2961b080bd0c05519883094fc2cd9a93413ca8c1bb1f7935a3a24b0841":
        issues.append("historical-collision-v5-registry-changed")
    collision_rows = collision.get("collisions", []) if isinstance(collision, dict) else []
    recovered = next((row for row in collision_rows if row.get("collision_safe_recovery_identity") == "AR8R-HR-P236P242-T236-v1"), None)
    if not recovered:
        issues.append("historical-collision-recovery-row-missing")
    else:
        if recovered.get("exact_payload_sha256") != expected_collision_hash or recovered.get("exact_payload_bytes") != 1408:
            issues.append("historical-collision-receipt-payload-mismatch")
        if recovered.get("owner_adoption") != "PENDING" or recovered.get("credit_effect") != "NONE":
            issues.append("historical-collision-recovery-promotion")
    if collision.get("source_boundary", {}).get("original_historical_file_bytes_recovered") is not False:
        issues.append("historical-collision-original-byte-overclaim")
    canonical_t236 = next((row for row in origin_v5.get("theorems", []) if row.get("id") == "AR8R-T236"), {})
    if "authenticated root support" not in canonical_t236.get("statement", ""):
        issues.append("canonical-t236-identity-drift")
    if any(row.get("id") == "AR8R-HR-P236P242-T236-v1" for row in origin_v5.get("theorems", [])):
        issues.append("collision-recovery-injected-into-v5")

    post_merge = load_yaml(POST_MERGE_CATALOG)
    issues.extend(validate_post_merge_catalog(post_merge))

    source_counts = {
        PACKET / "programs" / "full-program-reentry-v2-source": 22,
        PACKET / "post-merge-pmr001-source": 27,
        PACKET / "post-merge-pmr002-006-source": 12,
    }
    for source_dir, expected_count in source_counts.items():
        actual_count = sum(1 for path in source_dir.rglob("*") if path.is_file())
        if actual_count != expected_count:
            issues.append(f"post-merge-source-count-mismatch:{source_dir.name}")

    receipt = load_yaml(PMR007_RECEIPT)
    if receipt.get("source_archive", {}).get("sha256") != "d7a44100b72218988b3f6d116048d31fffe3997d278e855542207b5a84769e64":
        issues.append("pmr007-proposal-archive-hash-mismatch")
    if receipt.get("proposal_boundary", {}).get("result_count") != 10:
        issues.append("pmr007-proposal-result-count-mismatch")

    sums_path = PMR007_PROPOSAL / "SHA256SUMS"
    listed: set[str] = set()
    if not sums_path.is_file():
        issues.append("pmr007-missing-internal-sha256sums")
    else:
        for line in sums_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, relative = line.split(maxsplit=1)
            relative = relative.lstrip("*").replace("\\", "/")
            target = PMR007_PROPOSAL / relative
            listed.add(relative)
            if not target.is_file():
                issues.append(f"pmr007-missing-checksummed-member:{relative}")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                issues.append(f"pmr007-member-hash-mismatch:{relative}")
        actual = {
            path.relative_to(PMR007_PROPOSAL).as_posix()
            for path in PMR007_PROPOSAL.rglob("*")
            if path.is_file() and path.name != "SHA256SUMS"
        }
        if len(listed) != 130 or listed != actual:
            issues.append("pmr007-internal-sha256sums-coverage-mismatch")

    issues.extend(validate_post_merge_thread_custody(load_yaml(THREAD_CUSTODY)))
    issues.extend(validate_link_drift(load_yaml(LINK_DRIFT)))
    issues.extend(validate_pmr007_correction(PMR007_CORRECTION.read_text(encoding="utf-8")))

    deep_receipt_owner = load_yaml(PMR007_DEEP_RECEIPT)
    issues.extend(validate_pmr007_deep_execution(load_yaml(PMR007_DEEP_EXECUTION)))
    deep_index = load_yaml(PMR007_DEEP_PROPOSAL / "PROPOSED_RESULT_INDEX.yaml")
    issues.extend(
        validate_pmr007_deep_proposal(
            deep_index,
            deep_receipt_owner,
            PMR007_DEEP_CORRECTION.read_text(encoding="utf-8"),
        )
    )
    deep_sums = PMR007_DEEP_PROPOSAL / "SHA256SUMS"
    deep_listed: set[str] = set()
    if not deep_sums.is_file():
        issues.append("pmr007-deep-missing-internal-sha256sums")
    else:
        for line in deep_sums.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, relative = line.split(maxsplit=1)
            relative = relative.lstrip("*").replace("\\", "/")
            target = PMR007_DEEP_PROPOSAL / relative
            deep_listed.add(relative)
            if not target.is_file():
                issues.append(f"pmr007-deep-missing-checksummed-member:{relative}")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                issues.append(f"pmr007-deep-member-hash-mismatch:{relative}")
        deep_actual = {
            path.relative_to(PMR007_DEEP_PROPOSAL).as_posix()
            for path in PMR007_DEEP_PROPOSAL.rglob("*")
            if path.is_file() and path.name != "SHA256SUMS"
        }
        if len(deep_listed) != 830 or deep_listed != deep_actual:
            issues.append("pmr007-deep-internal-sha256sums-coverage-mismatch")

    issues.extend(validate_visible_source_manifest(load_yaml(VISIBLE_SOURCE_MANIFEST)))
    issues.extend(validate_file_card_archive_conflicts(load_yaml(FILE_CARD_ARCHIVE_CONFLICTS)))
    for source_receipt in SOURCE_RECEIPTS:
        issues.extend(validate_source_receipt(load_yaml(source_receipt)))

    issues.extend(validate_deferred_exact_source())
    issues.extend(validate_a_to_n_architecture(load_yaml(A_TO_N)))
    issues.extend(validate_bridge_ledger(load_yaml(BRIDGE_LEDGER)))
    issues.extend(validate_typed_matrices(load_yaml(PROPER_FUNCTION_MATRIX), load_yaml(ONTOLOGY_MATRIX), load_yaml(TAC_REGISTRY)))
    issues.extend(validate_formalization_owners(load_yaml(PMR_MAP), load_yaml(LEAN_QUEUE), load_yaml(TEN_CONFLICT), load_yaml(FAMILY_CROSSWALK)))
    issues.extend(validate_connes_and_osw(load_yaml(CONNES_RECEIPT), load_yaml(OSW15), load_yaml(LEAN_V7)))

    deep_receipt = load_yaml(DEEP_CONTEXT_RECEIPT)
    if deep_receipt.get("selection_totals") != {"files": 24, "bytes": 84163} or len(deep_receipt.get("members", [])) != 24:
        issues.append("deep-context-receipt-selection-mismatch")
    if any(row.get("adoption_effect") != "NONE" for row in deep_receipt.get("members", []) if isinstance(row, dict)):
        issues.append("deep-context-receipt-adoption-promoted")
    issues.extend(validate_task7_ledgers_and_crosswalks(catalog, ledger, load_yaml(SURFACE_CUSTODY), load_yaml(FLYWHEEL), load_yaml(TWO_THREAD_RECEIPT)))
    issues.extend(validate_milestone_architecture(load_yaml(MILESTONES)))
    issues.extend(validate_task7a_owner_integration())
    issues.extend(validate_osm_program_integration(load_yaml(OSM_PROGRAM_CROSSWALK), load_yaml(MILESTONES), load_yaml(FLYWHEEL), catalog))
    issues.extend(validate_task7_public_privacy())

    current_state = load_yaml(CURRENT_STATE)
    task7_state = current_state.get("authored", {}).get("ar8r_v11_task7", {}) if isinstance(current_state, dict) else {}
    expected_task7_state = {
        "candidate_e_status": "DEFERRED_INSUFFICIENT_AUDIT",
        "candidate_g_status": "DEFERRED_INSUFFICIENT_AUDIT",
        "pmr007_owner_adoption": "PENDING",
        "t354_status": "BLOCKED_FORMAL_DEFECT",
        "ten_advances_comparator_count": "CONFLICTING_38_42",
        "connes_rigidity_status": "UNRESOLVED_PENDING_OPERATOR_ALGEBRA_SPECIALIST_REVIEW",
        "lean_machine_check_claim": "NONE",
        "integrated_champion": "NO_INTEGRATED_CHAMPION",
        "meniscus": "MENISCUS_NOT_REACHED",
        "natural_closure": "NATURAL_CLOSURE_NOT_REACHED",
    }
    if any(task7_state.get(key) != value for key, value in expected_task7_state.items()):
        issues.append("current-state-task7-authority-mismatch")

    return list(dict.fromkeys(issues))


def main() -> int:
    issues = validate_packet()
    if issues:
        for issue in issues:
            print(f"[FAIL] {issue}")
        print(f"TOTAL: {len(issues)} failures")
        return 1
    print(f"[PASS] 65 downloaded-file rows and {len(load_yaml(CATALOG)['items'])} claim-level rows have exact terminal dispositions")
    print("[PASS] private, superseded, and duplicate-credit publication gates")
    print("[PASS] false-zero campaign fixture rejected with required issue codes")
    print("[PASS] live V11 campaign projection reconciles every controlling open owner")
    print("[PASS] complete 514-row V5 authority and 42-target V8 overlay remain separate")
    print("[PASS] structural closure maps cover messages, attachments, Activity, references, and archive hashes")
    print("[PASS] post-merge full-program and PMR source packets retain exact public-safe custody")
    print("[PASS] PMR-007 Rounds 11-20 and Deep A-AP remain external-review proposals with all internal hashes verified")
    print("[PASS] new-thread custody and six historical-link drift incidents are explicitly reconciled")
    print("[PASS] Task 7 deferred exact source, A-N/bridge owners, typed matrices, PMR/Lean map, and family crosswalk")
    print("[PASS] Connes dispute dispositions, OSW-15 coordinates, private-source boundary, and static-only Lean V7 status")
    print("[PASS] Task 7A owner charter, 18 milestones, 9 non-adopted meniscus candidates, crosswalks, and anti-promotion controls")
    print("[PASS] V12 OSM learning-trajectory program crosswalk and anti-transfer gates")
    print("AR8R V11 reconciliation packet: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
