#!/usr/bin/env python3
"""Exact independent table/odds and convex-conditioning controls; stdlib only."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json, hashlib

def norm(v):
    z=sum(v)
    return tuple(x/z for x in v) if z else None

def blend(v,w,t):return tuple((1-t)*a+t*b for a,b in zip(v,w))
def stats(v):
    # (theta1,A1), (theta0,A1), (theta1,A0), (theta0,A0)
    a,b,c,d=v; p=a+c; m=a+b
    return p,m,a/m if m else None,(a/p)/(b/(1-p)) if a and b and p and p<1 else None

def odds(p,r):return p*r/(1-p+p*r)
def condition(v):return norm((v[0],v[1]))
def matrix_apply(M,v):return tuple(sum(a*b for a,b in zip(row,v)) for row in M)
def run():
    K=((F(1,8),F(1,8),F(1,8),F(5,8)),(F(1,8),F(1,8),F(5,8),F(1,8)))
    L=((F(1,40),F(9,40),F(9,40),F(21,40)),(F(9,40),F(1,40),F(21,40),F(9,40)))
    for family in (K,L):
        vals=[stats(v) for v in family]
        assert sorted(v[0] for v in vals)==[F(1,4),F(3,4)]
        assert sorted(v[3] for v in vals)==[F(1,3),F(3)]
        for i in range(101):
            t=F(i,100);v=blend(*family,t);p,m,q,r=stats(v)
            assert min(v)>0 and sum(v)==1 and m==F(1,4)
            assert q==odds(p,r) and F(1,3)<=r<=3
            assert q==(F(1,2) if family==K else (1+8*t)/10)
    assert [stats(v)[2] for v in K]==[F(1,2)]*2
    assert [stats(v)[2] for v in L]==[F(1,10),F(9,10)]
    assert (odds(F(1,4),F(1,3)),odds(F(3,4),F(3)))==(F(1,10),F(9,10))
    # General vertex conditioning, including impossible vertices. Direct joint-table
    # conditioning is compared to event-mass-reweighted posterior convex mixtures.
    rows=sorted(set(norm(tuple(map(F,v))) for v in product(range(3),repeat=4) if any(v)))
    checks=0; impossible=0
    for v,w in combinations_with_replacement(rows,2):
        for j in range(11):
            t=F(j,10); mixed=blend(v,w,t); actual=condition(mixed)
            mv=sum(v[:2]);mw=sum(w[:2]);z=(1-t)*mv+t*mw
            if not z:
                assert actual is None;impossible+=1;continue
            expected=tuple(((1-t)*v[k]+t*w[k])/z for k in range(2))
            assert actual==expected
            positive=[condition(x) for x in (v,w) if sum(x[:2])]
            assert min(x[0] for x in positive)<=actual[0]<=max(x[0] for x in positive)
            # Recover a prior mixture that realizes an arbitrary desired posterior
            # vertex mixture, independently of the actual prior mixture t.
            if mv and mw:
                desired=blend(condition(v),condition(w),t)
                prior_t=(t/mw)/((1-t)/mv+t/mw)
                assert condition(blend(v,w,prior_t))==desired
            checks+=1
    # Linear-operation composition: do not project to scalar target intervals.
    M=((F(1,2),0,F(1,3),0),(0,F(1,4),0,F(2,3)))
    N=((F(2,3),F(1,5)),(F(1,3),F(4,5)))
    composition=0
    for family in (K,L):
        outs=[matrix_apply(N,matrix_apply(M,v)) for v in family]
        for j in range(21):
            t=F(j,20);v=blend(*family,t)
            direct=norm(matrix_apply(N,matrix_apply(M,v)))
            seq=norm(matrix_apply(N,norm(matrix_apply(M,v))))
            assert direct==seq==norm(blend(*outs,t))
            assert min(norm(o)[0] for o in outs)<=direct[0]<=max(norm(o)[0] for o in outs)
            composition+=1
    # Parent-supplied compact/nonpolyhedral full-support boundary.
    for j in range(1,101):
        q=F(j,200);v=q;u=q*q
        row=(u,v-u,(1-v)/2,(1-v)/2)
        assert min(row)>0 and sum(row)==1 and stats(row)[2]==q
        assert v*v<=u<=v/2
    assert condition((F(0),F(0),F(1,2),F(1,2))) is None
    bindings=json.loads(Path('INPUT_BINDINGS.json').read_text())
    for b in bindings:
        assert hashlib.sha256(Path(b['path']).read_bytes()).hexdigest()==b['sha256']
    result={'status':'PASS','normalized_joint_tables':len(rows),'positive_pair_mixture_cases':checks,'null_pair_mixture_cases':impossible,'linear_composition_cases':composition,'fixture_grid_cases':202,'input_bindings':len(bindings),'review_status':'author controls only; not independent review or kernel certification'}
    Path('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
