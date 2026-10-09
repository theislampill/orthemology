#!/usr/bin/env python3
"""Exact rational / certified-algebraic controls. No empirical sampling."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
from pathlib import Path
from functools import lru_cache
import json

counts=Counter()
def check(cond, family):
    assert cond, family
    counts[family]+=1

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[1],x[1]-y[0])
def mul(x,y):
    p=[a*b for a in x for b in y]
    return min(p),max(p)
def I(x): return (F(x),F(x))
@lru_cache(None)
def power_interval(x,p,q,bits=96):
    x=F(x)
    if x in (0,1) or q==1:
        return I(x**p)
    y=x**p
    lo,hi=F(0),F(1)
    for _ in range(bits):
        mid=(lo+hi)/2
        if mid**q<y: lo=mid
        else: hi=mid
    assert lo**q<=y<=hi**q
    return lo,hi
@lru_cache(None)
def H(z,c):
    c=F(c)
    return sub(I(1),power_interval(1-F(z),c.numerator,c.denominator))
def J(a,b,c): return H(a*b,c)
def cells(a,b,c):
    u,v,j=H(a,c),H(b,c),J(a,b,c)
    return j,sub(u,j),sub(v,j),add(sub(sub(I(1),u),v),j)
def rect(a0,a1,b0,b1,c):
    return add(sub(sub(J(a1,b1,c),J(a0,b1,c)),J(a1,b0,c)),J(a0,b0,c))

# Certified, not floating-point, positivity of all four Bernoulli cells.
cs=[F(1,4),F(1,3),F(1,2),F(2,3),F(3,4),F(1)]
grid=[F(i,8) for i in range(1,8)]
for c,a,b in product(cs,grid,grid):
    t=cells(a,b,c)
    for cell in t: check(cell[0]>0,'positive_interior_Bernoulli_cells')
    total=I(0)
    for cell in t: total=add(total,cell)
    check(total[0]<=1<=total[1],'table_mass_interval_contains_one')
    # All margins recovered by summing the appropriate table cells.
    for expected,got in [(H(a,c),add(t[0],t[1])),(H(b,c),add(t[0],t[2]))]:
        check(not(expected[1]<got[0] or got[1]<expected[0]),'margin_interval_consistency')
    # Sign of derivative reduced exactly to sign(1-cab), remaining factors positive.
    check(1-c*a*b>0,'valid_mixed_derivative_sign')

# Valid rectangle masses, including upper boundary, via certified rational roots.
rectgrid=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
for c,(a0,a1),(b0,b1) in product(cs,combinations(rectgrid,2),combinations(rectgrid,2)):
    mass=rect(a0,a1,b0,b1,c)
    check(mass[0]>0,'positive_nondegenerate_CDF_rectangles')

# Explicit endpoint/margin values, with zero/one arguments handled exactly.
for c,a in product(cs,rectgrid):
    check(J(a,F(0),c)==I(0),'grounded_CDF')
    check(J(a,F(1),c)==H(a,c),'CDF_margins')
    check(H(F(0),c)==I(0) and H(F(1),c)==I(1),'calibration_endpoints')

# Exact rational endpoint equivalence for every integer pair 1<=n<=m<=10.
# Set 1-ab=t^q so its rational c=p/q power is exactly t^p.
transport=[]
for m in range(1,11):
    for n in range(1,m+1):
        c=F(n,m); p,q=c.numerator,c.denominator; t=F(3,4)
        ab=1-t**q; b=(1+ab)/2; a=ab/b; j=1-t**p
        check(0<a<1 and 0<b<1,'rational_transport_commands_interior')
        check((1-j)**m==(1-a*b)**n,'exact_endpoint_transport')
        check((1-j)**q==(1-a*b)**p,'exact_joint_success_defining_power')
        ji=J(a,b,c)
        check(ji[0]<=j<=ji[1],'algebraic_interval_contains_exact_joint')
        transport.append({'n':n,'m':m,'a':str(a),'b':str(b),'J':str(j),'Q':str((1-j)**m)})

# Joe formula and inverse reparameterization agree exactly in their rational bases.
for theta,u,v in product(range(1,6),[F(1,4),F(1,2),F(3,4)],[F(1,4),F(1,2),F(3,4)]):
    c=F(1,theta); a=1-(1-u)**theta; b=1-(1-v)**theta
    expanded=(1-u)**theta+(1-v)**theta-(1-u)**theta*(1-v)**theta
    check(1-a*b==expanded,'Joe_reparameterization_exact_base')
    cop=sub(I(1),power_interval(expanded,1,theta))
    check(cop==J(a,b,c),'Joe_reparameterization_exact_intervals')
    hi=H(a,c)
    check(hi[0]<=u<=hi[1],'calibration_inverse_exact_target')

# Independence at c=1 is literal rational equality.
for a,b in product(rectgrid,rectgrid):
    check(J(a,b,F(1))==I(a*b),'independence_boundary')

# Countercontrols: c=2 is increasing/probability-valued but not 2-increasing.
def H2(z): return 2*z-z*z
def R2(a0,a1,b0,b1):
    return H2(a1*b1)-H2(a0*b1)-H2(a1*b0)+H2(a0*b0)
check(R2(F(3,4),F(1),F(3,4),F(1))==F(-17,256),'invalid_upper_rectangle_exact')
check(R2(F(3,4),F(7,8),F(3,4),F(7,8))==F(-41,4096),'invalid_interior_rectangle_exact')
check(R2(F(0),F(1,2),F(0),F(1,2))==F(7,16),'valid_low_rectangle_of_invalid_surface')
a=b=F(3,4); u,v,j=H2(a),H2(b),H2(a*b)
check((j,u-j,v-j,1-u-v+j)==tuple(F(k,256) for k in [207,33,33,-17]),'invalid_Bernoulli_table_exact')
for a,b in product(rectgrid,rectgrid):
    check(0<=H2(a*b)<=1,'invalid_surface_probability_values')
    check(2*b*(1-a*b)>=0 and 2*a*(1-a*b)>=0,'invalid_surface_monotone_derivatives')

# Valid c=1/2 example: certify dependence and endpoint equality.
a=b=F(1,2); c=F(1,2)
j=J(a,b,c); uv=mul(H(a,c),H(b,c))
check(sub(j,uv)[0]>0,'strict_within_route_dependence')
check(F(3,4)==1-a*b,'two_route_sqrt_endpoint_identity_base')
valid_rect=rect(F(1,2),F(1),F(1,2),F(1),c)
check(valid_rect[0]>0,'valid_upper_rectangle_radical')

# The panel distinguishes separability, not actual hidden count in the larger class.
a1,a2,b1,b2=F(1,4),F(3,4),F(1,3),F(2,3)
for m in range(1,6):
    c=F(1,m)
    det=sub(mul(J(a1,b1,c),J(a2,b2,c)),mul(J(a1,b2,c),J(a2,b1,c)))
    check((det==I(0) if m==1 else det[0]>0),'panel_rank_under_wrong_factorization')

# Exact necessary bound rules out every tested m<n, even heterogeneous copulas.
heterogeneous=[]
for n in range(2,13):
    for m in range(1,n):
        eps=F(1,2)
        while (2-eps)**n<=2**m: eps/=2
        check(eps>0 and (2-eps)**n>2**m,'heterogeneous_shared_margin_bound_contradiction')
        target=(eps*(2-eps))**n
        upper=2**m*eps**n
        check(target>upper,'heterogeneous_target_exceeds_Frechet_product_bound')
        heterogeneous.append({'n':n,'m':m,'epsilon':str(eps),'target':str(target),'upper_bound':str(upper)})

# Existing semantic controls, retained attribution; no new discovery credit.
a=b=F(1,2)
check((1-a)*(1-a*b)!=1-a,'inherited_shared_gate_vs_independent_route')
crossA=a*(2-a*b)/(2-b); crossB=b*(2-b)
check(crossA*crossB==H2(a*b) and crossA!=a,'inherited_cross_talk_factorization')

out={'status':'PASS','arithmetic':'Python Fraction and certified rational root intervals; no floating-point claims',
     'assertions':sum(counts.values()),'families':dict(counts),'transport_witnesses':transport,
     'heterogeneous_impossibility_controls':heterogeneous,
     'valid_c_half_upper_rectangle_interval':[str(x) for x in valid_rect],
     'invalid_c_two_upper_rectangle':'-17/256','invalid_c_two_interior_rectangle':'-41/4096',
     'limits':'Finite diagnostics do not replace the general direct proofs, test arbitrary copula software, or certify physical premises.'}
path=Path(__file__).resolve().parent/'results'/'exact_controls.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','assertions','families']},indent=2))
