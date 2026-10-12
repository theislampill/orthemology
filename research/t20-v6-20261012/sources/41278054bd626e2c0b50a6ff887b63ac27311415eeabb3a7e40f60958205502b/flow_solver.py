"""Exact rational vertex enumeration for P02's row-polytope correspondence.
No floating point, numerical tolerances, or canonical adoption. Exponential
search is intentional: this is a terminating feasibility construction.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
from typing import Sequence

Constraint=tuple[tuple[Q,...],Q]

def _q(x)->Q:
    if type(x) is int:return Q(x)
    if type(x) is Q:return x
    raise TypeError('Only integers or exact fractions; floats/booleans refused')

def rref(eqs:Sequence[Constraint],dim:int)->tuple[list[list[Q]],list[int]]|None:
    a=[list(v)+[c] for v,c in eqs];piv=[];row=0
    for col in range(dim):
        k=next((i for i in range(row,len(a)) if a[i][col]),None)
        if k is None:continue
        a[row],a[k]=a[k],a[row];scale=a[row][col];a[row]=[v/scale for v in a[row]]
        for i in range(len(a)):
            if i!=row:
                scale=a[i][col];a[i]=[v-scale*w for v,w in zip(a[i],a[row])]
        piv.append(col);row+=1
    if any(not any(r[:dim]) and r[-1] for r in a):return None
    return a[:row],piv

def vertex(dim:int,eqs:Sequence[Constraint],ineqs:Sequence[Constraint])->tuple[Q,...]|None:
    """Returns a vertex if it exists. Completeness requires a bounded polyhedron."""
    if type(dim) is not int or dim<1:raise ValueError('Positive dimension')
    def norm(cs):
        out=[]
        for v,c in cs:
            if len(v)!=dim:raise ValueError('Constraint dimension')
            out.append((tuple(_q(t) for t in v),_q(c)))
        return out
    eqs=norm(eqs);ineqs=norm(ineqs);base=rref(eqs,dim)
    if base is None:return None
    independent=[(tuple(r[:dim]),r[-1]) for r in base[0]];rank=len(base[1])
    for active in combinations(ineqs,dim-rank):
        ans=rref(independent+list(active),dim)
        if ans is None or len(ans[1])!=dim:continue
        x=[Q(0)]*dim
        for row,p in zip(ans[0],ans[1]):x[p]=row[-1]
        if all(sum(a*b for a,b in zip(v,x))==c for v,c in eqs) and all(sum(a*b for a,b in zip(v,x))<=c for v,c in ineqs):return tuple(x)
    return None

def simplex_constraints(m:int)->tuple[list[Constraint],list[Constraint]]:
    eq=[(tuple(Q(1) for _ in range(m)),Q(1))]
    le=[(tuple(Q(-int(i==j)) for j in range(m)),Q(0)) for i in range(m)]
    return eq,le

def solve(rows:Sequence[Sequence[Constraint]])->dict:
    """rows[i] gives A_i r <= b_i in the probability simplex.
    Empty row sets are explicitly REFUSED even if their stationary mass is zero.
    """
    m=len(rows)
    if not m:raise ValueError('At least one row')
    normal=[];witness=[];eq,le=simplex_constraints(m)
    for constraints in rows:
        cs=[]
        for a,b in constraints:
            if len(a)!=m:raise ValueError('Row constraint dimension')
            cs.append((tuple(_q(x) for x in a),_q(b)))
        v=vertex(m,eq,le+cs)
        if v is None:raise ValueError('Empty row polytope: nonempty-value hypothesis fails')
        normal.append(cs);witness.append(v)
    dim=m*m
    eqs=[(tuple(Q(1) for _ in range(dim)),Q(1))]
    for k in range(m):
        eqs.append((tuple(Q(int(i==k)-int(j==k)) for i in range(m) for j in range(m)),Q(0)))
    ineq=[(tuple(Q(-int(k==l)) for l in range(dim)),Q(0)) for k in range(dim)]
    for i,cs in enumerate(normal):
        for a,b in cs:
            ineq.append((tuple(a[j]-b if k==i else Q(0) for k in range(m) for j in range(m)),Q(0)))
    flow=vertex(dim,eqs,ineq)
    if flow is None:raise RuntimeError('Feasibility theorem violated; do not return a fabricated solution')
    f=tuple(tuple(flow[i*m+j] for j in range(m)) for i in range(m));p=tuple(sum(f[i]) for i in range(m))
    selected=tuple(tuple(x/p[i] for x in f[i]) if p[i] else witness[i] for i in range(m))
    result={'probabilities':p,'flow':f,'rows':selected,'input_rows':tuple(tuple(cs) for cs in normal)}
    if not verify(result,normal):raise RuntimeError('Independent exact result check failed')
    return result

def verify(r:dict,expected_rows:Sequence[Sequence[Constraint]]|None=None)->bool:
    """Check a self-contained exact result; optionally bind external row inputs.

    Missing/ragged/inexact fields are refused. Without expected_rows this checks
    only the constraints recorded in r, not some unstated external input identity.
    """
    try:
        if not isinstance(r,dict):return False
        p,f,rows,cs=(r[k] for k in ('probabilities','flow','rows','input_rows'))
        if not isinstance(p,(tuple,list)) or not p:return False
        m=len(p)
        if any(not isinstance(t,(tuple,list)) or len(t)!=m for t in (f,rows,cs)):return False
        if any(not isinstance(t,(tuple,list)) or len(t)!=m for t in tuple(f)+tuple(rows)):return False
        p=tuple(_q(x) for x in p)
        f=tuple(tuple(_q(x) for x in line) for line in f)
        rows=tuple(tuple(_q(x) for x in line) for line in rows)
        def constraints(data):
            if not isinstance(data,(tuple,list)) or len(data)!=m:raise ValueError('Row count')
            answer=[]
            for line in data:
                if not isinstance(line,(tuple,list)):raise ValueError('Finite constraint row')
                parsed=[]
                for item in line:
                    if not isinstance(item,(tuple,list)) or len(item)!=2:raise ValueError('Constraint pair')
                    a,b=item
                    if not isinstance(a,(tuple,list)) or len(a)!=m:raise ValueError('Constraint dimension')
                    parsed.append((tuple(_q(x) for x in a),_q(b)))
                answer.append(tuple(parsed))
            return tuple(answer)
        cs=constraints(cs)
        if expected_rows is not None and cs!=constraints(expected_rows):return False
        if sum(p)!=1 or any(x<0 for x in p):return False
        for i in range(m):
            if sum(rows[i])!=1 or any(x<0 for x in rows[i]):return False
            if any(sum(a[j]*rows[i][j] for j in range(m))>b for a,b in cs[i]):return False
            if any(f[i][j]!=p[i]*rows[i][j] for j in range(m)):return False
        return all(sum(p[i]*rows[i][j] for i in range(m))==p[j] for j in range(m))
    except (TypeError,ValueError,KeyError,IndexError):
        return False
