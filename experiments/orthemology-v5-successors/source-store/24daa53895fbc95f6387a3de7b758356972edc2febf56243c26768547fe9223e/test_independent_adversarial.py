"""Independent controls for the written-only one-variable reference.

These tests supplement the proof review; passing them is not kernel refinement.
"""
import copy
import unittest
import root_extension_checker as q


def c(n): return ['c', n]
x = ['v', 0]
def add(a, b): return ['add', a, b]
def mul(a, b): return ['mul', a, b]
def old(a): return ['old', a]
def test(a, b): return ['test', a, b]
def if0(a, b, d): return ['if0', a, b, d]


class IndependentAdversarialControls(unittest.TestCase):
    def test_symbolic_cancellation_to_zero(self):
        a, b = mul(x, add(x, c(1))), add(mul(x, x), x)
        self.assertEqual(q.tail(test(a, b)), (1, {0: 1}))
        self.assertIsNone(q.distinguish(test(a, b), old(c(1))))
        self.assertEqual(q.comparison_bound(test(a, b), old(c(1))), 1)

    def test_vanished_leading_coefficients_and_constant_difference(self):
        s = test(add(mul(x, x), c(3)), add(mul(x, x), c(4)))
        self.assertEqual(q.tail(s), (1, {}))
        self.assertIsNone(q.distinguish(s, old(c(0))))
        self.assertEqual(q.root_bound({100: 0, 1: -1, 0: 3}), 4)
        self.assertEqual(q.root_bound({100: 0, 0: -7}), 1)

    def test_nested_old_zero_conditionals_keep_zero_separate(self):
        s = old(if0(if0(x, c(0), x), c(7), add(x, c(1))))
        t = old(if0(x, c(7), add(x, c(1))))
        self.assertEqual(q.tail(s), (1, {0: 1, 1: 1}))
        self.assertTrue(q.equivalent(s, t))
        self.assertEqual(q.distinguish(s, old(add(x, c(1)))), 0)
        # On the positive mask the inner test becomes zero, even though
        # at zero the outer expression selects a different branch.
        u = old(if0(if0(x, c(1), c(0)), mul(x, x), c(8)))
        self.assertEqual(q.tail(u), (1, {2: 1}))
        self.assertEqual(q.evaluate(u, 0), 8)
        self.assertEqual(q.distinguish(u, old(mul(x, x))), 0)

    def test_late_repeated_root_and_inclusive_bound(self):
        # (x-97)^2 = 0, represented without subtraction in either comparand.
        s = test(add(mul(x, x), c(9409)), mul(c(194), x))
        self.assertEqual(q.tail(s), (9604, {}))
        self.assertEqual(q.comparison_bound(s, old(c(0))), 9604)
        self.assertEqual(q.distinguish(s, old(c(0))), 97)
        self.assertEqual([q.evaluate(s, n) for n in [96, 97, 98, 9604]], [0, 1, 0, 0])

    def test_different_tail_bound_is_an_actual_witness(self):
        pairs = [(old(c(0)), old(c(1))), (old(x), test(x, x)),
                 (test(x, x), old(add(x, c(1)))),
                 (old(mul(x, x)), old(add(mul(x, x), c(1))))]
        for s, t in pairs:
            n = q.comparison_bound(s, t)
            self.assertEqual(q.distinguish(s, t), n)
            self.assertNotEqual(q.evaluate(s, n), q.evaluate(t, n))

    def test_deep_purity_and_invalid_interfaces(self):
        bad = [test(add(x, mul(c(0), if0(x, c(0), c(1)))), x),
               test(add(x, test(x, x)), x), ['old', x, c(0)],
               ['test', x], ('old', x), ['old', ['v', True]],
               ['old', ['v', -1]], ['old', ['c', 1.0]],
               ['old', ['add', x]], []]
        for s in bad:
            for action in [lambda: q.validate(s), lambda: q.tail(s),
                           lambda: q.evaluate(s, 0),
                           lambda: q.comparison_bound(s, old(c(0))),
                           lambda: q.distinguish(s, old(c(0))),
                           lambda: q.equivalent(s, old(c(0)))]:
                with self.assertRaises(ValueError): action()
        for p in [{True: 1}, {0: True}, {-1: 1}, {0.5: 2}, {0: 1.0}, [], None]:
            with self.assertRaises(ValueError): q.root_bound(p)

    def test_arithmetic_maps_and_source_inputs_are_not_mutated(self):
        p = {0: -2, 2: 0, 7: 3}
        before = p.copy()
        self.assertEqual(q.root_bound(p), 3)
        self.assertEqual(p, before)
        s = old(if0(x, c(17), add(x, c(4))))
        before = copy.deepcopy(s)
        q.tail(s); q.evaluate(s, 0); q.distinguish(s, old(c(0)))
        self.assertEqual(s, before)


if __name__ == '__main__': unittest.main()
