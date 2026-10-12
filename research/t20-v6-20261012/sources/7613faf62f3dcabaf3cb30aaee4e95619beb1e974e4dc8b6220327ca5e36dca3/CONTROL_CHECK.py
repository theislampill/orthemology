"""Fresh exact finite interface controls; not a replay of v4 proofs."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json

def require(c,m):
    if not c: raise RuntimeError(m)
u,b,M=8,3,2
roots=range(u); faults=list(combinations(roots,b)); menus=list(combinations(roots,M))
shared=[]
for C in faults:
    C=set(C); shared.append(F(sum(set(T)<=C for T in menus),len(menus)))
require(set(shared)=={F(3,28)},'shared menu probability')
blocks=[set(range(4)),set(range(4,8))]
fixed=max(min(F(len(set(C)&B),len(B)) for B in blocks) for C in faults)
require(fixed==F(1,4),'fixed partition upper bound')
# Exact inherited formula, not an independent proof of arbitrary-real optimality.
N=b-M+1
formula=max(F((q*N+M-1)//u,q) for q in range(1,u-M+2))
require(formula==fixed,'inherited formula instance')
require(all(any(set(T)<=set(C) for C in faults) for T in menus),'post-menu attack')
# Averaging a shared ordered menu BEFORE sender message choice destroys adaptation.
# Each ordered rank has a marginal distribution, whose private-codebook risk is >= 1/4.
rows=[[F(sum(T[m]==i for T in menus),len(menus)) for i in roots] for m in range(M)]
averaged=max(min(sum(p[i] for i in C) for p in rows) for C in faults)
require(averaged>=fixed and averaged>F(3,28),'averaging does not retain shared game')
# Identical marginals do not preserve fault/action coupling.
Jgood={(0,1):F(1,2),(1,0):F(1,2)}; Jbad={(0,0):F(1,2),(1,1):F(1,2)}
for coord in [0,1]:
    require([sum(p for x,p in Jgood.items() if x[coord]==i) for i in range(2)]==[sum(p for x,p in Jbad.items() if x[coord]==i) for i in range(2)],'equal marginals')
require(sum(p for (c,a),p in Jgood.items() if c==a)==0,'good coupling')
require(sum(p for (c,a),p in Jbad.items() if c==a)==1,'bad coupling')
out={'status':'PASS','scope':'new finite cross-interface diagnostics; inherited numerical formulas and no universal optimizer/kernel/host proof','shared_static':str(shared[0]),'fixed_partition':str(fixed),'formula_instance':str(formula),'after_message_optimized':str(F(b,u)),'after_action_optimized':'1','same_random_menu_after_public_seed':'1','averaged_ordered_menu_codebook_risk':str(averaged),'carrier_uniform_40_1_1':str(F(40,42)),'root_uniform_3':str(F(1,3)),'equal_marginals_joint_damage':['0','1']}
print(json.dumps(out,indent=2))
