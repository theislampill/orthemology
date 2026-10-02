#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import random,json,sys
if sys.flags.optimize:raise RuntimeError('Optimized Python refused')
def starts(h):return not h or h[-1]==1
def prefix(h,x):return x[:len(h)]==h
r={'prefix_free_slot_families':0,'exact_slot_union_tails':0,'chronological_trials':0,'global_postcount_trials':0}
Omega=list(product((0,1),repeat=8));mass=F(1,len(Omega))
for j in range(7):
 family=[h for n in range(7) for h in product((0,1),repeat=n) if starts(h) and sum(h)==j]
 for i,h in enumerate(family):
  for g in family[i+1:]:assert not prefix(h,g) and not prefix(g,h)
 total=sum((F(1,2**len(h)) for h in family),F(0));assert total<=1;r['prefix_free_slot_families']+=1
 for d in range(3):
  event=lambda x:any(prefix(h,x) and x[len(h):len(h)+d]==(0,)*d for h in family)
  actual=sum((mass for x in Omega if event(x)),F(0));assert actual==total/F(2)**d and actual<=F(1,2**d);r['exact_slot_union_tails']+=1
# The same conditional tail is not payable just once if chronological slots
# are merged: first two fair-coin opportunities have union probability 3/4.
assert sum((mass for x in Omega if x[0]==0 or (x[0]==1 and x[1]==0)),F(0))==F(3,4)>F(1,2)
r['dropping_slot_separation_counterexample']={'correct_union':'3/4','single_tail':'1/2'}
rng=random.Random(202610012318)
for _ in range(2000):
 n=rng.randrange(1,41);progress=[rng.choice((0,1)) for _ in range(n)];bad=[rng.choice((0,1)) for _ in range(n)];d=rng.randrange(11)
 indices=[];ages=[];starts_=[];j=s=0
 for t in range(n):
  indices.append(j);starts_.append(s);ages.append(t-s)
  if progress[t]:j+=1;s=t+1
 ends={t for t in range(n) if progress[t] or t==n-1};J=len(ends)
 assert len(set(zip(indices,ages)))==n and all(i<J for i in indices)
 if sum(bad)>J*d:
  choices=[t for t in range(n) if bad[t] and ages[t]>=d];assert choices
  t=choices[0];s=starts_[t];assert (s==0 or progress[s-1]) and not any(progress[s:s+d])
 r['chronological_trials']+=1
 for L in (1,2,3,7):
  q=3;counts=[0]*q;marks=[]
  for t in range(n):
   a=rng.randrange(q);counts[a]+=1
   if counts[a]<L and rng.choice((0,1)):marks.append((a,counts[a]))
  assert len(marks)==len(set(marks)) and len(marks)<=q*(L-1);r['global_postcount_trials']+=1
# Square-geometric costs meet the two-parameter fallback envelope yet need not
# possess a positive exponential moment. This exact finite grid checks the tail
# inclusion; the infinite-series counterargument is stated in the review.
from math import isqrt
for N,k in product(range(1,80),repeat=2):
 actual=F(1,2**isqrt(N*k));bound=F(1,2**N)+N*F(1,2**k);assert actual<=bound
r['square_geometric_two_parameter_checks']=79**2;r['status']='PASS_INDEPENDENT_STOPPED_UNION_CONTROLS'
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
