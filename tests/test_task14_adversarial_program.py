#!/usr/bin/env python3
"""Task 14 durable attack-inventory and execution-accounting tests."""
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "tests" / "schema-mutations" / "mutation-spec.json"
PLAN_PATH = (
    ROOT
    / "docs"
    / "superpowers"
    / "plans"
    / "2026-07-21-r7e-sol-independent-repair.md"
)
MODULE_PATH = ROOT / "scripts" / "validate_recursive_mutations.py"


def load_module():
    spec = importlib.util.spec_from_file_location("task14_recursive", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def plan_attack_names():
    line = next(
        line
        for line in PLAN_PATH.read_text(encoding="utf-8").splitlines()
        if line.startswith("**Step 1:** Make every mandatory attack durable:")
    )
    names = line.split("durable: ", 1)[1].rstrip(".").split("; ")
    names[-1] = names[-1].removeprefix("and ")
    return names


class Task14AdversarialProgramTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    def test_exact_plan_inventory_is_unique_complete_and_executable(self):
        attacks = self.spec.get("mandatory_attacks")
        self.assertIsInstance(attacks, list)
        self.assertEqual(plan_attack_names(), [row["name"] for row in attacks])
        self.assertEqual(
            [f"R7E-T14-A{index:02d}" for index in range(1, len(attacks) + 1)],
            [row["attack_id"] for row in attacks],
        )
        self.assertEqual(len(attacks), len({row["mutation_id"] for row in attacks}))
        self.assertEqual([], self.module.audit_task14_spec(self.spec, ROOT))

    def test_spec_audit_rejects_duplicate_missing_and_phrase_only_coverage(self):
        attacks = self.spec["mandatory_attacks"]

        duplicate = copy.deepcopy(self.spec)
        duplicate["mandatory_attacks"][1]["mutation_id"] = attacks[0]["mutation_id"]
        self.assertTrue(
            any(
                "duplicate mutation ID" in issue
                for issue in self.module.audit_task14_spec(duplicate, ROOT)
            )
        )

        missing = copy.deepcopy(self.spec)
        missing["mandatory_attacks"].pop()
        self.assertTrue(
            any(
                "plan attack inventory differs" in issue
                for issue in self.module.audit_task14_spec(missing, ROOT)
            )
        )

        phrase_only = copy.deepcopy(self.spec)
        phrase_only["mandatory_attacks"][0]["coverage_kind"] = "phrase-presence"
        self.assertTrue(
            any(
                "must use structured semantic coverage" in issue
                for issue in self.module.audit_task14_spec(phrase_only, ROOT)
            )
        )

    def test_runner_executes_each_unique_command_once_and_accounts_for_every_attack(self):
        calls = []

        def fake_runner(command, **kwargs):
            del kwargs
            calls.append(tuple(command))
            return type("Result", (), {"returncode": 0, "stdout": "OK", "stderr": ""})()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        self.assertEqual([], issues)
        self.assertEqual(len(self.spec["mandatory_attacks"]), len(results))
        self.assertEqual(
            len({tuple(row["command"]) for row in self.spec["mandatory_attacks"]}),
            len(calls),
        )
        self.assertTrue(all(row["control_result"] == "accepted" for row in results))
        self.assertTrue(all(row["mutation_result"] == "rejected" for row in results))
        self.assertTrue(all(row["verification_exit_code"] == 0 for row in results))

    def test_runner_propagates_one_group_failure_to_every_covered_attack(self):
        failed = tuple(self.spec["mandatory_attacks"][0]["command"])

        def fake_runner(command, **kwargs):
            del kwargs
            rc = 1 if tuple(command[1:]) == failed[1:] else 0
            return type(
                "Result",
                (),
                {"returncode": rc, "stdout": "", "stderr": "bounded failure"},
            )()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        expected_failed = {
            row["attack_id"]
            for row in self.spec["mandatory_attacks"]
            if tuple(row["command"]) == failed
        }
        observed_failed = {
            row["attack_id"]
            for row in results
            if row["verification_exit_code"] != 0
        }
        self.assertEqual(expected_failed, observed_failed)
        self.assertTrue(issues)

    def test_report_is_derived_from_results_and_task14_ar6_rows(self):
        def fake_runner(command, **kwargs):
            del command, kwargs
            return type("Result", (), {"returncode": 0, "stdout": "OK", "stderr": ""})()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        self.assertEqual([], issues)
        report = self.module.render_task14_report(self.spec, results, ROOT)
        for attack in self.spec["mandatory_attacks"]:
            self.assertEqual(1, report.count(f"| {attack['attack_id']} |"))

        ledger = self.module.load_task14_ar6_rows(ROOT)
        self.assertEqual(
            {row["artifact_id"] for row in ledger},
            set(self.spec["task14_ar6_artifact_ids"]),
        )
        for row in ledger:
            self.assertEqual(1, report.count(f"| {row['artifact_id']} |"))
        self.assertIn("derived from the integrated tree", report)
        self.assertNotIn("solver result inferred", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
