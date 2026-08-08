import importlib.util
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pmr007_deep_bv_semantic_reissue.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("Deep BL-BV semantic-reissue validator is missing")
    spec = importlib.util.spec_from_file_location("pmr007_bv_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Pmr007DeepBvSemanticReissueTests(unittest.TestCase):
    def copy_repo(self, temporary):
        copied = pathlib.Path(temporary) / "repo"
        shutil.copytree(ROOT, copied)
        return copied

    def test_reissue_passes_only_at_the_regenerated_custody_ceiling(self):
        validator = load_validator()

        receipt = validator.validate(ROOT)

        self.assertEqual(receipt["result"], "PASS_WITH_SEMANTIC_REISSUE_CEILING")
        self.assertEqual(receipt["source_files"], 22)
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertTrue(receipt["source_manifest_exact"])
        self.assertEqual(receipt["structured_parse_errors"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertEqual(receipt["exact_original_response_linked_files"], 2)
        self.assertEqual(receipt["regenerated_response_linked_files"], 26)
        self.assertEqual(receipt["original_response_linked_bytes_unavailable"], 26)
        self.assertTrue(receipt["authority_ceiling_exact"])
        self.assertTrue(receipt["deep_bk_exact_snapshot_unchanged"])
        self.assertFalse(receipt["executable_reproduction_established"])

    def test_source_manifest_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            manifest = copied / validator.REISSUE_REL / "SOURCE_SHA256SUMS"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace("33bb04fd", "03bb04fd", 1),
                encoding="utf-8",
            )

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["source_manifest_exact"])

    def test_source_hash_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            target = copied / validator.SOURCE_REL / "PMR-007_DEEP_ROUND_BV_COMMON_INTERVENTION_IDENTIFIABILITY_V2.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["source_hash_mismatches"], 0)

    def test_authority_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            receipt_path = copied / validator.PROVENANCE_RECEIPT_REL
            document = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
            document["proposal_boundary"]["owner_adoption"] = "ADOPTED"
            document["proposal_boundary"]["integrated_champion"] = "PMR-007-CIID-1"
            document["proposal_boundary"]["meniscus"] = "MENISCUS_REACHED"
            receipt_path.write_text(
                yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["authority_ceiling_exact"])

    def test_transcribed_experiment_counts_cannot_be_promoted_to_rerun(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            result_path = copied / validator.SOURCE_REL / "pmr007_deep_bv_distinct_partition_experiment_rereview_results.json"
            import json

            document = json.loads(result_path.read_text(encoding="utf-8"))
            document["independently_rerun_in_custody_repair"] = True
            result_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["executable_reproduction_established"])

    def test_unmanifested_private_locator_fails_coverage_and_privacy(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            leaked = copied / validator.SOURCE_REL / "UNMANIFESTED.txt"
            separator = chr(92)
            leaked.write_text(
                "private: C:%sUsers%sowner%sevidence.txt\n"
                % (separator, separator, separator),
                encoding="utf-8",
            )

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["source_coverage_exact"])
        self.assertGreater(receipt["private_path_findings"], 0)


if __name__ == "__main__":
    unittest.main()
