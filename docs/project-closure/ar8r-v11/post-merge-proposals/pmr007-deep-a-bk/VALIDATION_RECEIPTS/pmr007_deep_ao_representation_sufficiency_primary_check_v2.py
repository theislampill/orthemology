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

def dists(n=4,den=3): return [tuple(Fraction(x,den) for x in c) for c in comps(den,n)]
def partitions(n):
    out=[]
    def rec(a):
        if len(a)==n: out.append(tuple(a)); return
        m=max(a) if a else -1
        for x in range(m+2): rec(a+[x])
    rec([]); return out

def support(p,q): return tuple(i for i in range(len(p)) if p[i]+q[i]>0)
def relabel_on_support(t,s):
    labels={}; out=[]
    for i in s:
        if t[i] not in labels: labels[t[i]]=len(labels)
        out.append(labels[t[i]])
    return tuple(out)
def restrict(p,s): return tuple(p[i] for i in s)
def push(p,t):
    k=max(t)+1 if t else 0
    return tuple(sum((p[i] for i in range(len(p)) if t[i]==y),Fraction(0)) for y in range(k))
def tv(p,q): return sum((abs(a-b) for a,b in zip(p,q)),Fraction(0))/2
def ratio(p,q,i): return 'INF' if q[i]==0 and p[i]>0 else p[i]/q[i]
def ratio_constant(p,q,t):
    by={}
    for i,y in enumerate(t):
        r=ratio(p,q,i)
        if y in by and by[y]!=r: return False
        by[y]=r
    return True
def exact_bf(p,q,t):
    pt,qt=push(p,t),push(q,t)
    for i,y in enumerate(t):
        raw=ratio(p,q,i)
        represented='INF' if qt[y]==0 and pt[y]>0 else pt[y]/qt[y]
        if raw!=represented: return False
    return True
def lr_partition(p,q):
    labels={}; out=[]
    for i in range(len(p)):
        r=ratio(p,q,i)
        if r not in labels: labels[r]=len(labels)
        out.append(labels[r])
    return tuple(out)
def refines(t,target): return all(t[i]!=t[j] or target[i]==target[j] for i in range(len(t)) for j in range(len(t)))

D=dists(); T=partitions(4)
counts={'distributions':len(D),'model_pairs':0,'partitions':len(T),'support_partition_cases':0,'tv_failures':0,'bf_characterization_failures':0,'minimality_failures':0,'strict_loss_witnesses':0,'null_point_cases_removed':0}
for p0,q0 in product(D,repeat=2):
    counts['model_pairs']+=1
    s=support(p0,q0); p=restrict(p0,s); q=restrict(q0,s)
    if len(s)<4: counts['null_point_cases_removed']+=1
    lp=lr_partition(p,q)
    seen=set()
    for t0 in T:
        t=relabel_on_support(t0,s)
        if t in seen: continue
        seen.add(t); counts['support_partition_cases']+=1
        pt,qt=push(p,t),push(q,t)
        if tv(pt,qt)>tv(p,q): counts['tv_failures']+=1
        if exact_bf(p,q,t)!=ratio_constant(p,q,t): counts['bf_characterization_failures']+=1
        if exact_bf(p,q,t) and not refines(t,lp): counts['minimality_failures']+=1
        if tv(pt,qt)<tv(p,q): counts['strict_loss_witnesses']+=1
claims={
 'tv_data_processing':counts['tv_failures']==0,
 'exact_bf_iff_ratio_constant_on_support_fibres':counts['bf_characterization_failures']==0,
 'every_exact_support_representation_refines_lr_partition':counts['minimality_failures']==0,
 'strict_coarsening_loss_exercised':counts['strict_loss_witnesses']>0,
 'null_support_repair_exercised':counts['null_point_cases_removed']>0,
}
res={'schema':'PMR007_DEEP_AO_PRIMARY_RESULTS_V2','counts':counts,'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json'); out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
