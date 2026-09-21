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


class AcceptedPublicationRegistrationTests(unittest.TestCase):
    def test_current_publication_inventory_matches_exact_source_occurrences(self):
        self.assertEqual([], VALIDATOR.validate_inventory(ROOT))

    def test_generated_quotation_scope_requires_exact_manifest_binding(self):
        from validate_repo import preserved_math_source, load_source_map
        path = ROOT / "docs/provenance/v5-consolidation/THEOREM_INDEX.md"
        sources = load_source_map(ROOT)
        original = path.read_bytes()
        self.assertTrue(preserved_math_source(path, sources, ROOT))
        try:
            path.write_bytes(original + b"\nChanged index.\n")
            self.assertFalse(preserved_math_source(path, sources, ROOT))
        finally:
            path.write_bytes(original)
        self.assertFalse(preserved_math_source(ROOT / "docs/notation-gallery.md", sources, ROOT))

    def test_prime_renders_without_silent_unknown_command_fallback(self):
        import typst
        from latex_to_typst_math import translate_inline, MathConvertError
        rendered = translate_inline(r"m\prime \mapsto O^*(m\prime; A)")
        self.assertIn("prime", rendered)
        self.assertTrue(typst.compile(("$" + rendered + "$").encode()).startswith(b"%PDF"))
        with self.assertRaises(MathConvertError):
            translate_inline(r"m\unregisteredPrime")


class BuildSourceExtractionTests(unittest.TestCase):
    def test_extracts_only_docs_owner_and_ignores_unrelated_paths(self):
        build_text = """
COMPATIBILITY_REPORT_PATH = pathlib.Path(
    "docs/project-closure/r7e-sol/R7E-SOL-ARXIV-COMPATIBILITY.md"
)
DOCS = [
    (
        "sample",
        [
            "manuscript/orthemma-ortheme-systems-revised-draft.md",
            "companion/orthability-and-the-ground-of-intelligibility.md",
        ],
    ),
]
"""
        extract = getattr(VALIDATOR, "extract_build_sources", None)
        self.assertIsNotNone(extract, "exact DOCS source extraction is missing")
        self.assertEqual(
            extract(build_text),
            {
                "manuscript/orthemma-ortheme-systems-revised-draft.md",
                "companion/orthability-and-the-ground-of-intelligibility.md",
            },
        )


if __name__ == "__main__":
    unittest.main()
