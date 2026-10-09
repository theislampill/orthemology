#!/usr/bin/env python3
"""Deterministic diagnostics; written inequalities, not this script, prove the rate.

No random samples, author-code imports, external files, or network calls.
Exact ordered-simplex integrals independently check low-order PPP series.
"""
import json
import math
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 70
HERE = Path(__file__).resolve().parent
OUT = {}


def s(v):
    return str(v)


def moment_simplex(expr, xs, ys):
    """Exact ∫ over 0<x1<...<xk<1 and 1>y1>...>yk>0.

    Monomial denominators are prefix sums of x exponents and suffix
    sums of y exponents, incremented by the integrated dimension.
    """
    k = len(xs)
    poly = sp.Poly(sp.expand(expr), *(xs + ys))
    ans = sp.Rational(0)
    for powers, coeff in poly.terms():
        ax, ay = powers[:k], powers[k:]
        den = 1
        acc = 0
        for i, v in enumerate(ax, 1):
            acc += v
            den *= acc + i
        acc = 0
        for i, v in enumerate(reversed(ay), 1):
            acc += v
            den *= acc + i
        ans += coeff / den
    return sp.factor(ans)


def geometry(k):
    xs = sp.symbols(f'x0:{k}')
    ys = sp.symbols(f'y0:{k}')
    nextx = xs[1:] + (sp.Integer(1),)
    u = xs[0] + sum((b-a)*y for a,b,y in zip(xs,nextx,ys))
    m1 = (xs[0]**2 + sum((b*b-a*a)*y*y for a,b,y in zip(xs,nextx,ys)))/4
    vis = sum(x*y for x,y in zip(xs,ys))
    return xs,ys,u,m1,vis


# Symbolic derivative signs, separate from any coordinate integration.
t,M,Z,A,C2,C3 = sp.symbols('t M Z A C2 C3')
series = sp.exp(-t*M-Z*t*t/2+Z*t**3/6-Z*t**4/24).series(t,0,5).removeO()
second = sp.expand(2*series.coeff(t,2))
fourth = sp.expand(24*series.coeff(t,4))
assert second == M*M-Z
assert sp.expand(fourth-(M**4-6*M*M*Z-4*M*Z+3*Z*Z-Z)) == 0
weighted = sp.exp(-t*A-C2*t*t/2+C3*t**3/6).series(t,0,3).removeO()
assert sp.expand(2*weighted.coeff(t,2)-(A*A-C2)) == 0
assert sp.expand(fourth-(M**4-6*M*M*Z+4*M*Z+3*Z*Z-Z)) != 0
OUT['derivative_signs'] = {'second':s(second),'fourth':s(fourth),
    'weighted_second':s(sp.expand(2*weighted.coeff(t,2))),
    'wrong_mixed_sign_rejected':True}


# Formal power coefficients around intensity m=0. For order ≤5, strata k>5
# cannot contribute. Finite coefficient calculation is exact, not truncation
# of a numerical Poisson experiment at some chosen intensity.
order = 5
m = sp.Symbol('m')
acc = {name:[sp.Rational(0) for _ in range(order+1)]
       for name in ['normalization','fourth_identity','weighted_variance']}
empty = {name:list(values) for name,values in acc.items()}
strata = []
for k in range(order+1):
    if k == 0:
        xs = ys = ()
        u,m1,vis = sp.Integer(1),sp.Rational(1,4),sp.Integer(0)
        integrate = lambda q: sp.expand(q)
    else:
        xs,ys,u,m1,vis = geometry(k)
        integrate = lambda q, xs=xs, ys=ys: moment_simplex(q,xs,ys)
        assert integrate(1) == sp.Rational(1,math.factorial(k)**2)
    centered = k-m*u
    polynomials = {
        'normalization':sp.Integer(1),
        'fourth_identity':centered**4-6*centered**2*m*u-4*centered*m*u+3*(m*u)**2-m*u,
        'weighted_variance':(vis-m*m1)**2,
    }
    exp_trunc = sum((-m*u)**r/sp.factorial(r) for r in range(order-k+1))
    krecord = {'k':k}
    for name,p in polynomials.items():
        # Take m coefficients before expanding the coordinate polynomial.
        coeffs = sp.Poly(sp.expand(p*exp_trunc),m)
        vals = [sp.Integer(0)]*k
        for r in range(order-k+1):
            q = coeffs.coeff_monomial(m**r)
            val = integrate(q)
            vals.append(val)
            acc[name][k+r] += val
            if k == 0:
                empty[name][k+r] = val
        krecord[name] = list(map(s,vals))
    strata.append(krecord)
assert acc['normalization'] == [1,0,0,0,0,0]
assert all(v == 0 for v in acc['fourth_identity'])
target = [sp.Integer(0)] + [sp.Rational((-1)**(r-1),math.factorial(r-1)*(r+2)**2)
                          for r in range(1,order+1)]
assert acc['weighted_variance'] == target
assert empty['weighted_variance'][2] == sp.Rational(1,16)
assert empty['fourth_identity'][4] != 0
OUT['exact_poisson_series'] = {
    'order':order,'strata_including_empty':order+1,
    'sums':{name:list(map(s,vals)) for name,vals in acc.items()},
    'weighted_integral_target':list(map(s,target)),
    'empty_contributions':{name:list(map(s,vals)) for name,vals in empty.items()},
    'omitting_empty_stratum_rejected':True,'strata':strata}


