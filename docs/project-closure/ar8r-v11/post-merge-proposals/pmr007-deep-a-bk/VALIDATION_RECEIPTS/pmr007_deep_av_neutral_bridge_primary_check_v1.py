#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")

# one Boolean X, one N, one Y. A table indexed (x,n); C indexed (n,y).
def bit(table,idx): return (table>>idx)&1
def A_val(A,x,n): return bit(A,2*x+n)
def C_val(C,n,y): return bit(C,2*n+y)
def SA_table(A):
    return tuple(int(any(A_val(A,x,n) for x in (0,1))) for n in (0,1))
def TC_table(C):
    return tuple(int(all(C_val(C,n,y) for y in (0,1))) for n in (0,1))
def entails_AC(A,C):
    return all((not A_val(A,x,n)) or C_val(C,n,y) for x,n,y in itertools.product((0,1),repeat=3))
def table_entails(P,Q): return all((not p) or q for p,q in zip(P,Q))
def interp_tables(A,C):
    SA=SA_table(A); TC=TC_table(C); out=[]
    for I in itertools.product((0,1),repeat=2):
        if table_entails(SA,I) and table_entails(I,TC): out.append(I)
    return out

r={"schema":"pmr007-deep-av-primary-check-v1-results","table_pairs":0,"criterion_failures":0,
   "entailed_pairs":0,"nonentailed_pairs":0,"unique_bridge_pairs":0,"multiple_bridge_pairs":0,
   "v1_uniqueness_failures":0,"examples":{},"overall":""}
for A in range(16):
  for C in range(16):
    r["table_pairs"]+=1
    ent=entails_AC(A,C)
    criterion=table_entails(SA_table(A),TC_table(C))
    if ent!=criterion: r["criterion_failures"]+=1
    if ent:
      r["entailed_pairs"]+=1
      ints=interp_tables(A,C)
      if len(ints)==1: r["unique_bridge_pairs"]+=1
      if len(ints)>1:
        r["multiple_bridge_pairs"]+=1
        if SA_table(A) in ints: r["v1_uniqueness_failures"]+=1
        if "multiple_interpolants" not in r["examples"]:
          r["examples"]["multiple_interpolants"]={"A_table":A,"C_table":C,"S_A":SA_table(A),"T_C":TC_table(C),"interpolants":ints}
    else: r["nonentailed_pairs"]+=1

# Explicit controls.
# A=n (independent of x), C=true: S_A=n, T_C=true, so n and true are both interpolants.
A_n=sum((n<< (2*x+n)) for x in (0,1) for n in (0,1))
C_true=15
r["examples"]["satisfiable_nonunique"]={"A_table":A_n,"C_table":C_true,"S_A":SA_table(A_n),"T_C":TC_table(C_true),"interpolants":interp_tables(A_n,C_true)}
# No shared N effectively: use constant projection. Satisfiable A and contingent C cannot entail for all y.
A_true=15; C_y=sum((y<<(2*n+y)) for n in (0,1) for y in (0,1))
r["examples"]["no_shared_contingent"]={"entails":entails_AC(A_true,C_y)}
r["examples"]["inconsistent_source"]={"A_table":0,"C_table":0,"entails":entails_AC(0,0),"interpolants":interp_tables(0,0)}
r["overall"]="PASS_WITH_V1_NONUNIQUENESS_COUNTEREXAMPLE" if r["criterion_failures"]==0 and r["v1_uniqueness_failures"]>0 else "FAIL"
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
print(json.dumps(r,indent=2,sort_keys=True))
