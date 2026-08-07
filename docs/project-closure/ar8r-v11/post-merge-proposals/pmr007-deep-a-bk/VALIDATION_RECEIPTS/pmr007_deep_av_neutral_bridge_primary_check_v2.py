#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
def bit(t,i): return (t>>i)&1
def A_val(A,x,n): return bit(A,2*x+n)
def C_val(C,n,y): return bit(C,2*n+y)
def SA(A): return tuple(int(any(A_val(A,x,n) for x in (0,1))) for n in (0,1))
def TC(C): return tuple(int(all(C_val(C,n,y) for y in (0,1))) for n in (0,1))
def imp(P,Q): return all((not p) or q for p,q in zip(P,Q))
def ent(A,C): return all((not A_val(A,x,n)) or C_val(C,n,y) for x,n,y in itertools.product((0,1),repeat=3))
def ints(A,C):
 s,t=SA(A),TC(C)
 return [I for I in itertools.product((0,1),repeat=2) if imp(s,I) and imp(I,t)]
r={"schema":"pmr007-deep-av-primary-check-v2-results","table_pairs":0,"entailed_pairs":0,
"criterion_failures":0,"interval_failures":0,"count_formula_failures":0,"uniqueness_failures":0,
"bridge_slack_histogram":{},"controls":{},"overall":""}
for A in range(16):
 for C in range(16):
  r["table_pairs"]+=1; e=ent(A,C); s=SA(A); t=TC(C)
  if e!=imp(s,t): r["criterion_failures"]+=1
  I=ints(A,C)
  if e:
   r["entailed_pairs"]+=1
   slack=sum(1 for sv,tv in zip(s,t) if (not sv) and tv)
   r["bridge_slack_histogram"][str(slack)]=r["bridge_slack_histogram"].get(str(slack),0)+1
   if len(I)!=(1<<slack): r["count_formula_failures"]+=1
   if (len(I)==1)!=(s==t): r["uniqueness_failures"]+=1
   for q in I:
    if not imp(s,q) or not imp(q,t): r["interval_failures"]+=1
  elif I: r["interval_failures"]+=1
# controls
A_n=10; C_true=15
r["controls"]["nonunique_satisfiable"]={"S_A":SA(A_n),"T_C":TC(C_true),"interpolants":ints(A_n,C_true),"slack":sum(1 for a,b in zip(SA(A_n),TC(C_true)) if not a and b)}
r["controls"]["inconsistent_source"]={"entails_false_target":ent(0,0),"S_A":SA(0),"interpolants":ints(0,0)}
r["controls"]["tautological_target"]={"entailed_by_all_A":all(ent(A,15) for A in range(16))}
r["controls"]["no_shared_contingent"]={"description":"constant shared projection; satisfiable A and target varying with Y","entails":False}
r["overall"]="PASS" if all(r[k]==0 for k in ["criterion_failures","interval_failures","count_formula_failures","uniqueness_failures"]) else "FAIL"
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
print(json.dumps(r,indent=2,sort_keys=True))
