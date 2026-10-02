from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
H=Path(__file__).resolve().parent

def ceil(x):return -((-x.numerator)//x.denominator)
# Dropping ceilings to floors falsely predicts a 1/2 universal guarantee.
u,b,t=7,3,F(1,2)
assert max((t*s).__floor__()+(t*(u-s)).__floor__() for s in range(u+1))<=b
assert F(b,u)<t
# Three orderings need not have a set meeting every ordinal quota at B.
u,b,t=9,4,F(1,4)
orders=[(0,5,6,7,8,1,2,3,4),(1,3,4,7,8,0,2,5,6),(2,3,4,5,6,0,1,7,8)]
assert all(sorted(o)==list(range(u)) for o in orders)
quota_solutions=[]
for C in combinations(range(u),b):
    if all(len(set(C)&set(o[:k]))>=ceil(t*k) for o in orders for k in range(u+1)):
        quota_solutions.append(C)
assert quota_solutions==[]
# This ordinal obstruction is NOT a probability-row counterexample: taking
# uniform rows on the first five objects has worst-case common mass 2/5 > 1/4.
rows=[[F(int(i in o[:5]),5) for i in range(u)] for o in orders]
risk=max(min(sum(p[i] for i in C) for p in rows) for C in combinations(range(u),b))
assert risk==F(2,5)>t
# Private/public conditioning separation retained at the reviewed exact case.
assert F(1,4)>F(3,28)
out={'status':'PASS','controls':{'ceiling_to_floor_false_claim':{'u':7,'b':3,'false_threshold':'1/2','uniform_counterexample_risk':'3/7'},'three_ordering_ordinal_extension_fails':{'u':9,'b':4,'threshold':'1/4','orders':orders,'quota_feasible_four_sets':0,'uniform_prefix_row_risk':str(risk),'interpretation':'Ordinal proof route fails; this does not disprove partition optimality for three probability rows'},'private_shared_separation':['1/4','3/28']}}
(H/'SCOPE_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,sort_keys=True))
