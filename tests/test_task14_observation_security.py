#!/usr/bin/env python3
"""Fail-closed Task 14 direct-observation protocol tests."""
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_recursive_mutations.py"
PROBE_PATH = ROOT / "scripts" / "run_task14_probe.py"
SPEC_PATH = ROOT / "tests" / "schema-mutations" / "mutation-spec.json"


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Task14ObservationSecurityTests(unittest.TestCase):
    def setUp(self):
        self.validator = load(VALIDATOR_PATH, "task14_recursive_security")
        self.probe = load(PROBE_PATH, "task14_probe_security")
        self.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        self.registry = self.validator.load_task14_probe_registry(ROOT)
        self.binding = self.registry[("R7E-T14-A01", "R7E-T14-A01-V01")]

    def expected(self, role: str = "control"):
        return self.validator.expected_task14_observation(self.binding, role, ROOT)

    def payload(self, role: str = "control"):
        expected = self.expected(role)
        outcome = "accepted" if role == "control" else "rejected"
        return {
            "schema": self.validator.TASK14_OBSERVATION_SCHEMA,
            **expected,
            "observed_validator_outcome": outcome,
            "evidence_process_exit_code": 0,
            "exit_semantics": (
                "0 means direct probe execution succeeded; validator acceptance "
                "or rejection is carried only by observed_validator_outcome"
            ),
            "input_sha256": "1" * 64,
            "observation_id": self.validator.task14_observation_id(
                expected, outcome, "1" * 64
            ),
        }

    @staticmethod
    def completed(payload):
        return type(
            "Completed",
            (),
            {"returncode": 0, "stdout": json.dumps(payload), "stderr": ""},
        )()

    def test_parser_rejects_every_identity_digest_and_shape_forgery(self):
        base = self.payload()
        attacks = {
            "missing mutation id": ("mutation_id", None),
            "wrong mutation id": ("mutation_id", "R7E-T14-A01-M99"),
            "wrong owner": ("validator_owner", "fabricated owner"),
            "wrong entrypoint": ("validator_entry_point", "scripts/validate_repo.py"),
            "stale digest": ("validator_sha256", "0" * 64),
            "swapped selector": (
                "evidence_selector",
                self.registry[
                    ("R7E-T14-A02", "R7E-T14-A02-V01")
                ].control_evidence_selector,
            ),
        }
        for name, (field, value) in attacks.items():
            payload = copy.deepcopy(base)
            if value is None:
                payload.pop(field)
            else:
                payload[field] = value
            with self.subTest(attack=name):
                with self.assertRaises(ValueError):
                    self.validator._parse_task14_observation(
                        self.completed(payload), self.expected()
                    )

        extra = copy.deepcopy(base)
        extra["untrusted_extra"] = "accepted"
        with self.assertRaises(ValueError):
            self.validator._parse_task14_observation(
                self.completed(extra), self.expected()
            )

    def test_parser_rejects_forged_positive_only_mutation_outcome(self):
        payload = self.payload("mutation")
        payload["observed_validator_outcome"] = "accepted"
        payload["observation_id"] = self.validator.task14_observation_id(
            self.expected("mutation"), "accepted", payload["input_sha256"]
        )
        with self.assertRaises(ValueError):
            self.validator._parse_task14_observation(
                self.completed(payload), self.expected("mutation")
            )

    def test_parser_rejects_forged_json_against_independent_direct_execution(self):
        payload = self.payload()
        trusted = self.probe.execute_direct_probe(self.binding, "control")
        with self.assertRaisesRegex(ValueError, "independent direct execution"):
            self.validator._parse_task14_observation(
                self.completed(payload),
                self.expected(),
                trusted_direct_result=trusted,
            )

    def test_spec_audit_uses_closed_registry_not_mutable_owner_or_selectors(self):
        mutations = []
        wrong_owner = copy.deepcopy(self.spec)
        wrong_owner["mandatory_attacks"][0]["owner"] = "fabricated owner"
        wrong_owner["mandatory_attacks"][0]["variants"][0][
            "validator_owner"
        ] = "fabricated owner"
        mutations.append(wrong_owner)

        wrong_entrypoint = copy.deepcopy(self.spec)
        wrong_entrypoint["mandatory_attacks"][0]["variants"][0][
            "validator_entry_point"
        ] = "scripts/validate_repo.py"
        mutations.append(wrong_entrypoint)

        swapped = copy.deepcopy(self.spec)
        first = swapped["mandatory_attacks"][0]["variants"][0]
        second = swapped["mandatory_attacks"][1]["variants"][0]
        first["control_evidence_selector"], second["control_evidence_selector"] = (
            second["control_evidence_selector"],
            first["control_evidence_selector"],
        )
        mutations.append(swapped)

        positive_only = copy.deepcopy(self.spec)
        positive_only["mandatory_attacks"][0]["variants"][0][
            "mutation_evidence_selector"
        ] = positive_only["mandatory_attacks"][0]["variants"][0][
            "control_evidence_selector"
        ]
        mutations.append(positive_only)

        for index, mutated in enumerate(mutations):
            with self.subTest(case=index):
                self.assertTrue(
                    self.validator.audit_task14_spec(mutated, ROOT),
                    "closed registry drift must fail",
                )

    def test_probe_reports_executor_outcome_without_deriving_it_from_role(self):
        accepted = self.probe.observe(
            "R7E-T14-A01",
            "R7E-T14-A01-V01",
            "mutation",
            executor=lambda binding, role: {
                "outcome": "accepted",
                "input_sha256": "2" * 64,
            },
        )
        self.assertEqual("accepted", accepted["observed_validator_outcome"])

    def test_all_closed_registry_cases_observe_direct_control_and_mutation_outcomes(self):
        observed = []
        for binding in self.registry.values():
            control = self.probe.execute_direct_probe(binding, "control")
            mutation = self.probe.execute_direct_probe(binding, "mutation")
            observed.append((binding.variant_id, control, mutation))
        self.assertEqual(77, len(observed))
        self.assertTrue(all(row[1]["outcome"] == "accepted" for row in observed))
        self.assertTrue(all(row[2]["outcome"] == "rejected" for row in observed))
        self.assertTrue(
            all(row[1]["input_sha256"] != row[2]["input_sha256"] for row in observed)
        )

    def test_runner_rejects_duplicate_observation_and_cross_variant_replay(self):
        payload = self.payload()
        seen = set()
        self.validator._parse_task14_observation(
            self.completed(payload), self.expected(), seen
        )
        with self.assertRaisesRegex(ValueError, "duplicate observation"):
            self.validator._parse_task14_observation(
                self.completed(payload), self.expected(), seen
            )

        replay = self.payload()
        other = self.registry[("R7E-T14-A01", "R7E-T14-A01-V02")]
        with self.assertRaises(ValueError):
            self.validator._parse_task14_observation(
                self.completed(replay),
                self.validator.expected_task14_observation(other, "control", ROOT),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
