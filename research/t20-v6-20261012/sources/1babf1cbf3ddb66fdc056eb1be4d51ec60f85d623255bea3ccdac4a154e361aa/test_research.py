"""Exact finite checks for P02 proposals; not a measure-theory proof."""
from fractions import Fraction as F
import importlib.util
import unittest
SPEC = importlib.util.find_spec('p02_research')
if SPEC is not None:
    import p02_research as r

class Availability(unittest.TestCase):
    def test_implementation_exists(self):
        self.assertIsNotNone(SPEC, 'P02 finite research implementation has not yet been written')

@unittest.skipIf(SPEC is None, 'Implementation absent in initial RED run')
class ResearchTests(unittest.TestCase):
    def test_coin_has_no_deterministic_state(self):
        self.assertEqual(r.deterministic_states((((0,0),(0,1)),)), set())
    def test_constant_is_atomic(self):
        self.assertEqual(r.atomic_mass((((0,0),(0,0)),)), [F(1)])
    def test_mixture_mass(self):
        m=(((1,0),(2,1)),((1,0),(1,0)),((2,0),(2,1)))
        self.assertEqual(r.atomic_mass(m),[F(1,2),F(1),F(0)])
    def test_delayed_distinguishing_is_not_determinism(self):
        m=(((1,0),(2,0)),((1,0),(1,0)),((2,1),(2,1)))
        self.assertEqual(r.deterministic_states(m),{1,2})
        self.assertEqual(r.deterministic_states_independent(m),{1,2})
        self.assertEqual(r.atomic_mass(m),[F(1),F(1),F(1)])
    def test_rational_hitting_one_third(self):
        m=(((1,0),(2,1)),((3,0),(0,1)),((2,0),(2,1)),((3,0),(3,0)))
        self.assertEqual(r.atomic_mass(m),[F(1,3),F(2,3),F(0),F(1)])
    def test_invalid_machines_refused(self):
        for m in [(), (((1,0),(0,0)),), (((0,0),),), (((0,2),(0,0)),), (((True,0),(0,0)),)]:
            with self.subTest(m=m),self.assertRaises((ValueError,TypeError)):r.atomic_mass(m)
    def test_parity_support_and_proper_marginals(self):
        for n in range(3,7):
            e,o=r.parity_law(n,0),r.parity_law(n,1)
            self.assertEqual(sum(e.values()),F(1));self.assertEqual(len(e),2**(n-1))
            for mask in range((1<<n)-1):
                j=tuple(i for i in range(n) if mask>>i&1)
                self.assertEqual(r.marginal(e,j),r.marginal(o,j))
    def test_mixture_pair_profile(self):
        for n in range(3,7):
            e=r.parity_law(n,0);mix=r.mixture(e,{(0,)*n:F(1)},F(1,2))
            self.assertTrue(all(sum(x)%2==0 for x in mix))
            self.assertEqual(r.marginal(mix,(0,1)),{(0,0):F(5,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(1,8)})
    def test_full_marginal_is_not_blind(self):
        self.assertNotEqual(r.marginal(r.parity_law(3,0),(0,1,2)),r.marginal(r.parity_law(3,1),(0,1,2)))
    def test_selector_exact_brackets(self):
        for q in [F(0),F(1),F(1,3),F(2,5),F(7,13)]:
            for n in range(12):
                low,high,undecided=r.selector_bracket(q,n)
                self.assertLessEqual(low,q);self.assertLessEqual(q,high)
                self.assertEqual(high-low,undecided)
                self.assertLessEqual(undecided,F(1,2**n))
    def test_selector_invalid_refused(self):
        for q in [F(-1),F(2),0.5]:
            with self.subTest(q=q),self.assertRaises((ValueError,TypeError)):r.selector_bracket(q,3)
    def test_soft_mass_coin_and_constant(self):
        for k in range(1,8):
            vals=[r.soft_mass({i:F(1,2**n) for i in range(2**n)},k) for n in range(9)]
            self.assertEqual(vals[-1],F(0))
            self.assertTrue(all(a>=b for a,b in zip(vals,vals[1:])))
            self.assertEqual(r.soft_mass({0:F(1)},k),1-F(1,2**k))
    def test_finite_refinement_cannot_charge_extinction(self):
        delta,j=F(1,3),F(5,12)
        self.assertLessEqual(delta,F(1,2))
        self.assertGreater(delta+j,F(1,2))
        self.assertEqual(delta+j,F(3,4))

if __name__=='__main__':unittest.main(verbosity=2)
