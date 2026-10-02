#!/usr/bin/env python3
"""Independent bounded exact controls; continuous proofs remain ordinary mathematics."""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from math import comb, gcd
import json

def compositions(n,k):
    if k==1:
        yield (n,); return
    for a in range(n+1):
        for rest in compositions(n-a,k-1): yield (a,)+rest

grid_cases=boundary_cases=0
for u in range(2,6):
    rows=list(compositions(3,u))
    for b in range(1,u):
        faults=list(combinations(range(u),b))
        masses=[[sum(row[i] for i in C) for C in faults] for row in rows]
        for M in range(1,min(3,b)+1):
            for inds in combinations_with_replacement(range(len(rows)),M):
                val=Q(max(min(masses[j][c] for j in inds) for c in range(len(faults))),3)
                assert val>=Q(b-M+1,u)
                grid_cases+=1
                if M==b:
                    assert val>=Q(1,u-b+1);boundary_cases+=1

def block_value(sizes,b):
    # A threshold q is attainable simultaneously precisely when the minimal
    # integer allocation ceil(q*s_j) fits the budget. Remaining faults can pad.
    candidates={Q(c,s) for s in sizes for c in range(s+1)}
    return max(q for q in candidates if sum((q.numerator*s+q.denominator-1)//q.denominator for s in sizes)<=b)

family_cases=0
for u in range(2,31):
    for b in range(1,u):
        for M in range(1,b+1):
            N=b-M+1;d=gcd(u,N)
            if d>=M:
                q=u//d;sizes=[q]*(M-1)+[(d-M+1)*q]
                assert block_value(sizes,b)==Q(N,u);family_cases+=1
        assert block_value([1]*(b-1)+[u-b+1],b)==Q(1,u-b+1)

shared_scenarios=0
for u in range(2,9):
    for b in range(1,u):
        for M in range(1,b+1):
            menus=list(combinations(range(u),M))
            for C in combinations(range(u),b):
                assert Q(sum(set(T)<=set(C) for T in menus),len(menus))==Q(comb(b,M),comb(u,M))
                shared_scenarios+=1

product_cases=0
for u in range(2,6):
    for b in range(1,u):
        for M in range(1,min(b,3)+1):
            for offset in range(3):
                rows=[tuple(Q(1+(i+j+offset)%3,sum(1+(a+j+offset)%3 for a in range(u))) for i in range(u)) for j in range(M)]
                faults=list(combinations(range(u),b));avg=Q(0);minavg=Q(0)
                for C in faults:
                    v=[sum(p[i] for i in C) for p in rows]
                    mult=Q(1)
                    for x in v:mult*=x
                    avg+=mult;minavg+=min(v)
                avg/=len(faults);minavg/=len(faults)
                representative=Q(0)
                for draws in product(range(u),repeat=M):
                    mass=Q(1)
                    for j,i in enumerate(draws):mass*=rows[j][i]
                    k=len(set(draws));representative+=mass*Q(comb(b,k),comb(u,k))
                assert avg==representative and minavg>=avg>=Q(comb(b,M),comb(u,M))
                product_cases+=1

assert block_value([4,4],3)==Q(1,4)<Q(2,7)
assert Q(comb(3,2),comb(8,2))==Q(3,28)<Q(1,4)
print(json.dumps({'status':'PASS_INDEPENDENT_EXACT_CONTROLS','rational_grid_codebooks':grid_cases,'last_boundary_grid_codebooks':boundary_cases,'arithmetic_family_cases_u_le_30':family_cases,'shared_menu_fault_scenarios_u_le_8':shared_scenarios,'independent_product_identity_cases':product_cases,'scope':'bounded exact checks; not a proof of the continuous general theorems or the open fixed-codebook frontier'},indent=2))
