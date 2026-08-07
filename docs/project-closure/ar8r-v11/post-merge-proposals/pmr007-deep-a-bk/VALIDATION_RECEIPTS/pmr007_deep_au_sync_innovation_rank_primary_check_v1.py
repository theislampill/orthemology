#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

OUT = Path(__file__).with_name(Path(__file__).stem + "_results.json")

def rank_mod2(M):
    A=[list(map(lambda x:x&1,row)) for row in M]
    if not A: return 0
    m=len(A); n=len(A[0]); r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(m):
            if i!=r and A[i][c]:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
        r+=1
        if r==m: break
    return r

def mat(bits, rows, cols):
    return [list(bits[i*cols:(i+1)*cols]) for i in range(rows)]

def mm(A,B):
    if not A: return []
    if not B: return [[] for _ in A]
    return [[sum(a*b for a,b in zip(row,col))%2 for col in zip(*B)] for row in A]

def stack(*Ms):
    out=[]
    for M in Ms: out.extend(M)
    return out

res={
 "schema":"pmr007-deep-au-primary-check-v1-results",
 "field":"GF(2)",
 "sync_cases":0,"sync_rank_failures":0,"strict_sync_losses":0,
 "duplicate_cases":0,"duplicate_failures":0,
 "contraction_cases":0,"contraction_failures":0,
 "innovation_cases":0,"v1_balance_failures":0,"v1_minimal_mismatches":[],
 "repaired_decomposition_failures":0,
 "fresh_rank_lower_bound_failures":0,
 "controls":{},
}

mats3=[mat(bits,3,3) for bits in itertools.product((0,1), repeat=9)]
for A in mats3:
    ra=rank_mod2(A)
    for B in mats3:
        rba=rank_mod2(mm(B,A))
        res["sync_cases"]+=1
        if rba>ra: res["sync_rank_failures"]+=1
        if rba<ra: res["strict_sync_losses"]+=1

for A in mats3:
    ra=rank_mod2(A)
    for i in range(3):
        res["duplicate_cases"]+=1
        if rank_mod2(A+[A[i]])!=ra: res["duplicate_failures"]+=1

# Exhaustive 2x2 root contractions.
mats2=[mat(bits,2,2) for bits in itertools.product((0,1), repeat=4)]
for A in mats2:
    ra=rank_mod2(A)
    for Q in mats2:
        res["contraction_cases"]+=1
        if rank_mod2(mm(A,Q))>ra: res["contraction_failures"]+=1

# Existing synchronized rows P in old root space F^2; new rows C in F^(2+1).
# Check V1 claim and the repaired quotient decomposition independently by ranks.
Ps=mats2
Cs=[mat(bits,2,3) for bits in itertools.product((0,1), repeat=6)]
for P in Ps:
    rp=rank_mod2(P)
    Pext=[row+[0] for row in P]
    for C in Cs:
        res["innovation_cases"]+=1
        U=stack(Pext,C)
        ru=rank_mod2(U)
        D=[[row[2]] for row in C]
        rd=rank_mod2(D)
        v1_pred=rp+rd
        if ru!=v1_pred:
            res["v1_balance_failures"]+=1
            if len(res["v1_minimal_mismatches"])<12:
                res["v1_minimal_mismatches"].append({"P":P,"C":C,"rank_P":rp,"rank_fresh":rd,"rank_after":ru})
        # gamma_total = gamma_old + gamma_fresh, where gamma_old is kernel
        # dimension of projection-to-fresh on U, relative to P.
        gamma_total=ru-rp
        gamma_fresh=rd
        gamma_old=(ru-rd)-rp
        if gamma_total!=gamma_old+gamma_fresh or gamma_old<0:
            res["repaired_decomposition_failures"]+=1
        if gamma_total<gamma_fresh:
            res["fresh_rank_lower_bound_failures"]+=1

A=[[1,0],[0,1]]; B=[[1,1],[1,1]]
res["controls"]["total_sync"]={"before":rank_mod2(A),"after":rank_mod2(mm(B,A))}
res["controls"]["copied_root"]={"rank":rank_mod2([[1,0],[1,0],[1,0]]),"apparent_count":3}
P=[[1,0],[0,0]]; C=[[0,1,0],[0,0,0]]
res["controls"]["old_root_recovery"]={"rank_P":rank_mod2(P),"rank_fresh":rank_mod2([[r[2]] for r in C]),"rank_after":rank_mod2([r+[0] for r in P]+C)}
res["controls"]["independent_convergence"]={"root_rank":rank_mod2([[1,0],[0,1]]),"projected_current_output_count":1}
res["controls"]["unauthenticated_alias"]={"displayed_rank":rank_mod2([[1,0],[0,1]]),"contracted_rank":rank_mod2(mm([[1,0],[0,1]],[[1],[1]]))}

res["overall"]="PASS_WITH_V1_COUNTEREXAMPLE" if all(res[k]==0 for k in ["sync_rank_failures","duplicate_failures","contraction_failures","repaired_decomposition_failures","fresh_rank_lower_bound_failures"]) and res["v1_balance_failures"]>0 else "FAIL"
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
print(json.dumps(res,indent=2,sort_keys=True))
