"""Finite probes for CV-C and CV-O; never substitutes for their infinite proofs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from convergence import Mealy, soft_mass
import operational as op
import observations as obs
from boundaries import Rejection

class ConvergenceTests(unittest.TestCase):
    def test_constant_stream(self):
        m=Mealy((((0,0),(0,0)),))
        self.assertEqual(m.deterministic_states(),frozenset({0}))
        self.assertEqual(m.defect(),F(0))
    def test_fair_stream(self):
        m=Mealy((((0,0),(0,1)),))
        self.assertEqual(m.deterministic_states(),frozenset())
        self.assertEqual(m.defect(),F(1))
    def test_mixed_atomic_diffuse(self):
        m=Mealy((((1,0),(2,1)),((1,0),(1,0)),((2,0),(2,1))))
        self.assertEqual(m.deterministic_states(),frozenset({1}))
        self.assertEqual(m.defect(),F(1,2))
    def test_countably_atomic_not_just_finite_support(self):
        m=Mealy((((0,0),(1,1)),((1,1),(1,1))))
        self.assertEqual(m.deterministic_states(),frozenset({1}))
        self.assertEqual(m.defect(),F(0))
    def test_all_two_state_descriptions(self):
        n=0
        for entries in product(product(range(2),range(2)),repeat=4):
            m=Mealy((entries[:2],entries[2:]))
            # Independent finite distinguishing-word criterion. A failed pair
            # has a witness by the fourth relation-removal round for two states.
            direct=frozenset(s for s in range(2) if len({m.output(w,s) for w in product((0,1),repeat=4)})==1)
            self.assertEqual(m.deterministic_states(),direct)
            ds=[m.defect(s) for s in range(2)]
            for s in range(2):
                self.assertTrue(F(0)<=ds[s]<=F(1))
                if s in direct:self.assertEqual(ds[s],0)
                else:self.assertEqual(ds[s],sum((ds[t] for t,_ in m.rows[s]),F())/2)
            n+=1
        self.assertEqual(n,256)
    def test_invalid_machine_rejected(self):
        with self.assertRaises(ValueError):Mealy(())
        with self.assertRaises(ValueError):Mealy((((4,0),(0,1)),))
        with self.assertRaises(ValueError):Mealy((((0,2),(0,1)),))
    def test_soft_mass_counterexample_to_wrong_limit_order(self):
        # At any fixed depth, k→∞ gives 1 even for fair continuous stream;
        # at any fixed k, n sufficiently large gives zero. Order is essential.
        for n in range(1,7):
            masses=[F(1,2**n)]*(2**n)
            self.assertEqual(soft_mass(masses,n),0)
            self.assertEqual(soft_mass(masses,n+3),F(7,8))
        self.assertEqual(soft_mass([F(1)],4),F(15,16))
    def test_refinement_tower_and_direct_composition(self):
        def model(v):return {'space':'tagged-uniform-intervals','law':'v5-tower','weights':[[1,3],[2,3]],'view':v,'events':'full-measurable'}
        chain=[model([0,0]),model([2,3]),model([-1,6]),model([-1,-1])]
        steps=[F(*obs.refinement(a,b)['increment']) for a,b in zip(chain,chain[1:])]
        self.assertEqual(steps,[F(0),F(1,3),F(2,3)])
        self.assertEqual(sum(steps),F(*obs.refinement(chain[0],chain[-1])['increment']))
    def test_exact_licence_transport_finite_traces(self):
        actions=list(product(('primitive:succ','primitive:not'),(False,True)))
        count=0
        for n in range(6):
            for trace in product(actions,repeat=n):
                e=op.Engine.standard();lic=e.admit({'op':'primitive','name':'succ'})
                touched=False
                for key,value in trace:
                    e.revise_rule(key,value)
                    touched |= key=='primitive:succ'
                if touched:
                    with self.assertRaises(Rejection):e.dispatch(lic,2)
                else:self.assertEqual(e.dispatch(lic,2),3)
                count+=1
        self.assertEqual(count,1365)

if __name__=='__main__':unittest.main(verbosity=2)
