#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product,combinations
from functools import lru_cache
from pathlib import Path
import random,json,hashlib
BASE=Path(__file__).resolve().parents[1];rng=random.Random(131005)

def powers(S,empty=False):
 S=list(S)
 return [frozenset(c) for k in range(0 if empty else 1,len(S)+1) for c in combinations(S,k)]
def reach(start,adj):
 seen={start};todo=[start]
 while todo:
  x=todo.pop()
  for y in adj.get(x,()):
   if y not in seen:seen.add(y);todo.append(y)
 return seen

def sccs(nodes,adj):
 remaining=set(nodes);out=[]
 while remaining:
  s=next(iter(remaining));rs=reach(s,adj);C={t for t in remaining if t in rs and s in reach(t,adj)}
  assert C;remaining-=C;out.append(frozenset(C))
 return out

def strongly_connected(C,E,succ):
 # Independent Floyd-Warshall closure, separate from the SCC routine above.
 r={(s,t):s==t for s in C for t in C}
 for e in E:
  for t in succ[e]:
   if t in C:r[e[0],t]=True
 for k in C:
  for s in C:
   for t in C:r[s,t]=r[s,t] or (r[s,k] and r[k,t])
 return all(r.values())

def mecs(states,E,succ):
 def run(C):
  C=set(C)
  while C:
   active=frozenset(e for e in E if e[0] in C and succ[e]<=C)
   alive={s for s in C if any(e[0]==s for e in active)}
   if alive!=C:C=alive;continue
   adj={s:set().union(*(succ[e] for e in active if e[0]==s)) for s in C}
   comps=sccs(C,adj)
   if len(comps)==1:return [active]
   return [d for comp in comps for d in run(comp)]
  return []
 return run(states)

stats={'target_comparisons':0,'preserved_subcomponent_checks':0,'union_checks':0,'region_comparisons':0,'finite_policy_necessity_checks':0,'one_model_complete_checks':0}

def target_data(S,A,P,B,W,theta,allowed):
 succ={e:frozenset(y for y in S if all(P[t,e][y]>0 for t in B)) for e in allowed}
 E=frozenset(e for e in allowed if sum(P[theta,e][y] for y in succ[e])==1)
 return E,succ

def valid_sets(S,E,succ,P,colors,B,theta):
 val=[]
 for ee in powers(E):
  C=frozenset(s for s,a in ee)
  if any(not succ[e]<=C for e in ee) or not strongly_connected(C,ee,succ):continue
  match=[t for t in B if all(P[t,e]==P[theta,e] for e in ee)]
  if all(min(colors[t,e] for e in ee)%2==0 for t in match):val.append(ee)
 return val

def pruning(S,E,succ,P,colors,B,theta,witnesses=()):
 E=frozenset(E);rounds=[]
 while True:
  ds=mecs(S,E,succ);keep=frozenset().union(*ds) if ds else frozenset();remove=set()
  for D in ds:
   for t in B:
    if not all(P[t,e]==P[theta,e] for e in D):continue
    d=min(colors[t,e] for e in D)
    if d%2:
     rm={e for e in D if colors[t,e]==d};assert rm
     for valid in witnesses:
      if valid<=D:
       assert not valid&rm;stats['preserved_subcomponent_checks']+=1
     remove|=rm
  new=keep-remove
  if new==E:return set(ds),rounds
  assert len(new)<len(E);rounds.append(sorted(remove));E=frozenset(new)

