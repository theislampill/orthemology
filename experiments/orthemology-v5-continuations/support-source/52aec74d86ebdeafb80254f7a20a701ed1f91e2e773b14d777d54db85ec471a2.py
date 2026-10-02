#!/usr/bin/env python3
"""Independent finite semantics and exact-arithmetic countercontrols."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math
checks=0
for T in range(9):
 for progress in product((0,1),repeat=T):
  pc=[sum(progress[:t]) for t in range(T+1)]
  for danger in product((0,1),repeat=T):
   slots=[sum(danger[t] and pc[t]==j for t in range(T)) for j in range(T+1)]
   assert sum(slots)==sum(danger)
   for s in range(T+1):
    for i in range(pc[s]):
     assert slots[i]==sum(danger[t] and pc[t]==i for t in range(s))
   if T:assert max(pc[:-1]) < sum(bool(progress[t] or t+1==T) for t in range(T))
   checks+=1
for D in range(1,9):
 for n in range(41):
  for k in range(14):assert (k<(n+D-1)//D)==(k*D<n)
# Two maximally dependent durations, each either 1 or 2, both selected by one coin.
a=F(4,3);factor=[a,a*a]; expectation=sum(factor)/2;product_expectation=sum(x*x for x in factor)/2
assert product_expectation != expectation**2
assert all(x<=2 for x in factor) and product_expectation<=4
# A no-start branch retains arbitrary past weight; dropping it breaks the bound.
past=[F(100),F(2)];fac=[F(1),a]; lhs=sum(x*y for x,y in zip(past,fac))/2
union_only_rhs=2*past[1]/2; proper_rhs=2*sum(past)/2
assert union_only_rhs<lhs<=proper_rhs
rates=[]
for p in [1.0,0.5,0.1]:
 for D in [1,2,5]:
  q=1-p**D; lam=math.log(2/(1+q)); assert 0<=q<1 and lam>0; assert math.isclose(1+(2/(1+q)-1)/(1-2*q/(1+q)),2,rel_tol=1e-10)
  rates.append({'p':p,'D':D,'lambda':lam,'physical_rate':lam/D})
result={'status':'PASS','exhaustive_progress_danger_horizon_cases':checks,'ceil_div_boundary_cases':8*41*14,'dependent_duration_product':str(product_expectation),'incorrect_independence_product':str(expectation**2),'no_start_total':str(lhs),'incorrect_omitted_complement_bound':str(union_only_rhs),'correct_weighted_bound':str(proper_rhs),'first_action_counterexample':{'actual_count':1,'count_if_skipping_zero':0,'ceil_block_charge':1,'floor_block_charge':0},'rate_samples':rates,'scope':'Finite exact rational and enumeration controls are supporting semantic checks, not substitutes for source proofs'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
