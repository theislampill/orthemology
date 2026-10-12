from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict
from math import isqrt
from pathlib import Path
import json
A=Path(__file__).resolve().parent
# State=(phase,L0,L1,candidate,index,partial observations); all histories newest first.
def P(theta,a,y):
 if not theta and a:return F(0) if y else F(1)
 return (F(16,25) if theta else F(9,25)) if y else (F(9,25) if theta else F(16,25))
def plan(phase,candidate):return (True,) if phase else ((True,False) if candidate else (False,))
def spawn(phase,L0=F(1),L1=F(1)):
 candidate=True if phase or L1>=L0 else False
 return phase,L0,L1,candidate,0,()
def action(s):return plan(s[0],s[3])[s[4]]
def step(s,y):
 phase,L0,L1,candidate,i,obs=s;a=action(s);obs=obs+(y,)
 if not phase and a and y:return spawn(True),True
 if i+1<len(plan(phase,candidate)):return (phase,L0,L1,candidate,i+1,obs),False
 ls=[L0,L1]
 for theta in [False,True]:
  for a0,y0 in zip(plan(phase,candidate),obs):ls[theta]*=P(theta,a0,y0)
 return spawn(phase,*ls),True
def sqrtq(q):
 assert q>=0;n,d=isqrt(q.numerator),isqrt(q.denominator);assert n*n==q.numerator and d*d==q.denominator
 return F(n,d)
def Fmacro(theta,s):
 phase,L0,L1,*_=s
 if phase:return F(0)
 mass=L1 if theta else L0
 if mass==0:return F(0)
 return 25*sqrtq(L0/L1)+F(25,16) if theta else F(125,53)*sqrtq(L1/L0)
@lru_cache(None)
def Vnode(theta,s):
 a=action(s);ans=F(a!=theta)
 for y in [False,True]:
  p=P(theta,a,y)
  if p:
   nxt,leaf=step(s,y);ans+=p*(Fmacro(theta,nxt) if leaf else Vnode(theta,nxt))
 return ans

def replay(h):
 s=spawn(False)
 for a,y in reversed(h):s,_=step(s,y)
 return s

def compatible(h):
 s=spawn(False)
 for a,y in reversed(h):
  if a!=action(s):return False
  s,_=step(s,y)
 return True

def support(h):return {theta for theta in [False,True] if all(P(theta,a,y)>0 for a,y in h)}
def menu(B):return {True} if B=={True} else {False,True}
def terminal_blocks(theta,s):
 a=action(s)
 for y in [False,True]:
  p=P(theta,a,y)
  if not p:continue
  nxt,leaf=step(s,y)
  if leaf:yield ((a,y),),nxt,p
  else:
   for tail,end,q in terminal_blocks(theta,nxt):yield ((a,y),)+tail,end,p*q
counts={'positive_physical_histories':0,'one_step_drift_checks':0,'macro_spawn_bounds':0,'canonical_history_mass_checks':0,'dynamic_licence_checks':0,'micro_macro_prefix_law_equalities':0,'zero_branches_skipped':0}
for theta in [False,True]:
 root=spawn(False);bound=Fmacro(theta,root)
 assert bound==(F(125,53) if not theta else F(425,16))
 frontier={():F(1)}
 for N in range(9):
  expected=F(0)
  for h,prob in frontier.items():
   s=replay(h);a=action(s)
   assert compatible(h) and theta in support(h)
   assert a in menu(support(h));counts['dynamic_licence_checks']+=1
   raw=F(1)
   for aa,yy in h:raw*=P(theta,aa,yy)
   assert raw==prob;counts['canonical_history_mass_checks']+=1
   assert s[2 if theta else 1]>0
   drift=F(a!=theta)
   for y in [False,True]:
    p=P(theta,a,y)
    if p:drift+=p*Vnode(theta,step(s,y)[0])
    else:counts['zero_branches_skipped']+=1
   assert drift<=Vnode(theta,s);counts['one_step_drift_checks']+=1
   if s[4]==0:
    assert Vnode(theta,s)<=Fmacro(theta,s);counts['macro_spawn_bounds']+=1
   expected+=prob*sum(aa!=theta for aa,yy in h)
   counts['positive_physical_histories']+=1
  assert expected<=bound
  # Independently generate whole stopped blocks, then integrate away overshoot.
  macro=defaultdict(F)
  def visit(s,chron,prob):
   if len(chron)>=N:
    macro[tuple(reversed(chron[:N]))]+=prob;return
   for block,nxt,p in terminal_blocks(theta,s):visit(nxt,chron+block,prob*p)
  visit(root,(),F(1))
  assert dict(macro)==frontier;counts['micro_macro_prefix_law_equalities']+=1
  nxt=defaultdict(F)
  for h,prob in frontier.items():
   a=action(replay(h))
   for y in [False,True]:
    p=P(theta,a,y)
    if p:nxt[((a,y),)+h]+=prob*p
  frontier=dict(nxt)
wrong=((True,True),(True,False))
assert not compatible(wrong) and support(wrong)=={True} and action(replay(wrong))==False and False not in menu(support(wrong))
# Positive likelihood is essential: an impossible killed history can have zero
# normalized potential even though an attempted new action carries positive cost.
zero_guard={'phase':'before one-cost exit to a zero-cost absorbing phase','killed_history_mass':0,'normalized_potential':0,'current_charge':1,'next_expected_potential':0,'unguarded_drift_claim':False}
r={'status':'PASS','counts':counts,'bounds':{'theta_false':'125/53','theta_true':'425/16'},'action_consistency_counterexample':{'newest_first_history':wrong,'exact_support':[True],'allowed_next_actions':[True],'replayed_next_action':False,'compatible':False},'zero_likelihood_guard':zero_guard,'scope':'Exact rational and exact square-root finite fixture for the predecessor two-phase zero-support model; universal canonical-law and recursive-certificate conclusions are the Lean theorems, not a Python refinement claim.'}
(A/'FINITE_CONTROL_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
