#!/usr/bin/env python3
"""Focused Task 4 tests for bounded waking/somnic contracts."""
from __future__ import annotations

import contextlib
import copy
import hashlib
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
HISTORY = ROOT / "examples" / "somnus" / "somnus-history-checkpoints.yaml"
INVENTORY = ROOT / "applications" / "agentic-runtime" / "SOMNUS-CANDIDATE-INVENTORY.yaml"
ADOPTION = ROOT / "applications" / "agentic-runtime" / "HERMES-WRITEBACK-ADOPTION-PROFILE.yaml"
COLLECTIVE = ROOT / "applications" / "agentic-runtime" / "COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml"
DECISION = ROOT / "docs" / "decisions" / "0035-somnic-orthing-and-activation-contracts.md"
SCHEMAS = [
    ROOT / "schemas" / name
    for name in (
        "activation-contract.schema.json",
        "activation-contract-fixtures.schema.json",
        "orthing-event.schema.json",
        "meta-orthability-assessment.schema.json",
        "somnus-run.schema.json",
        "somnic-assessment.schema.json",
        "residual-recurrence-report.schema.json",
        "somnus-record-fixtures.schema.json",
        "somnus-history-checkpoints.schema.json",
        "somnus-claim-status.schema.json",
        "somnus-candidate-inventory.schema.json",
        "hermes-writeback-adoption-profile.schema.json",
        "collective-somnus-transclusion-profile.schema.json",
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
        required = [SCRIPT, ACTIVATION, RECORDS, HISTORY, INVENTORY, ADOPTION, COLLECTIVE, DECISION, *SCHEMAS]
        self.assertEqual([], [str(path) for path in required if not path.exists()])
        self.activation = yaml.safe_load(ACTIVATION.read_text(encoding="utf-8"))
        self.records = yaml.safe_load(RECORDS.read_text(encoding="utf-8"))
        self.inventory = yaml.safe_load(INVENTORY.read_text(encoding="utf-8"))
        self.adoption = yaml.safe_load(ADOPTION.read_text(encoding="utf-8"))
        self.collective = yaml.safe_load(COLLECTIVE.read_text(encoding="utf-8"))

    def assertRejected(self, *, activation=None, records=None, inventory=None,
                       adoption=None, collective=None, decision_text=None,
                       fragment=None):
        code, output = production_exit(
            self.activation if activation is None else activation,
            self.records if records is None else records,
            self.inventory if inventory is None else inventory,
            self.adoption if adoption is None else adoption,
            self.collective if collective is None else collective,
            decision_text,
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
        item(mutation["authorizations"], "authorization_id", "AUTH-INDEPENDENT-001")["source"] = "provisional_placement"
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
            proposal = item(self.records["proposals"], "proposal_id", proposal_id)
            self.assertNotIn("authorized", proposal)
            for authorization in self.records["authorizations"]:
                if authorization["proposal_id"] == proposal_id:
                    self.assertEqual("independent_governance", authorization["source"])
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
                self.assertEqual("authorized", authorization["decision"])

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

    def test_independent_review_38_case_regression_suite(self):
        """Every independent-review case must fail through ``main()``."""
        cases = []

        # Capture / identity / routing / evidence / time (9).
        mutation = copy.deepcopy(self.records)
        mutation.pop("identity_fixture")
        cases.append(("capture-01-missing-identity-fixture", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        identity = mutation["identity_fixture"]
        identity["occurrence_ids"] = list(identity["episode_ids"])
        identity["orthing_ids"] = list(identity["episode_ids"])
        cases.append(("capture-02-collapsed-global-identities", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation.pop("claimant_routing_cases")
        cases.append(("capture-03-missing-claimant-routing", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        route = item(mutation["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")
        route["selected_claimant_id"] = "claimant-c"
        cases.append(("capture-04-indeterminate-claimant-selected", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["orthing_events"] = []
        cases.append(("capture-05-no-incremental-events", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        event = item(mutation["orthing_events"], "event_id", "EV-WAKE-001")
        event["event_type"] = "orthability_assessed"
        event["claim_attempt_id"] = None
        event["orthability_assessment_id"] = None
        cases.append(("capture-06-assessment-event-without-claimant-identities", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-EVIDENCE-TIMING-001")["t2_configuration"]["assessed_at"] = "2026-07-19T09:00:00Z"
        cases.append(("capture-07-t2-before-target-t1", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        timing = item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["evidence_timing"]
        timing["indexed_unused_at_t1"].append("E-T1-USED")
        cases.append(("capture-08-evidence-used-and-unused", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["evidence_timing"]["used_at_t1"].append("E-UNKNOWN")
        cases.append(("capture-09-unresolved-evidence-reference", {"records": mutation}))

        # Per-contract four-class activation evidence (3).
        mutation = copy.deepcopy(self.activation)
        overlap = item(mutation["fixture_outcomes"], "fixture_id", "ACT-OVERLAP-001")
        overlap["claimant_assessments"] = [
            row for row in overlap["claimant_assessments"]
            if row["activation_contract_id"] != "database-schema-activation"
        ]
        cases.append(("activation-01-contract-missing-class-assessment", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        assessment = item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")["claimant_assessments"][0]
        assessment["result"] = "inapplicable"
        cases.append(("activation-02-inapplicable-despite-properties", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        item(mutation["fixture_outcomes"], "fixture_id", "ACT-OVERLAP-001").pop("conflict")
        cases.append(("activation-03-overlap-without-conflict", {"activation": mutation}))

        # Frontier / idempotency / recurrence / independence (8).
        mutation = copy.deepcopy(self.records)
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["historical_comparator_ids"] = list(run["anchor_subject_ids"])
        cases.append(("frontier-01-anchor-comparator-overlap", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-NEXT-001")["idempotency_key"] = item(
            mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001"
        )["idempotency_key"]
        cases.append(("frontier-02-idempotency-key-reused-for-input", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["started_at"], run["completed_at"] = run["completed_at"], run["started_at"]
        cases.append(("frontier-03-reversed-run-time", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["output_ids"].append("UNKNOWN-OUTPUT")
        cases.append(("frontier-04-unresolved-output", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        dims = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["dependence_dimensions"]
        dims.update(session_count=3, normalized_input_family_count=3, actor_count=3, source_family_count=3)
        cases.append(("frontier-05-falsified-dependence-counts", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        independence = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["independence_assessment"]
        independence.update(passed=True, label="independent episodes")
        cases.append(("frontier-06-independence-over-common-source", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["threshold"] = 9
        cases.append(("frontier-07-threshold-exceeds-support", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["fingerprint"]["source_orthing_ids"] = ["ORTH-UNRELATED"]
        cases.append(("frontier-08-fingerprint-support-disconnected", {"records": mutation}))

        # Writeback chain (5).
        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["authorized"] = True
        cases.append(("writeback-01-proposal-self-authorizes", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation.pop("writeback_timeline")
        cases.append(("writeback-02-missing-timeline", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        for row in mutation["writeback_timeline"]:
            row["time_role"] = "t3"
        cases.append(("writeback-03-collapsed-timeline", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        investigation = item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")
        investigation["proposal_ids"] = ["PROP-MEMORY-001"]
        cases.append(("writeback-04-investigation-carries-proposal", {"records": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"]["ordinary_targets"] = []
        mutation["subsumption"]["governing_targets"] = []
        cases.append(("writeback-05-target-vocabularies-erased", {"adoption": mutation}))

        # Collective profile (7).
        mutation = copy.deepcopy(self.collective)
        mutation["status"] = "implemented"
        cases.append(("collective-01-profile-implemented", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        for row in mutation["modes"]:
            row["information_path"] = "same-path"
            row["coordination"] = "same-coordination"
        cases.append(("collective-02-modes-semantically-identical", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["source_envelope"]["required_identity"] = []
        cases.append(("collective-03-source-identity-erased", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["receiving_assessment"]["append_only"] = False
        mutation["receiving_assessment"]["local_meta_orthability_required"] = False
        mutation["receiving_assessment"]["local_authorization_required"] = False
        cases.append(("collective-04-receiving-gates-disabled", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["semantic_boundaries"]["exported_record_is_direct_soul_access"] = True
        mutation["semantic_boundaries"]["multi_operator_recurrence_proves_tawatur"] = True
        cases.append(("collective-05-testimony-interior-boundaries-reversed", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["security"]["threats"] = []
        mutation["security"]["controls"] = []
        cases.append(("collective-06-safeguards-erased", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["transclusion"].pop("levels")
        mutation["transclusion"].pop("gates")
        cases.append(("collective-07-levels-and-gates-erased", {"collective": mutation}))

        # Structured non-claims (2).
        mutation = copy.deepcopy(self.inventory)
        mutation["claim_status"] = {
            "empirical_validation": {"status": "established"},
            "runtime": {"status": "implemented"},
        }
        cases.append(("claims-01-inventory-boundary-inverted", {"inventory": mutation}))

        decision_text = DECISION.read_text(encoding="utf-8") + """
<!-- somnus-claim-status:start -->
```yaml
empirical_validation: established
runtime: implemented
```
<!-- somnus-claim-status:end -->
"""
        cases.append(("claims-02-decision-boundary-inverted", {"decision_text": decision_text}))

        # Nested malformed values (4); diagnostics, never traceback.
        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["dependence_dimensions"] = "malformed"
        cases.append(("malformed-01-recurrence-dimensions-scalar", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["independence_assessment"] = 7
        cases.append(("malformed-02-independence-scalar", {"records": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["event_instances"] = "malformed"
        cases.append(("malformed-03-event-instances-scalar", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["source_envelope"] = 7
        cases.append(("malformed-04-source-envelope-scalar", {"collective": mutation}))

        self.assertEqual(38, len(cases))
        for name, changes in cases:
            with self.subTest(case=name):
                self.assertRejected(**changes)

    def test_review_equivalence_classes_and_nested_variants_fail_closed(self):
        cases = []

        mutation = copy.deepcopy(self.records)
        mutation["evidence_records"].append({"evidence_id": "E-T1-USED", "timing": "used_at_t1"})
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")["material_delta_ids"] = ["UNKNOWN-DELTA"]
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["opportunity_denominator"] = 2
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")["authorization_refs"] = ["UNKNOWN-AUTH"]
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.collective)
        mutation["receiving_assessment"] = []
        cases.append({"collective": mutation})

        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"] = "malformed"
        cases.append({"adoption": mutation})

        mutation = copy.deepcopy(self.records)
        route_event = item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")
        route_event["claim_attempt_id"] = "CA-001"
        route_event["orthability_assessment_id"] = "OA-001"
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["privacy_source_disposition"]["privacy_scope_applied"] = False
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["somnus_run_id"] = "RUN-NEXT-001"
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["proposed_action"]["action_label"] = "mismatched-action"
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-NEXT-001")["output_ids"] = ["SA-RECURRENCE-001"]
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["meta_orthability_assessments"], "meta_orthability_assessment_id", "MOA-001")["subject_ids"].append("ORTH-002")
        cases.append({"records": mutation})

        mutation = copy.deepcopy(self.records)
        item(mutation["outcome_evaluations"], "outcome_evaluation_id", "OUTCOME-001")["evaluated_at"] = "2026-07-21T19:04:00Z"
        cases.append({"records": mutation})

        for index, changes in enumerate(cases, 1):
            with self.subTest(variant=index):
                self.assertRejected(**changes)

    def test_second_rereview_18_fresh_mutations_fail_closed(self):
        cases = []

        # Meta-orthability scope and bidirectional run-output ownership (3).
        mutation = copy.deepcopy(self.records)
        item(mutation["meta_orthability_assessments"], "meta_orthability_assessment_id", "MOA-001")["subject_ids"] = ["ORTH-002"]
        cases.append(("meta-gate-wrong-resolved-subject", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        gate = item(mutation["meta_orthability_assessments"], "meta_orthability_assessment_id", "MOA-001")
        gate.update(result="inapplicable", assessable=False, non_assessment_reason="declared inapplicable")
        cases.append(("meta-gate-coherent-but-nonassessable", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-EVIDENCE-TIMING-001")["somnus_run_id"] = "RUN-NEXT-001"
        cases.append(("assessment-missing-from-declared-run-outputs", {"records": mutation}))

        # One authoritative t1-t5 writeback chain and record chronology (2).
        mutation = copy.deepcopy(self.records)
        mutation["writeback_timeline"][2]["record_ids"] = ["PROP-MEMORY-001", "AUTH-FAILED-001"]
        mutation["writeback_timeline"][3]["record_ids"] = ["APP-FAILED-001", "SUCCESSOR-CONTRACT-001"]
        cases.append(("disconnected-but-resolvable-writeback-timeline", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["applications"], "application_id", "APP-APPLIED-001")["applied_at"] = "2026-07-21T19:02:00Z"
        cases.append(("application-record-time-precedes-authorization", {"records": mutation}))

        # Count-preserving Collective semantic inversions (5).
        mutation = copy.deepcopy(self.collective)
        for index, mode in enumerate(mutation["modes"], 1):
            mode.update(name=f"garbage-name-{index}", information_path=f"garbage-path-{index}", coordination=f"garbage-rule-{index}")
        cases.append(("collective-mode-meanings-replaced", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["dependence_dimensions"] = [f"garbage-dependence-{index}" for index in range(9)]
        cases.append(("collective-dependence-vocabulary-replaced", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        for level in mutation["transclusion"]["levels"]:
            level["permitted_effect"] = "automatic_execution"
            level["prohibited_effect"] = "local_assessment"
        cases.append(("collective-level-effects-inverted", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["source_envelope"]["disclosure"] = [f"garbage-disclosure-{index}" for index in range(6)]
        cases.append(("collective-disclosure-vocabulary-replaced", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["collective_closure"]["permitted"] = [f"garbage-closure-{index}" for index in range(7)]
        cases.append(("collective-closure-vocabulary-replaced", {"collective": mutation}))

        # Nested malformed values must diagnose through production main (8).
        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["required_properties"] = [["nested"]]
        cases.append(("malformed-activation-required-properties", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["contract_id"] = []
        cases.append(("malformed-activation-contract-id", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")["claimant_assessments"][0]["claimant_id"] = []
        cases.append(("malformed-routing-claimant-id", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["session_id"] = []
        cases.append(("malformed-event-session-id", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["anchor_subject_ids"] = [["nested"]]
        cases.append(("malformed-run-anchor-subjects", {"records": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["modes"][0]["information_path"] = {}
        cases.append(("malformed-collective-information-path", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["bearer_separation"] = [["nested"], "represented_standard_at_actor_time", "case_bound_metaorthemma", "execution_trace", "transclusion_envelope"]
        cases.append(("malformed-collective-bearer-separation", {"collective": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"]["ordinary_targets"] = [["nested"]]
        cases.append(("malformed-adoption-ordinary-targets", {"adoption": mutation}))

        self.assertEqual(18, len(cases))
        for name, changes in cases:
            with self.subTest(case=name):
                self.assertRejected(**changes)

    def test_third_review_40_cross_document_mutations_fail_closed(self):
        """Close the fresh second-rereview's exact cross-document families."""
        cases = []

        # Exact activation-contract/evaluator/evidence/authorship binding (8).
        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["activation_contract_id"] = "unknown-contract"
        cases.append(("meta-01-unknown-contract", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["activation_contract_version"] = "99.0.0"
        cases.append(("meta-02-unknown-contract-version", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["orthability_evaluator_id"] = "unknown-evaluator"
        cases.append(("meta-03-unknown-evaluator", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["orthability_evaluator_version"] = "99.0.0"
        cases.append(("meta-04-unknown-evaluator-version", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["evidence_state_ids"] = ["E-UNKNOWN"]
        cases.append(("meta-05-unknown-evidence", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        gate = mutation["meta_orthability_assessments"][0]
        gate["satisfied_properties"] = ["preserved-target"]
        gate["absent_properties"] = ["sufficient-residual-structure"]
        cases.append(("meta-06-applicable-with-absent-property", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["non_assessment_reason"] = "not assessable"
        cases.append(("meta-07-applicable-with-non-assessment-reason", {"records": mutation}))

        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["authorship"] = {"mode": "normal", "orthing_id": "ORTH-UNKNOWN"}
        cases.append(("meta-08-unknown-normal-authoring-orthing", {"activation": mutation}))

        # Globally typed event identity, provenance, and lifecycle order (6).
        mutation = copy.deepcopy(self.records)
        replacement = {
            "session_id": "SESSION-UNREGISTERED",
            "episode_id": "EP-UNREGISTERED",
            "occurrence_id": "OCC-UNREGISTERED",
            "orthing_id": "ORTH-UNREGISTERED",
        }
        for event_id in ("EV-WAKE-001", "EV-WAKE-001-ASSESS", "EV-WAKE-001-ROUTE"):
            item(mutation["orthing_events"], "event_id", event_id).update(replacement)
        mutation["claimant_routing_cases"][0]["occurrence_id"] = "OCC-UNREGISTERED"
        cases.append(("event-01-unregistered-lifecycle-identities", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        retro = item(mutation["orthing_events"], "event_id", "EV-R7E-RETRO-001")
        retro.pop("source_case")
        retro["capture_mode"] = "live_capture"
        cases.append(("event-02-retrospective-provenance-bypass", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        assessed = item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ASSESS")
        routed = item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")
        assessed.update(sequence=3, occurred_at="2026-07-20T10:02:00Z")
        routed.update(sequence=2, occurred_at="2026-07-20T10:01:00Z")
        cases.append(("event-03-route-before-assessment", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-002-CAPTURE")["actor_id"] = "SESSION-001"
        cases.append(("event-04-wrong-kind-actor-identity", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-002-CAPTURE")["occurrence_id"] = "OCC-UNKNOWN"
        item(mutation["orthing_events"], "event_id", "EV-WAKE-002")["occurrence_id"] = "OCC-UNKNOWN"
        cases.append(("event-05-unknown-occurrence-identity", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        duplicate = copy.deepcopy(mutation["claimant_routing_cases"][0])
        duplicate["case_id"] = "ROUTE-DUPLICATE-001"
        duplicate["claimant_assessments"] = [{
            "claim_attempt_id": "CA-001",
            "orthability_assessment_id": "OA-001",
            "claimant_id": "claimant-duplicate",
            "result": "applicable",
        }]
        duplicate["selected_claimant_id"] = "claimant-duplicate"
        duplicate["retained_residual_claimants"] = []
        duplicate["retained_inapplicable_claimants"] = []
        mutation["claimant_routing_cases"].append(duplicate)
        cases.append(("event-06-duplicate-route-for-occurrence", {"records": mutation}))

        # Append-only assessment history and globally unique run output ownership (7).
        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-CLOSED-001")["prior_assessment_ids"] = ["SA-CLOSED-001"]
        cases.append(("history-01-self-prior-assessment", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-CLOSED-001")["prior_assessment_ids"] = ["SA-REOPENED-001"]
        item(mutation["somnic_assessments"], "assessment_id", "SA-REOPENED-001")["prior_assessment_ids"] = ["SA-CLOSED-001"]
        cases.append(("history-02-cyclic-prior-assessments", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["target_history_digest"] = "2" * 64
        cases.append(("history-03-unverifiable-target-digest", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["recurrence_report_id"] = "SA-RECURRENCE-001"
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["output_ids"] = [value for value in run["output_ids"] if value != "RR-001"]
        cases.append(("output-01-cross-kind-id-collision", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["t2_configuration"]["assessed_at"] = "2026-07-21T18:30:00Z"
        cases.append(("output-02-assessment-before-owning-run", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["t2_configuration"]["assessed_at"] = "2026-07-21T20:00:00Z"
        cases.append(("output-03-assessment-after-owning-run", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["historical_comparators_reopened"] = True
        cases.append(("output-04-false-comparator-reopened-assertion", {"records": mutation}))

        # Recurrence provenance, threshold, fingerprint, opportunity, and policy (6).
        mutation = copy.deepcopy(self.records)
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["supporting_occurrences"][0]["episode_id"] = "EP-FABRICATED"
        cases.append(("recurrence-01-fabricated-episode", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["supporting_occurrences"][0]["session_id"] = "SESSION-FABRICATED"
        cases.append(("recurrence-02-fabricated-session", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        for row in report["supporting_occurrences"]:
            row["episode_id"] = "EP-ONE"
        report["dependence_dimensions"]["episode_count"] = 1
        cases.append(("recurrence-03-threshold-with-one-episode", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["supporting_occurrences"][2]["session_id"] = "SESSION-THIRD"
        report["dependence_dimensions"]["session_count"] = 3
        independence = report["independence_assessment"]
        independence["required_dimensions"] = ["session_count"]
        independence["evaluated_dimensions"]["session_count"] = True
        independence.update(passed=True, label="independent episodes")
        cases.append(("recurrence-04-ad-hoc-weakened-independence-policy", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["fingerprint"]["normalized_object"] = "unrelated-family"
        cases.append(("recurrence-05-fingerprint-not-bound-to-support", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["opportunity_denominator"] = 999
        cases.append(("recurrence-06-unbacked-opportunity-denominator", {"records": mutation}))

        # Writeback coherence and authoritative time (4).
        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["status"] = "rejected"
        cases.append(("writeback-01-applied-rejected-proposal", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-CORRECT-DEFECTIVE-001")["assessment_result"] = "no_change"
        cases.append(("writeback-02-no-change-result-with-mutation-proposal", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["writeback_timeline"][2]["occurred_at"] = "2026-07-21T19:02:30Z"
        cases.append(("writeback-03-timeline-contradicts-authoritative-authorization", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        proposal = item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")
        proposal.update(provenance_mode="legacy_reflective_proposal", supporting_assessment_id="unavailable")
        cases.append(("writeback-04-legacy-proposal-laundered-into-assessment", {"records": mutation}))

        # Closed adoption vocabularies and typed candidate/non-claim boundaries (6).
        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"]["outcomes"] = [f"garbage-outcome-{index}" for index in range(6)]
        mutation["record_separation"] = [f"garbage-record-{index}" for index in range(6)]
        mutation["temporal_roles"] = [f"garbage-time-{index}" for index in range(5)]
        cases.append(("profile-01-adoption-vocabularies-replaced", {"adoption": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["inputs"] = []
        cases.append(("profile-02-empty-candidate-inputs", {"inventory": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["outputs"] = []
        cases.append(("profile-03-empty-candidate-outputs", {"inventory": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["dependencies"] = []
        cases.append(("profile-04-empty-candidate-dependencies", {"inventory": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["authority_limit"] = "automatic execution authorized"
        cases.append(("profile-05-candidate-authority-inverted", {"inventory": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["non_claims"] = [
            "automatic writeback is implemented",
            "a collective runtime is deployed",
        ]
        cases.append(("profile-06-collective-non-claims-contradict-owner", {"collective": mutation}))

        # Exact malformed shapes from the second re-review (3).
        mutation = copy.deepcopy(self.activation)
        item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")["claimant_assessments"][0]["evaluator_id"] = []
        cases.append(("malformed-01-evaluator-id-list", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["independence_assessment"]["required_dimensions"] = [["nested"]]
        cases.append(("malformed-02-required-dimensions-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["independence_assessment"]["required_dimensions"] = [{"nested": True}]
        cases.append(("malformed-03-required-dimensions-map", {"records": mutation}))

        self.assertEqual(40, len(cases))
        observed = {"rejected": [], "false_pass": [], "traceback": []}
        for name, changes in cases:
            code, output = production_exit(
                changes.get("activation", self.activation),
                changes.get("records", self.records),
                changes.get("inventory", self.inventory),
                changes.get("adoption", self.adoption),
                changes.get("collective", self.collective),
            )
            if code == 1 and "TRACEBACK" not in output:
                observed["rejected"].append(name)
            elif code == 99 or "TRACEBACK" in output:
                observed["traceback"].append(name)
            else:
                observed["false_pass"].append(name)
        self.assertEqual([], observed["false_pass"], observed)
        self.assertEqual([], observed["traceback"], observed)
        self.assertEqual(40, len(observed["rejected"]), observed)

    def test_fourth_review_32_production_entry_regressions_fail_closed(self):
        """Close the third rereview's exact 32 production-entry cases."""
        cases = []

        # Activation authorship and deterministic fixture-summary binding (2).
        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["authorship"] = {
            "mode": "normal",
            "orthing_id": "ORTH-001",
        }
        cases.append((
            "activation-normal-authorship-unrelated-orthing",
            {"activation": mutation},
        ))

        mutation = copy.deepcopy(self.activation)
        outcome = item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")
        outcome["property_findings"] = {
            "satisfied": [],
            "absent": ["theological-proposition", "worldview-bearing-task"],
            "indeterminate": [],
        }
        cases.append((
            "activation-outcome-summary-contradicts-claimant-assessment",
            {"activation": mutation},
        ))

        # Identity, routing, source resolution, target history, and chronology (5).
        mutation = copy.deepcopy(self.records)
        mutation["orthing_events"] = [
            row for row in mutation["orthing_events"]
            if row["event_id"] != "EV-WAKE-001-ROUTE"
        ]
        cases.append(("routing-selected-case-has-no-route-event", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        route = item(mutation["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")
        claimant = item(route["claimant_assessments"], "claimant_id", "claimant-d")
        claimant["claimant_id"] = "SESSION-001"
        route["selected_claimant_id"] = "SESSION-001"
        cases.append(("routing-claimant-collides-with-session-identity", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["subject_records"], "subject_id", "ORTH-002")["source_record_ref"] = "SOURCE-MISSING"
        cases.append(("subject-source-record-unresolved", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")["governing_versions"]["selector"] = "selector-mutated@2"
        cases.append((
            "target-history-digest-ignores-governing-event-mutation",
            {"records": mutation},
        ))

        mutation = copy.deepcopy(self.records)
        assessed = item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ASSESS")
        routed = item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")
        assessed.update(sequence=3, occurred_at="2026-07-20T10:01:00Z")
        routed.update(sequence=4, occurred_at="2026-07-20T10:02:00Z")
        placement = copy.deepcopy(assessed)
        placement.update(
            event_id="EV-WAKE-001-EARLY-PLACEMENT",
            sequence=2,
            event_type="placement_committed",
            occurred_at="2026-07-20T10:00:30Z",
            claim_attempt_id=None,
            orthability_assessment_id=None,
        )
        mutation["orthing_events"].append(placement)
        cases.append(("placement-committed-before-claimant-assessment", {"records": mutation}))

        # Recurrence, reopening, provenance, opportunity, and policy ownership (6).
        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_support_records"], "support_record_id", "SUPPORT-OLD-002")["occurred_at"] = "2026-06-02T18:00:00Z"
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        item(report["supporting_occurrences"], "support_record_id", "SUPPORT-OLD-002")["occurred_at"] = "2026-06-02T18:00:00Z"
        cases.append(("recurrence-support-time-contradicts-subject-t1", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")["recorded_at"] = "2026-07-24T18:00:00Z"
        cases.append(("reopening-uses-future-material-delta", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["source_family_records"], "source_family_id", "corpus-A")["provenance_ref"] = "PROV-MISSING"
        cases.append(("source-family-provenance-unresolved", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["opportunity_records"].append({
            "opportunity_id": "OPP-DUPLICATE-SUBJECT",
            "subject_id": "ORTH-OPP-001",
            "classification": "other",
        })
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["opportunity_ids"].append("OPP-DUPLICATE-SUBJECT")
        report["opportunity_denominator"] = 9
        cases.append(("opportunity-denominator-inflated-by-duplicate-subject", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["opportunity_records"].append({
            "opportunity_id": "OPP-SAME-SUPPORT-COUNTEREXAMPLE",
            "subject_id": "ORTH-NEW-001",
            "classification": "counterexample",
        })
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["counterexample_ids"].append("ORTH-NEW-001")
        report["opportunity_ids"].append("OPP-SAME-SUPPORT-COUNTEREXAMPLE")
        report["opportunity_denominator"] = 9
        report["dependence_dimensions"]["success_counterexample_count"] = 2
        cases.append(("same-subject-is-support-and-counterexample", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["independence_policies"], "rule_id", "independence-rule-v1")["required_dimensions"] = ["session_count"]
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report["independence_assessment"]["required_dimensions"] = ["session_count"]
        cases.append(("independence-policy-registry-weakened-to-session-only", {"records": mutation}))

        # Global writeback IDs, reverse ownership, and chronology (3).
        mutation = copy.deepcopy(self.records)
        proposal = item(mutation["proposals"], "proposal_id", "PROP-MEMORY-001")
        proposal["proposal_id"] = "RR-001"
        assessment = item(mutation["somnic_assessments"], "assessment_id", "SA-ALTERNATIVES-001")
        assessment["proposal_ids"] = [
            "RR-001" if value == "PROP-MEMORY-001" else value
            for value in assessment["proposal_ids"]
        ]
        item(mutation["authorizations"], "authorization_id", "AUTH-FAILED-001")["proposal_id"] = "RR-001"
        item(mutation["applications"], "application_id", "APP-FAILED-001")["proposal_id"] = "RR-001"
        cases.append(("cross-kind-report-and-proposal-id-collision", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        legacy = item(mutation["proposals"], "proposal_id", "PROP-LEGACY-001")
        legacy.update(
            provenance_mode="somnus_grounded_proposal",
            supporting_assessment_id="SA-NO-CHANGE-001",
        )
        cases.append((
            "grounded-proposal-not-owned-by-supporting-assessment",
            {"records": mutation},
        ))

        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["proposed_at"] = "2026-07-21T18:59:30Z"
        cases.append(("proposal-created-before-supporting-assessment", {"records": mutation}))

        # Adoption and inventory contract meaning (6).
        mutation = copy.deepcopy(self.adoption)
        mutation["predecessor_classification"]["relative_granularity"] = "non_reasoning_toy"
        cases.append(("adoption-caricatures-predecessor", {"adoption": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["actuator"]["stages"] = []
        cases.append(("adoption-actuator-stages-erased", {"adoption": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["non_claims"] = [
            "Hermes implementation is repository verified",
            "empirical superiority is established",
            "runtime writeback is implemented",
        ]
        cases.append(("adoption-nonclaims-inverted", {"adoption": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["non_claims"] = [
            "an executable skill",
            "deployed runtime",
            "correctness established",
        ]
        cases.append(("inventory-nonclaims-inverted", {"inventory": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["event_emissions"] = ["rewrites_everything"]
        cases.append(("inventory-event-vocabulary-replaced", {"inventory": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["actuator"]["unknown_nested_key"] = "accepted because the object is open"
        cases.append(("adoption-unknown-nested-key", {"adoption": mutation}))

        # Exact malformed subtree controls (10): six bounded, four tracebacks at RED.
        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["event_type"] = {"nested": True}
        cases.append(("malformed-event-type-map", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["event_type"] = ["nested"]
        cases.append(("event-type-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["intervention_disposition"] = {"nested": True}
        cases.append(("assessment-disposition-map", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["subject_records"], "subject_id", "ORTH-001")["subject_kind"] = ["waking_orthing"]
        cases.append(("subject-kind-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["privacy_source_disposition"] = ["malformed"]
        cases.append(("event-privacy-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["assessment_result"] = ["reasonable"]
        cases.append(("assessment-result-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["applications"], "application_id", "APP-FAILED-001")["status"] = {"nested": True}
        cases.append(("application-status-map", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["opportunity_records"], "opportunity_id", "OPP-OTHER-001")["classification"] = ["other"]
        cases.append(("opportunity-classification-list", {"records": mutation}))

        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["status"] = {"nested": True}
        cases.append(("contract-status-map", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["unknown_nested_key"] = True
        cases.append(("proposal-unknown-nested-key", {"records": mutation}))

        self.assertEqual(32, len(cases))
        observed = {"rejected": [], "false_pass": [], "traceback": []}
        for name, changes in cases:
            code, output = production_exit(
                changes.get("activation", self.activation),
                changes.get("records", self.records),
                changes.get("inventory", self.inventory),
                changes.get("adoption", self.adoption),
                changes.get("collective", self.collective),
            )
            if code == 1 and "TRACEBACK" not in output:
                observed["rejected"].append(name)
            elif code == 99 or "TRACEBACK" in output:
                observed["traceback"].append(name)
            else:
                observed["false_pass"].append(name)
        self.assertEqual([], observed["false_pass"], observed)
        self.assertEqual([], observed["traceback"], observed)
        self.assertEqual(32, len(observed["rejected"]), observed)

    def test_fourth_review_neighboring_semantic_and_shape_controls_fail_closed(self):
        """Cover equivalent owner/time attacks and adjacent scalar/list/map shapes."""
        cases = []

        mutation = copy.deepcopy(self.activation)
        item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")["observed_indicators"] = ["database"]
        cases.append(("activation-summary-indicator-disagrees", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        overlap = item(mutation["fixture_outcomes"], "fixture_id", "ACT-REC-OVERLAP-001")
        overlap["property_findings"]["satisfied"] = ["preserved-target", "sufficient-residual-structure"]
        cases.append(("activation-overlap-summary-is-not-deterministic-union", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["subject_records"], "subject_id", "ORTH-002")["source_record_ref"] = "EV-WAKE-001"
        cases.append(("subject-source-record-resolves-to-wrong-owner", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        report_support = item(report["supporting_occurrences"], "support_record_id", "SUPPORT-OLD-001")
        registry_support = item(mutation["recurrence_support_records"], "support_record_id", "SUPPORT-OLD-001")
        report_support["episode_id"] = "EP-OLD-002"
        registry_support["episode_id"] = "EP-OLD-002"
        cases.append(("recurrence-support-synced-to-wrong-authoritative-episode", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        run["historical_comparator_ids"] = ["ORTH-OLD-001"]
        cases.append((
            "recurrence-support-outside-owning-run-inputs",
            {"records": mutation},
        ))

        mutation = copy.deepcopy(self.records)
        item(mutation["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")["source_ref"] = "recurrence-contract@unowned"
        cases.append(("reopening-material-delta-source-not-in-run-inputs", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["proposed_at"] = "2026-07-21T19:00:01Z"
        cases.append(("proposal-created-at-supporting-assessment-time", {"records": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["source_verification"]["implementation_claims"] = "source and behavior verified"
        cases.append(("adoption-source-verification-inverted", {"adoption": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["intervention_disposition"] = ["investigation"]
        cases.append(("assessment-disposition-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["subject_records"], "subject_id", "ORTH-001")["subject_kind"] = {"kind": "waking_orthing"}
        cases.append(("subject-kind-map", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["governing_versions"] = ["malformed"]
        cases.append(("event-governing-versions-list", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-CONTRACT-001")["status"] = ["proposed"]
        cases.append(("proposal-status-list", {"records": mutation}))

        self.assertEqual(12, len(cases))
        for name, changes in cases:
            with self.subTest(case=name):
                self.assertRejected(**changes)

    def test_fourth_review_exact_normal_authorship_positive_control(self):
        """A normal contract may pass only with its exact typed authoring record."""
        activation = copy.deepcopy(self.activation)
        records = copy.deepcopy(self.records)
        contract = activation["contracts"][0]
        contract["authorship"] = {"mode": "normal", "orthing_id": "ORTH-001"}
        records["contract_authoring_records"] = [{
            "authoring_record_id": "AUTHORING-NORMAL-001",
            "orthing_id": "ORTH-001",
            "contract_id": contract["contract_id"],
            "contract_version": contract["contract_version"],
            "authored_at": "2026-07-20T10:02:00Z",
            "fixture_suite": contract["fixture_suite"],
            "fixture_ids": list(contract["fixture_outcomes"]),
            "immutable": True,
        }]
        code, output = production_exit(
            activation, records, self.inventory, self.adoption, self.collective
        )
        self.assertEqual(0, code, output)
        self.assertIn("TOTAL: 0 failures", output)

    def test_nested_map_and_list_variants_never_reach_hash_operations(self):
        cases = []

        mutation = copy.deepcopy(self.activation)
        mutation["evaluators"][0]["result_vocabulary"] = [{"nested": True}]
        cases.append(("activation-evaluator-vocabulary", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        item(mutation["fixture_outcomes"], "fixture_id", "ACT-OVERLAP-001")["conflict"]["claimant_contracts"] = [{"nested": True}, ["nested"]]
        cases.append(("activation-overlap-contract-set", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")["selected_claimant_id"] = {"nested": True}
        cases.append(("routing-selected-claimant-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")["occurrence_id"] = {"nested": True}
        cases.append(("event-selected-route-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")["target_orthing_ids"] = [{"nested": True}]
        cases.append(("assessment-target-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-CORRECT-DEFECTIVE-001")["proposal_ids"] = [{"nested": True}]
        cases.append(("assessment-proposal-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["output_ids"] = [{"nested": True}]
        cases.append(("run-output-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")["governing_versions"] = [["nested"]]
        cases.append(("run-governing-version-sort", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["counterexample_ids"] = [{"nested": True}]
        cases.append(("report-counterexample-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["fingerprint"]["source_orthing_ids"] = [["nested"]]
        cases.append(("report-fingerprint-source-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["writeback_timeline"][2]["record_ids"] = [{"nested": True}]
        cases.append(("timeline-record-set", {"records": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["candidate_id"] = {"nested": True}
        cases.append(("inventory-candidate-set", {"inventory": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["transclusion"]["gates"] = [{"nested": True}]
        cases.append(("collective-gate-set", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["privacy"]["controls"] = [["nested"]]
        cases.append(("collective-privacy-set", {"collective": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["transclusion"]["levels"][0]["level"] = ["nested"]
        cases.append(("collective-level-key", {"collective": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"]["governing_targets"] = [{"nested": True}]
        cases.append(("adoption-governing-target-set", {"adoption": mutation}))

        mutation = copy.deepcopy(self.activation)
        mutation["authoring_records"][0]["provenance_record_id"] = []
        cases.append(("activation-authoring-record-key", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        mutation["contracts"][0]["authorship"] = {"mode": "normal", "orthing_id": []}
        cases.append(("activation-normal-authoring-orthing-key", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["identity_registry"][0]["identity_id"] = []
        cases.append(("identity-registry-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001")["provenance_record_id"] = []
        cases.append(("event-provenance-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["evidence_state_ids"] = [["nested"]]
        cases.append(("meta-evidence-state-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["meta_orthability_assessments"][0]["activation_contract_id"] = []
        cases.append(("meta-contract-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-CLOSED-001")["prior_assessment_ids"] = [{"nested": True}]
        cases.append(("assessment-prior-set", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-CLOSED-001")["t2_configuration"] = []
        cases.append(("assessment-t2-map", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["recurrence_support_records"][0]["support_record_id"] = []
        cases.append(("support-registry-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["supporting_occurrences"][0]["episode_id"] = []
        cases.append(("support-episode-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["opportunity_records"][0]["opportunity_id"] = []
        cases.append(("opportunity-registry-key", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")["independence_assessment"]["rule_id"] = []
        cases.append(("independence-policy-key", {"records": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"][0]["authority_boundary"] = []
        cases.append(("candidate-authority-map", {"inventory": mutation}))

        mutation = copy.deepcopy(self.collective)
        mutation["non_claims"] = []
        cases.append(("collective-non-claims-map", {"collective": mutation}))

        for name, changes in cases:
            with self.subTest(case=name):
                self.assertRejected(**changes)

    def test_fifth_review_23_ownership_and_meaning_regressions_fail_closed(self):
        """Close the fourth rereview's exact I01-I23 production-entry cases."""
        cases = []

        def recompute_target_history_digests(records, target_ids):
            subject_by_id = {
                row["subject_id"]: row for row in records["subject_records"]
            }
            source_by_id = {
                row["source_record_id"]: row for row in records["source_records"]
            }
            event_by_id = {
                row["event_id"]: row for row in records["orthing_events"]
            }
            assessment_by_id = {
                row["assessment_id"]: row for row in records["somnic_assessments"]
            }
            target_ids = set(target_ids)
            for assessment in records["somnic_assessments"]:
                targets = set(assessment["target_orthing_ids"])
                if not targets & target_ids:
                    continue
                payload = []
                for target in sorted(targets):
                    subject = subject_by_id[target]
                    source_ref = subject["source_record_ref"]
                    source = (
                        source_by_id.get(source_ref)
                        or event_by_id.get(source_ref)
                        or assessment_by_id.get(source_ref)
                    )
                    history = sorted(
                        [
                            event
                            for event in records["orthing_events"]
                            if event.get("orthing_id") == target
                        ],
                        key=lambda event: (
                            event.get("sequence")
                            if isinstance(event.get("sequence"), int)
                            else 0,
                            event.get("event_id")
                            if isinstance(event.get("event_id"), str)
                            else "",
                        ),
                    )
                    payload.append({
                        "subject": subject,
                        "source_record": source,
                        "event_history": history,
                    })
                encoded = json.dumps(
                    payload, sort_keys=True, separators=(",", ":")
                ).encode("utf-8")
                assessment["target_history_digest"] = hashlib.sha256(encoded).hexdigest()

        mutation = copy.deepcopy(self.activation)
        fixture = item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")
        fixture["observed_indicators"] = ["undeclared-boundary-token"]
        fixture["claimant_assessments"][0]["observed_indicators"] = [
            "undeclared-boundary-token"
        ]
        cases.append(("I01", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        fixture = item(mutation["fixture_outcomes"], "fixture_id", "ACT-OVERLAP-001")
        fixture["conflict"]["claimant_contracts"].append("phantom-contract@9.9.9")
        cases.append(("I02", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        fixture = item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")
        fixture["claimant_assessments"][0]["result"] = {"nested": ["applicable"]}
        cases.append(("I03", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")[
            "fixture_class"
        ] = ["positive"]
        cases.append(("I04", {"activation": mutation}))

        mutation = copy.deepcopy(self.activation)
        item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")[
            "claimant_assessments"
        ][0]["result"] = 7
        cases.append(("I05", {"activation": mutation}))

        mutation = copy.deepcopy(self.records)
        event = item(mutation["orthing_events"], "event_id", "EV-WAKE-002-ASSESS")
        event.update(claim_attempt_id="CA-001", orthability_assessment_id="OA-001")
        cases.append(("I06", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        event = item(mutation["orthing_events"], "event_id", "EV-WAKE-002")
        event.update(claim_attempt_id="CA-001", orthability_assessment_id="OA-001")
        cases.append(("I07", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        mutation["claimant_routing_cases"].append({
            "case_id": "ROUTE-GHOST-001",
            "occurrence_id": "OCC-GHOST-001",
            "claimant_assessments": [{
                "claim_attempt_id": "CA-001",
                "orthability_assessment_id": "OA-001",
                "claimant_id": "claimant-c",
                "result": "indeterminate",
            }],
            "selected_claimant_id": None,
            "route_status": "deferred",
            "retained_residual_claimants": ["claimant-c"],
            "retained_inapplicable_claimants": [],
        })
        cases.append(("I08", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        route = item(mutation["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")
        assessment = item(route["claimant_assessments"], "claimant_id", "claimant-d")
        assessment["claimant_id"] = "theological-claimant"
        route["selected_claimant_id"] = "theological-claimant"
        cases.append(("I09", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")[
            "governing_versions"
        ]["selector"] = "selector-hindsight-rewrite@7"
        recompute_target_history_digests(mutation, {"ORTH-001"})
        cases.append(("I10", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        future_event = copy.deepcopy(
            item(mutation["orthing_events"], "event_id", "EV-WAKE-001-ROUTE")
        )
        future_event.update(
            event_id="EV-WAKE-001-FUTURE",
            sequence=4,
            event_type="residual_recorded",
            occurred_at="2026-07-24T10:00:00Z",
        )
        mutation["orthing_events"].append(future_event)
        recompute_target_history_digests(mutation, {"ORTH-001"})
        cases.append(("I11", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")
        item(mutation["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")[
            "recorded_at"
        ] = run["started_at"]
        cases.append(("I12", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnic_assessments"], "assessment_id", "SA-REOPENED-001")[
            "prior_assessment_ids"
        ] = ["SA-NO-CHANGE-001"]
        cases.append(("I13", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")[
            "historical_comparator_ids"
        ].append("ORTH-SUCCESS-001")
        cases.append(("I14", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        run = item(mutation["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")
        run["anchor_subject_ids"] = ["ORTH-NEW-002"]
        run["reopens_subject_ids"] = ["ORTH-NEW-002"]
        cases.append(("I15", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["material_deltas"], "material_delta_id", "DELTA-CONTRACT-0.1.1")[
            "source_ref"
        ] = "analysis-retro@1"
        cases.append(("I16", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["authorizations"], "authorization_id", "AUTH-FAILED-001")[
            "decision"
        ] = "rejected"
        cases.append(("I17", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["proposals"], "proposal_id", "PROP-MEMORY-001")[
            "status"
        ] = "rejected"
        cases.append(("I18", {"records": mutation}))

        mutation = copy.deepcopy(self.records)
        item(mutation["successor_states"], "successor_state_id", "SUCCESSOR-MEMORY-001")[
            "created_at"
        ] = "2026-07-21T18:00:00Z"
        cases.append(("I19", {"records": mutation}))

        mutation = copy.deepcopy(self.inventory)
        item(mutation["candidates"], "candidate_id", "guarded-writeback-actuator")[
            "downstream_owner"
        ] = "orthemology built-in deployed writeback engine"
        cases.append(("I20", {"inventory": mutation}))

        mutation = copy.deepcopy(self.inventory)
        item(mutation["candidates"], "candidate_id", "orthing-dream")[
            "authority_limit"
        ] = (
            "may schedule, execute, promote, close, and mutate governance after an "
            "operator request"
        )
        cases.append(("I21", {"inventory": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["actuator"]["stages"] = list(reversed(mutation["actuator"]["stages"]))
        cases.append(("I22", {"adoption": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"]["governing_targets"].append(
            "autonomous_self_patch_runtime"
        )
        cases.append(("I23", {"adoption": mutation}))

        self.assertEqual(23, len(cases))
        observed = {"rejected": [], "false_pass": [], "traceback": []}
        for name, changes in cases:
            code, output = production_exit(
                changes.get("activation", self.activation),
                changes.get("records", self.records),
                changes.get("inventory", self.inventory),
                changes.get("adoption", self.adoption),
                changes.get("collective", self.collective),
            )
            if code == 1 and "TRACEBACK" not in output:
                observed["rejected"].append(name)
            elif code == 99 or "TRACEBACK" in output:
                observed["traceback"].append(name)
            else:
                observed["false_pass"].append(name)
        self.assertEqual([], observed["false_pass"], observed)
        self.assertEqual([], observed["traceback"], observed)
        self.assertEqual(23, len(observed["rejected"]), observed)

    def test_fifth_review_meaning_preserving_controls_are_accepted(self):
        """Retain all C01-C07 controls, including declared subsets and neutral prose."""
        cases = [("C01", {})]

        mutation = copy.deepcopy(self.activation)
        fixture = item(mutation["fixture_outcomes"], "fixture_id", "ACT-POS-001")
        fixture["observed_indicators"] = ["tawhid"]
        fixture["claimant_assessments"][0]["observed_indicators"] = ["tawhid"]
        cases.append(("C02", {"activation": mutation}))

        mutation = copy.deepcopy(self.inventory)
        mutation["candidates"] = list(reversed(mutation["candidates"]))
        cases.append(("C03", {"inventory": mutation}))

        mutation = copy.deepcopy(self.inventory)
        candidate = item(mutation["candidates"], "candidate_id", "orthing-ledger")
        candidate["event_emissions"] = list(reversed(candidate["event_emissions"]))
        cases.append(("C04", {"inventory": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["subsumption"]["ordinary_targets"] = list(
            reversed(mutation["subsumption"]["ordinary_targets"])
        )
        cases.append(("C05", {"adoption": mutation}))

        mutation = copy.deepcopy(self.adoption)
        mutation["predecessor_characterization"] = (
            "a coarser or more implicit orthing architecture focused on source "
            "interpretation, proposal generation, destination selection, and safe writeback"
        )
        cases.append(("C06", {"adoption": mutation}))

        mutation = copy.deepcopy(self.records)
        old_support_id = "SUPPORT-OLD-001"
        new_support_id = "SUPPORT-HISTORICAL-A"
        item(mutation["recurrence_support_records"], "support_record_id", old_support_id)[
            "support_record_id"
        ] = new_support_id
        report = item(mutation["recurrence_reports"], "recurrence_report_id", "RR-001")
        item(report["supporting_occurrences"], "support_record_id", old_support_id)[
            "support_record_id"
        ] = new_support_id
        cases.append(("C07", {"records": mutation}))

        observed = []
        for name, changes in cases:
            code, output = production_exit(
                changes.get("activation", self.activation),
                changes.get("records", self.records),
                changes.get("inventory", self.inventory),
                changes.get("adoption", self.adoption),
                changes.get("collective", self.collective),
            )
            if code != 0:
                observed.append((name, code, output))
        self.assertEqual([], observed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
