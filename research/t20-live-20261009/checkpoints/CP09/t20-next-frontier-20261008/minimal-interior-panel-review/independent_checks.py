#!/usr/bin/env python3
"""Independent exhaustive discrete semantics vs. claimed interval formula."""
from itertools import product
from functools import lru_cache
from random import Random

def le(a,b): return all(x<=y for x,y in zip(a,b))
def brute(P,N):
    if not P:return 0
    # Any covering route can be replaced by the coordinatewise minimum
    # of its covered positives. Enumerate ALL such corners, not partitions.
    corners=set()
    for mask in range(1,1<<len(P)):
        corners.add(tuple(min(P[i][j] for i in range(len(P)) if mask>>i&1) for j in range(len(P[0]))))
    masks=set()
    for c in corners:
        if not any(le(c,q) for q in N):
            masks.add(sum(1<<i for i,p in enumerate(P) if le(c,p)))
    full=(1<<len(P))-1
    @lru_cache(None)
    def solve(remaining):
        if not remaining:return 0
        first=remaining&-remaining
        return min((1+solve(remaining&~m) for m in masks if m&first),default=float("inf"))
    return solve(full)

def interval(P,N):
    if any(le(p,q) for p in P for q in N):return float("inf")
    P=sorted(p for p in P if not any(q!=p and le(q,p) for q in P))
    k=len(P)
    if not k:return 0
    intervals=[]
    for a,b in N:
        L=max([i for i,(x,y) in enumerate(P,1) if x<=a],default=0)
        R=min([i for i,(x,y) in enumerate(P,1) if y<=b],default=k+1)
        assert L<R
        if L and R<=k:intervals.append(set(range(L,R)))
    return 1+min(mask.bit_count() for mask in range(1<<max(k-1,0)) if all(any(mask>>(i-1)&1 for i in I) for I in intervals))

def check(P,N):
    b=brute(P,N); a=interval(P,N)
    assert a==b,(P,N,a,b)
    if b<100 and b:
        assert len(P)+len(N)>=2*b-1,(P,N,b)

G=list(product(range(3),repeat=2)); count=0
for labels in product(range(3),repeat=len(G)):
    P=[p for p,t in zip(G,labels) if t==1]
    N=[p for p,t in zip(G,labels) if t==2]
    check(P,N);count+=1
print('PASS exhaustive 3x3 absent/positive/negative panels:',count)
rng=Random(20261008); G=list(product(range(4),repeat=2))
for _ in range(1500):
    labels=[rng.randrange(3) for _ in G]
    check([p for p,t in zip(G,labels) if t==1],[p for p,t in zip(G,labels) if t==2])
print('PASS seeded random 4x4 panels: 1500')
for m in range(1,9):
    P=[(i,m+1-i) for i in range(1,m+1)]
    N=[(i,m-i) for i in range(1,m)]
    assert brute(P,N)==interval(P,N)==m
print('PASS sharp staircases: m=1,...,8')
P=[(2,1,1),(1,2,1),(1,1,2)];N=[(1,1,1)]
assert brute(P,N)==3
print('PASS 3D failure of universal 2m-1: three routes required by four queries')
