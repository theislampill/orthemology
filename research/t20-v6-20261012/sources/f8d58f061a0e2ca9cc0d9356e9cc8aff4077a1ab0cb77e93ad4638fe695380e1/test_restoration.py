"""Synthetic model tests. They do not assert any actual-world model adequacy."""
import unittest
from restoration import Game, bounded_sure, verify_controller, Controller, classify_chain, classify_mdp
from fractions import Fraction as F


def blind_game(edges, bad, initial=None):
    n = len(edges)
    actions = tuple(sorted(edges[0]))
    return Game(
        states=tuple(range(n)), public=(0,), actions=actions,
        initial=tuple(range(n)) if initial is None else tuple(initial), initial_public=0,
        transitions={(0, x, a): tuple((y, 'o') for y in edges[x][a])
                     for x in range(n) for a in actions},
        public_update={(0, a, 'o'): 0 for a in actions},
        safe={(0, x) for x in range(n)},
        target={(0, x) for x in range(n) if x not in bad})


class RestorationTests(unittest.TestCase):
    def test_delayed_single_bad_visit_is_sure_winning(self):
        # Changes that label a belief bad whenever one member is bad must fail this.
        g = blind_game({0: {'a': (0,)}, 1: {'a': (0,)},
                        2: {'a': (0, 1, 2)}}, {1}, initial=(2,))
        self.assertFalse(bounded_sure(g, 0).winning)
        result = bounded_sure(g, 1)
        self.assertTrue(result.winning)
        self.assertTrue(verify_controller(g, result.controller)['sure'])

    def test_alternation_requires_memory_beyond_constant_belief(self):
        # A belief-only action selector cannot alternate because its support stays fixed.
        g = blind_game({0: {'a': (2,), 'b': (2,)},
                        1: {'a': (1,), 'b': (2,)},
                        2: {'a': (0,), 'b': (0, 1)}}, {1})
        self.assertFalse(bounded_sure(g, 1).winning)
        result = bounded_sure(g, 2)
        self.assertTrue(result.winning)
        self.assertTrue(verify_controller(g, result.controller)['sure'])

    def test_unauthorized_discriminator_remains_unavailable(self):
        g = blind_game({0: {'repair': (1,), 'hold': (0,)},
                        1: {'repair': (1,), 'hold': (1,)}}, {0}, initial=(0,))
        g.warrant = lambda c, b, a: a != 'repair'
        self.assertFalse(bounded_sure(g, 3).winning)
        g.warrant = None
        self.assertTrue(bounded_sure(g, 1).winning)

    def test_unsafe_outcome_is_not_silently_discarded(self):
        g = blind_game({0: {'a': (1, 2)}, 1: {'a': (1,)},
                        2: {'a': (2,)}}, {0, 2}, initial=(0,))
        g.safe.remove((0, 2))
        self.assertFalse(bounded_sure(g, 2).winning)

    def test_dead_end_is_not_vacuously_winning(self):
        g = blind_game({0: {'a': ()}}, set(), initial=(0,))
        self.assertFalse(bounded_sure(g, 0).winning)

    def test_public_permission_expiry_is_observed(self):
        g = Game(states=(0, 1), public=('valid', 'expired'), actions=('repair',),
                 initial=(0,), initial_public='valid',
                 transitions={(c, x, 'repair'): ((1, 'tick'),)
                              for c in ('valid', 'expired') for x in (0, 1)},
                 public_update={(c, 'repair', 'tick'): 'expired'
                                for c in ('valid', 'expired')},
                 safe={(c, x) for c in ('valid', 'expired') for x in (0, 1)},
                 target={(c, 1) for c in ('valid', 'expired')},
                 eligibility={('valid', x, 'repair') for x in (0, 1)})
        self.assertFalse(bounded_sure(g, 1).winning)

    def test_geometric_repair_is_almost_sure_but_not_sure(self):
        r = classify_chain({'b': {'b': F(1, 2), 'g': F(1, 2)},
                            'g': {'g': F(1)}}, {'b'}, {'b'})
        self.assertTrue(r['almost_sure'])
        self.assertFalse(r['sure'])

    def test_recurrent_bad_chain_loses_almost_sure(self):
        r = classify_chain({'b': {'g': F(1)}, 'g': {'b': F(1)}}, {'b'}, {'b'})
        self.assertFalse(r['almost_sure'])
        self.assertFalse(r['sure'])

    def test_bad_mdp_end_component_need_not_be_bottom_union_scc(self):
        # Union support reaches g, but adversary can choose the stay kernel.
        r = classify_mdp({'b': ({'b': F(1)}, {'g': F(1)}),
                          'g': ({'g': F(1)},)}, {'b'}, {'b'})
        self.assertFalse(r['almost_sure_all_adversaries'])
        self.assertIn(frozenset({'b'}), r['bad_maximal_end_components'])

    def test_unavoidable_geometric_progress_survives_finite_kernel_choice(self):
        r = classify_mdp({'b': ({'b': F(1, 2), 'g': F(1, 2)},
                                {'b': F(2, 3), 'g': F(1, 3)}),
                          'g': ({'g': F(1)},)}, {'b'}, {'b'})
        self.assertTrue(r['almost_sure_all_adversaries'])


if __name__ == '__main__':
    unittest.main()
