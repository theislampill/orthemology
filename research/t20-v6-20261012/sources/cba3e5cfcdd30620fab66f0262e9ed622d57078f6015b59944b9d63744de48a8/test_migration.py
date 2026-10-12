from fractions import Fraction as F
import unittest
from migration import coupling, verify_probabilistic_migration, verify_rank_migration


class MigrationTests(unittest.TestCase):
    def test_many_to_one_coupling_preserves_mass(self):
        result = coupling({'b': F(1, 2), 'g1': F(1, 4), 'g2': F(1, 4)},
                          {'qb': F(1, 2), 'qg': F(1, 2)},
                          {('b', 'qb'), ('g1', 'qg'), ('g2', 'qg')})
        self.assertIsNotNone(result)
        self.assertEqual(result['g1', 'qg'], F(1, 4))

    def test_support_match_does_not_imply_probability_match(self):
        result = coupling({'b': F(1, 2), 'g': F(1, 2)}, {'qb': F(1)}, {('b', 'qb')})
        self.assertIsNone(result)

    def test_geometric_many_to_one_migration(self):
        src = {'b': {'b': F(1, 2), 'g1': F(1, 4), 'g2': F(1, 4)},
               'g1': {'g1': F(1)}, 'g2': {'g2': F(1)}}
        dst = {'qb': {'qb': F(1, 2), 'qg': F(1, 2)}, 'qg': {'qg': F(1)}}
        relation = {('b', 'qb'), ('g1', 'qg'), ('g2', 'qg')}
        result = verify_probabilistic_migration(src, dst, {'b'}, {'qb'}, relation,
                                              {('b', 'qb')}, set(dst))
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['couplings']), 3)

    def test_bad_label_reflection_is_required(self):
        result = verify_probabilistic_migration({'g': {'g': F(1)}}, {'qb': {'qb': F(1)}},
                     set(), {'qb'}, {('g', 'qb')}, {('g', 'qb')}, {'qb'})
        self.assertFalse(result['valid'])
        self.assertIn(('bad_reflection', 'g', 'qb'), result['violations'])

    def test_sure_rank_migration_uses_witness_minimum_with_bad_reflection(self):
        src = {'p': {'t'}, 't': {'t'}}
        dst = {'q': {'q'}}
        # q is target; p (rank 1) or t (rank 0) is a proof witness.
        result = verify_rank_migration(src, dst, {'p'}, set(), {'p': 1, 't': 0},
                   {('p', 'q'), ('t', 'q')}, {('p', 'q')}, {'q'})
        self.assertTrue(result['valid'])
        self.assertEqual(result['destination_rank'], {'q': 0})

    def test_missing_destination_license_is_detected(self):
        result = verify_rank_migration({'t': {'t'}}, {'q': {'q'}}, set(), set(), {'t': 0},
                   {('t', 'q')}, {('t', 'q')}, set())
        self.assertFalse(result['valid'])
        self.assertIn(('destination_license', 'q'), result['violations'])


if __name__ == '__main__':
    unittest.main()
