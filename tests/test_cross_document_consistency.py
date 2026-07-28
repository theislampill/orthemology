#!/usr/bin/env python3
"""Regression contracts for migrated cross-document mathematics."""

import contextlib
import importlib.util
import io
import pathlib
import shutil
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_cross_document_consistency.py"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_cross_document_consistency",
        VALIDATOR_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


class MigratedMathConsistencyTests(unittest.TestCase):
    FILES = (
        "docs/verdict-registry.yaml",
        "theory/orthemic-core-formalization.md",
        "manuscript/orthemma-ortheme-systems-revised-draft.md",
        "docs/architecture-overview.md",
        "tests/verdict-fixtures.json",
        "schemas/verdict-record.schema.json",
        "docs/glossary.md",
    )

    def setUp(self):
        self.original_root = validator.ROOT

    def tearDown(self):
        validator.ROOT = self.original_root
        validator.FAILS.clear()

    def copy_fixture(self, destination):
        for relative in self.FILES:
            source = ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        shutil.copytree(
            ROOT / "docs" / "decisions",
            destination / "docs" / "decisions",
        )

    def run_validator(self, root):
        validator.ROOT = str(root)
        validator.FAILS.clear()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as stopped:
                validator.main()
        return stopped.exception.code, output.getvalue()

    def test_current_migrated_math_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = pathlib.Path(tmp)
            self.copy_fixture(fixture)

            code, output = self.run_validator(fixture)

        self.assertEqual(code, 0, output)
        self.assertIn("TOTAL: 0 failures", output)

    def test_semantic_mutations_are_rejected(self):
        mutations = (
            (
                "manuscript/orthemma-ortheme-systems-revised-draft.md",
                r"\operatorname{V5}, \operatorname{V6}\}",
                r"\operatorname{V5}\}",
                "manuscript states the registry CorePath",
            ),
            (
                "theory/orthemic-core-formalization.md",
                (
                    r"\operatorname{V2b-T}_q(e) \to "
                    r"\operatorname{V1}_q(e)"
                ),
                (
                    r"\operatorname{V1}_q(e) \to "
                    r"\operatorname{V2b-T}_q(e)"
                ),
                "core states the sole entailment V2b-T_q -> V1_q",
            ),
            (
                "manuscript/orthemma-ortheme-systems-revised-draft.md",
                r"\operatorname{V2b-T}_q \to \operatorname{V1}_q",
                r"\operatorname{V1}_q \to \operatorname{V2b-T}_q",
                "manuscript states the sole entailment",
            ),
            (
                "theory/orthemic-core-formalization.md",
                (
                    r"\operatorname{V3c} \notin "
                    r"\operatorname{ReqPath}(e)"
                ),
                r"\operatorname{V3c} \in \operatorname{ReqPath}(e)",
                "zero-burden rule uses ReqPath in core",
            ),
        )
        for relative, original, altered, expected_failure in mutations:
            with self.subTest(relative=relative, failure=expected_failure):
                with tempfile.TemporaryDirectory() as tmp:
                    fixture = pathlib.Path(tmp)
                    self.copy_fixture(fixture)
                    path = fixture / relative
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(original, text)
                    path.write_text(
                        text.replace(original, altered),
                        encoding="utf-8",
                    )

                    code, output = self.run_validator(fixture)

                self.assertEqual(code, 1, output)
                self.assertIn("[FAIL] %s" % expected_failure, output)


if __name__ == "__main__":
    unittest.main()
