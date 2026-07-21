#!/usr/bin/env python3
"""Focused corpus-boundary tests for the production repository validator."""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_repo.py"


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
        mutation = ROOT / ".superpowers" / "sdd" / "repo-validator-ignored-mutation.md"
        mutation.write_text("Ignored control artifact.\n", encoding="utf-8")
        try:
            module = load_validator()
            corpus = {
                Path(path).relative_to(ROOT).as_posix()
                for path in module.text_files()
            }
        finally:
            mutation.unlink(missing_ok=True)
        self.assertNotIn(mutation.relative_to(ROOT).as_posix(), corpus)
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
