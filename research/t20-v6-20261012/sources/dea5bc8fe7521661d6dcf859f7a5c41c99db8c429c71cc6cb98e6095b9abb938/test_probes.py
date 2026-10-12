"""New, isolated P01 research-probe tests; not the canonical engine suite."""
import unittest
from fractions import Fraction as F
import probes as p

class ProbeTests(unittest.TestCase):
    def test_i_k_s_roots(self):
        x,y,z=p.V(0),p.V(1),p.V(2)
        self.assertIn(x,p.steps(p.A(p.I,x)))
        self.assertIn(x,p.steps(p.A(p.K,x,y)))
        self.assertIn(p.A(x,z,p.A(y,z)),p.steps(p.A(p.S,x,y,z)))
    def test_context_steps(self):
        t=p.A(p.V(2),p.A(p.I,p.V(0)))
        self.assertIn(p.A(p.V(2),p.V(0)),p.steps(t))
    def test_nonempty_simulation(self):
        for t in (p.A(p.I,p.V(0)),p.A(p.K,p.V(0),p.V(1)),p.A(p.S,p.V(0),p.V(1),p.V(2))):
            for w in p.step_edges(t):
                path=p.simulate(t,w)
                self.assertGreater(len(path),1)
                self.assertEqual(path[0],p.translate(t))
                self.assertEqual(path[-1],p.translate(w.target))
                self.assertTrue(all(b in p.lsteps(a) for a,b in zip(path,path[1:])))
    def test_term_substitution_square(self):
        t=p.A(p.S,p.V(0),p.A(p.I,p.V(1)))
        s={0:p.A(p.I,p.V(2)),1:p.K}
        self.assertEqual(p.translate(p.subst(t,s)),p.lfree_subst(p.translate(t),{k:p.translate(v) for k,v in s.items()}))
    def test_type_binder_capture_guard(self):
        t=('all',('t',1)); s=lambda _:('t',0)
        self.assertEqual(p.tsubst(t,s),('all',('t',1)))
        self.assertNotEqual(p.tsubst(t,s),('all',('t',0)))
        self.assertEqual(p.tsubst(('bot',),s),('bot',))
    def test_parallel_triangle(self):
        t=p.A(p.S,p.A(p.I,p.V(0)),p.K,p.A(p.I,p.V(1)))
        for u in p.parallel(t): self.assertIn(p.develop(t),p.parallel(u))
    def test_omega_shape_and_cycle(self):
        o,o1,o2=p.omega_cycle()
        self.assertIn(o1,p.steps(o));self.assertIn(o2,p.steps(o1));self.assertIn(o,p.steps(o2))
        for t in (o,o1,o2):self.assertIsNotNone(p.omega_shape(t))
    def test_discarded_omega_is_convertible_to_i(self):
        t=p.A(p.K,p.I,p.omega_cycle()[0])
        self.assertIn(p.I,p.steps(t))
        self.assertGreater(len(p.steps(t)),1)
    def test_intensional_identity_extension_obstruction(self):
        e=p.A(p.S,p.K,p.K)
        self.assertFalse(p.steps(e));self.assertFalse(p.steps(p.I));self.assertNotEqual(e,p.I)
        x=p.V(0);s1=p.A(p.K,x,p.A(p.K,x))
        self.assertIn(s1,p.steps(p.A(e,x)));self.assertIn(x,p.steps(s1))
    def test_bracket_beta_and_failure_of_xi(self):
        body=p.A(p.I,p.V(0));b=p.abstract(0,body)
        self.assertEqual(b,p.A(p.S,p.A(p.K,p.I),p.I))
        self.assertFalse(p.steps(b));self.assertNotEqual(b,p.abstract(0,p.V(0)))
        path=p.abstraction_path(0,body,p.K)
        self.assertEqual(path[-1],p.subst(body,{0:p.K}))
        self.assertTrue(all(b in p.steps(a) for a,b in zip(path,path[1:])))
    def test_eta_shortcut_still_fails_xi(self):
        body=p.A(p.K,p.V(0),p.I)
        self.assertIn(p.V(0),p.steps(body))
        left=p.abstract_eta(0,body);right=p.abstract_eta(0,p.V(0))
        self.assertEqual(left,p.A(p.S,p.K,p.A(p.K,p.I)))
        self.assertFalse(p.steps(left));self.assertFalse(p.steps(right))
        self.assertNotEqual(left,right)
    def test_bracket_naturality_for_fresh_substitutions(self):
        body=p.A(p.V(1),p.V(0),p.V(2))
        s={1:p.A(p.I,p.K),2:p.A(p.S,p.K,p.K)}
        self.assertEqual(p.subst(p.abstract(0,body),s),p.abstract(0,p.subst(body,s)))
    def test_finite_distribution(self):
        e=('mix',F(1,3),('pure',p.I),('pure',p.K))
        self.assertEqual(p.mass(e),{p.I:F(1,3),p.K:F(2,3)})
        self.assertEqual(sum(p.mass(('eapp',e,e)).values()),F(1))
    def test_coupling_quantifier_counterexample(self):
        eq={(0,0),(1,1)};flip={(0,1),(1,0)}
        self.assertTrue(p.fair_couplings(eq));self.assertTrue(p.fair_couplings(flip))
        self.assertFalse(p.fair_couplings(eq&flip))
    def test_diagonal_coupling_exact_marginals(self):
        m={p.I:F(1,3),p.K:F(2,3)};c=p.diagonal_coupling(m)
        self.assertEqual(p.marginals(c),(m,m))
    def test_incoherent_j_motive(self):
        proof=p.A(p.I,p.I)
        self.assertIn(p.I,p.steps(proof))
        motive=lambda q:q==p.I
        self.assertTrue(motive(p.I));self.assertFalse(motive(proof))

if __name__=='__main__':unittest.main(verbosity=2)
