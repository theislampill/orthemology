"""Synthetic-only verification of the independent controls, not archival results."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from itertools import product
import unittest
from independent_oracles import (GAMMAS, adaptive_tail, closed_enclosure,
    descriptive_oracle, exhaustive_adaptive, exp_negative_enclosure, fixture,
    product_tail_max)


class IndependentControlTests(unittest.TestCase):
    def test_unequal_roster_fixed_weighting(self):
        s = descriptive_oracle(fixture())
        expected = dict(S=Q(1,2), T=Q(1,2), H=Q(3,4), total_abs=Q(3,4), V=Q(1,192),
            Q_plus=Q(5,8), Q_minus=Q(1,8), present=144, absent=0, eligible=120)
        for k,v in expected.items(): self.assertEqual(s[k],v,k)
        self.assertEqual(s['game_weights'], {'game-A':Q(1,2),'game-B':Q(1,2)})
        self.assertEqual(s['S'],s['Q_plus']-s['Q_minus'])

    def test_absence_is_not_midpoint_and_no_renormalization(self):
        r=fixture();r[0]['forecast']=None
        a=descriptive_oracle(r)
        r[0]['forecast']=Q(50)
        m=descriptive_oracle(r)
        self.assertEqual(a['S'],Q(47,96));self.assertEqual(a['S'],m['S'])
        self.assertEqual(a['present'],143);self.assertEqual(m['present'],144)
        self.assertEqual(a['midpoint'],0);self.assertEqual(m['midpoint'],1)
        self.assertEqual(a['H'],Q(3,4));self.assertEqual(a['game_weights'],m['game_weights'])

    def test_zero_support_game_remains_in_denominator(self):
        r=fixture()
        for row in r:
            if row['game']=='game-A':row['global_correct']=row['local_correct']
        s=descriptive_oracle(r)
        self.assertEqual(s['H'],Q(1,2));self.assertEqual(s['S'],Q(1,4))
        self.assertEqual(s['game_weights']['game-A'],Q(1,2))

    def test_sign_encoding_controls(self):
        baseline=descriptive_oracle(fixture())
        r=fixture()
        for row in r:row['local_left']=not row['local_left']
        s=descriptive_oracle(r)
        self.assertEqual(s['S'],-baseline['S']);self.assertEqual(s['T'],baseline['T'])
        for h,lc,gc in product((False,True),repeat=3):
            L=h if lc else not h;J=h if gc else not h
            self.assertEqual(L!=J,lc!=gc)
            for F in map(Q,['0','.1','50','99.9','100']):
                B=(2*int(L)-1)*(F/50-1)
                self.assertEqual(B,(2*int(not L)-1)*((100-F)/50-1))
                if L!=J:
                    for A in [-1,1]:self.assertEqual(A*B,-A*(2*int(J)-1)*(F/50-1))

    def test_tail_separation_and_exact_ties(self):
        self.assertEqual(adaptive_tail([1,1],2,3),Q(3,4))
        self.assertEqual(product_tail_max([1,1],2,3),Q(5,8))
        for direction in [-1,1]:self.assertEqual(product_tail_max([1,1],2,3,direction),Q(9,16))
        self.assertEqual(adaptive_tail([Q(1,3),-Q(2,3)],1,1),Q(1,2))
        self.assertEqual(adaptive_tail([Q(1,3),-Q(2,3)],Q(100000000000000000001,10**20),1),0)
        self.assertEqual(adaptive_tail([0,0],0,10),1)
        self.assertEqual(adaptive_tail([0,0],Q(1,10**100),10),0)

    def test_bellman_exhaustive_and_closed_bound_direction(self):
        arrays=[[1],[0],[1,1],[1,-2,0],[Q(1,3),-Q(2,7),Q(5,9)]]
        self.comparisons=0
        for a in arrays:
            aa=sum(map(abs,a),Q(0));v=sum((x*x for x in a),Q(0))
            for t in [Q(0),Q(1,3),Q(1),Q(2),Q(7)]:
                previous=None
                for gamma in GAMMAS:
                    exact=adaptive_tail(a,t,gamma)
                    self.assertEqual(exact,exhaustive_adaptive(a,t,gamma))
                    lo,hi=closed_enclosure(t,aa,v,gamma)
                    self.assertGreaterEqual(hi,exact)
                    self.assertTrue(0<=lo<=hi<=1)
                    if previous:self.assertGreaterEqual(hi,previous[0])
                    previous=(lo,hi);self.comparisons+=1
        self.assertEqual(self.comparisons,200)

    def test_independent_numeric_evaluations_inside_enclosures(self):
        for x in [Q(0),Q(1,10**50),Q(1,3),Q(1),Q(23,7),Q(100),Q(1000)]:
            lo,hi=exp_negative_enclosure(x)
            with localcontext() as ctx:
                ctx.prec=220
                value=(-(Decimal(x.numerator)/Decimal(x.denominator))).exp()
                self.assertLessEqual(Decimal(lo.numerator)/Decimal(lo.denominator),value)
                self.assertGreaterEqual(Decimal(hi.numerator)/Decimal(hi.denominator),value)
            self.assertGreater(hi,0);self.assertLessEqual(hi-lo,Q(1,10**12))

    def test_dependent_counterexample_requires_drift(self):
        _,hi=exp_negative_enclosure(Q(1))
        self.assertLess(2*hi,Q(3,4))
        lo,hi=closed_enclosure(2,2,2,3)
        self.assertGreaterEqual(hi,Q(3,4));self.assertEqual((lo,hi),(1,1))

    def test_exact_boundary_and_near_boundary(self):
        for eps in [Q(-1,10**30),Q(1,10**30)]:
            x=Q('3.688879454113936302852455697600717343752101757349283484912')+eps
            lo,hi=exp_negative_enclosure(x)
            if eps<0:self.assertGreater(2*lo,Q(1,20))
            else:self.assertLess(2*hi,Q(1,20))


if __name__=='__main__': unittest.main(verbosity=2)
