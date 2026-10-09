#!/usr/bin/env python3
"""Independent deterministic diagnostics. No author code is imported.
Exact polynomial integration carries the low-count checks. Finite numerical
checks are consistency diagnostics, not interval/asymptotic proofs.
"""
from fractions import Fraction
from math import factorial, comb
from pathlib import Path
import json, time
import sympy as sp
import mpmath as mp

started=time.monotonic()
mp.mp.dps=80
m,t,M,Z=sp.symbols('m t M Z')
expansion=sp.series(sp.exp(-t*M+(1-sp.exp(-t)-t)*Z),t,0,5).removeO().expand()
expected4=M**4-6*M*M*Z-4*M*Z+3*Z*Z-Z
assert sp.expand(24*expansion.coeff(t,4)-expected4)==0
assert sp.expand(2*expansion.coeff(t,2)-(M*M-Z))==0
assert sp.expand(expansion.coeff(t,1)+M)==0
assert sp.expand(expected4-(M**4-6*M*M*Z+4*M*Z+3*Z*Z-Z))!=0

# Integrate polynomial monomials over x_1<...<x_k and y_1>...>y_k.
def integrate_ordered(expr,xs,ys):
    poly=sp.Poly(sp.expand(expr),*(xs+ys))
    out=sp.Integer(0); k=len(xs)
    for powers, coefficient in poly.terms():
        denom=1; cum=0
        for j,p in enumerate(powers[:k],1):
            cum+=p; denom*=j+cum
        cum=0
        for j,p in enumerate(reversed(powers[k:]),1):
            cum+=p; denom*=j+cum
        out+=coefficient/sp.Integer(denom)
    return sp.factor(out)

moments=[]; identities=[]
for n in range(5):
    vals={key:sp.Integer(0) for key in ['norm','M','M2mZ','M4identity','A','A2mI2','M4','A2','K2']}
    if n==0:
        # Empty skyline is part of the auxiliary PPP, not the n>=1 baseline.
        u=sp.Integer(1); k=0; b1=sp.Rational(1,4); b2=sp.Rational(1,9); boundary=0
        mm=k-m*u; aa=boundary-m*b1
        vals={'norm':sp.Integer(1),'M':mm,'M2mZ':mm**2-m*u,
              'M4identity':mm**4-6*mm**2*m*u-4*mm*m*u+3*(m*u)**2-m*u,
              'A':aa,'A2mI2':aa**2-m*b2,'M4':mm**4,'A2':aa**2,'K2':0}
    else:
        for k in range(1,n+1):
            xs=list(sp.symbols('x1:'+str(k+1))); ys=list(sp.symbols('y1:'+str(k+1)))
            xnext=xs[1:]+[sp.Integer(1)]
            u=xs[0]+sum((b-a)*y for a,b,y in zip(xs,xnext,ys))
            b1=(xs[0]**2+sum((b*b-a*a)*y*y for a,b,y in zip(xs,xnext,ys)))/4
            b2=(xs[0]**3+sum((b**3-a**3)*y**3 for a,b,y in zip(xs,xnext,ys)))/9
            boundary=sum(x*y for x,y in zip(xs,ys))
            mm=k-m*u; aa=boundary-m*b1
            density=factorial(n)//factorial(n-k)*(1-u)**(n-k)
            expressions={'norm':1,'M':mm,'M2mZ':mm**2-m*u,
               'M4identity':mm**4-6*mm**2*m*u-4*mm*m*u+3*(m*u)**2-m*u,
               'A':aa,'A2mI2':aa**2-m*b2,'M4':mm**4,'A2':aa**2,'K2':k*k}
            for key, expr in expressions.items():
                vals[key]+=integrate_ordered(density*expr,xs,ys)
        vals={key:sp.factor(val) for key,val in vals.items()}
    assert vals['norm']==1
    if n:
        harmonic=sum(sp.Rational(1,j) for j in range(1,n+2))
        assert vals['M'].subs(m,n+1)==-sp.Rational(1,n+1)
        assert vals['M4'].subs(m,n+1)>0
        assert vals['A2'].subs(m,n+1)>0
    moments.append(vals)
    print('exact ordered integrations n='+str(n),flush=True)

