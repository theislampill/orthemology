#!/usr/bin/env python3
"""Focused Task 4 tests for bounded waking/somnic contracts."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_somnic_orthing.py"
ACTIVATION = ROOT / "examples" / "somnus" / "activation-contract-fixtures.yaml"
RECORDS = ROOT / "examples" / "somnus" / "somnus-record-fixtures.yaml"
INVENTORY = ROOT / "applications" / "agentic-runtime" / "SOMNUS-CANDIDATE-INVENTORY.yaml"
ADOPTION = ROOT / "applications" / "agentic-runtime" / "HERMES-WRITEBACK-ADOPTION-PROFILE.yaml"
COLLECTIVE = ROOT / "applications" / "agentic-runtime" / "COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml"
DECISION = ROOT / "docs" / "decisions" / "0035-somnic-orthing-and-activation-contracts.md"
SCHEMAS = [
    ROOT / "schemas" / name
    for name in (
        "activation-contract.schema.json",
        "orthing-event.schema.json",
        "meta-orthability-assessment.schema.json",
        "somnus-run.schema.json",
        "somnic-assessment.schema.json",
        "residual-recurrence-report.schema.json",
    )
]


def load_module():
    spec = importlib.util.spec_from_file_location("somnic_orthing_probe", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not import production validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def item(rows, key, value):
    return next(row for row in rows if row[key] == value)


def production_exit(activation, records, inventory, adoption, collective, decision_text=None):
    module = load_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        documents = {
            "ACTIVATION_PATH": (temp / "activation.yaml", activation),
            "RECORDS_PATH": (temp / "records.yaml", records),
            "INVENTORY_PATH": (temp / "inventory.yaml", inventory),
            "ADOPTION_PATH": (temp / "adoption.yaml", adoption),
            "COLLECTIVE_PATH": (temp / "collective.yaml", collective),
        }
        for attr, (path, value) in documents.items():
            path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
            setattr(module, attr, path)
        decision_path = temp / "decision.md"
        decision_path.write_text(
            DECISION.read_text(encoding="utf-8") if decision_text is None else decision_text,
            encoding="utf-8",
        )
        module.DECISION_PATH = decision_path
        output = io.StringIO()
        exit_code = 0
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                module.main()
            except SystemExit as exc:
                exit_code = int(exc.code or 0)
            except Exception as exc:  # traceback is itself a contract failure
                exit_code = 99
                output.write("TRACEBACK: %s: %s" % (type(exc).__name__, exc))
        return exit_code, output.getvalue()


class SomnicOrthingTests(unittest.TestCase):
    def setUp(self):
        required = [SCRIPT, ACTIVATION, RECORDS, INVENTORY, ADOPTION, COLLECTIVE, DECISION, *SCHEMAS]
        self.assertEqual([], [str(path) for path in required if not path.exists()])
        self.activation = yaml.safe_load(ACTIVATION.read_text(encoding="utf-8"))
        self.records = yaml.safe_load(RECORDS.read_text(encoding="utf-8"))
        self.inventory = yaml.safe_load(INVENTORY.read_text(encoding="utf-8"))
        self.adoption = yaml.safe_load(ADOPTION.read_text(encoding="utf-8"))
        self.collective = yaml.safe_load(COLLECTIVE.read_text(encoding="utf-8"))

    def assertRejected(self, *, activation=None, records=None, inventory=None,
                       adoption=None, collective=None, fragment=None):
        code, output = production_exit(
            self.activation if activation is None else activation,
            self.records if records is None else records,
            self.inventory if inventory is None else inventory,
            self.adoption if adoption is None else adoption,
            self.collective if collective is None else collective,
        )
        self.assertEqual(1, code, output)
        self.assertNotIn("TRACEBACK", output)
        if fragment:
            self.assertIn(fragment, output)

    def test_valid_documents_pass_schemas_and_production_entry_point(self):
        for path in SCHEMAS:
            with self.subTest(schema=path.name):
                Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
        code, output = production_exit(
            self.activation, self.records, self.inventory, self.adoption, self.collective
        )
        self.assertEqual(0, code, output)
        self.assertIn("TOTAL: 0 failures", output)

    def test_eighteen_controlling_attacks_fail_through_production_entry_point(self):
        cases = []

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["target_history_mutated"] = True
        cases.append(("target-history overwrite", {"records": mutation}, "append-only"))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["target_orthing_ids"] = []
        cases.append(("missing target identity", {"records": mutation}, "target"))

        mutation = copy.deepcopy(self.records)
        event = item(mutation["orthing_events"], "event_id", "EV-WAKE-001")
        event["episode_id"] = event["session_id"]
        event["occurrence_id"] = event["session_id"]
        event["orthing_id"] = event["session_id"]
        cases.append(("collapsed identity levels", {"records": mutation}, "identity"))

        mutation = copy.deepcopy(self.activation)
        outcome = item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")["claimant_assessments"][0]
        outcome.pop("evaluator_version")
        cases.append(("missing evaluator version", {"activation": mutation}, "evaluator"))

        mutation = copy.deepcopy(self.activation)
        outcome = item(mutation["fixture_outcomes"], "fixture_id", "ACT-MIXED-LEXICAL-001")["claimant_assessments"][0]
        outcome["result"] = "applicable"
        cases.append(("keyword-only applicability", {"activation": mutation}, "required properties"))

        mutation = copy.deepcopy(self.activation)
        mutation["evaluators"][0]["result_vocabulary"] = ["applicable", "inapplicable"]
        cases.append(("binary-only evaluator", {"activation": mutation}, "tri-state"))

        mutation = copy.deepcopy(self.records)
        assessment = item(mutation["somnic_assessments"], "assessment_id", "SA-EVIDENCE-TIMING-001")
        assessment["evidence_timing"]["observed_at_t1"].append(
            assessment["evidence_timing"]["discovered_after_t1"].pop()
        )
        cases.append(("later evidence relabeled t1", {"records": mutation}, "evidence timing"))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-R7E-RETRO-001")["capture_mode"] = "live_capture"
        cases.append(("retrospective capture relabeled live", {"records": mutation}, "R7E"))

        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["fixture_outcomes"] = []
        cases.append(("accepted contract without outcomes", {"activation": mutation}, "fixture outcomes"))

        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["authorship"] = {"mode": "normal"}
        cases.append(("normal contract without authoring orthing", {"activation": mutation}, "authorship"))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["retroactive_conformity_rewrite"] = True
        cases.append(("revision rewrites conformity", {"records": mutation}, "historical conformity"))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")["material_delta_ids"] = []
        cases.append(("reopen without delta", {"records": mutation}, "material delta"))

        mutation = copy.deepcopy(self.records)
        duplicate = copy.deepcopy(item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001"))
        duplicate["somnus_run_id"] = "RUN-RECURRENCE-DUPLICATE"
        duplicate["output_ids"] = ["RR-NON-EQUIVALENT"]
        mutation["somnus_runs"].append(duplicate)
        cases.append(("duplicate idempotency output", {"records": mutation}, "idempotency"))

        mutation = copy.deepcopy(self.records)
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["supporting_occurrences"] = [copy.deepcopy(report["supporting_occurrences"][0])] * 3
        report["dependence_dimensions"]["episode_count"] = 3
        cases.append(("copy-count inflated recurrence", {"records": mutation}, "distinct episodes"))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["systemic_defect_proven"] = True
        cases.append(("threshold treated as proof", {"records": mutation}, "review trigger"))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["emitted_actions"] = ["automatic_patch"]
        cases.append(("automatic v0 mutation", {"records": mutation}, "v0"))

        mutation = copy.deepcopy(self.records)
        item(mutation["authorizations"], "authorization_id", "AUTH-PROVISIONAL-001")["authorized"] = True
        cases.append(("placement self-authorizes mutation", {"records": mutation}, "authorization"))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["status"] = "implemented"
        mutation["candidates"][0]["execution"] = "deployed"
        cases.append(("outline represented as runtime", {"inventory": mutation}, "outline-only"))

        for name, changes, fragment in cases:
            with self.subTest(attack=name):
                self.assertRejected(fragment=fragment, **changes)

    def test_claimant_frontier_and_recurrence_precision_fixtures_are_structured(self):
        identity = self.records["identity_fixture"]
        self.assertEqual(2, len(identity["occurrence_ids"]))
        self.assertEqual(2, len(identity["episode_ids"]))
        self.assertTrue(set(identity["occurrence_ids"]).isdisjoint(identity["episode_ids"]))

        route = item(self.records["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")
        results = {row["claimant_id"]: row["result"] for row in route["claimant_assessments"]}
        self.assertEqual("indeterminate", results["claimant-c"])
        self.assertEqual("applicable", results["claimant-d"])
        self.assertEqual("claimant-d", route["selected_claimant_id"])
        self.assertIn("claimant-c", route["retained_residual_claimants"])
        self.assertIn("claimant-e", route["retained_inapplicable_claimants"])

        run = item(self.records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        self.assertNotEqual(run["anchor_subject_ids"], run["historical_comparator_ids"])
        self.assertEqual(False, run["historical_comparators_reopened"])
        next_run = item(self.records["somnus_runs"], "somnus_run_id", "RUN-NEXT-001")
        self.assertNotIn("SA-CLOSED-001", next_run["anchor_subject_ids"])
        reopened = item(self.records["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")
        self.assertIn("SA-CLOSED-001", reopened["anchor_subject_ids"])
        self.assertTrue(reopened["material_delta_ids"])

        report = item(self.records["recurrence_reports"], "recurrence_report_id", "RR-001")
        self.assertFalse(report["independence_assessment"]["passed"])
        self.assertEqual("not-established", report["causal_diagnosis"])
        self.assertFalse(report["systemic_defect_proven"])
        pathway = item(self.records["somnic_assessments"], "assessment_id", "SA-CORRECT-DEFECTIVE-001")
        self.assertEqual("correct", pathway["placement_result"])
        self.assertEqual("defective", pathway["pathway_result"])

    def test_writeback_subsumption_keeps_assessment_proposal_authorization_and_outcome_distinct(self):
        expected_cases = {
            "memory-proposal", "skill-proposal", "contract-locus", "no-change",
            "alternative-proposals", "rejected-proposal", "failed-application",
            "later-outcome-required", "legacy-provenance", "grounded-provenance",
            "unwarranted-user-state", "upstream-evidence-defect",
            "correct-output-defective-pathway",
        }
        self.assertTrue(expected_cases <= set(self.records["writeback_fixture_cases"]))
        no_change = item(self.records["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")
        self.assertEqual("no_change", no_change["intervention_disposition"])
        self.assertEqual([], no_change["proposal_ids"])
        alternatives = item(self.records["somnic_assessments"], "assessment_id", "SA-ALTERNATIVES-001")
        self.assertEqual(2, len(alternatives["proposal_ids"]))
        for proposal_id in alternatives["proposal_ids"]:
            self.assertFalse(item(self.records["proposals"], "proposal_id", proposal_id)["authorized"])
        self.assertEqual(
            {"legacy_reflective_proposal", "somnus_grounded_proposal"},
            {row["provenance_mode"] for row in self.records["proposals"]},
        )
        timeline = self.records["writeback_timeline"]
        self.assertEqual(["t1", "t2", "t3", "t4", "t5"], [row["time_role"] for row in timeline])
        for application in self.records["applications"]:
            authorization = item(
                self.records["authorizations"],
                "authorization_id",
                application["authorization_id"],
            )
            self.assertEqual(application["proposal_id"], authorization["proposal_id"])
            if application["status"] == "applied":
                self.assertTrue(authorization["authorized"])

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")["proposal_ids"] = ["PROP-FORCED"]
        self.assertRejected(records=mutation, fragment="no-change")

    def test_collective_profile_attacks_fail_closed(self):
        mutations = []
        mutation = copy.deepcopy(self.collective); mutation["modes"][1]["mode_id"] = "C1"; mutations.append((mutation, "mode"))
        mutation = copy.deepcopy(self.collective); mutation["shared_types_supply_transport"] = True; mutations.append((mutation, "transport"))
        mutation = copy.deepcopy(self.collective); mutation["event_instances"]["actor_ledger_version_indexed"] = False; mutations.append((mutation, "actor"))
        mutation = copy.deepcopy(self.collective); mutation["source_applicability_auto_propagates"] = True; mutations.append((mutation, "applicability"))
        mutation = copy.deepcopy(self.collective); mutation["receipt_can_govern_or_execute"] = True; mutations.append((mutation, "receipt"))
        mutation = copy.deepcopy(self.collective); mutation["transclusion"]["semantic_character"] = "structural-not-semantic-and-lossless"; mutations.append((mutation, "semantic"))
        mutation = copy.deepcopy(self.collective); mutation["multi_operator_count_implies"] = ["independence"]; mutations.append((mutation, "multi-operator"))
        mutation = copy.deepcopy(self.collective); mutation["source_envelope"]["immutable"] = False; mutations.append((mutation, "source envelope"))
        mutation = copy.deepcopy(self.collective); mutation["collective_closure"]["preserves_dissent"] = False; mutations.append((mutation, "dissent"))
        mutation = copy.deepcopy(self.collective); mutation["privacy"]["redacted_projection_may_claim_complete"] = True; mutations.append((mutation, "redacted"))
        mutation = copy.deepcopy(self.collective); mutation["automatic adoption"] = "allowed"; mutations.append((mutation, "automatic"))
        for mutation, fragment in mutations:
            with self.subTest(fragment=fragment):
                self.assertRejected(collective=mutation, fragment=fragment)

    def test_malformed_documents_fail_with_diagnostics_not_traceback(self):
        cases = [
            ([], self.records, self.inventory, self.adoption, self.collective),
            (self.activation, [], self.inventory, self.adoption, self.collective),
            (self.activation, self.records, [], self.adoption, self.collective),
            (self.activation, self.records, self.inventory, [], self.collective),
            (self.activation, self.records, self.inventory, self.adoption, []),
        ]
        for documents in cases:
            with self.subTest(types=[type(value).__name__ for value in documents]):
                code, output = production_exit(*documents)
                self.assertEqual(1, code, output)
                self.assertNotIn("TRACEBACK", output)
                self.assertIn("TOTAL:", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
