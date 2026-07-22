#!/usr/bin/env python3
"""Task 7 regressions for evidence, fiṭrah, and mental/external boundaries."""

import copy
import importlib.util
import json
import pathlib
import unittest

import jsonschema
import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
APP = ROOT / "applications" / "daee-epistemics"


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MEMETIC = load_module("task7_memetic", "scripts/validate_memetic_ecology.py")
NOETIC = load_module("task7_noetic", "scripts/validate_noetic_claims.py")
META = load_module("task7_meta", "scripts/validate_meta_noetic_memetics.py")


def valid_warrant():
    return {
        "schema": "orthemology-tawatur-warrant-v2",
        "assessments": [{
            "id": "TWW-CONTROL",
            "school": "Athari creed-internal reconstruction",
            "proposition": {
                "id": "PROP-P",
                "text": "proposition P",
                "objective_truth_status": "not-adjudicated",
            },
            "claim_role": "secondary-reconstruction",
            "source_status_refs": ["ELT-3"],
            "source_units": [
                {"unit_id": "SU-1", "origin_id": "O-1", "transmission_paths": ["P-1"],
                 "unit_status": "originating-unit"},
                {"unit_id": "SU-2", "origin_id": "O-2", "transmission_paths": ["P-2"],
                 "unit_status": "originating-unit"},
            ],
            "origin_analysis": {
                "common_cause_status": "not-detected",
                "copying_status": "not-detected",
                "path_independence": "supported",
                "non_collusion": "supported",
                "mutation_lineage": "no-single-lineage-detected",
                "evidence_refs": ["ev-origin-map"],
            },
            "transmitter_quality": [
                {"source_unit_id": "SU-1", "honesty_or_trust": "supported",
                 "domain_competence": "supported", "evidence_refs": ["ev-q1"]},
                {"source_unit_id": "SU-2", "honesty_or_trust": "supported",
                 "domain_competence": "supported", "evidence_refs": ["ev-q2"]},
            ],
            "circumstantial_indicants": ["independent regional transmission"],
            "content_coherence": {"status": "supported", "evidence_refs": ["ev-content"]},
            "acquisition_routes": [
                {"route_id": "AR-1", "source_unit_ids": ["SU-1"]},
                {"route_id": "AR-2", "source_unit_ids": ["SU-2"]},
            ],
            "subject_assessments": [
                {"subject_id": "SUB-A", "access_status": "acquired",
                 "route_refs": ["AR-1", "AR-2"], "subject_relative_conditions": ["access to both routes"],
                 "assessor_id": "ASSESSOR-1", "assessor_evidence": ["ev-access-a"],
                 "defeaters": ["hidden common cause"], "warrant_conclusion": "supported"},
                {"subject_id": "SUB-B", "access_status": "not-observed",
                 "route_refs": [], "subject_relative_conditions": ["route access not observed"],
                 "assessor_id": "ASSESSOR-1", "assessor_evidence": ["ev-access-b"],
                 "defeaters": ["new access evidence"], "warrant_conclusion": "held"},
            ],
            "non_claims": [
                "machine source-independence does not establish tawatur warrant",
                "count popularity graph degree and institutional persistence do not establish warrant",
                "subject access does not alter objective proposition truth",
            ],
        }],
    }


def valid_claim():
    return {
        "claim_id": "NC-CONTROL",
        "target_bearer": "m_discourse",
        "target_id": "objection-utterance-abc123",
        "target_version": "as-received",
        "target_type": "overt-discourse",
        "analysis_id": "A",
        "analysis_version": "v1",
        "proposition_identity": "PROP-CONTROL",
        "proposition_truth_status": "not-adjudicated",
        "proposition": "a bounded discourse claim",
        "claim_role": "secondary-reconstruction",
        "source_status_refs": ["ELT-1"],
        "evidence_access_status": "secondary-reconstruction",
        "comparison_scope": "not-applicable",
        "candidate_alternatives": [],
        "evidence_ids": ["ev-wording-1"],
        "support_rule": "structural",
        "uncertainty": {"level": "low", "basis": "observed wording"},
        "status": "asserted",
        "defeaters": ["contrary evidence"],
        "non_claims": ["no interior claim"],
    }


