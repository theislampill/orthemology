#!/usr/bin/env python3
"""Retained production-entry regressions from the Task 4 closure review."""
from __future__ import annotations

import copy
import unittest

from tests import test_task4_postfinal_approval_regressions as retained


def item(rows, key, value):
    return next(row for row in rows if row.get(key) == value)


def make_reverted(
    documents,
    *,
    provenance="REVERT-PROVENANCE-CLOSURE-001",
    reverted_at="2026-07-22T20:05:00.000001Z",
):
    records = documents["records"]
    application = item(records["applications"], "application_id", "APP-APPLIED-001")
    application["status"] = "reverted"
    application["revert_transition"] = {
        "revert_transition_id": "REVERT-CLOSURE-001",
        "application_id": "APP-APPLIED-001",
        "prior_successor_state_id": "SUCCESSOR-CONTRACT-001",
        "reverted_at": reverted_at,
        "restoration_disposition": "held_for_governance",
        "revert_provenance_ref": provenance,
        "immutable": True,
    }
    item(
        records["outcome_evaluations"],
        "outcome_evaluation_id",
        "OUTCOME-001",
    )["result"] = "harmful"


def cases():
    rows = []

    def invalid(case_id, mutate):
        rows.append((case_id, "invalid", mutate))

    def control(case_id, mutate):
        rows.append((case_id, "control", mutate))

    invalid(
        "I01",
        lambda d: d.update(
            decision=d["decision"]
            + "\n### Activation and claimant routing\n\nA second real owner heading.\n"
        ),
    )

    def malformed_version_identity(documents):
        versions = documents["activation"]["version_transition_authority"][
            "accepted_versions"
        ]
        changed = copy.deepcopy(versions[0])
        changed["artifact_version"] = {"nested": ["1.0.0"]}
        versions[0] = changed

    invalid("I02", malformed_version_identity)
    invalid(
        "I03",
        lambda d: d["activation"]["version_transition_authority"][
            "accepted_versions"
        ].append(
            copy.deepcopy(
                d["activation"]["version_transition_authority"][
                    "accepted_versions"
                ][0]
            )
        ),
    )
    invalid(
        "I04",
        lambda d: d["records"]["source_family_records"].append(
            {
                "source_family_id": "unused-family-closure",
                "provenance_ref": "MISSING-PROVENANCE",
            }
        ),
    )
    invalid(
        "I05",
        lambda d: d["records"]["authorization_rule_records"][0].update(
            owner_ref=(
                "docs/decisions/0035-somnic-orthing-and-activation-contracts.md"
                "#activation-and-claimant-routing"
            )
        ),
    )
    invalid(
        "I06",
        lambda d: d["records"]["authorization_rule_records"][0].update(
            simultaneous_decisions={"policy": "prohibited"}
        ),
    )
    invalid(
        "I07",
        lambda d: make_reverted(
            d, provenance="MISSING-REVERT-PROVENANCE-OWNER"
        ),
    )

    def duplicate_candidate(documents):
        candidate = item(
            documents["inventory"]["candidates"],
            "candidate_id",
            "guarded-writeback-actuator",
        )
        documents["inventory"]["candidates"].append(copy.deepcopy(candidate))

    invalid("I08", duplicate_candidate)

    def swap_candidate_outputs(documents):
        candidates = documents["inventory"]["candidates"]
        left = item(candidates, "candidate_id", "somnus-export")
        right = item(candidates, "candidate_id", "somnus-import")
        left["outputs"], right["outputs"] = right["outputs"], left["outputs"]

    invalid("I09", swap_candidate_outputs)

    def malformed_candidate_owner(documents):
        candidate = item(
            documents["inventory"]["candidates"],
            "candidate_id",
            "guarded-writeback-actuator",
        )
        candidate["downstream_owner"]["owner_role"] = {
            "nested": ["writeback runtime owner"]
        }

    invalid("I10", malformed_candidate_owner)

    def malformed_revert_time(documents):
        make_reverted(documents)
        item(
            documents["records"]["applications"],
            "application_id",
            "APP-APPLIED-001",
        )["revert_transition"]["reverted_at"] = {
            "nested": ["2026-07-22T20:05:00Z"]
        }

    invalid("I11", malformed_revert_time)
    invalid(
        "I12",
        lambda d: make_reverted(d, reverted_at="2026-07-22T19:05:00-00:00"),
    )

    control("C01", lambda d: None)
    control(
        "C02",
        lambda d: d.update(
            decision=d["decision"]
            + "\n```text\n### Activation and claimant routing\n```\n"
        ),
    )
    control(
        "C03",
        lambda d: d["records"]["source_family_records"].append(
            {
                "source_family_id": "unused-family-owned",
                "provenance_ref": "PROV-LIVE-001",
            }
        ),
    )
    control(
        "C04",
        lambda d: [
            row.update(outputs=list(reversed(row["outputs"])))
            for row in d["inventory"]["candidates"]
        ],
    )
    control(
        "C05",
        lambda d: [
            row.update(dependencies=list(reversed(row["dependencies"])))
            for row in d["inventory"]["candidates"]
        ],
    )
    control("C06", lambda d: make_reverted(d))
    control("C07", lambda d: d["records"]["authorizations"].reverse())
    control(
        "C08",
        lambda d: d.update(
            decision=d["decision"].replace(
                "### Activation and claimant routing",
                "### **Activation and claimant routing**",
                1,
            )
        ),
    )
    return rows


