import importlib.util
import pathlib
import shutil
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_ar8r_six_lane_v14_intake.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("six-lane V14 intake validator is missing")
    spec = importlib.util.spec_from_file_location("ar8r_six_lane_v14_intake", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Ar8rSixLaneV14IntakeTests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "six-lane-v14-intake"
        shutil.copytree(ROOT / validator.INTAKE_REL, copied)
        return copied

    def test_all_six_lanes_validate_without_scientific_promotion(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS_PROPOSAL_CUSTODY_AND_BOUNDED_SOURCE_INTAKE")
        self.assertEqual(receipt["lane_count"], 6)
        self.assertEqual(receipt["source_file_counts"], {
            "central": 178,
            "specialist-a": 77,
            "specialist-b": 29,
        })
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertTrue(receipt["specialist_a_checks_reproduced"])
        self.assertTrue(receipt["specialist_a_original_lean_failures_recorded"])
        self.assertTrue(receipt["specialist_a_repaired_lean_receipts_exact"])
        self.assertTrue(receipt["specialist_b_original_lean_failure_recorded"])
        self.assertTrue(receipt["specialist_b_repaired_lean_receipt_exact"])
        self.assertTrue(receipt["deep_research_locator_corrections_exact"])
        self.assertTrue(receipt["tensor_arm_specification_blocked"])
        self.assertTrue(receipt["deep_research_22_readiness_fail_closed"])
        self.assertTrue(receipt["deep_research_22_b1_b4_gap_explicit"])

    def test_source_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "specialist-a/source-files/README.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["source_hash_mismatches"], 0)

    def test_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            leaked = copied / "LEAK.txt"
            private_locator = "C:" + "\\Users\\owner\\private.txt\n"
            leaked.write_text(private_locator, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["private_path_findings"], 0)

    def test_owner_adoption_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-SIX-LANE-V14-INTEGRATION-LEDGER.yaml"
            text = target.read_text(encoding="utf-8").replace(
                "owner_adoption: PENDING", "owner_adoption: ADOPTED", 1
            )
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")

    def test_bad_classical_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            text = target.read_text(encoding="utf-8").replace("volume 12, pages 98 and 409", "volume 12, pages 98 and 173")
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["deep_research_locator_corrections_exact"])

    def test_tensor_arm_ambiguity_cannot_be_silently_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            text = target.read_text(encoding="utf-8").replace(
                "status: BLOCKED_SPECIFICATION_AMBIGUITY", "status: READY_TO_RUN", 1
            )
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["tensor_arm_specification_blocked"])

    def test_deep_research_22_protocols_cannot_be_promoted_or_credited(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            text = target.read_text(encoding="utf-8").replace(
                "ready_to_run_count: 0", "ready_to_run_count: 1", 1
            ).replace(
                "status: NOT_ANSWERED_BY_CURRENT_REPORT", "status: ANSWERED", 1
            )
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["deep_research_22_readiness_fail_closed"])
        self.assertFalse(receipt["deep_research_22_b1_b4_gap_explicit"])


if __name__ == "__main__":
    unittest.main()
