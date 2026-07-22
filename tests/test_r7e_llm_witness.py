#!/usr/bin/env python3
"""Focused Task 5 tests for the bounded R7E LLM-mediated witness."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_r7e_llm_witness.py"
SCHEMA = ROOT / "schemas" / "llm-mediated-orthing-witness.schema.json"
WITNESS = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-LLM-MEDIATED-ORTHING-WITNESS.yaml"
CROSSWALK = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-SOMNIC-CASE-CROSSWALK.yaml"
NARRATIVE = ROOT / "docs" / "project-closure" / "r7e-sol" / "R7E-LLM-MEDIATED-ORTHING-WITNESS.md"


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("validate_r7e_llm_witness", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def production_exit(witness: object, crosswalk: object, narrative: str):
    module = load_module()
    if module is None:
        return 1, "[FAIL] Task 5 production validator is missing\nTOTAL: 1 failures\n"
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        issues = module.collect_issues(witness, crosswalk, narrative)
        for issue in issues:
            print("[FAIL] %s" % issue)
        print("TOTAL: %d failures" % len(issues))
    return (1 if issues else 0), output.getvalue()


def bounded_control() -> tuple[dict, dict, str]:
    witness = {
        "schema": "orthemology-llm-mediated-orthing-witness-v1",
        "status": "current-candidate",
        "witness_id": "R7E-LLM-WITNESS-001",
        "declared_analysis": {
            "analysis_id": "A-R7E-LLM-WITNESS",
            "scope": "retrospective classification of repository-preserved R7E evidence",
            "evidence_refs": ["E-R7E-STATE", "E-R7E-PROVENANCE"],
        },
        "classifications": {
            "llm_applicability": "supported",
            "llm_mediated_realizability": "partially-supported",
            "comparative_utility": "not-established",
        },
        "original_history": {
            "capture_mode": "retrospective_reconstruction",
            "episode_cardinality": "underdetermined",
            "authoritative_identity_evidence_refs": [],
            "original_t1_checkpoint_status": "missing",
            "original_t1_evidence_status": "not-observed",
        },
        "identity_records": [
            {"identity_kind": "turn", "status": "unknown", "identifier": None},
            {"identity_kind": "session", "status": "unresolved", "identifier": None},
            {"identity_kind": "episode", "status": "underdetermined", "identifier": None},
            {"identity_kind": "occurrence", "status": "unresolved", "identifier": None},
            {"identity_kind": "orthing", "status": "unresolved", "identifier": None},
            {"identity_kind": "reconstruction_event", "status": "reconstruction-only", "identifier": "EV-R7E-RETRO-001"},
        ],
        "evidence_registry": [
            {"evidence_id": "E-R7E-STATE", "source_ref": "docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json", "state": "repository-verified", "claim_boundary": "file identity only; workflow claims remain attributed"},
            {"evidence_id": "E-R7E-PROVENANCE", "source_ref": "docs/project-closure/r7e-sol/R7E-INPUT-PROVENANCE.json", "state": "repository-verified", "claim_boundary": "current provenance accounting only"},
            {"evidence_id": "E-WORKFLOW-JOURNAL", "source_ref": "workflow journal", "state": "missing", "claim_boundary": "no original event or checkpoint reconstruction"},
            {"evidence_id": "E-PER-AGENT-REPORTS", "source_ref": "per-agent reports", "state": "missing", "claim_boundary": "no independent role reconstruction"},
            {"evidence_id": "E-FULL-DRAFTS", "source_ref": "full candidate drafts", "state": "missing", "claim_boundary": "no complete candidate reconstruction"},
            {"evidence_id": "E-REJECTIONS-PRESERVED", "source_ref": "eight repository rejection bullets", "state": "repository-verified", "claim_boundary": "preserved records only"},
            {"evidence_id": "E-REJECTIONS-MISSING", "source_ref": "eight reported rejection records", "state": "missing", "claim_boundary": "absent records are not inferred"},
            {"evidence_id": "E-ATTACHMENTS", "source_ref": "supplied R7E attachments", "state": "attachment-observed", "claim_boundary": "original-run binding unresolved"},
            {"evidence_id": "E-AGGREGATE-STATISTICS", "source_ref": "R7E implementing-run aggregate statistics", "state": "implementing-run-attributed", "claim_boundary": "not repository fact or independent reconstruction"},
            {"evidence_id": "E-SOL-REVIEW", "source_ref": "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml", "state": "repository-verified", "claim_boundary": "later review evidence only"},
        ],
        "witness_objects": [
            {"object_id": "WO-ORTHEMMATA", "object_kind": "orthemmata", "illustration_role": "retrospective-reconstruction", "evidence_refs": ["E-R7E-STATE"], "description": "The preserved repository sources bound the reconstructed cases without supplying original target identities."},
            {"object_id": "WO-ANALYSIS", "object_kind": "declared-analysis", "illustration_role": "schema-conformant-illustrative-mapping", "evidence_refs": ["E-R7E-PROVENANCE"], "description": "The present analysis is a later classification owner, not an original runtime record."},
            {"object_id": "WO-ROLES", "object_kind": "executor-subagent-roles", "illustration_role": "documented-historical-fact", "evidence_refs": ["E-R7E-STATE", "E-AGGREGATE-STATISTICS"], "description": "The repository preserves an LLM-mediated orchestration account while its aggregate details remain attributed."},
            {"object_id": "WO-GOVERNING", "object_kind": "governing-types", "illustration_role": "schema-conformant-illustrative-mapping", "evidence_refs": ["E-R7E-PROVENANCE"], "description": "Existing episode, evidence, route, verdict, and governance types supply a bounded retrospective mapping."},
            {"object_id": "WO-BINDINGS", "object_kind": "case-bound-applications", "illustration_role": "unsupported-live-runtime-claim", "evidence_refs": ["E-WORKFLOW-JOURNAL"], "description": "Original case-bound runtime bindings are not observed."},
            {"object_id": "WO-SOURCES", "object_kind": "sources", "illustration_role": "documented-historical-fact", "evidence_refs": ["E-R7E-STATE", "E-R7E-PROVENANCE"], "description": "Repository source identities and current provenance accounting are documented."},
            {"object_id": "WO-CANDIDATES", "object_kind": "candidate-findings-profiles", "illustration_role": "retrospective-reconstruction", "evidence_refs": ["E-FULL-DRAFTS", "E-REJECTIONS-PRESERVED", "E-REJECTIONS-MISSING"], "description": "Occurrence-level remnants are reconstructible, while complete drafts and rejection records are not."},
            {"object_id": "WO-ROUTES", "object_kind": "routes", "illustration_role": "retrospective-reconstruction", "evidence_refs": ["E-R7E-STATE", "E-WORKFLOW-JOURNAL"], "description": "Phase-level routing is reported, but original event-level routes are unavailable."},
            {"object_id": "WO-ACTIONS", "object_kind": "integrated-actions", "illustration_role": "documented-historical-fact", "evidence_refs": ["E-R7E-STATE", "E-SOL-REVIEW"], "description": "Repository diffs document integrated candidate actions without establishing correctness."},
            {"object_id": "WO-RESIDUAL", "object_kind": "residual-backlog", "illustration_role": "documented-historical-fact", "evidence_refs": ["E-R7E-PROVENANCE"], "description": "The current provenance ledger documents unresolved residuals and duplicate historical IDs."},
            {"object_id": "WO-SUCCESSOR", "object_kind": "successor-state", "illustration_role": "documented-historical-fact", "evidence_refs": ["E-SOL-REVIEW"], "description": "The later repository candidate state is documented without a runtime continuity claim."},
            {"object_id": "WO-AUDIT", "object_kind": "higher-order-audit", "illustration_role": "retrospective-reconstruction", "evidence_refs": ["E-SOL-REVIEW"], "description": "The Sol review is a later human and LLM-mediated retrospective assessment."},
        ],
        "higher_order_audit": {
            "audit_id": "R7E-SOL-RETRO-AUDIT-001",
            "subject_witness_id": "R7E-LLM-WITNESS-001",
            "audit_authority_id": "R7E-SOL-INDEPENDENT-REVIEW",
            "implementing_authority_id": "R7E-IMPLEMENTING-RUN",
            "self_certifying": False,
            "assessment_kind": "human-llm-mediated-retrospective-assessment",
            "meta_orthability_disposition": "record-insufficient",
            "somnic_conformance": "not-established",
            "authoritative_target_identity_status": "unresolved",
            "target_history_checkpoint_status": "missing",
            "target_history_digest_status": "not-observed",
            "original_t1_evidence_refs": [],
            "later_evidence_refs": ["E-SOL-REVIEW"],
        },
        "claim_boundaries": {
            "correctness": "not-established",
            "empirical_validation": "not-established",
            "terminology_benefit_or_adoption": "not-established",
            "exact_internal_model_ontology": "not-established",
            "cross_model_or_domain_generalization": "not-established",
            "live_append_only_capture": "not-observed",
            "claimant_contract_enforcement": "not-observed",
            "recurrence_detection": "not-observed",
            "idempotent_frontier_processing": "not-observed",
            "full_somnus_writeback_chain": "not-implemented",
            "nightly_autonomy": "not-implemented",
            "runtime_deployment": "not-implemented",
        },
        "proof_protocol_placement": {
            "status": "requires-separately-numbered-reviewed-follow-up",
            "concepts": ["PoW", "PoR", "Proof-of-Orth", "capability-grant", "execution-receipt"],
            "implemented": False,
            "normative_owner_created": False,
        },
    }
    crosswalk = {
        "schema": "orthemology-r7e-somnic-case-crosswalk-v1",
        "status": "current-candidate",
        "witness_ref": "R7E-LLM-WITNESS-001",
        "source_case": "R7E",
        "original_history": {
            "episode_cardinality": "underdetermined",
            "target_identity_status": "unresolved",
            "t1_checkpoint_status": "missing",
            "t1_evidence_partition_status": "not-observed",
            "capture_mode": "retrospective_reconstruction",
        },
        "later_review": {
            "audit_ref": "R7E-SOL-RETRO-AUDIT-001",
            "assessment_kind": "human-llm-mediated-retrospective-assessment",
            "meta_orthability_disposition": "record-insufficient",
            "somnic_conformance": "not-established",
        },
        "relation_disposition": {
            "inter_somnic_relation": "not-established",
            "temporal_separation_is_sufficient": False,
            "reason": "Authoritative episode and assessment identities are unavailable.",
        },
        "illustration_roles": [
            "documented-historical-fact",
            "retrospective-reconstruction",
            "schema-conformant-illustrative-mapping",
            "unsupported-live-runtime-claim",
        ],
        "evidence_refs": ["E-R7E-STATE", "E-R7E-PROVENANCE", "E-SOL-REVIEW"],
    }
    narrative = """# Bounded R7E LLM-mediated orthing witness

