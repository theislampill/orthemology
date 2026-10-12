from fractions import Fraction as F
import unittest
from epistemic import target_decoder, weight_witness_2d, is_nash_2x2, local_factorization

class EpistemicTests(unittest.TestCase):
    def test_score_collision_is_target_relative(self):
        profiles = ((1, 0), (0, 1))
        self.assertIsNone(target_decoder(profiles, lambda x: sum(x), lambda x: x[0]))
        self.assertEqual(target_decoder(profiles, lambda x: sum(x), lambda x: sum(x)), {1: 1})

    def test_injective_score_recovers_any_finite_target_without_order_claim(self):
        profiles = ((1, 0), (0, 1))
        self.assertEqual(target_decoder(profiles, lambda x: x[0]+2*x[1], lambda x: x[0]),
                         {1: 1, 2: 0})

    def test_strict_positive_weights_detect_boundary_pareto_gain(self):
        self.assertIsNone(weight_witness_2d(((0, 0), (1, 0))))
        self.assertEqual(weight_witness_2d(((0, 0), (1, 0)), strict_positive=False), (F(0), F(1)))

    def test_supported_crossing_frontier_has_positive_weight_witness(self):
        weights = weight_witness_2d(((0, 0), (-2, 1), (-3, 3)))
        self.assertIsNotNone(weights)
        self.assertTrue(all(v > 0 for v in weights))

    def test_pure_unsupported_middle_is_dominated_after_mixing(self):
        self.assertIsNone(weight_witness_2d(((2, -1), (0, 0), (-1, 2))))

    def test_nonlinear_payoff_reencoding_changes_mixed_equilibrium(self):
        a = ((0, 2), (1, 0)); b = ((1, 0), (0, 1))
        self.assertTrue(is_nash_2x2(a, b, F(1, 2), F(2, 3)))
        aa = ((0, 4), (1, 0))
        self.assertFalse(is_nash_2x2(aa, b, F(1, 2), F(2, 3)))
        self.assertTrue(is_nash_2x2(aa, b, F(1, 2), F(4, 5)))

    def test_hidden_repair_bit_cannot_be_read_by_local_chooser(self):
        self.assertIsNone(local_factorization((0, 1), lambda b: 'same', lambda b: b))
        self.assertEqual(local_factorization((0, 1), lambda b: b, lambda b: b), {0: 0, 1: 1})

if __name__ == '__main__': unittest.main()
