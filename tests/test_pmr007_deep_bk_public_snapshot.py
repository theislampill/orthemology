import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pmr007_deep_bk_public_snapshot.py"
SOURCE_PAIRS = [('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/AR8R-PROPER-FUNCTION-TYPED-MATRIX-V11.yaml'), ('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/AR8R-TRANSCENDENTAL-BRIDGE-AND-RIVAL-LEDGER-V11.yaml'), ('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/ar8r-r5-minimal-nonintegration-control.md'), ('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/candidate-g-derivational-unification.md'), ('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md'), ('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/track-t-authority-and-bridge-status.md'), ('DEEP_BG', 'docs/project-closure/ar8r-v11/programs/uncreated-grammar-and-articulability.md'), ('DEEP_BH', 'docs/project-closure/ar8r-v11/programs/AR8R-PROPER-FUNCTION-TYPED-MATRIX-V11.yaml'), ('DEEP_BH', 'docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md'), ('DEEP_BI', 'docs/project-closure/ar8r-v11/programs/AR8R_TRANSCENDENTAL_ORTHABILITY_AND_SOURCE_ASCENT_V2.yaml'), ('DEEP_BI', 'docs/project-closure/ar8r-v11/programs/language-translation-and-version-custody.md'), ('DEEP_BI', 'docs/project-closure/ar8r-v11/programs/uncreated-grammar-and-articulability.md')]
ROUND_LIMITS = {'DEEP_BF': {'public_static_custody': 'COMPLETE_FOR_INCLUDED_BYTES', 'public_execution': 'UNAVAILABLE_PRIVATE_SOURCE_PDFS'}, 'DEEP_BG': {'public_static_custody': 'COMPLETE_FOR_INCLUDED_BYTES', 'public_execution': 'PARTIAL_ORIGINAL_SOURCE_SIDECAR_EXCLUDED'}, 'DEEP_BH': {'public_static_custody': 'COMPLETE_FOR_INCLUDED_BYTES', 'public_execution': 'PARTIAL_PRIVATE_RENDERINGS_AND_ORIGINAL_SOURCE_SIDECAR_EXCLUDED'}, 'DEEP_BI': {'public_static_custody': 'COMPLETE_FOR_INCLUDED_BYTES', 'public_execution': 'PARTIAL_ORIGINAL_SOURCE_SIDECAR_EXCLUDED'}, 'DEEP_BJ': {'public_static_custody': 'COMPLETE_FOR_INCLUDED_BYTES', 'public_execution': 'PARTIAL_V2_PRIMARY_GENERATOR_ABSENT'}, 'DEEP_BK': {'public_static_custody': 'COMPLETE_FOR_INCLUDED_BYTES', 'public_execution': 'DISPOSABLE_COPY_REQUIRED_WRITES_RESULTS'}}
PATH_CLASSES = {'theorem': 'PROPOSED_THEOREM_FILES', 'model': 'PROPOSED_COUNTERMODELS', 'audit_repair_rereview_and_results': 'VALIDATION_RECEIPTS', 'admission_and_frozen_hashes': 'PROPOSED_LEDGER_UPDATES', 'source_and_ancestry_notes': 'PROPOSED_ORIGIN_AND_ANCESTRY_UPDATES'}
FORBIDDEN_CLAIMS = ['COMPLETE_PUBLIC_SAFE_AUDIT_CUSTODY', 'EXTERNAL_MATHEMATICAL_REVIEW', 'GENERAL_NOVELTY', 'MENISCUS', 'NATURAL_CLOSURE', 'OWNER_ADOPTION', 'SELF_CONTAINED_PUBLIC_REREVIEW_REPRODUCTION']
PROPOSAL_BOUNDARY = {
    "indexed_results": 73, "existing_round_11_through_20_results": 10,
    "deep_a_through_bk_results": 63, "historical_identity_assigned": False,
    "historical_theorem_origin_credit": False, "external_review": "OPEN",
    "owner_adoption": "PENDING", "repository_readiness": "EXTERNAL_REVIEW_REQUIRED",
    "general_novelty_credit": "NOT_GRANTED", "lean_source_or_kernel_claim": "NONE",
    "integrated_champion": "NONE", "meniscus": "MENISCUS_NOT_REACHED",
    "natural_closure": "NOT_REACHED",
}
EXECUTION_BOUNDARY = {
    "public_snapshot_self_contained_executable": False,
    "independent_reproduction_from_public_snapshot": "NOT_ESTABLISHED",
}
INTERPRETATION = {
    "external_mathematical_review": "OPEN", "owner_adoption": "PENDING",
    "source_world_or_metaphysical_truth_effect": "NONE",
    "general_novelty_effect": "NONE", "meniscus_effect": "NONE",
}
SOURCING_MARKERS = ("10.1016/0024-3795(93)90224-C", "1605.06848", "PMR-BH-SRC-01",
                    "UNVERIFIED", "ELT-2", "10.1038/s41586-024-08548-w")


