#!/usr/bin/env python3
"""Task 6 contract and corrective-transition regression tests."""

import copy
import hashlib
import importlib.util
import io
import json
import os
import unittest

import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "applications", "daee-epistemics")


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


semantic = load_module("semantic", "scripts/validate_semantic_operator_contract.py")
transition = load_module("transition", "scripts/validate_corrective_transition.py")


class SemanticOperatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with io.open(os.path.join(APP, "SEMANTIC-OPERATOR-CONTRACT.yaml"), encoding="utf-8") as f:
            cls.contract = yaml.safe_load(f)
        with io.open(os.path.join(APP, "SEMANTIC-OPERATOR-FIXTURES.yaml"), encoding="utf-8") as f:
            cls.fixtures = yaml.safe_load(f)

    def test_exactly_seven_typed_operators(self):
        rows = self.contract["operator_contracts"]
        self.assertEqual(
            {r["semantic_operator_id"] for r in rows},
            {"route-pressure", "event-transition", "field-divergence", "field-curl",
             "loop-break", "whole-state-reread", "runtime-closure"},
        )
        for row in rows:
            for key in ("inputs", "outputs", "target_field", "preconditions", "semantic_kind",
                        "claim_role", "owner_binding", "sources", "correctness_relation",
                        "pathway_relation", "non_claims"):
                self.assertIn(key, row)
        self.assertEqual([], semantic.validate_contract(copy.deepcopy(self.contract)))

    def test_predicate_alias_is_one_identity_and_one_computation(self):
        predicates = self.contract["predicate_registry"]
        self.assertEqual(5, len(predicates))
        canonical = [p for p in predicates if p["canonical_id"] == "reasoning_path_adequate_q"]
        self.assertEqual(1, len(canonical))
        self.assertEqual("ReasoningPathAdequate_q(e)", canonical[0]["normative_symbol"])
        self.assertEqual("ClaimRelevantReasoningPathAdequate", canonical[0]["display_label"])
        self.assertEqual("decision-0011-required-reason-projection", canonical[0]["computation"])
        self.assertNotIn("ClaimRelevantReasoningPathAdequate", {p["canonical_id"] for p in predicates})
        strict = next(p for p in predicates if p["canonical_id"] == "strictly_sound_reasoning_q")
        self.assertEqual(["reasoning_path_adequate_q", "token_truth_linked_q"], strict["requires"])

    def test_alias_mutations_reject_but_label_removal_is_semantically_inert(self):
        divergent = copy.deepcopy(self.contract)
        divergent["predicate_alias_statuses"] = {
            "reasoning_path_adequate_q": "pass", "ClaimRelevantReasoningPathAdequate": "fail"
        }
        self.assertIn("predicate-alias-divergence", semantic.issue_codes(divergent))

        duplicate = copy.deepcopy(self.contract)
        duplicate["predicate_registry"].append(copy.deepcopy(duplicate["predicate_registry"][3]))
        self.assertIn("duplicate-normative-predicate", semantic.issue_codes(duplicate))

        relabel = copy.deepcopy(self.contract)
        predicate = next(p for p in relabel["predicate_registry"]
                         if p["canonical_id"] == "reasoning_path_adequate_q")
        predicate.pop("display_label")
        self.assertNotIn("predicate-semantics-changed", semantic.issue_codes(relabel))
        renamed = copy.deepcopy(self.contract)
        predicate = next(p for p in renamed["predicate_registry"]
                         if p["canonical_id"] == "reasoning_path_adequate_q")
        predicate["display_label"] = "Readable label changed without semantic effect"
        self.assertEqual([], semantic.issue_codes(renamed))

    def test_all_declared_semantic_attacks_and_controls(self):
        for case in self.fixtures["fixtures"]:
            issues = semantic.issue_codes(semantic.contract_for_case(self.contract, case))
            self.assertEqual(case["expected_valid"], not issues, (case["id"], issues))
            if not case["expected_valid"]:
                self.assertIn(case["violates"], issues, case["id"])


class CorrectiveTransitionV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with io.open(os.path.join(APP, "CORRECTIVE-TRANSITION.example.json"), encoding="utf-8") as f:
            cls.v2 = json.load(f)

    def test_current_v2_and_missing_or_unknown_versions(self):
        self.assertEqual("orthemology-corrective-transition-v2", self.v2["schema"])
        self.assertEqual((True, None), transition.document_ok(copy.deepcopy(self.v2)))
        missing = copy.deepcopy(self.v2); missing.pop("schema")
        self.assertEqual("missing-version", transition.document_ok(missing)[1])
        unknown = copy.deepcopy(self.v2); unknown["schema"] = "orthemology-corrective-transition-v99"
        self.assertEqual("unknown-version", transition.document_ok(unknown)[1])
        missing_field = copy.deepcopy(self.v2); missing_field["transitions"][0].pop("operator_trace")
        self.assertEqual("v2-schema-invalid", transition.document_ok(missing_field)[1])

    def test_explicit_v1_historical_branch_cannot_claim_v2_guarantees(self):
        v1 = transition.historical_v1_control()
        before = transition.canonical_bytes(v1)
        self.assertEqual(transition.HISTORICAL_V1_DIGEST, hashlib.sha256(before).hexdigest())
        self.assertEqual((True, None), transition.document_ok(v1))
        self.assertEqual(before, transition.canonical_bytes(v1))
        implicit = copy.deepcopy(v1); implicit.pop("schema")
        self.assertEqual("missing-version", transition.document_ok(implicit)[1])
        v1["transitions"][0]["operator_trace"] = []
        self.assertEqual("v1-claims-v2-guarantee", transition.document_ok(v1)[1])

    def test_explicit_migration_is_deterministic_provenance_bearing_and_non_mutating(self):
        v1 = transition.historical_v1_control()
        original = transition.canonical_bytes(v1)
        supplied = transition.v2_migration_supplied_fields()
        first = transition.migrate_v1_to_v2(v1, supplied)
        second = transition.migrate_v1_to_v2(v1, supplied)
        self.assertEqual(first, second)
        self.assertEqual(original, transition.canonical_bytes(v1))
        migration = first["migration"]
        self.assertEqual(hashlib.sha256(original).hexdigest(), migration["original_content_digest"])
        for key in ("original_record_identity", "source_contract", "migration_operation",
                    "migration_version", "migration_time", "provenance", "fields_mapped_directly",
                    "fields_newly_supplied", "fields_unavailable_or_held", "resulting_v2_digest"):
            self.assertIn(key, migration)
        self.assertEqual((True, None), transition.document_ok(first))
        tampered = copy.deepcopy(first)
        tampered["migration"]["resulting_v2_digest"] = "0" * 64
        self.assertEqual("migration-result-digest-mismatch", transition.document_ok(tampered)[1])


if __name__ == "__main__":
    unittest.main()
