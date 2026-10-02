#!/usr/bin/env python3
"""Exact Fraction controls; theorem proofs remain in POSITIVE_ERROR_FRONTIERS.md."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd
from pathlib import Path
import json, random
HERE=Path(__file__).resolve().parent

def mass(p,C): return sum((p[i] for i in C),F())
def fixed_risk(ps,b):
    u=len(ps[0])
    return max(min(mass(p,C) for p in ps) for C in combinations(range(u),b))
def block_codebook(sizes):
    u=sum(sizes); start=0; out=[]
    for s in sizes:
        out.append(tuple(F(1,s) if start<=i<start+s else F() for i in range(u)))
        start+=s
    return out

def hyper_ratio(u,b,m):
    return F(comb(b,m),comb(u,m)) if m<=b else F()

def integer_partitions(total,parts,minimum=1):
    if parts==1:
        if total>=minimum: yield (total,)
    else:
        for first in range(minimum,total//parts+1):
            for rest in integer_partitions(total-first,parts-1,first):
                yield (first,)+rest

cases=[]
for u,b,m,sizes in [(8,3,2,(4,4)),(9,4,2,(3,6)),(11,5,2,(3,8)),(9,4,3,(1,4,4))]:
    value=fixed_risk(block_codebook(sizes),b)
    proposed=F(b-m+1,u-m+1)
    assert value<proposed
    cases.append({'u':u,'b':b,'M':m,'blocks':sizes,'exact_constructive_risk':str(value),
        'singleton_construction':str(proposed),'LP_lower':str(F(b-m+1,u))})
assert cases[0]['exact_constructive_risk']=='1/4'
assert cases[1]['exact_constructive_risk']=='1/3'

family=[]
for u in range(2,14):
    for b in range((u-1)//2+1): # inherited u>=2b+1
        for m in range(1,b+2):
            N=b-m+1; d=gcd(u,N)
            if N==0:
                sizes=(1,)*(m-1)+(u-m+1,)
            elif d>=m:
                q=u//d
                sizes=(q,)*(m-1)+((d-m+1)*q,)
            else: continue
            value=fixed_risk(block_codebook(sizes),b)
            assert value==F(N,u)
            family.append({'u':u,'b':b,'M':m,'blocks':sizes,'risk':str(value)})

public_cases=0; public_scenarios=0
for u in range(2,10):
    for b in range(min(4,u-1)+1):
        for m in range(1,b+2):
            menus=list(combinations(range(u),m))
            target=hyper_ratio(u,b,m)
            for Ctuple in combinations(range(u),b):
                C=set(Ctuple)
                # An actual informed sender selects first intact menu root, if any.
                failures=0
                for T in menus:
                    chosen=next((r for r in T if r not in C),T[0])
                    failures += int(chosen in C)
                observed=F(failures,len(menus))
                assert observed==target
                public_scenarios+=1
            public_cases+=1

rng=random.Random(2601002)
product_controls=0; lp_regressions=0
for u,b,m in [(5,2,2),(7,3,2),(7,3,3),(8,3,2),(9,4,3),(6,2,3)]:
    cs=list(combinations(range(u),b))
    for repetition in range(8):
        ps=[]
        for _ in range(m):
            raw=[rng.randrange(8) for _ in range(u)]
            if not any(raw):raw[0]=1
            ps.append(tuple(F(w,sum(raw)) for w in raw))
        avg_product=F(); avg_min=F()
        for C in cs:
            losses=[mass(p,C) for p in ps]
            prod=F(1)
            for loss in losses:prod*=loss
            assert min(losses)>=prod
            avg_product+=prod/F(len(cs));avg_min+=min(losses)/F(len(cs))
        representative_average=F()
        for representatives in product(range(u),repeat=m):
            probability=F(1)
            for j,i in enumerate(representatives):probability*=ps[j][i]
            r=len(set(representatives))
            inclusion=hyper_ratio(u,b,r)
            representative_average+=probability*inclusion
        assert representative_average==avg_product
        assert avg_min>=avg_product>=hyper_ratio(u,b,m)
        assert fixed_risk(ps,b)>=F(b-m+1,u)
        product_controls+=1;lp_regressions+=1

# Exact shared/private separation, and a deletion of the pre-seed static adversary.
assert F(1,4)>hyper_ratio(8,3,2)==F(3,28)
# If the adversary may see the random menu and choose C afterwards, include it.
for T in combinations(range(8),2):
    C=set(T)
    C.add(next(i for i in range(8) if i not in C))
    assert all(i in C for i in T)

# Duplicate message choices do not increase the codebook's action diversity.
ps=block_codebook((4,4));assert fixed_risk(ps+[ps[0]],3)==fixed_risk(ps,3)
# Averaging a public random menu before informed message selection loses conditioning.
# For two uniformly ordered distinct roots, each fixed message marginal is uniform.
uniform=tuple(F(1,8) for _ in range(8))
assert fixed_risk([uniform,uniform],3)==F(3,8)>F(3,28)

# Constructive lower-bound witness for M=b, including mass-one residual rows.
def boundary_witness(ps):
    m=len(ps);u=len(ps[0]);t=F(1,u-m+1)
    if m==1:
        return {max(range(u),key=lambda i:ps[0][i])}
    for row,p in enumerate(ps):
        for i,a in enumerate(p):
            if a>=t:
                remaining=[j for j in range(u) if j!=i];reduced=[]
                for h,q in enumerate(ps):
                    if h==row:continue
                    a=q[i]
                    reduced.append(tuple(F(1,u-1) for _ in remaining) if a==1 else
                        tuple(q[j]/(1-a) for j in remaining))
                return {i}|{remaining[j] for j in boundary_witness(reduced)}
    return set(range(m))

boundary_rng=random.Random(819);boundary_controls=0;boundary_upper_controls=0
for u in range(2,14):
    for m in range(1,u):
        for repetition in range(20):
            ps=[]
            for _ in range(m):
                raw=[boundary_rng.randrange(8) for _ in range(u)]
                if not any(raw):raw[0]=1
                ps.append(tuple(F(w,sum(raw)) for w in raw))
            C=boundary_witness(ps);t=F(1,u-m+1)
            assert len(C)<=m and all(mass(p,C)>=t for p in ps)
            boundary_controls+=1
        sizes=(1,)*(m-1)+(u-m+1,)
        assert fixed_risk(block_codebook(sizes),m)==F(1,u-m+1)
        boundary_upper_controls+=1
# Deliberately duplicated point masses force a normalized row with a=1.
ps=[(F(1),F(),F(),F()),(F(1),F(),F(),F())]
C=boundary_witness(ps)
assert all(mass(p,C)>=F(1,3) for p in ps)

report={'status':'PASS','exact_constructive_counterexamples':cases,
 'boundary_induction_controls':boundary_controls,'boundary_upper_controls':boundary_upper_controls,
 'mass_one_residual_control':True,
 'arithmetic_family_cases':len(family),'arithmetic_family':family,
 'public_menu_parameter_cases':public_cases,'public_menu_fault_scenarios':public_scenarios,
 'representative_product_controls':product_controls,'LP_bound_finite_regressions':lp_regressions,
 'private_shared_separation':{'u':8,'b':3,'M':2,'fixed_exact':'1/4','shared_exact':'3/28'},
 'guard_controls':{'post_seed_adversary_forces_one':True,'duplicated_messages_do_not_help':True,
 'averaged_codebook_loses_sender_conditioning':True},
 'proof_ceiling':'Exact finite controls; general ordinary proofs in main note, no numerical optimum claims'}
(HERE/'EXACT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('arithmetic_family',)},indent=2))
