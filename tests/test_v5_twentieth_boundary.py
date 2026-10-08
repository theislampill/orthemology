"""The Twentieth cutoff is additive; it confers no scientific or adoption credit."""
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
    'twentieth_boundary_validator',
    Path(__file__).resolve().parents[1] / 'scripts/validate_v5_successors.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class TwentiethBoundaryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bundle, self.anchor = make_bundle(self.root)

    def run_gate(self, tranche=20, cutoff='twentieth-final', calculus='NONE'):
        self.bundle['registry']['cutoff'] = cutoff
        self.bundle['results'][0].update(tranche=tranche, calculus=calculus)
        self.bundle['calculus'][0]['calculus'] = calculus
        rebind(self.bundle)
        save_bundle(self.root, self.bundle)
        return validator.validate_bundle(
            self.bundle, self.root, baseline_anchor=self.anchor,
            suite_validator=fixture_suite_validator,
            receipt_validator=fixture_receipt_validator)

    def test_twentieth_admits_only_bounded_seventh_through_twentieth(self):
        for tranche in (7, 15, 16, 17, 18, 19, 20):
            with self.subTest(tranche=tranche):
                self.assertEqual(self.run_gate(tranche=tranche)['results'], 1)

    def test_twentieth_does_not_create_fresh_kernel_credit(self):
        self.assertEqual(self.run_gate()['fresh_qualified_results'], 0)
        self.assertEqual(self.bundle['statuses'][0]['fresh_evidence'], 'NOT_RUN')
        self.assertEqual(self.bundle['statuses'][0]['receipt_ids'], [])
        self.assertEqual(self.bundle['calculus'][0]['canonical_adoption'], 'NOT_ADOPTED')

    def test_twenty_first_is_outside_twentieth_cutoff(self):
        with self.assertRaisesRegex(ValueError, 'Out-of-scope tranche'):
            self.run_gate(tranche=21)

    def test_lower_bound_and_true_integer_requirement_remain(self):
        for tranche in (6, True, False, '20', 20.0):
            with self.subTest(tranche=tranche):
                with self.assertRaisesRegex(ValueError, 'Out-of-scope tranche'):
                    self.run_gate(tranche=tranche)

    def test_sixteenth_still_rejects_seventeenth(self):
        with self.assertRaisesRegex(ValueError, 'Out-of-scope tranche'):
            self.run_gate(tranche=17, cutoff='sixteenth-final')

    def test_fifteenth_still_rejects_sixteenth(self):
        with self.assertRaisesRegex(ValueError, 'Out-of-scope tranche'):
            self.run_gate(tranche=16, cutoff='fifteenth-final')

    def test_unknown_cutoff_is_rejected(self):
        with self.assertRaises(ValueError):
            self.run_gate(cutoff='twenty-first-final')

    def test_twentieth_does_not_widen_hasc_assignment(self):
        for tranche in (15, 17, 18, 19, 20):
            with self.subTest(tranche=tranche):
                with self.assertRaisesRegex(ValueError, 'HasC belongs'):
                    self.run_gate(tranche=tranche, calculus='P01AC.UnaryCertificate.HasC')
        self.assertEqual(self.run_gate(tranche=16, calculus='P01AC.UnaryCertificate.HasC')['results'], 1)

    def test_hase_does_not_collapse_other_calculus_identities(self):
        self.assertEqual(self.run_gate(calculus='P01AC.ExtensionalRepair.HasE')['results'], 1)
        self.assertEqual(self.bundle['results'][0]['calculus'], 'P01AC.ExtensionalRepair.HasE')
        with self.assertRaises(ValueError):
            self.run_gate(calculus='HasE')

    def test_fresh_qualification_requires_actual_receipts(self):
        self.bundle['statuses'][0]['fresh_evidence'] = 'FRESH_KERNEL_COMPONENTS'
        with self.assertRaises(ValueError):
            self.run_gate()


if __name__ == '__main__':
    unittest.main()