This record classifies only the evidence-qualified witness in `R7E-LLM-WITNESS-001`. The repository documents an LLM-mediated implementing account through `E-R7E-STATE`, while `E-R7E-PROVENANCE` preserves the missing journal, reports, drafts, and original identity bindings. The later Sol record `E-SOL-REVIEW` is a human and LLM-mediated retrospective assessment with record-insufficient meta-orthability, not deployed Somnus.

The classification supports LLM applicability, partially supports bounded LLM-mediated realizability, and does not establish comparative utility, correctness, empirical validation, terminology benefit or adoption, exact internal model ontology, cross-model or cross-domain generalization, live append-only capture, claimant-contract enforcement, recurrence detection, idempotent frontier processing, a full writeback chain, nightly autonomy, or runtime deployment.
"""
    return witness, crosswalk, narrative


class R7ELLMWitnessTests(unittest.TestCase):
    def assertAccepted(self, witness=None, crosswalk=None, narrative=None):
        valid_witness, valid_crosswalk, valid_narrative = bounded_control()
        exit_code, output = production_exit(
            valid_witness if witness is None else witness,
            valid_crosswalk if crosswalk is None else crosswalk,
            valid_narrative if narrative is None else narrative,
        )
        self.assertEqual(0, exit_code, output)

    def assertRejected(self, witness=None, crosswalk=None, narrative=None, fragment=None):
        valid_witness, valid_crosswalk, valid_narrative = bounded_control()
        exit_code, output = production_exit(
            valid_witness if witness is None else witness,
            valid_crosswalk if crosswalk is None else crosswalk,
            valid_narrative if narrative is None else narrative,
        )
        self.assertEqual(1, exit_code, output)
        self.assertNotIn("Traceback", output)
        if fragment:
            self.assertIn(fragment, output)

    def test_neighboring_bounded_control_accepts(self):
        self.assertAccepted()

    def test_canonical_schema_and_records_accept(self):
        self.assertTrue(SCHEMA.exists(), "Task 5 schema is missing")
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        witness = yaml.safe_load(WITNESS.read_text(encoding="utf-8"))
        crosswalk = yaml.safe_load(CROSSWALK.read_text(encoding="utf-8"))
        narrative = NARRATIVE.read_text(encoding="utf-8")
        self.assertFalse(list(Draft202012Validator(schema).iter_errors(witness)))
        self.assertAccepted(witness, crosswalk, narrative)

    def test_rejects_invented_episode_cardinality_or_identity(self):
        witness, _, _ = bounded_control()
        witness["original_history"]["episode_cardinality"] = "single-episode"
        self.assertRejected(witness=witness, fragment="episode cardinality")

    def test_rejects_invented_original_identity_without_authoritative_evidence(self):
        witness, _, _ = bounded_control()
        session = next(row for row in witness["identity_records"] if row["identity_kind"] == "session")
        session["status"] = "repository-verified"
        session["identifier"] = "R7E-ORIGINAL-SESSION-001"
        self.assertRejected(witness=witness, fragment="original identity")

    def test_rejects_missing_artifact_promoted_to_verified(self):
        witness, _, _ = bounded_control()
        witness["evidence_registry"][2]["state"] = "repository-verified"
        self.assertRejected(witness=witness, fragment="missing source")

    def test_rejects_missing_artifact_laundered_through_source_rename(self):
        witness, _, _ = bounded_control()
        witness["evidence_registry"][2]["source_ref"] = "available workflow journal"
        witness["evidence_registry"][2]["state"] = "repository-verified"
        self.assertRejected(witness=witness, fragment="evidence inventory")

    def test_rejects_attributed_statistic_promoted_to_repository_fact(self):
        witness, _, _ = bounded_control()
        witness["evidence_registry"][8]["state"] = "repository-verified"
        self.assertRejected(witness=witness, fragment="attributed statistic")

    def test_rejects_repository_source_demotion_under_supported_classification(self):
        witness, _, _ = bounded_control()
        witness["evidence_registry"][0]["state"] = "missing"
        self.assertRejected(witness=witness, fragment="must retain evidence state")

    def test_rejects_duplicate_witness_object_ids(self):
        witness, _, _ = bounded_control()
        witness["witness_objects"][1]["object_id"] = witness["witness_objects"][0]["object_id"]
        self.assertRejected(witness=witness, fragment="duplicate witness object ID")

    def test_rejects_dangling_evidence_reference(self):
        witness, _, _ = bounded_control()
        witness["witness_objects"][0]["evidence_refs"] = ["E-NOT-REGISTERED"]
        self.assertRejected(witness=witness, fragment="dangling evidence reference")

    def test_rejects_self_certifying_higher_order_audit(self):
        witness, _, _ = bounded_control()
        witness["higher_order_audit"]["audit_authority_id"] = witness["higher_order_audit"]["implementing_authority_id"]
        self.assertRejected(witness=witness, fragment="self-certify")

    def test_rejects_identity_level_collapse(self):
        witness, _, _ = bounded_control()
        for row in witness["identity_records"][:5]:
            row["status"] = "reconstruction-only"
            row["identifier"] = "COLLAPSED-001"
        self.assertRejected(witness=witness, fragment="identity levels")

    def test_rejects_reconstruction_relabelled_live(self):
        witness, _, _ = bounded_control()
        witness["original_history"]["capture_mode"] = "live_capture"
        self.assertRejected(witness=witness, fragment="retrospective reconstruction")

    def test_rejects_later_evidence_inserted_into_t1(self):
        witness, _, _ = bounded_control()
        witness["higher_order_audit"]["original_t1_evidence_refs"] = ["E-SOL-REVIEW"]
        self.assertRejected(witness=witness, fragment="later evidence")

    def test_rejects_missing_meta_orthability_disposition(self):
        witness, _, _ = bounded_control()
        witness["higher_order_audit"]["meta_orthability_disposition"] = "applicable-assessable"
        self.assertRejected(witness=witness, fragment="meta-orthability")

    def test_rejects_evidence_state_outside_exact_vocabulary(self):
        witness, _, _ = bounded_control()
        witness["evidence_registry"][5]["state"] = "repository-verified-partial"
        self.assertRejected(witness=witness, fragment="evidence state")

    def test_rejects_somnic_conformance_without_authoritative_target_history(self):
        witness, _, _ = bounded_control()
        witness["higher_order_audit"]["somnic_conformance"] = "established"
        self.assertRejected(witness=witness, fragment="somnic conformance")

    def test_rejects_collapsed_illustration_roles(self):
        witness, _, _ = bounded_control()
        for row in witness["witness_objects"]:
            row["illustration_role"] = "documented-historical-fact"
        self.assertRejected(witness=witness, fragment="illustration roles")

    def test_rejects_role_swap_that_preserves_the_role_set(self):
        witness, _, _ = bounded_control()
        witness["witness_objects"][0]["illustration_role"], witness["witness_objects"][1]["illustration_role"] = (
            witness["witness_objects"][1]["illustration_role"],
            witness["witness_objects"][0]["illustration_role"],
        )
        self.assertRejected(witness=witness, fragment="role disagrees with object kind")

    def test_rejects_inter_somnic_relation_from_time_alone(self):
        _, crosswalk, _ = bounded_control()
        crosswalk["relation_disposition"]["inter_somnic_relation"] = "established"
        crosswalk["relation_disposition"]["temporal_separation_is_sufficient"] = True
        self.assertRejected(crosswalk=crosswalk, fragment="temporal separation")

    def test_rejects_claim_promotions(self):
        promoted_values = {
            "correctness": "established",
            "empirical_validation": "established",
            "terminology_benefit_or_adoption": "established",
            "exact_internal_model_ontology": "established",
            "cross_model_or_domain_generalization": "established",
            "live_append_only_capture": "observed",
            "claimant_contract_enforcement": "observed",
            "recurrence_detection": "observed",
            "idempotent_frontier_processing": "observed",
            "full_somnus_writeback_chain": "implemented",
            "nightly_autonomy": "implemented",
            "runtime_deployment": "implemented",
        }
        for key, promoted in promoted_values.items():
            witness, _, _ = bounded_control()
            witness["claim_boundaries"][key] = promoted
            with self.subTest(key=key):
                self.assertRejected(witness=witness, fragment=key.replace("_", " "))

    def test_rejects_normative_proof_protocol_implementation(self):
        witness, _, _ = bounded_control()
        witness["proof_protocol_placement"]["implemented"] = True
        self.assertRejected(witness=witness, fragment="separate reviewed follow-up")

    def test_malformed_inputs_fail_closed_without_traceback(self):
        for witness, crosswalk, narrative in (([], {}, ""), ({}, [], ""), ({"bad": object()}, {}, None)):
            with self.subTest(witness_type=type(witness).__name__, crosswalk_type=type(crosswalk).__name__):
                self.assertRejected(witness=witness, crosswalk=crosswalk, narrative=narrative)


if __name__ == "__main__":
    unittest.main(verbosity=2)
