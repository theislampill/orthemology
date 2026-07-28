#!/usr/bin/env python3
"""Retained production-entry regressions from the three Task 4 parallel reviews."""
from __future__ import annotations

import unittest

from tests import task4_parallel_a_regressions as lane_a
from tests import task4_parallel_b_regressions as lane_b
from tests import task4_parallel_c_regressions as lane_c


class Task4ParallelReviewUnionTests(unittest.TestCase):
    def assertCase(self, case_id, kind, expected_exit, actual_exit, output):
        self.assertNotEqual(99, actual_exit, f"{case_id} traceback: {output}")
        self.assertNotIn("TRACEBACK", output, f"{case_id} traceback: {output}")
        self.assertEqual(
            expected_exit,
            actual_exit,
            f"{case_id} {kind} expected {expected_exit}, got {actual_exit}: {output}",
        )

    def test_lane_a_ownership_and_chronology_cases(self):
        baseline = {
            "activation": lane_a.load_yaml(lane_a.ACTIVATION),
            "records": lane_a.load_yaml(lane_a.RECORDS),
            "history": lane_a.load_yaml(lane_a.HISTORY),
            "inventory": lane_a.load_yaml(lane_a.INVENTORY),
            "adoption": lane_a.load_yaml(lane_a.ADOPTION),
            "collective": lane_a.load_yaml(lane_a.COLLECTIVE),
            "decision": lane_a.DECISION.read_text(encoding="utf-8"),
        }
        cases = [
            *(('invalid', case) for case in lane_a.invalid_cases(baseline)),
            *(('control', case) for case in lane_a.valid_controls(baseline)),
        ]
        self.assertEqual(13, len(cases))
        for kind, (case_id, _name, documents, _domain) in cases:
            with self.subTest(case_id=case_id, kind=kind):
                actual_exit, output = lane_a.production_exit(documents)
                self.assertCase(case_id, kind, 1 if kind == "invalid" else 0, actual_exit, output)

    def test_lane_b_history_and_identity_cases(self):
        baseline = {name: lane_b.load_yaml(path) for name, path in lane_b.PATHS.items()}
        cases = lane_b.build_cases(baseline)
        self.assertEqual(25, len(cases))
        for case_id, kind, _name, expected_exit, mutate in cases:
            with self.subTest(case_id=case_id, kind=kind):
                documents = lane_b.clone(baseline)
                mutate(documents)
                actual_exit, output = lane_b.production_exit(documents)
                self.assertCase(case_id, kind, expected_exit, actual_exit, output)

    def test_lane_c_schema_and_consistency_cases(self):
        baseline = lane_c.load_base()
        cases = lane_c.build_cases(baseline)
        self.assertEqual(40, len(cases))
        for case_id, _name, kind, expected_exit, _boundary, mutate in cases:
            with self.subTest(case_id=case_id, kind=kind):
                documents = lane_c.fresh(baseline)
                mutate(documents)
                actual_exit, output = lane_c.production_exit(documents)
                self.assertCase(case_id, kind, expected_exit, actual_exit, output)


if __name__ == "__main__":
    unittest.main()
