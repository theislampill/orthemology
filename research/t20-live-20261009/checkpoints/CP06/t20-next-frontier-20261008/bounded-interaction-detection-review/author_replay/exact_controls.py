#!/usr/bin/env python3
"""Exact interval controls for the bounded support-detection construction."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

families={};stats={'world_name_runs':0,'oracle_calls':0,'largest_precision_bits':0,'support_decisions':0}
def check(k,cond):
    if not cond:raise AssertionError(k)
    families[k]=families.get(k,0)+1

def prod(xs):
    out=F(1)
    for x in xs:out*=x
    return out

def subsets(s):
    t=s
    while True:
        yield t
        if not t:break
        t=(t-1)&s

def actual(x,spec):
    direction,k=spec
    return x**k if direction=='low' else 1-(1-x)**k

def qtrue(counts,x,cal):
    rates=[actual(z,spec) for z,spec in zip(x,cal)]
    return prod((1-prod(rates[i] for i in range(len(x)) if s>>i&1))**n for s,n in counts.items() if n)

def oracle(counts,x,cal,eps,style):
    stats['oracle_calls']+=1
    q=qtrue(counts,x,cal)
    noise=F(0) if style==0 else eps/2 if style==1 else -eps/3 if style==2 else (eps/2 if (sum(v.numerator+v.denominator for v in x)+eps.denominator)%2 else -eps/2)
    return q+noise

def interval(counts,x,cal,bits,style):
    eps=F(1,2**bits);center=oracle(counts,x,cal,eps,style)
    stats['largest_precision_bits']=max(stats['largest_precision_bits'],bits)
    return max(F(0),center-eps),min(F(1),center+eps)

def detect(counts,cal,M,style):
    r=len(cal);full=(1<<r)-1;stats['world_name_runs']+=1
    active=[]
    for s in range(1<<r):
        x=[F(bool(s>>i&1)) for i in range(r)]
        center=oracle(counts,x,cal,F(1,4),style)
        if center<F(1,2):active.append(s)
    mins=[s for s in active if not any(t!=s and t&s==t for t in active)]
    true_mins=[s for s,n in counts.items() if n and not any(t!=s and nt and t&s==t for t,nt in counts.items())]
    check('minimal_antichain',set(mins)==set(true_mins))
    if not mins:
        check('empty_inventory_branch',not any(counts.values()))
        return {s:False for s in range(1,1<<r)},set(),set()
    check('positive_case_M_nonzero',M>=1)
    A=0
    for t in mins:A|=t
    B=full^A
    for s,n in counts.items():
        if n:check('every_route_meets_A',bool(s&A))
    lam={}
    for t in mins:
        x=[F(1,2) if t>>i&1 else F(0) for i in range(r)]
        p=prod(actual(F(1,2),cal[i]) for i in range(r) if t>>i&1)
        check('minimal_factor_exact',qtrue(counts,x,cal)==(1-p)**counts[t])
        bits=2
        while True:
            lo,hi=interval(counts,x,cal,bits,style)
            if hi<1:break
            bits*=2
        ell=(1-hi)/M
        check('ceiling_product_lower_bound',0<ell<=p)
        for i in range(r):
            if t>>i&1:lam[i]=max(lam.get(i,F(0)),ell)
    for i,value in lam.items():check('rootwise_lower_bounds',0<value<=actual(F(1,2),cal[i])<1)
    for s in range(1<<r):
        x=[F(1,2) if (s&A)&(1<<i) else F(1) if s&B & (1<<i) else F(0) for i in range(r)]
        check('mixed_grid_strictly_positive',qtrue(counts,x,cal)>0)
    decisions={s:False for s in range(1,1<<r) if not s&A};bits=2
    while len(decisions)<full:
        vals={}
        for s in range(1<<r):
            x=[F(1,2) if (s&A)&(1<<i) else F(1) if (s&B)&(1<<i) else F(0) for i in range(r)]
            vals[s]=interval(counts,x,cal,bits,style)
        if any(lo<=0 for lo,hi in vals.values()):bits*=2;continue
        for s in range(1,1<<r):
            if s in decisions:continue
            numerator=[vals[t] for t in subsets(s) if (s.bit_count()-t.bit_count())%2==0]
            denominator=[vals[t] for t in subsets(s) if (s.bit_count()-t.bit_count())%2==1]
            zlo=prod(v[0] for v in numerator)/prod(v[1] for v in denominator)
            zhi=prod(v[1] for v in numerator)/prod(v[0] for v in denominator)
            d=prod(lam[i] for i in range(r) if s&A & (1<<i));threshold=1-d/2
            if zhi<threshold:decisions[s]=True
            elif zlo>threshold:decisions[s]=False
        bits*=2
        if bits>4096:raise AssertionError('unexpected finite control nonseparation')
    for s,value in decisions.items():
        check('all_support_decisions',value==bool(counts.get(s,0)));stats['support_decisions']+=1
        if s&A:
            exact_q={}
            for t in subsets(s):
                x=[F(1,2) if (t&A)&(1<<i) else F(1) if (t&B)&(1<<i) else F(0) for i in range(r)]
                exact_q[t]=qtrue(counts,x,cal)
            z=prod(exact_q[t]**(1 if (s.bit_count()-t.bit_count())%2==0 else -1) for t in subsets(s))
            p=prod(actual(F(1,2),cal[i]) for i in range(r) if (s&A)&(1<<i))
            check('double_mobius_exact',z==(1-p)**counts.get(s,0))
            d=prod(lam[i] for i in range(r) if (s&A)&(1<<i))
            check('certified_gap_alternatives',z==1 if not value else z<=1-d)
    return decisions,{i for i in range(r) if A>>i&1},{i for i in range(r) if B>>i&1}

# Complete two-root count catalogue, including no interactions and empty cases.
cal2=[ [('low',1),('low',4)], [('high',8),('low',1)] ]
for tup in product(range(3),repeat=3):
    counts=dict(enumerate(tup,1));total=sum(tup)
    for cal in cal2:
        for style in range(4):detect(counts,cal,total+2 if total else 0,style)
# Three-root binary inventories, with overlapping minimal supports and swallowed supersets.
for tup in product(range(2),repeat=7):
    counts=dict(enumerate(tup,1));total=sum(tup)
    for style in [0,3]:detect(counts,[('low',1),('low',3),('high',6)],total if total else 0,style)
# Four-root fixtures include tiny A rates and very small positive raw probabilities.
fixtures=[{1:1,3:1,5:2,15:1},{3:2,6:1,7:2,15:1},{1:3,2:2,4:2,8:2,15:1},{3:1},{1:2},{15:1}]
for counts in fixtures:
    for cal in [[('low',32),('low',7),('high',3),('low',2)],[('high',16),('high',8),('high',3),('high',2)]]:
        for style in range(4):detect(counts,cal,sum(counts.values())+3,style)

# Exact total-ceiling count fibres and realizability of the unary gauge.
for fixed in range(5):
    for k in range(1,4):
        for slack in range(4):
            budget=k+slack;M=fixed+budget
            tuples=[v for v in product(range(1,budget+1),repeat=k) if sum(v)<=budget]
            check('count_fibre_nonempty',len(tuples)>=1)
            check('count_fibre_collapse',(len(tuples)==1)==(budget==k))
            if budget>k:
                for i in range(k):check('each_isolated_count_ambiguous',len({v[i] for v in tuples})>=2)
            original=[1 for _ in range(k)]  # This baseline also satisfies the same total ceiling.
            for v in tuples:
                check('joint_total_ceiling',fixed+sum(v)<=M)
                t=[F(i+1,i+3) for i in range(k)]
                old=prod((t[i]**v[i])**original[i] for i in range(k))
                new=prod((t[i]**original[i])**v[i] for i in range(k))
                check('isolated_unary_full_power_identity',old==new)
# A false total ceiling can produce a false lower bound. It is an external premise.
t=F(9,10);N=10;q=t**N;qplus=F(1,2);false_ell=1-qplus
check('false_ceiling_invalidates_gap',q<qplus and false_ell>1-t)

out={'status':'PASS','arithmetic':'Exact Fraction probability intervals, rational products and quotients; no sampled data or floating-point decisions',
     'assertions':sum(families.values()),'families':families,'statistics':stats,
     'scope':'Finite support-detector and fibre diagnostics only; imported sign lemmas are credited to their own stages and proofs establish all-name termination.'}
p=Path(__file__).parent/'results'/'exact_controls.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