class Task4ClosureApprovalRegressionTests(unittest.TestCase):
    def test_closure_review_cases(self):
        source = retained.baseline()
        review_cases = cases()
        self.assertEqual(20, len(review_cases))
        for case_id, kind, mutate in review_cases:
            with self.subTest(case_id=case_id, kind=kind):
                documents = copy.deepcopy(source)
                mutate(documents)
                actual_exit, output = retained.production.production_exit(documents)
                self.assertNotEqual(99, actual_exit, f"{case_id} traceback: {output}")
                self.assertNotIn("TRACEBACK", output, f"{case_id} traceback: {output}")
                self.assertEqual(
                    1 if kind == "invalid" else 0,
                    actual_exit,
                    f"{case_id} {kind} got {actual_exit}: {output}",
                )

    def test_neighboring_nested_identity_and_owner_values_fail_closed(self):
        source = retained.baseline()

        def nested_version_field(field, value):
            def mutate(documents):
                documents["activation"]["version_transition_authority"][
                    "accepted_versions"
                ][0][field] = value

            return mutate

        def nested_owner_role(value):
            def mutate(documents):
                item(
                    documents["inventory"]["candidates"],
                    "candidate_id",
                    "guarded-writeback-actuator",
                )["downstream_owner"]["owner_role"] = value

            return mutate

        mutations = (
            ("artifact-kind-mapping", nested_version_field("artifact_kind", {"nested": True})),
            ("artifact-id-list", nested_version_field("artifact_id", ["database-schema-activation"])),
            ("owner-role-list", nested_owner_role(["writeback runtime owner"])),
            ("owner-role-mapping", nested_owner_role({"role": "writeback runtime owner"})),
        )
        for case_id, mutate in mutations:
            with self.subTest(case_id=case_id):
                documents = copy.deepcopy(source)
                mutate(documents)
                actual_exit, output = retained.production.production_exit(documents)
                self.assertNotEqual(99, actual_exit, f"{case_id} traceback: {output}")
                self.assertNotIn("TRACEBACK", output, f"{case_id} traceback: {output}")
                self.assertEqual(1, actual_exit, f"{case_id} got {actual_exit}: {output}")

    def test_revert_provenance_registry_accepts_authorized_immutable_owner(self):
        documents = retained.baseline()
        documents["records"]["revert_provenance_records"] = [
            {
                "revert_provenance_ref": "REVERT-PROVENANCE-CLOSURE-001",
                "application_id": "APP-APPLIED-001",
                "authorization_id": "AUTH-INDEPENDENT-001",
                "source_revision": "task4-revert-fixture-v1",
                "immutable": True,
            }
        ]
        make_reverted(documents)
        actual_exit, output = retained.production.production_exit(documents)
        self.assertEqual(0, actual_exit, output)

    def test_revert_provenance_owner_must_match_application_authorization(self):
        documents = retained.baseline()
        owner = item(
            documents["records"]["revert_provenance_records"],
            "revert_provenance_ref",
            "REVERT-PROVENANCE-CLOSURE-001",
        )
        owner["authorization_id"] = "AUTH-FAILED-001"
        make_reverted(documents)
        actual_exit, output = retained.production.production_exit(documents)
        self.assertNotEqual(99, actual_exit, output)
        self.assertEqual(1, actual_exit, output)


if __name__ == "__main__":
    unittest.main()
