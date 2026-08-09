import importlib.util
import pathlib
import shutil
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_ar8r_external_challenges.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("external-challenge validator is missing")
    spec = importlib.util.spec_from_file_location("ar8r_external_challenges", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Ar8rExternalChallengeTests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "external-challenges"
        shutil.copytree(ROOT / validator.CHALLENGES_REL, copied)
        return copied

    def test_bounded_challenges_validate_without_adoption(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS_NONAUTHORITATIVE_CHALLENGE_CUSTODY")
        self.assertEqual(receipt["challenger_a_source_files"], 1)
        self.assertEqual(receipt["challenger_b_source_files"], 12)
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertTrue(receipt["challenger_b_finite_checker_reproduced"])
        self.assertTrue(receipt["challenger_b_original_lean_failure_recorded"])
        self.assertTrue(receipt["challenger_b_repaired_lean_receipt_exact"])

    def test_source_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "challenger-a-common-intervention/source-files/BOUNDED_CHALLENGER_A_COMMON_INTERVENTION_PACKET.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["source_hash_mismatches"], 0)

    def test_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            leaked = copied / "challenger-b-formal-ancestry/source-files/LEAK.txt"
            separator = chr(92)
            leaked.write_text(
                "C:%sUsers%sowner%sprivate.txt\n" % (separator, separator, separator),
                encoding="utf-8",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["private_path_findings"], 0)

    def test_lean_receipt_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            receipt_path = copied / "challenger-b-formal-ancestry/intake-review/LEAN_INTAKE_RECEIPT.json"
            text = receipt_path.read_text(encoding="utf-8").replace('"owner_adoption": "PENDING"', '"owner_adoption": "ADOPTED"')
            receipt_path.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["challenger_b_repaired_lean_receipt_exact"])


if __name__ == "__main__":
    unittest.main()
