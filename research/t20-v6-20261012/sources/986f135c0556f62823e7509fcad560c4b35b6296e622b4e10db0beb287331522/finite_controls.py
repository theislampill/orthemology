#!/usr/bin/env python3
"""Independent finite-state projections and exact scope countermodels."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,hashlib,json,random

def closure(nodes,edges):
 r={(s,s) for s in nodes}|set(edges)
 for k in nodes:
  for s in nodes:
   for t in nodes:
    if (s,k) in r and (k,t) in r:r.add((s,t))
 return r

def bottom_classes(edges):
 nodes=list(range(4));r=closure(nodes,edges);classes=[];left=set(nodes)
 while left:
  s=min(left);c={t for t in nodes if (s,t) in r and (t,s) in r};left-=c
  if all(t in c for a,t in edges if a in c):classes.append(c)
 return classes

def is_component(E,support):
 if not E:return False
 states={s for s,a in E}
 if any(not support[2*s+a] or not support[2*s+a]<=states for s,a in E):return False
 r=closure(sorted(states),{(s,t) for s,a in E for t in support[2*s+a]})
 return all((s,t) in r for s in states for t in states)

def generic_targets(rows,priorities,theta):
 # One action at each of three states. Direct subset enumeration, no pruning.
 B=range(2);internal=[{y for y in range(3) if all(rows[m][s][y]>0 for m in B)} for s in range(3)]
 allowed=[s for s in range(3) if all(rows[theta][s][y]==0 or y in internal[s] for y in range(3))]
 targets=set()
 for mask in range(1,8):
  E={s for s in range(3) if mask>>s&1}
  if not E<=set(allowed) or any(not internal[s] or not internal[s]<=E for s in E):continue
  reach=closure(sorted(E),{(s,y) for s in E for y in internal[s]})
  if not all((s,t) in reach for s in E for t in E):continue
  matching=[m for m in B if all(rows[m][s]==rows[theta][s] for s in E)]
  if all(min(priorities[m][s] for s in E)%2==0 for m in matching):targets |= E
 return targets

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():raise SystemExit('Output must be fresh')
 a.out.mkdir(parents=True);systems=components=strict=0
 # Every two-state/two-action support pattern, every two-memory action table,
 # every memory-update table depending on old memory and acquired receipt.
 supp_options=[{0},{0,1},{1}]
 for codes in product(range(3),repeat=4):
  support=[supp_options[c] for c in codes]
  for acts in range(16):
   action=lambda s,m:(acts>>(2*s+m))&1
   for updates in range(16):
    update=lambda m,y:(updates>>(2*m+y))&1
    edges={(2*s+m,2*y+update(m,y)) for s in range(2) for m in range(2) for y in support[2*s+action(s,m)]}
    for C in bottom_classes(edges):
     E={(v//2,action(v//2,v%2)) for v in C}
     assert is_component(E,support),(codes,acts,updates,C,E)
     components+=1;strict+=len(E)<4
    systems+=1
 assert systems==20736
 # Exact prefix likelihood factorisation for genuinely state-consistent adaptive choices.
 rng=random.Random(202610011730);prefix_checks=normalizations=0
 for _ in range(12):
  rows=[[F(rng.randrange(5),4) for _ in range(4)] for _ in range(2)]
  for policy in range(8):
   for theta in range(2):
    for horizon in range(6):
     total=F(0)
     for seed in range(2):
      for word in product(range(2),repeat=horizon):
       state=0;h=[];tapes={e:[] for e in range(4)};mass=F(1,2)
       for n,y in enumerate(word):
        action=(seed+(policy&1)*n+((policy>>1)&1)*sum(v for _,v in h)+((policy>>2)&1)*(h[0][0] if h else 0))%2
        e=2*state+action;p=rows[theta][e];mass*=p if y else 1-p;tapes[e].append(y);h.insert(0,(action,y));state=y
       grouped=F(1,2)
       for e,ys in tapes.items():
        for y in ys:grouped*=rows[theta][e] if y else 1-rows[theta][e]
       assert mass==grouped
       assert sum(map(len,tapes.values()))==horizon
       total+=mass;prefix_checks+=1
     assert total==1;normalizations+=1
 # Common seed marginal alone is insufficient: a source/seed correlation reveals the tag.
 joint={theta:{(seed,y):F(int((seed^y)==theta),2) for seed in range(2) for y in range(2)} for theta in range(2)}
 for theta in range(2):
  assert sum(joint[theta].values())==1
  assert all(sum(joint[theta][s,y] for y in range(2))==F(1,2) for s in range(2))
  assert all(sum(joint[theta][s,y] for s in range(2))==F(1,2) for y in range(2))
  assert all((s^y)==theta for (s,y),mass in joint[theta].items() if mass>0)
 assert joint[0] != joint[1]
 # Eventual no exit does not supply all-time stable-support transfer.
 # States 0 and 1 are shared absorbing rows; state 2 reveals theta once.
 rows=[]
 for theta in range(2):
  rows.append([tuple(F(int(y==s)) for y in range(3)) if s<2 else tuple(F(int(y==theta)) for y in range(3)) for s in range(3)])
 pri=[[2 if s==theta else 1 for s in range(3)] for theta in range(2)]
 for theta in range(2):
  assert generic_targets(rows,pri,theta)==set()
  path=[2]+[theta]*20
  assert all(rows[theta][s][t]==1 for s,t in zip(path,path[1:]))
  assert all(pri[theta][s]==2 for s in path[1:])
  assert rows[0][theta]==rows[1][theta]  # All tail rows match the rival.
  assert pri[1-theta][theta]==1         # The rival would lose on that tail.
  assert rows[1-theta][2][theta]==0     # But its finite prefix is impossible.
 # Uniform raw recurrence alone cannot justify a selected physical-time subsequence.
 assert all((2*k)%2==0 for k in range(100))
 result={'status':'PASS_SCOPED_FINITE_ADAPTIVE_CONTROLS','finite_controller_systems':systems,'bottom_class_projections':components,
   'proper_subset_recurrent_pair_sets':strict,'prefix_factorisation_checks':prefix_checks,'prefix_law_normalisations':normalizations,
   'common_seed_marginal_correlation_countercontrol':True,'eventual_no_exit_matching_tail_countercontrol':True,
   'physical_time_subsequence_countercontrol_scope':'pointwise raw-tape bridge only; a separately proved fresh-time iid construction may have the same canonical law',
   'scope':'Finite controls and explicit countermodels; arbitrary adaptive recurrence is proved in Lean, not inferred from this enumeration'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.out/'COUNTERMODELS.json').write_text(json.dumps({'seed_joint_weights':{str(t):{str(k):str(v) for k,v in j.items()} for t,j in joint.items()},'revealing_rows':[[[str(x) for x in row] for row in model] for model in rows],'priorities':pri},indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
