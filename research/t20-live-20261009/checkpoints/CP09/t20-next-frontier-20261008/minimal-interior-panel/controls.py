#!/usr/bin/env python3
"""Finite exhaustive controls; no proof assistant, simulation, or empirical data."""
from itertools import product, combinations
from collections import deque
import json, hashlib, pathlib, datetime
HERE=pathlib.Path(__file__).resolve().parent

def le(x,y): return all(a<=b for a,b in zip(x,y))
def union_costs(points):
    routes=set(sum(1<<i for i,q in enumerate(points) if le(t,q)) for t in points)
    costs={0:0}; queue=deque([0])
    while queue:
        x=queue.popleft()
        for r in routes:
            y=x|r
            if y not in costs: costs[y]=costs[x]+1;queue.append(y)
    return costs

def formula(points,pos,neg):
    ps=[points[i] for i in range(len(points)) if pos>>i&1]
    ns=[points[i] for i in range(len(points)) if neg>>i&1]
    if any(le(x,z) for x in ps for z in ns): return None
    mins=sorted(x for x in ps if not any(y!=x and le(y,x) for y in ps))
    if not mins: return 0
    p=len(mins); intervals=[]
    for z in ns:
        j=max([i+1 for i,x in enumerate(mins) if x[0]<=z[0]],default=0)
        k=min([i+1 for i,x in enumerate(mins) if x[1]<=z[1]],default=p+1)
        assert j<k
        if 1<=j<k<=p: intervals.append(set(range(j,k)))
    # Exhaustive stabbing, deliberately no greedy optimization.
    for size in range(p):
        for cuts in combinations(range(1,p),size):
            if all(set(cuts)&iv for iv in intervals): return 1+size
    raise AssertionError('No hitting set')

def exhaustive(shape, use_formula):
    pts=list(product(*(range(1,s+1) for s in shape)))
    unions=union_costs(pts); total=consistent=0; minimum_size={}; histogram={}
    for labels in product(range(3),repeat=len(pts)):
        total+=1
        pos=sum(1<<i for i,v in enumerate(labels) if v==1)
        neg=sum(1<<i for i,v in enumerate(labels) if v==2)
        best=min((c for mask,c in unions.items() if mask&pos==pos and not mask&neg),default=None)
        if use_formula:
            predicted=formula(pts,pos,neg)
            assert predicted==best,(shape,labels,predicted,best)
        if best is not None:
            consistent+=1; histogram[best]=histogram.get(best,0)+1
            size=(pos|neg).bit_count()
            minimum_size[best]=min(size,minimum_size.get(best,size))
            if use_formula and best>0: assert size>=2*best-1
    return dict(shape=shape,ternary_panels=total,consistent_panels=consistent,
                realizable_union_functions=len(unions),minimum_probe_count_by_exact_min_routes=minimum_size,
                histogram=histogram,formula_checked=use_formula)

def interval_controls():
    total=0
    for p in range(1,6):
        possible=[set(range(j,k)) for j in range(1,p) for k in range(j+1,p+1)]
        for bits in range(1<<len(possible)):
            family=[v for i,v in enumerate(possible) if bits>>i&1]
            chosen=[]
            for iv in sorted(family,key=max):
                if not set(chosen)&iv: chosen.append(max(iv))
            brute=min(len(c) for r in range(p) for c in combinations(range(1,p),r)
                      if all(set(c)&iv for iv in family))
            assert len(chosen)==brute
            total+=1
    return {'families_checked':total,'maximum_positive_antichain_size':5}

def witness3d():
    q=[(2,1,1),(1,2,1),(1,1,2)]; z=(1,1,1)
    assert all(tuple(min(a,b) for a,b in zip(x,y))==z for x,y in combinations(q,2))
    # Strictly feasible witness boxes, coordinates in sixths: (3,1,1), etc.
    thresholds=[(3,1,1),(1,3,1),(1,1,3)]
    qs=[tuple(2*v for v in x) for x in q]; zz=(2,2,2)
    assert all(any(le(t,x) for t in thresholds) for x in qs)
    assert not any(le(t,zz) for t in thresholds)
    assert all(all(a!=b for a,b in zip(t,x)) for t in thresholds for x in qs+[zz])
    return {'positive_points':['(2/3,1/3,1/3)','(1/3,2/3,1/3)','(1/3,1/3,2/3)'],
            'negative_point':'(1/3,1/3,1/3)','minimum_routes':3,'probes':4,
            'strict_threshold_witnesses':['(1/2,1/6,1/6)','(1/6,1/2,1/6)','(1/6,1/6,1/2)']}

if __name__=='__main__':
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result={'kind':'deterministic exhaustive finite controls; not kernel proof',
            'started_utc':started,
            'two_dimensional':[exhaustive((3,3),True),exhaustive((4,3),True)],
            'interval_greedy':interval_controls(),
            'three_dimensional':exhaustive((2,2,2),False),
            'three_dimensional_counterexample':witness3d(),
            'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
