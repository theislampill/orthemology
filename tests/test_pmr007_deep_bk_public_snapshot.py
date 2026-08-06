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
    def copy_repo(self, temporary):
        copied = pathlib.Path(temporary) / "repo"
        shutil.copytree(ROOT, copied)
        return copied

    def test_exact_snapshot_and_public_corrections_pass_with_partial_ceiling(self):
        validator = load_validator()

        receipt = validator.validate(ROOT)

        self.assertEqual(receipt["result"], "PASS_WITH_PARTIAL_REPRODUCTION_CEILING")
        self.assertEqual(receipt["snapshot_hash_mismatches"], 0)
        self.assertEqual(receipt["snapshot_manifest_rows"], 1186)
        self.assertEqual(receipt["snapshot_actual_files"], 1186)
        self.assertTrue(receipt["snapshot_manifest_coverage_exact"])
        self.assertEqual(receipt["snapshot_manifest_duplicate_paths"], 0)
        self.assertEqual(receipt["snapshot_manifest_unsafe_paths"], 0)
        self.assertEqual(receipt["snapshot_manifest_malformed_rows"], 0)
        self.assertEqual(receipt["repository_source_hash_mismatches"], 0)
        self.assertEqual(receipt["private_paths_in_public_snapshot"], 0)
        self.assertEqual(receipt["private_paths_in_public_corrections"], 0)
        self.assertFalse(receipt["self_contained_public_rereview_reproduction"])

    def test_repository_source_hash_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            target = (
                copied
                / "docs/project-closure/ar8r-v11/programs"
                / "proper-function-and-candidate-e.md"
            )
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["repository_source_hash_mismatches"], 0)

    def test_empty_or_incomplete_manifest_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            snapshot = copied / validator.SNAPSHOT_REL
            manifest = snapshot / "SHA256SUMS"
            original_manifest = manifest.read_bytes()

            manifest.write_text("", encoding="utf-8")
            empty_receipt = validator.validate(copied)

            manifest.write_bytes(original_manifest)
            first_relative = original_manifest.decode("utf-8").splitlines()[0].split(None, 1)[1]
            removed = snapshot / pathlib.PurePosixPath(first_relative)
            removed_bytes = removed.read_bytes()
            removed.unlink()
            incomplete_receipt = validator.validate(copied)
            removed.write_bytes(removed_bytes)

        self.assertEqual(empty_receipt["result"], "FAIL")
        self.assertFalse(empty_receipt["snapshot_manifest_coverage_exact"])
        self.assertEqual(empty_receipt["snapshot_manifest_rows"], 0)
        self.assertEqual(incomplete_receipt["result"], "FAIL")
        self.assertFalse(incomplete_receipt["snapshot_manifest_coverage_exact"])
        self.assertEqual(incomplete_receipt["snapshot_actual_files"], 1185)

    def test_unmanifested_private_file_fails_both_coverage_and_privacy(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            snapshot = copied / validator.SNAPSHOT_REL
            leaked = snapshot / "UNMANIFESTED_PRIVATE_LOCATOR.txt"
            separator = chr(92)
            leaked.write_text(
                "private locator: C:%sUsers%sowner%sprivate-evidence.txt\n"
                % (separator, separator, separator),
                encoding="utf-8",
            )

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["snapshot_manifest_coverage_exact"])
        self.assertEqual(receipt["snapshot_actual_files"], 1187)
        self.assertGreater(receipt["private_paths_in_public_snapshot"], 0)

    def test_duplicate_unsafe_and_malformed_manifest_rows_fail_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            manifest = copied / validator.SNAPSHOT_REL / "SHA256SUMS"
            first_line = manifest.read_text(encoding="utf-8").splitlines()[0]
            manifest.write_text(
                manifest.read_text(encoding="utf-8")
                + first_line
                + "\n"
                + ("0" * 64)
                + "  ../outside.txt\n"
                + "not-a-valid-sha-row\n",
                encoding="utf-8",
            )

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["snapshot_manifest_coverage_exact"])
        self.assertGreater(receipt["snapshot_manifest_duplicate_paths"], 0)
        self.assertGreater(receipt["snapshot_manifest_unsafe_paths"], 0)
        self.assertGreater(receipt["snapshot_manifest_malformed_rows"], 0)


if __name__ == "__main__":
    unittest.main()
