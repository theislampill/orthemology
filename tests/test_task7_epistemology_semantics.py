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

    def test_source_unit_origin_and_path_overlap_constrain_independence(self):
        cases = {
            "shared-origin": ("origin_id", "source-origin-common-cause-conflict"),
            "shared-path": ("transmission_paths", "source-path-independence-conflict"),
        }
        for label, (field, expected_issue) in cases.items():
            with self.subTest(label=label):
                case = valid_warrant()
                units = case["assessments"][0]["source_units"]
                units[1][field] = copy.deepcopy(units[0][field])
                self.assertIn(expected_issue, self.issues(case))

    def test_supported_warrant_requires_plural_qualifying_routes(self):
        case = valid_warrant()
        assessment = case["assessments"][0]
        assessment["acquisition_routes"] = assessment["acquisition_routes"][:1]
        assessment["subject_assessments"][0]["route_refs"] = ["AR-1"]
        self.assertIn("supported-warrant-requires-plural-routes", self.issues(case))

    def test_supported_warrant_routes_must_be_independent_and_quality_supported(self):
        cases = {
            "same-source-unit": "supported-warrant-routes-not-independent",
            "quality-underdetermined": "supported-warrant-route-quality-insufficient",
        }
        for label, expected_issue in cases.items():
            with self.subTest(label=label):
                case = valid_warrant()
                assessment = case["assessments"][0]
                if label == "same-source-unit":
                    assessment["acquisition_routes"][1]["source_unit_ids"] = ["SU-1"]
                else:
                    assessment["transmitter_quality"][1]["domain_competence"] = "underdetermined"
                self.assertIn(expected_issue, self.issues(case))

    def test_supported_warrant_requires_all_qualitative_dimensions(self):
        mutations = {
            "common-cause": lambda assessment: assessment["origin_analysis"].update(
                {"common_cause_status": "detected", "path_independence": "rejected"}),
            "copying": lambda assessment: assessment["origin_analysis"].update(
                {"copying_status": "detected", "path_independence": "rejected"}),
            "non-collusion-rejected": lambda assessment: assessment["origin_analysis"].update(
                {"non_collusion": "rejected"}),
            "non-collusion-underdetermined": lambda assessment: assessment["origin_analysis"].update(
                {"non_collusion": "underdetermined"}),
            "single-lineage": lambda assessment: assessment["origin_analysis"].update(
                {"mutation_lineage": "single-lineage-detected"}),
            "content-incoherent": lambda assessment: assessment["content_coherence"].update(
                {"status": "rejected"}),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                case = valid_warrant()
                mutate(case["assessments"][0])
                self.assertTrue(self.issues(case))

    def test_adverse_qualitative_dimension_remains_representable_when_held(self):
        case = valid_warrant()
        assessment = case["assessments"][0]
        assessment["origin_analysis"]["non_collusion"] = "rejected"
        assessment["subject_assessments"][0]["warrant_conclusion"] = "held"
        self.assertEqual([], self.issues(case))

    def test_held_single_route_record_remains_representable(self):
        case = valid_warrant()
        assessment = case["assessments"][0]
        assessment["acquisition_routes"] = assessment["acquisition_routes"][:1]
        subject = assessment["subject_assessments"][0]
        subject["access_status"] = "underdetermined"
        subject["route_refs"] = ["AR-1"]
        subject["warrant_conclusion"] = "held"
        self.assertEqual([], self.issues(case))

    def test_proposition_identity_preserves_text_and_objective_truth(self):
        control = valid_warrant()
        second = copy.deepcopy(control["assessments"][0])
        second["id"] = "TWW-SECOND"
        second["subject_assessments"][0]["subject_id"] = "SUB-SECOND"
        control["assessments"].append(second)
        self.assertEqual([], self.issues(control))

        conflicts = {
            "truth": ("objective_truth_status", "false", "proposition-identity-truth-conflict"),
            "text": ("text", "a conflicting proposition text", "proposition-identity-text-conflict"),
        }
        for label, (field, value, expected_issue) in conflicts.items():
            with self.subTest(label=label):
                case = copy.deepcopy(control)
                case["assessments"][1]["proposition"][field] = value
                self.assertIn(expected_issue, self.issues(case))

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

    def test_cross_record_nested_values_reject_without_exception(self):
        mutations = {
            "proposition-id": lambda assessment: assessment["proposition"].update(
                {"id": {"nested": "PROP-P"}}),
            "source-status-refs": lambda assessment: assessment.update(
                {"source_status_refs": [{"nested": "ELT-3"}]}),
            "source-unit-id": lambda assessment: assessment["source_units"][0].update(
                {"unit_id": {"nested": "SU-1"}}),
            "source-origin-id": lambda assessment: assessment["source_units"][0].update(
                {"origin_id": {"nested": "O-1"}}),
            "source-transmission-paths": lambda assessment: assessment["source_units"][0].update(
                {"transmission_paths": None}),
            "quality-source-unit-id": lambda assessment: assessment["transmitter_quality"][0].update(
                {"source_unit_id": {"nested": "SU-1"}}),
            "route-id": lambda assessment: assessment["acquisition_routes"][0].update(
                {"route_id": {"nested": "AR-1"}}),
            "route-source-unit-ids": lambda assessment: assessment["acquisition_routes"][0].update(
                {"source_unit_ids": [{"nested": "SU-1"}]}),
            "subject-id": lambda assessment: assessment["subject_assessments"][0].update(
                {"subject_id": {"nested": "SUB-A"}}),
            "subject-route-refs": lambda assessment: assessment["subject_assessments"][0].update(
                {"route_refs": None}),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                case = valid_warrant()
                mutate(case["assessments"][0])
                try:
                    issues = self.issues(case)
                except Exception as exc:  # pragma: no cover - regression assertion
                    self.fail("validator raised %s: %s" % (type(exc).__name__, exc))
                self.assertTrue(issues)
                self.assertTrue(all("Traceback" not in issue for issue in issues))


class ClaimRoleAndMentalBoundaryTests(unittest.TestCase):
    def issues(self, claim):
        return NOETIC.claim_semantic_issues(claim, {
            "ELT-1": "SECONDARY_RECONSTRUCTION",
            "ELT-3": "SECONDARY_VERIFIED",
            "EXT-1": "ORTHEMOLOGICAL_EXTENSION",
        })

    def external_claim_context(self):
        occurrences = {
            "m_discourse": {
                "identity": "objection-utterance-abc123",
                "version": "as-received",
                "in_scope": True,
            }
        }
        source_statuses = {"ELT-1": "SECONDARY_RECONSTRUCTION"}
        claim = valid_claim()
        claim["target_type"] = "external-possibility"
        claim["inference_boundary"] = {
            "source_kind": "mental-conceivability",
            "conclusion_kind": "external-possibility",
            "bridge_status": "independently-warranted",
            "bridge_evidence_ids": ["ev-authoritative-external-premise"],
        }
        return claim, occurrences, source_statuses

    def evidence_records(self):
        registry = json.loads(
            (APP / "NOETIC-EVIDENCE-REGISTRY.example.json").read_text(encoding="utf-8")
        )
        return {record["evidence_id"]: record for record in registry["evidence"]}

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
        case["target_type"] = "external-possibility"
        case["inference_boundary"] = {
            "source_kind": "mental-conceivability",
            "conclusion_kind": "external-possibility",
            "bridge_status": "independently-warranted",
            "bridge_evidence_ids": ["ev-authoritative-external-premise"],
        }
        self.assertEqual([], NOETIC.claim_semantic_issues(
            case,
            {
                "ELT-1": "SECONDARY_RECONSTRUCTION",
                "ELT-3": "SECONDARY_VERIFIED",
                "EXT-1": "ORTHEMOLOGICAL_EXTENSION",
            },
            self.evidence_records(),
        ))

    def test_external_bridge_control_resolves_and_accepts(self):
        control, occurrences, source_statuses = self.external_claim_context()
        self.assertEqual(
            (True, None),
            NOETIC.claim_supported(
                control, self.evidence_records(), occurrences, source_statuses
            ),
        )

    def test_external_bridge_requires_typed_current_valid_relevant_evidence(self):
        control, occurrences, source_statuses = self.external_claim_context()
        records = self.evidence_records()
        control["inference_boundary"]["bridge_evidence_ids"] = ["ev-external-premise"]
        records["ev-external-premise"] = {
            "evidence_id": "ev-external-premise",
            "observed_occurrence": "m_external_premise",
            "property_class": "provenance",
            "provenance": "independent evidence for the external premise",
            "scope": "external-possibility",
            "currentness": "current",
            "validity": "valid",
            "relation_to_target": "independently supports the external conclusion",
            "support_roles": ["mental-external-bridge"],
            "supported_target_types": ["external-possibility"],
        }
        self.assertEqual(
            (True, None),
            NOETIC.claim_supported(control, records, occurrences, source_statuses),
        )

        for evidence_id in ("ev-reread-1", "ev-route-1"):
            with self.subTest(evidence_id=evidence_id):
                case = copy.deepcopy(control)
                case["inference_boundary"]["bridge_evidence_ids"] = [evidence_id]
                self.assertEqual(
                    (False, "bridge-evidence-not-authoritative"),
                    NOETIC.claim_supported(case, records, occurrences, source_statuses),
                )

    def test_malformed_structured_claim_scalars_reject_without_exception(self):
        mutations = {
            "claim-role": lambda claim: claim.update(
                {"claim_role": {"nested": "secondary-reconstruction"}}),
            "access-status": lambda claim: claim.update(
                {"evidence_access_status": {"nested": "secondary-reconstruction"}}),
            "target-type": lambda claim: claim.update(
                {"target_type": {"nested": "overt-discourse"}}),
            "source-kind": lambda claim: claim["inference_boundary"].update(
                {"source_kind": {"nested": "mental-conceivability"}}),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                case, occurrences, source_statuses = self.external_claim_context()
                mutate(case)
                try:
                    ok, rule = NOETIC.claim_supported(
                        case, self.evidence_records(), occurrences, source_statuses
                    )
                except Exception as exc:  # pragma: no cover - regression assertion
                    self.fail("validator raised %s: %s" % (type(exc).__name__, exc))
                self.assertFalse(ok)
                self.assertIsInstance(rule, str)

    def test_malformed_typed_bridge_record_rejects_without_exception(self):
        control, occurrences, source_statuses = self.external_claim_context()
        mutations = {
            "support-roles-null": lambda record: record.update({"support_roles": None}),
            "target-types-map": lambda record: record.update(
                {"supported_target_types": {"nested": "external-possibility"}}),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                records = self.evidence_records()
                mutate(records["ev-authoritative-external-premise"])
                try:
                    result = NOETIC.claim_supported(
                        control, records, occurrences, source_statuses
                    )
                except Exception as exc:  # pragma: no cover - regression assertion
                    self.fail("validator raised %s: %s" % (type(exc).__name__, exc))
                self.assertEqual((False, "bridge-evidence-not-authoritative"), result)

    def test_external_bridge_evidence_must_resolve(self):
        control, occurrences, source_statuses = self.external_claim_context()
        unresolved = copy.deepcopy(control)
        unresolved["inference_boundary"]["bridge_evidence_ids"] = ["ev-missing"]
        self.assertEqual(
            (False, "bridge-evidence-unresolved"),
            NOETIC.claim_supported(unresolved, {"ev-wording-1"}, occurrences, source_statuses),
        )

    def test_asserted_external_conclusion_rejects_held_bridge(self):
        control, occurrences, source_statuses = self.external_claim_context()
        held = copy.deepcopy(control)
        held["inference_boundary"]["bridge_status"] = "held"
        held["inference_boundary"]["bridge_evidence_ids"] = []
        self.assertEqual(
            (False, "asserted-external-conclusion-without-warranted-bridge"),
            NOETIC.claim_supported(held, {"ev-wording-1"}, occurrences, source_statuses),
        )

    def test_inference_conclusion_kind_must_match_claim_target(self):
        case = valid_claim()
        case["target_type"] = "external-existence"
        case["inference_boundary"] = {
            "source_kind": "mental-conceivability",
            "conclusion_kind": "external-possibility",
            "bridge_status": "independently-warranted",
            "bridge_evidence_ids": ["ev-wording-1"],
        }
        self.assertIn("inference-conclusion-target-mismatch", self.issues(case))

    def test_malformed_inference_boundary_rejects_without_traceback(self):
        case = valid_claim()
        case["inference_boundary"] = ["bad-shape"]
        issues = self.issues(case)
        self.assertTrue(issues)
        self.assertTrue(all("Traceback" not in issue for issue in issues))

    def test_malformed_bridge_evidence_ids_reject_without_exception(self):
        case, occurrences, source_statuses = self.external_claim_context()
        case["inference_boundary"]["bridge_evidence_ids"] = [{"nested": "ev-wording-1"}]
        try:
            result = NOETIC.claim_supported(
                case, {"ev-wording-1"}, occurrences, source_statuses
            )
        except Exception as exc:  # pragma: no cover - regression assertion
            self.fail("validator raised %s: %s" % (type(exc).__name__, exc))
        self.assertEqual((False, "malformed-bridge-evidence-ids"), result)

    def test_malformed_claim_evidence_ids_reject_without_exception(self):
        case, occurrences, source_statuses = self.external_claim_context()
        case["evidence_ids"] = [{"nested": "ev-wording-1"}]
        try:
            result = NOETIC.claim_supported(
                case, {"ev-wording-1"}, occurrences, source_statuses
            )
        except Exception as exc:  # pragma: no cover - regression assertion
            self.fail("validator raised %s: %s" % (type(exc).__name__, exc))
        self.assertEqual((False, "malformed-evidence-ids"), result)


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

    def test_qualitative_metadata_control_accepts(self):
        case = self.boundary()
        case["rejected_analogy"] = "minimum-entropy attractor is not adopted"
        self.assertEqual([], META.validate_fitrah_boundary(case))

    def test_rejected_analogy_remains_qualitative_metadata(self):
        control = self.boundary()
        control["rejected_analogy"] = "minimum-entropy attractor is not adopted"
        self.assertEqual([], META.validate_fitrah_boundary(control))

        structured_payloads = {
            "scalar-score": {"scalar_score": 0.8},
            "nested-field-coordinate": {"nested": {"field_coordinate": [1, 2]}},
            "nested-soul-state-readout": {
                "nested": {"soul_state_readout": "guided"},
            },
        }
        for label, payload in structured_payloads.items():
            with self.subTest(label=label):
                case = self.boundary()
                case["rejected_analogy"] = payload
                issues = META.validate_fitrah_boundary(case)
                self.assertIn("fitrah-rejected-analogy-not-qualitative", issues)
                self.assertTrue(all("Traceback" not in issue for issue in issues))

    def test_explicit_reifying_fields_reject_at_every_allowed_level(self):
        mutations = {
            "top-level-scalar": lambda boundary: boundary.update({"scalar_score": 0.9}),
            "top-level-coordinate": lambda boundary: boundary.update(
                {"field_coordinate": [0.2, 0.8]}),
            "nested-soul-readout": lambda boundary: boundary["corruption_assessment"].update(
                {"soul_state_readout": "corrupt"}),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                case = self.boundary()
                mutate(case)
                self.assertTrue(META.validate_fitrah_boundary(case))

    def test_each_reified_or_interior_model_rejects_when_not_forbidden(self):
        for prohibited in ("measurable-scalar", "field-coordinate", "metaortheme", "algorithm",
                           "discourse-readable-soul-state", "guaranteed-attractor"):
            with self.subTest(prohibited=prohibited):
                case = self.boundary()
                case["is_not"].remove(prohibited)
                self.assertTrue(META.validate_fitrah_boundary(case))

    def test_forbidden_positive_fitrah_property_rejects(self):
        positive = self.boundary()
        positive["is"].append("discourse-readable-soul-state")
        positive_issues = META.validate_fitrah_boundary(positive)
        self.assertIn("fitrah-positive-model-forbidden", positive_issues)
        self.assertIn("fitrah-positive-negative-conflict", positive_issues)

    def test_quantitative_fitrah_property_rejects(self):
        quantitative = self.boundary()
        quantitative["model_properties"].append("quantitative")
        self.assertIn("fitrah-properties-forbidden", META.validate_fitrah_boundary(quantitative))

    def test_positive_and_negative_vocabularies_cannot_intersect(self):
        case = self.boundary()
        case["is_not"].append("normative-disposition")
        self.assertIn("fitrah-positive-negative-conflict", META.validate_fitrah_boundary(case))

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

    def test_malformed_nested_fitrah_vocabularies_reject_without_exception(self):
        for field in ("model_properties", "is", "is_not"):
            with self.subTest(field=field):
                case = self.boundary()
                case[field].append({"nested": "value"})
                issues = META.validate_fitrah_boundary(case)
                self.assertTrue(issues)
                self.assertTrue(all("Traceback" not in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
