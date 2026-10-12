from fractions import Fraction as F
from collections import defaultdict
import json
from pathlib import Path
# Exact duplicated-state lift of action-dependent binary source kernels.
K=lambda s,a:[((r,t),F(1+(s+a+r+t)%3,1)) for r in range(2) for t in range(2)]
def kernel(s,a):
 raw=K(s,a);z=sum(w for _,w in raw);return [(x,w/z) for x,w in raw]
def policy(h):
 p=F(1+sum(a+2*r for a,r in h)%3,4);return [(0,p),(1,1-p)]
def step(law,lift):
 out=defaultdict(F)
 for (h,s),w in law.items():
  base=s[0] if lift else s
  for a,pa in policy(h):
   for (r,t),p in kernel(base,a):
    for tag,pt in ([(0,F(1,3)),(1,F(2,3))] if lift else [(None,F(1))]):
     out[(h+((a,r),),(t,tag) if lift else t)]+=w*pa*p*pt
 return dict(out)
a={((),0):F(2,5),((),1):F(3,5)};b={((),(s,t)):p*q for s,p in [(0,F(2,5)),(1,F(3,5))] for t,q in [(0,F(1,3)),(1,F(2,3))]};checks=[]
for n in range(5):
 erased=defaultdict(F)
 for (h,(s,t)),v in b.items():erased[h,s]+=v
 if dict(erased)!=a:raise RuntimeError(('transport',n))
 checks.append({'horizon':n,'source_cells':len(a),'lifted_cells':len(b),'exact_equal':True})
 if n<4:a=step(a,False);b=step(b,True)
# Equal receipt/state marginals do not entail joint equality.
c={(0,0):F(1,2),(1,1):F(1,2)};d={(0,1):F(1,2),(1,0):F(1,2)}
for coord in [0,1]:
 def marg(p):
  o=defaultdict(F)
  for x,w in p.items():o[x[coord]]+=w
  return dict(o)
 if marg(c)!=marg(d):raise RuntimeError('marginals')
if c==d:raise RuntimeError('joint')
print(json.dumps({'status':'PASS','finite_horizon_checks':checks,'same_marginals_different_joint':True,'scope':'Independent exact finite controls; no general-proof replacement.'},indent=2))
