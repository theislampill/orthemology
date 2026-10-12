from itertools import product
from pathlib import Path
import json
out=Path(__file__).resolve().parent
pool=[(),(0,),(1,),(0,1),(1,0),(1,1,0)]
def prefix(b,n):return sum(len(b(i)) for i in range(n))
def flatten(b,t):
 k=0;p=0
 while p+len(b(k))<=t:p+=len(b(k));k+=1
 return k,t-p,b(k)[t-p]
counts={'finite_prefix_patterns':0,'least_crossing_value_checks':0,'eventual_good_checks':0,'nonempty_index_locality_checks':0,'occasional_empty_checks':0}
for n in range(5):
 for pre in product(pool,repeat=n):
  counts['finite_prefix_patterns']+=1
  b=lambda k:pre[k] if k<n else(1,)
  concat=tuple(x for block in pre for x in block)+(1,)*12
  for t,val in enumerate(concat):
   k,j,a=flatten(b,t)
   assert prefix(b,k)<=t<prefix(b,k+1) and 0<=j<len(b(k)) and a==val
   counts['least_crossing_value_checks']+=1
  N=prefix(b,n)
  for t in range(N,N+10):
   k,j,a=flatten(b,t);assert k>=n and a==1
   counts['eventual_good_checks']+=1
nonempty=pool[1:]
for t in range(4):
 for pre in product(nonempty,repeat=t+1):
  b=lambda k:pre[k] if k<len(pre) else (0,)
  other=lambda k:pre[k] if k<len(pre) else (1,1,1,1)
  kb,jb,ab=flatten(b,t);ko,jo,ao=flatten(other,t)
  assert kb==ko and kb<=t and ab==ao
  counts['nonempty_index_locality_checks']+=1
for period in range(2,10):
 b=lambda k:(1,) if k%period==0 else()
 for t in range(100):
  k,j,a=flatten(b,t);assert k==period*t and j==0 and a==1
  counts['occasional_empty_checks']+=1
assert prefix(lambda _:(),100)==0
counts['all_empty_has_no_crossing_at_time_zero']=True
(out/'FINITE_CONTROLS.json').write_text(json.dumps({'status':'PASS','counts':counts},indent=2)+'\n')
print(json.dumps(counts,indent=2))
