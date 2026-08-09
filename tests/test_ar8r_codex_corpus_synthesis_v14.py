import importlib.util
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_ar8r_codex_corpus_synthesis_v14.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("Codex corpus-synthesis V14 validator is missing")
    spec = importlib.util.spec_from_file_location(
        "ar8r_codex_corpus_synthesis_v14", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Ar8rCodexCorpusSynthesisV14Tests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "codex-corpus-synthesis-v14"
        shutil.copytree(ROOT / validator.SYNTHESIS_REL, copied)
        return copied

    def assert_failed_with(self, receipt, issue_fragment):
        self.assertEqual(receipt["result"], "FAIL", receipt)
        self.assertTrue(
            any(issue_fragment in issue for issue in receipt["issues"]),
            receipt,
        )

    def test_current_synthesis_is_bounded_and_complete(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)
        self.assertEqual(
            receipt["result"],
            "PASS_BOUNDED_CODEX_CORPUS_SYNTHESIS_NO_SCIENTIFIC_PROMOTION",
        )
        self.assertEqual(receipt["instance_count"], 12)
        self.assertEqual(receipt["candidate_count"], 5)
        self.assertEqual(receipt["countermodel_count"], 11)
        self.assertEqual(receipt["protocol_count"], 4)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertTrue(receipt["authority_ceiling_exact"])
        self.assertTrue(receipt["theorem_ancestry_bounded"])
        self.assertTrue(receipt["lean_receipt_exact"])
        self.assertTrue(receipt["checker_receipt_exact"])
        self.assertTrue(receipt["audit_chain_complete"])
        self.assertTrue(receipt["protocol_readiness_fail_closed"])

    def test_duplicate_instance_identity_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["instances"][1]["id"] = data["instances"][0]["id"]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "typed instance exact identity/order mismatch")

    def test_unknown_relation_class_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["relations"][0]["relation"] = "SAME_VIBES"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "unknown theorem-family relation: REL-01")

    def test_historical_identity_or_novelty_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["authority"]["historical_identity"] = "AR8R-T999"
            data["authority"]["general_novelty"] = 1
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "authority ceiling drift or promotion")
        self.assertFalse(receipt["authority_ceiling_exact"])

    def test_meniscus_or_closure_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["program_status"]["meniscus"] = "MENISCUS_REACHED"
            data["program_status"]["natural_closure"] = "REACHED"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "champion, meniscus, or closure promotion")

    def test_source_world_or_transcendental_bridge_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            row = next(row for row in data["instances"] if row["id"] == "CLIM-12")
            row["source_world_bridge_established"] = True
            row["nonclaims"] = []
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "instance bridge/nonclaim boundary mismatch: CLIM-12")

    def test_candidate_without_nonclaims_or_ancestry_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["candidates"][0]["nonclaims"] = []
            data["candidates"][0]["earliest_internal_ancestor"] = None
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "candidate ancestry/nonclaim boundary missing: CCS-V14-C1")

    def test_protocols_cannot_be_promoted_to_ready_to_run(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["empirical_protocols"][0]["status"] = "READY_TO_RUN"
            data["empirical_protocols"][0]["experiment_executed"] = True
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["protocol_readiness_fail_closed"])

    def test_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "PRIVATE-LEAK.txt").write_text(
                "C:" + "\\Users\\owner\\private.txt\n", encoding="utf-8"
            )
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["private_path_findings"], 0)

    def test_checker_or_lean_receipt_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            checker = copied / "checks/codex_fibre_synthesis_check_results.json"
            checker.write_text("{}\n", encoding="utf-8")
            lean = copied / "lean/LEAN_RECEIPT.json"
            lean.write_text("{}\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["checker_receipt_exact"])
        self.assertFalse(receipt["lean_receipt_exact"])

    def test_candidate_freeze_manifest_is_independently_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/CANDIDATE_FREEZE_SHA256SUMS"
            target.write_text(target.read_text(encoding="utf-8") + "0" * 64 + "  ghost.txt\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "candidate freeze manifest or frozen member drift")

    def test_allowed_but_wrong_instance_class_fails_with_specific_issue(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["instances"][0]["relation_class"] = "FORMAL_ANALOGUE_ONLY"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "instance relation class drift: CLIM-01")

    def test_relation_truncation_fails_with_exact_coverage_issue(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["relations"] = data["relations"][:2]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "theorem-family exact identity/order mismatch")

    def test_candidate_identity_and_verdict_map_are_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["candidates"][0]["id"] = "CCS-V14-RENAMED"
            data["candidates"][1]["verdict"] = "COMMON_THEOREM_ESTABLISHED"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "candidate exact identity/order mismatch")
        self.assert_failed_with(receipt, "candidate verdict drift: CCS-V14-C2")

    def test_countermodel_identity_map_is_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-COUNTERMODELS-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["countermodels"][0]["id"] = "CM-X"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "countermodel exact identity/order mismatch")

    def test_b1_b4_exact_status_map_is_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["empirical_protocols"][0]["status"] = "PREREGISTRATION_READY_FOR_REVIEW_DRAFT"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "empirical protocol readiness or execution promoted")

    def test_residual_status_and_authority_are_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-RESIDUAL-GUIDED-HYPOTHESIS-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["hypotheses"][0]["status"] = "COMMON_THEOREM_ESTABLISHED"
            data["authority_ceiling"]["general_novelty"] = 1
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "residual-hypothesis status drift: RGH-01")
        self.assert_failed_with(receipt, "residual-hypothesis authority drift or promotion")

    def test_all_secondary_authority_surfaces_fail_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            instance = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            instance_data = yaml.safe_load(instance.read_text(encoding="utf-8"))
            instance_data["authority"]["owner_adoption"] = "ADOPTED"
            instance.write_text(yaml.safe_dump(instance_data, sort_keys=False), encoding="utf-8")
            counter = copied / "AR8R-CODEX-COUNTERMODELS-V14.yaml"
            counter_data = yaml.safe_load(counter.read_text(encoding="utf-8"))
            counter_data["authority"]["general_novelty"] = 1
            counter.write_text(yaml.safe_dump(counter_data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "cross-lane instance authority drift or promotion")
        self.assert_failed_with(receipt, "countermodel authority drift or promotion")

    def test_t354_and_tac_sac_controls_are_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["preserved_controls"]["AR8R-T354"] = "REPOSITORY_READY"
            data["preserved_controls"]["TAC_SAC_HISTORICAL_DEFINITIONS"] = "DEFINED_HERE"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "T354 or TAC/SAC preserved-control drift")

    def test_prose_promotion_is_rejected_independently_of_machine_yaml(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "README.md"
            target.write_text(target.read_text(encoding="utf-8") + "\nMENISCUS_REACHED\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "prose or machine authority promotion: MENISCUS_REACHED")

    def test_semantic_source_contract_is_not_path_existence_only(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            row = next(row for row in data["relations"] if row["id"] == "REL-06")
            row["source_refs"] = ["docs/project-closure/ar8r-v11/README.md"]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "relation semantic source contract drift: REL-06")


if __name__ == "__main__":
    unittest.main()
