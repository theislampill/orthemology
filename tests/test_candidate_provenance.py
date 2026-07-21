#!/usr/bin/env python3
"""Focused Task 3 tests for R7E candidate provenance and backlog supersession."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_candidate_provenance.py"
SCHEMA = ROOT / "schemas" / "orthing-candidate-ledger.schema.json"
LEDGER = ROOT / "docs" / "project-closure" / "r7e-sol" / "ORTHING-CANDIDATE-LEDGER.json"
PROVENANCE = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-INPUT-PROVENANCE.json"
AUDIT = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-PROVENANCE-AND-BACKLOG-AUDIT.md"
BACKLOG = ROOT / "docs" / "project-closure" / "r7e" / "ORTHING-CANDIDATE-BACKLOG.md"
R7E_STATE = ROOT / "docs" / "project-closure" / "r7e" / "AUTONOMOUS-R7E-STATE.json"

PRESERVED_SHA256 = {
    R7E_STATE: "359c7041a6c4045aa9b8e3af2c40164a282e27caa35cc2bfab715e8c3e66c9d7",
    BACKLOG: "ea0cfac0e55629441885f782d4b807d61de7890515ed73510e4b07a7524c285a",
}

PROVENANCE_BOUNDARIES = (
    {
        "boundary_id": "R7E-PROV-B001-IDENTITY-COLLAPSE",
        "status": "disallowed",
        "assertion": (
            "turn identity may equal orthing identity or session identity may equal "
            "episode identity"
        ),
    },
    {
        "boundary_id": "R7E-PROV-B002-EPISODE-INDEPENDENCE",
        "status": "disallowed",
        "assertion": "episode IDs prove independent observations",
    },
    {
        "boundary_id": "R7E-PROV-B003-RETROSPECTIVE-LIVE-CAPTURE",
        "status": "disallowed",
        "assertion": "retrospective reconstruction may be treated as live capture",
    },
    {
        "boundary_id": "R7E-PROV-B004-EVIDENCE-BACKDATING",
        "status": "disallowed",
        "assertion": (
            "current Sol evidence may be inserted into the original R7E t1 evidence state"
        ),
    },
    {
        "boundary_id": "R7E-PROV-B005-DEFECT-LOCUS-COLLAPSE",
        "status": "disallowed",
        "assertion": (
            "a single sound/unsound field may replace defect-locus accounting"
        ),
    },
    {
        "boundary_id": "R7E-PROV-B006-UNCONTROLLED-RECURRENCE",
        "status": "disallowed",
        "assertion": (
            "recurrence may be claimed without controlled fingerprint and distinct-source "
            "accounting"
        ),
    },
    {
        "boundary_id": "R7E-PROV-B007-INFERRED-REJECTION",
        "status": "disallowed",
        "assertion": "missing rejection records or rationale may be inferred",
    },
)


def source_rows(text: str) -> list[tuple[int, str]]:
    rows = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if not match or match.group(1).strip() == "id" or set(match.group(1).strip()) <= {"-", ":"}:
            continue
        rows.append((line_number, match.group(1).strip()))
    return rows


def rejection_bullets(text: str) -> list[str]:
    section = text.split("## Rejected by the adversarial pass", 1)[1].split(
        "## Survivors", 1
    )[0]
    return [line for line in section.splitlines() if re.match(r"^- \*\*.+\*\*", line)]


def load_module():
    spec = importlib.util.spec_from_file_location("candidate_provenance_probe", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not import production validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def production_exit(ledger: object, provenance: object, backlog_text: str | None = None):
    module = load_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        ledger_path = temp / "ledger.json"
        provenance_path = temp / "provenance.json"
        backlog_path = temp / "backlog.md"
        schema_path = temp / "schema.json"
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
        provenance_path.write_text(json.dumps(provenance, ensure_ascii=False), encoding="utf-8")
        backlog_path.write_text(
            backlog_text if backlog_text is not None else BACKLOG.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        schema_path.write_bytes(SCHEMA.read_bytes())
        module.LEDGER_PATH = ledger_path
        module.PROVENANCE_PATH = provenance_path
        module.BACKLOG_PATH = backlog_path
        module.SCHEMA_PATH = schema_path
        output = io.StringIO()
        exit_code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                module.main()
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
            except Exception as exc:  # a traceback is a validator contract failure
                exit_code = 99
                output.write("TRACEBACK: %s: %s" % (type(exc).__name__, exc))
        return exit_code, output.getvalue()


class CandidateProvenanceTests(unittest.TestCase):
    def setUp(self):
        required = [SCRIPT, SCHEMA, LEDGER, PROVENANCE, AUDIT]
        self.assertEqual([], [str(path) for path in required if not path.exists()])
        self.module = load_module()
        self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        self.backlog_text = BACKLOG.read_text(encoding="utf-8")

    def assertRejected(self, ledger=None, provenance=None, fragment=None):
        exit_code, output = production_exit(
            self.ledger if ledger is None else ledger,
            self.provenance if provenance is None else provenance,
        )
        self.assertEqual(1, exit_code, output)
        self.assertNotIn("TRACEBACK", output)
        if fragment:
            self.assertIn(fragment, output)

    def test_preserved_sources_expose_the_expected_incompleteness(self):
        rows = source_rows(self.backlog_text)
        legacy_ids = [legacy_id for _line, legacy_id in rows]
        duplicates = {legacy_id for legacy_id in legacy_ids if legacy_ids.count(legacy_id) > 1}
        self.assertEqual(221, len(rows))
        self.assertEqual(172, len(set(legacy_ids)))
        self.assertEqual(49, len(rows) - len(set(legacy_ids)))
        self.assertEqual(19, len(duplicates))
        self.assertEqual(8, len(rejection_bullets(self.backlog_text)))

    def test_preserved_r7e_sources_remain_byte_identical(self):
        for path, expected in PRESERVED_SHA256.items():
            with self.subTest(path=path.name):
                self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_schema_and_valid_documents_pass_the_production_entry_point(self):
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual([], list(Draft202012Validator(self.schema).iter_errors(self.ledger)))
        self.assertEqual(
            [], self.module.collect_issues(self.ledger, self.provenance, self.backlog_text)
        )
        exit_code, output = production_exit(self.ledger, self.provenance)
        self.assertEqual(0, exit_code, output)
        self.assertIn("TOTAL: 0 failures", output)

    def test_every_legacy_occurrence_has_one_stable_immutable_mapping(self):
        expected = source_rows(self.backlog_text)
        actual = self.ledger["rows"]
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(
            expected,
            [(row["legacy_line"], row["legacy_id"]) for row in actual],
        )
        self.assertEqual(
            [f"R7E-BACKLOG-L{line_number:04d}" for line_number, _legacy_id in expected],
            [row["immutable_id"] for row in actual],
        )

    def test_duplicate_missing_and_multiply_mapped_occurrences_are_rejected(self):
        duplicate_id = copy.deepcopy(self.ledger)
        duplicate_id["rows"][1]["immutable_id"] = duplicate_id["rows"][0]["immutable_id"]

        missing = copy.deepcopy(self.ledger)
        missing["rows"].pop()

        multiple = copy.deepcopy(self.ledger)
        extra = copy.deepcopy(multiple["rows"][0])
        extra["immutable_id"] = "R7E-BACKLOG-L9999"
        multiple["rows"].append(extra)

        for name, mutation in (("duplicate", duplicate_id), ("missing", missing), ("multiple", multiple)):
            with self.subTest(name=name):
                self.assertRejected(ledger=mutation, fragment="mapping")

    def test_count_drift_and_false_completeness_are_rejected(self):
        total_drift = copy.deepcopy(self.ledger)
        total_drift["summary"]["mapped_occurrence_count"] = 220
        self.assertRejected(ledger=total_drift, fragment="summary")

        complete = copy.deepcopy(self.provenance)
        complete["coverage"]["complete"] = True
        self.assertRejected(provenance=complete, fragment="completeness")

    def test_truncated_text_cannot_be_marked_complete(self):
        mutation = copy.deepcopy(self.ledger)
        mutation["rows"][0]["target"]["completeness"] = "complete"
        self.assertRejected(ledger=mutation, fragment="truncated")

    def test_missing_artifacts_cannot_be_marked_verified(self):
        mutation = copy.deepcopy(self.provenance)
        journal = next(row for row in mutation["artifacts"] if row["artifact_id"] == "workflow-journal")
        journal["evidence_state"] = "repository-verified"
        self.assertRejected(provenance=mutation, fragment="missing artifact")

    def test_attachment_observation_cannot_be_promoted_to_original_run_binding(self):
        mutation = copy.deepcopy(self.provenance)
        rebake = next(row for row in mutation["artifacts"] if row["artifact_id"] == "rebake-attachment")
        rebake["original_run_binding"] = "verified"
        self.assertRejected(provenance=mutation, fragment="attachment")

    def test_agent_sourcing_cannot_be_promoted_to_verified_scholarship(self):
        mutation = copy.deepcopy(self.ledger)
        mutation["rows"][0]["scholarship_status"] = "independently-verified"
        self.assertRejected(ledger=mutation, fragment="scholarship")

    def test_malformed_extensionless_reference_cannot_be_marked_verified(self):
        mutation = copy.deepcopy(self.ledger)
        mutation["rows"][0]["target"] = {
            "text": "applications/daee-epistemics/CURRENT-RUNTIME-BOUNDARY",
            "completeness": "truncated",
            "reference_state": "repository-verified",
        }
        self.assertRejected(ledger=mutation, fragment="extensionless")

    def test_implementing_run_statistics_cannot_be_marked_independently_verified(self):
        mutation = copy.deepcopy(self.provenance)
        mutation["reported_statistics"][0]["evidence_state"] = "independently-verified"
        self.assertRejected(provenance=mutation, fragment="statistic")

    def test_malformed_documents_fail_without_traceback(self):
        cases = [
            ([], self.provenance),
            (self.ledger, []),
            ({"rows": "bad"}, self.provenance),
            (self.ledger, {"artifacts": "bad"}),
        ]
        for ledger, provenance in cases:
            with self.subTest(ledger=type(ledger).__name__, provenance=type(provenance).__name__):
                exit_code, output = production_exit(ledger, provenance)
                self.assertEqual(1, exit_code, output)
                self.assertNotIn("TRACEBACK", output)
                self.assertIn("TOTAL:", output)

    def test_audit_states_the_non_claims_and_exact_repository_counts(self):
        text = AUDIT.read_text(encoding="utf-8")
        for phrase in (
            "221 legacy rows",
            "172 unique legacy IDs",
            "49 reused occurrences",
            "19 duplicate legacy IDs",
            "eight rejection records",
            "implementing-run-attributed",
            "attachment-observed",
            "unresolved",
            "not source verification",
            "not merge readiness",
        ):
            self.assertIn(phrase, text)

    def test_all_seven_provenance_boundary_reversals_are_rejected(self):
        for boundary in PROVENANCE_BOUNDARIES:
            mutation = copy.deepcopy(self.provenance)
            mutation["provenance_boundaries"] = copy.deepcopy(PROVENANCE_BOUNDARIES)
            row = next(
                item
                for item in mutation["provenance_boundaries"]
                if item["boundary_id"] == boundary["boundary_id"]
            )
            row["status"] = "allowed"
            with self.subTest(boundary_id=boundary["boundary_id"]):
                self.assertRejected(
                    provenance=mutation,
                    fragment=boundary["boundary_id"],
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
