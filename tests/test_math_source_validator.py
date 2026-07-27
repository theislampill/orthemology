#!/usr/bin/env python3
"""Focused contract for B5 inline machine-assignment classification."""
import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_math_source", ROOT / "scripts" / "validate_math_source.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def classify(span):
    """Use the desired boundary; parent behavior intentionally classifies none."""
    return getattr(VALIDATOR, "is_machine_assignment", lambda _span: False)(span)


class MachineAssignmentClassificationTests(unittest.TestCase):
    def test_accepts_complete_environment_assignments(self):
        accepted = (
            "PYTHONUTF8=1",
            "PYTHONIOENCODING=utf-8",
            "HOME=/srv/orthemology",
            "ENDPOINT=https://example.test/search?x=1",
            "QUERY_URL=https://example.test/search?q=a+b#result",
            "$env:Path='C:\\Python311'",
            "export LC_ALL=C.UTF-8",
        )
        for span in accepted:
            with self.subTest(span=span):
                self.assertTrue(classify(span), span)

    def test_accepts_neighboring_machine_identifiers(self):
        accepted = (
            "_CACHE_KEY=alpha.beta",
            "BUILD_ID=run-17",
            "CI_JOB_ID=12345",
            "$env:PYTHONHASHSEED=\"0\"",
            "MODE='$HOME'",
            "$env:MODE='$env:HOME'",
            "MODE='$(whoami)'",
            "PRICE='literal$cash'",
            "MODE='(whoami)'",
            'MODE="(literal)"',
            '$env:MODE="(Get-Date)"',
            '$env:MODE="`$env:HOME"',
            '$env:MODE="prefix-`$env:HOME"',
        )
        for span in accepted:
            with self.subTest(span=span):
                self.assertTrue(classify(span), span)

    def test_rejects_math_malformed_and_mixed_spans(self):
        rejected = (
            "x = y",
            "{x | P(x)}",
            "x ∈ A",
            "p → q",
            "x⃗",
            "=value",
            "MODE = fast",
            "MODE==fast",
            "MODE='fast",
            "$env:=fast",
            "MODE=fast=slow",
            "MODE=fast ∧ x",
            "MODE={x | P(x)}",
            "MODE=$(whoami)",
            "MODE=$HOME",
            "$env:MODE=$(Get-Date)",
            "$env:MODE=$env:HOME",
            'MODE="$HOME"',
            '$env:MODE="$env:HOME"',
            "MODE=(whoami)",
            "$env:MODE=(Get-Date)",
            'MODE="`$HOME"',
            '$env:MODE="``$env:HOME"',
            '$env:MODE="`$env:HOME`"',
            '$env:MODE="`"',
        )
        for span in rejected:
            with self.subTest(span=span):
                self.assertFalse(classify(span), span)


class BuildSourceExtractionTests(unittest.TestCase):
    def test_extracts_only_docs_owner_and_ignores_unrelated_paths(self):
        build_text = """
COMPATIBILITY_REPORT_PATH = pathlib.Path(
    "docs/project-closure/report.md"
)
DOCS = [
    ("sample", ["manuscript/source.md", "companion/source.md"]),
]
"""
        extract = getattr(VALIDATOR, "extract_build_sources", None)
        self.assertIsNotNone(extract, "exact DOCS source extraction is missing")
        self.assertEqual(
            extract(build_text),
            {"manuscript/source.md", "companion/source.md"},
        )


if __name__ == "__main__":
    unittest.main()
