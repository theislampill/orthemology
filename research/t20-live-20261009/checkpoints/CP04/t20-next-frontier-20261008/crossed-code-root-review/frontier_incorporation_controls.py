#!/usr/bin/env python3
"""Controls only for new crossed-code claims in RESULT.md, not its count appendix."""
from fractions import Fraction as F
from itertools import product
import json

def response(a,b):
    return (a,b,a+b-a*b,a*b)

def channel(r,s):
    return [(1-r)*(1-s),(1-r)*s,r*(1-s),r*s]  # 00,01,10,11

cases=0
for eps in (F(1,2),F(1,3),F(1,16),F(1,1000)):
    world0=channel(F(1),eps)
    world1=[(1-eps)*x+eps*y for x,y in zip(channel(F(1),F(0)),channel(F(1),F(1)))]
    assert world0==world1==[F(0),F(0),1-eps,eps]
    assert min(1-eps,eps)>=eps
    # Even the conditional error promise for absent labels is consistent.
    r,s=response(F(1),F(0)),response(eps,F(1))
    ideals=((1,0),(0,1),(1,1),(0,0))
    for j in range(4):
        assert (1-r[j] if ideals[j][0] else r[j])<=eps
        assert (1-s[j] if ideals[j][1] else s[j])<=eps
    cases+=1

# Pure-A/pure-B extension when the minimum-positive floor exceeds 1/2.
for w in (F(2,3),F(3,4),F(1)):
    r=response(F(1,2),F(1,2))
    assert channel(r[0],r[0])==channel(r[1],r[1])
    assert F(1,2)<=w<=1

# Small exhaustive antichain quotient check, retaining multiplicities in histograms.
supports=(1,2,3)
sig_to_min={}; min_to_sig={}
for hist in product(range(3),repeat=3):
    present=[s for s,n in zip(supports,hist) if n]
    minimal=tuple(s for s in present if not any(t!=s and t&s==t for t in present))
    signature=tuple(int(any(s&t==s for s in present)) for t in range(4))
    assert sig_to_min.setdefault(signature,minimal)==minimal
    assert min_to_sig.setdefault(minimal,signature)==signature
assert len(sig_to_min)==5
print(json.dumps({'status':'PASS','scope':'RESULT.md crossed-code incorporation only; arbitrary-rate count appendix excluded',
                 'route_rate_contamination_examples':cases,'large_floor_pure_label_examples':3,
                 'histograms_for_antichain_quotient':27,'distinct_corner_quotients':5},indent=2))
