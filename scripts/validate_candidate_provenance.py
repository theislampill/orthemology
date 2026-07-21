#!/usr/bin/env python3
"""Validate the provenance-qualified R7E candidate occurrence ledger.

The preserved R7E state and Markdown backlog are historical inputs.  This
validator requires a one-to-one immutable mapping of every parseable survivor
row while preventing implementing-run attributions, truncated text, missing
artifacts, or observed attachments from being promoted into verification.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "orthing-candidate-ledger.schema.json"
LEDGER_PATH = ROOT / "docs" / "project-closure" / "r7e-sol" / "ORTHING-CANDIDATE-LEDGER.json"
PROVENANCE_PATH = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-INPUT-PROVENANCE.json"
BACKLOG_PATH = ROOT / "docs" / "project-closure" / "r7e" / "ORTHING-CANDIDATE-BACKLOG.md"

EXPECTED_ARTIFACT_IDS = {
    "workflow-journal",
    "per-agent-reports",
    "full-candidate-drafts",
    "rebake-attachment",
    "maximaltrajectory-attachment",
    "rejection-records",
}
MISSING_ARTIFACT_IDS = {
    "workflow-journal",
    "per-agent-reports",
    "full-candidate-drafts",
}
ATTACHMENT_IDS = {"rebake-attachment", "maximaltrajectory-attachment"}
EXPECTED_PROVENANCE_BOUNDARIES = {
    "R7E-PROV-B001-IDENTITY-COLLAPSE": (
        "turn identity may equal orthing identity or session identity may equal "
        "episode identity"
    ),
    "R7E-PROV-B002-EPISODE-INDEPENDENCE": (
        "episode IDs prove independent observations"
    ),
    "R7E-PROV-B003-RETROSPECTIVE-LIVE-CAPTURE": (
        "retrospective reconstruction may be treated as live capture"
    ),
    "R7E-PROV-B004-EVIDENCE-BACKDATING": (
        "current Sol evidence may be inserted into the original R7E t1 evidence state"
    ),
    "R7E-PROV-B005-DEFECT-LOCUS-COLLAPSE": (
        "a single sound/unsound field may replace defect-locus accounting"
    ),
    "R7E-PROV-B006-UNCONTROLLED-RECURRENCE": (
        "recurrence may be claimed without controlled fingerprint and distinct-source "
        "accounting"
    ),
    "R7E-PROV-B007-INFERRED-REJECTION": (
        "missing rejection records or rationale may be inferred"
    ),
}


def parse_legacy_rows(text: str) -> list[dict[str, object]]:
    rows = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6 or cells[0] == "id" or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(
            {
                "legacy_line": line_number,
                "legacy_id": cells[0],
                "topic": cells[1],
                "legacy_disposition": cells[2],
                "substance": cells[3],
                "legacy_sourcing_claim": cells[4],
                "target_text": cells[5],
            }
        )
    return rows


def parse_rejection_count(text: str) -> int:
    if "## Rejected by the adversarial pass" not in text or "## Survivors" not in text:
        return 0
    section = text.split("## Rejected by the adversarial pass", 1)[1].split(
        "## Survivors", 1
    )[0]
    return sum(1 for line in section.splitlines() if re.match(r"^- \*\*.+\*\*", line))


def _schema_issues(ledger: object) -> list[str]:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError) as exc:
        return ["ledger schema unavailable or malformed: %s" % exc]
    errors = sorted(
        Draft202012Validator(schema).iter_errors(ledger),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    issues = []
    for error in errors:
        locus = ".".join(str(part) for part in error.absolute_path) or "<root>"
        issues.append("ledger schema %s: %s" % (locus, error.message))
    return issues


def _mapping_issues(ledger: dict[str, object], expected: list[dict[str, object]]) -> list[str]:
    issues = []
    rows = ledger.get("rows")
    if not isinstance(rows, list):
        return ["legacy occurrence mapping rows must be an array"]

    mappings = [row for row in rows if isinstance(row, dict)]
    if len(mappings) != len(rows):
        issues.append("legacy occurrence mapping contains a non-object row")

    immutable_ids = [row.get("immutable_id") for row in mappings]
    if len(immutable_ids) != len(set(map(str, immutable_ids))):
        issues.append("legacy occurrence mapping has duplicate immutable IDs")

    actual_lines = [row.get("legacy_line") for row in mappings]
    expected_lines = [row["legacy_line"] for row in expected]
    if Counter(actual_lines) != Counter(expected_lines):
        issues.append("legacy occurrence mapping is missing or multiply maps source lines")

    expected_by_line = {row["legacy_line"]: row for row in expected}
    for row in mappings:
        line = row.get("legacy_line")
        source = expected_by_line.get(line)
        if not source:
            continue
        expected_id = "R7E-BACKLOG-L%04d" % line
        if row.get("immutable_id") != expected_id:
            issues.append("legacy occurrence mapping at line %s has unstable immutable ID" % line)
        if row.get("legacy_id") != source["legacy_id"]:
            issues.append("legacy occurrence mapping at line %s changes legacy_id" % line)
        for key in ("topic", "legacy_disposition", "substance", "legacy_sourcing_claim"):
            if row.get(key) != source[key]:
                issues.append("legacy occurrence mapping at line %s changes %s" % (line, key))

        target = row.get("target")
        if not isinstance(target, dict):
            issues.append("legacy occurrence mapping at line %s has malformed target" % line)
            continue
        if target.get("text") != source["target_text"]:
            issues.append("legacy occurrence mapping at line %s changes truncated target text" % line)
        if target.get("completeness") != "truncated":
            issues.append("truncated source target at line %s cannot be marked complete" % line)
        target_text = str(target.get("text", ""))
        leaf = target_text.rstrip("/").rsplit("/", 1)[-1]
        if (
            target.get("reference_state") == "repository-verified"
            and "/" in target_text
            and "." not in leaf
        ):
            issues.append("extensionless target at line %s cannot be repository-verified" % line)
        if row.get("evidence_state") != "implementing-run-attributed":
            issues.append("legacy occurrence at line %s promotes attribution to verification" % line)
        if row.get("scholarship_status") != "not-independently-verified":
            issues.append("legacy sourcing claim at line %s is not verified scholarship" % line)

    ids = [str(row["legacy_id"]) for row in expected]
    duplicate_ids = {legacy_id for legacy_id, count in Counter(ids).items() if count > 1}
    expected_summary = {
        "legacy_row_count": len(expected),
        "unique_legacy_id_count": len(set(ids)),
        "reused_occurrence_count": len(expected) - len(set(ids)),
        "duplicate_legacy_id_count": len(duplicate_ids),
        "mapped_occurrence_count": len(mappings),
        "available_rejection_record_count": 8,
        "implementing_run_attributed_rejection_count": 16,
        "missing_rejection_record_count": 8,
    }
    summary = ledger.get("summary")
    if not isinstance(summary, dict):
        issues.append("ledger summary must be an object")
    else:
        for key, value in expected_summary.items():
            if summary.get(key) != value:
                issues.append("ledger summary %s must equal %s" % (key, value))
    return issues


def _provenance_issues(provenance: object, rejection_count: int) -> list[str]:
    if not isinstance(provenance, dict):
        return ["provenance document must be an object"]
    issues = []
    artifacts = provenance.get("artifacts")
    if not isinstance(artifacts, list):
        return ["provenance artifacts must be an array"]
    artifact_rows = [row for row in artifacts if isinstance(row, dict)]
    if len(artifact_rows) != len(artifacts):
        issues.append("provenance artifacts contain a non-object row")
    ids = [str(row.get("artifact_id")) for row in artifact_rows]
    if set(ids) != EXPECTED_ARTIFACT_IDS or len(ids) != len(set(ids)):
        issues.append("provenance artifact inventory is incomplete or duplicated")
    by_id = {str(row.get("artifact_id")): row for row in artifact_rows}

    boundaries = provenance.get("provenance_boundaries")
    if not isinstance(boundaries, list):
        issues.append("provenance boundaries must be an array")
    else:
        boundary_rows = [row for row in boundaries if isinstance(row, dict)]
        if len(boundary_rows) != len(boundaries):
            issues.append("provenance boundaries contain a non-object row")
        boundary_ids = [str(row.get("boundary_id")) for row in boundary_rows]
        if (
            set(boundary_ids) != set(EXPECTED_PROVENANCE_BOUNDARIES)
            or len(boundary_ids) != len(set(boundary_ids))
        ):
            issues.append("provenance boundary inventory is incomplete, duplicated, or expanded")
        boundaries_by_id = {
            str(row.get("boundary_id")): row for row in boundary_rows
        }
        for boundary_id, assertion in EXPECTED_PROVENANCE_BOUNDARIES.items():
            row = boundaries_by_id.get(boundary_id, {})
            if (
                set(row) != {"boundary_id", "status", "assertion"}
                or row.get("status") != "disallowed"
                or row.get("assertion") != assertion
            ):
                issues.append(
                    "%s provenance boundary must remain exact and disallowed" % boundary_id
                )

    for artifact_id in MISSING_ARTIFACT_IDS:
        row = by_id.get(artifact_id, {})
        if row.get("availability") != "missing" or row.get("evidence_state") != "missing":
            issues.append("missing artifact %s cannot be marked verified" % artifact_id)
        if row.get("original_run_binding") != "unresolved":
            issues.append("missing artifact %s cannot have a resolved run binding" % artifact_id)

    for artifact_id in ATTACHMENT_IDS:
        row = by_id.get(artifact_id, {})
        if row.get("availability") != "attachment-observed" or row.get(
            "evidence_state"
        ) != "attachment-observed":
            issues.append("attachment %s must remain attachment-observed" % artifact_id)
        if row.get("original_run_binding") != "unresolved":
            issues.append("attachment %s original-run binding remains unresolved" % artifact_id)
        if row.get("repository_source") is not False:
            issues.append("attachment %s is not a repository source" % artifact_id)

    rejection = by_id.get("rejection-records", {})
    if (
        rejection.get("availability") != "partial-repository"
        or rejection.get("evidence_state") != "repository-verified-partial"
        or rejection.get("preserved_count") != rejection_count
        or rejection.get("reported_count") != 16
        or rejection.get("missing_count") != 8
    ):
        issues.append("rejection artifact must preserve the verified eight-of-sixteen partial record")

    statistics = provenance.get("reported_statistics")
    if not isinstance(statistics, list) or not statistics:
        issues.append("reported statistics must be a non-empty array")
    else:
        for index, row in enumerate(statistics):
            if not isinstance(row, dict):
                issues.append("reported statistic %s must be an object" % index)
                continue
            if row.get("evidence_state") != "implementing-run-attributed":
                issues.append("reported statistic %s cannot be independently verified" % index)
            if row.get("independently_reconstructed") is not False:
                issues.append("reported statistic %s was not independently reconstructed" % index)

    coverage = provenance.get("coverage")
    if not isinstance(coverage, dict):
        issues.append("provenance coverage must be an object")
    else:
        if coverage.get("complete") is not False:
            issues.append("provenance completeness must remain false while artifacts are missing")
        if coverage.get("mapped_parseable_survivor_rows") != 221:
            issues.append("provenance coverage survivor count drift")
        if coverage.get("available_rejection_records") != 8 or coverage.get(
            "missing_rejection_records"
        ) != 8:
            issues.append("provenance coverage rejection count drift")
        if set(coverage.get("missing_artifact_ids") or []) != MISSING_ARTIFACT_IDS:
            issues.append("provenance coverage missing-artifact inventory drift")
        if set(coverage.get("unresolved_attachment_bindings") or []) != ATTACHMENT_IDS:
            issues.append("provenance coverage attachment-binding inventory drift")
    return issues


def collect_issues(ledger: object, provenance: object, backlog_text: str) -> list[str]:
    issues = _schema_issues(ledger)
    expected = parse_legacy_rows(backlog_text)
    rejection_count = parse_rejection_count(backlog_text)
    if len(expected) != 221:
        issues.append("preserved backlog must expose exactly 221 parseable legacy rows")
    if rejection_count != 8:
        issues.append("preserved backlog must expose exactly eight rejection records")
    if isinstance(ledger, dict):
        issues.extend(_mapping_issues(ledger, expected))
    else:
        issues.append("legacy occurrence mapping ledger must be an object")
    issues.extend(_provenance_issues(provenance, rejection_count))
    return issues


def _load_json(path: Path) -> tuple[object, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, ValueError) as exc:
        return {}, ["cannot read %s: %s" % (path.name, exc)]


def main() -> None:
    issues = []
    ledger, load_issues = _load_json(LEDGER_PATH)
    issues.extend(load_issues)
    provenance, load_issues = _load_json(PROVENANCE_PATH)
    issues.extend(load_issues)
    try:
        backlog_text = BACKLOG_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        backlog_text = ""
        issues.append("cannot read preserved backlog: %s" % exc)
    try:
        issues.extend(collect_issues(ledger, provenance, backlog_text))
    except Exception as exc:  # fail closed at the CLI boundary, never traceback
        issues.append("malformed provenance input: %s: %s" % (type(exc).__name__, exc))

    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] R7E candidate provenance and immutable occurrence mapping")
    print("TOTAL: %d failures" % len(issues))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
