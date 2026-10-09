#!/usr/bin/env python3
"""Exact population controls, not empirical samples or approximate recovery."""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, comb, prod
from functools import reduce
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent; results={}
def save(name,data):results[name]=data;print('PASS',name)
def egcd(a,b):
    if b==0:return a,1,0
    g,x,y=egcd(b,a%b);return g,y,x-(a//b)*y
def bezout(v):
    g=0;c=[]
    for a in v:
        ng,x,y=egcd(g,a);c=[x*z for z in c]+[y];g=ng
    assert sum(a*b for a,b in zip(c,v))==g
    return g,c
def prime_divisor(n):
    if n%2==0:return 2
    d=3
    while d*d<=n:
        if n%d==0:return d
        d+=2
    return n
def vp(q,p):
    a,b=q.numerator,q.denominator;v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v
def decode(q):
    assert q and all(0<x<1 for x in q) and all(q[i]>q[i+1] for i in range(len(q)-1))
    p=prime_divisor(q[0].denominator);a=[vp(z,p) for z in q]
    assert all(z<0 for z in a)
    g=reduce(gcd,[-z for z in a]);v=[-z//g for z in a]
    bg,c=bezout(v);assert bg==1
    b=prod((z**n for z,n in zip(q,c)),start=F(1))
    assert 0<b<1 and all(b**n==z for n,z in zip(v,q))
    return v,b
def moments(support,w,t,R):return [sum((z*t**(j*r) for j,z in zip(support,w)),F(0)) for r in range(R+1)]
def countlaw(q,w,R):return [sum((z*comb(R,s)*x**s*(1-x)**(R-s) for x,z in zip(q,w)),F(0)) for s in range(R+1)]
def poly(v,w,w0,z):return w0+sum((a*z**n for n,a in zip(v,w)),F(0))

decoded=0
for h in range(1,5):
    for J in combinations(range(1,11),h):
        d=reduce(gcd,J);q=[F(2,3)**j for j in J]
        v,b=decode(q)
        assert v==[j//d for j in J] and b==F(2,3)**d
        decoded+=1
save('rational_atom_primitive_decoder',{'count_supports':decoded})
bad=[[F(1,2),F(1,3)],[F(1,2),F(1,4),F(1,9)],[F(1,2),F(1,2)],[F(1)]]
for q in bad:
    try:decode(q)
    except AssertionError:pass
    else:raise AssertionError(('malformed accepted',q))
save('decoder_rejects_noncommon_power_or_boundary_inputs',len(bad))

vectors=[(1,),(1,2),(2,3),(2,5),(1,3,4),(2,3,5),(3,4,5)]
equiv=0
for v in vectors:
    h=len(v)
    for d,e,u,w0 in product(range(1,4),range(1,4),[F(1,2),F(2,3)],[F(0),F(1,5)]):
        w=[(1-w0)*F(i+1,h*(h+1)//2) for i in range(h)]
        J=[d*n for n in v];L=[e*n for n in v];t=u**e;s=u**d
        if w0:J=[0]+J;L=[0]+L;ww=[w0]+w
        else:ww=w
        R=2*len(J)-1
        assert moments(J,ww,t,R)==moments(L,ww,s,R)
        q0=[t**j for j in J];q1=[s**j for j in L]
        assert q0==q1 and countlaw(q0,ww,R)==countlaw(q1,ww,R)
        equiv+=1
save('integer_dilations_full_finite_horizon_equivalence',{'world_pairs':equiv})

q=[F(1,64),F(1,4096)]
assert decode(q)==([1,2],F(1,64))
assert [F(1,8)**j for j in [2,4]]==[F(1,4)**j for j in [3,6]]==q
save('noninteger_direct_scale_three_halves',True)

maxcases=0
for v in vectors:
    V=max(v)
    for M in range(V,6*V+1):
        feasible=[d for d in range(1,M+1) if max(d*x for x in v)<=M]
        assert feasible==list(range(1,M//V+1));maxcases+=1
save('known_maximum_leaves_integer_scale_set',maxcases)

b=F(1,64);x0=F(7,8);D=3
bandsets={}
for eta in [F(0),F(1,10),F(7,64),F(1,8)]:
    A=max(F(0),1-x0-eta);B=min(F(1),1-x0+eta)
    ds=[d for d in range(1,D+1) if A**d<=b<=B**d]
    assert ds=={F(0):[2],F(1,10):[2],F(7,64):[1,2],F(1,8):[1,2,3]}[eta]
    bandsets[str(eta)]=ds
    for d in ds:
        true_rate={1:F(63,64),2:F(7,8),3:F(3,4)}[d]
        def r(x):return true_rate*x/x0 if x<=x0 else true_rate+(1-true_rate)*(x-x0)/(1-x0)
        grid=sorted(set([F(i,64) for i in range(65)]+[x0]))
        assert r(F(0))==0 and r(F(1))==1
        assert all(r(y)>r(x) for x,y in zip(grid,grid[1:]))
        assert max(abs(r(x)-x) for x in grid)==abs(true_rate-x0)<=eta
save('eta_feasible_scales_and_piecewise_linear_extensions',bandsets)

J=[1,3];L=[2,4];w=[F(27,175),F(148,175)];ww=[F(111,175),F(64,175)];t=F(3,4)
m=moments(J,w,t,3);mm=moments(L,ww,t,3)
assert m[:3]==mm[:3] and m[3]-mm[3]==F(26973,6553600)
assert m[1]==F(189,400) and m[2]==F(243,1024)
assert countlaw([t**j for j in J],w,2)==countlaw([t**j for j in L],ww,2)
assert decode([t**j for j in J])[0]!=decode([t**j for j in L])[0]
save('insufficient_two_repeat_primitive_counterexample',{'moments_left':m,'moments_right':mm,'third_gap':m[3]-mm[3]})

for n in range(65):
    t=F(n,64);s=(t+t*t)/2
    assert 0<=t-s<=F(1,8)
    gap=(t*t+t**4)/2-s*s
    assert gap==(t-t*t)**2/4
    assert (gap>0)==(0<t<1)
assert F(1,2)-(F(1,2)+F(1,4))/2==F(1,8)
save('fresh_resampling_band_and_held_second_moment_separation',True)

for t in [F(i,32) for i in range(33)]:
    w0=F(1,5);Fval=w0+F(3,10)*t*t+F(1,2)*t**5;s=(Fval-w0)/(1-w0)
    assert Fval==w0+(1-w0)*s and 0<=s<=1
save('general_fresh_positive_mixture_collapse',True)

for u in [F(1,4),F(1,2),F(3,4)]:
    t=u**3
    assert [t,t*t]==[t,(u*u)**3]
assert [F(1,8),F(1,8)**2]==[F(1,8),F(1,4)**3]
save('label_specific_calibration_invalidates_ratios',True)

for x in [F(i,16) for i in range(17)]:
    rr=F(x>=F(1,2));t=1-rr
    assert abs(rr-x)<=F(1,2)
    assert len({t**j for j in range(1,11)})==1
save('step_calibration_without_any_interior_value',True)

pc=0
for d in range(1,7):
    for e in range(d+1,9):
        h=e-d;theta_power=F(e-d,2*e)**h*F(d,e)**d
        rows=[]
        for u in [F(i,32) for i in range(33)]:
            t=u**e;s=u**d;x=1-(t+s)/2;rd=1-t;re=1-s
            assert t**d==s**e
            assert abs(rd-x)==abs(re-x)==(s-t)/2
            assert ((s-t)/2)**h<=theta_power
            rows.append((x,rd,re));pc+=1
        rows.sort()
        assert all(y[0]>x[0] and y[1]>x[1] and y[2]>x[2] for x,y in zip(rows,rows[1:]))
save('general_pair_global_power_maps_and_exact_radius_power_bounds',{'rational_parameter_cases':pc})

sc=0
for D in range(2,13):
    u=F(D-1,D);ts=u**D;ss=u**(D-1);theta=(ss-ts)/2;m=(ts+ss)/2
    assert theta==F(1,2*D)*u**(D-1)
    for eta in [F(0),theta/2,3*theta/4]:
        A=m-eta;B=m+eta
        assert 0<A<=B<1
        for v in vectors:
            h=len(v);w0=F(1,5);w=[F(4,5*h)]*h
            for d in range(1,D):
                assert A**d>B**(d+1)
                assert poly(v,w,w0,A**d)>poly(v,w,w0,B**(d+1));sc+=1
save('remaining_scale_catalogue_population_separation',{'adjacent_F_interval_checks':sc})

oracle=[];t=F(1,2)
for n in [2,3,5,10,100,1000]:
    assert gcd(n,2*n+1)==1
    lo=t*t*(1-F(1,n));hi=t*t;target=t**(2*n+1)
    assert lo**n<=target<=hi**n
    for r in range(1,9):
        original=(t**r+t**(2*r))/2
        lower=(t**r+lo**r)/2;upper=(t**r+hi**r)/2
        assert upper==original and upper-lower<=F(r,8*n)
    oracle.append({'n':n,'primitive_support':[n,2*n+1],'algebraic_node_interval':[lo,hi],'moment_error_bound':'r/(8n)'})
save('equal_weight_gcd_one_cauchy_countermodel_certificates',oracle)

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x
(HERE/'results').mkdir(exist_ok=True)
(HERE/'results'/'exact_controls.json').write_text(json.dumps(enc({'families_passed':len(results),'controls':results}),indent=2)+'\n')
print('ALL',len(results),'EXACT CONTROL FAMILIES PASS')
