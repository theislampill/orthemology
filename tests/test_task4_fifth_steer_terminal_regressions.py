#!/usr/bin/env python3
"""Terminal regressions for the bounded Task 4.x fifth-steer repair union.

Every acceptance or rejection probe routes through the production Task 4
validator entry point and the canonical fixture bundle.
"""
from __future__ import annotations

import copy
import unittest

import yaml

from tests.test_somnic_orthing import (
    ACTIVATION,
    ADOPTION,
    COLLECTIVE,
    INVENTORY,
    RECORDS,
    item,
    production_exit,
)


def relation(records, relation_id="ISR-CROSS-OPERATOR-TRANSCLUSION-001"):
    return item(
        records["inter_somnic_relations"],
        "inter_somnic_relation_id",
        relation_id,
    )


def subject(records, subject_id="TRANSCLUSION-PACKET-001"):
    return item(records["subject_records"], "subject_id", subject_id)


class FifthSteerTerminalRegressions(unittest.TestCase):
    def setUp(self):
        self.activation = yaml.safe_load(ACTIVATION.read_text(encoding="utf-8"))
        self.records = yaml.safe_load(RECORDS.read_text(encoding="utf-8"))
        self.inventory = yaml.safe_load(INVENTORY.read_text(encoding="utf-8"))
        self.adoption = yaml.safe_load(ADOPTION.read_text(encoding="utf-8"))
        self.collective = yaml.safe_load(COLLECTIVE.read_text(encoding="utf-8"))

    def production(self, records):
        return production_exit(
            self.activation,
            records,
            self.inventory,
            self.adoption,
            self.collective,
        )

    def assertAccepted(self, mutate=lambda records: None):
        records = copy.deepcopy(self.records)
        mutate(records)
        code, output = self.production(records)
        self.assertEqual(0, code, output)
        self.assertNotIn("TRACEBACK", output)

    def assertRejected(self, mutate, fragment=None):
        records = copy.deepcopy(self.records)
        mutate(records)
        code, output = self.production(records)
        self.assertEqual(1, code, output)
        self.assertNotIn("TRACEBACK", output)
        if fragment is not None:
            self.assertIn(fragment, output)

    def test_exact_empty_redaction_preservation_is_accepted(self):
        def mutate(records):
            subject(records)["recorded_redactions"] = []
            relation(records)["provenance"]["redactions"] = []

        self.assertAccepted(mutate)

    def test_reordered_redactions_are_rejected_as_ordered_data(self):
        def mutate(records):
            subject(records)["recorded_redactions"] = [
                "private-session-identifiers",
                "contract-text",
            ]
            relation(records)["provenance"]["redactions"] = [
                "contract-text",
                "private-session-identifiers",
            ]

        self.assertRejected(
            mutate,
            "transclusion must preserve its recorded redactions in order",
        )

    def test_exact_ordered_nonempty_redaction_preservation_is_accepted(self):
        def mutate(records):
            exact = ["private-session-identifiers", "contract-text"]
            subject(records)["recorded_redactions"] = exact
            relation(records)["provenance"]["redactions"] = list(exact)

        self.assertAccepted(mutate)

    def test_transcluded_artifact_identity_participates_in_global_collisions(self):
        def mutate(records):
            collision_id = "ISR-SAME-RUN-COMPARE-001"
            packet = subject(records)
            packet["subject_id"] = collision_id
            relation(records)["provenance"]["received_artifact_ref"] = collision_id
            gate = item(
                records["meta_orthability_assessments"],
                "meta_orthability_assessment_id",
                "MOA-TRANSCLUSION-001",
            )
            gate["subject_ids"] = [collision_id]

        self.assertRejected(mutate, "global typed record ID")

    def test_unique_transcluded_artifact_identity_remains_accepted(self):
        def mutate(records):
            unique_id = "TRANSCLUSION-PACKET-TERMINAL-CONTROL-001"
            packet = subject(records)
            packet["subject_id"] = unique_id
            relation(records)["provenance"]["received_artifact_ref"] = unique_id
            gate = item(
                records["meta_orthability_assessments"],
                "meta_orthability_assessment_id",
                "MOA-TRANSCLUSION-001",
            )
            gate["subject_ids"] = [unique_id]

        self.assertAccepted(mutate)

    def test_canonical_transclusion_resolves_source_assessment_and_status_owner(self):
        edge = relation(self.records)
        source_ids = edge["source_assessment_ids"]
        self.assertTrue(source_ids, "canonical transclusion lacks a source assessment")
        self.assertEqual(1, len(source_ids))
        source_assessment = item(
            self.records["somnic_assessments"],
            "assessment_id",
            source_ids[0],
        )
        self.assertEqual(edge["source_episode_id"], source_assessment["somnic_episode_id"])
        self.assertEqual(
            edge["provenance"]["source_status_result"],
            source_assessment["source_status_result"],
        )
        self.assertAccepted()

    def test_target_only_source_status_rewrites_are_rejected(self):
        for replacement in ("verified", "unverified", "not-applicable"):
            with self.subTest(replacement=replacement):
                self.assertRejected(
                    lambda records, value=replacement: relation(records)[
                        "provenance"
                    ].__setitem__("source_status_result", value),
                    "source status must equal its authoritative source assessment owner",
                )

    def test_unchanged_source_status_and_recipient_local_disposition_are_independent(self):
        source_status = relation(self.records)["provenance"]["source_status_result"]

        def mutate(records):
            relation(records)["provenance"]["local_disposition"] = "held"

        self.assertAccepted(mutate)
        self.assertEqual(
            source_status,
            relation(self.records)["provenance"]["source_status_result"],
        )

    def test_malformed_nested_terminal_shapes_reject_without_traceback(self):
        mutations = {
            "source-redactions-container": lambda records: relation(records)[
                "provenance"
            ].__setitem__("redactions", {"nested": []}),
            "source-redactions-member": lambda records: relation(records)[
                "provenance"
            ].__setitem__("redactions", [["private-session-identifiers"]]),
            "artifact-redactions-member": lambda records: subject(records).__setitem__(
                "recorded_redactions", [{"nested": "private-session-identifiers"}]
            ),
            "source-assessment-member": lambda records: relation(records).__setitem__(
                "source_assessment_ids", [{"nested": "SA-REMOTE-SOURCE-001"}]
            ),
            "source-status": lambda records: relation(records)["provenance"].__setitem__(
                "source_status_result", {"nested": "qualified"}
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                self.assertRejected(mutate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
