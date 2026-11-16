#!/usr/bin/env python3
"""Focused source-classification, publication and scholarly-display contracts."""
import importlib.util
import json
import pathlib
import tempfile
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


class ScholarlyDisplaySourceTests(unittest.TestCase):
    """Catch omitted current-source scans and the observed raw-HTML delimiter risk."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)
        self.owner = self.root / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json"
        self.owner.parent.mkdir(parents=True)
        self.source = self.root / "mathematics/example.md"
        self.source.parent.mkdir()
        self.source.write_text("```math\n0\\lt{}x<1\n```\n", encoding="utf-8")
        self.write_owner([{"role": "work-source", "path": "mathematics/example.md"}])

    def write_owner(self, rows):
        self.owner.write_text(json.dumps({"source_additions": rows}), encoding="utf-8")

    def issues(self):
        check = getattr(VALIDATOR, "validate_scholarly_display_source", lambda _root: [])
        return check(self.root)

    def test_rejects_the_two_observed_unsafe_product_limit_forms(self):
        for formula in (r"\prod_{s<N}p_s", r"L_t=\prod_{s<t}p_s", r"0<x<1"):
            with self.subTest(formula=formula):
                self.source.write_text("```math\n" + formula + "\n```\n", encoding="utf-8")
                issues = self.issues()
                self.assertTrue(issues, "current scholarly display bypassed the source guard")
                self.assertTrue(any("mathematics/example.md:1" in issue for issue in issues), issues)

    def test_accepts_explicit_relations_and_non_tag_operands(self):
        self.source.write_text(
            "```math\n" + r"\prod_{s\lt{}N}p_s,\quad 0\lt{}x<1,\quad f(x)<\infty" + "\n```\n",
            encoding="utf-8",
        )
        self.assertEqual(self.issues(), [])

    def test_finds_nested_and_long_math_fences_without_reading_code_examples(self):
        self.source.write_text(
            "Inline $`x<y`$.\n\n```python\nprint('x<y')\n```\n\n"
            "````text\n```math\nx<y\n```\n````\n\n"
            "> ~~~~math\n> x<y\n> ~~~~\n",
            encoding="utf-8",
        )
        issues = self.issues()
        self.assertEqual(len(issues), 1, issues)
        self.assertIn("mathematics/example.md:13", issues[0])

    def test_checks_every_current_work_and_ignores_supporting_prose(self):
        second = self.root / "mathematics/second.md"
        second.write_text("```math\nx<y\n```\n", encoding="utf-8")
        support = self.root / "fixture-docs" / "notes.md"
        support.parent.mkdir()
        support.write_text("```math\nx<y\n```\n", encoding="utf-8")
        self.write_owner([
            {"role": "work-source", "path": "mathematics/example.md"},
            {"role": "work-source", "path": "mathematics/second.md"},
            {"role": "supporting-evidence", "path": "fixture-docs/notes.md"},
        ])
        issues = self.issues()
        self.assertEqual(len(issues), 1, issues)
        self.assertIn("mathematics/second.md", issues[0])

    def test_missing_owner_or_source_and_empty_population_fail(self):
        self.owner.unlink()
        self.assertTrue(self.issues(), "missing owner must not make the gate empty-success")
        self.write_owner([])
        self.assertTrue(self.issues(), "empty source population must not pass")
        self.write_owner([{"role": "work-source", "path": "mathematics/missing.md"}])
        self.assertTrue(self.issues(), "a missing admitted work must not be skipped")

    def test_malformed_owner_records_and_escaping_paths_fail(self):
        for rows in (None, [None], [{"role": "work-source"}],
                     [{"role": "work-source", "path": "../outside.md"}],
                     [{"role": "work-source", "path": "/outside.md"}]):
            with self.subTest(rows=rows):
                self.write_owner(rows)
                self.assertTrue(self.issues(), "invalid source owner must not be skipped")


if __name__ == "__main__":
    unittest.main()
