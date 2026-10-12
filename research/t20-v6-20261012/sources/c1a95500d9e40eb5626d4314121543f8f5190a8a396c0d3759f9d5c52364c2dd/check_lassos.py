#!/usr/bin/env python3
from pathlib import Path
from itertools import product
from fractions import Fraction
import json,hashlib
A=Path(__file__).resolve().parent
alphabet=range(3);prefixes=[x for n in range(5) for x in product(alphabet,repeat=n)];periods=[x for n in range(1,5) for x in product(alphabet,repeat=n)]
counts={'lassos':0,'target_implications':0,'tail_cutoffs':0,'positive_partition_cases':0}
for pre in prefixes:
 for per in periods:
  U=frozenset(per);assert U
  outside=[n for n,a in enumerate(pre) if a not in U];N=max(outside,default=-1)+1
  def x(n):return pre[n] if n<len(pre) else per[(n-len(pre))%len(per)]
  assert all(x(n) in U for n in range(N,len(pre)+2*len(per)));assert not outside or x(N-1) not in U;counts['tail_cutoffs']+=1
  for mask in range(8):
   G={a for a in alphabet if mask>>a&1}
   eventual=all(a in G for a in per)
   assert eventual==(U<=G);counts['target_implications']+=1
  counts['lassos']+=1
streams=[((1,), (0,)),((2,2),(0,)),((0,),(1,)),((),(0,1))]
for weights in product(range(3),repeat=4):
 total=sum(weights)
 if not total:continue
 probs=[Fraction(w,total) for w in weights];cells={}
 for i,(pre,per) in enumerate(streams):cells[frozenset(per)]=cells.get(frozenset(per),Fraction())+probs[i]
 assert sum(cells.values())==1
 for mask in range(8):
  G={a for a in alphabet if mask>>a&1}
  if all(not probs[i] or set(per)<=G for i,(_,per) in enumerate(streams)):
   choices=[U for U,p in cells.items() if p>0 and U<=G];assert choices and all(choices)
   for U in choices:
    pos=[i for i,(pre,per) in enumerate(streams) if probs[i]>0 and frozenset(per)==U];N=max(len(streams[i][0]) for i in pos)
    assert sum(probs[i] for i in pos)>0;assert all(set(streams[i][1])<=U for i in pos)
   counts['positive_partition_cases']+=1
assert frozenset((1,)+(0,)) != frozenset((0,)) # One transient appearance is not recurrence.
result={'status':'PASS_FINITE_CONTROLS','source_sha256':hashlib.sha256((A/'snapshot/RecurrentSupport.lean').read_bytes()).hexdigest(),'checks':counts,'scope':'Exact finite-prefix/eventually-periodic controls and finite rational law partitions; general recurrence and measure statements are separately kernel checked.'}
(A/'FINITE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
