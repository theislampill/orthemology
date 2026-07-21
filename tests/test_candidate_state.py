#!/usr/bin/env python3
"""Focused contract tests for the generated R7 candidate topology."""
import copy
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_candidate_state import build_overlay, collect_issues  # noqa: E402
import scripts.generate_candidate_state as candidate_generator  # noqa: E402


INPUT = ROOT / "docs" / "project-closure" / "r7e-sol" / "CANDIDATE-TOPOLOGY-INPUT.yaml"
OUTPUT = ROOT / "docs" / "current-candidate-state.yaml"
TOPOLOGY_SCHEMA = ROOT / "schemas" / "candidate-topology.schema.json"
OVERLAY_SCHEMA = ROOT / "schemas" / "candidate-overlay.schema.json"
DECISIONS = ROOT / "docs" / "decision-status.yaml"
SCRIPTS = ROOT / "scripts"


def generator_exit(data):
    """Run the real generator main against a disposable frozen input."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / "input.yaml"
        output_path = Path(temp_dir) / "output.yaml"
        input_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        old_input = candidate_generator.INPUT_PATH
        old_output = candidate_generator.OUTPUT_PATH
        old_argv = sys.argv
        candidate_generator.INPUT_PATH = str(input_path)
        candidate_generator.OUTPUT_PATH = str(output_path)
        sys.argv = ["generate_candidate_state.py"]
        stream = io.StringIO()
        try:
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                try:
                    exit_code = candidate_generator.main()
                except Exception as exc:  # test boundary: a traceback is a contract failure
                    exit_code = 99
                    stream.write("TRACEBACK: %s: %s" % (type(exc).__name__, exc))
        finally:
            candidate_generator.INPUT_PATH = old_input
            candidate_generator.OUTPUT_PATH = old_output
            sys.argv = old_argv
        return exit_code, stream.getvalue(), output_path.exists()


def production_validator_exit(data, overlay=None):
    """Run the real production validator with only input/output reads replaced."""
    scripts_path = str(SCRIPTS)
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    spec = importlib.util.spec_from_file_location(
        "candidate_state_production_probe",
        SCRIPTS / "validate_candidate_state.py",
    )
    if spec is None or spec.loader is None:
        return 2, "could not import production validator"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if overlay is None:
        try:
            overlay = build_overlay(data)
        except Exception:
            overlay = yaml.safe_load(OUTPUT.read_text(encoding="utf-8"))
    overrides = {
        "docs/project-closure/r7e-sol/CANDIDATE-TOPOLOGY-INPUT.yaml": yaml.safe_dump(
            data, sort_keys=False
        ),
        "docs/current-candidate-state.yaml": yaml.safe_dump(overlay, sort_keys=False),
    }
    real_read = module.read
    module.read = lambda rel: overrides.get(rel, real_read(rel))
    module.FAILS.clear()
    stream = io.StringIO()
    try:
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            try:
                exit_code = module.main()
            except Exception as exc:  # test boundary: a traceback is a contract failure
                exit_code = 99
                stream.write("TRACEBACK: %s: %s" % (type(exc).__name__, exc))
    finally:
        module.read = real_read
    return exit_code, stream.getvalue()


class CandidateStateTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load(INPUT.read_text(encoding="utf-8"))
        self.decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))["decisions"]

    def issues(self, data=None, decisions=None):
        return collect_issues(data or self.data, decisions or self.decisions)

    def assertIssue(self, issues, fragment):
        self.assertTrue(
            any(fragment in issue for issue in issues),
            f"expected issue containing {fragment!r}, got {issues!r}",
        )

    def authority_mutations(self):
        cases = []

        omitted_document = copy.deepcopy(self.data)
        omitted_document["candidate_documents"]["closure"].pop()
        cases.append(("omitted document", omitted_document, "candidate document inventory"))

        extra_document = copy.deepcopy(self.data)
        extra_document["candidate_documents"]["closure"].append("README.md")
        cases.append(("extra document", extra_document, "candidate document inventory"))

        nonexistent_document = copy.deepcopy(self.data)
        nonexistent_document["candidate_documents"]["closure"][-1] = (
            "docs/" + "does-not-exist.md"
        )
        cases.append(("nonexistent document", nonexistent_document, "does not resolve"))

        omitted_pdf = copy.deepcopy(self.data)
        omitted_pdf["candidate_pdfs"].pop()
        cases.append(("omitted PDF", omitted_pdf, "candidate PDF inventory"))

        extra_pdf = copy.deepcopy(self.data)
        extra_pdf["candidate_pdfs"].append("artifacts/orthemic-core-reference-draft.pdf")
        cases.append(("extra PDF", extra_pdf, "candidate PDF inventory"))

        nonexistent_pdf = copy.deepcopy(self.data)
        nonexistent_pdf["candidate_pdfs"][-1] = "artifacts/does-not-exist.pdf"
        cases.append(("nonexistent PDF", nonexistent_pdf, "does not resolve"))

        revision = copy.deepcopy(self.data)
        revision["pull_requests"][-1]["revision"] = "R7F"
        cases.append(("revision drift", revision, "revision drift"))

        provenance_layer = copy.deepcopy(self.data)
        provenance_layer["pull_requests"][-1]["provenance"]["layer"] = "fabricated-layer"
        cases.append(("provenance layer drift", provenance_layer, "provenance layer drift"))

        provenance_model = copy.deepcopy(self.data)
        provenance_model["pull_requests"][-1]["provenance"]["model"] = "Unknown"
        cases.append(("provenance model drift", provenance_model, "provenance model drift"))

        observation_source = copy.deepcopy(self.data)
        observation_source["observation_source"] = "fabricated"
        cases.append(("observation-source drift", observation_source, "observation_source drift"))

        return cases

    def test_frozen_input_and_generated_overlay_validate_against_schemas(self):
        topology_schema = json.loads(TOPOLOGY_SCHEMA.read_text(encoding="utf-8"))
        overlay_schema = json.loads(OVERLAY_SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(topology_schema)
        Draft202012Validator.check_schema(overlay_schema)
        self.assertEqual([], list(Draft202012Validator(topology_schema).iter_errors(self.data)))
        overlay = build_overlay(self.data)
        self.assertEqual([], list(Draft202012Validator(overlay_schema).iter_errors(overlay)))

    def test_build_overlay_is_deterministic_complete_and_non_self_referential(self):
        first = build_overlay(copy.deepcopy(self.data))
        second = build_overlay(copy.deepcopy(self.data))
        self.assertEqual(first, second)
        self.assertEqual([8, 9, 10, 11, 12], [row["pr"] for row in first["pr_chain"]])
        self.assertEqual([12, 11, 10, 9, 8], first["merge_order"])
        self.assertEqual(
            "cbab14747835855d232448f648eefa1d4e36074e",
            first["pr_chain"][-1]["head_at_observation"],
        )
        self.assertNotIn("head", first["pr_chain"][-1])
        self.assertFalse(first["timeless_state"])

    def test_tracked_overlay_exactly_matches_generated_model(self):
        self.assertEqual(
            build_overlay(self.data),
            yaml.safe_load(OUTPUT.read_text(encoding="utf-8")),
        )

    def test_valid_topology_has_no_issues(self):
        self.assertEqual([], self.issues())

    def test_review_provenance_is_distinct_from_implementation_provenance(self):
        self.assertEqual(
            {
                "layer": "independent-review",
                "model": "gpt-5.6-sol",
                "statement": (
                    "Controller-confirmed Sol review provenance; separate from the "
                    "historical candidate implementation provenance."
                ),
            },
            self.data.get("review_provenance"),
        )
        overlay = build_overlay(self.data)
        self.assertEqual(self.data["review_provenance"], overlay.get("review_provenance"))
        self.assertNotEqual(
            overlay["pr_chain"][-1]["provenance"],
            overlay["review_provenance"],
        )

    def test_semantics_reject_complete_authority_mutations(self):
        for name, mutated, fragment in self.authority_mutations():
            with self.subTest(name=name):
                self.assertIssue(self.issues(mutated), fragment)

    def test_generator_rejects_complete_authority_mutations(self):
        for name, mutated, _ in self.authority_mutations():
            with self.subTest(name=name):
                exit_code, output, output_exists = generator_exit(mutated)
                self.assertEqual(1, exit_code, output)
                self.assertNotIn("TRACEBACK", output)
                self.assertFalse(output_exists, output)

    def test_production_validator_rejects_complete_authority_mutations(self):
        for name, mutated, _ in self.authority_mutations():
            with self.subTest(name=name):
                exit_code, output = production_validator_exit(mutated)
                self.assertEqual(1, exit_code, output)
                self.assertNotIn("TRACEBACK", output)

        key_drift_overlay = build_overlay(self.data)
        key_drift_overlay["provenance_layers"]["r7f"] = key_drift_overlay[
            "provenance_layers"
        ].pop("r7e")
        exit_code, output = production_validator_exit(self.data, key_drift_overlay)
        self.assertEqual(1, exit_code, output)
        self.assertNotIn("TRACEBACK", output)

    def test_generator_and_validator_report_malformed_shapes_without_traceback(self):
        cases = []

        nested_decision = copy.deepcopy(self.data)
        nested_decision["pull_requests"][-1]["candidate_decisions"] = [["0034"]]
        cases.append(("nested-list decision ID", nested_decision))

        nonmapping_claims = copy.deepcopy(self.data)
        nonmapping_claims["status_claims"] = []
        cases.append(("non-mapping status_claims", nonmapping_claims))

        nonmapping_evidence = copy.deepcopy(self.data)
        nonmapping_evidence["status_claims"]["evidence"] = "fabricated"
        cases.append(("non-mapping evidence", nonmapping_evidence))

        for name, mutated in cases:
            with self.subTest(component="generator", name=name):
                exit_code, output, output_exists = generator_exit(mutated)
                self.assertEqual(1, exit_code, output)
                self.assertIn("schema:", output)
                self.assertIn("TOTAL:", output)
                self.assertNotIn("TRACEBACK", output)
                self.assertFalse(output_exists, output)
            with self.subTest(component="production validator", name=name):
                exit_code, output = production_validator_exit(mutated)
                self.assertEqual(1, exit_code, output)
                self.assertIn("schema", output)
                self.assertIn("TOTAL:", output)
                self.assertNotIn("TRACEBACK", output)

    def test_omitted_pr_11_or_12_is_rejected(self):
        for omitted in (11, 12):
            with self.subTest(omitted=omitted):
                mutated = copy.deepcopy(self.data)
                mutated["pull_requests"] = [
                    row for row in mutated["pull_requests"] if row["pr"] != omitted
                ]
                self.assertIssue(self.issues(mutated), f"missing PR #{omitted}")

    def test_duplicate_or_noninteger_pr_is_rejected(self):
        duplicate = copy.deepcopy(self.data)
        duplicate["pull_requests"][-1]["pr"] = 11
        self.assertIssue(self.issues(duplicate), "duplicate PR #11")

        noninteger = copy.deepcopy(self.data)
        noninteger["pull_requests"][-1]["pr"] = "12"
        self.assertIssue(self.issues(noninteger), "PR number must be an integer")

    def test_placeholder_or_non_40_hex_head_is_rejected(self):
        for bad in ("set at delivery (child PR head)", "abc123"):
            with self.subTest(head=bad):
                mutated = copy.deepcopy(self.data)
                mutated["pull_requests"][-1]["head_at_observation"] = bad
                self.assertIssue(self.issues(mutated), "40-lowercase-hex")

    def test_broken_parent_link_is_rejected(self):
        mutated = copy.deepcopy(self.data)
        mutated["pull_requests"][3]["base_branch"] = "candidate/wrong-parent"
        self.assertIssue(self.issues(mutated), "PR #11 base_branch does not match PR #10")

        mutated = copy.deepcopy(self.data)
        mutated["pull_requests"][3]["base_head_at_observation"] = "0" * 40
        self.assertIssue(self.issues(mutated), "PR #11 base head does not match PR #10")

    def test_wrong_merge_order_is_rejected(self):
        mutated = copy.deepcopy(self.data)
        mutated["merge_order"] = [8, 9, 10, 11, 12]
        self.assertIssue(self.issues(mutated), "merge_order must be [12, 11, 10, 9, 8]")

    def test_stale_frozen_observation_is_rejected(self):
        mutated = copy.deepcopy(self.data)
        mutated["observed_at_utc"] = "2026-07-21T18:10:21Z"
        self.assertIssue(self.issues(mutated), "frozen observation is stale")

    def test_missing_provenance_layer_is_rejected(self):
        mutated = copy.deepcopy(self.data)
        del mutated["pull_requests"][-1]["provenance"]["layer"]
        self.assertIssue(self.issues(mutated), "PR #12 provenance layer is missing")

    def test_decision_allocation_drift_is_rejected(self):
        mutated = copy.deepcopy(self.data)
        mutated["pull_requests"][-1]["candidate_decisions"] = []
        self.assertIssue(self.issues(mutated), "decision allocation drift")

    def test_candidate_decision_self_promotion_is_rejected(self):
        decisions = copy.deepcopy(self.decisions)
        decisions["0034"]["status"] = "adopted-merged"
        self.assertIssue(self.issues(decisions=decisions), "candidate self-promotion")

    def test_evidence_free_terminal_claims_are_rejected(self):
        for claim in ("merged", "independent_signoff", "ready_for_merge"):
            with self.subTest(claim=claim):
                mutated = copy.deepcopy(self.data)
                mutated["status_claims"][claim] = True
                mutated["status_claims"]["evidence"][claim] = []
                issues = self.issues(mutated)
                self.assertIssue(issues, f"{claim} claim lacks evidence")
                self.assertIssue(issues, "candidate topology cannot self-promote")


if __name__ == "__main__":
    unittest.main(verbosity=2)
