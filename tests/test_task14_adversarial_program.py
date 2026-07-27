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
        mutation_ids = [
            variant["mutation_id"]
            for attack in attacks
            for variant in attack["variants"]
        ]
        self.assertEqual(len(mutation_ids), len(set(mutation_ids)))
        self.assertEqual([], self.module.audit_task14_spec(self.spec, ROOT))

    def test_spec_audit_rejects_duplicate_missing_and_arbitrary_coverage_labels(self):
        attacks = self.spec["mandatory_attacks"]

        duplicate = copy.deepcopy(self.spec)
        duplicate["mandatory_attacks"][1]["variants"][0]["mutation_id"] = attacks[0][
            "variants"
        ][0]["mutation_id"]
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
                "must not use an arbitrary coverage label" in issue
                for issue in self.module.audit_task14_spec(phrase_only, ROOT)
            )
        )

    def test_spec_audit_rejects_positive_only_selector_only_and_mismatched_probes(self):
        attack = self.spec["mandatory_attacks"][0]

        positive_only = copy.deepcopy(self.spec)
        positive_only["mandatory_attacks"][0]["variants"][0].pop("mutation_command")
        self.assertTrue(
            any(
                "has no mutation command" in issue
                for issue in self.module.audit_task14_spec(positive_only, ROOT)
            )
        )

        selector_only = copy.deepcopy(self.spec)
        selector_only["mandatory_attacks"][0]["variants"][0]["mutation_command"] = [
            "python",
            "-m",
            "unittest",
            "tests.test_candidate_state.CandidateStateTests."
            "test_omitted_pr_11_or_12_is_rejected",
        ]
        self.assertTrue(
            any(
                "must invoke the production observation probe" in issue
                for issue in self.module.audit_task14_spec(selector_only, ROOT)
            )
        )

        mismatch = copy.deepcopy(self.spec)
        mismatch["mandatory_attacks"][0]["variants"][0]["variant_id"] = (
            attack["attack_id"] + "-V99"
        )
        self.assertTrue(
            any(
                "variant command identity mismatch" in issue
                for issue in self.module.audit_task14_spec(mismatch, ROOT)
            )
        )

        wrong_owner = copy.deepcopy(self.spec)
        wrong_owner["mandatory_attacks"][0]["variants"][0][
            "validator_owner"
        ] = "unrelated owner"
        self.assertTrue(
            any(
                "validator owner differs from attack owner" in issue
                for issue in self.module.audit_task14_spec(wrong_owner, ROOT)
            )
        )

    def test_runner_executes_each_unique_command_once_and_accounts_for_every_attack(self):
        calls = []

        def fake_runner(command, **kwargs):
            del kwargs
            calls.append(tuple(command))
            identity = self.module.task14_probe_identity(command)
            role = identity["role"]
            attack = next(
                row
                for row in self.spec["mandatory_attacks"]
                if row["attack_id"] == identity["attack_id"]
            )
            variant = next(
                row
                for row in attack["variants"]
                if row["variant_id"] == identity["variant_id"]
            )
            payload = {
                "schema": "orthemology-task14-observation-v1",
                "attack_id": identity["attack_id"],
                "variant_id": identity["variant_id"],
                "role": role,
                "validator_owner": variant["validator_owner"],
                "validator_entry_point": variant["validator_entry_point"],
                "asserted_validator_outcome": (
                    "accepted" if role == "control" else "rejected"
                ),
                "evidence_process_exit_code": 0,
                "exit_semantics": (
                    "0 means the role-specific focused selector completed and its "
                    "production-validator assertion passed; it is not the validator's "
                    "own exit code"
                ),
            }
            return type(
                "Result",
                (),
                {"returncode": 0, "stdout": json.dumps(payload), "stderr": ""},
            )()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        self.assertEqual([], issues)
        variants = [
            variant
            for attack in self.spec["mandatory_attacks"]
            for variant in attack["variants"]
        ]
        self.assertEqual(len(variants), len(results))
        self.assertEqual(2 * len(variants), len(calls))
        self.assertTrue(all(row["control_asserted_outcome"] == "accepted" for row in results))
        self.assertTrue(
            all(row["control_evidence_process_exit_code"] == 0 for row in results)
        )
        self.assertTrue(all(row["mutation_asserted_outcome"] == "rejected" for row in results))
        self.assertTrue(
            all(row["mutation_evidence_process_exit_code"] == 0 for row in results)
        )

    def test_runner_rejects_arbitrary_rc0_without_exact_machine_observation(self):
        def fake_runner(command, **kwargs):
            del command, kwargs
            return type(
                "Result",
                (),
                {"returncode": 0, "stdout": "OK", "stderr": ""},
            )()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        self.assertEqual([], results)
        self.assertTrue(any("machine-readable observation" in issue for issue in issues))

    def test_runner_rejects_positive_only_and_identity_drift_observations(self):
        first = self.spec["mandatory_attacks"][0]["variants"][0]

        def fake_runner(command, **kwargs):
            del kwargs
            identity = self.module.task14_probe_identity(command)
            role = identity["role"]
            payload = {
                "schema": "orthemology-task14-observation-v1",
                "attack_id": identity["attack_id"],
                "variant_id": identity["variant_id"],
                "role": role,
                "validator_owner": first["validator_owner"],
                "validator_entry_point": first["validator_entry_point"],
                "asserted_validator_outcome": "accepted",
                "evidence_process_exit_code": 0,
                "exit_semantics": (
                    "0 means the role-specific focused selector completed and its "
                    "production-validator assertion passed; it is not the validator's "
                    "own exit code"
                ),
            }
            if identity["attack_id"] != self.spec["mandatory_attacks"][0]["attack_id"]:
                payload["attack_id"] = "R7E-T14-A00"
            return type(
                "Result",
                (),
                {"returncode": 0, "stdout": json.dumps(payload), "stderr": ""},
            )()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        self.assertTrue(issues)
        self.assertTrue(
            any(
                "mutation observed accepted" in issue
                or "observation identity mismatch" in issue
                for issue in issues
            )
        )

    def test_report_is_derived_from_results_and_task14_ar6_rows(self):
        def fake_runner(command, **kwargs):
            del kwargs
            identity = self.module.task14_probe_identity(command)
            attack = next(
                row
                for row in self.spec["mandatory_attacks"]
                if row["attack_id"] == identity["attack_id"]
            )
            variant = next(
                row
                for row in attack["variants"]
                if row["variant_id"] == identity["variant_id"]
            )
            role = identity["role"]
            payload = {
                "schema": "orthemology-task14-observation-v1",
                "attack_id": identity["attack_id"],
                "variant_id": identity["variant_id"],
                "role": role,
                "validator_owner": variant["validator_owner"],
                "validator_entry_point": variant["validator_entry_point"],
                "asserted_validator_outcome": (
                    "accepted" if role == "control" else "rejected"
                ),
                "evidence_process_exit_code": 0,
                "exit_semantics": (
                    "0 means the role-specific focused selector completed and its "
                    "production-validator assertion passed; it is not the validator's "
                    "own exit code"
                ),
            }
            return type(
                "Result",
                (),
                {"returncode": 0, "stdout": json.dumps(payload), "stderr": ""},
            )()

        results, issues = self.module.run_task14_attacks(
            self.spec, ROOT, runner=fake_runner, python="PYTHON"
        )
        self.assertEqual([], issues)
        report = self.module.render_task14_report(self.spec, results, ROOT)
        for attack in self.spec["mandatory_attacks"]:
            self.assertEqual(
                len(attack["variants"]),
                report.count(f"| {attack['attack_id']} |"),
            )

        ledger = self.module.load_task14_ar6_rows(ROOT)
        self.assertEqual(
            {row["artifact_id"] for row in ledger},
            set(self.spec["task14_ar6_artifact_ids"]),
        )
        for row in ledger:
            self.assertEqual(1, report.count(f"| {row['artifact_id']} |"))
        self.assertIn("derived from the integrated tree", report)
        self.assertNotIn("solver result inferred", report)

    def test_ar6_rows_are_explicitly_reproduced_or_retained_as_provenance_only(self):
        mappings = self.spec["task14_ar6_mappings"]
        ledger = self.module.load_task14_ar6_rows(ROOT)
        self.assertEqual(
            {row["artifact_id"] for row in ledger},
            {row["artifact_id"] for row in mappings},
        )
        negative = [
            row
            for row in ledger
            if row["required_disposition"] == "COUNTERMODEL_OR_NEGATIVE_EVIDENCE"
        ]
        interrupted = [
            row
            for row in ledger
            if row["required_disposition"] == "INTERRUPTED_UNVERIFIED_RESEARCH"
        ]
        self.assertEqual(9, len(negative))
        self.assertEqual(10, len(interrupted))

        mapping_by_id = {row["artifact_id"]: row for row in mappings}
        for row in interrupted:
            self.assertEqual(
                "NOT_REPRODUCED_RETAINED_PROVENANCE_ONLY",
                mapping_by_id[row["artifact_id"]]["reproduction_status"],
            )
        for row in negative:
            mapping = mapping_by_id[row["artifact_id"]]
            if row["current_repository_representation"] == (
                "NO_CANONICAL_REPOSITORY_OWNER_IDENTIFIED"
            ):
                self.assertEqual(
                    "NOT_REPRODUCED_RETAINED_PROVENANCE_ONLY",
                    mapping["reproduction_status"],
                )

    def test_ar6_audit_rejects_unmapped_reproduction_and_unreproduced_promotion(self):
        reproduced = next(
            row
            for row in self.spec["task14_ar6_mappings"]
            if row["reproduction_status"] == "REPRODUCED_AGAINST_INTEGRATED_TREE"
        )
        missing = copy.deepcopy(self.spec)
        target = next(
            row
            for row in missing["task14_ar6_mappings"]
            if row["artifact_id"] == reproduced["artifact_id"]
        )
        target.pop("variant_id")
        self.assertTrue(
            any(
                "reproduced AR6 row lacks exact attack/variant/result mapping" in issue
                for issue in self.module.audit_task14_spec(missing, ROOT)
            )
        )

        unreproduced = next(
            row
            for row in self.spec["task14_ar6_mappings"]
            if row["reproduction_status"]
            == "NOT_REPRODUCED_RETAINED_PROVENANCE_ONLY"
        )
        promoted = copy.deepcopy(self.spec)
        target = next(
            row
            for row in promoted["task14_ar6_mappings"]
            if row["artifact_id"] == unreproduced["artifact_id"]
        )
        target["normative_flow"] = "PUBLICATION_READY"
        self.assertTrue(
            any(
                "unreproduced AR6 row may not enter normative flow" in issue
                for issue in self.module.audit_task14_spec(promoted, ROOT)
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
