"""Schema and custody tests for the AR8R V11 reconciliation packet."""

from __future__ import annotations

import hashlib
import importlib.util
import csv
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "project-closure" / "ar8r-v11"
CATALOG = PACKET / "AR8R-V11-EVIDENCE-CATALOG.yaml"
LEDGER = PACKET / "AR8R-V11-RECONCILIATION-LEDGER.yaml"
FALSE_ZERO_FIXTURE = PACKET / "governance" / "FALSE-ZERO-NEGATIVE-FIXTURE.yaml"
CURRENT_PROJECTION = PACKET / "governance" / "CURRENT-CAMPAIGN-PROJECTION.yaml"
RECONCILIATION_VALIDATOR = ROOT / "scripts" / "validate_ar8r_reconciliation.py"
RECOVERY_VALIDATOR = ROOT / "scripts" / "validate_ar8r_recovery.py"
CANDIDATE_1 = PACKET / "theorems" / "candidate-1-hidden-matching-threshold.md"
CANDIDATE_1_PROVENANCE = PACKET / "theorems" / "candidate-1-provenance.yaml"
CANDIDATE_1_RESULTS = PACKET / "theorems" / "candidate-1-small-case-results.json"
T227_AUTH = PACKET / "theorems" / "ar8r-t227-graph-only-root-authentication-factorization.md"
T228_PROGRESS = PACKET / "theorems" / "ar8r-t228-strict-progress-coinductive-collapse.md"
T227_T228_CROSSWALK = PACKET / "theorems" / "ar8r-t227-t228-identity-crosswalk.yaml"
T227_T228_RECEIPT = PACKET / "theorems" / "ar8r-t227-t228-validation-receipt.yaml"
T299_LANDING = PACKET / "theorems" / "ar8r-t299-matched-intervention-burden-landing.md"
T300_BLINDNESS = PACKET / "theorems" / "ar8r-t300-lower-order-alignment-blind-restoration.md"
T299_T300_PILOT = PACKET / "experiments" / "t299-t300-negative-synthetic-pilot.md"
T299_T300_PILOT_RECORD = PACKET / "experiments" / "t299-t300-negative-synthetic-pilot.yaml"
EXPERIMENT_INDEX = ROOT / "experiments" / "experiment-status.yaml"
ORIGIN_V6 = PACKET / "provenance" / "AR8R-CANONICAL-THEOREM-ORIGIN-REGISTRY-V6.yaml"
ORIGIN_V5 = PACKET / "provenance" / "AR8R-CANONICAL-THEOREM-ORIGIN-REGISTRY-V5-PUBLIC-SANITIZED.yaml"
RECOVERY_OVERLAY = PACKET / "provenance" / "AR8R-TARGET-IDENTITY-RECOVERY-OVERLAY-V8.yaml"
SOURCE_UNIVERSE = PACKET / "provenance" / "AR8R-SOURCE-UNIVERSE-RECEIPT-V1.yaml"
SOURCE_UNIVERSE_V2 = PACKET / "provenance" / "AR8R-SOURCE-UNIVERSE-RECEIPT-V2.yaml"
HISTORICAL_COLLISION_RECEIPT = PACKET / "provenance" / "AR8R-HISTORICAL-ID-COLLISION-RECEIPT-P236-P242-V1.yaml"
HISTORICAL_COLLISION_PAYLOAD = PACKET / "theorems" / "historical-collision-recoveries" / "AR8R-HR-P236P242-T236-v1-payload.md"
FAMILY_V1 = PACKET / "provenance" / "AR8R-THEOREM-FAMILY-REGISTRY-V1.yaml"
CORE_RECEIPT = PACKET / "provenance" / "AR8R-CANONICAL-CORE-RECEIPT.yaml"
PAIR_RECEIPT = PACKET / "provenance" / "AR8R-CANONICAL-PAIR-RECEIPT.yaml"
LEAN_V6 = PACKET / "provenance" / "AR8R-LEAN-STATUS-MAP-V6.yaml"
LEAN_V7 = PACKET / "provenance" / "AR8R-LEAN-STATUS-MAP-V7.yaml"
PROGRAMS = PACKET / "programs"
DEFERRED_EXACT = PROGRAMS / "deferred-candidate-source" / "exact"
DEEP_CONTEXT_RECEIPT = PACKET / "provenance" / "AR8R-DEEP-CONTEXT-SOURCE-RECEIPT-V11.yaml"
A_TO_N = PROGRAMS / "AR8R-THREE-TRACK-A-TO-N-ARCHITECTURE-V11.yaml"
BRIDGE_LEDGER = PROGRAMS / "AR8R-TRANSCENDENTAL-BRIDGE-AND-RIVAL-LEDGER-V11.yaml"
PROPER_FUNCTION_MATRIX = PROGRAMS / "AR8R-PROPER-FUNCTION-TYPED-MATRIX-V11.yaml"
ONTOLOGY_MATRIX = PROGRAMS / "AR8R-ONTOLOGY-AND-REPRESENTATION-ALTERNATIVES-MATRIX-V11.yaml"
TAC_REGISTRY = PROGRAMS / "AR8R-TAC-SAC-TYPED-COORDINATE-AND-COUNTERMODEL-REGISTRY-V11.yaml"
PMR_MAP = PACKET / "formalization" / "AR8R-PMR007-TEN-RESULT-FORMALIZATION-MAP-V11.yaml"
LEAN_QUEUE = PACKET / "formalization" / "AR8R-V11-LEAN-FORMALIZATION-QUEUE.yaml"
FAMILY_CROSSWALK = PACKET / "provenance" / "AR8R-THEOREM-FAMILY-RELATION-CROSSWALK-V11.yaml"
TEN_CONFLICT = PACKET / "provenance" / "AR8R-TEN-ADVANCES-STATIC-CONFLICT-RECEIPT-V11.yaml"
CONNES_RECEIPT = PACKET / "provenance" / "AR8R-CONNES-RIGIDITY-DISPUTE-RECEIPT-V11.yaml"
OSW15 = PACKET / "governance" / "ORTHEMOLOGICAL-SPECIFICATION-WARRANT-OSW-15.yaml"
SURFACE_CUSTODY = PROGRAMS / "program-surface-and-correction-custody.yaml"
FLYWHEEL = PROGRAMS / "AR8R-RESEARCH-FLYWHEEL-CROSSWALK-V1.yaml"
MILESTONE_CHARTER = PROGRAMS / "AR8R-ORTHEMOLOGY-MENISCUS-MILESTONE-ARCHITECTURE-V1.md"
MILESTONES = PROGRAMS / "AR8R-ORTHEMOLOGY-MENISCUS-MILESTONES-V1.yaml"
OSM_PROGRAM_CROSSWALK = PROGRAMS / "AR8R-OSM-LEARNING-TRAJECTORY-CONVERGENCE-CROSSWALK-V12.yaml"
FABLE_INTEGRATED_PROMPT = PROGRAMS / "AR8R-FABLE-INTEGRATED-ORTHEMOLOGY-MENISCUS-RESEARCH-PROMPT-V2.md"
TWO_THREAD_RECEIPT = PACKET / "provenance" / "AR8R-TWO-THREAD-SYNTHESIS-RECEIPT-V11.yaml"
POST_MERGE_CATALOG = PACKET / "AR8R-V11-POST-MERGE-EVIDENCE-CATALOG.yaml"
THREAD_CUSTODY = PACKET / "provenance" / "AR8R-POST-MERGE-THREAD-CUSTODY-RECEIPT-V1.yaml"
LINK_DRIFT = PACKET / "provenance" / "AR8R-POST-MERGE-LINK-DRIFT-SUMMARY-V1.yaml"
VISIBLE_SOURCE_MANIFEST = PACKET / "provenance" / "AR8R-POST-MERGE-VISIBLE-FILE-CARD-MANIFEST-V1.yaml"
FILE_CARD_ARCHIVE_CONFLICTS = PACKET / "provenance" / "AR8R-POST-MERGE-FILE-CARD-ARCHIVE-CONFLICTS-V1.yaml"
SOURCE_RECEIPTS = (
    PACKET / "provenance" / "AR8R-FULL-PROGRAM-REENTRY-V2-SOURCE-RECEIPT.yaml",
    PACKET / "provenance" / "AR8R-POST-MERGE-PMR001-SOURCE-RECEIPT.yaml",
    PACKET / "provenance" / "AR8R-POST-MERGE-PMR002-006-SOURCE-RECEIPT.yaml",
)
PMR007_PROPOSAL = PACKET / "post-merge-proposals" / "pmr007-rounds11-20"
PMR007_DEEP_PROPOSAL = PACKET / "post-merge-proposals" / "pmr007-deep-a-ap"
PMR007_DEEP_RECEIPT = PACKET / "provenance" / "AR8R-PMR007-DEEP-A-AP-PROPOSAL-RECEIPT-V1.yaml"
PMR007_DEEP_EXECUTION = PACKET / "provenance" / "AR8R-PMR007-DEEP-A-AP-EXECUTION-RECEIPT-V1.yaml"
PMR007_DEEP_CORRECTION = PACKET / "post-merge-proposals" / "PMR007-DEEP-A-AP-ADOPTION-BOUNDARY-CORRECTION.md"
PROGRAM_FILES = (
    "tensor-and-bitter-lesson.md",
    "proper-function-and-candidate-e.md",
    "candidate-g-derivational-unification.md",
    "agentic-communication.md",
    "language-translation-and-version-custody.md",
    "tac-sac-identity-and-independence.md",
    "uncreated-grammar-and-articulability.md",
    "candidate-n-r5-track-t-and-source-ascent.md",
    "ten-advances-and-source-custody.md",
)
TRACK_T_STATUS = PROGRAMS / "track-t-authority-and-bridge-status.md"
CANDIDATE_N_STATUS = PROGRAMS / "candidate-n-authority-status.md"
R5_CONTROL = PROGRAMS / "ar8r-r5-minimal-nonintegration-control.md"
SOURCE_ASCENT_STATUS = PROGRAMS / "p597-p620-source-ascent-status.md"

ALLOWED_DISPOSITIONS = {
    "PUBLIC_INTEGRATE",
    "PUBLIC_SUMMARY",
    "DEFERRED_INSUFFICIENT_AUDIT",
    "DEFERRED_OWNER_ADOPTION",
    "BLOCKED_FORMAL_DEFECT",
    "SUPERSEDED_EXACT_VERSION",
    "DUPLICATE_EXACT_BYTES",
    "PRIVATE_LOCAL_EVIDENCE",
    "UNAVAILABLE_CONTEXT_ONLY",
}
ALLOWED_EVIDENCE_CLASSES = {
    "EXACT_HISTORICAL_BYTES",
    "EXACT_VERBATIM_TRANSCRIPT",
    "EXACT_ACTIVITY_RENDERING",
    "EXACT_AUDIT_OR_LEDGER",
    "POST_HOC_RECONSTRUCTION",
    "ROLE_PRESERVING_REPLACEMENT",
    "PROGRAM_OR_BURDEN_RECORD",
    "CUSTODY_RECEIPT",
}
ALLOWED_PRIVACY = {"PUBLIC_SAFE", "PRIVATE_EXCLUDED", "PUBLIC_HASH_ONLY"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ABSOLUTE_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|/mnt/data/|/home/|file://)", re.I)
MESSAGE_ID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.I,
)


