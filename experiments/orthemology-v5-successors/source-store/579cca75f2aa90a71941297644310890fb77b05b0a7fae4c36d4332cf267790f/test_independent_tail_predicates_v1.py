"""Synthetic-only tests. Actual aggregates are deliberately absent."""
import unittest
from fractions import Fraction
from independent_tail_predicates_v1 import parse_rational, evaluate


class IndependentPredicateTests(unittest.TestCase):
    def result(self, t='1/20', v='1/400', k=400, r=1):
        result = evaluate(t, v, k, r)
        self.assertIsInstance(result, dict)
        return result

    def test_exact_rational_parser(self):
        self.assertEqual(parse_rational('3/6'), Fraction(1, 2))
        self.assertEqual(parse_rational('-3/6'), Fraction(-1, 2))
        self.assertEqual(parse_rational('+3'), Fraction(3))
        self.assertEqual(parse_rational('0/7'), Fraction(0))

    def test_malformed_rationals_rejected(self):
        for token in ('', ' 1/2', '1/2 ', '1.5', '1e-3', 'NaN', '1/0', '1/-2', '--1', '1/2/3', True, 1, 0.5, None):
            with self.subTest(token=token):
                with self.assertRaises(ValueError):
                    parse_rational(token)

    def test_positive_certificate(self):
        result = self.result()
        self.assertEqual(result['status'], 'certificate_conditions_hold')
        self.assertIs(result['A'], True)
        self.assertIs(result['B'], True)
        self.assertEqual(result['A_margin'], '21/400')
        self.assertEqual(result['B_margin'], '1221/400')
        self.assertEqual(result['M'], '1/400')
        self.assertEqual(result['strict_lower_bound'], '167/1500')

    def test_strict_a_equality_is_failure(self):
        result = self.result('11/10', '1', 1000, 1000)
        self.assertIs(result['A'], False)
        self.assertEqual(result['A_margin'], '0')
        self.assertEqual(result['status'], 'certificate_unavailable')
        self.assertNotIn('strict_lower_bound', result)

    def test_strict_b_equality_is_failure(self):
        result = self.result('1/1000', '1/3721', 1000, 1)
        self.assertIs(result['B'], False)
        self.assertEqual(result['B_margin'], '0')
        self.assertEqual(result['status'], 'certificate_unavailable')

    def test_each_negative_predicate_margin_fails(self):
        self.assertEqual(self.result('2', '1', 1000, 1)['status'], 'certificate_unavailable')
        self.assertEqual(self.result('1/100', '1', 1, 1)['status'], 'certificate_unavailable')

    def test_zero_threshold_has_exact_tail_one(self):
        for variance in ('0', '1/400'):
            result = self.result('0', variance)
            self.assertEqual(result['status'], 'zero_threshold_exact_tail_one')
            self.assertEqual(result['exact_tail'], '1')
            self.assertNotIn('A', result)

    def test_bad_counts_or_inconsistent_threshold_rejected(self):
        cases = [('1', '0', 1, 1), ('-1', '1', 1, 1), ('0', '-1', 1, 1),
                 ('0', '0', 0, 1), ('0', '0', 1, -1), ('0', '0', True, 1),
                 ('0', '0', 1, False), ('0', '0', 1.0, 1), ('0', '0', '1', 1)]
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    evaluate(*args)


if __name__ == '__main__':
    unittest.main()
