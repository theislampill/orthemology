import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pmr007_deep_bw_cj_semantic_reissue.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("Deep BW-CJ semantic-reissue validator is missing")
    spec = importlib.util.spec_from_file_location("pmr007_bw_cj_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Pmr007DeepBwCjSemanticReissueTests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "reissue"
        shutil.copytree(ROOT / validator.REISSUE_REL, copied)
        receipt = pathlib.Path(temporary) / "receipt.yaml"
        shutil.copy2(ROOT / validator.PROVENANCE_RECEIPT_REL, receipt)
        return copied, receipt

    def test_reissue_passes_only_at_the_proposal_custody_ceiling(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)

        self.assertEqual(receipt["result"], "PASS_WITH_SEMANTIC_REISSUE_CEILING")
        self.assertEqual(receipt["source_files"], 40)
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertTrue(receipt["source_manifest_exact"])
        self.assertEqual(receipt["structured_parse_errors"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertEqual(receipt["indexed_results"], 14)
        self.assertTrue(receipt["authority_ceiling_exact"])
        self.assertTrue(receipt["deep_bv_baseline_unchanged"])
        self.assertTrue(receipt["v3_checker_reproduced"])
        self.assertTrue(receipt["v3_result_semantic_match"])
        self.assertTrue(receipt["v3_result_byte_match"])
        self.assertTrue(receipt["v1_false_pass_detected"])

    def test_source_hash_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            target = copied / "source-files/PROPOSAL/theorems/PMR-007_DEEP_CJ_PMR-007-FSGW-1_REISSUE_V1.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertGreater(result["source_hash_mismatches"], 0)

    def test_authority_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            document = yaml.safe_load(receipt.read_text(encoding="utf-8"))
            document["proposal_boundary"]["owner_adoption"] = "ADOPTED"
            document["proposal_boundary"]["meniscus"] = "MENISCUS_REACHED"
            receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["authority_ceiling_exact"])

    def test_identity_omission_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            index = copied / "source-files/PROPOSAL/ledgers/RESULT_INDEX.yaml"
            document = yaml.safe_load(index.read_text(encoding="utf-8"))
            document["results"] = document["results"][:-1]
            index.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertNotEqual(result["indexed_results"], 14)

    def test_checker_result_promotion_or_tamper_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            result_path = copied / "intake-review/checks/post_bv_consolidated_recheck_v3_results.json"
            document = json.loads(result_path.read_text(encoding="utf-8"))
            document["overall_pass"] = False
            result_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["v3_result_semantic_match"])

    def test_v3_checker_semantic_mutation_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            checker = copied / "intake-review/checks/post_bv_consolidated_recheck_v3.py"
            text = checker.read_text(encoding="utf-8")
            text = text.replace(
                'return projection(left) == projection(right) and left["target"] != right["target"]',
                'return projection(left) == projection(right) or left["target"] != right["target"]',
                1,
            )
            checker.write_text(text, encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["v3_checker_reproduced"])

    def test_unmanifested_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            leaked = copied / "source-files/UNMANIFESTED.txt"
            separator = chr(92)
            leaked.write_text(
                "private: C:%sUsers%sowner%sevidence.txt\n" % (separator, separator, separator),
                encoding="utf-8",
            )
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["source_coverage_exact"])
        self.assertGreater(result["private_path_findings"], 0)


if __name__ == "__main__":
    unittest.main()
