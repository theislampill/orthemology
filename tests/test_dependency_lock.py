#!/usr/bin/env python3
"""Focused regressions for dependency-lock import classification."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from importlib import metadata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_dependency_lock.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
POPPLER_LOCK = ROOT / "publication" / "poppler-linux-64.explicit.txt"
PROVISIONER = ROOT / "scripts" / "provision_ci_infrastructure.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_dependency_lock", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


class DependencyClassificationTests(unittest.TestCase):
    def classify(self, used, local_modules=()):
        return validator.classify_imports(set(used), set(local_modules))

    def test_future_import_is_stdlib(self):
        result = self.classify({"__future__"})
        self.assertEqual({"__future__"}, result["stdlib"])
        self.assertEqual(set(), result["third_party"])
        self.assertEqual(set(), result["unmapped"])

    def test_second_old_hint_omission_is_stdlib(self):
        self.assertIn("zoneinfo", sys.stdlib_module_names)
        result = self.classify({"zoneinfo"})
        self.assertEqual({"zoneinfo"}, result["stdlib"])
        self.assertEqual(set(), result["third_party"])
        self.assertEqual(set(), result["unmapped"])

    def test_mapped_third_party_and_missing_pin_control(self):
        result = self.classify({"yaml"})
        self.assertEqual({"yaml"}, result["third_party"])
        self.assertEqual(set(), result["unmapped"])
        self.assertEqual(
            ["PyYAML"],
            validator.find_missing_distributions(
                result["third_party"], {}, validator.IMPORT_TO_DIST
            ),
        )
        self.assertEqual(
            [],
            validator.find_missing_distributions(
                result["third_party"], {"PyYAML": "6.0.3"}, validator.IMPORT_TO_DIST
            ),
        )

    def test_python311_transitive_backport_is_exactly_pinned(self):
        self.assertLess(sys.version_info, (3, 13))
        requirements = metadata.requires("referencing") or []
        self.assertTrue(
            any(requirement.startswith("typing-extensions") for requirement in requirements)
        )
        lock_lines = {
            line.strip()
            for line in (ROOT / "requirements-ci.lock.txt")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip() and not line.startswith("#")
        }
        self.assertIn("typing_extensions==4.16.0", lock_lines)

    def test_unknown_import_fails_closed(self):
        unknown = "orthemology_unmapped_dependency_probe"
        result = self.classify({unknown})
        self.assertEqual({unknown}, result["unmapped"])
        self.assertEqual(set(), result["stdlib"])
        self.assertEqual(set(), result["third_party"])
        self.assertEqual(set(), result["local"])

    def test_repository_local_module_is_excluded(self):
        local = "orthemology_local_dependency_probe"
        result = self.classify({local}, {local})
        self.assertEqual({local}, result["local"])
        self.assertEqual(set(), result["third_party"])
        self.assertEqual(set(), result["unmapped"])

    def test_top_level_namespace_package_is_repository_local(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            namespace = root / "local_namespace"
            namespace.mkdir()
            (namespace / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
            package = root / "local_package"
            package.mkdir()
            (package / "__init__.py").write_text("", encoding="utf-8")
            unrelated = root / "unrelated_directory"
            unrelated.mkdir()

            local_modules = validator.find_local_modules(root)
            self.assertIn("local_namespace", local_modules)
            self.assertIn("local_package", local_modules)
            self.assertNotIn("unrelated_directory", local_modules)

    def test_mixed_partition_is_exact_and_disjoint(self):
        local = "orthemology_local_dependency_probe"
        unknown = "orthemology_unmapped_dependency_probe"
        used = {"__future__", "zoneinfo", "yaml", local, unknown}
        result = self.classify(used, {local})
        expected = {
            "stdlib": {"__future__", "zoneinfo"},
            "third_party": {"yaml"},
            "local": {local},
            "unmapped": {unknown},
        }
        self.assertEqual(expected, result)
        self.assertEqual(used, set().union(*result.values()))
        categories = list(result.values())
        for index, left in enumerate(categories):
            for right in categories[index + 1 :]:
                self.assertTrue(left.isdisjoint(right))

    def test_repository_scan_retains_future_import_without_unmapped_failure(self):
        used = validator.scan_repository_imports(ROOT)
        self.assertIn("__future__", used)
        local_modules = validator.find_local_modules(ROOT)
        result = validator.classify_imports(used, local_modules)
        self.assertNotIn("__future__", result["unmapped"])
        self.assertEqual(set(), result["unmapped"])

    def test_workflow_runs_focused_test_beside_production_validator(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        focused = "python tests/test_dependency_lock.py"
        production = "python scripts/validate_dependency_lock.py"
        self.assertEqual(1, workflow.count(focused))
        self.assertEqual(1, workflow.count(production))
        self.assertLess(workflow.index(focused), workflow.index(production))
        install_lines = [
            line.strip() for line in workflow.splitlines() if "pip install" in line
        ]
        self.assertEqual(
            ["run: pip install --quiet -r requirements-ci.lock.txt"], install_lines
        )

    def test_ci_poppler_lock_is_complete_sha256_explicit_environment(self):
        self.assertTrue(
            hasattr(validator, "parse_explicit_package_lock"),
            "dependency validator must parse the governed Poppler lock",
        )
        entries = validator.parse_explicit_package_lock(
            POPPLER_LOCK.read_text(encoding="utf-8")
        )
        self.assertEqual(61, len(entries))
        self.assertTrue(
            all(
                entry["url"].startswith(
                    "https://conda.anaconda.org/conda-forge/"
                )
                for entry in entries
            )
        )
        self.assertTrue(
            all(
                len(entry["sha256"]) == 64
                and set(entry["sha256"]) <= set("0123456789abcdef")
                for entry in entries
            )
        )
        poppler = [
            entry
            for entry in entries
            if entry["filename"].startswith("poppler-25.07.0-h13eef12_1.")
        ]
        self.assertEqual(
            [
                {
                    "filename": "poppler-25.07.0-h13eef12_1.conda",
                    "sha256": (
                        "a45c9c35808c44d817209af859d2e9d90b89c72f8cd8fcea"
                        "20163ee774583ed8"
                    ),
                    "url": (
                        "https://conda.anaconda.org/conda-forge/linux-64/"
                        "poppler-25.07.0-h13eef12_1.conda"
                    ),
                }
            ],
            poppler,
        )

    def test_workflow_provisions_and_verifies_exact_pdf_infrastructure(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        provisioner = PROVISIONER.read_text(encoding="utf-8")
        self.assertIn('python-version: "3.11.9"', workflow)
        self.assertIn(
            "run: python scripts/provision_ci_infrastructure.py",
            workflow,
        )
        required = (
            (
                "https://github.com/mamba-org/micromamba-releases/releases/"
                "download/2.8.1-0/micromamba-linux-64"
            ),
            "9689782d863c05a1bf5d2d371ba527104e7a4eb4310c1637d8653b751aed9c82",
            "bc1b26e6a386d853fd6e07225bb3b0b7a17a2a19b2ed51b5aaacedb3597ec6c3",
            "poppler-linux-64.explicit.txt",
            '"create"',
            '"--no-rc"',
            (
                "texlive/texlive@sha256:"
                "ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51"
            ),
            "sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1",
            "linux/amd64",
            '("pdfinfo", "pdftoppm", "pdffonts")',
            '[executable, "-v"]',
        )
        for literal in required:
            with self.subTest(literal=literal):
                self.assertIn(literal, provisioner)
        self.assertLess(
            provisioner.index("observed = sha256_file(download)"),
            provisioner.index("str(micromamba),"),
        )
        self.assertLess(
            provisioner.index("observed_lock = sha256_file(POPPLER_LOCK)"),
            provisioner.index("str(micromamba),"),
        )

    def test_workflow_fetches_publication_source_history(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "- uses: actions/checkout@v6\n"
            "        with:\n"
            "          fetch-depth: 0",
            workflow,
            "PDF parity requires the source commits bound by package sidecars",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