# Exact algebra of the posterior density ratio and finite high-precision
# checks of the analytical ≤3 bound. K,U values are test configurations,
# not stochastic samples or an estimate of a supremum.
rn = []
for n in [1,2,3,7,15,63,255,1023]:
    mm = mp.mpf(n+1)
    pm = mp.exp(-mm)*mm**n/mp.factorial(n)
    for k in sorted(set([1,min(n,2),min(n,5),n])):
        for us in ['0.001','0.1','0.25','0.5','0.75','0.99']:
            u = mp.mpf(us); d = 1-u
            direct = mp.factorial(n)/mp.factorial(n-k)*d**(n-k)/(mm**k*mp.exp(-mm*u))
            post = mp.exp(-mm*d)*(mm*d)**(n-k)/mp.factorial(n-k)/pm
            assert mp.almosteq(direct,post,rel_eps=mp.mpf('1e-64'))
            if u <= mp.mpf('.5'):
                assert post < 3
            rn.append({'n':n,'k':k,'U':us,'ratio':mp.nstr(post,22)})
maxchecks=[]
for mm in [2,3,4,7,16,64,1024,2**20]:
    den=mp.exp(-mm+mm*mp.log(mm)-mp.loggamma(mm+1))
    for ds in ['0.5','0.50001','0.7','0.9','1']:
        v=mm*mp.mpf(ds); k=int(mp.floor(v))
        pmf=mp.exp(-v+k*mp.log(v)-mp.loggamma(k+1))
        assert pmf <= 1/mp.sqrt(mp.pi*v)
        ratio=pmf/den
        assert ratio < 2*mp.exp(mp.mpf(1)/24) < 3
        maxchecks.append({'m':mm,'D':ds,'maximum_pmf_ratio':mp.nstr(ratio,22)})
OUT['posterior_ratio']={'algebra_cases':len(rn),'cases':rn,
    'max_mass_cases':maxchecks,'bound':mp.nstr(2*mp.exp(mp.mpf(1)/24),22)}


weighted_integrals=[]
for mm in [2,3,8,64,1024,2**20]:
    edges=sorted(set([mp.mpf(0),mp.mpf(1),mp.mpf(min(mm,10)),
                      mp.mpf(min(mm,100)),mp.mpf(mm)]))
    integrand=lambda u: mp.mpf(0) if u == 0 else u*u*(mp.log(mm)-mp.log(u))*mp.exp(-u)
    scaled=mp.quad(integrand,edges)
    upper=2*mp.log(mm)+mp.mpf(1)/9
    assert 0 < scaled <= upper
    weighted_integrals.append({'m':mm,'m2_E_A2':mp.nstr(scaled,30),
                               'upper':mp.nstr(upper,30)})
OUT['weighted_integral']={'cases':weighted_integrals,'certified_intervals':False}


# Exact rational record distributions check both the second and sixth
# moment bounds, separately from the symbolic factorial expansion.
q=sp.Symbol('q')
ff=lambda j:sp.prod(q-i for i in range(j))
assert sp.expand(q**6-sum(a*ff(j) for j,a in enumerate([0,1,31,90,65,15,1]))) == 0
dist=[Fraction(1)]
H=Fraction(0)
record=[]
for n in range(1,65):
    p=Fraction(1,n); new=[Fraction(0)]*(len(dist)+1)
    for k,v in enumerate(dist):
        new[k] += v*(1-p);new[k+1] += v*p
    dist=new; H+=p
    mom2=sum(Fraction(k*k)*v for k,v in enumerate(dist))
    mom6=sum(Fraction(k**6)*v for k,v in enumerate(dist))
    P6=H**6+15*H**5+65*H**4+90*H**3+31*H**2+H
    assert mom2 <= H*H+H
    assert mom6 <= P6
    record.append({'n':n,'second':s(mom2),'sixth':s(mom6),'sixth_bound':s(P6)})
OUT['record_moments']={'cases':64,'values':record}


# Finite scale diagnostics corroborate the proved asymptotic comparisons;
# they do not prove any eventual assertion or numerical leading constant.
scale=[]
for power in [8,12,16,20,24,32,48]:
    mm=mp.mpf(2)**power;n=mm-1;J=power;Jm=power
    logdelta=mp.log(J)-(n/2-1)/J
    Fm=46*(1+(1+mp.sqrt(2)*Jm)**2)
    Hn=mp.digamma(n+1)+mp.euler
    Vm=3*Fm+Hn*Hn+Hn+24*(2*mp.log(mm)+mp.mpf(1)/9)
    scale.append({'m_power_of_two':power,'log_m8_delta':mp.nstr(8*mp.log(mm)+logdelta,25),
                  'Vm_over_log2m':mp.nstr(Vm/mp.log(mm)**2,25),
                  'log4m_over_m2':mp.nstr(mp.log(mm)**4/mm**2,25)})
OUT['scale_diagnostics']={'proof_status':'diagnostics only','values':scale}
OUT['status']='PASS'
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('PASS: symbolic derivatives; exact PPP skyline coefficients through order 5;')
print(f'PASS: {len(rn)} posterior-ratio cases; {len(maxchecks)} Poisson maximum-mass cases;')
print('PASS: 6 weighted integrals; 64 exact record distributions; 7 scale diagnostics.')
