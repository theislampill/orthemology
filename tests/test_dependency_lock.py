#!/usr/bin/env python3
"""Focused regressions for dependency-lock import classification."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_dependency_lock.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
