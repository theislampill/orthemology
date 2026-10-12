from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import defaultdict
import json
A=Path(__file__).resolve().parent
alphabet=[(),(0,),(1,),(1,1),(0,1),(2,0,2)]
cost={0:0,1:2,2:3}
counts=dict(block_patterns=0,position_bijections=0,prefix_cost_identities=0,positive_stopped_paths=0,finite_budget_checks=0,record_index_checks=0,physical_pushforward_checks=0)
for n in range(6):
 for blocks in product(alphabet,repeat=n):
  counts['block_patterns']+=1
  flat=tuple(a for b in blocks for a in b);addr=[];s=0
  for j,b in enumerate(blocks):
   for i,a in enumerate(b): addr.append((s+i,j,i));assert flat[s+i]==a
   s+=len(b)
  assert sorted(t for t,j,i in addr)==list(range(len(flat)))
  assert len({t for t,j,i in addr})==len(addr)
  counts['position_bijections']+=len(addr)
  for k in range(len(flat)+1):
   lhs=sum(cost[a] for a in flat[:k]);rhs=0
   for t,j,i in addr:
    if t<k:rhs+=cost[blocks[j][i]]
   assert lhs==rhs;counts['prefix_cost_identities']+=1
  assert sum(cost[a] for a in flat)==sum(sum(cost[a] for a in b) for b in blocks)

def P(theta,a,y):
 if not theta and a:return F(0) if y else F(1)
 return (F(16,25) if theta else F(9,25)) if y else (F(9,25) if theta else F(16,25))
def acts(phase,sigma):return (True,) if phase else ((True,False) if sigma else (False,))
def stay(phase,a,y):return phase or not(a and y)
def outcomes(theta,phase,plan):
 def go(i,obs,prob):
  if i==len(plan):yield(obs,True,prob);return
  for y in [False,True]:
   p=prob*P(theta,plan[i],y)
   if not p:continue
   if stay(phase,plan[i],y):yield from go(i+1,obs+(y,),p)
   else:yield(obs+(y,),False,p)
 yield from go(0,(),F(1))
def choose(phase,lik):return True if phase or lik[True]>=lik[False] else False
bounds={False:F(250,53),True:F(425,8)}
for theta in [False,True]:
 frontier=[(False,{False:F(1),True:F(1)},(),F(1))]
 for horizon in range(1,6):
  nxt=[]
  for phase,lik,records,prob in frontier:
   sigma=choose(phase,lik);plan=acts(phase,sigma)
   for obs,complete,p in outcomes(theta,phase,plan):
    executed=plan[:len(obs)];assert executed
    newphase=phase or not complete
    if complete:
     nlik={eta:lik[eta] for eta in [False,True]}
     for eta in nlik:
      for a,y in zip(plan,obs):nlik[eta]*=P(eta,a,y)
    else:nlik={False:F(1),True:F(1)}
    nxt.append((newphase,nlik,records+((phase,sigma,executed,complete),),prob*p))
    counts['positive_stopped_paths']+=1
  frontier=nxt;assert sum(p for ph,l,rs,p in frontier)==1
  expected=F(0);push=defaultdict(F)
  for phase,lik,records,prob in frontier:
   blocks=[r[2] for r in records];flat=tuple(a for b in blocks for a in b)
   recordcost=sum(sum(a!=theta for a in b) for b in blocks)
   physicalcost=sum(a!=theta for a in flat)
   assert physicalcost==recordcost;expected+=prob*physicalcost
   post=[()]+blocks
   assert tuple(a for b in post[1:] for a in b)==flat;counts['record_index_checks']+=1
   push[flat]+=prob
   for t in range(len(flat)):
    prefix=tuple(a for b in post[1:t+2] for a in b)
    assert prefix[t]==flat[t]
  assert expected<=bounds[theta];counts['finite_budget_checks']+=1
  assert expected==sum(prob*sum(a!=theta for a in path) for path,prob in push.items());counts['physical_pushforward_checks']+=1
  for k in range(1,6):assert sum(p for path,p in push.items() if sum(a!=theta for a in path)>=k)<=bounds[theta]/k

witnesses={
 'deduplicating_bad_actions':{'executed':[1,1],'actual_bad_count':2,'deduplicated_bad_count':1},
 'dropping_exit_record':{'theta':True,'initial_plan':[True,False],'exit_feedback':True,'probability':'16/25','actual_executed':[True],'dropped_executed':[]},
 'exporting_unexecuted_plan':{'theta':True,'actual_bad_count':0,'planned_bad_count':1},
 'initial_placeholder_not_skipped':{'records':[[],[0]],'default':9,'wrong_first_action':9,'correct_first_action':0},
 'unbounded_is_not_all_nonempty':{'blocks':[[0],[],[1]],'default':9,'decode_time_1':9,'flatten_time_1':1},
 'zero_tail_threshold':{'zero_bad_count':0,'event_count_ge_0_probability':1,'zero_budget_div_zero':0},
 'count_not_last_error_time':{'distribution':'P(T=2^k)=2^-k for k>=1; exactly one bad action at T','expected_error_count':1,'partial_expected_last_time':[str(sum(F(1,2**k)*2**k for k in range(1,n+1))) for n in range(1,9)],'expected_last_error_time':'infinite'}}
r={'status':'PASS','counts':counts,'fixture_scope':'Exact finite-rational predecessor interruptible phase fixture and finite block combinatorics; not universal Python-to-Lean refinement or equality to seeded actionLaw.','bounds':{str(k):str(v) for k,v in bounds.items()},'mutation_witnesses':witnesses}
(A/'FINITE_CONTROL_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
