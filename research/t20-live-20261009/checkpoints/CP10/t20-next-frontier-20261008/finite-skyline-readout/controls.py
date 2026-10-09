#!/usr/bin/env python3
"""Exhaustive finite deterministic controls. Not empirical sampling or formal verification."""
from itertools import combinations_with_replacement, product
from fractions import Fraction
from math import ceil, log2
from pathlib import Path
import json

def minima(points):
    points=set(points)
    return sorted(p for p in points if not any(q != p and q[0]<=p[0] and q[1]<=p[1] for q in points))

def extract(points,L):
    calls=0
    def hit(a,b):
        nonlocal calls
        calls+=1
        return any(x<=a and y<=b for x,y in points)
    def first_true(hi,pred):
        lo=0 # pred(hi) is known true before entry
        while lo<hi:
            mid=(lo+hi)//2
            if pred(mid):hi=mid
            else:lo=mid+1
        return lo
    out=[]; b=L
    while b>=0:
        if not hit(L,b):break
        a=first_true(L,lambda a:hit(a,b))
        y=first_true(b,lambda y:hit(a,y))
        out.append((a,y)); b=y-1
    return out,calls

def grid_resolution(n,R,eta):
    A=Fraction((n+1)*n*R,1)/eta
    numerator=A.numerator**(n+1); denominator=A.denominator**(n+1)
    def valid(L):return L**n*denominator>=numerator
    hi=1
    while not valid(hi):hi*=2
    lo=1
    while lo<hi:
        mid=(lo+hi)//2
        if valid(mid):hi=mid
        else:lo=mid+1
    return lo

counts={}; worst={}
for L in range(1,5):
    atoms=list(product(range(L+1),repeat=2)); tested=0; maxcalls=0
    for N in range(5):
        for p in combinations_with_replacement(atoms,N):
            got,q=extract(p,L); want=minima(p)
            assert got==want,(L,p,got,want)
            K=len(want)
            assert q<=K+1+2*K*ceil(log2(L+1))
            assert K<=N
            tested+=1; maxcalls=max(maxcalls,q)
    counts[str(L)]=tested; worst[str(L)]=maxcalls
# Quantize a fine rational grid including endpoints, duplicates and coordinate ties.
checks=0; collision_free=0; strict_losses=[]
D=4; L=2
atoms=list(product(range(D+1),repeat=2))
for N in range(5):
    for p in combinations_with_replacement(atoms,N):
        qp=[((L*x+D-1)//D,(L*y+D-1)//D) for x,y in p]
        K=len(minima(p)); Kg=len(minima(qp))
        assert Kg<=K
        no_collision=all(len({q[j] for q in qp})==N for j in (0,1))
        if no_collision:
            assert Kg==K; collision_free+=1
        if Kg<K and len(strict_losses)<3:strict_losses.append({'points_scaled_by_4':p,'quantized_indices':qp,'K':K,'K_grid':Kg})
        checks+=1
resolution=[]
for n,R,eta in product(range(1,9),[1,7,100],[Fraction(1,10),Fraction(1,3)]):
    L=grid_resolution(n,R,eta); A=Fraction((n+1)*n*R,1)/eta
    assert Fraction(L**n)>=A**(n+1)
    assert L==1 or Fraction((L-1)**n)<A**(n+1)
    resolution.append({'n':n,'R':R,'eta':str(eta),'L':L})
result={'status':'PASS','kind':'exhaustive deterministic finite controls; general proofs in RESULT.md','algorithm_multiset_cases_by_L':counts,'max_actual_queries_by_L':worst,'quantization_cases':checks,'collision_free_cases':collision_free,'strict_loss_examples':strict_losses,'exact_resolution_cases':len(resolution),'exact_resolution_examples':resolution[:6]}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
