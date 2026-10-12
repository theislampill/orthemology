import unittest
from itertools import product
from choice_semantics import ability, rectangle, powerset, inherited_output, inherited_run, exact_guaranteeing_commands


class ChoiceSemanticsTests(unittest.TestCase):
    def test_nonempty_catalogue_is_really_enumerated(self):
        self.assertEqual(set(powerset(('e0', 'e1'))),
                         {frozenset(), frozenset(('e0',)), frozenset(('e1',)), frozenset(('e0','e1'))})

    def test_quantifier_order_is_not_collapsed(self):
        xor = lambda a, b: a ^ b
        r = ability(xor, (0, 1), (0, 1), 0)
        self.assertTrue(r['reactive'])
        self.assertFalse(r['uniform'])
        self.assertTrue(r['joint'])

    def test_absent_admissibility_never_creates_vacuous_control(self):
        r = ability(lambda a, b: a, (0, 1), (0, 1), 1, frozenset({(0, 0)}))
        self.assertFalse(r['uniform'])
        self.assertFalse(r['joint'])

    def test_diagonal_is_not_independent_choice(self):
        diagonal = frozenset({(0, 0), (1, 1)})
        self.assertFalse(rectangle(diagonal))
        for i in (0, 1):
            for q in (0, 1):
                self.assertTrue(ability(lambda a, b: a, (0, 1), (0, 1), q,
                                        diagonal, i)['uniform'])

    def test_singleton_harmony_is_settled_but_not_unrestricted(self):
        d = frozenset({(1, 1)})
        self.assertTrue(rectangle(d))
        for i in (0, 1):
            self.assertTrue(ability(lambda a, b: a | b, (0, 1), (0, 1), 1, d, i)['uniform'])
            self.assertFalse(ability(lambda a, b: a | b, (0, 1), (0, 1), 0, d, i)['uniform'])

    def test_same_target_can_be_uniformly_ensured_by_both(self):
        for i in (0, 1):
            self.assertTrue(ability(lambda a, b: a | b, (0, 1), (0, 1), 1, agent=i)['uniform'])
            self.assertFalse(ability(lambda a, b: a | b, (0, 1), (0, 1), 0, agent=i)['uniform'])

    def test_familiar_product_incompatibility_all_binary_tables(self):
        for entries in product((0, 1), repeat=4):
            f = lambda a, b: entries[2*a+b]
            a0 = ability(f, (0, 1), (0, 1), 0)['uniform']
            b1 = ability(f, (0, 1), (0, 1), 1, agent=1)['uniform']
            self.assertFalse(a0 and b1)

    def test_inherited_maximal_peer_domain_and_command_formula(self):
        commands = powerset(('e0', 'e1'))
        self.assertEqual(len(commands), 4)
        # Test all 15 nonempty peer domains and 4 targets, not just one conflict.
        for q in commands:
            for k in powerset(commands):
                if not k:
                    continue
                actual = exact_guaranteeing_commands(commands, k, q)
                common = set.intersection(*(set(t) for t in k))
                expected = tuple(s for s in commands
                                 if all(t <= q for t in k) and q - common <= s <= q)
                self.assertEqual(actual, expected)
                self.assertEqual(q in actual, all(t <= q for t in k))

    def test_inherited_solo_capacity_is_not_uniform_sovereignty(self):
        commands = powerset(('e0', 'e1'))
        empty = frozenset()
        for q in commands:
            self.assertEqual(inherited_output(q, empty), q)
            self.assertEqual(inherited_output(empty, q), q)
            for i in (0, 1):
                r = ability(inherited_output, commands, commands, q, agent=i)
                self.assertEqual(r['uniform'], q == frozenset(('e0', 'e1')))

    def test_failure_does_not_require_empty_target_or_idle_peer(self):
        commands = tuple(q for q in powerset(('e0', 'e1')) if q)
        for q in (frozenset(('e0',)), frozenset(('e1',))):
            for i in (0, 1):
                self.assertFalse(ability(inherited_output, commands, commands, q, agent=i)['uniform'])

    def test_universal_enforcement_need_not_make_every_own_move_determining(self):
        table = ((0, 0), (0, 1), (1, 1))
        f = lambda a, b: table[a][b]
        self.assertTrue(all(ability(f, (0, 1, 2), (0, 1), q)['uniform'] for q in (0, 1)))
        self.assertNotEqual(f(1, 0), f(1, 1))

    def test_robust_exact_output_does_not_supply_exclusive_original_provenance(self):
        q = frozenset(('e0',))
        commands = powerset(q)
        self.assertEqual(len(commands), 2)
        for i in (0, 1):
            self.assertTrue(ability(inherited_output, commands, commands, q, agent=i)['uniform'])
        result = inherited_run(q, q)
        self.assertEqual(result['output'], q)
        self.assertEqual(result['support'], {'e0': frozenset(('A','B'))})
        self.assertEqual(result['entire'], {'e0': frozenset()})
        # Presence/power is held; B's coactive Q is one legal exercise. This
        # source-indexed target fails without any opposed output intention.
        for s in commands:
            result = inherited_run(s, q)
            self.assertNotEqual(result['entire']['e0'], frozenset(('A',)))


if __name__ == '__main__':
    unittest.main()
