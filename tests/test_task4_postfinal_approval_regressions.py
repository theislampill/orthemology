#!/usr/bin/env python3
"""Retained production-entry regressions from the Task 4 post-final review."""
from __future__ import annotations

import copy
import unittest

from tests import task4_parallel_a_regressions as production
from tests import task4_parallel_b_regressions as history_helpers


def item(rows, key, value):
    return next(row for row in rows if row.get(key) == value)


def baseline():
    return {
        "activation": production.load_yaml(production.ACTIVATION),
        "records": production.load_yaml(production.RECORDS),
        "history": production.load_yaml(production.HISTORY),
        "inventory": production.load_yaml(production.INVENTORY),
        "adoption": production.load_yaml(production.ADOPTION),
        "collective": production.load_yaml(production.COLLECTIVE),
        "decision": production.DECISION.read_text(encoding="utf-8"),
    }


def refresh_history(documents):
    history_helpers.recompute_all_chains(documents["records"], documents["history"])
    history_helpers.recompute_all_assessment_digests(
        documents["records"], documents["history"]
    )


def rename_heading(documents, old, new):
    documents["decision"] = documents["decision"].replace(old, new, 1)


def unregistered_source_family(documents):
    source = item(
        documents["records"]["source_records"],
        "subject_id",
        "ORTH-NO-CHANGE-001",
    )
    source["source_family"] = "unregistered-family"
    refresh_history(documents)


def append_corpus(documents, owner_ref):
    documents["records"]["reference_corpus_records"].append(
        {
            "reference_corpus_revision": "UNUSED-REV-001",
            "owner_ref": owner_ref,
            "immutable": True,
        }
    )


def unowned_authorization_rule(documents):
    item(
        documents["records"]["authorizations"],
        "authorization_id",
        "AUTH-INDEPENDENT-001",
    )["authorization_rule_ref"] = "unregistered-governance-rule@77"


def conflicting_authorization(documents):
    records = documents["records"]
    original = item(records["authorizations"], "authorization_id", "AUTH-INDEPENDENT-001")
    competing = copy.deepcopy(original)
    competing.update(
        authorization_id="AUTH-CROSS-RULE-CONFLICT-001",
        authorization_rule_ref="independent-governance-rule@2",
        decision="rejected",
        reason="a second rule rejects at the same effective instant",
    )
    records["authorizations"].append(competing)
    item(records["somnic_assessments"], "assessment_id", "SA-CORRECT-DEFECTIVE-001")[
        "authorization_refs"
    ].append(competing["authorization_id"])


def unproved_revert(documents):
    records = documents["records"]
    item(records["applications"], "application_id", "APP-APPLIED-001")["status"] = "reverted"
    item(records["outcome_evaluations"], "outcome_evaluation_id", "OUTCOME-001")[
        "result"
    ] = "harmful"


def change_candidate(documents, field, value):
    item(
        documents["inventory"]["candidates"],
        "candidate_id",
        "guarded-writeback-actuator",
    )[field] = value


CASES = [
    ("I01", "invalid", lambda d: rename_heading(d, "### Activation and claimant routing", "### Claimant routing without version authority")),
    ("I02", "invalid", lambda d: rename_heading(d, "### Frontier, recurrence, and retrospective loci", "### Recurrence examples without corpus authority")),
    ("I03", "invalid", unregistered_source_family),
    ("I04", "invalid", lambda d: append_corpus(d, "missing-authority")),
    ("I05", "invalid", unowned_authorization_rule),
    ("I06", "invalid", conflicting_authorization),
    ("I07", "invalid", unproved_revert),
    ("I08", "invalid", lambda d: change_candidate(d, "downstream_owner", {"ownership_scope": "external/downstream", "owner_role": "transport owner", "local_runtime_ownership": "prohibited"})),
    ("I09", "invalid", lambda d: change_candidate(d, "inputs", ["operator command that directly authorizes and executes mutation"])),
    ("I10", "invalid", lambda d: change_candidate(d, "layer", "live-routing")),
    ("C01", "control", lambda d: d["activation"]["version_transition_authority"]["accepted_versions"].reverse()),
    ("C02", "control", lambda d: d["adoption"].update(predecessor_characterization="a coarser or more implicit orthing architecture focused on source interpretation, proposal generation, destination selection, and safe writeback")),
    ("C03", "control", lambda d: d["inventory"]["candidates"].reverse()),
    ("C04", "control", lambda d: d["records"]["source_records"].reverse()),
    ("C05", "control", lambda d: append_corpus(d, "docs/decisions/0035-somnic-orthing-and-activation-contracts.md#frontier-recurrence-and-retrospective-loci")),
    ("C06", "control", lambda d: item(d["records"]["outcome_evaluations"], "outcome_evaluation_id", "OUTCOME-001").update(result="undetermined")),
]


class Task4PostFinalApprovalRegressionTests(unittest.TestCase):
    def test_postfinal_review_cases(self):
        source = baseline()
        self.assertEqual(16, len(CASES))
        for case_id, kind, mutate in CASES:
            with self.subTest(case_id=case_id, kind=kind):
                documents = copy.deepcopy(source)
                mutate(documents)
                actual_exit, output = production.production_exit(documents)
                self.assertNotEqual(99, actual_exit, f"{case_id} traceback: {output}")
                self.assertNotIn("TRACEBACK", output, f"{case_id} traceback: {output}")
                self.assertEqual(
                    1 if kind == "invalid" else 0,
                    actual_exit,
                    f"{case_id} {kind} got {actual_exit}: {output}",
                )

    def test_well_formed_later_revert_control(self):
        documents = baseline()
        records = documents["records"]
        application = item(
            records["applications"], "application_id", "APP-APPLIED-001"
        )
        application["status"] = "reverted"
        application["revert_transition"] = {
            "revert_transition_id": "REVERT-APP-APPLIED-001",
            "application_id": "APP-APPLIED-001",
            "prior_successor_state_id": "SUCCESSOR-CONTRACT-001",
            "reverted_at": "2026-07-22T20:05:00Z",
            "restoration_disposition": "held_for_governance",
            "revert_provenance_ref": "REVERT-PROVENANCE-001",
            "immutable": True,
        }
        item(
            records["outcome_evaluations"],
            "outcome_evaluation_id",
            "OUTCOME-001",
        )["result"] = "harmful"
        actual_exit, output = production.production_exit(documents)
        self.assertEqual(0, actual_exit, output)


if __name__ == "__main__":
    unittest.main()
