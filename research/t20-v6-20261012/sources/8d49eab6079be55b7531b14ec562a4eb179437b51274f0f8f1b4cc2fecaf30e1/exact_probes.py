from fractions import Fraction as F
import itertools as it
import json
from pathlib import Path
from accuracy_checks import brier, project_complements, uniform_coherent_repair, convex_regret


grid=[F(i,10) for i in range(11)]
weights=[F(i,20) for i in range(1,20)]
projection_cases=statewise_checks=0
for x,y,a in it.product(grid,grid,weights):
    b=(x,y);c=project_complements(b,a);assert sum(c)==1
    delta=a*(1-a)*(x+y-1)**2
    for v in [(1,0),(0,1)]:
        assert brier(b,v,a)-brier(c,v,a)==delta
        assert delta>0 if x+y!=1 else delta==0
        statewise_checks+=1
    projection_cases+=1

b=(F(7,10),F(3,5));threshold_cases=0
for j in range(50):
    h=F(j,100)
    r=uniform_coherent_repair(b,F(1,2)-h,F(1,2)+h)
    assert r['exists']==(h*h+330*h-25<0)
    threshold_cases+=1

proper_cases=0
for p,q,g in it.product(grid,grid,['quadratic','complement_quartic','symmetric_quadratic','symmetric_quartic']):
    regret=convex_regret(p,q,g)
    assert regret>0 if p!=q else regret==0
    proper_cases+=1

# All absolute-error loss pairs have constant sum two, so no strict dominance.
absolute_cases=0
for x,y in it.product(grid,repeat=2):
    losses=[abs(x-v[0])+abs(y-v[1]) for v in [(1,0),(0,1)]]
    assert sum(losses)==2;absolute_cases+=1

# Jensen's identity for a two-point randomized coherent repair.
jensen_cases=0
for t,u,mix,a,v in it.product(grid,grid,[F(1,4),F(1,2),F(3,4)],
                              [F(1,4),F(3,4)],[(1,0),(0,1)]):
    c=(t,1-t);d=(u,1-u);mean=tuple(mix*x+(1-mix)*y for x,y in zip(c,d))
    gap=mix*brier(c,v,a)+(1-mix)*brier(d,v,a)-brier(mean,v,a)
    assert gap==mix*(1-mix)*(t-u)**2
    assert gap>=0;jensen_cases+=1

# Proposed narrow common repair has exact uniform endpoint margin.
c=(F(11,20),F(9,20));gains=[brier(b,v,a)-brier(c,v,a)
 for a in [F(9,20),F(11,20)] for v in [(1,0),(0,1)]]
assert min(gains)==F(3,500)
# Calibration comparison and report-dependent outcome example.
assert (F(3,5)-1)**2==F(4,25)<F(1,4)
assert F(1,2)*(1-F(1,2))==F(1,4)>0*(1-0)

# Observed-outcome locality deletion controls.
q=(F(1,2),F(1,4),F(1,4)); r=(F(1,2),F(49,100),F(1,100))
proper_brier_reward=lambda report,i:2*report[i]-sum(x*x for x in report)
assert proper_brier_reward(q,0)==F(5,8)
assert proper_brier_reward(r,0)==F(2549,5000)
p=(F(1,2),F(3,10),F(1,5)); q=(F(51,100),F(3,10),F(19,100))
naive_local_reward=lambda report:sum(p[i]*(-2*(1-report[i])**2) for i in range(3))
assert naive_local_reward(q)-naive_local_reward(p)==F(173,50000)

out={'status':'EXACT_FINITE_PROBES_NOT_FORMAL_NORMATIVE_AUTHORITY',
     'projection_cases':projection_cases,'statewise_gain_identities':statewise_checks,
     'uncertainty_threshold_cases':threshold_cases,'strict_propriety_grid_cases':proper_cases,
     'absolute_error_constant_sum_cases':absolute_cases,'randomized_jensen_identities':jensen_cases,
     'narrow_uniform_gain':str(min(gains)),'broad_common_weak_repair':False,'locality_deletion_checks':3,'mismatches':0}
Path('probe_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
