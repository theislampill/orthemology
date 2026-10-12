from fractions import Fraction as F
import unittest
from correlation import maximize_relation_mass, fixed_marginal_law_2x2

class CorrelationTests(unittest.TestCase):
    def test_marginal_mismatch_forces_exact_disagreement_mass(self):
        r=maximize_relation_mass({0:F(4,5),1:F(1,5)}, {0:F(1,5),1:F(4,5)}, {(0,0),(1,1)})
        self.assertEqual(r['minimum_violation'],F(3,5))
        self.assertEqual(sum(v for (x,y),v in r['coupling'].items() if x!=y),F(3,5))

    def test_matching_pennies_incentives_block_target_supported_coupling(self):
        u=((1,0),(0,1)); v=((0,1),(1,0))
        r=fixed_marginal_law_2x2(F(1,2),F(1,2),{(0,0),(1,1)},ce_games=((u,v),))
        self.assertTrue(r['feasible'])
        self.assertEqual(r['minimum_violation'],F(1,2))
        blocked=fixed_marginal_law_2x2(F(1,2),F(1,2),{(0,0),(1,1)},
                  allowed={(0,0),(1,1)},ce_games=((u,v),))
        self.assertFalse(blocked['feasible'])

    def test_coordination_correlation_is_incentive_compatible(self):
        u=((1,0),(0,1))
        r=fixed_marginal_law_2x2(F(1,2),F(1,2),{(0,0),(1,1)},ce_games=((u,u),))
        self.assertTrue(r['feasible'])
        self.assertEqual(r['minimum_violation'],0)

    def test_hard_action_constraints_can_prevent_hall_deficit_attainment(self):
        mu={0:F(1,2),1:F(1,2)}; relation={(0,0)}
        self.assertEqual(maximize_relation_mass(mu,mu,relation)['minimum_violation'],F(1,2))
        r=fixed_marginal_law_2x2(F(1,2),F(1,2),relation,allowed={(0,0),(0,1),(1,0)})
        self.assertTrue(r['feasible'])
        self.assertEqual(r['minimum_violation'],1)

if __name__=='__main__':unittest.main()
