#!/usr/bin/env python3
"""Finite exact-rational regression checks; not a replacement for the proofs."""
from fractions import Fraction as F
from itertools import combinations
from math import comb, gcd, prod
from functools import reduce
import json

checks = {}

def ceil(x):
    return -((-x.numerator)//x.denominator)

def target(support):
    pos = tuple(j for j in support if j)
    g = reduce(gcd, pos) if pos else 1
    return (tuple(j//g for j in pos), 0 in support)

def hausdorff(a, b):
    return max(max(min(abs(x-y) for y in b) for x in a),
               max(min(abs(x-y) for x in a) for y in b))

def mul(a,b):
    ans = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): ans[i+j] += x*y
    return ans

def moment(support, weights, t, r):
    return sum(w*t**(r*j) for j,w in zip(support,weights))

# Floor/gap endpoint controls; both extrema are included.
for M in range(3,129):
    for t in (1-F(3,2*M), 1-F(1,2*M)):
        q = tuple(t**j for j in range(M+1))
        assert min(q) >= F(1,8)
        assert min(q[j]-q[j+1] for j in range(M)) >= F(1,16*M)
checks['floor_and_gap_endpoint_worlds'] = 2*126

# All support shapes of at most 3 atoms and three survival values, M=3..6.
# Directly test the target separation consequence, independently of moments.
comparisons = close_pairs = 0
for M in range(3,7):
    eps = F(1,32*M*M)
    ts = (1-F(3,2*M), 1-F(1,M), 1-F(1,2*M))
    worlds = [(s,t,tuple(t**j for j in s))
              for k in range(1,4) for s in combinations(range(M+1),k) for t in ts]
    for a,b in combinations(worlds,2):
        h = hausdorff(a[2],b[2])
        comparisons += 1
        if h < eps:
            close_pairs += 1
            assert target(a[0]) == target(b[0])
            assert len(a[0]) == len(b[0])
            assert all(abs(x-y) <= h for x,y in zip(a[2],b[2]))
checks['hausdorff_pair_comparisons'] = comparisons
checks['hausdorff_close_pairs'] = close_pairs

# A genuinely distinct dilation pair can have identical scalar atoms.
a = F(23,25)
s1,s2 = (2,4),(3,6)
t1,t2 = a**3,a**2
assert 1-F(3,12) <= t1 <= 1-F(1,12)
assert 1-F(3,12) <= t2 <= 1-F(1,12)
assert tuple(t1**j for j in s1) == tuple(t2**j for j in s2)
assert target(s1)==target(s2)
checks['noninteger_direct_scale_equivalence'] = 'PASS: {2,4} and {3,6}'

# Squared-annihilator and coefficient-l1 controls for disjoint and zero cases.
ann_controls = 0
for M in (3,5,8):
    C = 3
    eps = F(1,32*M*M)
    w = F(1,10)
    worlds = [((0,), (F(1),),1-F(3,2*M)),
              ((1,), (F(1),),1-F(1,2*M)),
              ((0,1,M),(F(1,4),F(1,4),F(1,2)),1-F(1,M)),
              ((1,2,M),(F(1,3),)*3,1-F(3,2*M))]
    D = (w/2)*eps**(2*C)/4**C
    for a,b in combinations(worlds,2):
        qa=tuple(a[2]**j for j in a[0]); qb=tuple(b[2]**j for j in b[0])
        h=hausdorff(qa,qb)
        if h < eps: continue
        if not any(min(abs(x-y) for y in qb)>=eps for x in qa):
            a,b=b,a; qa,qb=qb,qa
        P=[F(1)]
        for q in qb: P=mul(P,[q*q,-2*q,F(1)])
        assert sum(abs(c) for c in P)<=4**C
        integ_a=sum(P[r]*moment(*a,r) for r in range(len(P)))
        integ_b=sum(P[r]*moment(*b,r) for r in range(len(P)))
        assert integ_b==0
        assert integ_a >= (w/2)*eps**(2*C)
        md=max(abs(moment(*a,r)-moment(*b,r)) for r in range(1,2*C+1))
        assert md>=D
        ann_controls+=1
checks['annihilator_controls']=ann_controls

# Exact grid rounding at enormous denominators, without enumerating the grid.
round_controls=[]
for M in (3,7,20):
    for C,support,weights in [
        (1,(0,),(F(1),)),
        (1,(M,),(F(1),)),
        (2,(0,M),(F(1,7),F(6,7))),
        (3,(0,1,M),(F(1,8),F(1,4),F(5,8))),
        (3,(1,2,M),(F(1,8),F(3,8),F(1,2))),
    ]:
        w=F(1,10); eps=F(1,32*M*M)
        D=(w/2)*eps**(2*C)/4**C
        for alpha in (None,F(1,100)):
            if alpha is None:
                tau=D/8; Q=ceil(32*C/D)
            else:
                A=(32*M)**(C-1); B=C*(16*M)**(C-1)
                ee=min(eps,alpha/(2*B))
                DD=(w/2)*ee**(2*C)/4**C
                tau=min(DD/8,alpha/(6*A)); Q=ceil(4*C/tau)
            tw=tuple(F((q*Q).numerator//(q*Q).denominator,Q) for q in weights[:-1])
            tw=tw+(1-sum(tw),)
            assert min(tw)>=w/2 and sum(tw)==1
            assert sum(abs(p-q) for p,q in zip(weights,tw)) <= F(2*(len(weights)-1),Q)
            tmin=1-F(3,2*M)
            t=tmin+F(37,113*M)
            h=((t-tmin)*M*Q).numerator//((t-tmin)*M*Q).denominator
            tq=tmin+F(h,M*Q)
            assert tmin<=tq<=t and t-tq<F(1,M*Q)
            err=max(abs(moment(support,weights,t,r)-moment(support,tw,tq,r)) for r in range(1,2*C+1))
            assert err<=F(4*C,Q)<=tau
            round_controls.append({'M':M,'C':C,'support':support,'weight_extension':alpha is not None,
                                   'Q_decimal_digits':len(str(Q)),'PASS':True})
checks['grid_rounding_controls']=round_controls

# Factorial statistics are bounded and have the exact binomial moments.
factorial_controls=0
for R in range(2,9):
    for theta in (F(0),F(1,8),F(3,5),F(1)):
        for r in range(1,R+1):
            stats=[F(comb(s,r),comb(R,r)) if s>=r else F(0) for s in range(R+1)]
            assert all(0<=z<=1 for z in stats)
            expectation=sum(stats[s]*comb(R,s)*theta**s*(1-theta)**(R-s) for s in range(R+1))
            assert expectation==theta**r
            factorial_controls+=1
checks['factorial_identity_controls']=factorial_controls

# Lagrange coefficient and derivative sup certificates for representative supports.
lagrange_controls=0
for M in (3,5,8):
    for support in [(0,), (M,), (0,M), (0,1,M), (1,2,M)]:
        C=len(support); A=(32*M)**(C-1); B=C*(16*M)**(C-1)
        t=1-F(3,2*M); qs=tuple(t**j for j in support)
        for i,q in enumerate(qs):
            p=[F(1)]; den=F(1)
            for k,z in enumerate(qs):
                if k!=i: p=mul(p,[-z,F(1)]); den*=q-z
            p=[c/den for c in p]
            assert sum(abs(c) for c in p)<=A
            # The product-rule bound is uniform on [0,1].
            assert F(max(0,C-1),1)/abs(den)<=B
            lagrange_controls+=1
checks['lagrange_controls']=lagrange_controls
checks['status']='PASS'
print(json.dumps(checks,indent=2))
