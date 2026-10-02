#!/usr/bin/env python3
"""Independent finite cover/support checks for zero-error disclosure."""
from itertools import combinations,product
import json
out=[];support_checks=0
for s in range(1,7):
 U=set(range(s))
 for b in range(s):
  Cs=[set(c) for j in range(b+1) for c in combinations(U,j)]
  minimum=None
  for M in range(1,s+1):
   menus=[set(t) for t in combinations(U,M)]
   wins=[all(bool(T-C) for C in Cs) for T in menus]
   assert all(w==(M>b) for w in wins)
   if any(wins) and minimum is None:minimum=M
  assert minimum==b+1
  if s<=5:
   supports=[set(t) for j in range(1,s+1) for t in combinations(U,j)]
   for M in range(1,min(b,2)+1):
    for family in product(supports,repeat=M):
     # One positive-probability representative per message yields a static C.
     C={min(t) for t in family}
     assert len(C)<=b and all(C&t for t in family)
     support_checks+=1
  out.append({'roots':s,'residual_budget':b,'minimal_zero_error_alphabet':minimum})
print(json.dumps({'status':'PASS_FINITE_DISCLOSURE_COVER_AND_SUPPORTS','families':out,'private_support_controls':support_checks,'shared_randomness':'General probability-one finite-intersection argument inspected separately; not simulated','scope':'Finite checks supplement ordinary proof, not source/channel authentication'},indent=2))
