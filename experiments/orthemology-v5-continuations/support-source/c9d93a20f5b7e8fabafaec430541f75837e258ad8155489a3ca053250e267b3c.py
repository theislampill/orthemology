#!/usr/bin/env python3
"""Reviewer-owned bit-matrix census, implemented without importing author code."""
import json,time
from itertools import product

def bits(x,n): return [i for i in range(n) if x>>i&1]
def survey(n,mask):
    # Each row is strict descendants. Input encodes only off-diagonal arrows.
    rows=[0]*n; k=0
    for i in range(n):
        for j in range(n):
            if i!=j:
                if mask>>k&1: rows[i]|=1<<j
                k+=1
    # An independently formulated Boolean-matrix containment criterion.
    trans=all((rows[j]&~rows[i])==0 for i in range(n) for j in bits(rows[i],n))
    reflexive=[rows[i]|(1<<i) for i in range(n)]
    incoming=[sum((bool(rows[i]>>j&1)<<i) for i in range(n)) for j in range(n)]
    roots=sum((not incoming[i])<<i for i in range(n))
    cover=[]; unique=[]; support=[]
    for x in range(n):
        cone=incoming[x]|(1<<x)
        candidates=[g for g in bits(cone,n) if cone&~reflexive[g]==0]
        cover.append(candidates)
        unique.append((cone&roots).bit_count()==1)
        support.append(all(((incoming[y]|(1<<y))&roots)!=0 for y in bits(cone,n)))
    reach=1 if n else 0
    while True:
        expanded=reach
        for i in bits(reach,n): expanded |= rows[i]|incoming[i]
        if expanded==reach:break
        reach=expanded
    conn=(reach==(1<<n)-1)
    least=[g for g in range(n) if reflexive[g]==(1<<n)-1]
    return trans,rows,roots,cover,unique,support,conn,least

def main():
    start=time.time(); census=[]
    for n in range(0,6):
        row=dict(n=n,loop_free_relations=1<<(n*(n-1)),strict_orders=0,connected=0,locally_complete=0,local_connected=0,least=0,pointwise=0)
        for mask in range(row['loop_free_relations']):
            trans,arrows,roots,cover,unique,support,conn,least=survey(n,mask)
            if not trans:continue
            row['strict_orders']+=1
            local=all(cover)
            assert local==all(unique)
            assert all(bool(cover[x])==(unique[x] and support[x]) for x in range(n))
            assert all(support), 'Every finite strict ancestral cone has root support'
            assert all(len(c)<=1 for c in cover)
            assert all(roots>>g&1 for c in cover for g in c)
            assert n==0 or (local and conn)==bool(least)
            assert len(least)<=1
            for x in range(n):
                for y in bits(arrows[x],n):
                    if cover[x] and cover[y]:assert cover[x]==cover[y]
            row['pointwise']+=n
            row['connected']+=conn; row['locally_complete']+=local
            row['local_connected']+=local and conn;row['least']+=bool(least)
        census.append(row)
    assert [r['strict_orders'] for r in census]==[1,1,3,19,219,4231]
    # Dropping transitivity: 0->1->2, no 0->2. Covers exist everywhere,
    # graph is connected, but no least ancestor. This is not a strict order.
    n=3;edges={(0,1),(1,2)};pairs=[(i,j) for i in range(n) for j in range(n) if i!=j]
    mask=sum(1<<k for k,p in enumerate(pairs) if p in edges)
    t,a,r,c,u,s,cn,l=survey(n,mask)
    assert not t and all(c) and cn and not l
    # Restriction can manufacture roothood: induced singleton {1} omits 0->1.
    ambient_root_at_1=not any(b==1 for a,b in {(0,1)})
    induced_root_at_1=not any(b==1 for a,b in set())
    assert not ambient_root_at_1 and induced_root_at_1
    return {'status':'PASS_REVIEWER_MATRIX_CENSUS', 'census':census,
      'scope':'Loop-free relations sizes 0–5, independently implemented with row bitmasks; infinite support claims rely on kernel proofs, not this census.',
      'additional_controls':{'dropping_transitivity_breaks_field_theorem':True,'non_predecessor_closed_restriction_manufactures_roothood':True},
      'elapsed_seconds':round(time.time()-start,3)}
if __name__=='__main__': print(json.dumps(main(),indent=2))
