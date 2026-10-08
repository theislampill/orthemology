from itertools import product
from fractions import Fraction as F
import json
signs=lambda n:list(product((-1,1),repeat=n))
def flip(x,e,blocks):
 y=list(x)
 for k,b in enumerate(blocks):
  for i in b:y[i]*=e[k]
 return tuple(y)
def stat(x,a):return abs(sum(v*w for v,w in zip(x,a)))
def orbit(x,blocks):return [flip(x,e,blocks) for e in signs(len(blocks))]
def pval(x,a,blocks):
 o=orbit(x,blocks);return F(sum(stat(y,a)>=stat(x,a) for y in o),len(o))
blocks=((0,1),(2,3));patterns=[(1,b,1,d) for b,d in signs(2)];masses=[F(1,10),F(2,10),F(3,10),F(4,10)]
weights=[(F(1),)*4,(F(0),F(1),F(0),F(-1)),(F(1,3),F(-2,7),F(5,9),F(0)),(F(0),)*4]
conditional_checks=0;unconditional_checks=0
for a in weights:
 full={}
 for pattern,mass in zip(patterns,masses):
  o=orbit(pattern,blocks);assert len(set(o))==4
  ps=[pval(x,a,blocks) for x in o]
  for alpha in set(ps+[F(0),F(1),F(1,20)]):
   assert F(sum(p<=alpha for p in ps),4)<=alpha;conditional_checks+=1
  for x in o:full[x]=mass/4
 for alpha in set([pval(x,a,blocks) for x in full]+[F(0),F(1),F(1,20)]):
  assert sum(q for x,q in full.items() if pval(x,a,blocks)<=alpha)<=alpha;unconditional_checks+=1
six=tuple((i,) for i in range(6));a=(F(1),)*6
assert pval((1,)*6,a,six)==F(1,32)
assert pval((-1,)*6,a,six)==F(1,32)
wrong_size=sum(F(1,2) for x in [(1,)*6,(-1,)*6] if pval(x,a,six)<=F(1,20));assert wrong_size==1
assert pval((1,)*6,a,(tuple(range(6)),))==1
for a in [(F(0),)*6,(F(1),F(-2),F(0),F(0),F(0),F(0)),(F(1),)*6]:
 k=sum(v!=0 for v in a);bound=F(2,2**k) if k else F(1)
 ps=[pval(x,a,six) for x in signs(6)];assert min(ps)==bound
out={'purpose':'Independent exact arithmetic controls for successor orbit section; synthetic inputs only','conditional_rank_inequalities':conditional_checks,'unconditional_rank_inequalities':unconditional_checks,'unequal_orbit_probability_mass':'1/10,2/10,3/10,4/10','weight_choices':4,'six_block_extreme_tail':'1/32','common_orientation_wrong_test_size':'1','valid_global_complement_tail':'1','zero_and_mixed_contribution_resolution_cases':3,'status':'PASS','proofs_reviewed_separately':True}
print(json.dumps(out,indent=2))
