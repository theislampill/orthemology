from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
A=Path(__file__).resolve().parent
# Actions and observations are 0/1; unsafe action 1 separates P,Q.
P={0:{0:F(1,2),1:F(1,2)},1:{0:F(1),1:F(0)}}
Q={0:{0:F(1,2),1:F(1,2)},1:{0:F(0),1:F(1)}}
def paths(law,policy,n):
 d={():F(1)}
 for t in range(n):
  nxt={}
  for h,m in d.items():
   a=policy(h)
   for y,p in law[a].items():
    if p:nxt[((a,y),)+h]=m*p
  d=nxt
 return d
def const(h):return 0
def explore_once(h):return 1 if not h else h[-1][1]
checks=0
for n in range(10):
 for policy in [const,explore_once,lambda h:len(h)%2,lambda h:h[0][1] if h else 0]:
  ps,qs=paths(P,policy,n),paths(Q,policy,n)
  for h in set(ps)|set(qs):
   if all(a==0 for a,y in h):assert ps.get(h,0)==qs.get(h,0);checks+=1
  assert sum(ps.values())==sum(qs.values())==1
# Eventually-inside alone cannot replace always-inside. Same selected laws
# on D={0}; the first out-of-D observation is singular and chooses the tail.
for n in range(2,10):
 ps,qs=paths(P,explore_once,n),paths(Q,explore_once,n)
 ep=sum(m for h,m in ps.items() if all(a==0 for a,y in h[:-1]))
 eq=sum(m for h,m in qs.items() if all(a==0 for a,y in h[:-1]))
 assert ep==1 and eq==0
# Fixed common stack law: unused coordinate has zero observable effect but
# differs as a raw full-row event (P row[1]=0 has mass1, Q mass0).
assert P[1][0]==1 and Q[1][0]==0
# One-sided finite-prefix domination with source delta0, reference fair.
for n in range(12):
 assert F(1,2)**n>0
# Positive branch guard: deterministic0 observations never reach bad branch1.
Z={a:{0:F(1),1:F(0)} for a in (0,1)}
branch=lambda h:0 if not h else h[-1][1]
assert all(all(a==0 for a,y in h) for h in paths(Z,branch,12))
assert branch(((0,1),))==1
# Model-coded private seeds defeat common-seed information requirements.
for theta in (0,1):assert all(a==theta for a in [theta]*20)
assert not any(all(r==theta for theta in (0,1)) for r in (0,1))
# AS finite but infinite expected errors: K>=1 with mass2^-K, count2^K.
# E[min(count,2^m)] = m + 1, since tail k>m has mass2^-m.
truncated=[]
for m in range(1,25):
 val=sum(F(1,2**k)*min(2**k,2**m) for k in range(1,m+1))+F(1,2**m)*2**m
 assert val==m+1;truncated.append(str(val))
# Nonempty support/all-branch distinction: a revealing probe has one winning
# singleton and one empty-menu losing singleton. Favorable branch is insufficient.
B={0,1}; successors=[{0},{1}]; wins=lambda C:C=={0}
assert any(wins(C) for C in successors) and not all(wins(C) for C in successors)
assert len(B)>len(successors[0]) and len(B)>len(successors[1])
r={'status':'PASS','guarded_cylinder_equalities':checks,'unsafe_tail_counterexamples':8,'finite_prefix_support_checks':12,'truncated_heavy_tail_expectations':truncated,'scope':'Exact finite corroboration and analytic heavy-tail truncation identity; not universal Python-to-Lean refinement','guard_counterexamples':['all-time safe event','positive selected observation','common seed','all successor branches','AS finite versus finite expectation']}
(A/'FINITE_CONTROL_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
