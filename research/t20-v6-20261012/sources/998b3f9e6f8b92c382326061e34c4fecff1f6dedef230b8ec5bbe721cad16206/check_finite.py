from itertools import product
from pathlib import Path
import json
r=Path(__file__).resolve().parent
pool=[(),(0,),(1,),(0,1),(1,0),(1,1,0)]
def concat(b,N):return tuple(x for n in range(N) for x in b(n))
def decode(d,b,t):
 xs=concat(b,t+1);return xs[t] if t<len(xs) else d
def flat(b,t):
 n=0;p=0
 while p+len(b(n))<=t:p+=len(b(n));n+=1
 return b(n)[t-p]
c={'prefix_locality':0,'covered_prefix_flatten_equality':0,'nonempty_decoder_identity':0,'all_empty_fallbacks':0}
for t in range(5):
 for pre in product(pool,repeat=t+1):
  b=lambda n:pre[n] if n<len(pre) else(0,)
  other=lambda n:pre[n] if n<len(pre) else(1,1,1)
  assert decode(99,b,t)==decode(99,other,t);c['prefix_locality']+=1
  for N in range(t+2):
   xs=concat(b,N)
   for k,a in enumerate(xs):assert a==flat(b,k);c['covered_prefix_flatten_equality']+=1
  if all(pre):
   assert decode(99,b,t)==flat(b,t);c['nonempty_decoder_identity']+=1
for t in range(100):assert decode(99,lambda _:(),t)==99;c['all_empty_fallbacks']+=1
sparse=lambda n:(n//2,) if n%2==0 else()
assert decode(99,sparse,1)==99 and flat(sparse,1)==1
result={'status':'PASS','counts':c,'sharp_boundary':{'unbounded_recurring_empty_path':True,'decode_at_1':99,'flatten_at_1':1,'meaning':'Unbounded alone cannot replace every-block nonemptiness in decode_eq_flatten'}}
(r/'FINITE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
