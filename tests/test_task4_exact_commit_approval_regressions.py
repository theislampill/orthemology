#!/usr/bin/env python3
"""Retained production-entry regressions from the exact-commit Task 4 review."""
from __future__ import annotations

import copy
import unittest

from tests import test_task4_postfinal_approval_regressions as retained
from tests.test_task4_closure_approval_regressions import item, make_reverted


def replace_heading(documents, replacement):
    documents["decision"] = documents["decision"].replace(
        "### Activation and claimant routing", replacement, 1
    )


def failed_application_revert_owner(documents):
    owner = item(
        documents["records"]["revert_provenance_records"],
        "revert_provenance_ref",
        "REVERT-PROVENANCE-001",
    )
    owner.update(
        application_id="APP-FAILED-001",
        authorization_id="AUTH-FAILED-001",
        source_revision="failed-application-cannot-own-revert-v1",
    )


def rename_unused_revert_owner(documents, new_ref):
    item(
        documents["records"]["revert_provenance_records"],
        "revert_provenance_ref",
        "REVERT-PROVENANCE-001",
    )["revert_provenance_ref"] = new_ref


def colliding_revert_transition_id(documents, collision):
    make_reverted(documents)
    item(
        documents["records"]["applications"],
        "application_id",
        "APP-APPLIED-001",
    )["revert_transition"]["revert_transition_id"] = collision


def cases():
    rows = []

    def invalid(case_id, mutate):
        rows.append((case_id, "invalid", mutate))

    def control(case_id, mutate):
        rows.append((case_id, "control", mutate))

    invalid(
        "I01",
        lambda d: replace_heading(d, "> ### Activation and claimant routing"),
    )
    invalid(
        "I02",
        lambda d: replace_heading(d, "- ### Activation and claimant routing"),
    )
    invalid("I03", failed_application_revert_owner)
    invalid(
        "I04", lambda d: rename_unused_revert_owner(d, "RUN-RECURRENCE-001")
    )
    invalid(
        "I05", lambda d: rename_unused_revert_owner(d, "DELTA-CONTRACT-0.1.1")
    )
    invalid(
        "I06", lambda d: colliding_revert_transition_id(d, "AUTH-INDEPENDENT-001")
    )
    invalid(
        "I07", lambda d: colliding_revert_transition_id(d, "APP-APPLIED-001")
    )
    invalid(
        "I08", lambda d: rename_unused_revert_owner(d, "EV-WAKE-001")
    )

    control("C01", lambda d: None)
    control(
        "C02",
        lambda d: replace_heading(
            d,
            "### [Activation and claimant routing](#activation-and-claimant-routing)",
        ),
    )
    control(
        "C03",
        lambda d: replace_heading(d, "### `Activation and claimant routing`"),
    )
    control(
        "C04",
        lambda d: replace_heading(d, "Activation and claimant routing\n---"),
    )
    control("C05", lambda d: None)
    control("C06", lambda d: make_reverted(d))
    control(
        "C07",
        lambda d: d.update(
            decision=d["decision"]
            + "\n> ### Activation and claimant routing\n> Quoted historical text only.\n"
        ),
    )
    return rows


class Task4ExactCommitApprovalRegressionTests(unittest.TestCase):
    def test_exact_commit_review_cases(self):
        source = retained.baseline()
        review_cases = cases()
        self.assertEqual(15, len(review_cases))
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


if __name__ == "__main__":
    unittest.main()
