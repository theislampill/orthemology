#!/usr/bin/env python3
"""Focused contract tests for the generated R7 candidate topology."""
import copy
import json
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_candidate_state import build_overlay, collect_issues  # noqa: E402


INPUT = ROOT / "docs" / "project-closure" / "r7e-sol" / "CANDIDATE-TOPOLOGY-INPUT.yaml"
OUTPUT = ROOT / "docs" / "current-candidate-state.yaml"
TOPOLOGY_SCHEMA = ROOT / "schemas" / "candidate-topology.schema.json"
OVERLAY_SCHEMA = ROOT / "schemas" / "candidate-overlay.schema.json"
DECISIONS = ROOT / "docs" / "decision-status.yaml"


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
