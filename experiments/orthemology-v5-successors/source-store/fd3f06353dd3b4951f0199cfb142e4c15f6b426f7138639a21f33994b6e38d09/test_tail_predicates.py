"""Synthetic-only predicate tests, preserving the corresponding frozen v2 tests."""
import itertools
from fractions import Fraction as F
import unittest
import tail_predicates

class TailCheckerTests(unittest.TestCase):
    def setUp(self):
        self.c = tail_predicates

    def test_synthetic_pass_and_exact_differences(self):
        r = self.c.evaluate(400, 1, F(1, 20), F(1, 400))
        self.assertEqual(r["status"], "STRICT_LOWER_CERTIFICATE_PASS")
        self.assertEqual(self.c.rational(r["checks"]["A"]["right_minus_left"]), F(21, 400))
        self.assertEqual(self.c.rational(r["strict_lower_bound"]), F(167, 1500))


    def test_each_strict_equality_fails(self):
        a = self.c.evaluate(100, 1, F(11, 10), F(1))
        b = self.c.evaluate(1, 1, F(1), F(1000000, 3721))
        self.assertFalse(a["checks"]["A"]["passed"])
        self.assertFalse(b["checks"]["B"]["passed"])
        self.assertEqual(a["status"], "CERTIFICATE_UNAVAILABLE")
        self.assertNotIn("strict_lower_bound", a)


    def test_degenerate_and_malformed_cases(self):
        self.assertEqual(self.c.evaluate(1, 1, F(0), F(0))["status"], "ZERO_THRESHOLD_TAIL_ONE")
        self.assertEqual(self.c.evaluate(1, 1, F(0), F(1))["status"], "ZERO_THRESHOLD_TAIL_ONE")
        for args in [(1, 1, F(1), F(0)), (1, 1, F(-1), F(1)), (1, 1, F(1), F(-1)),
                     (0, 1, F(0), F(1)), (True, 1, F(0), F(1)), (1, 1.0, F(0), F(1)),
                     (1, 1, 0.0, F(1))]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.c.evaluate(*args)


    def test_rational_parser_rejects_nonexact_inputs(self):
        self.assertEqual(self.c.rational({"numerator": "-2", "denominator": "4"}), F(-1, 2))
        for obj in [{"numerator": 1, "denominator": "2"}, {"numerator": "1.0", "denominator": "2"},
                    {"numerator": "NaN", "denominator": "2"}, {"numerator": "1", "denominator": "0"},
                    {"numerator": "1", "denominator": "-2"}, {"numerator": "1"},
                    {"numerator": "1", "denominator": "2", "extra": 3}]:
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                self.c.rational(obj)


    def test_independent_aggregate_field_reconciliation(self):
        description = {"games": 400, "T": {"numerator": "1", "denominator": "20"},
                       "V": {"numerator": "1", "denominator": "400"}}
        a = {"exact_description": description}
        b = {"independent_exact_description": dict(description)}
        self.assertEqual(self.c.reconcile(a, b), (400, F(1, 20), F(1, 400)))
        b["independent_exact_description"]["games"] = 399
        with self.assertRaises(ValueError):
            self.c.reconcile(a, b)


    def test_each_games_count_requires_positive_nonboolean_integer(self):
        original = {"games": 400, "T": {"numerator": "1", "denominator": "20"},
                    "V": {"numerator": "1", "denominator": "400"}}
        for field in ("original", "independent"):
            for bad in (400.0, True, 0, -1, "400"):
                a, b = dict(original), dict(original)
                (a if field == "original" else b)["games"] = bad
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    self.c.reconcile({"exact_description": a}, {"independent_exact_description": b})


    def test_inclusive_endpoint_controls_and_zero_case(self):
        for coefficients, threshold, expected in [([F(1), F(1)], F(2), F(1, 2)),
                                                   ([F(1), F(-2), F(0)], F(1), F(1)),
                                                   ([F(0)], F(0), F(1))]:
            sums = [sum((a * e for a, e in zip(coefficients, signs)), F(0))
                    for signs in itertools.product((-1, 1), repeat=len(coefficients))]
            inclusive = F(sum(abs(s) >= threshold for s in sums), len(sums))
            self.assertEqual(inclusive, expected)
            if threshold > 0:
                identity = F(sum(s <= -threshold for s in sums) + sum(s >= threshold for s in sums), len(sums))
                self.assertEqual(identity, inclusive)
                self.assertGreater(inclusive, F(sum(abs(s) > threshold for s in sums), len(sums)))


