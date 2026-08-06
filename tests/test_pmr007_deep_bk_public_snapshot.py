import importlib.util
import pathlib
import shutil
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pmr007_deep_bk_public_snapshot.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("pmr007_bk_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Pmr007DeepBkPublicSnapshotTests(unittest.TestCase):
    def test_exact_snapshot_and_public_corrections_pass_with_partial_ceiling(self):
        validator = load_validator()

        receipt = validator.validate(ROOT)

        self.assertEqual(receipt["result"], "PASS_WITH_PARTIAL_REPRODUCTION_CEILING")
        self.assertEqual(receipt["snapshot_hash_mismatches"], 0)
        self.assertEqual(receipt["repository_source_hash_mismatches"], 0)
        self.assertEqual(receipt["private_paths_in_public_corrections"], 0)
        self.assertFalse(receipt["self_contained_public_rereview_reproduction"])

    def test_repository_source_hash_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = pathlib.Path(temporary) / "repo"
            shutil.copytree(ROOT, copied)
            target = (
                copied
                / "docs/project-closure/ar8r-v11/programs"
                / "proper-function-and-candidate-e.md"
            )
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["repository_source_hash_mismatches"], 0)


if __name__ == "__main__":
    unittest.main()
