#!/usr/bin/env python3
"""Retained regressions from the bounded fifth-steer independent review."""
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


def relation(records, relation_id):
    return item(
        records["inter_somnic_relations"],
        "inter_somnic_relation_id",
        relation_id,
    )


class FifthSteerReviewRegressions(unittest.TestCase):
    """The eight reproduced false passes plus the review's valid controls."""

    def setUp(self):
        self.activation = yaml.safe_load(ACTIVATION.read_text(encoding="utf-8"))
        self.records = yaml.safe_load(RECORDS.read_text(encoding="utf-8"))
        self.inventory = yaml.safe_load(INVENTORY.read_text(encoding="utf-8"))
        self.adoption = yaml.safe_load(ADOPTION.read_text(encoding="utf-8"))
        self.collective = yaml.safe_load(COLLECTIVE.read_text(encoding="utf-8"))

    def assertRejected(self, mutate, fragment):
        records = copy.deepcopy(self.records)
        mutate(records)
        code, output = production_exit(
            self.activation,
            records,
            self.inventory,
            self.adoption,
            self.collective,
        )
        self.assertEqual(1, code, output)
        self.assertNotIn("TRACEBACK", output)
        self.assertIn(fragment, output)

    def assertAccepted(self, mutate=lambda records: None):
        records = copy.deepcopy(self.records)
        mutate(records)
        code, output = production_exit(
            self.activation,
            records,
            self.inventory,
            self.adoption,
            self.collective,
        )
        self.assertEqual(0, code, output)
        self.assertNotIn("TRACEBACK", output)

    def test_i06_non_reopening_relation_cannot_declare_reopen(self):
        self.assertRejected(
            lambda records: relation(
                records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001"
            ).__setitem__("reopens_source", True),
            "only a reopening relation can reopen its source",
        )

    def test_i07_reassessment_source_must_be_target_predecessor(self):
        def mutate(records):
            edge = relation(records, "ISR-REASSESSES-001")
            edge["source_assessment_ids"] = ["SA-RECURRENCE-001"]
            source = item(records["somnic_assessments"], "assessment_id", "SA-CLOSED-001")
            source["inter_somnic_relation_ids"].remove("ISR-REASSESSES-001")
            replacement = item(
                records["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001"
            )
            replacement["inter_somnic_relation_ids"] = [
                *replacement["inter_somnic_relation_ids"],
                "ISR-REASSESSES-001",
            ]

        self.assertRejected(mutate, "reassessment must match target assessment lineage and depth")

    def test_i08_reassessment_depth_must_match_target_depth(self):
        self.assertRejected(
            lambda records: relation(records, "ISR-REASSESSES-001").__setitem__(
                "assessment_depth", 99
            ),
            "reassessment must match target assessment lineage and depth",
        )

    def test_i15_transclusion_preserves_recorded_redactions(self):
        self.assertRejected(
            lambda records: relation(
                records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001"
            )["provenance"].__setitem__("redactions", []),
            "transclusion must preserve its recorded redactions",
        )

    def test_i16_transclusion_meta_assessment_is_receiving_case_bound(self):
        self.assertRejected(
            lambda records: relation(
                records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001"
            )["provenance"].__setitem__(
                "local_meta_orthability_assessment_id", "MOA-CLOSED-001"
            ),
            "local meta-orthability assessment must be bound to the receiving case",
        )

    def test_i18_received_t2_evidence_resolves_with_t2_timing(self):
        self.assertRejected(
            lambda records: relation(
                records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001"
            ).__setitem__("received_at_t2_evidence_ids", ["E-GHOST-T2"]),
            "relation evidence IDs must resolve through their exact timing owners",
        )

    def test_i19_source_t1_evidence_resolves_with_t1_timing(self):
        self.assertRejected(
            lambda records: relation(
                records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001"
            ).__setitem__("source_t1_evidence_ids", ["E-GHOST-T1"]),
            "relation evidence IDs must resolve through their exact timing owners",
        )

    def test_i20_receipt_bearing_relation_cannot_claim_independent_discovery(self):
        def mutate(records):
            edge = relation(records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001")
            edge["information_path"] = "none-independent-discovery"
            edge["independence_claim"] = True
            edge["idempotency_key"] = edge["idempotency_key"].replace(
                "direct-transclusion", "none-independent-discovery"
            )

        self.assertRejected(mutate, "receipt-bearing relation cannot claim independent discovery")

    def test_neighboring_valid_controls_remain_accepted(self):
        def add_noop_run(records):
            new = copy.deepcopy(
                item(records["somnus_runs"], "somnus_run_id", "RUN-NEXT-001")
            )
            new.update({
                "somnus_run_id": "RUN-NOOP-001",
                "idempotency_key": "recurrence-0.1.0:ORTH-NEW-002:LEDGER-REV-002:noop",
                "historical_comparator_ids": [],
                "used_comparator_ids": [],
                "output_ids": [],
                "somnic_episode_ids": [],
            })
            records["somnus_runs"].append(new)

        def reverse_relations(records):
            records["inter_somnic_relations"] = list(
                reversed(records["inter_somnic_relations"])
            )

        def reverse_nonclaims(records):
            edge = relation(records, "ISR-CROSS-RUN-COMPARE-001")
            edge["non_claims"] = list(reversed(edge["non_claims"]))

        # C01 and C08-C09 are mutation controls.
        self.assertAccepted(add_noop_run)
        self.assertAccepted(reverse_relations)
        self.assertAccepted(reverse_nonclaims)

        # C02-C07 and C10 are independent assertions over the accepted
        # canonical fixture, followed by a production-entry acceptance check.
        run = item(self.records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        self.assertGreater(len(run["somnic_episode_ids"]), 1)  # C02
        local = item(self.records["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")
        self.assertEqual([], local["inter_somnic_relation_ids"])  # C03
        comparison = relation(self.records, "ISR-CROSS-RUN-COMPARE-001")
        self.assertFalse(comparison["reopens_source"])  # C04
        self.assertTrue(comparison["source_episode_state_preserved"])
        reopening = relation(self.records, "ISR-REOPENS-001")
        self.assertTrue(reopening["material_delta_id"])  # C05
        self.assertTrue(reopening["source_assessment_ids"])
        collective = item(
            self.records["somnic_episodes"],
            "somnic_episode_id",
            "SEP-COLLECTIVE-001",
        )
        self.assertEqual(2, len(collective["collective_context"]["source_episode_ids"]))  # C06
        transclusion = relation(
            self.records, "ISR-CROSS-OPERATOR-TRANSCLUSION-001"
        )["provenance"]
        self.assertTrue(transclusion["receipt_time"])  # C07
        self.assertTrue(transclusion["local_meta_orthability_assessment_id"])
        episode = item(
            self.records["somnic_episodes"],
            "somnic_episode_id",
            "SEP-RECURRENCE-001",
        )
        self.assertTrue(all(  # C10
            activity["somnic_episode_id"] == "SEP-RECURRENCE-001"
            for activity in episode["activity_events"]
        ))
        self.assertAccepted()


if __name__ == "__main__":
    unittest.main()