class TestAr8rV11Reconciliation(unittest.TestCase):
    def load_yaml(self, path: Path):
        self.assertTrue(path.is_file(), f"missing required V11 file: {path}")
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def load_validator(self):
        spec = importlib.util.spec_from_file_location("ar8r_v11_task7_validator", RECONCILIATION_VALIDATOR)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_task7_exact_source_and_current_owner_contract(self):
        validator = self.load_validator()
        self.assertEqual(validator.validate_deferred_exact_source(DEFERRED_EXACT), [])

        receipt = self.load_yaml(DEEP_CONTEXT_RECEIPT)
        self.assertEqual(receipt["selection_totals"], {"files": 24, "bytes": 84163})
        self.assertEqual(len(receipt["members"]), 24)
        self.assertTrue(all(row["adoption_effect"] == "NONE" for row in receipt["members"]))

        architecture = self.load_yaml(A_TO_N)
        self.assertEqual(validator.validate_a_to_n_architecture(architecture), [])
        self.assertEqual({row["candidate"] for row in architecture["candidates"]}, set("ABCDEFGHIJKLMN"))

        bridge = self.load_yaml(BRIDGE_LEDGER)
        self.assertEqual(validator.validate_bridge_ledger(bridge), [])
        self.assertEqual({row["id"] for row in bridge["bridges"]}, {f"B{i}" for i in range(17)})
        self.assertEqual({row["id"] for row in bridge["hard_premises"]}, {f"H{i}" for i in range(17)})
        self.assertEqual({row["id"] for row in bridge["soft_considerations"]}, {f"S{i}" for i in range(8)})

    def test_task7_typed_matrices_and_tac_countermodels_fail_closed(self):
        validator = self.load_validator()
        proper = self.load_yaml(PROPER_FUNCTION_MATRIX)
        ontology = self.load_yaml(ONTOLOGY_MATRIX)
        tac = self.load_yaml(TAC_REGISTRY)
        self.assertEqual(validator.validate_typed_matrices(proper, ontology, tac), [])
        self.assertEqual(len(proper["accounts"]), 10)
        self.assertEqual(len(ontology["alternatives"]), 11)
        dualism = next(row for row in ontology["alternatives"] if row["id"] == "property_dualism")
        self.assertEqual(dualism["source_class"], "NEW_V11")
        self.assertEqual(dualism["historical_presence"], "NONE_FOUND")
        self.assertEqual({row["id"] for row in tac["countermodels"]}, {f"CM{i:02d}" for i in range(1, 33)})
        coordinate_ids = {row["id"] for row in tac["coordinate_registry"]}
        self.assertEqual(len(coordinate_ids), 66)
        self.assertTrue(all(set(row["compared_coordinates"]).issubset(coordinate_ids) for row in tac["countermodels"]))
        self.assertTrue(all(row["objects_or_carriers"] and row["relations_or_valuations"] for row in tac["countermodels"]))

        promoted = yaml.safe_load(yaml.safe_dump(ontology))
        next(row for row in promoted["alternatives"] if row["id"] == "property_dualism")["source_class"] = "HISTORICAL_EXACT"
        self.assertIn("property-dualism-provenance-promoted", validator.validate_typed_matrices(proper, promoted, tac))

    def test_task7_formalization_t299_ten_and_family_boundaries(self):
        validator = self.load_validator()
        pmr = self.load_yaml(PMR_MAP)
        queue = self.load_yaml(LEAN_QUEUE)
        ten = self.load_yaml(TEN_CONFLICT)
        family = self.load_yaml(FAMILY_CROSSWALK)
        self.assertEqual(validator.validate_formalization_owners(pmr, queue, ten, family), [])

        self.assertEqual(len(pmr["results"]), 10)
        cob = next(row for row in pmr["results"] if row["result_id"] == "PMR-007-COB-1")
        self.assertNotIn("PMR-007-FRLA-1", cob["pure_dependencies"])
        prrc = next(row for row in pmr["results"] if row["result_id"] == "PMR-007-PRRC-1")
        self.assertNotIn("PMR-007-PRQT-1", prrc["pure_dependencies"])
        self.assertEqual(ten["Comparator_sorry_count"], "CONFLICTING_38_42")
        self.assertEqual(family["counts"]["focused_exact_relations"], 74)

        candidate_1_family = next(
            row
            for row in family["later_label_crosswalk"]
            if row["later_labels"] == ["Candidate 1", "PMR-007-PRQT-1"]
        )
        self.assertIsNone(candidate_1_family["v5_family"])
        self.assertEqual(
            candidate_1_family["candidate_v5_families"],
            ["FAMILY-FIBRE", "FAMILY-HIGHER"],
        )
        self.assertEqual(
            candidate_1_family["classification_status"],
            "UNRESOLVED_PUBLIC_OWNER_CONFLICT",
        )
        self.assertEqual(len(candidate_1_family["basis_locators"]), 3)

        t299 = T299_LANDING.read_text(encoding="utf-8")
        for token in (
            "Q(S_term^(a))=a",
            "D_b(S_term^(a))=LANDED",
            "L_b(M_cause,u)=1",
            "L_b(M_spont,u)=0",
            "c2b70f73a3b490ae12311802615c788df07fd1734d725686fc8b912faea304c7",
            "4b64280cbf8fe51324cb2d55836eca396f47f4adbd757f648f40448bdf0ce12d",
        ):
            self.assertIn(token, t299)

    def test_task7_connes_dispute_osw15_and_lean_v7_boundaries(self):
        validator = self.load_validator()
        receipt = self.load_yaml(CONNES_RECEIPT)
        osw = self.load_yaml(OSW15)
        lean_v7 = self.load_yaml(LEAN_V7)
        self.assertEqual(validator.validate_connes_and_osw(receipt, osw, lean_v7), [])
        self.assertEqual(receipt["openai_result"]["disposition"], "NIELSEN_CHALLENGE_REJECTED__SPECIALIST_SETTLEMENT_OPEN")
        self.assertEqual(receipt["nielsen_critique"]["disposition"], "DOES_NOT_REFUTE_EXACT_PUBLIC_OPENAI_OBJECT")
        self.assertEqual(receipt["nielsen_positive_proof"]["disposition"], "REJECTED_AS_PROOF__FATAL_GAPS")
        self.assertEqual(receipt["overall_disposition"], "UNRESOLVED_PENDING_OPERATOR_ALGEBRA_SPECIALIST_REVIEW")
        self.assertEqual(len(osw["coordinates"]), 15)
        self.assertEqual(lean_v7["connes_rigidity"]["build_status"], "NOT_PERFORMED")
        self.assertEqual(lean_v7["connes_rigidity"]["kernel_status"], "NOT_PERFORMED")

    def test_task7_negative_mutations_are_rejected(self):
        validator = self.load_validator()
        architecture = self.load_yaml(A_TO_N)
        mutated = yaml.safe_load(yaml.safe_dump(architecture))
        mutated["candidates"] = mutated["candidates"][:-1]
        self.assertIn("a-to-n-candidate-coverage-mismatch", validator.validate_a_to_n_architecture(mutated))

        historical_drift = yaml.safe_load(yaml.safe_dump(architecture))
        next(row for row in historical_drift["candidates"] if row["candidate"] == "A")["historical_evidence"]["truth_status"] = "PROMOTED"
        self.assertIn("a-to-n-historical-evidence-drift:A:truth_status", validator.validate_a_to_n_architecture(historical_drift))

        strict_cycle = yaml.safe_load(yaml.safe_dump(architecture))
        candidate_a = next(row for row in strict_cycle["candidates"] if row["candidate"] == "A")
        candidate_b = next(row for row in strict_cycle["candidates"] if row["candidate"] == "B")
        candidate_a["dependencies"] = [yaml.safe_load(yaml.safe_dump(candidate_b["dependencies"][0]))]
        candidate_a["dependencies"][0]["target"] = "B"
        self.assertIn("a-to-n-strict-dependency-cycle", validator.validate_a_to_n_architecture(strict_cycle))

        bad_dependency_source = yaml.safe_load(yaml.safe_dump(architecture))
        next(row for row in bad_dependency_source["candidates"] if row["candidate"] == "B")["dependencies"][0]["source_locator"] = "summary-only"
        self.assertIn("a-to-n-dependency-provenance-mismatch:B:A", validator.validate_a_to_n_architecture(bad_dependency_source))

        bridge = self.load_yaml(BRIDGE_LEDGER)
        mutated_bridge = yaml.safe_load(yaml.safe_dump(bridge))
        mutated_bridge["closure_state"]["meniscus"] = "MENISCUS_REACHED"
        self.assertIn("bridge-ledger-meniscus-promoted", validator.validate_bridge_ledger(mutated_bridge))

        pmr = self.load_yaml(PMR_MAP)
        queue = self.load_yaml(LEAN_QUEUE)
        ten = self.load_yaml(TEN_CONFLICT)
        family = self.load_yaml(FAMILY_CROSSWALK)
        promoted = yaml.safe_load(yaml.safe_dump(pmr))
        promoted["results"][0]["owner_adoption_status"] = "ADOPTED"
        self.assertIn("pmr-result-owner-adoption-promoted", validator.validate_formalization_owners(promoted, queue, ten, family))

        bad_ten = yaml.safe_load(yaml.safe_dump(ten))
        bad_ten["Comparator_sorry_count"] = 42
        self.assertIn("ten-advances-conflict-token-mismatch", validator.validate_formalization_owners(pmr, queue, bad_ten, family))

        bad_queue = yaml.safe_load(yaml.safe_dump(queue))
        bad_queue["status_axes"]["kernel"] = "KERNEL_CHECKED"
        self.assertIn("lean-queue-status-promoted", validator.validate_formalization_owners(pmr, bad_queue, ten, family))

        bad_family = yaml.safe_load(yaml.safe_dump(family))
        bad_family["no_new_identity_merges"] = False
        self.assertIn("theorem-family-identity-promoted", validator.validate_formalization_owners(pmr, queue, ten, bad_family))

        misrouted_family = yaml.safe_load(yaml.safe_dump(family))
        next(
            row
            for row in misrouted_family["later_label_crosswalk"]
            if row["later_labels"] == ["Candidate 1", "PMR-007-PRQT-1"]
        )["v5_family"] = "FAMILY-RIVAL"
        self.assertIn(
            "theorem-family-later-crosswalk-mismatch:Candidate 1|PMR-007-PRQT-1",
            validator.validate_formalization_owners(pmr, queue, ten, misrouted_family),
        )

        proper = self.load_yaml(PROPER_FUNCTION_MATRIX)
        ontology = self.load_yaml(ONTOLOGY_MATRIX)
        tac = self.load_yaml(TAC_REGISTRY)
        undeclared_coordinate = yaml.safe_load(yaml.safe_dump(tac))
        undeclared_coordinate["countermodels"][0]["compared_coordinates"][0] = "undeclared_coordinate"
        self.assertIn("tac-countermodel-coordinate-undeclared:CM01:undeclared_coordinate", validator.validate_typed_matrices(proper, ontology, undeclared_coordinate))

        invalid_projection = yaml.safe_load(yaml.safe_dump(tac))
        invalid_projection["coordinate_registry"][0]["relevant_projections"][0]["codomain"] = "numerical_identity"
        self.assertIn("tac-projection-codomain-mismatch:registered_type:entity_to_registered_type", validator.validate_typed_matrices(proper, ontology, invalid_projection))

        missing_collapse = yaml.safe_load(yaml.safe_dump(tac))
        missing_collapse["coordinate_registry"][0]["forbidden_collapses"] = []
        self.assertIn("tac-forbidden-collapse-malformed:registered_type", validator.validate_typed_matrices(proper, ontology, missing_collapse))

        empty_witness = yaml.safe_load(yaml.safe_dump(tac))
        empty_witness["countermodels"][0]["objects_or_carriers"] = {}
        self.assertIn("tac-countermodel-witness-empty:CM01:objects_or_carriers", validator.validate_typed_matrices(proper, ontology, empty_witness))

    def test_task7_exact_source_mutations_are_rejected_without_touching_evidence(self):
        validator = self.load_validator()
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "exact"
            shutil.copytree(DEFERRED_EXACT, copied)
            target = next((copied / "candidate-e").iterdir())
            target.write_bytes(target.read_bytes() + b"X")
            issues = validator.validate_deferred_exact_source(copied)
            self.assertTrue(any(code.startswith("deferred-exact-source-") for code in issues))

        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "exact"
            shutil.copytree(DEFERRED_EXACT, copied)
            (copied / "integration" / "EXTRA.md").write_text("extra", encoding="utf-8")
            self.assertIn("deferred-exact-source-allowlist-mismatch", validator.validate_deferred_exact_source(copied))

    def test_task7_connes_osw_and_flywheel_mutations_are_rejected(self):
        validator = self.load_validator()
        receipt = self.load_yaml(CONNES_RECEIPT)
        osw = self.load_yaml(OSW15)
        lean = self.load_yaml(LEAN_V7)

        cases = []
        collapsed = yaml.safe_load(yaml.safe_dump(receipt))
        collapsed["nielsen_critique"]["disposition"] = "PROVED_OPENAI_FALSE"
        cases.append((collapsed, osw, lean, "connes-disposition-separation-mismatch"))
        promoted = yaml.safe_load(yaml.safe_dump(receipt))
        promoted["overall_disposition"] = "THEOREM_ESTABLISHED"
        cases.append((promoted, osw, lean, "connes-overall-disposition-promoted"))
        credited = yaml.safe_load(yaml.safe_dump(receipt))
        credited["zero_credit_boundary"]["novelty_credit"] = 1
        cases.append((credited, osw, lean, "connes-credit-promoted"))
        malformed_n11 = yaml.safe_load(yaml.safe_dump(receipt))
        next(row for row in malformed_n11["blocking_defects"] if row["id"] == "N-11")["injectivity"] = None
        cases.append((malformed_n11, osw, lean, "connes-n11-shape-mismatch"))
        altered_n11 = yaml.safe_load(yaml.safe_dump(receipt))
        next(row for row in altered_n11["blocking_defects"] if row["id"] == "N-11")["finding"] = "Incomplete wording."
        cases.append((altered_n11, osw, lean, "connes-n11-finding-mismatch"))
        short_osw = yaml.safe_load(yaml.safe_dump(osw))
        short_osw["coordinates"] = short_osw["coordinates"][:-1]
        cases.append((receipt, short_osw, lean, "osw15-coordinate-coverage-mismatch"))
        lean_promoted = yaml.safe_load(yaml.safe_dump(lean))
        lean_promoted["connes_rigidity"]["kernel_status"] = "KERNEL_CHECKED"
        cases.append((receipt, osw, lean_promoted, "lean-v7-connes-status-promoted:kernel_status"))
        for candidate_receipt, candidate_osw, candidate_lean, expected in cases:
            self.assertIn(expected, validator.validate_connes_and_osw(candidate_receipt, candidate_osw, candidate_lean))

        catalog = self.load_yaml(CATALOG)
        ledger = self.load_yaml(LEDGER)
        surface = self.load_yaml(SURFACE_CUSTODY)
        flywheel = self.load_yaml(FLYWHEEL)
        receipt_two = self.load_yaml(TWO_THREAD_RECEIPT)
        bad_flywheel = yaml.safe_load(yaml.safe_dump(flywheel))
        bad_flywheel["edges"][0]["kind"] = "proves"
        self.assertTrue(any(code.startswith("flywheel-edge-kind-invalid") for code in validator.validate_task7_ledgers_and_crosswalks(catalog, ledger, surface, bad_flywheel, receipt_two)))

        unknown_endpoint = yaml.safe_load(yaml.safe_dump(flywheel))
        unknown_endpoint["edges"][0]["to"] = "missing_node"
        self.assertIn(
            "flywheel-edge-target-unknown:1:missing_node",
            validator.validate_task7_ledgers_and_crosswalks(catalog, ledger, surface, unknown_endpoint, receipt_two),
        )

        missing_nontransfer = yaml.safe_load(yaml.safe_dump(flywheel))
        del missing_nontransfer["edges"][0]["nontransfer"]
        self.assertIn(
            "flywheel-edge-nontransfer-missing:1",
            validator.validate_task7_ledgers_and_crosswalks(catalog, ledger, surface, missing_nontransfer, receipt_two),
        )

        empty_contribution = yaml.safe_load(yaml.safe_dump(flywheel))
        empty_contribution["edges"][0]["contribution"] = ""
        self.assertIn(
            "flywheel-edge-contribution-missing:1",
            validator.validate_task7_ledgers_and_crosswalks(catalog, ledger, surface, empty_contribution, receipt_two),
        )

        duplicate_edge = yaml.safe_load(yaml.safe_dump(flywheel))
        duplicate_edge["edges"].append(yaml.safe_load(yaml.safe_dump(duplicate_edge["edges"][0])))
        self.assertIn(
            "flywheel-edge-duplicate-endpoint:source_custody:language_version",
            validator.validate_task7_ledgers_and_crosswalks(catalog, ledger, surface, duplicate_edge, receipt_two),
        )

        missing_owner = yaml.safe_load(yaml.safe_dump(flywheel))
        missing_owner["nodes"]["source_custody"]["owner"] = "missing-owner.md"
        self.assertIn(
            "flywheel-node-owner-missing:source_custody:missing-owner.md",
            validator.validate_task7_ledgers_and_crosswalks(catalog, ledger, surface, missing_owner, receipt_two),
        )

    def test_task7a_owner_charter_and_milestone_projection_contract(self):
        validator = self.load_validator()
        self.assertEqual(MILESTONE_CHARTER.stat().st_size, 76682)
        self.assertEqual(
            hashlib.sha256(MILESTONE_CHARTER.read_bytes()).hexdigest(),
            "f4245d44e79e50c9fbef9173ee22e50795a08b02c027059d4abbae2aef15a0c8",
        )

        milestones = self.load_yaml(MILESTONES)
        self.assertEqual(validator.validate_milestone_architecture(milestones), [])
        self.assertEqual(
            {row["milestone_id"] for row in milestones["milestones"]},
            {f"M{i}" for i in range(1, 19)},
        )
        self.assertEqual(
            {row["candidate_id"] for row in milestones["meniscus_candidates"]},
            {f"MEN-{i}" for i in range(1, 10)},
        )
        self.assertEqual(
            {row["phase_id"] for row in milestones["dependency_phases"]},
            {f"PHASE-{i}" for i in range(1, 7)},
        )
        self.assertEqual(
            {row["milestone_id"]: row["status"] for row in milestones["milestones"]},
            validator.EXPECTED_MILESTONE_STATUSES,
        )
        self.assertEqual(
            {row["candidate_id"]: set(row["required_milestones"]) for row in milestones["meniscus_candidates"]},
            validator.EXPECTED_MENISCUS_REQUIREMENTS,
        )
        self.assertEqual(len(milestones["flywheels"]), 5)
        self.assertEqual(milestones["formalization_loop"]["loop_id"], "FORMALIZATION-FLYWHEEL")
        self.assertEqual(milestones["closure_state"]["integrated_champion"], "NO_INTEGRATED_CHAMPION")
        self.assertEqual(milestones["closure_state"]["meniscus"], "MENISCUS_NOT_REACHED")
        self.assertEqual(milestones["closure_state"]["natural_closure"], "NATURAL_CLOSURE_NOT_REACHED")

    def test_task7a_negative_mutations_are_rejected(self):
        validator = self.load_validator()
        source = self.load_yaml(MILESTONES)

        duplicate = yaml.safe_load(yaml.safe_dump(source))
        duplicate["milestones"][1]["milestone_id"] = "M1"
        self.assertIn("milestone-id-coverage-mismatch", validator.validate_milestone_architecture(duplicate))

        unknown_dependency = yaml.safe_load(yaml.safe_dump(source))
        unknown_dependency["milestones"][0]["dependencies"] = ["M99"]
        self.assertIn("milestone-unknown-reference:M1:M99", validator.validate_milestone_architecture(unknown_dependency))

        self_dependency = yaml.safe_load(yaml.safe_dump(source))
        self_dependency["milestones"][0]["dependencies"] = ["M1"]
        self.assertIn("milestone-self-dependency:M1", validator.validate_milestone_architecture(self_dependency))

        cyclic = yaml.safe_load(yaml.safe_dump(source))
        cyclic["milestones"][0]["dependencies"] = ["M2"]
        self.assertIn("milestone-strict-dependency-cycle", validator.validate_milestone_architecture(cyclic))

        missing_field = yaml.safe_load(yaml.safe_dump(source))
        del missing_field["milestones"][0]["nonclaims"]
        self.assertIn("milestone-required-fields-missing:M1", validator.validate_milestone_architecture(missing_field))

        unsupported_completion = yaml.safe_load(yaml.safe_dump(source))
        unsupported_completion["milestones"][0]["status"] = "COMPLETED"
        self.assertIn("milestone-completion-without-evidence:M1", validator.validate_milestone_architecture(unsupported_completion))

        roadmap_promotion = yaml.safe_load(yaml.safe_dump(source))
        roadmap_promotion["meniscus_candidates"][0]["adoption_status"] = "ADOPTED"
        roadmap_promotion["meniscus_candidates"][0]["evidence_classes"] = ["OWNER_PROGRAM_CHARTER"]
        self.assertIn("meniscus-roadmap-only-promotion:MEN-1", validator.validate_milestone_architecture(roadmap_promotion))

        draft_promoted = yaml.safe_load(yaml.safe_dump(source))
        pr9 = next(row for row in draft_promoted["artifact_crosswalk"] if row["artifact_id"] == "DAEE-DRAFT-PR9")
        pr9["authority"] = "MERGED_MAIN_AUTHORITY"
        self.assertIn("daee-draft-authority-promoted:DAEE-DRAFT-PR9", validator.validate_milestone_architecture(draft_promoted))

        missing_target = yaml.safe_load(yaml.safe_dump(source))
        local = next(row for row in missing_target["artifact_crosswalk"] if row["path_kind"] == "REPOSITORY")
        local["path"] = (
            Path("docs")
            / "project-closure"
            / "ar8r-v11"
            / "does-not-exist.yaml"
        ).as_posix()
        self.assertTrue(any(code.startswith("milestone-crosswalk-target-missing:") for code in validator.validate_milestone_architecture(missing_target)))

        fusha_overclaim = yaml.safe_load(yaml.safe_dump(source))
        fusha = next(row for row in fusha_overclaim["artifact_crosswalk"] if row["artifact_id"] == "FUSHA-QAMUS-BOUNDARY")
        fusha["implementation_status"] = "LIVE_IMPLEMENTATION_VERIFIED"
        self.assertIn("fusha-qamus-live-state-overclaim", validator.validate_milestone_architecture(fusha_overclaim))

        closure_promoted = yaml.safe_load(yaml.safe_dump(source))
        closure_promoted["closure_state"]["meniscus"] = "MENISCUS_REACHED"
        self.assertIn("milestone-architecture-meniscus-promoted", validator.validate_milestone_architecture(closure_promoted))

    def test_task7a_existing_owner_integration_preserves_task7_scopes(self):
        validator = self.load_validator()
        self.assertEqual(validator.validate_task7a_owner_integration(), [])

        catalog = self.load_yaml(CATALOG)
        ledger = self.load_yaml(LEDGER)
        self.assertEqual(len(catalog["v11_task7_public_owners"]["owners"]), 22)
        self.assertEqual(
            ledger["v11_task6_and_pdf_addendum_decisions"]["totals"],
            {"INTEGRATE": 26, "PROPOSAL_ONLY": 8, "DEFERRED": 6, "BLOCKED": 9, "PRIVATE_EXCLUDED": 4, "TOTAL": 53},
        )
        self.assertEqual(ledger["v11_task7a_milestone_architecture_decision"]["task7_decision_count_effect"], 0)

    def test_v12_osm_program_crosswalk_contract(self):
        validator = self.load_validator()
        crosswalk = self.load_yaml(OSM_PROGRAM_CROSSWALK)
        milestones = self.load_yaml(MILESTONES)
        flywheel = self.load_yaml(FLYWHEEL)
        catalog = self.load_yaml(CATALOG)
        self.assertEqual(validator.validate_osm_program_integration(crosswalk, milestones, flywheel, catalog), [])
        self.assertEqual(crosswalk["source"]["source_id"], "LAT-1")
        self.assertEqual(crosswalk["source"]["access_copy_bytes"], 137824)
        self.assertEqual(
            crosswalk["source"]["access_copy_sha256"],
            "0d097cba7bbb25a949e2bf95af28b5a2259bd8d60b0e5fac5a74cdf7d05aa814",
        )
        self.assertEqual(crosswalk["closure_state"]["meniscus"], "MENISCUS_NOT_REACHED")

    def test_v12_osm_program_crosswalk_rejects_promotions(self):
        validator = self.load_validator()
        source = self.load_yaml(OSM_PROGRAM_CROSSWALK)
        milestones = self.load_yaml(MILESTONES)
        flywheel = self.load_yaml(FLYWHEEL)
        catalog = self.load_yaml(CATALOG)

        promoted = yaml.safe_load(yaml.safe_dump(source))
        promoted["authority"]["empirical_validation_effect"] = "VALIDATES_ORTHEMOLOGY"
        self.assertIn(
            "osm-program-authority-promoted-or-drifted",
            validator.validate_osm_program_integration(promoted, milestones, flywheel, catalog),
        )

        metaphysical = yaml.safe_load(yaml.safe_dump(source))
        next(row for row in metaphysical["milestone_crosswalk"] if row["milestone_id"] == "M11")["relation"] = "DIRECT_SUPPORT"
        self.assertIn(
            "osm-program-milestone-row-drift:M11",
            validator.validate_osm_program_integration(metaphysical, milestones, flywheel, catalog),
        )

        closed = yaml.safe_load(yaml.safe_dump(source))
        closed["closure_state"]["meniscus"] = "MENISCUS_REACHED"
        self.assertIn(
            "osm-program-closure-promoted",
            validator.validate_osm_program_integration(closed, milestones, flywheel, catalog),
        )

        overattached = yaml.safe_load(yaml.safe_dump(milestones))
        next(row for row in overattached["milestones"] if row["milestone_id"] == "M11")["artifact_ids"].append("OSM-LEARNING-TRAJECTORY-V12")
        self.assertIn(
            "osm-program-artifact-milestone-scope-mismatch",
            validator.validate_osm_program_integration(source, overattached, flywheel, catalog),
        )

        source_drift = yaml.safe_load(yaml.safe_dump(source))
        next(row for row in source_drift["source_reported_constraints"] if row["id"] == "OSM-SRC-01")["claim"] = (
            "The hippocampus implements CSCG."
        )
        self.assertIn(
            "osm-program-source-constraint-drift:OSM-SRC-01",
            validator.validate_osm_program_integration(source_drift, milestones, flywheel, catalog),
        )

        synthesis_drift = yaml.safe_load(yaml.safe_dump(source))
        next(row for row in synthesis_drift["project_syntheses"] if row["id"] == "OSM-SYN-01")["claim"] = (
            "Mouse CA1 empirically validates Orthemology and human noetic structure."
        )
        self.assertIn(
            "osm-program-synthesis-drift:OSM-SYN-01",
            validator.validate_osm_program_integration(synthesis_drift, milestones, flywheel, catalog),
        )

        for milestone_id, field, replacement in (
            ("M8", "contribution", "The study establishes human noetic architecture."),
            ("M10", "nontransfer", "Task efficiency establishes proper function and warrant."),
            ("M14", "nontransfer", "The paper supplies a Lean kernel proof."),
        ):
            milestone_drift = yaml.safe_load(yaml.safe_dump(source))
            next(row for row in milestone_drift["milestone_crosswalk"] if row["milestone_id"] == milestone_id)[field] = replacement
            self.assertIn(
                f"osm-program-milestone-row-drift:{milestone_id}",
                validator.validate_osm_program_integration(milestone_drift, milestones, flywheel, catalog),
            )

        crosswalk_edge_drift = yaml.safe_load(yaml.safe_dump(source))
        next(row for row in crosswalk_edge_drift["flywheel_contributions"] if row["edge_id"] == "OSM-FW-04")["nontransfer"] = (
            "Task learning is noetic restoration."
        )
        self.assertIn(
            "osm-program-crosswalk-flywheel-drift:OSM-FW-04",
            validator.validate_osm_program_integration(crosswalk_edge_drift, milestones, flywheel, catalog),
        )

        main_edge_drift = yaml.safe_load(yaml.safe_dump(flywheel))
        next(
            row for row in main_edge_drift["edges"]
            if row["from"] == "osm_learning_trajectory" and row["to"] == "restoration"
        )["nontransfer"] = "task learning is noetic restoration"
        self.assertIn(
            "osm-program-main-flywheel-edge-drift:osm_learning_trajectory:restoration",
            validator.validate_osm_program_integration(source, milestones, main_edge_drift, catalog),
        )

        catalog_drift = yaml.safe_load(yaml.safe_dump(catalog))
        next(row for row in catalog_drift["items"] if row["item_id"] == "OSM-LEARNING-TRAJECTORY-V12")[
            "source_access_copy_sha256"
        ] = "0" * 64
        self.assertIn(
            "osm-program-evidence-catalog-mismatch",
            validator.validate_osm_program_integration(source, milestones, flywheel, catalog_drift),
        )

        catalog_class_drift = yaml.safe_load(yaml.safe_dump(catalog))
        next(row for row in catalog_class_drift["items"] if row["item_id"] == "OSM-LEARNING-TRAJECTORY-V12")[
            "source_surface"
        ] = "EXTERNAL_MATHEMATICS"
        self.assertIn(
            "osm-program-evidence-catalog-mismatch",
            validator.validate_osm_program_integration(source, milestones, flywheel, catalog_class_drift),
        )

        duplicate_source = yaml.safe_load(yaml.safe_dump(source))
        unsafe_source = yaml.safe_load(yaml.safe_dump(duplicate_source["source_reported_constraints"][0]))
        unsafe_source["claim"] = "The hippocampus implements CSCG."
        duplicate_source["source_reported_constraints"].insert(0, unsafe_source)
        duplicate_source_issues = validator.validate_osm_program_integration(duplicate_source, milestones, flywheel, catalog)
        self.assertIn("osm-program-source-constraint-collection-mismatch", duplicate_source_issues)
        self.assertIn("osm-program-source-constraint-duplicate-id", duplicate_source_issues)

        duplicate_synthesis = yaml.safe_load(yaml.safe_dump(source))
        unsafe_synthesis = yaml.safe_load(yaml.safe_dump(duplicate_synthesis["project_syntheses"][0]))
        unsafe_synthesis["claim"] = "Mouse CA1 empirically validates Orthemology."
        duplicate_synthesis["project_syntheses"].insert(0, unsafe_synthesis)
        duplicate_synthesis_issues = validator.validate_osm_program_integration(duplicate_synthesis, milestones, flywheel, catalog)
        self.assertIn("osm-program-synthesis-collection-mismatch", duplicate_synthesis_issues)
        self.assertIn("osm-program-synthesis-duplicate-id", duplicate_synthesis_issues)

        duplicate_crosswalk_edge = yaml.safe_load(yaml.safe_dump(source))
        unsafe_crosswalk_edge = yaml.safe_load(yaml.safe_dump(duplicate_crosswalk_edge["flywheel_contributions"][3]))
        unsafe_crosswalk_edge["nontransfer"] = "Task learning is noetic restoration."
        duplicate_crosswalk_edge["flywheel_contributions"].insert(3, unsafe_crosswalk_edge)
        duplicate_crosswalk_issues = validator.validate_osm_program_integration(
            duplicate_crosswalk_edge, milestones, flywheel, catalog
        )
        self.assertIn("osm-program-crosswalk-flywheel-collection-mismatch", duplicate_crosswalk_issues)
        self.assertIn("osm-program-crosswalk-flywheel-duplicate-id", duplicate_crosswalk_issues)

        duplicate_main_edge = yaml.safe_load(yaml.safe_dump(flywheel))
        unsafe_main_edge = yaml.safe_load(yaml.safe_dump(next(
            row for row in duplicate_main_edge["edges"]
            if row["from"] == "osm_learning_trajectory" and row["to"] == "restoration"
        )))
        unsafe_main_edge["nontransfer"] = "task learning is noetic restoration"
        insertion_index = next(
            index for index, row in enumerate(duplicate_main_edge["edges"])
            if row["from"] == "osm_learning_trajectory" and row["to"] == "restoration"
        )
        duplicate_main_edge["edges"].insert(insertion_index, unsafe_main_edge)
        duplicate_main_issues = validator.validate_osm_program_integration(source, milestones, duplicate_main_edge, catalog)
        self.assertIn("osm-program-main-flywheel-collection-mismatch", duplicate_main_issues)
        self.assertIn("osm-program-main-flywheel-duplicate-endpoint", duplicate_main_issues)

    def test_evidence_catalog_schema_and_download_coverage(self):
        doc = self.load_yaml(CATALOG)
        self.assertEqual(doc["schema_version"], 1)
        self.assertEqual(doc["downloaded_file_count"], 65)
        items = doc["items"]
        self.assertGreaterEqual(len(items), 65)

        ids = [item["item_id"] for item in items]
        self.assertEqual(len(ids), len(set(ids)), "catalog item_id values must be unique")

        download_rows = [item for item in items if item["source_surface"] == "V8_DOWNLOADED_FILE"]
        self.assertEqual(len(download_rows), 65)
        self.assertEqual(
            len({item["sha256"] for item in download_rows}),
            65,
            "every V8 downloaded file must have its own exact hash row",
        )

        for item in items:
            self.assertIn(item["evidence_class"], ALLOWED_EVIDENCE_CLASSES)
            self.assertIn(item["privacy_class"], ALLOWED_PRIVACY)
            self.assertIn(item["recommended_disposition"], ALLOWED_DISPOSITIONS)
            self.assertTrue(item["public_locator"])
            self.assertIsInstance(item["repository_relevance"], str)
            self.assertTrue(item["repository_relevance"].strip())
            if item.get("sha256"):
                self.assertRegex(item["sha256"], SHA256_RE)

        rendered = CATALOG.read_text(encoding="utf-8")
        self.assertIsNone(ABSOLUTE_PATH_RE.search(rendered))
        self.assertIsNone(MESSAGE_ID_RE.search(rendered))

    def test_reconciliation_ledger_has_terminal_owner_for_every_catalog_row(self):
        catalog = self.load_yaml(CATALOG)
        ledger = self.load_yaml(LEDGER)
        rows = ledger["items"]
        ids = [row["item_id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)), "ledger item_id values must be unique")
        self.assertEqual(set(ids), {item["item_id"] for item in catalog["items"]})

        for row in rows:
            self.assertIn(row["disposition"], ALLOWED_DISPOSITIONS)
            self.assertTrue(row["owner_path"])
            self.assertIn(
                row["publication_state"],
                {"INTEGRATED", "MATERIALIZED_PUBLIC_PROPOSAL_NOT_ADOPTED", "DEFERRED", "BLOCKED", "EXCLUDED"},
            )
            if row["publication_state"] == "MATERIALIZED_PUBLIC_PROPOSAL_NOT_ADOPTED":
                self.assertTrue((ROOT / row["owner_path"]).exists())
            self.assertTrue(row["basis"])
            self.assertTrue(row["remaining_burden"] is not None)

    def test_catalog_sha256s_are_lowercase(self):
        catalog = self.load_yaml(CATALOG)
        for item in catalog["items"]:
            if item.get("sha256"):
                self.assertEqual(item["sha256"], item["sha256"].lower())

    def test_post_merge_source_and_proposal_custody(self):
        post_merge = self.load_yaml(POST_MERGE_CATALOG)
        expected = {
            "PMR-007-MLT-1",
            "PMR-007-SMRB-1",
            "PMR-007-FRLA-1",
            "PMR-007-COB-1",
            "PMR-007-TRC-1",
            "PMR-007-VCT-1",
            "PMR-007-RSD-1",
            "PMR-007-ORTC-V4",
            "PMR-007-PRQT-1",
            "PMR-007-PRRC-1",
        }
        self.assertEqual({row["id"] for row in post_merge["pmr007_proposals"]}, expected)
        boundary = post_merge["pmr007_common_boundary"]
        self.assertEqual(boundary["historical_identity"], "NONE")
        self.assertEqual(boundary["owner_adoption"], "PENDING")
        self.assertEqual(boundary["external_review"], "OPEN")
        self.assertEqual(boundary["repository_readiness"], "EXTERNAL_REVIEW_REQUIRED")

        source_counts = {
            PROGRAMS / "full-program-reentry-v2-source": 22,
            PACKET / "post-merge-pmr001-source": 27,
            PACKET / "post-merge-pmr002-006-source": 12,
        }
        for directory, count in source_counts.items():
            self.assertEqual(sum(path.is_file() for path in directory.rglob("*")), count)

        sums = PMR007_PROPOSAL / "SHA256SUMS"
        listed = set()
        for line in sums.read_text(encoding="utf-8").splitlines():
            digest, relative = line.split(maxsplit=1)
            relative = relative.lstrip("*").replace("\\", "/")
            target = PMR007_PROPOSAL / relative
            self.assertTrue(target.is_file(), relative)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest, relative)
            listed.add(relative)
        actual = {
            path.relative_to(PMR007_PROPOSAL).as_posix()
            for path in PMR007_PROPOSAL.rglob("*")
            if path.is_file() and path.name != "SHA256SUMS"
        }
        self.assertEqual(len(listed), 130)
        self.assertEqual(listed, actual)

    def test_pmr007_deep_a_ap_snapshot_is_exact_and_fail_closed(self):
        self.assertTrue(PMR007_DEEP_PROPOSAL.is_dir(), "missing Deep A-AP proposal snapshot")
        receipt = self.load_yaml(PMR007_DEEP_RECEIPT)
        self.assertEqual(
            receipt["source_archive"]["sha256"],
            "80c1679744374f20740dbb9817bb333fb9ae7f399d166afb39d28d23c3fc9d59",
        )
        self.assertEqual(receipt["source_archive"]["archive_members"], 831)
        self.assertEqual(receipt["source_archive"]["internal_sha256sums_entries"], 830)
        self.assertEqual(receipt["repository_copy"]["exact_archive_members"], 831)
        self.assertEqual(receipt["overlap_with_existing_main"]["byte_duplicate_members"], 99)
        self.assertEqual(receipt["overlap_with_existing_main"]["duplicate_credit_effect"], "NONE")

        index = self.load_yaml(PMR007_DEEP_PROPOSAL / "PROPOSED_RESULT_INDEX.yaml")
        rows = index["results"] + index["items"]
        self.assertEqual(len(rows), 52)
        self.assertEqual(len({row["pmr_identity"] for row in rows}), 52)
        deep_rows = [row for row in rows if row["round"].startswith("DEEP_")]
        self.assertEqual(len(deep_rows), 42)
        expected_deep_ids = {
            "PMR-007-NFG-1", "PMR-007-DURP-1", "PMR-007-ICR-1", "PMR-007-UGEN-1",
            "PMR-007-TNAC-1", "PMR-007-FPF-1", "PMR-007-CBA-1", "PMR-007-UAP-1",
            "PMR-007-OAS-1", "PMR-007-UCA-1", "PMR-007-WFB-1", "PMR-007-SDL-1",
            "PMR-007-ETRP-1", "PMR-007-ANH-1", "PMR-007-GUPP-1", "PMR-007-TRPF-1",
            "PMR-007-FEAG-1", "PMR-007-R5CU-1", "PMR-007-SCRF-1", "PMR-007-MACC-1",
            "PMR-007-TRPD-1", "PMR-007-SWPC-1", "PMR-007-TIPC-1", "PMR-007-TKAA-1",
            "PMR-007-PFSA-1", "PMR-007-COWC-1", "PMR-007-CGIP-1", "PMR-007-FSPW-1",
            "PMR-007-SRVN-1", "PMR-007-RSMF-1", "PMR-007-IHDU-1", "PMR-007-NRID-1",
            "PMR-007-R5NR-1", "PMR-007-SDIG-1", "PMR-007-NMIB-1", "PMR-007-CIOB-1",
            "PMR-007-SAMC-1", "PMR-007-EGAC-1", "PMR-007-SRIN-1", "PMR-007-ABPD-1",
            "PMR-007-RPDS-1", "PMR-007-SWRI-1",
        }
        self.assertEqual({row["pmr_identity"] for row in deep_rows}, expected_deep_ids)
        self.assertTrue(all(row["historical_identity_relation"] == "NONE" for row in deep_rows))
        self.assertTrue(all(row["external_review_status"] == "OPEN" for row in deep_rows))
        self.assertTrue(all("PENDING" in row["owner_adoption_status"] for row in deep_rows))
        self.assertTrue(all("ZERO" in row["origin_and_novelty_ceiling"] for row in deep_rows))

        listed = set()
        for line in (PMR007_DEEP_PROPOSAL / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, relative = line.split(maxsplit=1)
            relative = relative.lstrip("*").replace("\\", "/")
            target = PMR007_DEEP_PROPOSAL / relative
            self.assertTrue(target.is_file(), relative)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest, relative)
            listed.add(relative)
        actual = {
            path.relative_to(PMR007_DEEP_PROPOSAL).as_posix()
            for path in PMR007_DEEP_PROPOSAL.rglob("*")
            if path.is_file() and path.name != "SHA256SUMS"
        }
        self.assertEqual(len(listed), 830)
        self.assertEqual(listed, actual)

        validator = self.load_validator()
        validate_deep = getattr(validator, "validate_pmr007_deep_proposal", None)
        self.assertIsNotNone(validate_deep, "missing Deep A-AP fail-closed validator")
        if validate_deep is not None:
            self.assertEqual(validate_deep(index, receipt, PMR007_DEEP_CORRECTION.read_text(encoding="utf-8")), [])
            promoted = yaml.safe_load(yaml.safe_dump(index))
            promoted["results"][10]["owner_adoption_status"] = "OWNER_ADOPTED"
            self.assertIn(
                "pmr007-deep-owner-adoption-promoted:PMR-007-NFG-1",
                validate_deep(promoted, receipt, PMR007_DEEP_CORRECTION.read_text(encoding="utf-8")),
            )

        catalog = self.load_yaml(POST_MERGE_CATALOG)
        self.assertEqual(validator.validate_post_merge_catalog(catalog), [])
        promoted_catalog = yaml.safe_load(yaml.safe_dump(catalog))
        promoted_catalog["pmr007_deep_a_through_ap_snapshot"]["meniscus"] = "MENISCUS_REACHED"
        self.assertIn(
            "pmr007-deep-catalog-boundary-mismatch:meniscus",
            validator.validate_post_merge_catalog(promoted_catalog),
        )

        execution = self.load_yaml(PMR007_DEEP_EXECUTION)
        self.assertEqual(execution["broad_disposable_run"]["scripts_discovered"], 73)
        self.assertEqual(execution["broad_disposable_run"]["exit_zero"], 52)
        self.assertEqual(execution["broad_disposable_run"]["exit_nonzero"], 21)
        self.assertEqual(execution["isolated_rereview_run"]["scripts_discovered"], 34)
        self.assertEqual(execution["isolated_rereview_run"]["exit_zero"], 15)
        self.assertEqual(execution["isolated_rereview_run"]["exit_nonzero"], 19)
        self.assertEqual(
            execution["verification_class"],
            "INTEGRATOR_REPORTED_NOT_INDEPENDENTLY_REPRODUCED",
        )
        for run_name in ("broad_disposable_run", "isolated_rereview_run"):
            run = execution[run_name]
            self.assertEqual(
                run["evidence_status"],
                "INTEGRATOR_REPORTED_NOT_INDEPENDENTLY_REPRODUCED",
            )
            self.assertIs(run["public_per_script_ledger_present"], False)
            self.assertIs(run["deterministic_compatibility_layout_recipe_present"], False)
        self.assertIs(execution["execution_boundary"]["sanitized_snapshot_self_contained_executable"], False)
        self.assertEqual(
            execution["interpretation"]["independent_reproduction_from_public_snapshot"],
            "NOT_ESTABLISHED",
        )
        self.assertEqual(execution["authority_effect"], "NONE")
        validate_execution = getattr(validator, "validate_pmr007_deep_execution", None)
        self.assertIsNotNone(validate_execution, "missing Deep A-AP execution-boundary validator")
        if validate_execution is not None:
            self.assertEqual(validate_execution(execution), [])
            overclaim = yaml.safe_load(yaml.safe_dump(execution))
            overclaim["execution_boundary"]["sanitized_snapshot_self_contained_executable"] = True
            self.assertIn("pmr007-deep-execution-self-contained-overclaim", validate_execution(overclaim))
            aggregate_overclaim = yaml.safe_load(yaml.safe_dump(execution))
            aggregate_overclaim["verification_class"] = "INDEPENDENTLY_REPRODUCED"
            aggregate_overclaim["broad_disposable_run"]["public_per_script_ledger_present"] = True
            aggregate_issues = validate_execution(aggregate_overclaim)
            self.assertIn("pmr007-deep-execution-verification-class-overclaim", aggregate_issues)
            self.assertIn("pmr007-deep-broad-ledger-boundary-mismatch", aggregate_issues)

    def test_private_locator_regex_does_not_misclassify_tex_type_annotations(self):
        spec = importlib.util.spec_from_file_location("ar8r_recovery_validator", RECOVERY_VALIDATOR)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        locator = getattr(module, "PRIVATE_LOCATOR_RE", None)
        self.assertIsNotNone(locator, "recovery validator must expose its private-locator pattern")
        if locator is not None:
            self.assertIsNone(locator.search(r"f_j:\{0,1\}^{V}\to\mathbb R"))
            windows_path = "C:" + "\\" + "workspace\\private\\evidence.md"
            self.assertIsNotNone(locator.search(windows_path))

    def test_new_thread_custody_and_drift_are_fail_closed(self):
        custody = self.load_yaml(THREAD_CUSTODY)
        counts = custody["capture_counts"]
        self.assertEqual(counts["conversation_turn_slots"], 30)
        self.assertEqual(counts["populated_messages"], 24)
        self.assertEqual(counts["worked_for_controls"], 9)
        self.assertEqual(counts["activity_panels_captured"], 8)
        self.assertEqual(counts["activity_panels_unavailable_with_evidence"], 1)
        self.assertEqual(counts["total_downloads_hashed"], 178)
        self.assertEqual(counts["archive_instances_tested"], 10)
        self.assertEqual(counts["historical_link_drift_incidents"], 6)
        self.assertTrue(all(value is False for value in custody["privacy_boundary"].values()))

        drift = self.load_yaml(LINK_DRIFT)
        self.assertEqual(drift["incident_count"], 6)
        self.assertEqual(len(drift["incidents"]), 6)
        self.assertTrue(all(row["id"].startswith("HLCD-V11-") for row in drift["incidents"]))

    def test_visible_file_card_manifest_hashes_every_selected_source_file(self):
        manifest = self.load_yaml(VISIBLE_SOURCE_MANIFEST)
        self.assertEqual(manifest["source_surface"], "VISIBLE_FILE_CARD_BYTES")
        expected_groups = {
            "FULL_PROGRAM_REENTRY_V2": 22,
            "PMR001": 27,
            "PMR002_THROUGH_PMR006": 12,
        }
        groups = {group["id"]: group for group in manifest["groups"]}
        self.assertEqual(set(groups), set(expected_groups))
        for group_id, expected_count in expected_groups.items():
            group = groups[group_id]
            self.assertEqual(group["file_count"], expected_count)
            self.assertEqual(len(group["files"]), expected_count)
            actual_paths = {
                path.relative_to(PACKET).as_posix()
                for path in (PACKET / group["directory"]).rglob("*")
                if path.is_file()
            }
            listed_paths = {row["path"] for row in group["files"]}
            self.assertEqual(actual_paths, listed_paths)
            for row in group["files"]:
                target = PACKET / row["path"]
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), row["sha256"])

        conflicts = self.load_yaml(FILE_CARD_ARCHIVE_CONFLICTS)
        self.assertEqual(conflicts["summary"]["byte_conflict_rows"], 8)
        self.assertEqual(conflicts["summary"]["archive_absence_rows"], 6)
        self.assertEqual(conflicts["summary"]["multiple_basename_rows"], 4)
        self.assertEqual(
            conflicts["summary"]["authority_resolution"],
            "VISIBLE_FILE_CARD_BYTES_SELECTED_ARCHIVE_VARIANTS_UNRESOLVED",
        )
        for receipt_path in SOURCE_RECEIPTS:
            receipt = self.load_yaml(receipt_path)
            self.assertNotIn("source_archive", receipt)
            self.assertIn("companion_archive", receipt)
            self.assertEqual(receipt["repository_selection"]["source_surface"], "VISIBLE_FILE_CARD_BYTES")
            self.assertEqual(
                receipt["repository_selection"]["selection_manifest"],
                "AR8R-POST-MERGE-VISIBLE-FILE-CARD-MANIFEST-V1.yaml",
            )

    def test_post_merge_mutation_guards_reject_deleted_or_promoted_records(self):
        spec = importlib.util.spec_from_file_location(
            "ar8r_v11_validator_mutations", RECONCILIATION_VALIDATOR
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        custody = self.load_yaml(THREAD_CUSTODY)
        custody["privacy_boundary"] = {}
        self.assertIn(
            "post-merge-privacy-boundary-fields-missing",
            module.validate_post_merge_thread_custody(custody),
        )

        drift = self.load_yaml(LINK_DRIFT)
        drift["incidents"] = [{"id": row["id"]} for row in drift["incidents"]]
        self.assertIn(
            "historical-link-drift-row-incomplete",
            module.validate_link_drift(drift),
        )

        catalog = self.load_yaml(POST_MERGE_CATALOG)
        catalog["pmr007_proposals"][-1]["status"] = "OWNER_ADOPTED_CURRENT_RESULT"
        self.assertIn(
            "pmr007-proposal-status-mismatch:PMR-007-PRRC-1",
            module.validate_post_merge_catalog(catalog),
        )

        manifest = self.load_yaml(VISIBLE_SOURCE_MANIFEST)
        manifest["groups"][0]["files"][0]["sha256"] = "0" * 64
        self.assertIn(
            "visible-file-card-member-hash-mismatch",
            module.validate_visible_source_manifest(manifest),
        )

        receipt = self.load_yaml(SOURCE_RECEIPTS[0])
        receipt["source_archive"] = receipt.pop("companion_archive")
        self.assertIn(
            "post-merge-source-receipt-archive-role-mismatch",
            module.validate_source_receipt(receipt),
        )

    def test_adoption_correction_rejects_round20_v1_promotion(self):
        spec = importlib.util.spec_from_file_location(
            "ar8r_v11_validator_correction", RECONCILIATION_VALIDATOR
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        correction = (
            PACKET
            / "post-merge-proposals"
            / "PMR007-ROUNDS11-20-ADOPTION-BOUNDARY-CORRECTION.md"
        ).read_text(encoding="utf-8")
        mutated = correction + "\nRound 20 V1 is the current adopted theorem.\n"
        self.assertIn(
            "pmr007-correction-contradictory-promotion",
            module.validate_pmr007_correction(mutated),
        )

    def test_packet_sha256s_are_self_consistent(self):
        sums = PACKET / "SHA256SUMS"
        self.assertTrue(sums.is_file(), "missing packet SHA256SUMS")
        listed = set()
        for line in sums.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, relative = line.split(maxsplit=1)
            relative = relative.lstrip("*")
            target = PACKET / relative
            self.assertTrue(target.is_file(), f"missing checksummed file: {relative}")
            listed.add(relative.replace("\\", "/"))
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            self.assertEqual(actual, digest, relative)
        actual_files = {
            path.relative_to(PACKET).as_posix()
            for path in PACKET.rglob("*")
            if path.is_file() and path != sums
        }
        self.assertEqual(actual_files, listed, "SHA256SUMS must cover every V11 packet file")

    def test_false_zero_fixture_is_rejected_by_campaign_validator(self):
        self.assertTrue(RECONCILIATION_VALIDATOR.is_file(), "missing V11 campaign validator")
        self.assertTrue(FALSE_ZERO_FIXTURE.is_file(), "missing false-zero negative fixture")
        spec = importlib.util.spec_from_file_location("ar8r_v11_validator", RECONCILIATION_VALIDATOR)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        fixture = yaml.safe_load(FALSE_ZERO_FIXTURE.read_text(encoding="utf-8"))
        issues = module.validate_campaign_state(fixture)
        self.assertIn("summary-overrides-open-lower-level-records", issues)
        self.assertIn("open-burden-count-mismatch", issues)
        self.assertIn("champion-has-pending-burdens", issues)

        projection = yaml.safe_load(CURRENT_PROJECTION.read_text(encoding="utf-8"))
        self.assertEqual(module.validate_campaign_state(projection), [])
        self.assertEqual(projection["summary"]["reported_open_burden_count"], 8)

    def test_v11_validator_accepts_current_packet_and_exercises_negative_fixture(self):
        result = subprocess.run(
            [sys.executable, str(RECONCILIATION_VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AR8R V11 reconciliation packet: PASS", result.stdout)

    def test_candidate_1_exact_bounded_packet(self):
        self.assertTrue(CANDIDATE_1.is_file(), "missing Candidate 1 theorem packet")
        text = CANDIDATE_1.read_text(encoding="utf-8")
        for required in (
            "D(m,n,t) = mn - binom(t,2)",
            "adaptive deterministic edge-membership queries",
            "Row-scan upper bound",
            "Adversary lower bound",
            "König",
            "exact randomized complexity remains open",
            "not an originality finding",
            "Owner adoption: pending",
        ):
            self.assertIn(required, text)

        provenance = self.load_yaml(CANDIDATE_1_PROVENANCE)
        self.assertEqual(
            provenance["historical_payload_sha256"],
            "558061bf28fc4ead94f8b3b2aa0d67826fc1180500190ab3c17a5128fe349088",
        )
        self.assertEqual(provenance["repository_status"], "NON_ADOPTED_RESEARCH_THEOREM")
        self.assertEqual(provenance["prior_art_confidence"], "moderate")
        self.assertFalse(provenance["originality_established"])
        self.assertFalse(provenance["external_review_completed"])

        import json

        results = json.loads(CANDIDATE_1_RESULTS.read_text(encoding="utf-8"))
        self.assertTrue(results["overall_pass"])
        self.assertEqual(results["instances"], 29)
        self.assertEqual(results["max_edges"], 12)
        self.assertEqual(
            results["historical_results_sha256"],
            "267cc7c06efd844408f3aca9833c3ea56dbe416a0898d065bcaf65f330fc2bfd",
        )

    def test_t227_t228_collision_is_resolved_without_payload_loss(self):
        auth = T227_AUTH.read_text(encoding="utf-8")
        progress = T228_PROGRESS.read_text(encoding="utf-8")
        self.assertIn("AR8R-T227", auth)
        self.assertIn("graph-only root-authentication factorization", auth)
        self.assertIn("reachability does not authenticate roots", auth.lower())
        self.assertIn("AR8R-T228", progress)
        self.assertIn("strict progress is sufficient, but not necessary", progress)
        self.assertIn("mu T = nu T", progress)

        crosswalk = self.load_yaml(T227_T228_CROSSWALK)
        self.assertEqual(crosswalk["canonical"]["authentication"], "AR8R-T227")
        self.assertEqual(crosswalk["canonical"]["strict_progress"], "AR8R-T228")
        self.assertEqual(
            crosswalk["historical_collision"]["strict_progress_as_written"],
            "AR8R-T227",
        )
        self.assertEqual(
            crosswalk["historical_collision"]["disposition"],
            "HISTORICAL_CUSTODY_ONLY_ZERO_ADDITIONAL_CREDIT",
        )

        receipt = self.load_yaml(T227_T228_RECEIPT)
        self.assertEqual(
            receipt["payloads"]["authentication"]["sha256"],
            "61b6b1df5d942ac649abed84ed94efa0458aca30bdf699ef76aa411cb0f99a1c",
        )
        self.assertEqual(
            receipt["payloads"]["strict_progress_pre_renumber"]["sha256"],
            "d2a65f07ffdc18cf5eb1613717d9b9dca8d04ff741f55f4da100e63da1867aea",
        )
        self.assertEqual(receipt["general_mathematical_novelty"], "NONE")

    def test_t299_t300_theorems_and_negative_pilot_remain_bounded(self):
        t299 = T299_LANDING.read_text(encoding="utf-8")
        for required in (
            "AR8R-T299",
            "profile-certifiable exactly when",
            "constant on every fibre",
            "matched operation/no-operation",
            "witnessed landing is not causally attributed landing",
            "VALIDATED_SCOPED_CENTRAL_ARCHITECTURE_CHARACTERIZATION",
            "No general mathematical novelty",
        ):
            self.assertIn(required, t299)

        t300 = T300_BLINDNESS.read_text(encoding="utf-8")
        t300_compact = re.sub(r"\s+", " ", t300)
        for required in (
            "AR8R-T300",
            "even- and odd-parity distributions",
            "every proper-subset marginal",
            "pairwise-profile movement is not necessary",
            "pairwise-profile movement is not sufficient",
            "logically independent",
            "arbitrary learned embedding",
            "VALIDATED_EXACT_CAUSAL_RESTORATION_LOWER_ORDER_PROFILE_BLINDNESS",
            "No general probability novelty",
        ):
            self.assertIn(required, t300_compact)

        pilot_text = T299_T300_PILOT.read_text(encoding="utf-8")
        for required in (
            "8 frozen seeds",
            "0 / 8",
            "0.9971370697021484",
            "support-overlapping",
            "not case-paired",
            "NEGATIVE_AT_CURRENT_EVIDENTIAL_CLASS",
            "PASS_WITH_NONBLOCKING_SCOPE_NOTES",
            "no theorem or meniscus credit",
        ):
            self.assertIn(required, pilot_text)

        pilot = self.load_yaml(T299_T300_PILOT_RECORD)
        self.assertEqual(pilot["seed_count"], 8)
        self.assertEqual(pilot["causal_landing_count"], 0)
        self.assertEqual(pilot["median_hidden_cka"], 0.9971370697021484)
        self.assertEqual(pilot["disposition"], "NEGATIVE_AT_CURRENT_EVIDENTIAL_CLASS")
        self.assertEqual(
            pilot["evidence_class"],
            "PREREGISTERED_SYNTHETIC_SUPPORT_OVERLAPPING_DISTRIBUTION_STRESS_PILOT",
        )
        self.assertFalse(pilot["externally_preregistered"])
        self.assertEqual(pilot["rereview"], "PASS_WITH_NONBLOCKING_SCOPE_NOTES")
        self.assertFalse(pilot["theorem_credit"])
        self.assertFalse(pilot["meniscus_credit"])
        self.assertEqual(
            pilot["source_hashes"]["interpretation_repaired_v2"],
            "49745ad7cedc7bc5f6909826e96e56f47143f15d196254897adc44ad529d0283",
        )
        self.assertEqual(
            pilot["source_hashes"]["cold_audit_143"],
            "e732dfd7e41db913d9c65ccc859cc5144b970096fc2ff45639ae16f391413ef8",
        )

        experiment_index = self.load_yaml(EXPERIMENT_INDEX)
        historical = experiment_index["historical_internal_synthetic_evidence"]
        self.assertEqual(len(historical), 1)
        self.assertEqual(historical[0]["evidence_id"], "AR8R-P661-P668-T299-T300-PILOT")
        self.assertEqual(historical[0]["disposition"], "NEGATIVE_AT_CURRENT_EVIDENTIAL_CLASS")
        self.assertFalse(historical[0]["public_experiment_packet"])
        self.assertFalse(historical[0]["external_empirical_validation"])

    def test_v11_provenance_reconciles_v5_and_v8_without_credit_inflation(self):
        origin = self.load_yaml(ORIGIN_V6)
        self.assertEqual(origin["base_registry"]["all_registry_records"], 514)
        self.assertEqual(origin["base_registry"]["active_ar8r_records"], 382)
        self.assertEqual(origin["base_registry"]["focused_exact_relation_edges"], 74)
        base = self.load_yaml(ORIGIN_V5)
        self.assertEqual(len(base["theorems"]), 514)
        self.assertEqual(base["counts"]["raw_active_ar8r_theorem_records"], 382)
        self.assertEqual(base["counts"]["focused_exact_relation_edges"], 74)
        self.assertEqual(base["public_sanitization"]["redacted_absolute_path_occurrences"], 2)
        self.assertEqual(base["public_sanitization"]["theorem_rows_preserved"], 514)
        overlay = self.load_yaml(RECOVERY_OVERLAY)
        self.assertEqual(overlay["counts"]["target_identities"], 42)
        self.assertEqual(overlay["counts"]["exact_historical_payloads"], 18)
        self.assertEqual(overlay["counts"]["unresolved_historical_identities"], 22)
        self.assertEqual(len(overlay["exact_historical_identities"]), 18)
        self.assertEqual(len(overlay["unresolved_historical_identities"]), 22)
        self.assertEqual(overlay["special_cases"]["AR8R-T150"]["provenance_class"], "ROLE_PRESERVING_REPLACEMENT")
        self.assertFalse(overlay["special_cases"]["AR8R-T150"]["original_historical_bytes_recovered"])
        self.assertEqual(overlay["special_cases"]["AR8R-T354"]["formal_status"], "BLOCKED_FORMAL_DEFECT")
        self.assertFalse(overlay["special_cases"]["AR8R-T354"]["repository_ready"])
        self.assertEqual(overlay["special_cases"]["AR8R-T366"]["provenance_class"], "CANONICAL_SEMANTIC_RECONSTRUCTION")
        self.assertFalse(overlay["special_cases"]["AR8R-T366"]["original_historical_bytes_recovered"])
        self.assertFalse(origin["natural_campaign_closure_claimed"])

        family = self.load_yaml(FAMILY_V1)
        self.assertEqual(family["independent_discovery_route_count"], "NOT_SUPPORTED_BY_CURRENT_PROVENANCE")
        self.assertEqual(family["known_identity_equivalence_classes"], 381)
        self.assertEqual(family["focused_exact_relation_edges"], 74)
        self.assertEqual(family["sole_proved_identity_merge"], "AR8R-T322_TO_AR8R-T319")
        self.assertIn("filename", family["zero_credit_multiplicity_surfaces"])
        self.assertIn("application", family["zero_credit_multiplicity_surfaces"])

        core = self.load_yaml(CORE_RECEIPT)
        self.assertEqual(core["canonical_member_count"], 489)
        self.assertEqual(core["source_sha256"], "0d3bf50dc84e9bed824410d6b7418978ae9a5cf33fbdd1687c3adf7c5b1aa576")
        self.assertEqual(core["status"], "HISTORICAL_CUSTODY_RECEIPT_NOT_REPOSITORY_THEOREM_COUNT")

        pairs = self.load_yaml(PAIR_RECEIPT)
        self.assertEqual(pairs["canonical_unordered_nonself_pair_count"], 119316)
        self.assertEqual(pairs["endpoint_count"], 489)
        self.assertTrue(pairs["validation"]["all_pairs_unique"])

        lean = self.load_yaml(LEAN_V6)
        self.assertEqual(lean["counts"]["all_declaration_records"], 230)
        self.assertEqual(lean["counts"]["source_present_declarations"], 221)
        self.assertEqual(lean["counts"]["intended_source_absent"], 9)
        self.assertEqual(lean["parse_status"], "NOT_PERFORMED")
        self.assertEqual(lean["elaboration_status"], "NOT_PERFORMED")
        self.assertEqual(lean["kernel_status"], "NOT_PERFORMED")
        self.assertEqual(lean["machine_check_claim"], "NONE")

    def test_research_program_charters_preserve_burdens_without_adoption(self):
        self.assertTrue((PROGRAMS / "README.md").is_file())
        texts = {}
        for name in PROGRAM_FILES:
            path = PROGRAMS / name
            self.assertTrue(path.is_file(), f"missing program charter: {name}")
            text = path.read_text(encoding="utf-8")
            texts[name] = text
            self.assertIn("## ", text, f"{name}: expected structured charter")
            self.assertRegex(text.lower(), r"forbidden|nonclaim|scope")

        tensor = texts["tensor-and-bitter-lesson.md"]
        self.assertIn("search controllers A-G", tensor)
        self.assertIn("representation candidates A-F", tensor)
        self.assertIn("Controller G is not representation G", tensor)
        self.assertIn("DATA_INADEQUATE_COLLECT_PROSPECTIVELY", tensor)
        self.assertIn("62,374", tensor)
        self.assertIn("Miettinen", tensor)
        self.assertIn("missing-not-at-random", tensor)

        proper = texts["proper-function-and-candidate-e.md"]
        self.assertIn("no counted cold audit", proper)
        self.assertIn("proper function", proper.lower())
        self.assertIn("epistemic unification", proper.lower())

        candidate_g = texts["candidate-g-derivational-unification.md"]
        self.assertIn("no counted cold audit", candidate_g)

        language = texts["language-translation-and-version-custody.md"]
        self.assertIn("translation fibre", language.lower())
        self.assertIn("same bytes", language.lower())
        self.assertIn("same applicability", language.lower())

        tac = texts["tac-sac-identity-and-independence.md"]
        self.assertIn("numerical identity", tac.lower())
        self.assertIn("evidential independence", tac.lower())

        grammar = texts["uncreated-grammar-and-articulability.md"]
        self.assertIn("uncreated grammar", grammar.lower())
        self.assertIn("divine speech", grammar.lower())

        portfolio = texts["candidate-n-r5-track-t-and-source-ascent.md"]
        self.assertIn("no_integrated_champion", portfolio.lower())
        self.assertIn("common-bearer", portfolio.lower())
        self.assertIn("transcendental", portfolio.lower())

        ten = texts["ten-advances-and-source-custody.md"]
        self.assertIn("external human review", ten.lower())
        self.assertIn("kernel", ten.lower())

    def test_source_universe_receipt_closes_every_structural_input(self):
        receipt = self.load_yaml(SOURCE_UNIVERSE)
        counts = {row["surface"]: row for row in receipt["source_universes"]}
        self.assertEqual(counts["V7_MESSAGE_INDEX"]["rows"], 95)
        self.assertEqual(counts["V7_ACTIVITY_INDEX"]["rows"], 44)
        self.assertEqual(counts["V7_ATTACHMENT_INDEX"]["rows"], 1127)
        self.assertEqual(counts["V8_ATTACHMENT_FINAL_CLASSIFICATION"]["rows"], 1127)
        self.assertEqual(counts["V8_FIRST_PARTY_ATTACHMENT_UNIVERSE"]["rows"], 464)
        self.assertEqual(counts["V8_ACTIVITY_ASSESSMENT"]["rows"], 1490)
        self.assertEqual(counts["V8_ACTIVITY_FILE_REFERENCES"]["rows"], 17293)
        self.assertEqual(counts["V8_DOWNLOADED_FILES"]["rows"], 65)
        self.assertEqual(counts["ARCHIVE_INTEGRITY"]["non_directory_members"], 62399)
        self.assertEqual(counts["ARCHIVE_INTEGRITY"]["unique_member_hashes"], 9968)
        for row in receipt["closure_maps"]:
            path = PACKET / "provenance" / row["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])

    def test_v11_source_universe_receipt_closes_every_later_thread_input(self):
        validator = self.load_validator()
        receipt = self.load_yaml(SOURCE_UNIVERSE_V2)
        expected_ledgers = {
            "V11_ATTACHMENT_INDEX": ("a236e9d40b2ed376953e7fce0d384224509a6567ac2549840b4bb3c764424b57", 1007),
            "V11_DOWNLOAD_AND_ARCHIVE_LEDGER_CSV": ("d1aa7644474123e2ae54c2cc46ea1bba9e7a40bde42447cd9c51dd75d69ba332", 187),
            "V11_DOWNLOAD_AND_ARCHIVE_LEDGER_JSONL": ("89caf73dcf7644acd0cd14b71a5b97ce872ac92361a171a5f9f6928ee91e0f06", 161),
            "V11_ARCHIVE_INTEGRITY_AND_EXTRACTION_LEDGER": ("35f8312da49dd8ab5d198755a17a5b0101543e4cb1a099439458a7f36b6300a7", 10),
            "V11_ARCHIVE_MEMBER_HASH_LEDGER": ("9c034a9d65a9cb6c6c5a9890ae3fb15eb850372dcca821f88845b65a428769ad", 957),
        }
        actual_ledgers = {
            row["surface"]: (row["sha256"], row["rows"])
            for row in receipt["immutable_v11_source_ledgers"]
        }
        self.assertEqual(actual_ledgers, expected_ledgers)

        expected_maps = {
            "AR8R-V11-ATTACHMENT-ROW-DISPOSITION-MAP-V1.csv": 1007,
            "AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv": 187,
            "AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv": 10,
            "AR8R-V11-ARCHIVE-MEMBER-HASH-DISPOSITION-MAP-V1.csv": 506,
        }
        for row in receipt["terminal_maps"]:
            path = SOURCE_UNIVERSE_V2.parent / row["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])
            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
            self.assertEqual(len(rows), expected_maps[row["path"]])
            self.assertEqual(
                validator.validate_v11_terminal_map_rows(row["path"], reader.fieldnames, rows),
                [],
            )

        download_path = SOURCE_UNIVERSE_V2.parent / "AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv"
        with download_path.open(encoding="utf-8", newline="") as handle:
            downloads = list(csv.DictReader(handle))
        self.assertEqual(len({row["sha256"] for row in downloads if row["sha256"]}), 157)
        self.assertEqual(sum(not bool(row["sha256"]) for row in downloads), 9)
        self.assertNotIn(
            "PRIVATE_OR_DUPLICATE_OR_UNSELECTED_SOURCE_NO_PUBLIC_IMPORT",
            {row["disposition"] for row in downloads},
        )

        archive_path = SOURCE_UNIVERSE_V2.parent / "AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv"
        with archive_path.open(encoding="utf-8", newline="") as handle:
            archives = list(csv.DictReader(handle))
        archive5 = next(row for row in archives if row["archive_sequence"] == "5")
        self.assertEqual(archive5["sha256"], "141deffc4323225e549149ba35b6d2ae55007242459bfb513957420b189a78e8")
        self.assertEqual(archive5["disposition"], "SUPERSEDED_BOUNDARY_CHECKPOINT_PRIVATE_NO_PUBLIC_IMPORT")

        relation = receipt["dual_hash_relations"][0]
        summary_path = (SOURCE_UNIVERSE_V2.parent / relation["public_summary_path"]).resolve()
        self.assertEqual(hashlib.sha256(summary_path.read_bytes()).hexdigest(), relation["public_summary_sha256"])
        self.assertNotEqual(relation["source_exact_sha256"], relation["public_summary_sha256"])
        self.assertEqual(relation["identity_claim"], "SUMMARY_IS_NOT_EXACT_SOURCE_BYTES")

    def test_v11_source_universe_maps_fail_closed_under_authority_mutations(self):
        validator = self.load_validator()
        maps: dict[str, tuple[list[str] | None, list[dict[str, str]]]] = {}
        for name in validator.V11_TERMINAL_MAP_FIELDS:
            path = SOURCE_UNIVERSE_V2.parent / name
            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                maps[name] = (reader.fieldnames, list(reader))

        attachment_name = "AR8R-V11-ATTACHMENT-ROW-DISPOSITION-MAP-V1.csv"
        attachment_fields, attachments = maps[attachment_name]
        self.assertIn(
            "v11-terminal-map-header-mismatch:" + attachment_name,
            validator.validate_v11_terminal_map_rows(attachment_name, attachment_fields[:-1], attachments),
        )
        mutated = yaml.safe_load(yaml.safe_dump(attachments))
        mutated[0]["row_id"] = "2"
        self.assertIn(
            "v11-attachment-row-sequence-mismatch",
            validator.validate_v11_terminal_map_rows(attachment_name, attachment_fields, mutated),
        )
        mutated = yaml.safe_load(yaml.safe_dump(attachments))
        mutated[0]["disposition"] = "ADOPTED"
        self.assertIn(
            "v11-attachment-disposition-mismatch",
            validator.validate_v11_terminal_map_rows(attachment_name, attachment_fields, mutated),
        )

        download_name = "AR8R-V11-DOWNLOAD-ROW-DISPOSITION-MAP-V1.csv"
        download_fields, downloads = maps[download_name]
        mutated = yaml.safe_load(yaml.safe_dump(downloads))
        exact_row = next(row for row in mutated if row["disposition"] == "EXACT_PUBLIC_BYTES_PRESENT")
        exact_row["sha256"] = "a" * 64
        self.assertTrue(
            any(
                issue.startswith("v11-download-public-bytes-absent:")
                for issue in validator.validate_v11_terminal_map_rows(
                    download_name,
                    download_fields,
                    mutated,
                    public_exact_hashes=set(),
                    public_mentioned_hashes=set(),
                )
            )
        )
        mutated = yaml.safe_load(yaml.safe_dump(downloads))
        failed_row = next(row for row in mutated if row["source_status"] == "DOWNLOAD_FAILED")
        failed_row["sha256"] = "b" * 64
        failed_row["bytes"] = "1"
        self.assertTrue(
            any(
                issue.startswith("v11-download-access-boundary-incoherent:")
                for issue in validator.validate_v11_terminal_map_rows(download_name, download_fields, mutated)
            )
        )

        archive_name = "AR8R-V11-ARCHIVE-INSTANCE-DISPOSITION-MAP-V1.csv"
        archive_fields, archives = maps[archive_name]
        mutated = yaml.safe_load(yaml.safe_dump(archives))
        mutated[0]["member_count"] = "1"
        self.assertIn(
            "v11-archive-member-total-mismatch",
            validator.validate_v11_terminal_map_rows(archive_name, archive_fields, mutated),
        )

        member_name = "AR8R-V11-ARCHIVE-MEMBER-HASH-DISPOSITION-MAP-V1.csv"
        member_fields, members = maps[member_name]
        mutated = yaml.safe_load(yaml.safe_dump(members))
        mutated[0]["occurrence_count"] = "0"
        member_issues = validator.validate_v11_terminal_map_rows(member_name, member_fields, mutated)
        self.assertTrue(any(issue.startswith("v11-archive-member-count-or-size-malformed:") for issue in member_issues))
        self.assertIn("v11-archive-member-occurrence-total-mismatch", member_issues)

    def test_integrated_fable_prompt_and_local_input_contract_fail_closed(self):
        validator = self.load_validator()
        prompt = FABLE_INTEGRATED_PROMPT.read_text(encoding="utf-8")
        self.assertEqual(validator.validate_integrated_fable_prompt(prompt), [])
        self.assertIn(
            "integrated-fable-prompt-hash-mismatch",
            validator.validate_integrated_fable_prompt(prompt + "\nYou may scan a private transcript.\n"),
        )
        ignore_lines = {
            line.strip()
            for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertTrue({"FABLE_LOCAL_START.md", "FABLE_LOCAL_SOURCES/"}.issubset(ignore_lines))

    def test_public_hash_evidence_excludes_ignored_local_inputs(self):
        validator = self.load_validator()
        local_dir = ROOT / "FABLE_LOCAL_SOURCES"
        local_path = local_dir / "ignored-public-hash-negative-fixture.txt"
        marker = "f" * 64
        payload = f"ignored owner-local input\n{marker}\n".encode("utf-8")
        local_hash = hashlib.sha256(payload).hexdigest()
        created_dir = not local_dir.exists()
        local_dir.mkdir(exist_ok=True)
        try:
            local_path.write_bytes(payload)
            ignored = subprocess.run(
                ["git", "check-ignore", "--quiet", "--", local_path.relative_to(ROOT).as_posix()],
                cwd=ROOT,
            )
            self.assertEqual(ignored.returncode, 0)
            exact, mentioned = validator.public_hash_evidence()
            self.assertNotIn(local_hash, exact)
            self.assertNotIn(marker, mentioned)
        finally:
            local_path.unlink(missing_ok=True)
            if created_dir:
                local_dir.rmdir()

    def test_historical_t236_collision_recovery_preserves_v5_authority(self):
        payload_hash = hashlib.sha256(HISTORICAL_COLLISION_PAYLOAD.read_bytes()).hexdigest()
        self.assertEqual(HISTORICAL_COLLISION_PAYLOAD.stat().st_size, 1408)
        self.assertEqual(payload_hash, "6e5f8fde52bd69c4c8e678b0ab7f0e2d5345ff4cf261cf143a7ecbb3c64835c5")

        receipt = self.load_yaml(HISTORICAL_COLLISION_RECEIPT)
        self.assertFalse(receipt["source_boundary"]["original_historical_file_bytes_recovered"])
        recovered = next(
            row for row in receipt["collisions"]
            if row.get("collision_safe_recovery_identity") == "AR8R-HR-P236P242-T236-v1"
        )
        self.assertEqual(recovered["exact_payload_sha256"], payload_hash)
        self.assertEqual(recovered["owner_adoption"], "PENDING")
        self.assertEqual(recovered["credit_effect"], "NONE")

        origin = self.load_yaml(ORIGIN_V5)
        canonical = next(row for row in origin["theorems"] if row.get("id") == "AR8R-T236")
        self.assertIn("authenticated root support", canonical["statement"])
        self.assertNotIn(
            "AR8R-HR-P236P242-T236-v1",
            {row.get("id") for row in origin["theorems"]},
        )

    def test_transcendental_authority_precedence_and_nonintegration_control(self):
        track = TRACK_T_STATUS.read_text(encoding="utf-8")
        for required in (
            "SAME_TOKEN_SAME_RESPECT_THEORY_ADEQUACY_NO_GO_ESTABLISHED",
            "WORLD_DIRECTED_EXTENSION_CONDITIONAL_ON_RB",
            "GLOBAL_UNDERIVED_MODAL_ORDER_NOT_ESTABLISHED",
            "NECESSARY_BEING_NOT_DEDUCTIVELY_ESTABLISHED",
            "positive-ground package remains incomplete",
        ):
            self.assertIn(required, track)

        candidate_n = CANDIDATE_N_STATUS.read_text(encoding="utf-8")
        for required in (
            "CHECKED_CORPUS_BOUNDED_TAYMIYYAN_TAXONOMIC_APPLICATION",
            "STRONGER_SIGNIFICANCE_NOT_ESTABLISHED",
            "GENERIC_METHOD_NOVELTY_REJECTED_OR_REDUCED",
            "EXTERNAL_SOURCE_SPECIALIST_CONFIRMATION_REQUIRED",
            "INDEPENDENT_INTERPRETIVE_PAYOFF_REQUIRED",
        ):
            self.assertIn(required, candidate_n)

        r5 = R5_CONTROL.read_text(encoding="utf-8")
        self.assertIn("AR8R-R5-MINIMAL-NONINTEGRATION", r5)
        self.assertIn("UNDEFEATED", r5)
        self.assertIn("NO_INTEGRATED_CHAMPION", r5)
        self.assertIn("not a universal separation theorem", r5.lower())

        ascent = SOURCE_ASCENT_STATUS.read_text(encoding="utf-8")
        for required in (
            "NO_INTEGRATED_CHAMPION",
            "CONDITIONAL_ACTUAL_ANCESTRY_RESULT_ONLY",
            "STATIC_SOURCE_ONLY_NO_PARSE_ELAB_KERNEL",
            "342 model-actionable open burdens",
            "B579",
            "B586",
        ):
            self.assertIn(required, ascent)

        e = re.sub(r"\s+", " ", (PROGRAMS / "proper-function-and-candidate-e.md").read_text(encoding="utf-8")).lower()
        self.assertIn("token-autonomous radical correction", e)
        self.assertIn("five-horn", e)
        g = re.sub(r"\s+", " ", (PROGRAMS / "candidate-g-derivational-unification.md").read_text(encoding="utf-8")).lower()
        self.assertIn("carrier packaging", g)
        self.assertIn("explanatory compression", g)


if __name__ == "__main__":
    unittest.main()
