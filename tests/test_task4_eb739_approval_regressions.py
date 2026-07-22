#!/usr/bin/env python3
"""Retained production-entry regressions from the Task 4 eb739 review."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests import test_task4_postfinal_approval_regressions as retained
from tests.test_task4_closure_approval_regressions import item, make_reverted


COLLISION = "APP-APPLIED-001"


def replace_scalar(value, old, new):
    """Replace exact scalar references recursively without changing keys."""
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if child == old:
                value[key] = new
            else:
                replace_scalar(child, old, new)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            if child == old:
                value[index] = new
            else:
                replace_scalar(child, old, new)


def collide_record_id(documents, collection, key, old, *, refresh=False):
    owner = item(documents["records"][collection], key, old)
    owner[key] = COLLISION
    replace_scalar(documents["records"], old, COLLISION)
    if refresh:
        retained.refresh_history(documents)


def collide_nested_revert_transition(documents):
    make_reverted(documents)
    application = item(
        documents["records"]["applications"],
        "application_id",
        "APP-APPLIED-001",
    )
    application["revert_transition"]["revert_transition_id"] = "MOA-001"


def malformed_revert_transition(documents):
    make_reverted(documents)
    application = item(
        documents["records"]["applications"],
        "application_id",
        "APP-APPLIED-001",
    )
    application["revert_transition"] = ["not", "a", "mapping"]


def replace_heading(documents, replacement):
    documents["decision"] = documents["decision"].replace(
        "### Activation and claimant routing", replacement, 1
    )


def reverse_unordered_registries(documents):
    for key in (
        "evidence_records",
        "meta_orthability_assessments",
        "source_family_records",
        "input_family_records",
        "recurrence_support_records",
        "opportunity_records",
        "revert_provenance_records",
    ):
        documents["records"][key].reverse()


def cases():
    rows = []

    def invalid(case_id, mutate):
        rows.append((case_id, "invalid", mutate))

    def control(case_id, mutate):
        rows.append((case_id, "control", mutate))

    collision_cases = (
        ("I01", "meta_orthability_assessments", "meta_orthability_assessment_id", "MOA-001", False),
        ("I02", "evidence_records", "evidence_id", "E-T1-OBSERVED", True),
        ("I03", "provenance_records", "provenance_record_id", "PROV-LIVE-001", True),
        ("I04", "source_records", "source_record_id", "fixture-subject-ORTH-NEW-001", True),
        ("I05", "source_family_records", "source_family_id", "corpus-A", True),
        ("I06", "input_family_records", "normalized_input_family_id", "malformed-input-family-A", False),
        ("I07", "recurrence_support_records", "support_record_id", "SUPPORT-NEW-001", False),
        ("I08", "opportunity_records", "opportunity_id", "OPP-SUPPORT-NEW-001", False),
        ("I09", "reference_corpus_records", "reference_corpus_revision", "LEDGER-REV-001", False),
    )
    for case_id, collection, key, old, refresh in collision_cases:
        invalid(
            case_id,
            lambda d, collection=collection, key=key, old=old, refresh=refresh:
                collide_record_id(d, collection, key, old, refresh=refresh),
        )
    invalid("I10", collide_nested_revert_transition)
    invalid("I11", malformed_revert_transition)

    control("C01", lambda d: None)
    control(
        "C02",
        lambda d: replace_heading(
            d, "### ![Activation and claimant&#32;routing](activation.png)"
        ),
    )
    control(
        "C03",
        lambda d: replace_heading(
            d, "### <span>Activation</span> and claimant routing"
        ),
    )
    control(
        "C04",
        lambda d: replace_heading(d, "### Activation and claimant&#32;routing"),
    )
    control(
        "C05",
        lambda d: replace_heading(
            d, "### ![*Activation* and claimant routing](activation.png)"
        ),
    )
    control("C06", make_reverted)
    control("C07", reverse_unordered_registries)
    control(
        "C08",
        lambda d: replace_heading(
            d, "### Activation <!-- annotation --> and claimant routing"
        ),
    )
    return rows


class Task4Eb739ApprovalRegressionTests(unittest.TestCase):
    def test_eb739_review_cases(self):
        source = retained.baseline()
        review_cases = cases()
        self.assertEqual(19, len(review_cases))
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