class TawaturContractTests(unittest.TestCase):
    def issues(self, doc):
        return MEMETIC.validate_tawatur_document(doc, {"ELT-3"})

    def test_closed_versioned_schema_accepts_qualitative_control(self):
        schema = json.loads((APP / "TAWATUR-WARRANT.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(valid_warrant(), schema)
        self.assertEqual([], self.issues(valid_warrant()))

    def test_count_popularity_and_degree_cannot_supply_warrant(self):
        for field in ("witness_count", "popularity", "graph_degree", "institutional_persistence"):
            with self.subTest(field=field):
                case = valid_warrant()
                case["assessments"][0][field] = 100
                self.assertTrue(self.issues(case))

    def test_common_cause_cannot_be_declared_independent(self):
        case = valid_warrant()
        case["assessments"][0]["origin_analysis"]["common_cause_status"] = "detected"
        self.assertIn("common-cause-conflicts-with-independence", self.issues(case))

    def test_quality_and_subject_context_are_required(self):
        for field in ("transmitter_quality", "subject_assessments"):
            with self.subTest(field=field):
                case = valid_warrant()
                del case["assessments"][0][field]
                self.assertTrue(self.issues(case))

    def test_honesty_and_competence_are_independent_required_dimensions(self):
        for field in ("honesty_or_trust", "domain_competence"):
            with self.subTest(field=field):
                case = valid_warrant()
                del case["assessments"][0]["transmitter_quality"][0][field]
                self.assertTrue(self.issues(case))

    def test_duplicate_source_units_reject(self):
        case = valid_warrant()
        case["assessments"][0]["source_units"].append(
            copy.deepcopy(case["assessments"][0]["source_units"][0]))
        self.assertIn("duplicate-source-unit", self.issues(case))

    def test_subject_access_cannot_rewrite_objective_truth(self):
        case = valid_warrant()
        case["assessments"][0]["subject_assessments"][1]["objective_truth_status"] = "false"
        self.assertTrue(self.issues(case))

    def test_malformed_nested_values_reject_without_traceback(self):
        for malformed in (None, "not-a-map", ["not", "a", "record"]):
            with self.subTest(malformed=malformed):
                case = valid_warrant()
                case["assessments"][0]["origin_analysis"] = malformed
                issues = self.issues(case)
                self.assertTrue(issues)
                self.assertTrue(all("Traceback" not in issue for issue in issues))


class ClaimRoleAndMentalBoundaryTests(unittest.TestCase):
    def issues(self, claim):
        return NOETIC.claim_semantic_issues(claim, {
            "ELT-1": "SECONDARY_RECONSTRUCTION",
            "ELT-3": "SECONDARY_VERIFIED",
            "EXT-1": "ORTHEMOLOGICAL_EXTENSION",
        })

    def test_claim_role_and_access_status_are_distinct(self):
        case = valid_claim()
        case["claim_role"] = "SECONDARY_VERIFIED"
        self.assertIn("invalid-claim-role", self.issues(case))
        case = valid_claim()
        case["source_status_refs"] = ["computational-analogy"]
        self.assertIn("unresolved-source-status-ref", self.issues(case))

    def test_computational_analogy_is_a_claim_role_only(self):
        case = valid_claim()
        case["claim_role"] = "computational-analogy"
        case["source_status_refs"] = ["EXT-1"]
        case["evidence_access_status"] = "orthemological-extension"
        case["non_claims"] = ["the model validates neither Orthemology nor theology"]
        self.assertEqual([], self.issues(case))

    def test_evidence_access_status_must_match_resolved_registry_owner(self):
        case = valid_claim()
        case["evidence_access_status"] = "primary-text-exact"
        self.assertIn("evidence-access-status-mismatch", self.issues(case))
        case = valid_claim()
        case["source_status_refs"] = ["ELT-1", "EXT-1"]
        self.assertIn("evidence-access-status-mismatch", self.issues(case))

    def test_modern_comparison_cannot_claim_primary_text_status(self):
        case = valid_claim()
        case["comparison_scope"] = "modern-comparison"
        case["claim_role"] = "primary-text-verified"
        self.assertIn("modern-comparison-not-primary", self.issues(case))
        case["claim_role"] = "secondary-reconstruction"
        self.assertEqual([], self.issues(case))

    def test_direct_mental_to_external_entailments_reject(self):
        pairs = [
            ("mental-conceivability", "external-possibility"),
            ("universal-abstraction", "external-existence"),
            ("model-representation", "unseen-modality"),
        ]
        for source, target in pairs:
            with self.subTest(source=source, target=target):
                case = valid_claim()
                case["inference_boundary"] = {
                    "source_kind": source,
                    "conclusion_kind": target,
                    "bridge_status": "direct-entailment",
                    "bridge_evidence_ids": [],
                }
                self.assertIn("mental-external-direct-entailment", self.issues(case))

    def test_separately_warranted_external_bridge_accepts(self):
        case = valid_claim()
        case["inference_boundary"] = {
            "source_kind": "mental-conceivability",
            "conclusion_kind": "external-possibility",
            "bridge_status": "independently-warranted",
            "bridge_evidence_ids": ["ev-external-premise"],
        }
        self.assertEqual([], self.issues(case))

    def test_malformed_inference_boundary_rejects_without_traceback(self):
        case = valid_claim()
        case["inference_boundary"] = ["bad-shape"]
        issues = self.issues(case)
        self.assertTrue(issues)
        self.assertTrue(all("Traceback" not in issue for issue in issues))


class FitrahBoundaryTests(unittest.TestCase):
    def boundary(self):
        return {
            "status": "creed-internal",
            "model_properties": ["qualitative", "defeasible", "multidimensional"],
            "is": ["normative-disposition", "proper-function-orientation"],
            "is_not": ["measurable-scalar", "field-coordinate", "metaortheme", "algorithm",
                       "discourse-readable-soul-state", "guaranteed-attractor"],
            "corruption_assessment": {
                "requires_independent_evidence": True,
                "dissent_alone_sufficient": False,
                "interior_status": "held-or-underdetermined",
            },
        }

    def test_qualitative_defeasible_multidimensional_control_accepts(self):
        self.assertEqual([], META.validate_fitrah_boundary(self.boundary()))

    def test_each_reified_or_interior_model_rejects_when_not_forbidden(self):
        for prohibited in ("measurable-scalar", "field-coordinate", "metaortheme", "algorithm",
                           "discourse-readable-soul-state", "guaranteed-attractor"):
            with self.subTest(prohibited=prohibited):
                case = self.boundary()
                case["is_not"].remove(prohibited)
                self.assertTrue(META.validate_fitrah_boundary(case))

    def test_dissent_alone_cannot_establish_corruption(self):
        case = self.boundary()
        case["corruption_assessment"]["dissent_alone_sufficient"] = True
        self.assertIn("dissent-alone-circular", META.validate_fitrah_boundary(case))

    def test_malformed_boundary_rejects_without_traceback(self):
        for malformed in (None, "fitrah", []):
            with self.subTest(malformed=malformed):
                issues = META.validate_fitrah_boundary(malformed)
                self.assertTrue(issues)
                self.assertTrue(all("Traceback" not in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
