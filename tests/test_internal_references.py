#!/usr/bin/env python3
"""Focused mutations for planned-output internal-reference handling."""
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_internal_references.py"
PLANNED_PATH = "docs/project-closure/" + "r7e-sol/ORTHING-CANDIDATE-LEDGER.json"


def run_validator():
    return subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
