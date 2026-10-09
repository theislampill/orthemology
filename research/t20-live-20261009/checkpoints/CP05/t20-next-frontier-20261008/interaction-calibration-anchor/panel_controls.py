#!/usr/bin/env python3
"""Certified rational interval diagnostics for the finite-panel appendix."""
from fractions import Fraction as F
from pathlib import Path
import json
families={}; max_bits=0

def check(k,b):
    if not b: raise AssertionError(k)
    families[k]=families.get(k,0)+1

def root_interval(x,d,bits):
    lo,hi=F(0),F(1)
    for _ in range(bits):
        mid=(lo+hi)/2
        if mid**d==x: return mid,mid
        if mid**d<x: lo=mid
        else: hi=mid
    return lo,hi

def det_interval(z,k,bits):
    entries=[]
    for row in z:
        er=[]
        for value in row:
            lo,hi=root_interval(value**2,2*k+1,bits)
            er.append((1-hi,1-lo))
        entries.append(er)
    a,b=entries[0];c,d=entries[1]
    return a[0]*d[0]-b[1]*c[1],a[1]*d[1]-b[0]*c[0]

def sign_at(z,k):
    global max_bits
    bits=8
    while True:
        lo,hi=det_interval(z,k,bits)
        if lo>0: max_bits=max(max_bits,bits);return 1
        if hi<0: max_bits=max(max_bits,bits);return -1
        bits*=2
        if bits>4096: raise AssertionError('control did not separate')

def recover(z):
    hi=1;cuts=1
    while sign_at(z,hi)<0: hi*=2;cuts+=1
    lo=1
    while lo<hi:
        mid=(lo+hi)//2;cuts+=1
        if sign_at(z,mid)>0: hi=mid
        else: lo=mid+1
    return lo,cuts

panels=[([F(1,4),F(3,4)],[F(1,5),F(4,5)],F(1)),
        ([F(1,9),F(4,9)],[F(1,8),F(27,64)],F(3,7)),
        ([F(1,101),F(2,101)],[F(1,103),F(2,103)],F(1,107))]
for n in range(1,17):
    for a,b,K in panels:
        z=[[(1-K*x*y)**n for y in b] for x in a]
        for k in [0,1,2,n-1,n,n+1,2*n]:
            check('half_integer_cut_sign',sign_at(z,k)==(1 if F(2*k+1,2)>n else -1))
        got,cuts=recover(z)
        check('unbounded_integer_search',got==n)
        check('finite_cut_count',cuts<=2*n+2)
        p=[[K*x*y for y in b] for x in a]
        check('true_count_rank_one',p[0][0]*p[1][1]==p[0][1]*p[1][0])
        check('relative_factors',p[1][0]/p[0][0]==a[1]/a[0] and p[0][1]/p[0][0]==b[1]/b[0])
for k in range(16):
    lo,hi=det_interval([[F(1),F(1)],[F(1),F(1)]],k,32)
    check('zero_support_not_sign_decidable',lo<=0<=hi)
# A concrete reciprocal scaling preserves a finite interior interaction panel.
a=[F(1,4),F(1,2)];b=[F(1,3),F(2,3)];lam=F(6,5)
for x in a:
    for y in b:check('finite_panel_scale_freedom',x*y==(lam*x)*(y/lam) and 0<lam*x<1 and 0<y/lam<1)
out={'status':'PASS','arithmetic':'Certified Fraction intervals and integer powers, no floating-point signs',
     'assertions':sum(families.values()),'families':families,'largest_bisection_bits_in_controls':max_bits,
     'scope':'Finite diagnostics only; measured control precision is not a uniform theorem bound.'}
p=Path(__file__).parent/'results'/'panel_controls.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
