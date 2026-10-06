"""The scoped Sixteenth successor must not rewrite the earlier cutoff."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_successor_fixtures import (
    make_bundle, rebind, save_bundle, fixture_suite_validator,
    fixture_receipt_validator,
)

spec = importlib.util.spec_from_file_location(
    'sixteenth_boundary_validator',
    Path(__file__).resolve().parents[1] / 'scripts/validate_v5_successors.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SixteenthBoundaryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bundle, self.anchor = make_bundle(self.root)

    def run_gate(self, tranche=16, cutoff='sixteenth-final', calculus='NONE'):
        self.bundle['registry']['cutoff'] = cutoff
        self.bundle['results'][0].update(tranche=tranche, calculus=calculus)
        self.bundle['calculus'][0]['calculus'] = calculus
        rebind(self.bundle)
        save_bundle(self.root, self.bundle)
        return validator.validate_bundle(
            self.bundle, self.root, baseline_anchor=self.anchor,
            suite_validator=fixture_suite_validator,
            receipt_validator=fixture_receipt_validator)

    def test_sixteenth_inherited_source_has_no_new_kernel_credit(self):
        self.assertEqual(self.run_gate()['fresh_qualified_results'], 0)

    def test_separate_hasc_can_be_registered_without_adoption(self):
        self.assertEqual(self.run_gate(calculus='P01AC.UnaryCertificate.HasC')['results'], 1)
        self.assertEqual(self.bundle['calculus'][0]['canonical_adoption'], 'NOT_ADOPTED')

    def test_fifteenth_cutoff_still_rejects_sixteenth(self):
        with self.assertRaises(ValueError):
            self.run_gate(cutoff='fifteenth-final')

    def test_seventeenth_is_not_authorized(self):
        with self.assertRaises(ValueError):
            self.run_gate(tranche=17)

    def test_hasc_is_not_retroactively_assigned_to_fifteenth(self):
        with self.assertRaises(ValueError):
            self.run_gate(tranche=15, calculus='P01AC.UnaryCertificate.HasC')


if __name__ == '__main__':
    unittest.main()
