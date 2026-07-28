#!/usr/bin/env python3
"""Retained production-entry regressions from the Task 4 terminal review."""
from __future__ import annotations

import copy
import unittest

from tests import test_task4_postfinal_approval_regressions as retained
from tests.test_task4_closure_approval_regressions import item, make_reverted


def used_revert_owner(documents):
    make_reverted(documents)
    return item(
        documents["records"]["revert_provenance_records"],
        "revert_provenance_ref",
        "REVERT-PROVENANCE-CLOSURE-001",
    )


def rename_used_revert_owner(documents, new_ref):
    owner = used_revert_owner(documents)
    owner["revert_provenance_ref"] = new_ref
    application = item(
        documents["records"]["applications"],
        "application_id",
        "APP-APPLIED-001",
    )
    application["revert_transition"]["revert_provenance_ref"] = new_ref


def cases():
    rows = []

    def invalid(case_id, mutate):
        rows.append((case_id, "invalid", mutate))

    def control(case_id, mutate):
        rows.append((case_id, "control", mutate))

    def unused_owner(documents):
        return item(
            documents["records"]["revert_provenance_records"],
            "revert_provenance_ref",
            "REVERT-PROVENANCE-001",
        )

    invalid(
        "I01",
        lambda d: unused_owner(d).update(application_id="MISSING-APPLICATION"),
    )
    invalid(
        "I02",
        lambda d: unused_owner(d).update(authorization_id="MISSING-AUTHORIZATION"),
    )
    invalid(
        "I03",
        lambda d: unused_owner(d).update(authorization_id="AUTH-FAILED-001"),
    )
    invalid(
        "I04",
        lambda d: unused_owner(d).update(application_id="APP-FAILED-001"),
    )
    invalid("I05", lambda d: rename_used_revert_owner(d, "PROP-MEMORY-001"))
    invalid("I06", lambda d: rename_used_revert_owner(d, "AUTH-INDEPENDENT-001"))

    def alias_on_wrong_candidate(documents):
        item(
            documents["inventory"]["candidates"],
            "candidate_id",
            "somnus-import",
        )["downstream_owner"]["owner_role"] = (
            "external bounded-record custody operator"
        )

    invalid("I07", alias_on_wrong_candidate)

    def casefold_candidate_clone(documents):
        candidate = copy.deepcopy(
            item(
                documents["inventory"]["candidates"],
                "candidate_id",
                "somnus-export",
            )
        )
        candidate["candidate_id"] = "Somnus-Export"
        documents["inventory"]["candidates"].append(candidate)

    invalid("I08", casefold_candidate_clone)

    def swap_candidate_owners(documents):
        left = item(
            documents["inventory"]["candidates"], "candidate_id", "somnus-export"
        )
        right = item(
            documents["inventory"]["candidates"], "candidate_id", "somnus-import"
        )
        left["downstream_owner"], right["downstream_owner"] = (
            right["downstream_owner"],
            left["downstream_owner"],
        )

    invalid("I09", swap_candidate_owners)
    invalid(
        "I10",
        lambda d: unused_owner(d).update(
            application_id={"nested": ["APP-APPLIED-001"]}
        ),
    )
    invalid(
        "I11",
        lambda d: d["inventory"]["candidates"][0].update(
            candidate_id={"nested": ["orthability-check"]}
        ),
    )
    invalid(
        "I12",
        lambda d: d["activation"]["version_transition_authority"].update(
            authority_ref={"nested": ["Decision 0035"]}
        ),
    )

    control("C01", lambda d: None)
    control(
        "C02",
        lambda d: d.update(
            decision=d["decision"]
            + "\n<!--\n### Activation and claimant routing\n-->\n"
        ),
    )
    control(
        "C03",
        lambda d: d.update(
            decision=d["decision"]
            + "\n<pre>\n### Activation and claimant routing\n</pre>\n"
        ),
    )
    control(
        "C04",
        lambda d: d["records"]["revert_provenance_records"].reverse(),
    )

    def append_valid_unused_owner(documents):
        documents["records"]["revert_provenance_records"].append(
            {
                "revert_provenance_ref": "REVERT-PROVENANCE-EXTRA-001",
                "application_id": "APP-APPLIED-001",
                "authorization_id": "AUTH-INDEPENDENT-001",
                "source_revision": "task4-revert-fixture-v2",
                "immutable": True,
            }
        )

    control("C05", append_valid_unused_owner)
    control(
        "C06",
        lambda d: rename_used_revert_owner(
            d, "REVERT-PROVENANCE-RENAMED-001"
        ),
    )

    def combined_candidate_aliases_and_order(documents):
        aliases = {
            "verdict-aware-patch-proposal": "external change-proposal custodian",
            "guarded-writeback-actuator": "downstream guarded actuation service owner",
            "somnus-export": "external bounded-record custody operator",
        }
        for candidate in documents["inventory"]["candidates"]:
            alias = aliases.get(candidate["candidate_id"])
            if alias:
                candidate["downstream_owner"]["owner_role"] = alias
            for field in ("inputs", "outputs", "dependencies"):
                candidate[field] = list(reversed(candidate[field]))
        documents["inventory"]["candidates"].reverse()

    control("C07", combined_candidate_aliases_and_order)
    control(
        "C08",
        lambda d: d.update(
            decision=d["decision"]
            + "\nA literal `### Activation and claimant routing` is not a heading.\n"
        ),
    )
    return rows


class Task4TerminalApprovalRegressionTests(unittest.TestCase):
    def test_terminal_review_cases(self):
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


if __name__ == "__main__":
    unittest.main()
