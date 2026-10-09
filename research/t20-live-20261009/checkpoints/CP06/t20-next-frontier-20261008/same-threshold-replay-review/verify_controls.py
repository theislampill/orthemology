#!/usr/bin/env python3
"""Independent exact rational controls. No numerical tolerances or external packages."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def frac(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def cells(t,c):
    return {(0,0):1-2*t+c,(1,0):t-c,(0,1):t-c,(1,1):c}

def aggregate(route_laws):
    result={}
    for route_states in product(*(list(x.items()) for x in route_laws)):
        probability=F(1)
        xs=[]; ys=[]; zs=[]
        for (x,y),p in route_states:
            probability*=p; xs.append(x); ys.append(y); zs.append(x*y)
        if probability:
            key=f'{max(xs)}{max(ys)}{max(zs)}'
            result[key]=result.get(key,F(0))+probability
    return result

t=F(3,4); u=F(1,2); c1=u; c2=u*u/2
q=(1-c1)*(1-c2)
j=(1-2*u+c1)*(1-2*u+c2)
face=(1-u)**2
assert q==1-t*t==F(7,16)
assert j==(1-t)**2==F(1,16)
assert face==1-t==F(1,4)
alternative=aggregate([cells(u,c1),cells(u,c2)])
baseline=aggregate([cells(t,t*t)])
assert alternative==baseline
assert sum(alternative.values())==1
assert alternative=={'000':F(1,16),'100':F(3,16),'010':F(3,16),'111':F(9,16)}

# Explicit globally valid finite-grid perturbation for A=B={0,3/4,1}.
epsilon=F(1,128)
def f(x): return x*(1-x)*(x-t)
def copula(a,b): return a*b+epsilon*f(a)*f(b)
grid=[F(0),t,F(1)]
assert all(f(x)==0 for x in grid)
assert all(copula(a,b)==a*b for a,b in product(grid,repeat=2))
# f'(x)=-3*x^2+(7/2)*x-3/4. On [0,1], the coefficient l1 bound is 29/4.
derivative_bound=F(29,4)
density_lower_bound=1-epsilon*derivative_bound**2
assert density_lower_bound>=F(1,2)
rectangles=[]
for a0,a1 in zip(grid,grid[1:]):
    for b0,b1 in zip(grid,grid[1:]):
        p=copula(a1,b1)-copula(a0,b1)-copula(a1,b0)+copula(a0,b0)
        assert p==(a1-a0)*(b1-b0)
        rectangles.append({'a':[frac(a0),frac(a1)],'b':[frac(b0),frac(b1)],'probability':frac(p)})
offgrid=copula(F(1,2),F(1,2))
assert offgrid-F(1,4)==F(1,32768)

# Independent exact coefficient accounting in the small-t log-J argument.
# h=c*t-c(c-1)t^2/2, sum C=n*t^2+O(t^4), m*c=n.
for m,n in product(range(1,12),repeat=2):
    c=F(n,m)
    first=-2*m*c
    second=m*c*(c-1)+n-2*m*c*c
    assert first==-2*n
    assert second==-n*c
    assert (second==-n)==(m==n)

result={
 'status':'PASS',
 'semantics':'Exact rational controls, not empirical certification or closure.',
 'high_command':{'target_n':1,'alternative_m':2,'command':frac(t),'calibrated_threshold':frac(u),'C1':frac(c1),'C2':frac(c2),'Q':frac(q),'J':frac(j),'each_face_no_hit':frac(face),'full_held_transcript_XYZ':{k:frac(v) for k,v in sorted(alternative.items())}},
 'finite_grid_perturbation':{'grid':[frac(x) for x in grid],'epsilon':frac(epsilon),'f':'x(1-x)(x-3/4)','certified_density_lower_bound':frac(density_lower_bound),'cell_probabilities':rectangles,'off_grid_point':['1/2','1/2'],'off_grid_copula':frac(offgrid),'off_grid_difference_from_product':frac(offgrid-F(1,4))},
 'asymptotic_coefficient_checks':{'m_range':'1..11','n_range':'1..11','cases':121,'purpose':'Arithmetic control only; the symbolic proof applies to every finite m and n.'}
}
(ROOT/'exact_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
