#!/usr/bin/env python3
from itertools import combinations,product
from fractions import Fraction as Q
import json
rows=[]
for f in range(1,5):
 n=2*f+1;roots=set(range(n));Cs=[set(c) for j in range(f+1) for c in combinations(roots,j)]
 views=0;cases=0;batches=0
 for reports in product((0,1),repeat=n):
  theta=int(sum(reports)>f)
  worlds=[c for c in Cs if all(reports[i]==theta for i in roots-c)]
  if not worlds:continue
  views+=1;cases+=len(worlds)
  known_bad={i for i,b in enumerate(reports) if b!=theta}; k=len(known_bad)
  possible_bad=set.union(*worlds)
  safe=roots-possible_bad
  assert safe==(roots-known_bad if k==f else set())
  survivors=roots-known_bad
  uniform_risk=max(Q(len(c&survivors),len(survivors)) for c in worlds)
  assert uniform_risk==Q(f-k,n-k)
  # Uniform mixing by adversary over maximal compatible C gives every unknown
  # root the same membership rate; any pure action therefore costs >= bound.
  maxworlds=[c for c in worlds if len(c)==f]
  rates=[Q(sum(i in c for c in maxworlds),len(maxworlds)) for i in roots]
  assert min(rates)==Q(f-k,n-k)
 for c in Cs:
  for batch in combinations(roots,f+1):
   q=False
   for i in batch:q=q or i not in c
   assert q;batches+=1
 rows.append({'f':f,'n':n,'views':views,'compatible_report_world_pairs':cases,'fail_silent_batches':batches})
# A corruptible shared gate is a one-vertex transversal regardless of n.
for n in (3,5,9):
 supports=[{-1,i} for i in range(n)]
 assert all(-1 in s for s in supports)
 assert not all(set()&s for s in supports)
print(json.dumps({'status':'PASS_INDEPENDENT_VIEW_AND_MINIMAX_CHECKS','families':rows,'common_gate_min_cut':1,'scope':'Finite source-independent implementation; general minimax proof is algebraic, not inferred from enumeration'},indent=2))
