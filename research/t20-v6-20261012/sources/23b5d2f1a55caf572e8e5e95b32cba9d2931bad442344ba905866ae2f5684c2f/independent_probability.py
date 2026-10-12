from fractions import Fraction as F
from collections import Counter
from math import lcm
from itertools import product
import json
checks=[]
def check(n,b):
    if not b: raise AssertionError(n)
    checks.append(n)
def compile_rows(rows):
    assert rows and all(all(p>=0 for p in row.values()) and sum(row.values())==1 for row in rows)
    D=lcm(*(p.denominator for row in rows for p in row.values()))
    assert D>0
    tables=[[r for r,p in row.items() for _ in range(int(D*p))] for row in rows]
    assert all(len(t)==D for t in tables)
    return D,tables
rows=[{(0,0,0):F(1,2),(1,0,1):F(1,3),(1,1,0):F(1,6),(9,9,9):F(0)},
      {(0,0,0):F(2,5),(1,0,1):F(3,5)}]
D,tables=compile_rows(rows)
check('heterogeneous_denominators_lcm_30',D==30)
for i,(row,t) in enumerate(zip(rows,tables)):
    c=Counter(t)
    check('joint_count_row_'+str(i),all(F(c[r],D)==p for r,p in row.items()))
check('zero_probability_out_of_range_atom_not_emitted',(9,9,9) not in tables[0])
# Separate branch and successor marginals cannot identify their joint law.
a={(0,0):F(1,2),(1,1):F(1,2)}
b={(0,1):F(1,2),(1,0):F(1,2)}
def push(law,f):
    ans={}
    for x,p in law.items(): ans[f(x)]=ans.get(f(x),F(0))+p
    return ans
check('same_two_marginals_wrong_joint',a!=b and all(push(a,lambda x:x[j])==push(b,lambda x:x[j]) for j in (0,1)))
# Current seed can be uniform before an action but revealed by selected action.
world={(u,u):F(1,2) for u in range(2)}
check('uniform_seed_before_action',push(world,lambda x:x[0])=={0:F(1,2),1:F(1,2)})
check('conditioning_action_breaks_uniformity',all(sum(p for (u,a),p in world.items() if u==a==v)/sum(p for (u,a),p in world.items() if a==v)==1 for v in range(2)))
# A hidden bit persists forever inside each two-seed fibre; fresh output bits suffice.
world={(v0,v1,h):F(1,8) for v0,v1,h in product(range(2),repeat=3)}
seeds=push(world,lambda x:(2*x[0]+x[2],2*x[1]+x[2]))
check('dependent_uniform_seeds',push(seeds,lambda x:x[0])=={u:F(1,4) for u in range(4)} and len(seeds)==8)
check('exact_iid_outputs_despite_hidden_correlation',push(seeds,lambda x:(x[0]//2,x[1]//2))=={v:F(1,4) for v in product(range(2),repeat=2)})
for h in (0,1):
    conditional={2*v+h:F(1,2) for v in (0,1)}
    check('nonuniform_correct_fibres_'+str(h),push(conditional,lambda u:u//2)=={0:F(1,2),1:F(1,2)})
print(json.dumps({'status':'PASS','checks':checks,'scope':'Independent exact finite controls. Standard counting and pushforward mathematics, no novelty claim; no source stochastic semantics.'},indent=2))
