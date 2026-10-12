#!/usr/bin/env python3
"""Exact end-to-end interrupted prefix/permission controls; no asymptotic inference."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json
from probe_hellinger_exact import stopped_outcomes
P=[[(F(16,25),F(9,25)),(F(1),F(0))],
   [(F(9,25),F(16,25)),(F(9,25),F(16,25))]]
G=[{0},{1}]
def plans(B,s): return (1,) if B==(1,) else ((1,0) if s else (0,))
def menu(B): return {1} if B==(1,) else {0,1}
rows=[]
for theta in range(2):
 states={((0,1),(F(1),F(1))):F(1)}
 actual_bad=planned_bad=F(0); total_actions=F(0); exits=F(0); normalization_checks=0
 for horizon in range(1,25):
  nxt=defaultdict(F)
  for (B,L),mass in states.items():
   s=max(B,key=lambda i:(L[i],i)); acts=plans(B,s)
   assert acts and set(acts)<=menu(B)
   outs=stopped_outcomes(P,B,acts)
   for m in B:
    assert sum(w[m] for word,C,w in outs)==1;normalization_checks+=1
   planned_bad+=mass*sum(a not in G[theta] for a in acts)
   for word,C,w in outs:
    prob=mass*w[theta]
    assert word and all(a in menu(B) for a,y in word)
    for j,(a,y) in enumerate(word):
     Bnext=tuple(m for m in B if P[m][a][y]>0)
     if Bnext!=B: assert j==len(word)-1 # first shrink ends old-menu execution
    actual_bad+=prob*sum(a not in G[theta] for a,y in word)
    total_actions+=prob*len(word)
    if C!=B:
     assert set(C)<set(B);exits+=prob
     Ln=tuple(F(m in C) for m in range(2))
    else:Ln=tuple(L[m]*w[m] for m in range(2))
    nxt[(C,Ln)]+=prob
  states=nxt
  assert sum(states.values())==1
  assert actual_bad<=planned_bad
  bound=F(125,53) if theta==0 else F(425,16)
  assert planned_bad<=bound
  assert total_actions>=horizon
  assert exits<=1
 rows.append({'theta':theta,'horizon':24,'normalization_checks':normalization_checks,
  'states':len(states),'actual_bad':str(actual_bad),'planned_charge':str(planned_bad),
  'certificate_bound':str(bound),'expected_actions':str(total_actions),'expected_exits':str(exits)})
# Initial tied MLE chooses candidate1 with old plan [1,0]. Under theta1, y=1
# on its first action reveals model1. Finishing action0 would violate the new menu.
violation_mass=P[1][1][1]
assert violation_mass==F(16,25)
result={'status':'PASS','arithmetic':'exact Fraction','models':rows,
 'mutant_finish_old_plan_forbidden_action_probability':str(violation_mass),
 'checks':['full branch normalization','true-model-preserving strict exits','equal-weight live reset',
 'nonempty executed prefixes','old-menu licensing','no post-exit tail action','actual bad count <= planned charge',
 'certificate expected charge bound at each tested finite horizon'],
 'scope':'Finite exact semantic controls; the infinite theorem is supplied by the separate Lean proof.'}
p=Path(__file__).parent/'evidence'/'RECORDED_PHYSICAL_EXACT_CHECKS.json';p.write_text(json.dumps(result,indent=2)+'\n');print(p);print('PASS')
