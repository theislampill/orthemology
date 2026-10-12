"""Focused regression tests, authored before the implementation module."""
import unittest
from modal_support import (minimal_supports, blockers, supported, absence_complex,
    skeleton_bounds, audit, union_closed, necessary_active)

class ModalSupportTests(unittest.TestCase):
    def test_conjunctive_dependency_is_not_two_alternatives(self):
        # a AND b -> q
        supp = minimal_supports(3, (0, 1), [(0b011, 2)])
        self.assertEqual(supp[2], (0b011,))
        self.assertFalse(supported(supp[2], 0b001))
        self.assertTrue(supported(supp[2], 0b011))

    def test_cycles_without_seed_do_not_produce(self):
        supp = minimal_supports(2, (), [(0b01, 1), (0b10, 0)])
        self.assertEqual(supp, ((), ()))

    def test_dual_of_alternatives_is_joint_cut(self):
        self.assertEqual(blockers((1, 2, 4), 3), (7,))

    def test_necessity_not_individual_necessity(self):
        active = (1, 2, 4)
        self.assertTrue(all(supported((1, 2, 4), a) for a in active))
        self.assertEqual(active[0] & active[1] & active[2], 0)
        self.assertFalse(union_closed(absence_complex(active, 3)))

    def test_skeleton_bounds_give_exact_ambiguity(self):
        known = frozenset(range(7))  # every proper subset of 3 indices
        lo, hi = skeleton_bounds(known, 3, 2)
        self.assertEqual(lo, known)
        self.assertEqual(hi, frozenset(range(8)))
        self.assertEqual(audit((1, 2, 4), known, 3, 2), 'UNDETERMINED')

    def test_contingent_root_is_not_made_necessary_by_no_parent(self):
        self.assertEqual(necessary_active((1, 2), 2), 0)
        self.assertEqual(necessary_active((1, 3), 2), 1)

    def test_empty_possible_world_family_is_rejected(self):
        with self.assertRaises(ValueError):
            absence_complex((), 2)

if __name__ == '__main__':
    unittest.main()