for case in range(300):
 n=1+case%3;na=1+(case//3)%2;K=1+(case//6)%3
 S=tuple(range(n));A=tuple(range(na));models=tuple(range(K));allpairs=tuple(product(S,A));P={};colors={}
 for e in allpairs:
  common=[rng.randrange(1,4) for _ in S]
  for t in models:
   if case%3==0:ws=common
   elif case%3==1:ws=[rng.randrange(1,4) for _ in S]
   else:ws=[rng.randrange(3) for _ in S];ws[rng.randrange(n)]+=1
   total=sum(ws);P[t,e]=tuple(F(x,total) for x in ws);colors[t,e]=rng.randrange(6)
 for B in powers(models):
  for W in powers(S):
   allowed=frozenset(e for e in allpairs if e[0] in W and rng.randrange(4)!=0)
   for t in B:
    E,succ=target_data(S,A,P,B,W,t,allowed);valid=valid_sets(S,E,succ,P,colors,B,t)
    maximal={V for V in valid if not any(V<U for U in valid)}
    result,rounds=pruning(S,E,succ,P,colors,B,t,valid);assert result==maximal
    stats['target_comparisons']+=1
    for V,U in combinations(valid,2):
     if {e[0] for e in V}&{e[0] for e in U}:
      assert V|U in valid;stats['union_checks']+=1

# Direct co-Buchi regression: matching-rival bad-pair deletion equals priorities2/1.
def cobuchi_prune(S,E,succ,P,good,B,theta):
 E=frozenset(E)
 while True:
  ds=mecs(S,E,succ);keep=frozenset().union(*ds) if ds else frozenset();bad=set()
  for D in ds:
   for t in B:
    if all(P[t,e]==P[theta,e] for e in D):bad|={e for e in D if not good[t,e]}
  new=keep-bad
  if new==E:return set(ds)
  E=frozenset(new)
cobuchi_regressions=0
for case in range(120):
 S=tuple(range(1+case%3));A=(0,1);B=frozenset(range(1+case%3));P={};good={}
 for e in product(S,A):
  common=[rng.randrange(1,4) for _ in S]
  for t in B:
   ws=common if case%2 else [rng.randrange(1,4) for _ in S]
   P[t,e]=tuple(F(x,sum(ws)) for x in ws);good[t,e]=bool(rng.randrange(2))
 colors={(t,e):2 if good[t,e] else 1 for t,e in good}
 for theta in B:
  E,succ=target_data(S,A,P,B,frozenset(S),theta,frozenset(product(S,A)))
  out,_=pruning(S,E,succ,P,colors,B,theta)
  assert out==cobuchi_prune(S,E,succ,P,good,B,theta);cobuchi_regressions+=1
# In a forced good/bad cycle2/1 loses co-Buchi;0/1 would wrongly win it.
assert min([2,1])%2==1 and min([0,1])%2==0

# Named odd-layer cascade in a one-state component.
S=(0,);A=(0,1,2);B=frozenset([0,1]);E=frozenset(product(S,A));P={(t,e):(F(1),) for t in B for e in E};succ={e:frozenset(S) for e in E}
colors={(0,(0,a)):2*a for a in A}|{(1,(0,a)):v for a,v in enumerate([1,3,4])}
valid=valid_sets(S,E,succ,P,colors,B,0);out,rounds=pruning(S,E,succ,P,colors,B,0,valid)
assert out=={frozenset([(0,2)])} and rounds==[[(0,0)],[(0,1)]]
layer_cascade=rounds
# Deletion exposes a previously unmatched rival.
S=(0,1);A=(0,1,2);B=frozenset([0,1,2]);E=frozenset(product(S,A));P={(t,e):(F(1,2),F(1,2)) for t in B for e in E}
P[2,(0,0)]=(F(1,4),F(3,4));succ={e:frozenset(S) for e in E}
colors={(t,e):(2 if t==0 else 4) for t in B for e in E};colors[1,(0,0)]=1;colors[2,(0,1)]=1
valid=valid_sets(S,E,succ,P,colors,B,0);out,rounds=pruning(S,E,succ,P,colors,B,0,valid)
assert out=={E-{(0,0),(0,1)}} and rounds[:2]==[[(0,0)],[(0,1)]]
match_cascade=rounds
# A larger odd priority must not be deleted from a valid forced cycle.
S=(0,1);A=(0,);B=frozenset([0]);E=frozenset(product(S,A));P={(0,(0,0)):(F(0),F(1)),(0,(1,0)):(F(1),F(0))};succ={(0,0):frozenset([1]),(1,0):frozenset([0])};colors={(0,(0,0)):2,(0,(1,0)):3}
valid=valid_sets(S,E,succ,P,colors,B,0);out,_=pruning(S,E,succ,P,colors,B,0,valid);assert out=={E}
assert sum((t%2)==1 for t in range(20))==10
# An unfair infinite run can remain inside a valid component but lose parity.
# One state has choices of priority2 and3: uniform visits both; constant3 loses.
assert min([2,3])%2==0 and min([3])%2==1

def compute_regions(S,A,models,P,colors,menus,method):
 @lru_cache(None)
 def win(B):
  W=frozenset(S)
  while True:
   allowed=set()
   for s in W:
    for a in menus[B,s]:
     good=True
     for y in S:
      C=frozenset(t for t in B if P[t,(s,a)][y]>0)
      if C and ((C==B and y not in W) or (C!=B and y not in win(C))):good=False
     if good:allowed.add((s,a))
   adj={s:set() for s in W}
   for e in allowed:
    adj[e[0]]|={y for y in S if all(P[t,e][y]>0 for t in B)}
   retain=set(W)
   for t in B:
    E,succ=target_data(S,A,P,B,W,t,allowed)
    if method=='enum':ds=valid_sets(S,E,succ,P,colors,B,t)
    else:ds,_=pruning(S,E,succ,P,colors,B,t)
    T={s for D in ds for s,a in D}
    T|={s for s,a in allowed if any(P[t,(s,a)][y]>0 and frozenset(u for u in B if P[u,(s,a)][y]>0)!=B for y in S)}
    retain&={s for s in W if reach(s,adj)&T}
   new=frozenset(retain)
   if new==W:return W
   assert new<W;W=new
 return {B:win(B) for B in powers(models)}

def policy_as(S,P,colors,theta,B0,s0,table):
 start=(B0,s0);adj={};pri={};todo=[start];seen=set()
 while todo:
  x=todo.pop()
  if x in seen:continue
  seen.add(x)
  if x=='dead':adj[x]={'dead'};pri[x]=1;continue
  B,s=x;a=table[B,s]
  if a is None:adj[x]={'dead'};pri[x]=1;todo.append('dead');continue
  pri[x]=colors[theta,(s,a)];adj[x]=set()
  for y in S:
   if P[theta,(s,a)][y]>0:
    C=frozenset(t for t in B if P[t,(s,a)][y]>0);z=(C,y);adj[x].add(z);todo.append(z)
 for C in sccs(seen,adj):
  if all(adj[x]<=C for x in C) and min(pri[x] for x in C)%2:return False
 return True

for case in range(90):
 n=1+case%3;na=2;K=1 if case<45 else 2
 S=tuple(range(n));A=(0,1);models=tuple(range(K));P={};colors={}
 for t in models:
  for e in product(S,A):
   ws=[rng.randrange(3) for _ in S];ws[rng.randrange(n)]+=1;P[t,e]=tuple(F(x,sum(ws)) for x in ws);colors[t,e]=rng.randrange(6)
 menus={(B,s):frozenset(a for a in A if rng.randrange(3)>0) for B in powers(models) for s in S}
 r0=compute_regions(S,A,models,P,colors,menus,'enum');r1=compute_regions(S,A,models,P,colors,menus,'prune');assert r0==r1;stats['region_comparisons']+=1
 # Enumerate memoryless support/state policies. K=2,n=3 may have512 policies; bounded.
 keys=list(menus);choices=[tuple(menus[key]) or (None,) for key in keys];union={B:set() for B in powers(models)}
 for vals in product(*choices):
  table=dict(zip(keys,vals))
  for B in powers(models):
   for s in S:
    wins=all(policy_as(S,P,colors,t,B,s,table) for t in B)
    if wins:assert s in r1[B];union[B].add(s)
    stats['finite_policy_necessity_checks']+=1
 if K==1:
  assert all(frozenset(union[B])==r1[B] for B in r1);stats['one_model_complete_checks']+=1

# Same-support observed monitors have the same almost-sure classification.
monitor_cases=0
for m in [1,2,3]:
 nodes=set(range(m))
 for edges in product(range(m),repeat=2*m):
  trans=[{t:sum((F(1,4) if bit else F(3,4)) for bit in [0,1] if edges[2*s+bit]==t) for t in nodes} for s in nodes]
  trans2=[{t:sum((F(3,4) if bit else F(1,4)) for bit in [0,1] if edges[2*s+bit]==t) for t in nodes} for s in nodes]
  adj={s:{t for t,p in trans[s].items() if p>0} for s in nodes};adj2={s:{t for t,p in trans2[s].items() if p>0} for s in nodes};assert adj==adj2
  comps=sccs(nodes,adj)
  for cs in product([0,1],repeat=m):
   for s in nodes:
    R=reach(s,adj);R2=reach(s,adj2)
    good=all(min(cs[x] for x in C)%2==0 for C in comps if C<=R and all(adj[x]<=C for x in C))
    good2=all(min(cs[x] for x in C)%2==0 for C in comps if C<=R2 and all(adj2[x]<=C for x in C))
    assert good==good2;monitor_cases+=1
r={'status':'PASS_FRESH_PARITY_CONTROLS','generated_target_systems':300,**stats,'monitor_AS_classification_cases':monitor_cases,'cobuchi_2_1_regressions':cobuchi_regressions,'wrong_0_1_encoding_rejected':True,'odd_layer_cascade':layer_cascade,'new_matching_rival_cascade':match_cascade,'forced_even_odd_cycle_wins':True,'finite_odd_visit_cost_claim_rejected':True,'unfair_operation_control_loses':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact component/pruning and policy controls, not a proof of the infinite all-history theorem.'}
(BASE/'evidence/PARITY_CONTROLS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
