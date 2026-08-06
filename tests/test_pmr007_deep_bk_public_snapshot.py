import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


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
        self.assertTrue(receipt["repository_source_exact_set"])
        self.assertTrue(receipt["crosswalk_values_exact"])
        self.assertTrue(receipt["authority_ceiling_exact"])
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

    def test_nested_sha256sums_is_not_excluded_from_tree_or_privacy(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            nested = copied / validator.SNAPSHOT_REL / "UNLISTED" / "SHA256SUMS"
            nested.parent.mkdir()
            separator = chr(92)
            nested.write_text(
                "private locator: C:%sUsers%sowner%sprivate.txt\n"
                % (separator, separator, separator),
                encoding="utf-8",
            )

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["snapshot_manifest_coverage_exact"])
        self.assertEqual(receipt["snapshot_actual_files"], 1187)
        self.assertGreater(receipt["private_paths_in_public_snapshot"], 0)

    def test_manifested_posix_private_path_fails_privacy_gate(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            snapshot = copied / validator.SNAPSHOT_REL
            manifest = snapshot / "SHA256SUMS"
            lines = manifest.read_text(encoding="utf-8").splitlines()
            line_index = next(
                index for index, line in enumerate(lines) if line.split(None, 1)[1].endswith(".md")
            )
            relative = lines[line_index].split(None, 1)[1]
            target = snapshot / pathlib.PurePosixPath(relative)
            separator = chr(47)
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nprivate locator: %shome%sreviewer%sevidence.txt\n"
                % (separator, separator, separator),
                encoding="utf-8",
            )
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            lines[line_index] = "%s  %s" % (digest, relative)
            manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

            receipt = validator.validate(copied)

        self.assertEqual(receipt["result"], "FAIL")
        self.assertTrue(receipt["snapshot_manifest_coverage_exact"])
        self.assertEqual(receipt["snapshot_hash_mismatches"], 0)
        self.assertGreater(receipt["private_paths_in_public_snapshot"], 0)

    def test_repository_source_rows_cannot_be_empty_or_escape_program_root(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            correction_path = copied / validator.CORRECTION_REL
            original = yaml.safe_load(correction_path.read_text(encoding="utf-8"))

            empty = dict(original)
            empty["repository_sources"] = []
            correction_path.write_text(
                yaml.safe_dump(empty, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            empty_receipt = validator.validate(copied)

            traversal = dict(original)
            traversal["repository_sources"] = [
                {
                    "round": "DEEP_BG",
                    "path": "../repo/README.md",
                    "sha256": hashlib.sha256((copied / "README.md").read_bytes()).hexdigest(),
                }
            ]
            correction_path.write_text(
                yaml.safe_dump(traversal, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            traversal_receipt = validator.validate(copied)

        self.assertEqual(empty_receipt["result"], "FAIL")
        self.assertFalse(empty_receipt["repository_source_exact_set"])
        self.assertEqual(traversal_receipt["result"], "FAIL")
        self.assertFalse(traversal_receipt["repository_source_exact_set"])
        self.assertGreater(traversal_receipt["repository_source_unsafe_paths"], 0)

    def test_crosswalk_and_proposal_authority_promotions_fail_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            crosswalk_path = copied / validator.CROSSWALK_REL
            crosswalk = yaml.safe_load(crosswalk_path.read_text(encoding="utf-8"))
            crosswalk["rounds"]["DEEP_BF"]["public_execution"] = "COMPLETE_SELF_CONTAINED"
            crosswalk["forbidden_claims"] = []
            crosswalk_path.write_text(
                yaml.safe_dump(crosswalk, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            crosswalk_receipt = validator.validate(copied)

            proposal_path = copied / validator.PROPOSAL_RECEIPT_REL
            proposal = yaml.safe_load(proposal_path.read_text(encoding="utf-8"))
            proposal["proposal_boundary"]["historical_identity_assigned"] = True
            proposal["proposal_boundary"]["owner_adoption"] = "ADOPTED"
            proposal["proposal_boundary"]["integrated_champion"] = "PMR-007-NCBD-1"
            proposal["proposal_boundary"]["meniscus"] = "MENISCUS_REACHED"
            proposal_path.write_text(
                yaml.safe_dump(proposal, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            authority_receipt = validator.validate(copied)

        self.assertEqual(crosswalk_receipt["result"], "FAIL")
        self.assertFalse(crosswalk_receipt["crosswalk_values_exact"])
        self.assertEqual(authority_receipt["result"], "FAIL")
        self.assertFalse(authority_receipt["authority_ceiling_exact"])

    def test_non_utf8_root_manifest_returns_structured_fail_without_traceback(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_repo(temporary)
            manifest = copied / validator.SNAPSHOT_REL / "SHA256SUMS"
            manifest.write_bytes(b"\xff\xfe\xfd")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(copied / "scripts/validate_pmr007_deep_bk_public_snapshot.py"),
                    "--root",
                    str(copied),
                ],
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )

        receipt = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stderr, "")
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["snapshot_manifest_read_errors"], 0)


if __name__ == "__main__":
    unittest.main()
