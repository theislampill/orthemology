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
        "somnus-record-fixtures.schema.json",
        "somnus-claim-status.schema.json",
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
        required = [SCRIPT, ACTIVATION, RECORDS, INVENTORY, ADOPTION, COLLECTIVE, DECISION, *SCHEMAS]
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

        for index, changes in enumerate(cases, 1):
            with self.subTest(variant=index):
                self.assertRejected(**changes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
