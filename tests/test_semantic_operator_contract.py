#!/usr/bin/env python3
"""Task 6 contract and corrective-transition regression tests."""

import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
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


def predicate(doc, canonical_id):
    return next(row for row in doc["predicate_registry"]
                if row["canonical_id"] == canonical_id)


def operator(doc, operator_id):
    return next(row for row in doc["operator_contracts"]
                if row["semantic_operator_id"] == operator_id)


def refresh_result_digest(doc):
    core = copy.deepcopy(doc)
    core.pop("migration", None)
    doc["migration"]["resulting_v2_digest"] = hashlib.sha256(
        transition.canonical_bytes(core)
    ).hexdigest()


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
        self.assertEqual(6, len(predicates))
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

    def test_registry_resolves_types_owners_and_predicate_relations(self):
        self.assertEqual([], semantic.validate_contract(copy.deepcopy(self.contract)))

        cases = []
        doc = copy.deepcopy(self.contract)
        operator(doc, "field-divergence")["inputs"] = ["undeclared-field-type"]
        cases.append(doc)

        doc = copy.deepcopy(self.contract)
        predicate(doc, "reasoning_path_adequate_q")["requires"] = [
            "transition_pathway_adequate"
        ]
        cases.append(doc)

        doc = copy.deepcopy(self.contract)
        predicate(doc, "reasoning_path_adequate_q")["alias_of"] = (
            "strictly_sound_reasoning_q"
        )
        cases.append(doc)

        doc = copy.deepcopy(self.contract)
        operator(doc, "event-transition")["pathway_relation"][
            "canonical_predicate"
        ] = "strictly_sound_reasoning_q"
        cases.append(doc)

        doc = copy.deepcopy(self.contract)
        operator(doc, "loop-break")["owner_binding"] = {
            "owner_kind": "governance-source",
            "owner_id": "unregistered-owner",
            "source_ref": "unregistered/source.md",
        }
        cases.append(doc)

        for case in cases:
            with self.subTest(case=cases.index(case)):
                self.assertTrue(semantic.validate_contract(case))

    def test_malformed_semantic_nested_values_reject_without_traceback(self):
        malformed = copy.deepcopy(self.contract)
        malformed["operator_contracts"][0] = None
        issues = semantic.validate_contract(malformed)
        self.assertTrue(issues)

        malformed = copy.deepcopy(self.contract)
        operator(malformed, "field-curl")["target_field"]["node_types"] = None
        issues = semantic.validate_contract(malformed)
        self.assertTrue(issues)

        label_free = copy.deepcopy(self.contract)
        predicate(label_free, "reasoning_path_adequate_q").pop("display_label", None)
        self.assertEqual([], semantic.validate_contract(label_free))


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
        with io.open(os.path.join(APP, "CORRECTIVE-TRANSITION.v1.example.json"), "rb") as f:
            source_bytes = f.read()
        self.assertEqual(
            transition.HISTORICAL_V1_DIGEST,
            hashlib.sha256(source_bytes).hexdigest(),
        )
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
        self.assertEqual(transition.HISTORICAL_V1_DIGEST, migration["original_content_digest"])
        for key in ("original_record_identity", "source_contract", "migration_operation",
                    "migration_version", "migration_time", "provenance", "fields_mapped_directly",
                    "fields_newly_supplied", "fields_unavailable_or_held", "resulting_v2_digest"):
            self.assertIn(key, migration)
        self.assertEqual((True, None), transition.document_ok(first))
        tampered = copy.deepcopy(first)
        tampered["migration"]["resulting_v2_digest"] = "0" * 64
        self.assertEqual("migration-result-digest-mismatch", transition.document_ok(tampered)[1])

    def test_burdens_authorization_and_closure_are_cross_field_consistent(self):
        invalids = []

        doc = copy.deepcopy(self.v2)
        burden = doc["transitions"][0]["live_burdens"][0]
        doc["transitions"][0]["burden_accounting"] = {
            "addressed": [burden],
            "carried_forward": list(doc["transitions"][0]["live_burdens"]),
        }
        invalids.append(doc)

        doc = copy.deepcopy(self.v2)
        doc["transitions"][0]["global_revision"] = {
            "requested": False,
            "authorized": True,
            "authorization_ref": None,
        }
        invalids.append(doc)

        doc = copy.deepcopy(self.v2)
        doc["transitions"][0]["terminal_posture"] = "HOLD"
        doc["transitions"][0]["verdicts"]["runtime_closure"] = True
        invalids.append(doc)

        for doc in invalids:
            with self.subTest(case=invalids.index(doc)):
                self.assertFalse(transition.document_ok(doc)[0])

        authorized = copy.deepcopy(self.v2)
        authorized["transitions"][0]["global_revision"] = {
            "requested": True,
            "authorized": True,
            "authorization_ref": "authorization/task-6-control",
        }
        self.assertEqual((True, None), transition.document_ok(authorized))

        closed = copy.deepcopy(self.v2)
        closed["transitions"][0]["terminal_posture"] = "CLOSURE"
        closed["transitions"][0]["verdicts"]["runtime_closure"] = True
        self.assertEqual((True, None), transition.document_ok(closed))

    def test_migration_is_recomputed_against_authoritative_historical_source(self):
        valid = transition.migrate_v1_to_v2(
            transition.historical_v1_control(),
            transition.v2_migration_supplied_fields(),
        )
        self.assertEqual((True, None), transition.document_ok(copy.deepcopy(valid)))

        invalids = []
        doc = copy.deepcopy(valid)
        doc["migration"]["original_content_digest"] = "1" * 64
        invalids.append(doc)

        doc = copy.deepcopy(valid)
        doc["migration"]["original_record_identity"] = "different-source-record"
        doc["transitions"][0]["transition_id"] = "different-source-record"
        refresh_result_digest(doc)
        invalids.append(doc)

        doc = copy.deepcopy(valid)
        doc["migration"]["fields_newly_supplied"] = []
        invalids.append(doc)

        doc = copy.deepcopy(valid)
        doc["migration"]["migration_time"] = ""
        doc["migration"]["provenance"] = ""
        invalids.append(doc)

        for doc in invalids:
            with self.subTest(case=invalids.index(doc)):
                self.assertFalse(transition.document_ok(doc)[0])

    def test_malformed_transition_values_reject_without_traceback(self):
        self.assertFalse(transition.document_ok([])[0])
        malformed = transition.historical_v1_control()
        malformed["transitions"] = [None]
        self.assertFalse(transition.document_ok(malformed)[0])

    def test_historical_v1_owner_preserves_parent_bytes(self):
        historical_path = os.path.join(
            APP, "CORRECTIVE-TRANSITION.v1.example.json"
        )
        self.assertTrue(os.path.isfile(historical_path))
        with io.open(historical_path, "rb") as handle:
            historical_bytes = handle.read()
        parent_bytes = subprocess.check_output(
            [
                "git", "show",
                "167ce32bdc396490d219cdfbbd436babaa59e21a:"
                "applications/daee-epistemics/CORRECTIVE-TRANSITION.example.json",
            ],
            cwd=ROOT,
        )
        self.assertEqual(parent_bytes, historical_bytes)
        self.assertEqual(
            "9b19572d7e1e43ed513a910811b21cbd49f9ab8c58a4626ea5347f1175216d5e",
            hashlib.sha256(historical_bytes).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
