#!/usr/bin/env python3
"""Focused tests for planned-output internal-reference handling.

The synthetic cases run an unchanged copy of the production validator inside
an isolated temporary Git repository.  No test depends on a future output in
the live implementation plan, so completing a later task cannot stale this
suite again.
"""
import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_internal_references.py"
DOCS = "do" + "cs"
SENTINEL = DOCS + "/future/SYNTHETIC-PLANNED-OUTPUT.json"
PLAN = Path(DOCS) / "superpowers/plans/synthetic-internal-reference-plan.md"


def run_command(command, cwd, *, check=True):
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=check,
    )


def run_git(root, *args):
    return run_command(["git", *args], root)


def write(root, relative_path, content):
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return target


def commit_all(root, message="synthetic fixture"):
    run_git(root, "add", "--all")
    run_git(root, "commit", "--quiet", "-m", message)


@contextlib.contextmanager
def temporary_corpus():
    """Yield a minimal committed corpus and always remove it afterward."""
    with tempfile.TemporaryDirectory(prefix="orthemology-internal-refs-") as temp:
        root = Path(temp)
        run_git(root, "init", "--quiet")
        run_git(root, "config", "user.name", "Internal Reference Fixture")
        run_git(root, "config", "user.email", "fixture@example.invalid")

        validator = root / "scripts" / "validate_internal_references.py"
        validator.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(VALIDATOR, validator)
        write(
            root,
            "docs/reference-exemptions.yaml",
            "external_paths:\n"
            "  owner_repository: synthetic-fixture\n"
            "  paths: []\n"
            "retired_paths:\n"
            "  paths: []\n",
        )
        # These are historical examples named in the validator's own docstring.
        write(root, "examples/shared-upstream-corroboration-failure.json", "{}\n")
        write(root, "scripts/validate_claim_reasoning_paths.py", "# fixture\n")
        write(root, ".gitignore", ".superpowers/sdd/\n")
        commit_all(root, "initialize synthetic corpus")
        yield root


def run_validator(root=ROOT):
    validator = root / "scripts" / "validate_internal_references.py"
    return run_command(
        [sys.executable, str(validator)],
        root,
        check=False,
    )


def assert_failure(test, result, cited, source=None):
    output = result.stdout + result.stderr
    test.assertEqual(1, result.returncode, output)
    test.assertIn(cited, output)
    if source is not None:
        test.assertIn(str(source).replace("\\", "/"), output)


class InternalReferenceTests(unittest.TestCase):
    def test_exact_committed_create_line_exempts_absent_output(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            commit_all(corpus)
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_current_evidence_for_same_missing_output_is_rejected(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            source = Path(DOCS) / "current-evidence.md"
            write(corpus, source, f"Current evidence: `{SENTINEL}`.\n")
            commit_all(corpus)
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, source)

    def test_ordinary_plan_reuse_is_not_a_planned_output(self):
        with temporary_corpus() as corpus:
            write(
                corpus,
                PLAN,
                f"- Create: `{SENTINEL}`\n\nCurrent evidence: `{SENTINEL}`.\n",
            )
            commit_all(corpus)
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_materialization_resolves_create_ordinary_and_current_occurrences(self):
        with temporary_corpus() as corpus:
            write(
                corpus,
                PLAN,
                f"- Create: `{SENTINEL}`\n\nOrdinary reuse: `{SENTINEL}`.\n",
            )
            source = Path(DOCS) / "current-evidence.md"
            write(corpus, source, f"Current evidence: `{SENTINEL}`.\n")
            commit_all(corpus)
            absent = run_validator(corpus)
            write(corpus, SENTINEL, "{}\n")
            materialized = run_validator(corpus)
        assert_failure(self, absent, SENTINEL)
        self.assertEqual(
            0,
            materialized.returncode,
            materialized.stdout + materialized.stderr,
        )

    def test_untracked_plan_create_line_is_not_authoritative(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_staged_only_plan_create_line_is_not_authoritative(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            run_git(corpus, "add", "--", PLAN.as_posix())
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_malformed_create_prefix_is_rejected(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}` after approval\n")
            commit_all(corpus)
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_windows_style_ordinary_missing_path_is_rejected(self):
        missing = DOCS + "/future/WINDOWS-MISSING.json"
        with temporary_corpus() as corpus:
            source = Path(DOCS) / "windows-path.md"
            windows_missing = DOCS + "\\future\\WINDOWS-MISSING.json"
            write(corpus, source, f"Current evidence: `{windows_missing}`.\n")
            result = run_validator(corpus)
        assert_failure(self, result, missing, source)

    def test_absolute_environment_paths_are_not_repository_citations(self):
        with temporary_corpus() as corpus:
            absolute_script = (
                "C:" + "\\work" + "space\\repo\\" + "scr" + "ipts\\ENVIRONMENT-MISSING.py"
            )
            mixed_case_venv = "C:" + "\\venv\\Scripts\\python.exe"
            write(
                corpus,
                Path(DOCS) / "environment-path.md",
                f"Interpreter candidates: `{absolute_script}` and `{mixed_case_venv}`.\n",
            )
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_ignored_report_is_not_part_of_the_prospective_corpus(self):
        with temporary_corpus() as corpus:
            write(
                corpus,
                ".superpowers/sdd/ignored-report.md",
                f"Current evidence: `{DOCS}/future/IGNORED-MISSING.json`.\n",
            )
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_resolved_path_in_a_prospective_file_passes(self):
        with temporary_corpus() as corpus:
            target = DOCS + "/CITING.md"
            write(corpus, target, "# Existing target\n")
            write(corpus, Path(DOCS) / "resolved.md", f"Current evidence: `{target}`.\n")
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_temporary_corpus_cleanup_leaves_no_repository_residue(self):
        before = run_git(ROOT, "status", "--porcelain=v1", "--ignored").stdout
        success_path = None
        with temporary_corpus() as corpus:
            success_path = corpus
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
        self.assertFalse(success_path.exists())

        failure_path = None
        with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
            with temporary_corpus() as corpus:
                failure_path = corpus
                raise RuntimeError("synthetic failure")
        self.assertFalse(failure_path.exists())
        after = run_git(ROOT, "status", "--porcelain=v1", "--ignored").stdout
        self.assertEqual(before, after)

    def test_workflow_runs_focused_then_production_validator(self):
        workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(
            encoding="utf-8"
        )
        focused = "python tests/test_internal_references.py"
        production = "python scripts/validate_internal_references.py"
        self.assertIn(f"{focused}\n          {production}", workflow)

    def test_unchanged_real_repository_production_validator_passes(self):
        result = run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
