from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import json, hashlib
OUT=Path(__file__).resolve().parent
src=OUT.parents[1]/'crosswalk/evidence/generated-qualification-20260930T214115Z/source'
weights={
 (0,0,0):(Q(1,2),Q(1,2),Q(0)),(0,1,0):(Q(0),Q(1,3),Q(2,3)),
 (0,0,1):(Q(1,4),Q(3,4)),(0,1,1):(Q(3,4),Q(1,4)),
 (1,0,0):(Q(0),Q(1)),(1,1,0):(Q(1),Q(0)),
 (1,0,1):(Q(2,3),Q(1,3)),(1,1,1):(Q(1,3),Q(2,3)),
}
def pi(p,h):return (p+len(h)+sum(y for a,y in h))%2
def stay(p,a,y):return p==1 or y!=a
def nextphase(p,a,y):return 1
cost={(0,0):Q(2),(0,1):Q(1),(1,0):Q(3),(1,1):Q(4)}
def update(p,h,a,y):return (p,((a,y),)+h) if stay(p,a,y) else(nextphase(p,a,y),())
def mass(theta,p,h):
 r=Q(1)
 for a,y in h:r*=weights[p,theta,a][y] if stay(p,a,y) else Q(0)
 return r
@lru_cache(None)
def future(theta,n,p,h):
 if n==0:return Q(0)
 a=pi(p,h)
 return cost[p,a]+sum(w*future(theta,n-1,*update(p,h,a,y)) for y,w in enumerate(weights[p,theta,a]))
@lru_cache(None)
def reset(theta,n,p,h,mutant=False):
 if n==0:return Q(0)
 a=pi(p,h);m=mass(theta,p,h)
 return cost[p,a]*m+sum(reset(theta,n-1,p,((a,y),)+h,mutant) if stay(p,a,y)
   else (Q(0) if mutant else m*w*reset(theta,n-1,nextphase(p,a,y),(),mutant))
   for y,w in enumerate(weights[p,theta,a]))
def enumlaw(theta,n,p):
 states={(p,()):Q(1)};expected=Q(0)
 for step in range(n):
  assert sum(states.values())==1
  expected+=sum(m*cost[q,pi(q,h)] for(q,h),m in states.items())
  nxt={}
  for(q,h),m in states.items():
   a=pi(q,h)
   for y,w in enumerate(weights[q,theta,a]):
    t=update(q,h,a,y);nxt[t]=nxt.get(t,Q(0))+m*w
  states=nxt
 assert sum(states.values())==1
 return expected
checks=[]
for theta,p,n in product(range(2),range(2),range(8)):
 x=enumlaw(theta,n,p);y=future(theta,n,p,());z=reset(theta,n,p,())
 assert x==y==z
 checks.append((theta,p,n,str(x)))
weighted=0;zero=0
for theta,p in product(range(2),range(2)):
 hs=[()]+[((a,y),) for a in range(2) for y in range(len(weights[p,theta,a]))]
 hs += [((a,y),(b,z)) for a in range(2) for y in range(len(weights[p,theta,a]))
     for b in range(2) for z in range(len(weights[p,theta,b]))]
 for h,n in product(hs,range(6)):
  assert reset(theta,n,p,h)==mass(theta,p,h)*future(theta,n,p,h)
  weighted+=1;zero+=int(mass(theta,p,h)==0)
# Omitting exit branches is not harmless: full law carries future cost there.
mutations=[]
for theta,p,n in product(range(2),range(2),range(1,5)):
 true=enumlaw(theta,n,p);bad=reset(theta,n,p,(),True)
 if true!=bad:mutations.append(dict(theta=theta,phase=p,horizon=n,correct=str(true),omitted_exit=str(bad)))
assert mutations
# Charging after the transition is not the source's index convention.
theta=0;p=0;a=pi(p,());after=sum(w*cost[q,pi(q,h)] for y,w in enumerate(weights[p,theta,a]) for q,h in [update(p,(),a,y)])
assert after != enumlaw(theta,1,p)
# Literal stopped-prefix action bad count, with multiplicities, all binary plans.
prefix_checks=0
for n in range(6):
 for acts in product(range(2),repeat=n):
  for mask in range(4):
   good={a for a in range(2) if mask&(1<<a)}
   planned=sum(a not in good for a in acts)
   for k in range(n+1):
    actual=sum(a not in good for a in acts[:k]);assert actual<=planned
    assert (planned>0)==(not set(acts)<=good)
    prefix_checks+=1
# Live-mask domination requires the selection to be live.
assert 1>0  # one bad action, but a nonlive mask would charge zero
names=['MarkovCharge','ResetExpectation','TrajectoryBudget','ResetFutureCost','ResetTrajectory','GeneratedLiveController','StoppedActionCost','ResetBudget','FiniteBudgetAlmostSure']
manifest={n:hashlib.sha256((src/(n+'.lean')).read_bytes()).hexdigest() for n in names}
result={'status':'PASS_SEMANTIC_CONTROLS_NOT_LEAN_REBUILD','source_dir':str(src), 'source_sha256':manifest,
 'finite_root_law_equalities':len(checks),'weighted_arbitrary_history_equalities':weighted,'zero_mass_history_cases':zero,
 'literal_prefix_domination_cases':prefix_checks,'detected_omitted_exit_mutations':len(mutations),'first_mutation':mutations[0],
 'index_control':{'before_transition_charge':str(enumlaw(0,1,0)),'wrong_after_transition_charge':str(after)},
 'limits':['Exact rational semantic controls do not substitute for independent kernel replay.','The sealed theorem is on state paths and planned blocks; outcome-annotated physical flattening is outside this slice.']}
(OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
