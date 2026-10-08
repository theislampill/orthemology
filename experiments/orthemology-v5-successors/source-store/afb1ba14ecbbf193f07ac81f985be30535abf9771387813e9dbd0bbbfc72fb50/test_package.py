"""Synthetic numerical and distribution-boundary tests; no source trials."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from scipy import special

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = importlib.import_module('reanalyse')
        cls.a = importlib.import_module('fit_bfgs')
        cls.b = importlib.import_module('fit_checked')

    def test_derivatives(self):
        X = np.column_stack([np.ones(8), np.linspace(-1, 1, 8)])
        y = np.array([0., 0., .2, .4, .8, .5, .9, 1.])
        w, beta, h = np.arange(1., 9.), np.array([.3, 1.4]), 1e-5
        _, g, H = self.b.objective_parts(beta, X, y, w)
        directions = np.eye(2) * h
        ng = np.array([(self.b.objective_parts(beta+d, X, y, w)[0]-self.b.objective_parts(beta-d, X, y, w)[0])/(2*h) for d in directions])
        nH = np.column_stack([(self.b.objective_parts(beta+d, X, y, w)[1]-self.b.objective_parts(beta-d, X, y, w)[1])/(2*h) for d in directions])
        np.testing.assert_allclose(g, ng, rtol=1e-7, atol=1e-8)
        np.testing.assert_allclose(H, nH, rtol=1e-7, atol=1e-8)

    def test_both_slope_signs_and_balanced_weighting(self):
        x = np.repeat(np.array([-.15, -.07, -.035, -.015, .015, .035, .07, .15]), 16)
        for beta in (.8, -.8):
            y = special.ndtr(.17+beta*x/.15)
            a = self.a.fit(x, y)
            b = self.b.fit(x, y)
            w = self.b.fit(x, y, 'trial_count')
            self.assertAlmostEqual(a['sensitivity'], beta/.15/np.sqrt(2*np.pi), places=6)
            self.assertAlmostEqual(b['sensitivity'], beta/.15/np.sqrt(2*np.pi), places=9)
            self.assertAlmostEqual(b['sensitivity'], w['sensitivity'], places=9)
            self.assertAlmostEqual(b['intercept'], .17, places=9)

    def test_unequal_bin_counts_do_not_change_default_weighting(self):
        levels = np.array([-.15, -.07, -.035, -.015, .015, .035, .07, .15])
        counts = [3,13,5,7,10,4,11,11]
        means = [.2,.1,.35,.4,.7,.8,.8,.9]
        x, y = np.repeat(levels, counts), np.repeat(means, counts)
        for implementation in (self.a, self.b):
            default = implementation.fit(x, y)['sensitivity']
            equal = implementation.fit(x, y, 'equal_bin')['sensitivity']
            counted = implementation.fit(x, y, 'trial_count')['sensitivity']
            self.assertAlmostEqual(default, equal, places=12)
            self.assertGreater(abs(equal-counted), 1e-3)

    def test_paired_direction_and_unit(self):
        ind = np.array([1., 2., 4., 8., 16.])
        inf = np.ones(5)
        d = inf-ind
        out = self.r.paired(ind, inf)
        self.assertEqual(out['paired_dyads'], 5)
        self.assertEqual(out['df'], 4)
        self.assertAlmostEqual(out['t'], d.mean()/(d.std(ddof=1)/np.sqrt(5)), places=13)
        self.assertLess(out['INF_minus_IND_mean'], 0)

    def test_missing_timing_preserves_all_choices(self):
        ind, inf = synthetic_matrices()
        curves, disagreements = self.r.channels(ind, inf)
        self.assertEqual(disagreements, 64)
        self.assertEqual(len(curves['joint_IND'][0]), 128)
        self.assertEqual(len(curves['kb_joint_IND'][0]), 64)
        self.assertTrue(np.isfinite(curves['joint_IND'][1]).all())
        np.testing.assert_array_equal(curves['kb_private'][1]+1, ind[:, 9])
        np.testing.assert_array_equal(curves['joint_INF'][1]+1, inf[:, 9])

    def test_missing_or_invalid_selected_response_is_rejected(self):
        for column, value in [(7, np.nan), (7, 0.)]:
            ind, inf = synthetic_matrices()
            ind[0, column] = value
            with self.assertRaises(ValueError):
                self.r.channels(ind, inf)

    def test_wrong_timing_missingness_rejected(self):
        ind, inf = synthetic_matrices()
        ind[1, 18] = np.nan
        with self.assertRaises(ValueError):
            self.r.channels(ind, inf)

    def test_bad_fit_inputs_rejected(self):
        x = np.array([-.15, -.07, -.035, -.015, .015, .035, .07, .15])
        for implementation in (self.a, self.b):
            with self.assertRaises(ValueError):
                implementation.fit(x, np.full(8, np.nan))
            with self.assertRaises(ValueError):
                implementation.fit(x, np.full(8, 1.2))
            with self.assertRaises(ValueError):
                implementation.fit(x, np.linspace(.1, .9, 8), 'unknown')

    def test_manifest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'input'
            path.write_bytes(b'not source data')
            with self.assertRaises(ValueError):
                self.r.checked_bytes(path, '0'*64)

    def test_cli_help_has_only_local_input_and_aggregate_output(self):
        p = subprocess.run([sys.executable, '-B', str(HERE/'reanalyse.py'), '--help'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('--decisions-zip', p.stdout)
        self.assertIn('--summary-xlsx', p.stdout)
        self.assertIn('--output', p.stdout)
        self.assertNotIn('--download', p.stdout)
        self.assertNotIn('--dyad', p.stdout)

    def test_aggregate_contract_rejects_record_output(self):
        self.assertEqual(set(self.r.aggregate_template()), {
            'paired_dyads','IND_mean','INF_mean','INF_minus_IND_mean','t','df',
            'p_two_sided','difference_CI95','workbook_reconciliation_4dp'})

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'input'
            path.write_text('preserve')
            with self.assertRaises(ValueError):
                self.r.write_aggregate({}, path, (path,))
            self.assertEqual(path.read_text(), 'preserve')

    def test_output_hardlink_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'source'
            destination = Path(directory)/'destination'
            source.write_text('preserve')
            destination.hardlink_to(source)
            with self.assertRaises(ValueError):
                self.r.write_aggregate({}, destination, (source,))
            self.assertEqual(source.read_text(), 'preserve')



def synthetic_matrices():
    """Invented balanced schema fixture; no empirical rows are embedded."""
    n = 128
    a, b = np.zeros((n, 19)), np.zeros((n, 11))
    x = np.tile(np.array([-.15, -.07, -.035, -.015, .015, .035, .07, .15]), 16)
    interval = np.where(x < 0, 1, 2)
    kb = np.arange(n)%2
    ms = np.where(np.arange(n)%2 == 0, kb, 1-kb)
    joint = kb.copy()
    for matrix in (a, b):
        matrix[:, 3], matrix[:, 4] = interval, np.abs(x)
    for y, sign, correct, stored in [(kb,7,8,9),(ms,10,11,12),(joint,13,14,15)]:
        a[:,sign], a[:,stored] = 2*y-1, y+1
        a[:,correct] = y+1 == interval
    a[:,18] = np.where(kb == ms, np.nan, 1.)
    b[:,7], b[:,9], b[:,8] = 2*joint-1, joint+1, joint+1 == interval
    return a, b


if __name__ == '__main__':
    unittest.main(verbosity=2)
