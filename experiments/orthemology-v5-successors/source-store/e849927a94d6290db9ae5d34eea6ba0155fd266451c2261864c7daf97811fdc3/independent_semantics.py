#!/usr/bin/env python3
"""Reviewer controls; no finite result is substituted for the generic kernel proof."""
from itertools import combinations,product,permutations
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json,sys

def require(x,m):
 if not x: raise RuntimeError(m)
def subsets(m,k): return tuple(frozenset(s) for s in combinations(range(m),k))
def minimum_cover(m,b,k):
 worlds,blocks=subsets(m,k),subsets(m,b)
 for n in range(len(blocks)+1):
  for family in combinations(blocks,n):
   if all(any(t<=a for a in family) for t in worlds): return n
 raise RuntimeError('No feasible cover')

exact={(0,0,0):1,(1,0,0):1,(4,1,1):4,(4,2,1):2,(5,2,1):3,(6,3,1):2,(5,2,2):10}
for args,n in exact.items(): require(minimum_cover(*args)==n,('cover',args))
sequence_cases=0
u=frozenset(range(4));paths=tuple(u-t for t in subsets(4,1));worlds=subsets(4,1)
for cap in range(5):
 for seq in product(paths,repeat=cap):
  misses=[t for t in worlds if all(not p.isdisjoint(t) for p in seq)]
  require((not misses)==(len(set(seq))==4),'dedup and sharp opaque cap')
  sequence_cases+=1
means={};probabilities={}
for t in worlds:
 positions=[next(i+1 for i,p in enumerate(seq) if p.isdisjoint(t)) for seq in permutations(paths)]
 means[str(sorted(t))]=str(Fraction(sum(positions),len(positions)))
 require(means[str(sorted(t))]=='5/2','as cap/expectation separation')
 require(max(positions)==4,'a.s. uniform-permutation cap')
 probabilities[str(sorted(t))]=str(Fraction(sum(n>3 for n in positions),len(positions)))
 require(probabilities[str(sorted(t))]=='1/4','fixed-world failure probability')

full_trace_cases=0;fixed_world_failures=[];defective_cases=0
for m,B,c,seed_count,caps in [(4,1,1,73,range(7)),(7,1,2,37,[0,1,3,10,20,21])]:
 k=B+c-1;u=frozenset(range(m));worlds=subsets(m,k);paths=tuple(u-t for t in worlds)
 target=('target-17','version-3','epoch-19','recipient-5','scope-2',(0,1))
 def policy(seed,h):
  # Every prior full action and control/effect/cancellation reply is included.
  z=int(sha256(repr((seed,h)).encode()).hexdigest()[:16],16)
  return (z%len(paths),seed*100000+len(h)*100+z%100,target)
 def control(cmd,h):
  idx,nonce,body=cmd
  return (tuple((label,'prepare',cmd,1) for label in sorted(paths[idx])),
          tuple((label,'cancel-close',cmd,3) for label in sorted(paths[idx])),
          sha256(repr(h).encode()).hexdigest()[:8])
 for cap in caps:
  fails={t:0 for t in worlds}
  for seed in range(seed_count):
   for t in worlds:
    a=tuple(sorted(t)[:c]);root=lambda i: ('alias',) if i in a else ('singleton',i)
    faults={root(i) for i in t}
    require(len(faults)==B and {i for i in u if root(i) in faults}==set(t),'one fixed alias/fault realizer')
    actual=[];spine=[];ahit=False;shit=False;nonces=[]
    for _ in range(cap):
     x=policy(seed,actual);good=paths[x[0]].isdisjoint(t);ahit|=good;nonces.append(x[1])
     actual=[(x,(control(x,actual),good))]+actual
     y=policy(seed,spine);shit|=paths[y[0]].isdisjoint(t)
     spine=[(y,(control(y,spine),False))]+spine
    require(len(nonces)==len(set(nonces)),'fresh nonordinal, history-dependent nonce')
    require(ahit==shit,'full actual-history/failure-spine first-hit equivalence')
    if not ahit: fails[t]+=1
    for initial in [False,True]:
     state=initial
     for cmd,reply in reversed(actual):
      if paths[cmd[0]].isdisjoint(t): state=True
     require(state==(initial or ahit),'identity-or-repair defective-start bridge')
     defective_cases+=1
    full_trace_cases+=1
  if cap<len(worlds):
   t=max(worlds,key=lambda t:fails[t]);p=Fraction(fails[t],seed_count)
   require(p>=Fraction(1,len(worlds)),'one fixed pre-coin world has positive probability')
   fixed_world_failures.append({'m':m,'B':B,'c':c,'cap':cap,'T':sorted(t),'alias':sorted(t)[:c],'failure_probability':str(p),'generic_union_bound':str(Fraction(1,len(worlds)))})

# A reliable failed-root identity is a genuinely different observation contract.
first=frozenset({0,1,2});u=frozenset(range(4));richer_attempts=[]
for t in subsets(4,1):
 if first.isdisjoint(t): richer_attempts.append(1)
 else:
  second=u-t;require(second.isdisjoint(t),'revealed fixed fault gives clean second path');richer_attempts.append(2)
require(max(richer_attempts)==2<4,'richer feedback invalidates opaque cap')
result={'status':'PASS','small_exact_cover_controls':{str(a):n for a,n in exact.items()},'all_failure_sequences_checked':sequence_cases,'full_command_trace_checks':full_trace_cases,'state_bridge_checks':defective_cases,'full_command_features':['complete prior history','history-dependent path','fresh nonordinal history-dependent nonce','fixed repair body','full-command per-label prepare/cancel replies','truthful effect receipt'],'fixed_root_worlds_outside_coin_quantifier':fixed_world_failures,'uniform_permutation_fixed_world_expectation':means,'uniform_permutation_fixed_world_failure_after_three':probabilities,'rich_failure_identity_cap':2,'opaque_cap':4}
payload=json.dumps(result,indent=2,sort_keys=True)+'\n';Path(sys.argv[1]).write_text(payload);print(payload)
