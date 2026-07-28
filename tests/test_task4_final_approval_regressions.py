#!/usr/bin/env python3
"""Retained production-entry regressions from the Task 4 final review."""
from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tests import task4_parallel_b_regressions as history_helpers
from tests import task4_parallel_c_regressions as production


def item(rows, key, value):
    return next(row for row in rows if row.get(key) == value)


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def fixture_digest(outcome):
    projection = {
        key: value
        for key, value in outcome.items()
        if key not in {"occurrence", "observed_indicators", "observed_exclusions"}
    }
    projection["claimant_assessments"] = [
        {
            key: value
            for key, value in assessment.items()
            if key not in {"observed_indicators", "observed_exclusions"}
        }
        for assessment in outcome.get("claimant_assessments", [])
        if isinstance(assessment, dict)
    ]
    return digest(projection)


def refresh_activation_authorship(documents):
    activation = documents["activation"]
    for record in activation["authoring_records"]:
        contract = next(
            row
            for row in activation["contracts"]
            if row["authorship"]["provenance_record_id"]
            == record["provenance_record_id"]
        )
        record["selected_contract_ref"] = "%s@%s" % (
            contract["contract_id"],
            contract["contract_version"],
        )
        record["contract_body_digest"] = digest(contract)
        record["fixture_semantic_digests"] = {
            fixture_id: fixture_digest(
                item(activation["fixture_outcomes"], "fixture_id", fixture_id)
            )
            for fixture_id in sorted(record["fixture_ids"])
        }


def rewrite_contract_version_history(documents):
    activation = documents["activation"]
    records = documents["records"]
    contract = item(
        activation["contracts"], "contract_id", "recurrence-meta-assessability"
    )
    old_version = contract["contract_version"]
    new_version = "9.9.9"
    contract["contract_version"] = new_version
    for outcome in activation["fixture_outcomes"]:
        for assessment in outcome["claimant_assessments"]:
            if assessment["activation_contract_id"] == contract["contract_id"]:
                assessment["activation_contract_version"] = new_version
        conflict = outcome.get("conflict")
        if isinstance(conflict, dict):
            old_ref = "%s@%s" % (contract["contract_id"], old_version)
            new_ref = "%s@%s" % (contract["contract_id"], new_version)
            conflict["claimant_contracts"] = [
                new_ref if ref == old_ref else ref
                for ref in conflict["claimant_contracts"]
            ]
    for assessment in records["meta_orthability_assessments"]:
        if assessment["activation_contract_id"] == contract["contract_id"]:
            assessment["activation_contract_version"] = new_version
    refresh_activation_authorship(documents)


def rewrite_evaluator_version_history(documents):
    activation = documents["activation"]
    records = documents["records"]
    evaluator = activation["evaluators"][0]
    old_version = evaluator["evaluator_version"]
    new_version = "9.9.9"
    evaluator["evaluator_version"] = new_version
    for outcome in activation["fixture_outcomes"]:
        for assessment in outcome["claimant_assessments"]:
            if assessment["evaluator_id"] == evaluator["evaluator_id"]:
                assessment["evaluator_version"] = new_version
    for assessment in records["meta_orthability_assessments"]:
        if assessment["orthability_evaluator_id"] == evaluator["evaluator_id"]:
            assessment["orthability_evaluator_version"] = new_version
    old_ref = "%s@%s" % (evaluator["evaluator_id"], old_version)
    new_ref = "%s@%s" % (evaluator["evaluator_id"], new_version)
    for event in records["orthing_events"]:
        versions = event.get("governing_versions", {})
        if versions.get("orthability_evaluator") == old_ref:
            versions["orthability_evaluator"] = new_ref
    refresh_activation_authorship(documents)
    history_helpers.recompute_all_chains(records, documents["history"])
    history_helpers.recompute_all_assessment_digests(records, documents["history"])


def duplicate_conflicting_subject_source(documents):
    records = documents["records"]
    source = copy.deepcopy(records["source_records"][0])
    source["source_record_id"] = "fixture-subject-ORTH-NEW-001-conflict"
    source["actor_id"] = "actor-local-2"
    records["source_records"].append(source)


def add_type_swapped_source_record(documents):
    records = documents["records"]
    source = copy.deepcopy(records["source_records"][0])
    source["source_record_id"] = "fixture-source-type-conflict"
    source["session_id"] = "EP-001"
    source["episode_id"] = "SESSION-001"
    records["source_records"].append(source)


def detach_corpus_owner(documents):
    corpus = item(
        documents["records"]["reference_corpus_records"],
        "reference_corpus_revision",
        "LEDGER-REV-001",
    )
    corpus["owner_ref"] = "unresolved-corpus-owner"


def add_equal_time_authorization_tie(documents):
    records = documents["records"]
    original = item(
        records["authorizations"], "authorization_id", "AUTH-INDEPENDENT-001"
    )
    competing = copy.deepcopy(original)
    competing["authorization_id"] = "AUTH-INDEPENDENT-TIE-002"
    competing["reason"] = "equally timed independent authorization"
    records["authorizations"].append(competing)
    item(
        records["somnic_assessments"],
        "assessment_id",
        "SA-CORRECT-DEFECTIVE-001",
    )["authorization_refs"].append(competing["authorization_id"])
    item(records["writeback_timeline"], "time_role", "t3")["record_ids"].append(
        competing["authorization_id"]
    )


