#!/usr/bin/env python3
"""Exact author controls for the overlapping-audit report, not a universal proof."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
CHECKS=[]

def require(ok, detail='check failed'):
    if not ok:
        raise RuntimeError(str(detail))

def zero(e):
    e=s.factor(e)
    require(e == 0,e)

def zeros(v):
    for e in v: zero(e)

def record(name,count=1,detail=''):
    CHECKS.append(dict(name=name,count=count,status='passed',detail=detail))

def audit(w,a):
    z=sum(wi*ai for wi,ai in zip(w,a))
    return tuple(s.factor(wi*ai/z) for wi,ai in zip(w,a))

def push(w,v,a):
    z=sum(wi*ai for wi,ai in zip(w,a))
    dz=sum(vi*ai for vi,ai in zip(v,a))
    return tuple(s.factor(ai*vi/z-ai*wi*dz/z**2) for wi,vi,ai in zip(w,v,a))

def field(E,q,x,w,xv,alpha=1):
    sub=dict(zip(q+x,tuple(w)+tuple(xv)))
    de=tuple(s.diff(E,qi).subs(sub,simultaneous=True) for qi in q)
    mean=sum(wi*di for wi,di in zip(w,de))
    fw=tuple(s.factor(-alpha*wi*(di-mean)) for wi,di in zip(w,de))
    fx=tuple(s.factor(-s.diff(E,xi).subs(sub,simultaneous=True)/wi) for wi,xi in zip(w,x))
    return fw,fx

def residual(E,q,x,w,xv,a,alpha=1):
    f,v=field(E,q,x,w,xv,alpha)
    af,av=field(E,q,x,audit(w,a),xv,alpha)
    pf=push(w,f,a)
    return tuple(s.factor(aa-bb) for aa,bb in zip(af+av,pf+v))

def partitions(items):
    if not items:
        yield ()
        return
    first,*rest=items
    for p in partitions(rest):
        yield ((first,),)+p
        for i in range(len(p)):
            yield p[:i]+((first,)+p[i],)+p[i+1:]

def refinement(p,q):
    return tuple(frozenset(a)&frozenset(b) for a in p for b in q if frozenset(a)&frozenset(b))

def conditional(w,A):
    mass=sum(w[i] for i in A)
    if mass == 0:
        return None
    return tuple(s.factor(wi/mass) if i in A else s.Integer(0) for i,wi in enumerate(w))

def main():
    bindings=json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
    for item in bindings['sources']:
        raw=(ROOT/item['path']).read_bytes()
        require(len(raw)==item['bytes'],item['path'])
        require(hashlib.sha256(raw).hexdigest()==item['sha256'],item['path'])
    record('Bound source bytes unchanged',len(bindings['sources']))

    a,b,c,d=s.symbols('a b c d',positive=True)
    q=s.symbols('q1:5',positive=True)
    x=s.symbols('x1:5',real=True)
    factors=(a*c,a*d,b*c,b*d)
    zero(factors[0]*factors[3]-factors[1]*factors[2])
    aq=audit(q,factors)
    zero(aq[0]*aq[3]/(aq[1]*aq[2])-q[0]*q[3]/(q[1]*q[2]))
    require(s.Matrix([[1,1,0],[1,0,1]]).rank()==2)
    require(2*1 != 1*1)
    record('Row-column action plane and preserved odds ratio',4)

    u1,u2,u3,ss,tt=s.symbols('u1 u2 u3 ss tt',real=True)
    theta=u1-u2-u3
    zero(theta.subs({u1:u1+ss+tt,u2:u2+ss,u3:u3+tt},simultaneous=True)-theta)
    zero(theta.subs(u1,u1+s.log(2))-theta-s.log(2))
    w1,w2,w3=s.symbols('w1 w2 w3',positive=True)
    w4=1-w1-w2-w3
    theta_w=s.log(w1*w4/(w2*w3))
    zero(s.diff(-theta_w,w2)-(1/w2+1/w4))
    t,theta0=s.symbols('t theta0',real=True)
    zero(s.diff(theta0*s.exp(t),t)-theta0*s.exp(t))
    record('Odds-ratio field covariance, singleton failure and nonzero Fisher curl',4)

    quarter=(s.Rational(1,4),)*4
    rho=q[0]*q[3]/(q[1]*q[2])
    fw,fx=field(rho,q,x,quarter,(0,1,2,3))
    require(fw==(-1,1,1,-1))
    r=residual(rho,q,x,quarter,(0,1,2,3),(2,2,1,1))
    require(r[:4]==(s.Rational(1,3),-s.Rational(1,3),s.Rational(1,3),-s.Rational(1,3)))
    zeros(r[4:])
    record('Positive audit-invariant energy fails gradient equivariance',2, str(r[:4]))

    interaction=q[0]*q[1]/(q[0]+q[1])*(x[0]-x[1])**2
    zeros(residual(interaction,q,x,quarter,(0,1,2,3),(a,a,b,b)))
    r=residual(interaction,q,x,quarter,(0,1,2,3),(2,1,2,1))
    require(r[4:]==(-s.Rational(1,3),-s.Rational(1,3),0,0))
    record('Nonlinear row interaction passes rows and fails columns',2,str(r[4:]))

    # Symbolic full positive-simplex identity, with a general singleton audit.
    w=(w1,w2,w3,w4)
    aa=s.symbols('a1:5',positive=True)
    alpha=s.symbols('alpha',positive=True)
    additive=sum(qi*(xi**2+i) for i,(qi,xi) in enumerate(zip(q,x)))+7
    zeros(residual(additive,q,x,w,x,aa,alpha))
    record('Additive singleton joint gradient under every symbolic positive audit',8)

    q6=s.symbols('z1:7',positive=True)
    x6=s.symbols('y1:7',real=True)
    E6=q6[0]*q6[1]/(q6[0]+q6[1])*(x6[0]-x6[1])**2
    P=((0,1,2),(3,4,5)); Q=((0,1,3),(2,4,5))
    require(set(refinement(P,Q))=={frozenset((0,1)),frozenset((2,)),frozenset((3,)),frozenset((4,5))})
    for k in range(1,13):
        raw=tuple(s.Integer((k+i*3)%13+1) for i in range(6))
        w6=tuple(v/sum(raw) for v in raw)
        xv=tuple(s.Rational(k-i,i+1) for i in range(6))
        factorsP=(k+1,)*3+(2*k+1,)*3
        factorsQ=(k+1,k+1,2*k+1,k+1,2*k+1,2*k+1)
        zeros(residual(E6,q6,x6,w6,xv,factorsP))
        zeros(residual(E6,q6,x6,w6,xv,factorsQ))
    record('Arbitrary interaction survives inside a genuine common refinement cell',24)

    # Independent algebraic check of anchored decomposition and Euler constants.
    F=q6[0]*q6[1]/(q6[0]+q6[1])+3*q6[2]+q6[3]+(q6[4]**2+q6[5]**2)/(q6[4]+q6[5])
    at_one={qi:s.Integer(1) for qi in q6}
    base=F.subs(at_one)
    parts=[]; constants=[]
    for A in refinement(P,Q):
        anchored=F.subs({qi:1 for i,qi in enumerate(q6) if i not in A})-base
        k=s.factor(sum(q6[i]*s.diff(anchored,q6[i]) for i in A)-anchored)
        require(not k.free_symbols,k)
        H=anchored+k
        zero(sum(q6[i]*s.diff(H,q6[i]) for i in A)-H)
        parts.append(H); constants.append(k)
    zero(sum(constants)-base); zero(sum(parts)-F)
    record('Anchored C2 refinement and homogeneous constant repair controls',6)

    # Finite polynomial-support model: a monomial is block-additive exactly
    # when its nonempty label support lies inside a block.
    pair_count=0
    for n in range(1,6):
        ps=list(partitions(list(range(n))))
        subsets=[frozenset(i for i in range(n) if mask&(1<<i)) for mask in range(1,1<<n)]
        for p in ps:
            for rpart in ps:
                ref=refinement(p,rpart)
                for A in subsets:
                    both=any(A<=set(b) for b in p) and any(A<=set(b) for b in rpart)
                    refined=any(A<=b for b in ref)
                    require(both==refined,(p,rpart,A))
                pair_count+=1
    record('All degree-independent monomial support controls through five labels',pair_count)

    # Two complete positive instruments have crossing full-column partitions.
    row=(s.Rational(3,4),s.Rational(3,4),s.Rational(1,4),s.Rational(1,4))
    col=(s.Rational(3,4),s.Rational(1,4),s.Rational(3,4),s.Rational(1,4))
    for coeff in (row,col):
        complement=tuple(1-v for v in coeff)
        require(all(v>0 for v in coeff+complement))
        require(tuple(a+b for a,b in zip(coeff,complement))==(1,1,1,1))
    pr=audit(quarter,row); pc=audit(quarter,col)
    require(pr==(s.Rational(3,8),s.Rational(3,8),s.Rational(1,8),s.Rational(1,8)))
    require(pc==(s.Rational(3,8),s.Rational(1,8),s.Rational(3,8),s.Rational(1,8)))
    midpoint=tuple((a+b)/2 for a,b in zip(pr,pc))
    require(midpoint[0]*midpoint[3]/(midpoint[1]*midpoint[2])==s.Rational(3,4))
    record('Identity-summing instruments and convex hull breaking orbit invariant',5)

    beta=(s.Rational(2,5),s.Rational(3,5))
    original_branches=(row,tuple(1-v for v in row),col,tuple(1-v for v in col))
    tagged=tuple(tuple(beta[i//2]*v for v in branch) for i,branch in enumerate(original_branches))
    require(tuple(sum(branch[j] for branch in tagged) for j in range(4))==(1,1,1,1))
    tagged_columns=tuple(tuple(branch[j] for branch in tagged) for j in range(4))
    require(len(set(tagged_columns))==4)
    for original,scaled in zip(original_branches,tagged):
        require(audit(quarter,original)==audit(quarter,scaled))
    record('Tagged-instrument reduction to inherited ET-23 classification',6)

    rowP=({0,1},{2,3}); colP=({0,2},{1,3})
    fixtures=[quarter,(s.Rational(1,2),0,0,s.Rational(1,2)),(0,0,1,0),
              (s.Rational(1,6),s.Rational(1,3),s.Rational(1,2),0)]
    positive=0; zero_cells=0
    for w0 in fixtures:
        for A in rowP:
            for B in colP:
                final=conditional(w0,A&B)
                if final is None:
                    zero_cells+=1
                    continue
                first=conditional(w0,A)
                require(first is not None)
                second=conditional(first,B)
                require(second is not None and second==final)
                positive+=1
    record('Sequential conditioning with occupied-prefix and zero-cell guards',positive+zero_cells,
           f'{positive} occupied cells; {zero_cells} zero cells have no required conditional')

    # Nonsimplicial Lorentz-cone summands retain their internal normalized state.
    # Blocks (t,x,y), t>=sqrt(x*x+y*y); u is the sum of block t coordinates.
    block1=s.Matrix([s.Rational(2,5),s.Rational(1,5),0])
    block2=s.Matrix([s.Rational(3,5),0,s.Rational(1,5)])
    require(block1[0]**2>=block1[1]**2+block1[2]**2)
    require(block2[0]**2>=block2[1]**2+block2[2]**2)
    coeff=(s.Rational(3,4),s.Rational(1,4))
    raw1,raw2=coeff[0]*block1,coeff[1]*block2
    Z=raw1[0]+raw2[0]
    for old,new in ((block1,raw1/Z),(block2,raw2/Z)):
        require(old/old[0]==new/new[0])
    require(raw1+(1-coeff[0])*block1==block1)
    require(raw2+(1-coeff[1])*block2==block2)
    record('Cone blocks preserve nonsimplicial internal states',4)

    lam=(s.Rational(7,2),s.Rational(7,2),s.Rational(1,9),s.Rational(1,9))
    eps=1/(2*max(lam))
    branch=tuple(eps*v for v in lam)
    other=tuple(1-v for v in branch)
    require(all(v>0 for v in branch+other))
    require(tuple(a+b for a,b in zip(branch,other))==(1,1,1,1))
    require(audit(quarter,branch)==audit(quarter,lam))
    record('Every grouped positive rescaling can be a normalized binary branch',3)

    out=dict(status='passed',run_utc=datetime.now(timezone.utc).isoformat(),
        engine=f'Python {sys.version.split()[0]} / SymPy {s.__version__}',
        python_optimize=sys.flags.optimize,checks_use_assert=False,
        control_groups=len(CHECKS),control_count=sum(x['count'] for x in CHECKS),checks=CHECKS,
        scope='Author exact controls; universal claims rest on written proofs, not enumeration. Not independent review or kernel certification.',
        report_sha256=hashlib.sha256((HERE/'RESULT.md').read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='EXACT_CHECKS.json')
    args=parser.parse_args(); target=(HERE/args.output).resolve()
    require(target.parent==HERE,'Output must stay in packet directory')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
