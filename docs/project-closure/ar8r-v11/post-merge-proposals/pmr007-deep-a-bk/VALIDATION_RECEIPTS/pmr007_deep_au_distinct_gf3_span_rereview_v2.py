#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, random
from pathlib import Path

P=3
SEED=2026080601
random.seed(SEED)
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")

def vadd(a,b): return tuple((x+y)%P for x,y in zip(a,b))
def smul(c,a): return tuple((c*x)%P for x in a)
def span(rows,n):
    # Incremental closure by generated subspace. Complexity depends on ambient
    # dimension, not on duplicate-row count; this is independent of the primary
    # Gaussian-elimination implementation.
    out={tuple([0]*n)}
    for row in rows:
        r=tuple(x%P for x in row)
        out={vadd(v,smul(c,r)) for v in out for c in range(P)}
    return out

def dim_of_span(S):
    size=len(S); d=0
    while size>1:
        assert size%P==0
        size//=P; d+=1
    return d

def mm(A,B):
    if not A: return []
    if not B: return [[] for _ in A]
    return [[sum(a*b for a,b in zip(row,col))%P for col in zip(*B)] for row in A]

def randmat(r,c): return [[random.randrange(P) for _ in range(c)] for __ in range(r)]

res={
 "schema":"pmr007-deep-au-distinct-gf3-span-rereview-v2-results",
 "field":"GF(3)","seed":SEED,
 "hash_check":{"checked":0,"mismatches":0},
 "sync_random_cases":0,"sync_failures":0,"strict_losses":0,
 "decomposition_random_cases":0,"decomposition_failures":0,
 "contraction_random_cases":0,"contraction_failures":0,
 "duplicate_random_cases":0,"duplicate_failures":0,
 "claim_relevance_projection_cases":0,"claim_relevance_failures":0,
 "controls":{},
}

# Frozen hashes checked independently.
hashfile=Path(__file__).parents[1]/"PMR-007_DEEP_AU_V2_FROZEN_HASHES.sha256"
import hashlib
for line in hashfile.read_text().splitlines():
    if not line.strip(): continue
    h,rel=line.split(None,1); rel=rel.strip()
    p=Path(__file__).parents[1]/rel
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    res["hash_check"]["checked"]+=1
    if got!=h: res["hash_check"]["mismatches"]+=1

# Random synchronization over different dimensions.
for _ in range(20000):
    r=random.randint(1,4); agents=random.randint(1,4); outs=random.randint(1,4)
    A=randmat(agents,r); B=randmat(outs,agents)
    EA=span(A,r); SBA=span(mm(B,A),r)
    res["sync_random_cases"]+=1
    if not SBA.issubset(EA): res["sync_failures"]+=1
    if dim_of_span(SBA)<dim_of_span(EA): res["strict_losses"]+=1

# Direct set/span computation of the exact sequence over V=F^3, W=F^2.
for _ in range(15000):
    Prows=randmat(random.randint(0,3),3)
    C=randmat(random.randint(0,3),5)
    S=span(Prows,3)
    S0={v+(0,0) for v in S}
    Q=span(C,5)
    U={vadd(x,y) for x in S0 for y in Q}
    Ucap={u for u in U if u[3:]==(0,0)}
    proj={u[3:] for u in U}
    ds=dim_of_span(S0)
    du=dim_of_span(U)
    di=dim_of_span(Ucap)
    dp=dim_of_span(proj)
    gamma_total=du-ds
    gamma_old=di-ds
    gamma_fresh=dp
    res["decomposition_random_cases"]+=1
    if gamma_total!=gamma_old+gamma_fresh or gamma_old<0 or gamma_total<gamma_fresh:
        res["decomposition_failures"]+=1

for _ in range(15000):
    agents=random.randint(1,4); r=random.randint(1,4); r2=random.randint(1,4)
    A=randmat(agents,r); R=randmat(r,r2)
    if dim_of_span(span(mm(A,R),r2))>dim_of_span(span(A,r)):
        res["contraction_failures"]+=1
    res["contraction_random_cases"]+=1

for _ in range(5000):
    agents=random.randint(1,4); r=random.randint(1,4)
    A=randmat(agents,r); i=random.randrange(agents)
    if dim_of_span(span(A+[A[i]],r))!=dim_of_span(span(A,r)):
        res["duplicate_failures"]+=1
    res["duplicate_random_cases"]+=1

# A relevance projection is another linear map and cannot raise scoped rank.
for _ in range(10000):
    agents=random.randint(1,4); raw=random.randint(1,4); rel=random.randint(1,4)
    A=randmat(agents,raw); Q=randmat(raw,rel)
    if dim_of_span(span(mm(A,Q),rel))>dim_of_span(span(A,raw)):
        res["claim_relevance_failures"]+=1
    res["claim_relevance_projection_cases"]+=1

# Mandatory controls using direct span sets.
A=[(1,0),(0,1)]; B=[(1,1),(1,1)]
res["controls"]["total_sync"]={"before":dim_of_span(span(A,2)),"after":dim_of_span(span(mm(B,A),2))}
res["controls"]["copied_root"]={"apparent_count":40,"rank":dim_of_span(span([(1,0)]*40,2))}
S=span([(1,0)],2); S0={v+(0,) for v in S}; Q=span([(0,1,0)],3); U={vadd(x,y) for x in S0 for y in Q}
res["controls"]["old_root_recovery"]={"rank_before_visible":dim_of_span(S0),"rank_after":dim_of_span(U),"fresh_projection_rank":dim_of_span({u[2:] for u in U})}
res["controls"]["independent_convergence"]={"root_span_rank":dim_of_span(span([(1,0),(0,1)],2)),"same_output_possible":True}
res["controls"]["alias_contraction"]={"displayed_rank":dim_of_span(span([(1,0),(0,1)],2)),"contracted_rank":dim_of_span(span(mm([(1,0),(0,1)],[(1,),(1,)]),1))}

fail_keys=["sync_failures","decomposition_failures","contraction_failures","duplicate_failures","claim_relevance_failures"]
res["overall"]="PASS" if res["hash_check"]["mismatches"]==0 and all(res[k]==0 for k in fail_keys) else "FAIL"
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
print(json.dumps(res,indent=2,sort_keys=True))