def mark_applied_outcome_harmful(documents):
    item(
        documents["records"]["outcome_evaluations"],
        "outcome_evaluation_id",
        "OUTCOME-001",
    )["result"] = "harmful"


def contradict_inventory_owner(documents):
    candidate = item(
        documents["inventory"]["candidates"], "candidate_id", "somnus-export"
    )
    candidate["downstream_owner"]["owner_role"] = (
        "local automatic executor and mutation owner"
    )


def contradict_predecessor_reasoning(documents):
    documents["adoption"]["predecessor_characterization"] = (
        "incapable of inference or interpretation despite emitting destination choices"
    )


def claim_automatic_residual_mutation(documents):
    candidate = item(
        documents["inventory"]["candidates"],
        "candidate_id",
        "residual-recurrence-somnic",
    )
    candidate["residual_behavior"] = (
        "automatically applies the inferred mutation and closes the source history"
    )


def malformed_nested_outcome(documents):
    item(
        documents["records"]["outcome_evaluations"],
        "outcome_evaluation_id",
        "OUTCOME-001",
    )["result"] = {"nested": "effective"}


def malformed_nested_checkpoint(documents):
    item(
        documents["history"]["checkpoints"],
        "checkpoint_id",
        "CP-ORTH-001-T2",
    )["predecessor_checkpoint_digest"] = {"nested": None}


def reorder_evaluator_vocabulary(documents):
    evaluator = documents["activation"]["evaluators"][0]
    evaluator["result_vocabulary"] = list(reversed(evaluator["result_vocabulary"]))


def reorder_identity_registry(documents):
    documents["records"]["identity_registry"] = list(
        reversed(documents["records"]["identity_registry"])
    )


def reorder_collective_dimensions(documents):
    dimensions = documents["collective"]["dependence_dimensions"]
    documents["collective"]["dependence_dimensions"] = list(reversed(dimensions))


def record_effective_applied_outcome(documents):
    item(
        documents["records"]["outcome_evaluations"],
        "outcome_evaluation_id",
        "OUTCOME-001",
    )["result"] = "effective"


def add_rejected_unapplied_authorization(documents):
    records = documents["records"]
    original = item(
        records["authorizations"], "authorization_id", "AUTH-INDEPENDENT-001"
    )
    rejected = copy.deepcopy(original)
    rejected.update(
        authorization_id="AUTH-SKILL-REJECTED-NEW",
        proposal_id="PROP-SKILL-001",
        decision="rejected",
        decided_at="2026-07-21T19:02:30Z",
        reason="independent rejection without application",
    )
    records["authorizations"].append(rejected)
    item(
        records["somnic_assessments"], "assessment_id", "SA-ALTERNATIVES-001"
    )["authorization_refs"].append(rejected["authorization_id"])


def reorder_inventory_inputs(documents):
    candidate = item(
        documents["inventory"]["candidates"], "candidate_id", "somnus-import"
    )
    candidate["inputs"] = list(reversed(candidate["inputs"]))


def neutral_owner_wording(documents):
    candidate = item(
        documents["inventory"]["candidates"], "candidate_id", "somnus-export"
    )
    candidate["downstream_owner"]["owner_role"] = (
        "external bounded-record custody operator"
    )


CASES = [
    ("I01", "invalid", rewrite_contract_version_history),
    ("I02", "invalid", rewrite_evaluator_version_history),
    ("I03", "invalid", duplicate_conflicting_subject_source),
    ("I04", "invalid", add_type_swapped_source_record),
    ("I05", "invalid", detach_corpus_owner),
    ("I06", "invalid", add_equal_time_authorization_tie),
    ("I07", "invalid", mark_applied_outcome_harmful),
    ("I08", "invalid", contradict_inventory_owner),
    ("I09", "invalid", contradict_predecessor_reasoning),
    ("I10", "invalid", claim_automatic_residual_mutation),
    ("I11", "invalid", malformed_nested_outcome),
    ("I12", "invalid", malformed_nested_checkpoint),
    ("C01", "control", reorder_evaluator_vocabulary),
    ("C02", "control", reorder_identity_registry),
    ("C03", "control", reorder_collective_dimensions),
    ("C04", "control", record_effective_applied_outcome),
    ("C05", "control", add_rejected_unapplied_authorization),
    ("C06", "control", reorder_inventory_inputs),
    ("C07", "control", neutral_owner_wording),
]


class Task4FinalApprovalRegressionTests(unittest.TestCase):
    def test_final_review_cases(self):
        baseline = production.load_base()
        self.assertEqual(19, len(CASES))
        for case_id, kind, mutate in CASES:
            with self.subTest(case_id=case_id, kind=kind):
                documents = copy.deepcopy(baseline)
                mutate(documents)
                actual_exit, output = production.production_exit(documents)
                self.assertNotEqual(99, actual_exit, f"{case_id} traceback: {output}")
                self.assertNotIn("TRACEBACK", output, f"{case_id} traceback: {output}")
                self.assertEqual(
                    1 if kind == "invalid" else 0,
                    actual_exit,
                    f"{case_id} {kind} got {actual_exit}: {output}",
                )


if __name__ == "__main__":
    unittest.main()
