#!/usr/bin/env python3
"""Deterministic finite-grid and symbolic checks; not empirical sampling."""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product, permutations
from math import factorial
from pathlib import Path
import json
import mpmath as mp
import sympy as sp

checks = 0
def check(b):
    global checks
    checks += 1
    assert b

def panel(m):
    return [Q(i, m+1) for i in range(1,m+1)], [Q(m+1-i,m+1) for i in range(1,m+1)]

def sig(x,y,a,b):
    pts=list(zip(a,b))+list(zip(a[:-1],b[1:]))
    return sum((1<<i) for i,(u,v) in enumerate(pts) if x<=u and y<=v)

def exact_box(x,y,i,a,b):
    return x<=a[i] and y<=b[i] and (i==0 or x>a[i-1]) and (i==len(a)-1 or y>b[i+1])

def iid_law(one,k):
    d={0:Q(1)}
    for _ in range(k):
        nxt=defaultdict(Q)
        for s,p in d.items():
            for t,q in one.items(): nxt[s|t]+=p*q
        d=nxt
    return d

grid_results=[]
for m in range(1,7):
    a,b=panel(m); goal=(1<<m)-1
    # Exhaust threshold ties, axes, unit boundaries, and open-grid representatives.
    gx=sorted(set([Q(0),Q(1)]+a+[(u+v)/2 for u,v in zip([Q(0)]+a,a+[Q(1)])]))
    gy=sorted(set([Q(0),Q(1)]+b+[(u+v)/2 for u,v in zip([Q(0)]+list(reversed(b)),list(reversed(b))+[Q(1)])]))
    for x,y in product(gx,gy):
        s=sig(x,y,a,b); hits=[i for i in range(m) if s>>i&1]
        if not s>>m:
            check(len(hits)<=1)
            for i in range(m): check(bool(s>>i&1)==exact_box(x,y,i,a,b))
        for i in range(m):
            for j in range(i+1,m):
                if s>>i&1 and s>>j&1: check(bool(s>>(m+i)&1))
    # Exact continuous product-uniform threshold-cell law on the whole panel grid.
    xs=[Q(0)]+a+[Q(1)]; ys=[Q(0)]+list(reversed(b))+[Q(1)]
    one=defaultdict(Q); masses=[Q(0)]*m
    for xl,xr in zip(xs,xs[1:]):
        for yl,yr in zip(ys,ys[1:]):
            x=(xl+xr)/2; y=(yl+yr)/2; w=(xr-xl)*(yr-yl)
            one[sig(x,y,a,b)]+=w
            for i in range(m):
                if exact_box(x,y,i,a,b):masses[i]+=w
    check(sum(one.values())==1)
    for k in range(m+2):
        d=iid_law(one,k); p=d.get(goal,Q(0)); check(sum(d.values())==1)
        if k<m:check(p==0)
        # Inclusion-exclusion: forbidden signatures excluded; each q label required.
        safe=sum(v for s,v in one.items() if s>>m==0)
        ie=sum((-1)**sum(bits)*(safe-sum(masses[i] for i in range(m) if bits[i]))**k
               for bits in product([0,1],repeat=m))
        check(p==ie)
        if k==m:
            prod=Q(1)
            for z in masses:prod*=z
            check(p==factorial(m)*prod)
            check(p<=Q(factorial(m),m**m))
    grid_results.append({'m':m,'one_route_signatures':len(one),'threshold_points_checked':len(gx)*len(gy),
                         'certificate_probability_m_uniform_routes':str(iid_law(one,m).get(goal,Q(0)))})

# Independent but heterogeneous rational cell laws: exact result is a permanent.
m=3;a,b=panel(m);cells=[]
xs=[Q(0)]+a+[Q(1)];ys=[Q(0)]+list(reversed(b))+[Q(1)]
for xl,xr in zip(xs,xs[1:]):
    for yl,yr in zip(ys,ys[1:]):cells.append(((xl+xr)/2,(yl+yr)/2))
d={0:Q(1)}; matrix=[]
for j in range(m):
    weights=[Q((i+1)**(j+1)) for i in range(len(cells))];total=sum(weights)
    law=defaultdict(Q);row=[Q(0)]*m
    for (x,y),w in zip(cells,weights):
        p=w/total;law[sig(x,y,a,b)]+=p
        for i in range(m):
            if exact_box(x,y,i,a,b):row[i]+=p
    nxt=defaultdict(Q)
    for s,p in d.items():
        for t,q in law.items():nxt[s|t]+=p*q
    d=nxt;matrix.append(row)
perm=Q(0)
for order in permutations(range(m)):
    term=Q(1)
    for j,i in enumerate(order):term*=matrix[j][i]
    perm+=term
check(d.get((1<<m)-1,Q(0))==perm)

# n=1 radical identity, its positivity, and square-box symmetry.
c=sp.Rational(1,2)
F=lambda a,b:1-(1-a*b)**c
mass=sp.simplify(F(sp.Rational(1,3),sp.Rational(2,3))-F(sp.Rational(1,3),sp.Rational(1,3)))
check(sp.simplify(mass-(2*sp.sqrt(2)-sp.sqrt(7))/3)==0)
p=sp.simplify(2*mass**2)
check(p>0);check(sp.simplify(p-(30-8*sp.sqrt(14))/9)==0)

# Failed-transport countercontrols: OR-of-AND route, state redraw, and unary inventory.
a,b=panel(2)
nonseparable=lambda u,v:any(u>=x and v>=y for x,y in zip(a,b))
check(all(nonseparable(x,y) for x,y in zip(a,b)))
check(not nonseparable(a[0],b[1]))
unary=lambda u,v:u>=Q(1,2) or v>=Q(1,2)
check(all(unary(x,y) for x,y in zip(a,b)))
check(not unary(a[0],b[1]))
# Diagonal first route cannot occupy either symmetric staircase box.
for z in [Q(i,12) for i in range(13)]:
    check(not exact_box(z,z,0,a,b));check(not exact_box(z,z,1,a,b))

mp.mp.dps=100
joes=[]
for n in [1,2,3,5,10,20,50,100]:
    m=n+1;c=mp.mpf(n)/m
    aa=[mp.mpf(i)/(m+1) for i in range(m+1)]
    bb=[mp.mpf(m+1-i)/(m+1) for i in range(1,m+2)]
    H=lambda x,y:-mp.expm1(c*mp.log1p(-x*y))
    masses=[H(aa[i+1],bb[i])-H(aa[i],bb[i])-H(aa[i+1],bb[i+1])+H(aa[i],bb[i+1]) for i in range(m)]
    for z in masses:check(z>0)
    lp=mp.loggamma(m+1)+sum(mp.log(z) for z in masses)
    ub=mp.loggamma(m+1)-m*mp.log(m)
    check(lp<=ub)
    joes.append({'n':n,'m':m,'log_probability':float(lp),'log_universal_upper_bound':float(ub)})

out={'classification':'Deterministic exact and numerical controls; no empirical sampling',
     'assertions':checks,'grid_results':grid_results,'heterogeneous_permanent':str(perm),
     'n1_probability_exact':str(p),'n1_probability_decimal':str(sp.N(p,40)),
     'joe_regular_staircase':joes,'all_passed':True}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
