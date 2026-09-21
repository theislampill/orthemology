#!/usr/bin/env python3
"""Focused corpus-boundary tests for the production repository validator."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_repo.py"
SOURCE_MAP = ROOT / "docs/provenance/v5-consolidation/SOURCE_MAP.json"
COMPACT_RECORD = ROOT / "docs/provenance/v5-consolidation/reconciliation/CONCEPT_CROSSWALK.jsonl"
INHERITED_LEDGER = ROOT / "experiments/orthemology-v5/source/CRITICISM_LEDGER.md"


@contextmanager
def changed_bytes(path, data):
    original = path.read_bytes() if path.exists() else None
    path.write_bytes(data)
    try:
        yield
    finally:
        if original is None:
            path.unlink()
        else:
            path.write_bytes(original)


def load_validator():
    spec = importlib.util.spec_from_file_location("repo_validator_corpus_probe", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import production repository validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_validator():
    return subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


class RepoValidatorCorpusTests(unittest.TestCase):
    def test_historical_notation_requires_exact_registered_source(self):
        module = load_validator()
        source = ROOT / "theory/lineages/h-modal/orthability_modal_grounding.md"
        rows = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))["sources"]
        self.assertTrue(module.historical_notation_source(source, rows))
        with changed_bytes(source, source.read_bytes() + b"\nChanged notation.\n"):
            self.assertFalse(module.historical_notation_source(source, rows))
        matching = next(r for r in rows if r.get("destination_repository_path") == source.relative_to(ROOT).as_posix())
        self.assertFalse(module.historical_notation_source(source, rows + [matching]))
        self.assertFalse(module.historical_notation_source(ROOT / "theory/orthemic-core-formalization.md", rows))

    def test_packet_root_reference_is_digest_bound_and_not_a_native_waiver(self):
        module = load_validator()
        rows = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))["sources"]
        source = ROOT / "experiments/orthemology-v5/source/ledgers/REMAINING_OBLIGATIONS.json"
        target = "examples/" + "RequiredAudit.preview.lean.txt"
        self.assertTrue(module.original_packet_locator(source, target, rows, from_packet_root=True))
        self.assertFalse(module.original_packet_locator(source, "examples/" + "unregistered.txt", rows, from_packet_root=True))
        self.assertFalse(module.original_packet_locator(source, "../" + target, rows, from_packet_root=True))
        with changed_bytes(source, source.read_bytes() + b" "):
            self.assertFalse(module.original_packet_locator(source, target, rows, from_packet_root=True))

    def test_exact_compact_provenance_is_not_a_session_dump(self):
        result = run_validator()
        self.assertIn("[PASS] no research-output/session-dump artifact files", result.stdout)

    def test_original_packet_locators_are_reported_as_external_custody(self):
        result = run_validator()
        self.assertIn("[PASS] all repository-relative links resolve", result.stdout)
        self.assertIn("131 original-packet locators (43 unique)", result.stdout)
        self.assertIn("public retrieval remains unconfirmed", result.stdout)

    def test_registered_jsonl_is_still_privacy_scanned_and_hash_bound(self):
        records = COMPACT_RECORD.read_text(encoding="utf-8").splitlines()
        row = json.loads(records[0])
        row["private_path_probe"] = "C:" + "\\work" + "space\\private\\evidence.md"
        records[0] = json.dumps(row)
        with changed_bytes(COMPACT_RECORD, ("\n".join(records) + "\n").encode()):
            result = run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("absolute workspace path", result.stdout)
        self.assertIn("[FAIL] no research-output/session-dump artifact files", result.stdout)

    def test_unregistered_jsonl_with_registered_basename_remains_rejected(self):
        mutation = ROOT / "docs" / COMPACT_RECORD.name
        with changed_bytes(mutation, b'{"message": "unregistered session payload"}\n'):
            result = run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("[FAIL] no research-output/session-dump artifact files", result.stdout)

    def test_new_broken_repository_link_remains_rejected(self):
        mutation = ROOT / "docs" / "repo-validator-broken-link-control.md"
        with changed_bytes(mutation, b'[Missing native source](missing-native-source.md)\n'):
            result = run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("[FAIL] all repository-relative links resolve", result.stdout)
        self.assertIn("missing-native-source.md", result.stdout)

    def test_changed_inherited_source_cannot_claim_packet_link_treatment(self):
        with changed_bytes(INHERITED_LEDGER, INHERITED_LEDGER.read_bytes() + b'\nChanged source control.\n'):
            result = run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("[FAIL] all repository-relative links resolve", result.stdout)

    def test_packet_target_requires_unique_same_artifact_external_binding(self):
        original = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
        target_path = "evidence/current/TOOLCHAIN_ACTUAL.txt"
        for mutation in ("missing", "duplicate", "wrong_artifact", "wrong_disposition", "missing_digest"):
            with self.subTest(mutation=mutation):
                document = json.loads(json.dumps(original))
                row = next(r for r in document["sources"]
                           if r["source_artifact"] == "V4" and r["source_path"] == target_path)
                if mutation == "missing":
                    document["sources"].remove(row)
                elif mutation == "duplicate":
                    document["sources"].append(dict(row))
                elif mutation == "wrong_artifact":
                    row["source_artifact"] = "UNBOUND"
                elif mutation == "wrong_disposition":
                    row["operation"] = "DO_NOT_LAND"
                else:
                    row["source_sha256"] = None
                with changed_bytes(SOURCE_MAP, json.dumps(document).encode()):
                    result = run_validator()
                self.assertEqual(1, result.returncode)
                self.assertIn("[FAIL] all repository-relative links resolve", result.stdout)
                self.assertIn(target_path, result.stdout)

    def test_corpus_includes_tracked_and_nonignored_prospective_files(self):
        mutation = ROOT / "docs" / "repo-validator-prospective-corpus-mutation.md"
        mutation.write_text("Prospective corpus control.\n", encoding="utf-8")
        try:
            module = load_validator()
            corpus = {
                Path(path).relative_to(ROOT).as_posix()
                for path in module.text_files()
            }
        finally:
            mutation.unlink(missing_ok=True)
        self.assertIn("README.md", corpus)
        self.assertIn(mutation.relative_to(ROOT).as_posix(), corpus)

    def test_corpus_excludes_ignored_sdd_control_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            subprocess.run(["git", "init", "-q", str(fixture)], check=True)
            (fixture / ".gitignore").write_text(".superpowers/\n", encoding="utf-8")
            mutation = fixture / ".superpowers" / "sdd" / "repo-validator-ignored-mutation.md"
            mutation.parent.mkdir(parents=True)
            mutation.write_text("Ignored control artifact.\n", encoding="utf-8")
            module = load_validator()
            module.ROOT = str(fixture)
            corpus = {
                Path(path).relative_to(fixture).as_posix()
                for path in module.text_files()
            }
            self.assertNotIn(mutation.relative_to(fixture).as_posix(), corpus)
        self.assertNotIn(
            ".superpowers/sdd/task-2-rereviewer-report.md",
            corpus,
        )

    def test_nonignored_prospective_banned_path_is_rejected(self):
        mutation = ROOT / "docs" / "repo-validator-banned-path-mutation.md"
        banned = "C:" + "\\work" + "space\\private\\evidence.md"
        mutation.write_text(f"Private path: `{banned}`.\n", encoding="utf-8")
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(mutation.name, output)
        self.assertIn("absolute workspace path", output)

    def test_nonignored_prospective_yaml_banned_path_is_rejected(self):
        mutation = ROOT / "docs" / "repo-validator-banned-path-mutation.yaml"
        banned = "C:" + "\\work" + "space\\private\\evidence.md"
        mutation.write_text(f"private_path: '{banned}'\n", encoding="utf-8")
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(mutation.name, output)
        self.assertIn("absolute workspace path", output)

    def test_ignored_control_reports_do_not_fail_repo_validation(self):
        result = run_validator()
        output = result.stdout + result.stderr
        self.assertIn(
            "[PASS] no absolute local paths / banned private patterns / secrets",
            output,
        )
        self.assertNotIn("task-2-rereviewer-report.md", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
