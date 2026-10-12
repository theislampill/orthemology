#!/usr/bin/env python3
"""Independent rational dynamic-programming, path-law and pair-weight checks."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json

def avoid(P,t,n,s):
    v=[F(1)]*len(P)
    for _ in range(n):v=[F(0) if x==t else sum(P[x][y]*v[y] for y in range(len(P))) for x in range(len(P))]
    return v[s]
def path_law(P,start,N):
    out={(start,):F(1)}
    for _ in range(N):
        nxt=defaultdict(F)
        for xs,w in out.items():
            for y,p in enumerate(P[xs[-1]]):
                if p:nxt[xs+(y,)]+=w*p
        out=dict(nxt)
    return out
count=0
for p,q in product([F(0),F(1,4),F(1,2),F(3,4),F(1)],repeat=2):
    P=((p,1-p),(q,1-q))
    for target,start,a,n in product(range(2),range(2),range(3),range(5)):
        law=path_law(P,start,max(0,a+n-1))
        actual=sum(w for xs,w in law.items() if all(xs[a+i]!=target for i in range(n)))
        if a==0:assert actual==avoid(P,target,n,start)
        assert actual<=max(avoid(P,target,n,s) for s in range(2))
        count+=1
# A biased strongly connected chain: the transition weights matter quantitatively.
P=((F(3,4),F(1,4)),(F(1),F(0)))
assert avoid(P,1,1,0)==1 and avoid(P,1,2,0)==F(3,4) and avoid(P,1,3,0)==F(9,16)
assert avoid(P,0,1,0)==0
for k in range(8):
    for s in range(2):assert avoid(P,1,k*2,s)<=F(3,4)**k
# Weights are uniform within an observed state's action fiber, not globally.
source=(0,0,1);weights=(F(1,2),F(1,2),F(1))
rows=((F(0),F(1)),(F(1),F(0)),(F(1),F(0)))
K=tuple(tuple(rows[e][source[f]]*weights[f] for f in range(3)) for e in range(3))
assert all(sum(r)==1 for r in K)
assert K[0]==(0,0,1) and K[1]==(F(1,2),F(1,2),0)
bad=tuple(tuple(rows[e][source[f]]*F(1,3) for f in range(3)) for e in range(3))
assert any(sum(r)!=1 for r in bad)
# A disconnected absorbing chain and a zero-weight action scheduler fail recurrence.
absorbing=((F(1),F(0)),(F(0),F(1)))
unfair=((F(0),F(1)),(F(0),F(1)))
assert all(avoid(absorbing,1,n,0)==1 and avoid(unfair,0,n,1)==1 for n in range(10))
print(json.dumps({'status':'PASS_INDEPENDENT_RECURRENCE_CONTROLS','exact_window_cases':count,
 'checks':{'coordinate_count_matches_path_law':True,'arbitrary_start_window_bound':True,
 'biased_geometric_bound':True,'state_fiber_normalization':True,
 'global_action_normalization_rejected':True,'disconnected_and_unfair_controls':True},
 'scope':'Finite exact controls only; the almost-sure infinite recurrence proof is separately cold-replayed'},indent=2))
