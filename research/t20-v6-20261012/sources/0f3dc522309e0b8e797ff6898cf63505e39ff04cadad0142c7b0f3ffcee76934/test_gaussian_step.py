"""Finite floating-point implementation controls, separate from the proofs."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np


class GaussianStepTests(unittest.TestCase):
    def step(self, *args):
        path = Path(__file__).with_name('gaussian_step.py')
        self.assertTrue(path.exists(), 'the Gaussian step implementation is missing')
        spec = importlib.util.spec_from_file_location('gaussian_step_under_test', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.gaussian_step(*args)

    def test_noncommuting_exact_rational_fixture(self):
        out = self.step([-1., 2.], [[2., 1.], [1., 3.]],
                        [3., -1.], [[1., 0.], [0., 2.]], np.log(4.))
        np.testing.assert_allclose(out['mean'], [1603/584, -371/584], atol=1e-14)
        np.testing.assert_allclose(out['covariance'], [[74/73, 2/73], [2/73, 150/73]], atol=1e-14)
        np.testing.assert_allclose(out['diffusion_covariance'], [[17/16, 1/8], [1/8, 9/4]], atol=1e-14)

    def test_singular_scalar_is_regularized_before_any_inverse(self):
        out = self.step([3.], [[0.]], [0.], [[1.]], np.log(2.))
        np.testing.assert_allclose(out['mean'], [6/7], atol=1e-14)
        np.testing.assert_allclose(out['covariance'], [[6/7]], atol=1e-14)

    def test_partial_rank_is_regularized(self):
        out = self.step([2., -1.], [[1., 1.], [1., 1.]],
                        [1., 3.], [[1., 0.], [0., .5]], np.log(2.))
        self.assertGreater(np.linalg.eigvalsh(out['covariance']).min(), 0.)

    def test_target_is_fixed(self):
        target = np.array([[2., .4], [.4, 1.]])
        out = self.step([1., -4.], target, [1., -4.], target, .7)
        np.testing.assert_allclose(out['mean'], [1., -4.], atol=1e-14)
        np.testing.assert_allclose(out['covariance'], target, atol=1e-14)

    def test_translation_covariance(self):
        m, g, shift = np.array([2., 3.]), np.array([1., -1.]), np.array([19., -7.])
        s, t = [[2., .2], [.2, .5]], [[1., 0.], [0., 2.]]
        one = self.step(m, s, g, t, .3)
        two = self.step(m+shift, s, g+shift, t, .3)
        np.testing.assert_allclose(two['mean']-shift, one['mean'], atol=1e-13)
        np.testing.assert_allclose(two['covariance'], one['covariance'], atol=1e-14)

    def test_invalid_step(self):
        for h in [0., -1., np.nan, np.inf]:
            with self.subTest(h=h), self.assertRaises(ValueError):
                self.step([0.], [[1.]], [0.], [[1.]], h)

    def test_invalid_target(self):
        for t in [[[0.]], [[-1.]], [[np.nan]]]:
            with self.subTest(t=t), self.assertRaises(ValueError):
                self.step([0.], [[1.]], [0.], t, .1)

    def test_negative_covariance(self):
        with self.assertRaises(ValueError):
            self.step([0.], [[-1e-4]], [0.], [[1.]], .1)

    def test_nonsymmetric_covariance(self):
        with self.assertRaises(ValueError):
            self.step([0., 0.], [[1., .1], [.2, 1.]], [0., 0.], np.eye(2), .1)

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            self.step([0., 0.], [[1.]], [0.], [[1.]], .1)

    def test_nonfinite_mean(self):
        with self.assertRaises(ValueError):
            self.step([np.nan], [[1.]], [0.], [[1.]], .1)

    def test_complex_parameters_rejected_before_float_cast(self):
        # A complex-to-float cast must not silently discard imaginary data.
        base = [np.array([0.]), np.array([[1.]]), np.array([0.]), np.array([[1.]]), .1]
        for index in range(4):
            values = list(base)
            values[index] = values[index].astype(complex)+7j
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.step(*values)

    def test_complex_step_rejected(self):
        for h in [1+2j, np.complex128(1+2j), np.complex128(1+0j)]:
            with self.subTest(h=h), self.assertRaises(ValueError):
                self.step([0.], [[1.]], [0.], [[1.]], h)


if __name__ == '__main__':
    unittest.main()
