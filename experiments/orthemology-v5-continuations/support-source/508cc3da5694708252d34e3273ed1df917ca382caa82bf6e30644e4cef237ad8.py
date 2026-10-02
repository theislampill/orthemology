"""Exact witnesses for the separately proved odd three-message family."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json, random, hashlib
H=Path(__file__).resolve().parent

def nullvector(a):
    """Nonzero rational kernel vector, or None if full column rank."""
    a=[r[:] for r in a];m=len(a);n=len(a[0]);piv=[];r=0
    for c in range(n):
        q=next((k for k in range(r,m) if a[k][c]),None)
        if q is None:continue
        a[r],a[q]=a[q],a[r];v=a[r][c];a[r]=[z/v for z in a[r]]
        for k in range(m):
            if k!=r and a[k][c]:
                v=a[k][c];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
        piv.append(c);r+=1
        if r==m:break
    free=next((c for c in range(n) if c not in piv),None)
    if free is None:return None
    v=[F(0)]*n;v[free]=F(1)
    for k,c in enumerate(piv):v[c]=-a[k][free]
    assert all(sum(x*y for x,y in zip(row,v))==0 for row in a)
    return v

def reduce_fractional(rows,t):
    """Move on all three equality hyperplanes, never increasing sum x."""
    u=len(rows[0]);x=[t]*u
    while True:
        I=[i for i,z in enumerate(x) if 0<z<1]
        if not I:break
        v=nullvector([[p[i] for i in I] for p in rows])
        if v is None:
            assert len(I)<=3
            break
        if sum(v)>0:v=[-z for z in v]
        step=min((1-x[i])/z if z>0 else -x[i]/z for i,z in zip(I,v) if z)
        old=sum(x)
        for i,z in zip(I,v):x[i]+=step*z
        assert all(0<=z<=1 for z in x) and sum(x)<=old
        assert all(sum(a*b for a,b in zip(p,x))==t for p in rows)
    return x

def witness(rows,s):
    t=F(1,s);u=2*s+1
    heavy=next(((m,i) for m,p in enumerate(rows) for i,z in enumerate(p) if z>=t),None)
    if heavy:
        m,r=heavy;remain=[i for i in range(u) if i!=r];others=[p for j,p in enumerate(rows) if j!=m]
        residual=[[p[i]/(1-p[r]) for i in remain] if p[r]<1 else [F(int(k==0)) for k in range(u-1)] for p in others]
        R=next(C for C in combinations(range(u-1),3) if all(sum(p[i] for i in C)>=t for p in residual))
        return {r}|{remain[i] for i in R},'heavy_atom'
    x=reduce_fractional(rows,t)
    A={i for i,z in enumerate(x) if z==1};R={i for i,z in enumerate(x) if 0<z<1}
    assert len(A)<=2 and len(R)<=3 and sum(x)<=2+t
    if len(A)<=1 or not R:return A|R,'round_support'
    assert sum(x[i] for i in R)<=t
    hs=[]
    for p in rows:
        d=t-sum(p[i] for i in A)
        if d<=0:continue
        assert d<=sum(p[i]*x[i] for i in R)<t*t
        S={i for i in range(u) if i not in A and p[i]>=d}
        assert len(S)>=s-1
        hs.append(S)
    if len(hs)<=2:B={min(S) for S in hs}
    else:
        pair=next((i,j) for i,j in combinations(range(3),2) if hs[i]&hs[j])
        k=next(i for i in range(3) if i not in pair)
        B={min(hs[pair[0]]&hs[pair[1]]),min(hs[k])}
    return A|B,'deficit_cover'

def risk(rows,b):
    return max(min(sum(p[i] for i in C) for p in rows) for C in combinations(range(len(rows[0])),b))

def main():
    rng=random.Random(202610020104);counts={'heavy_atom':0,'round_support':0,'deficit_cover':0};dig=hashlib.sha256();cases=0
    for s in range(3,16):
        u=2*s+1;t=F(1,s)
        for trial in range(60):
            rows=[]
            for j in range(3):
                if trial%10==0:nums=[int(i==j) for i in range(u)]
                elif trial%10==1:nums=[1]*u
                elif trial%10 in [2,3,4]:nums=[rng.randrange(80,121) for i in range(u)]
                else:nums=[rng.randrange(0,100) if rng.randrange(5) else 0 for i in range(u)]
                if sum(nums)==0:nums[0]=1
                rows.append([F(n,sum(nums)) for n in nums])
            C,branch=witness(rows,s)
            assert len(C)<=4 and all(sum(p[i] for i in C)>=t for p in rows)
            counts[branch]+=1;cases+=1;dig.update(repr((s,rows,sorted(C),branch)).encode())
    blocks=[]
    for s in range(2,17):
        u=2*s+1
        # Exact integer allocation calculation, rather than root subset explosion.
        v=max(min(F(c0),F(c1,s),F(c2,s)) for c0 in range(2) for c1 in range(s+1) for c2 in range(s+1) if c0+c1+c2==4)
        assert v==F(1,s)
        blocks.append({'s':s,'value':str(v)})
    # H sets of size s-1 cannot all be disjoint on 2s-1 roots for s>=3.
    assert all(3*(s-1)>2*s-1 for s in range(3,101))
    # Removing strict atom hypothesis breaks the deficit estimate: x=t on one
    # coordinate with atom=t gives equality d=t^2, not strict inequality.
    assert F(1,4)*F(1,4)==F(1,16)
    out={'status':'PASS','rational_codebooks':cases,'branch_counts':counts,'partition_cases':blocks,'witness_digest':dig.hexdigest(),'scope':'Exact constructive regressions; continuum claim comes from the supplied proof, not sampling'}
    (H/'ODD_THREE_EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
