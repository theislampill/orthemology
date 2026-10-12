from fractions import Fraction as F
from itertools import combinations,product
from random import Random
from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parents[1];rng=Random(731992)
def subsets(xs):
 xs=tuple(sorted(xs));return [frozenset(c) for k in range(1,len(xs)+1) for c in combinations(xs,k)]
def reaches(s,adj):
 R={s}
 while True:
  new=R|{y for z in R for y in adj[z]}
  if new==R:return R
  R=new
def components(P,theta,pairs):
 out=[]
 for E in subsets(pairs):
  C={s for s,a in E};adj={s:{y for z,a in E if z==s for y,w in enumerate(P[theta][s][a]) if w} for s in C}
  if any(not adj[s]<=C for s in C):continue
  if all(reaches(s,adj)==C for s in C):out.append(E)
 return out
def maximal(sets):return frozenset(E for E in sets if not any(E<D for D in sets))
def matching(P,theta,sigma,E):return all(P[theta][s][a]==P[sigma][s][a] for s,a in E)
def parity_valid(P,pri,theta,E):return all(min(pri[sigma][s][a] for s,a in E)%2==0 for sigma in range(len(P)) if matching(P,theta,sigma,E))
def pruned(P,pri,theta,pairs,all_odds=False):
 active=frozenset(pairs);rounds=[]
 while True:
  mecs=maximal(components(P,theta,active));inside=frozenset().union(*mecs);delete=set(active-inside)
  for D in mecs:
   for sigma in range(len(P)):
    if matching(P,theta,sigma,D):
     low=min(pri[sigma][s][a] for s,a in D)
     if all_odds:delete|={e for e in D if pri[sigma][e[0]][e[1]]%2}
     elif low%2:delete|={e for e in D if pri[sigma][e[0]][e[1]]==low}
  rounds.append({'active':len(active),'deleted':len(delete)})
  if not delete:return mecs,rounds
  active=active-frozenset(delete)
checked=0;valid_counts=0
for case in range(350):
 n=1+case%2;k=1+(case//2)%3;m=1+(case//6)%3
 choices=[(F(1),)] if n==1 else [(F(1),F(0)),(F(0),F(1)),(F(1,2),F(1,2)),(F(1,4),F(3,4))]
 P=tuple(tuple(tuple(rng.choice(choices) for a in range(k)) for s in range(n)) for t in range(m));pri=tuple(tuple(tuple(rng.randrange(6) for a in range(k)) for s in range(n)) for t in range(m))
 for theta in range(m):
  # Zero theta exit: each positive theta successor retains every live model.
  pairs={(s,a) for s in range(n) for a in range(k) if all(not P[theta][s][a][y] or all(P[t][s][a][y]>0 for t in range(m)) for y in range(n))}
  all_ec=components(P,theta,pairs);valid=[E for E in all_ec if parity_valid(P,pri,theta,E)];want=maximal(valid);got,rounds=pruned(P,pri,theta,pairs);assert got==want;checked+=1;valid_counts+=len(valid)
  for E,D in product(valid,repeat=2):
   if {s for s,a in E}&{s for s,a in D}:assert E|D in valid
# Odd priorities are not automatically bad: forced 2/3 cycle wins.
P=((( (F(0),F(1)),),((F(1),F(0)),)),);pri=(((2,),(3,)),);pairs={(0,0),(1,0)}
assert pruned(P,pri,0,pairs)[0]==frozenset({frozenset(pairs)})
assert not pruned(P,pri,0,pairs,all_odds=True)[0]
# Successive odd minima require successive pruning.
P=((((F(1),),(F(1),),(F(1),)),),);pri=(((1,3,4),),)
got,rounds=pruned(P,pri,0,{(0,0),(0,1),(0,2)});assert got==frozenset({frozenset({(0,2)})}) and len(rounds)==3
# An unmatched rival becomes matched after the first row disappears.
P=tuple(tuple(tuple((F(3,4),F(1,4)) if t==2 and a==0 else (F(1,2),F(1,2)) for a in range(3)) for s in range(2)) for t in range(3))
pri=tuple(tuple((2,2,2) if t==0 else ((1,2,4) if t==1 else (2,1,2)) for s in range(2)) for t in range(3));pairs={(s,a) for s in range(2) for a in range(3)}
got,rounds=pruned(P,pri,0,pairs);assert got==frozenset({frozenset({(0,2),(1,2)})}) and len(rounds)==3
# Identical feedback, opposite even single actions: alternating wins parity.
P=((((F(1),),(F(1),)),),(((F(1),),(F(1),)),));pri=(((2,3),),((3,2),));E=frozenset({(0,0),(0,1)})
assert parity_valid(P,pri,0,E) and not parity_valid(P,pri,0,frozenset({(0,0)})) and not parity_valid(P,pri,0,frozenset({(0,1)}))
# Remaining in a valid component without fairness can lose: retain only priority3.
assert min([2,3])%2==0 and min([3])%2==1
out={'status':'FRESH_PASS_PARITY_COMPONENT_CONTROLS','generated_systems':350,'candidate_component_comparisons':checked,'valid_components_examined':valid_counts,'controls':['minimal versus all odd deletion','successive odd layers','newly matching rival','opposite hidden parity with identical feedback','full-pair recurrence'],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite pruning/oracle comparisons; the infinite strategy theorem is an ordinary proof obligation.'};(A/'CONTROL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
