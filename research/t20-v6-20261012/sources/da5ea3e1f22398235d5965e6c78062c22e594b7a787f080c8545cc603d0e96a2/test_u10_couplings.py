#!/usr/bin/env python3
"""New independent, exact-rational finite tests of U10's stated quantifier boundary.
Not recovered source, not a general Hall theorem proof or Lean kernel result.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,unittest

def two_point_coupling(p,q,edges):
    lo,hi=max(F(0),p+q-1),min(p,q)
    forced=[]
    for edge,value in (((0,0),F(0)),((0,1),p),((1,0),q),((1,1),p+q-1)):
        if edge not in edges:forced.append(value)
    a=forced[0] if forced else lo
    if any(x!=a for x in forced) or not lo<=a<=hi:return None
    k={(0,0):a,(0,1):p-a,(1,0):q-a,(1,1):1-p-q+a}
    if not all(v>=0 and (v==0 or e in edges) for e,v in k.items()):raise AssertionError('invalid support')
    if (sum(k[(0,j)] for j in range(2)),sum(k[(1,j)] for j in range(2)))!=(p,1-p):raise AssertionError('invalid rows')
    if (sum(k[(i,0)] for i in range(2)),sum(k[(i,1)] for i in range(2)))!=(q,1-q):raise AssertionError('invalid columns')
    return k

def hall(p,q,edges):
    mu=(p,1-p);nu=(q,1-q)
    for bits in product((False,True),repeat=2):
        s={i for i in range(2) if bits[i]}
        nbr={j for i,j in edges if i in s}
        if sum(mu[i] for i in s)>sum(nu[j] for j in nbr):return False
    return True

EDGES=list(product(range(2),repeat=2))
RELATIONS=[{e for e,b in zip(EDGES,bits) if b} for bits in product((False,True),repeat=4)]

class U10FiniteMeaning(unittest.TestCase):
    def test_hall_iff_exact_coupling_all_two_point_tenths(self):
        for i,j in product(range(11),repeat=2):
            for r in RELATIONS:
                p,q=F(i,10),F(j,10)
                self.assertEqual(two_point_coupling(p,q,r) is not None,hall(p,q,r),(p,q,r))
    def test_relation_by_relation_witnesses_do_not_give_common_witness(self):
        eq={(0,0),(1,1)};flip={(0,1),(1,0)};p=F(1,2)
        self.assertIsNotNone(two_point_coupling(p,p,eq))
        self.assertIsNotNone(two_point_coupling(p,p,flip))
        self.assertIsNone(two_point_coupling(p,p,eq&flip))
    def test_common_support_exactly_intersection(self):
        for i,j in product(range(11),repeat=2):
            for r,s in product(RELATIONS,repeat=2):
                p,q=F(i,10),F(j,10)
                k=two_point_coupling(p,q,r&s)
                self.assertEqual(k is not None,hall(p,q,r&s))
                if k is not None:self.assertTrue(all(v==0 or (e in r and e in s) for e,v in k.items()))
    def test_unequal_weights_refused_by_equality_support(self):
        self.assertIsNone(two_point_coupling(F(1,3),F(2,3),{(0,0),(1,1)}))
    def test_zero_weight_branch_need_not_have_supported_edge(self):
        self.assertIsNotNone(two_point_coupling(F(1),F(1),{(0,0)}))

if __name__=='__main__':unittest.main(verbosity=2)
