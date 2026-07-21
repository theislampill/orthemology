#!/usr/bin/env python3
"""Focused mutations for planned-output internal-reference handling."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_internal_references.py"
PLANNED_PATH = "docs/project-closure/" + "r7e-sol/ORTHING-CANDIDATE-LEDGER.json"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-07-21-r7e-sol-independent-repair.md"


def run_validator(extra_env=None):
    env = os.environ.copy()
    env.update(extra_env or {})
    return subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def run_git(*args, extra_env=None):
    env = os.environ.copy()
    env.update(extra_env or {})
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )


class InternalReferenceTests(unittest.TestCase):
    def test_committed_create_inventory_lines_are_planned_outputs(self):
        result = run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_same_missing_path_cited_as_current_evidence_still_fails(self):
        mutation = ROOT / "docs" / "internal-reference-current-evidence-mutation.md"
        mutation.write_text(
            f"Current evidence: `{PLANNED_PATH}`.\n",
            encoding="utf-8",
        )
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(PLANNED_PATH, output)
        self.assertIn(mutation.name, output)

    def test_same_plan_ordinary_reuse_is_not_a_planned_output(self):
        original = PLAN.read_bytes()
        with PLAN.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(f"\nCurrent evidence is `{PLANNED_PATH}`.\n")
        try:
            result = run_validator()
        finally:
            PLAN.write_bytes(original)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(PLANNED_PATH, output)
        self.assertIn(PLAN.name, output)

    def test_create_prefix_with_extra_text_is_not_an_exact_inventory_line(self):
        missing = "docs/project-closure/" + "r7e-sol/NOT-AN-EXACT-CREATE.json"
        original = PLAN.read_bytes()
        with PLAN.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(f"\n- Create: `{missing}` after approval\n")
        try:
            result = run_validator()
        finally:
            PLAN.write_bytes(original)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(missing, output)

    def test_uncommitted_plan_create_line_is_not_a_planned_output(self):
        mutation = (
            ROOT
            / "docs"
            / "superpowers"
            / "plans"
            / "internal-reference-uncommitted-mutation.md"
        )
        missing = (
            "docs/project-closure/"
            + "r7e-sol/UNCOMMITTED-PLANNED-OUTPUT.json"
        )
        mutation.write_text(f"- Create: `{missing}`\n", encoding="utf-8")
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(missing, output)

    def test_staged_only_plan_create_line_is_not_a_planned_output(self):
        mutation = (
            ROOT
            / "docs"
            / "superpowers"
            / "plans"
            / "internal-reference-staged-only-mutation.md"
        )
        missing = (
            "docs/project-closure/"
            + "r7e-sol/STAGED-ONLY-PLANNED-OUTPUT.json"
        )
        mutation.write_text(f"- Create: `{missing}`\n", encoding="utf-8")
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                index_env = {"GIT_INDEX_FILE": str(Path(temp_dir) / "index")}
                run_git("read-tree", "HEAD", extra_env=index_env)
                run_git("add", "--", mutation.relative_to(ROOT).as_posix(), extra_env=index_env)
                result = run_validator(index_env)
        finally:
            mutation.unlink(missing_ok=True)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(missing, output)

    def test_windows_style_ordinary_missing_path_is_rejected(self):
        mutation = ROOT / "docs" / "internal-reference-windows-path-mutation.md"
        missing = "docs" + r"\future\WINDOWS-MISSING.json"
        mutation.write_text(f"Current evidence: `{missing}`.\n", encoding="utf-8")
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn(missing.replace("\\", "/"), output)

    def test_absolute_environment_paths_are_not_repository_citations(self):
        mutation = ROOT / "docs" / "internal-reference-environment-path-mutation.md"
        lowercase_segment = "scr" + r"ipts\ENVIRONMENT-MISSING.py"
        absolute_path = "C:" + "\\workspace\\repo\\" + lowercase_segment
        mixed_case_venv = "C:" + r"\venv\Scripts\python.exe"
        mutation.write_text(
            f"Interpreter candidates: `{absolute_path}` and `{mixed_case_venv}`.\n",
            encoding="utf-8",
        )
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_ignored_report_is_not_part_of_the_prospective_corpus(self):
        mutation = ROOT / ".superpowers" / "sdd" / "internal-reference-ignored-mutation.md"
        ignored_missing = "docs/future/" + "IGNORED-MISSING.json"
        mutation.write_text(
            f"Current evidence: `{ignored_missing}`.\n",
            encoding="utf-8",
        )
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_resolved_path_in_a_prospective_file_passes(self):
        mutation = ROOT / "docs" / "internal-reference-resolved-mutation.md"
        mutation.write_text("Current evidence: `docs/CITING.md`.\n", encoding="utf-8")
        try:
            result = run_validator()
        finally:
            mutation.unlink(missing_ok=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
