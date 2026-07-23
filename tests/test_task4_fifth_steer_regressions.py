#!/usr/bin/env python3
"""Task 4.x fifth-steer intra/inter-somnic regression contract.

These tests deliberately use the production Task 4 validator entry point and
the canonical fixture bundle.  They are not a second semantic harness.
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


def relation(rows, relation_id):
    return item(rows, "inter_somnic_relation_id", relation_id)


class FifthSteerRegressions(unittest.TestCase):
    """The 26 implications in the fifth additive steer, section 18."""

    def setUp(self):
        self.activation = yaml.safe_load(ACTIVATION.read_text(encoding="utf-8"))
        self.records = yaml.safe_load(RECORDS.read_text(encoding="utf-8"))
        self.inventory = yaml.safe_load(INVENTORY.read_text(encoding="utf-8"))
        self.adoption = yaml.safe_load(ADOPTION.read_text(encoding="utf-8"))
        self.collective = yaml.safe_load(COLLECTIVE.read_text(encoding="utf-8"))
        self.episodes = self.records.get("somnic_episodes", [])
        self.relations = self.records.get("inter_somnic_relations", [])

    def assertRecordsRejected(self, records, fragment):
        code, output = production_exit(
            self.activation, records, self.inventory, self.adoption,
            self.collective,
        )
        self.assertEqual(1, code, output)
        self.assertNotIn("TRACEBACK", output)
        self.assertIn(fragment, output)

    def test_01_one_run_may_contain_two_distinct_episodes(self):
        run = item(self.records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        self.assertGreaterEqual(len(run["somnic_episode_ids"]), 2)
        self.assertEqual(len(run["somnic_episode_ids"]), len(set(run["somnic_episode_ids"])))

    def test_02_run_id_cannot_substitute_for_episode_identity(self):
        mutation = copy.deepcopy(self.records)
        assessment = item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")
        assessment["somnic_episode_id"] = assessment["somnus_run_id"]
        self.assertRecordsRejected(mutation, "episode identity must remain distinct from run identity")

    def test_03_several_events_in_one_episode_are_intra_somnic(self):
        episode = item(self.episodes, "somnic_episode_id", "SEP-RECURRENCE-001")
        self.assertGreaterEqual(len(episode["activity_events"]), 2)
        self.assertTrue(all(
            event["somnic_episode_id"] == episode["somnic_episode_id"]
            and event["activity_scope"] == "intra-somnic"
            for event in episode["activity_events"]
        ))

    def test_04_two_episodes_in_one_run_are_inter_somnic(self):
        edge = relation(self.relations, "ISR-SAME-RUN-COMPARE-001")
        self.assertEqual("same-run", edge["run_relation"])
        self.assertNotEqual(edge["source_episode_id"], edge["target_episode_id"])

    def test_05_same_operator_cross_run_comparison_is_inter_somnic(self):
        edge = relation(self.relations, "ISR-CROSS-RUN-COMPARE-001")
        self.assertEqual("cross-run", edge["run_relation"])
        self.assertEqual("same-operator", edge["operator_relation"])
        self.assertEqual("compares-with", edge["semantic_relation"])

    def test_06_cross_operator_transclusion_preserves_receipt_and_local_assessment(self):
        edge = relation(self.relations, "ISR-CROSS-OPERATOR-TRANSCLUSION-001")
        provenance = edge["provenance"]
        self.assertEqual("cross-operator", edge["operator_relation"])
        self.assertEqual("direct-transclusion", edge["information_path"])
        for key in (
            "source_operator_id", "source_ledger_id", "received_artifact_ref",
            "receipt_time", "redactions", "source_status_result",
            "local_meta_orthability_assessment_id", "local_disposition",
        ):
            self.assertIn(key, provenance)
        mutation = copy.deepcopy(self.records)
        relation(
            mutation["inter_somnic_relations"],
            "ISR-CROSS-OPERATOR-TRANSCLUSION-001",
        )["provenance"]["local_meta_orthability_assessment_id"] = "MOA-GHOST"
        self.assertRecordsRejected(
            mutation,
            "direct transclusion requires receipt provenance and local assessment",
        )

    def test_07_self_inter_somnic_relation_is_rejected(self):
        mutation = copy.deepcopy(self.records)
        edge = relation(mutation["inter_somnic_relations"], "ISR-SAME-RUN-COMPARE-001")
        edge["target_episode_id"] = edge["source_episode_id"]
        self.assertRecordsRejected(mutation, "distinct source and target episodes")

    def test_08_comparison_preserves_closed_source_without_reopening(self):
        edge = relation(self.relations, "ISR-CROSS-RUN-COMPARE-001")
        source = item(self.episodes, "somnic_episode_id", edge["source_episode_id"])
        self.assertEqual("closed", source["disposition"])
        self.assertFalse(edge["reopens_source"])
        self.assertTrue(edge["source_episode_state_preserved"])

    def test_09_comparator_cannot_silently_reopen_source(self):
        mutation = copy.deepcopy(self.records)
        relation(mutation["inter_somnic_relations"], "ISR-CROSS-RUN-COMPARE-001")["reopens_source"] = True
        self.assertRecordsRejected(mutation, "comparison cannot reopen its source")

    def test_10_reopening_requires_new_episode_and_material_delta(self):
        edge = relation(self.relations, "ISR-REOPENS-001")
        self.assertEqual("reopens", edge["semantic_relation"])
        self.assertNotEqual(edge["source_episode_id"], edge["target_episode_id"])
        self.assertIsInstance(edge["material_delta_id"], str)
        self.assertTrue(edge["material_delta_id"])

    def test_11_reopening_cannot_mutate_source_episode_or_assessment(self):
        mutation = copy.deepcopy(self.records)
        edge = relation(mutation["inter_somnic_relations"], "ISR-REOPENS-001")
        edge["source_assessment_state_preserved"] = False
        self.assertRecordsRejected(mutation, "must preserve source episode and assessment state")

    def test_12_reassessment_has_lineage_depth_without_auto_requeue(self):
        edge = relation(self.relations, "ISR-REASSESSES-001")
        self.assertEqual("reassesses", edge["semantic_relation"])
        self.assertTrue(edge["source_assessment_ids"])
        self.assertGreaterEqual(edge["assessment_depth"], 1)
        self.assertFalse(edge["auto_requeue"])

    def test_13_closed_assessment_stays_out_of_frontier_without_trigger(self):
        assessment = item(self.records["somnic_assessments"], "assessment_id", "SA-CLOSED-001")
        self.assertEqual("closed", assessment["closure_status"])
        self.assertFalse(assessment["auto_requeue"])
        self.assertEqual([], assessment["frontier_trigger_ids"])

    def test_14_completed_run_preserves_closed_and_partial_children(self):
        run = item(self.records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        dispositions = {
            item(self.episodes, "somnic_episode_id", episode_id)["disposition"]
            for episode_id in run["somnic_episode_ids"]
        }
        self.assertEqual("completed", run["run_disposition"])
        self.assertTrue({"closed", "partial"}.issubset(dispositions))

    def test_15_run_completion_cannot_auto_complete_children(self):
        mutation = copy.deepcopy(self.records)
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["children_auto_completed"] = True
        self.assertRecordsRejected(mutation, "run completion cannot auto-complete child episodes")

    def test_16_collective_episode_has_intra_synthesis_and_inter_source_edges(self):
        episode = item(self.episodes, "somnic_episode_id", "SEP-COLLECTIVE-001")
        self.assertTrue(episode["collective_context"]["source_episode_ids"])
        self.assertTrue(all(
            event["activity_scope"] == "intra-somnic"
            for event in episode["activity_events"]
        ))
        source_edges = [
            edge for edge in self.relations
            if edge["target_episode_id"] == episode["somnic_episode_id"]
            and edge["semantic_relation"] == "collective-synthesizes"
        ]
        self.assertGreaterEqual(len(source_edges), 2)

    def test_17_collective_synthesis_preserves_dissent_and_source_closure(self):
        episode = item(self.episodes, "somnic_episode_id", "SEP-COLLECTIVE-001")
        self.assertTrue(episode["collective_context"]["dissent_preserved"])
        for source_id in episode["collective_context"]["source_episode_ids"]:
            self.assertEqual("closed", item(self.episodes, "somnic_episode_id", source_id)["disposition"])

    def test_18_independent_convergence_has_no_communication_path(self):
        edge = relation(self.relations, "ISR-INDEPENDENT-CORROBORATION-001")
        self.assertEqual("none-independent-discovery", edge["information_path"])
        self.assertTrue(edge["independence_claim"])

    def test_19_direct_transclusion_does_not_claim_independence(self):
        edge = relation(self.relations, "ISR-CROSS-OPERATOR-TRANSCLUSION-001")
        self.assertEqual("direct-transclusion", edge["information_path"])
        self.assertFalse(edge["independence_claim"])

    def test_20_relation_cannot_inherit_source_authority_state(self):
        mutation = copy.deepcopy(self.records)
        edge = relation(mutation["inter_somnic_relations"], "ISR-CROSS-OPERATOR-TRANSCLUSION-001")
        edge["inherited_properties"] = ["applicability", "closure", "confidence", "authorization"]
        self.assertRecordsRejected(mutation, "cannot inherit source properties")

    def test_21_received_t2_evidence_stays_separate_from_t1_evidence(self):
        edge = relation(self.relations, "ISR-CROSS-OPERATOR-TRANSCLUSION-001")
        self.assertFalse(set(edge["received_at_t2_evidence_ids"]) & set(edge["target_t1_evidence_ids"]))
        mutation = copy.deepcopy(self.records)
        mutated = relation(mutation["inter_somnic_relations"], "ISR-CROSS-OPERATOR-TRANSCLUSION-001")
        mutated["target_t1_evidence_ids"] = list(mutated["received_at_t2_evidence_ids"])
        self.assertRecordsRejected(mutation, "received t2 evidence cannot become target t1 evidence")

    def test_22_duplicate_relation_identity_is_rejected(self):
        mutation = copy.deepcopy(self.records)
        mutation["inter_somnic_relations"].append(copy.deepcopy(mutation["inter_somnic_relations"][0]))
        self.assertRecordsRejected(mutation, "inter-somnic relation registry duplicate")
        for field, malformed in (
            ("semantic_relation", {"not": "a scalar"}),
            ("information_path", ["direct-transclusion"]),
            ("operation_version", {"version": "0.1.0"}),
            ("material_delta_id", ["DELTA-CONTRACT-0.1.1"]),
            ("idempotency_key", {"not": "a scalar"}),
        ):
            with self.subTest(malformed_field=field):
                mutation = copy.deepcopy(self.records)
                relation(
                    mutation["inter_somnic_relations"],
                    "ISR-SAME-RUN-COMPARE-001",
                )[field] = malformed
                code, output = production_exit(
                    self.activation, mutation, self.inventory, self.adoption,
                    self.collective,
                )
                self.assertEqual(1, code, output)
                self.assertNotIn("TRACEBACK", output)

    def test_23_recursive_reopening_cycle_is_rejected(self):
        mutation = copy.deepcopy(self.records)
        edge = copy.deepcopy(relation(mutation["inter_somnic_relations"], "ISR-REOPENS-001"))
        edge["inter_somnic_relation_id"] = "ISR-REOPENS-CYCLE-001"
        edge["source_episode_id"], edge["target_episode_id"] = edge["target_episode_id"], edge["source_episode_id"]
        edge["idempotency_key"] = "reopen-cycle:forbidden"
        mutation["inter_somnic_relations"].append(edge)
        self.assertRecordsRejected(mutation, "reopening relation graph must be acyclic")

    def test_24_assessment_without_inter_somnic_relation_remains_valid(self):
        assessment = item(self.records["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")
        self.assertEqual([], assessment["inter_somnic_relation_ids"])
        related_assessments = {
            assessment_id
            for edge in self.relations
            for key in ("source_assessment_ids", "target_assessment_ids")
            for assessment_id in edge[key]
        }
        self.assertNotIn("SA-NO-CHANGE-001", related_assessments)

    def test_25_r7e_reconstruction_cannot_be_labeled_live_telemetry(self):
        episode = item(self.episodes, "somnic_episode_id", "SEP-R7E-RECONSTRUCTION")
        self.assertEqual("reconstructed-analogue-not-live", episode["telemetry_status"])
        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_episodes"], "somnic_episode_id", "SEP-R7E-RECONSTRUCTION")["telemetry_status"] = "live-telemetry"
        self.assertRecordsRejected(mutation, "R7E reconstruction cannot claim live telemetry")

    def test_26_existing_task4_production_surface_remains_green(self):
        code, output = production_exit(
            self.activation, self.records, self.inventory, self.adoption,
            self.collective,
        )
        self.assertEqual(0, code, output)
        self.assertIn("TOTAL: 0 failures", output)


if __name__ == "__main__":
    unittest.main()
