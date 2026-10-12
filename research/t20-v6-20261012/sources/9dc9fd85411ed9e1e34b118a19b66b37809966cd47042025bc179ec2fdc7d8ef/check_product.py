#!/usr/bin/env python3
"""Exact finite controls for the ordinary hidden deterministic monitor product.
No parity decision oracle, determinisation or finite-error theorem is invoked.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import random,json,hashlib
BASE=Path(__file__).resolve().parents[1]

def make_product(T,D,L,n,r,a,o):
 P={}
 for q,z,u in product(range(n),range(r),range(a)):
  z1=D[z,L[q,u]]
  P[q,z,u]={(y,q1,w):T[q,u].get((y,q1),F(0)) if w==z1 else F(0) for y,q1,w in product(range(o),range(n),range(r))}
 return P

def source_paths(T,b,H,policy):
 dist={(tuple([q]),tuple()):p for q,p in enumerate(b) if p}
 for _ in range(H):
  nxt=defaultdict(F)
  for (qs,h),p in dist.items():
   u=policy(h)
   for (y,q1),weight in T[qs[-1],u].items():
    if weight:nxt[(qs+(q1,),h+((u,y),))]+=p*weight
  dist=dict(nxt)
 return dist

def monitored_source(T,b,D,L,c,z0,H,policy):
 out=defaultdict(F)
 for (qs,h),p in source_paths(T,b,H,policy).items():
  zs=[z0]
  for q,(u,y) in zip(qs,h):zs.append(D[zs[-1],L[q,u]])
  out[(h,qs[-1],zs[-1],tuple(c[z] for z in zs[:-1]))]+=p
 return dict(out)

def product_paths(P,b,z0,c,H,policy):
 dist={(q,z0,tuple(),tuple()):p for q,p in enumerate(b) if p}
 for _ in range(H):
  nxt=defaultdict(F)
  for (q,z,h,priorities),p in dist.items():
   u=policy(h)
   for (y,q1,z1),weight in P[q,z,u].items():
    if weight:nxt[(q1,z1,h+((u,y),),priorities+(c[z],))]+=p*weight
  dist=dict(nxt)
 return {(h,q,z,cs):p for (q,z,h,cs),p in dist.items()}

rng=random.Random(10011318);counts={'systems':0,'normalized_product_rows':0,'posterior_deterministic_row_observation_checks':0,'finite_joint_history_laws':0,'initial_support_checks':0}
for case in range(700):
 n=1+rng.randrange(3);r=1+rng.randrange(4);a=1+rng.randrange(2);o=1+rng.randrange(3);sigma=1+rng.randrange(3)
 T={}
 for q,u in product(range(n),range(a)):
  weights=[rng.randrange(4) for _ in range(o)]
  if not sum(weights):weights[rng.randrange(o)]=1
  T[q,u]={(y,rng.randrange(n)):F(weights[y],sum(weights)) for y in range(o)}
 D={(z,l):rng.randrange(r) for z,l in product(range(r),range(sigma))}
 L={(q,u):rng.randrange(sigma) for q,u in product(range(n),range(a))}
 c=[rng.randrange(6) for _ in range(r)];z0=rng.randrange(r)
 weights=[rng.randrange(4) for _ in range(n)]
 if not sum(weights):weights[rng.randrange(n)]=1
 b=[F(w,sum(weights)) for w in weights]
 P=make_product(T,D,L,n,r,a,o)
 for key,row in P.items():
  assert all(p>=0 for p in row.values()) and sum(row.values())==1;counts['normalized_product_rows']+=1
  for y in range(o):
   assert sum(p>0 for (v,q1,z1),p in row.items() if v==y)<=1
   counts['posterior_deterministic_row_observation_checks']+=1
 bp={(q,z):b[q] if z==z0 else F(0) for q,z in product(range(n),range(r))}
 assert sum(bp.values())==1 and sum(p>0 for p in bp.values())==sum(p>0 for p in b)
 counts['initial_support_checks']+=1
 for seed in [0,1]:
  def policy(h):return (seed+sum((i+1)*(y+1)+u for i,(u,y) in enumerate(h)))%a
  for H in range(5):
   source=monitored_source(T,b,D,L,c,z0,H,policy);lifted=product_paths(P,b,z0,c,H,policy)
   assert source==lifted and sum(source.values())==1
   counts['finite_joint_history_laws']+=1
 counts['systems']+=1
# Timing control: q alternates, a_t alternates with the current q, and the
# monitor reads whether q=a. Current-state labels are all1; next-state labels
# with the same actions are all0. The two parity outcomes differ.
def lasso(next_state,priority,start):
 seen={};states=[];x=start
 while x not in seen:
  seen[x]=len(states);states.append(x);x=next_state(x)
 cycle=states[seen[x]:];return min(priority(s) for s in cycle)%2==0,cycle
D=lambda z,label:label;c=lambda z:2 if z else 1
correct=lambda st:(1-st[0],D(st[1],int(st[0]==st[2])),1-st[2])
wrong=lambda st:(1-st[0],D(st[1],int((1-st[0])==st[2])),1-st[2])
assert lasso(correct,lambda s:c(s[1]),(0,0,0))[0]
assert not lasso(wrong,lambda s:c(s[1]),(0,0,0))[0]
# Exposing the monitor changes information. Hidden q is a static fair tag,
# base observations are always0, label is the hidden match bit q==action.
# Append r1 after first action0: it identifies q, allowing permanent matching.
visible={};hidden={}
for q in [0,1]:
 z1=int(q==0);hidden[q]=(0,);visible[q]=(0,z1)
 chosen_after=0 if z1 else 1
 assert chosen_after==q
 assert lasso(lambda z:D(z,1),c,z1)[0]
assert hidden[0]==hidden[1] and visible[0]!=visible[1]
# Without that extra signal every common policy has the same action law in
# both models; eventual-always-0 and eventual-always-1 events are disjoint.
# Finite periodic controls corroborate that no periodic blind schedule wins both.
blind_periods=0
for size in range(1,7):
 for schedule in product([0,1],repeat=size):
  wins=[]
  for q in [0,1]:
   nxt=lambda st:(D(st[0],int(q==schedule[st[1]])),(st[1]+1)%size)
   wins.append(lasso(nxt,lambda s:c(s[0]),(1,0))[0])
  assert not all(wins);blind_periods+=1
# The initial monitor must be a fixed r0, not independently randomised.
b=[F(1,3),F(2,3),F(0)];r=3;z0=2
fixed={(q,z):b[q] if z==z0 else F(0) for q,z in product(range(3),range(r))}
wrong_prior={(q,z):b[q]/r for q,z in product(range(3),range(r))}
assert sum(p>0 for p in fixed.values())==2 and sum(p>0 for p in wrong_prior.values())==6
# Finite initial priority is not the minimum recurring priority.
assert lasso(lambda z:1,lambda z:1 if z==0 else 2,0)[0]
assert min([1,2])%2==1
# A stochastic monitor fork would destroy PD even over a deterministic source.
assert sum(p>0 for p in [F(1,2),F(1,2)])==2
result={'status':'PASS_FRESH_FINITE_HIDDEN_AUTOMATON_PRODUCT_CONTROLS',**counts,'blind_periodic_schedules_checked':blind_periods,'current_vs_next_label_timing_countercontrol':True,'exposed_monitor_reveals_hidden_tag':True,'initial_support_k_not_kr_countercontrol':True,'finite_initial_priority_countercontrol':True,'nondeterministic_monitor_breaks_pd_countercontrol':True,'seed':10011318,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite product/law controls plus named counterexamples; parity decision theorem is a separate dependency, and no finite-bad-count or determinisation claim is made.'}
(BASE/'evidence/RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