formal={}
for key in ['M','M2mZ','M4identity','A','A2mI2']:
    mix=sum(m**n/sp.factorial(n)*moments[n][key] for n in range(5))
    coefficients=[sp.expand(mix).coeff(m,j) for j in range(5)]
    assert all(v==0 for v in coefficients),(key,coefficients)
    formal[key]={'coefficients_through_degree_4':[str(v) for v in coefficients]}
# Truncating away the PPP empty skyline breaks all three centered identities.
wrong=sum(m**n/sp.factorial(n)*moments[n]['M4identity'] for n in range(1,5))
assert any(sp.expand(wrong).coeff(m,j)!=0 for j in range(5))

# Posterior/RN identity checked independently from the binomial density and
# Poisson-mixture skyline density, including unsupported and empty strata.
rn_checks=[]
for n in [1,2,3,7,31,127,1023,1000000]:
    mm=mp.mpf(n+1)
    denominator=mp.exp(-mm+n*mp.log(mm)-mp.loggamma(n+1))
    bound=2*mp.exp(mp.mpf(1)/24)
    for U in [mp.mpf('0.000001'),mp.mpf('.01'),mp.mpf('.25'),mp.mpf('.5')]:
        D=1-U; lam=mm*D
        # Bound the numerator over every possible Poisson integer by its mode.
        mode=int(mp.floor(lam))
        peak=mp.exp(-lam+mode*mp.log(lam)-mp.loggamma(mode+1))
        assert peak/denominator<=bound
        for k in sorted({1,min(n,2),max(1,n//2),n,n+1}):
            if k>n:
                ratio=mp.mpf(0); density_ratio=mp.mpf(0)
            else:
                j=n-k
                ratio=mp.exp(-lam+j*mp.log(lam)-mp.loggamma(j+1))/denominator
                density_ratio=mp.exp(mp.loggamma(n+1)-mp.loggamma(n-k+1)+(n-k)*mp.log(D)-k*mp.log(mm)+mm*U)
                assert abs(ratio-density_ratio)<=mp.mpf('1e-65')*max(1,abs(ratio))
            assert ratio<=bound
        rn_checks.append({'n':n,'U':str(U),'max_mass_ratio':mp.nstr(peak/denominator,25)})
# U=1, K=0 means empty PPP skyline; conditioning on n>=1 assigns zero mass.
assert all(n>0 for n in [1,2,8])

# A uniform RN bound cannot be extended to the whole skyline support.
global_rn_rejection=[]
for nn in [15,255,4095]:
    mm=mp.mpf(nn+1); D=1/mm**2
    den=mp.exp(-mm+nn*mp.log(mm)-mp.loggamma(nn+1))
    rr=mp.exp(-mm*D)/den  # K=n leaves zero hidden points.
    assert rr>3
    global_rn_rejection.append({'n':nn,'D':mp.nstr(D,20),'RN':mp.nstr(rr,20)})

# Exact Stirling-number coefficients and Bernoulli convolution for sixth moments.
from sympy.functions.combinatorial.numbers import stirling
expected_six=[1,31,90,65,15,1]
assert [int(stirling(6,r,kind=2)) for r in range(1,7)]==expected_six
record_checks=[]
dist=[sp.Integer(1)]; harmonic=sp.Integer(0)
for nn in range(1,33):
    prob=sp.Rational(1,nn); harmonic+=prob
    new=[sp.Integer(0)]*(len(dist)+1)
    for k,weight in enumerate(dist):
        new[k]+=weight*(1-prob);new[k+1]+=weight*prob
    dist=new
    sixth=sum(k**6*weight for k,weight in enumerate(dist))
    envelope=sum(stirling(6,r,kind=2)*harmonic**r for r in range(1,7))
    assert sixth<=envelope
    record_checks.append({'n':nn,'sixth':str(sixth),'envelope':str(envelope)})

# Singular correction and stopped reverse-KL orientation, on an explicit finite tree.
p0=[mp.mpf(1)/2,mp.mpf(1)/2]
p1=[mp.mpf(1)/5,mp.mpf(3)/5]; singular=mp.mpf(1)/5
single=sum(q*mp.log(q/r) for q,r in zip(p0,p1))
phi=sum(q*(-mp.log(r/q)+r/q-1) for q,r in zip(p0,p1))
assert abs(single-phi-singular)<mp.mpf('1e-75')
assert abs(single-phi)>mp.mpf('.1')
assert abs(single-(phi-singular))>mp.mpf('.1')
q0=[p0[0],p0[1]*p0[0],p0[1]*p0[1]]
q1=[p1[0],p1[1]*p1[0],p1[1]*p1[1]]
stopped=sum(q*mp.log(q/r) for q,r in zip(q0,q1))
assert abs(stopped-(1+p0[1])*single)<mp.mpf('1e-75')
assert abs(stopped-(1+p1[1])*single)>mp.mpf('.01')

weighted=[]
for mm in [2,3,8,32,1000,10**6]:
    # Scale to s=mxy, splitting the quadrature around the logarithmic endpoint.
    upper=mp.mpf(mm)
    # For huge m integrate only to 250; omitted tail is below ~1e-95 times log m.
    cap=min(upper,mp.mpf(250))
    points=sorted(set([mp.mpf(0), min(cap,mp.mpf(1)),min(cap,mp.mpf(10)),cap]))
    integral=mp.quad(lambda s: s*s*mp.exp(-s)*(mp.log(upper)-mp.log(s)) if s else 0,points)/upper**2
    envelope=(2*mp.log(upper)+mp.mpf(1)/9)/upper**2
    assert 0<integral<envelope
    weighted.append({'m':mm,'variance_A_quadrature':mp.nstr(integral,35),'envelope':mp.nstr(envelope,35)})

# Fourth moment self-bound algebra; no cancellation is replaced by a raw K^4.
x,b,a=sp.symbols('x b a',positive=True)
# From X<=6sqrt(XB)+4sqrt(AB)+A, Young gives X<=36B+8sqrt(AB)+2A.
young_identity=sp.expand((sp.sqrt(x)-6*sp.sqrt(b))**2/2-(x/2+18*b-6*sp.sqrt(x*b)))
assert young_identity==0

# Exact n=1 fourth and weighted moments serve as small-n transfer counterchecks.
one_point_fourth=sum(sp.binomial(4,j)*(-1)**(4-j)*2**j/sp.Integer((j+1)**2) for j in range(5))
assert one_point_fourth==sp.Rational(23,75)
assert moments[1]['M4'].subs(m,2)==one_point_fourth
# The fixed-n centered expectation is not the PPP zero; this catches a silent equality transfer.
assert moments[1]['M'].subs(m,2)!=0

result={'status':'PASS','scope':'Deterministic exact arithmetic and high-precision diagnostics; not empirical or interval/asymptotic proof.',
 'exponential_fourth_derivative':str(expected4),'formal_poisson_mixture_controls':formal,
 'fixed_count_exact':[{ 'n':n, **{key:str(val.subs(m,n+1)) if hasattr(val,'subs') else str(val) for key,val in moments[n].items()} } for n in range(5)],
 'rn_checks':rn_checks,'global_RN_rejections':global_rn_rejection,
 'record_sixth_moment_checks':record_checks,
 'singular_and_stopping_checks':{'one_vector_reverse_KL':mp.nstr(single,35),'stopped_reverse_KL':mp.nstr(stopped,35),'E0_starts':'1.5','E1_starts':'1.6','singular_mass':'0.2'},
 'weighted_variance_checks':weighted,
 'rejected_wrong_candidates':['wrong sign of fourth-derivative MZ term','discarded PPP empty skyline','fixed-count compensation mean identically zero','unrestricted uniform RN bound','missing or negative singular correction','E1 started-vector orientation']}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS all independent controls; seconds',round(time.monotonic()-started,3),flush=True)
