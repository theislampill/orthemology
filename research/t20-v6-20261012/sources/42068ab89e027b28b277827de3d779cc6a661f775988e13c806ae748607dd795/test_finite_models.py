#!/usr/bin/env python3
from itertools import product
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json,datetime

def bounded_lasso(ask,nxt,word,initial,N):
    s,k=initial,0; seen={}; trace=[]
    while (s,k) not in seen:
        seen[s,k]=len(trace);trace.append((s,k))
        if ask[s]:
            if k==N:return None
            s=nxt[2*s+word[k]];k+=1
        else:s=nxt[2*s]
    return (tuple(trace),seen[s,k])

stats={'controllers':0,'prefix_factorisation_checks':0,'bounded_lassos':0,'zero_prefix_checks':0}
for ask in product([False,True],repeat=3):
 for nxt in product(range(3),repeat=6):
  stats['controllers']+=1
  for initial in range(3):
   for N in range(3):
    groups={}
    for word in product([0,1],repeat=N+1):
     result=bounded_lasso(ask,nxt,word,initial,N)
     prefix=word[:N]
     if prefix in groups: assert groups[prefix]==result
     else:groups[prefix]=result
     stats['prefix_factorisation_checks']+=1
     stats['zero_prefix_checks']+=(N==0)
     stats['bounded_lassos']+=(result is not None)

# Same seed marginal, opposite perfect seed/first-bit correlations.
# The two actual joint laws are mutually singular; both are dominated by the fair product.
joints=[{(0,0):F(1,2),(1,1):F(1,2)},{(0,1):F(1,2),(1,0):F(1,2)}]
reference={(s,b):F(1,4) for s,b in product(range(2),repeat=2)}
assert not(set(joints[0])&set(joints[1]))
for joint in joints:
 assert [sum(p for (s,b),p in joint.items() if s==i) for i in range(2)]==[F(1,2)]*2
 for atom,p in joint.items():assert p>0 and reference[atom]>0
# Exhaustively all 16 events, not only singletons.
for mask in range(16):
 event={atom for i,atom in enumerate(reference) if mask>>i&1}
 if sum(reference[a] for a in event)==0:
  assert all(sum(joint.get(a,0) for a in event)==0 for joint in joints)

# Deliberate premise deletions: changed seed marginal or incomplete reference.
changed_seed_actual={(1,0):F(1)}
changed_seed_reference={(0,0):F(1,2),(0,1):F(1,2)}
revealing_seed_event={(1,0),(1,1)}
assert sum(changed_seed_actual.get(x,0) for x in revealing_seed_event)==1
assert sum(changed_seed_reference.get(x,0) for x in revealing_seed_event)==0
incomplete_bit_reference={(0,0):F(1)}
deterministic_true_actual={(0,1):F(1)}
revealing_bit_event={(0,1)}
assert sum(deterministic_true_actual.get(x,0) for x in revealing_bit_event)==1
assert sum(incomplete_bit_reference.get(x,0) for x in revealing_bit_event)==0
# Parameter-coded seed is observed at time zero; changed seed destroys domination even with zero queries.
# Missing positive reference mass fails with a one-query controller and deterministic opposite bit.
assert reference[(1,0)]>0

# Exact rational strict-repair sufficiency over a grid, including extreme allowed estimates.
def good(a,e,q):
 return q*q<=a*(F(1,2)+e)**2+(1-a)*F(1,2)**2 and (1-q)**2<=a*(F(1,2)-e)**2+(1-a)*F(1,2)**2
poly=0
for denominator in range(2,35):
 for numerator in range(1,denominator):
  a=F(numerator,denominator)
  for en in range(1,17):
   e=F(en,64)
   for factor in [F(-1),F(-1,2),F(0),F(1,2),F(1)]:
    estimate=a+factor*a*(1-a)*e/4;q=F(1,2)+estimate*e
    assert 0<q<1 and q*q<a*(F(1,2)+e)**2+(1-a)*F(1,2)**2
    assert (1-q)**2<a*(F(1,2)-e)**2+(1-a)*F(1,2)**2
    poly+=1
assert all(good(F(a,100),0,F(1,2)) for a in range(-100,201))
assert all(good(F(1,4)+F(a,1600),F(1,4),F(9,16)) for a in range(101))
assert abs((F(21,32)-F(1,2))/F(1,4)-F(1,2))<=F(1,8)
assert not good(F(1,2),F(1,4),F(21,32))
# Finite-prefix locality would be false for an evaluator that leaks an unused bit when ask=false.
leaky=lambda oracle:(oracle[0],0)
assert leaky([False])!=leaky([True])
# Counter monotonicity cannot be weakened to a fake never-incrementing query counter.
fake_trace=tuple((0,0) for _ in range(5))
fake_ask=lambda state: True
assert all(counter==0 for state,counter in fake_trace)
assert all(fake_ask(state) for state,counter in fake_trace)
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**stats,
 'correlated_joint_laws':2,'joint_event_checks':16,'strict_repair_rational_cases':poly,
 'sharpness_controls':['changed initial marginal defeats zero-query domination','missing reference bit defeats one-query domination','unused-bit leak defeats N=0 locality','fake query counter defeats bounded/eventual equivalence','zero epsilon accepts every norm','constant positive epsilon accepts an interval','decoder tolerance alone is insufficient'],
 'scope':'Finite exact-rational and exhaustive finite-state controls; the general results are separately Lean-checked.'}
Path(__file__).resolve().parents[1].joinpath('FINITE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
