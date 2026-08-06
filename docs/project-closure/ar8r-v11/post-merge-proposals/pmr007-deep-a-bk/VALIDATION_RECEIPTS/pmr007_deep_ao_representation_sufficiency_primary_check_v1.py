#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def comps(total,n):
    if n==1:
        yield (total,); return
    for i in range(total+1):
        for t in comps(total-i,n-1): yield (i,*t)

def dists(n=4,den=3):
    return [tuple(Fraction(x,den) for x in c) for c in comps(den,n)]

def partitions(n):
    # restricted growth strings, canonical labels 0..k
    out=[]
    def rec(a):
        if len(a)==n:
            out.append(tuple(a)); return
        m=max(a) if a else -1
        for x in range(m+2): rec(a+[x])
    rec([])
    return out

def push(p,t):
    k=max(t)+1 if t else 0
    return tuple(sum((p[i] for i in range(len(p)) if t[i]==y),Fraction(0)) for y in range(k))

def tv(p,q): return sum((abs(a-b) for a,b in zip(p,q)),Fraction(0))/2

def ratio(p,q,i):
    if q[i]==0:
        return 'INF' if p[i]>0 else 'ZEROZERO'
    return p[i]/q[i]

def ratio_constant(p,q,t):
    by={}
    for i,y in enumerate(t):
        if p[i]==0 and q[i]==0: continue
        r=ratio(p,q,i)
        if y in by and by[y]!=r: return False
        by[y]=r
    return True

def exact_bf(p,q,t):
    pt,qt=push(p,t),push(q,t)
    for i,y in enumerate(t):
        if p[i]==0 and q[i]==0: continue
        raw=ratio(p,q,i)
        represented='INF' if qt[y]==0 and pt[y]>0 else (pt[y]/qt[y] if qt[y]>0 else 'ZEROZERO')
        if raw!=represented: return False
    return True

def lr_partition(p,q):
    labels={}; out=[]
    for i in range(len(p)):
        r=ratio(p,q,i)
        if r not in labels: labels[r]=len(labels)
        out.append(labels[r])
    return tuple(out)

def refines(t,fine_target):
    # t refines fine_target iff same t-label implies same target label
    return all(t[i]!=t[j] or fine_target[i]==fine_target[j] for i in range(len(t)) for j in range(len(t)))

D=dists(); T=partitions(4)
counts={'distributions':len(D),'model_pairs':0,'partitions':len(T),'pair_partition_cases':0,'tv_failures':0,'bf_characterization_failures':0,'minimality_failures':0,'strict_loss_witnesses':0,'equal_experiment_discrimination_failures':0}
for p,q in product(D,repeat=2):
    counts['model_pairs']+=1
    lp=lr_partition(p,q)
    for t in T:
        counts['pair_partition_cases']+=1
        pt,qt=push(p,t),push(q,t)
        if tv(pt,qt)>tv(p,q): counts['tv_failures']+=1
        if exact_bf(p,q,t)!=ratio_constant(p,q,t): counts['bf_characterization_failures']+=1
        if exact_bf(p,q,t) and not refines(t,lp): counts['minimality_failures']+=1
        if tv(pt,qt)<tv(p,q): counts['strict_loss_witnesses']+=1
        if p==q and pt!=qt: counts['equal_experiment_discrimination_failures']+=1
claims={
 'tv_data_processing':counts['tv_failures']==0,
 'exact_bf_iff_ratio_constant_on_fibres':counts['bf_characterization_failures']==0,
 'every_exact_representation_refines_lr_partition':counts['minimality_failures']==0,
 'strict_coarsening_loss_exercised':counts['strict_loss_witnesses']>0,
 'equal_raw_experiment_remains_equal':counts['equal_experiment_discrimination_failures']==0,
}
res={'schema':'PMR007_DEEP_AO_PRIMARY_RESULTS_V1','counts':counts,'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json'); out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