def load_validator():
    spec = importlib.util.spec_from_file_location("pmr007_bk_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrontierCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        # These are current correction predicates over real synthetic files.
        # Historical resolver transport is independently owned, not exercised here.
        self.validator.digest_record_view_bytes = lambda p: pathlib.Path(p).read_bytes()
        self.validator.digest_record_view_text = lambda p, encoding="utf-8": pathlib.Path(p).read_text(encoding=encoding)
        self.validator.digest_record_view_is_file = lambda p: pathlib.Path(p).is_file()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)
        rows = []
        for round_id, relative in SOURCE_PAIRS:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            body = ("synthetic public source: " + relative + "\n").encode()
            target.write_bytes(body)
            rows.append({"round": round_id, "path": relative,
                         "sha256": hashlib.sha256(body).hexdigest()})
        v = self.validator
        self.documents = {
            v.CORRECTION_REL: {"public_reproduction_status": "PARTIAL_REPRODUCTION_ONLY",
                               "repository_sources": rows,
                               "private_exclusions": [{"public_path": None} for _ in range(4)]},
            v.CROSSWALK_REL: {
                "schema": "ar8r-pmr007-deep-bf-bk-public-reproduction-crosswalk-v1",
                "snapshot_root": "docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk",
                "mutation_policy": "READ_ONLY_SOURCE_NONMUTATING_VALIDATION",
                "historical_script_policy": "EXECUTE_ONLY_IN_DISPOSABLE_COPY",
                "path_classes": copy.deepcopy(PATH_CLASSES), "rounds": copy.deepcopy(ROUND_LIMITS),
                "public_validator": "scripts/validate_pmr007_deep_bk_public_snapshot.py",
                "public_validator_result": "PASS_WITH_PARTIAL_REPRODUCTION_CEILING",
                "forbidden_claims": list(FORBIDDEN_CLAIMS),
            },
            v.PROPOSAL_RECEIPT_REL: {"proposal_boundary": copy.deepcopy(PROPOSAL_BOUNDARY)},
            v.EXECUTION_RECEIPT_REL: {"execution_boundary": copy.deepcopy(EXECUTION_BOUNDARY),
                                      "interpretation": copy.deepcopy(INTERPRETATION),
                                      "authority_effect": "NONE"},
        }
        for rel, doc in self.documents.items():
            self.write_yaml(rel, doc)
        self.write_text(v.ADOPTION_REL, "PMR-007-NCBD-1\nowner adoption: PENDING\n")
        self.write_text(v.SOURCING_REL, "\n".join(SOURCING_MARKERS) + "\n")
        self.write_text(v.EQUATION_REL, "Synthetic equation presentation correction.\n")

    def write_text(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_yaml(self, relative, value):
        self.write_text(relative, yaml.safe_dump(value, sort_keys=False))

    def check_failure(self, field=None):
        receipt = self.validator.validate(self.root)
        self.assertEqual(receipt["result"], "FAIL")
        if field is not None:
            self.assertFalse(receipt[field])
        return receipt

    def test_current_corrections_pass_without_historical_snapshot(self):
        receipt = self.validator.validate(self.root)
        self.assertEqual(receipt["result"], "PASS_CURRENT_CORRECTIONS_ONLY")
        self.assertEqual(receipt["validation_scope"], "CURRENT_CORRECTION_AND_AUTHORITY_BOUNDARIES")
        self.assertEqual(receipt["historical_snapshot_validation"], "NOT_RUN")
        self.assertEqual(receipt["repository_source_rows"], 12)
        for key in ("repository_source_exact_set", "crosswalk_values_exact", "authority_ceiling_exact"):
            self.assertTrue(receipt[key])
        self.assertEqual(receipt["issues"], [])
        self.assertFalse((self.root / self.validator.SNAPSHOT_REL).exists())
        self.assertFalse(any(k.startswith("snapshot_") for k in receipt))
        self.assertFalse(receipt["self_contained_public_rereview_reproduction"])

    def test_historical_resolver_is_not_used_for_current_public_sources(self):
        v = self.validator
        snapshot = self.root / v.SNAPSHOT_REL
        self.write_text(v.SNAPSHOT_REL / "arbitrary.txt", "Not current correction evidence.\n")
        def bounded(fn):
            def read(path, *args, **kwargs):
                self.assertFalse(pathlib.Path(path).is_relative_to(snapshot))
                return fn(path, *args, **kwargs)
            return read
        with mock.patch.object(v, "digest_record_view_bytes", bounded(v.digest_record_view_bytes)), \
                mock.patch.object(v, "digest_record_view_text", bounded(v.digest_record_view_text)), \
                mock.patch.object(v, "digest_record_view_is_file", bounded(v.digest_record_view_is_file)), \
                mock.patch.object(v, "digest_record_view_paths", side_effect=AssertionError("historical enumeration"), create=True):
            self.assertEqual(v.validate(self.root)["result"], "PASS_CURRENT_CORRECTIONS_ONLY")

    def test_current_public_private_locator_without_manifest_is_rejected(self):
        v = self.validator
        self.write_text(v.SNAPSHOT_REL / "current-note.yaml", "locator: " + chr(47) + "home/fixture/private\n")
        receipt = self.check_failure()
        self.assertGreater(receipt["private_paths_in_current_public_sources"], 0)

    def test_current_public_non_utf8_and_symlinks_are_rejected(self):
        v = self.validator
        target = self.root / v.SNAPSHOT_REL / "SHA256SUMS"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"\xff\xfe")
        receipt = self.check_failure()
        self.assertGreater(receipt["current_public_non_utf8_files"], 0)
        target.unlink()
        outside = self.root / "outside.txt"
        outside.write_text("synthetic ordinary source\n")
        target.symlink_to(outside)
        self.check_failure()

    def test_current_public_root_symlink_is_rejected_without_reading(self):
        v = self.validator
        snapshot = self.root / v.SNAPSHOT_REL
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        outside = self.root / "outside-directory"
        outside.mkdir()
        (outside / "file.txt").write_text("synthetic outside source\n")
        snapshot.symlink_to(outside, target_is_directory=True)
        issues = []
        with mock.patch.object(pathlib.Path, "read_text", side_effect=AssertionError("unexpected body read")):
            result = v._current_public_source_privacy(self.root, issues)
        self.assertEqual(result, (0, 0, 0))
        self.assertTrue(issues)

    def test_current_non_utf8_source_returns_structured_cli_failure(self):
        v = self.validator
        target = self.root / v.SNAPSHOT_REL / "SHA256SUMS"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"\xff\xfe")
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", [str(SCRIPT), "--root", str(self.root)]), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = v.main()
        self.assertEqual(status, 1)
        self.assertEqual(err.getvalue(), "")
        receipt = json.loads(out.getvalue())
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["current_public_non_utf8_files"], 0)

    def test_current_public_files_do_not_require_a_historical_member_set(self):
        v = self.validator
        self.write_text(v.SNAPSHOT_REL / "only-current-note.txt", "A synthetic current public note.\n")
        receipt = v.validate(self.root)
        self.assertEqual(receipt["result"], "PASS_CURRENT_CORRECTIONS_ONLY")
        self.assertEqual(receipt["current_public_files_checked"], 1)
        self.assertEqual(receipt["historical_snapshot_validation"], "NOT_RUN")
        self.assertFalse((self.root / v.SNAPSHOT_REL / "SHA256SUMS").exists())

    def test_repository_source_corruption_or_symlink_is_rejected(self):
        path = self.root / SOURCE_PAIRS[0][1]
        original = path.read_bytes()
        path.write_bytes(original + b"drift\n")
        self.assertGreater(self.check_failure()["repository_source_hash_mismatches"], 0)
        path.unlink()
        target = self.root / "outside-source.txt"
        target.write_bytes(original)
        path.symlink_to(target)
        self.assertGreater(self.check_failure()["repository_source_hash_mismatches"], 0)

    def test_repository_source_rows_are_complete_unique_typed_and_bounded(self):
        v = self.validator
        base = self.documents[v.CORRECTION_REL]
        rows = base["repository_sources"]
        variants = [[], rows[:-1], rows[:-1] + [rows[0]], "not-a-list",
                    [dict(rows[0], path="../outside.txt")] + rows[1:],
                    [dict(rows[0], sha256="invalid")] + rows[1:],
                    [dict(rows[0], extra=True)] + rows[1:]]
        for value in variants:
            with self.subTest(value=value):
                doc = copy.deepcopy(base)
                doc["repository_sources"] = value
                self.write_yaml(v.CORRECTION_REL, doc)
                self.check_failure("repository_source_exact_set")
        self.write_yaml(v.CORRECTION_REL, base)

    def test_custody_ceiling_and_private_exclusions_are_preserved(self):
        v = self.validator
        base = self.documents[v.CORRECTION_REL]
        for key, value in [("public_reproduction_status", "COMPLETE"),
                           ("private_exclusions", []),
                           ("private_exclusions", [{"public_path": "claimed-public"}] * 4)]:
            with self.subTest(key=key):
                doc = copy.deepcopy(base)
                doc[key] = value
                self.write_yaml(v.CORRECTION_REL, doc)
                self.check_failure()
        self.write_yaml(v.CORRECTION_REL, base)

    def test_each_crosswalk_authority_or_scope_promotion_is_rejected(self):
        v = self.validator
        base = self.documents[v.CROSSWALK_REL]
        for key in base:
            with self.subTest(key=key):
                doc = copy.deepcopy(base)
                doc[key] = [] if isinstance(doc[key], list) else "PROMOTED"
                self.write_yaml(v.CROSSWALK_REL, doc)
                self.check_failure("crosswalk_values_exact")
        for round_id in ROUND_LIMITS:
            with self.subTest(round=round_id):
                doc = copy.deepcopy(base)
                doc["rounds"][round_id]["public_execution"] = "COMPLETE_SELF_CONTAINED"
                self.write_yaml(v.CROSSWALK_REL, doc)
                self.check_failure("crosswalk_values_exact")
        self.write_yaml(v.CROSSWALK_REL, base)

    def test_each_proposal_denominator_or_authority_promotion_is_rejected(self):
        v = self.validator
        for key, value in PROPOSAL_BOUNDARY.items():
            with self.subTest(key=key):
                doc = copy.deepcopy(self.documents[v.PROPOSAL_RECEIPT_REL])
                doc["proposal_boundary"][key] = True if value is False else (value + 1 if type(value) is int else "PROMOTED")
                self.write_yaml(v.PROPOSAL_RECEIPT_REL, doc)
                self.check_failure("authority_ceiling_exact")
        self.write_yaml(v.PROPOSAL_RECEIPT_REL, self.documents[v.PROPOSAL_RECEIPT_REL])

    def test_each_execution_or_truth_promotion_is_rejected(self):
        v = self.validator
        base = self.documents[v.EXECUTION_RECEIPT_REL]
        for group in ("execution_boundary", "interpretation"):
            for key, value in base[group].items():
                with self.subTest(group=group, key=key):
                    doc = copy.deepcopy(base)
                    doc[group][key] = True if value is False else "PROMOTED"
                    self.write_yaml(v.EXECUTION_RECEIPT_REL, doc)
                    self.check_failure("authority_ceiling_exact")
        doc = copy.deepcopy(base)
        doc["authority_effect"] = "PROMOTED"
        self.write_yaml(v.EXECUTION_RECEIPT_REL, doc)
        self.check_failure("authority_ceiling_exact")
        self.write_yaml(v.EXECUTION_RECEIPT_REL, base)

    def test_all_seven_correction_surfaces_remain_required(self):
        v = self.validator
        paths = [*self.documents, v.ADOPTION_REL, v.SOURCING_REL, v.EQUATION_REL]
        for relative in paths:
            with self.subTest(path=relative):
                path = self.root / relative
                body = path.read_bytes()
                path.unlink()
                self.check_failure()
                path.write_bytes(body)

    def test_current_correction_private_locators_are_rejected(self):
        v = self.validator
        path = self.root / v.EQUATION_REL
        for locator in ("C:" + chr(92) + "Users" + chr(92) + "fixture", chr(47) + "home/fixture/report"):
            with self.subTest(locator=locator):
                path.write_text("Synthetic private locator: " + locator + "\n", encoding="utf-8")
                self.assertGreater(self.check_failure()["private_paths_in_public_corrections"], 0)

    def test_each_sourcing_and_adoption_marker_remains_required(self):
        v = self.validator
        for marker in SOURCING_MARKERS:
            with self.subTest(marker=marker):
                self.write_text(v.SOURCING_REL, "\n".join(x for x in SOURCING_MARKERS if x != marker))
                self.check_failure()
        self.write_text(v.SOURCING_REL, "\n".join(SOURCING_MARKERS))
        for text in ("PMR-007-NCBD-1", "owner adoption: PENDING"):
            with self.subTest(text=text):
                self.write_text(v.ADOPTION_REL, text)
                self.check_failure()


if __name__ == "__main__":
    unittest.main()
