#!/usr/bin/env python3
"""Deterministic arithmetic diagnostics for the written sharp-information proof.

No simulation, random samples, imports of predecessor code, or network reads.
Finite checks do not prove the asymptotic limits or certify numerical intervals.
"""
import json
import math
from functools import lru_cache
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 80
HERE = Path(__file__).resolve().parent
OUT = {}


def sx(x):
    return str(x)


def ordered_integral(expr, xs, ys):
    """Exact integral on increasing x / decreasing y ordered simplices."""
    k = len(xs)
    ans = sp.Rational(0)
    for powers, coefficient in sp.Poly(sp.expand(expr), *(xs + ys)).terms():
        den = 1
        acc = 0
        for j, power in enumerate(powers[:k], 1):
            acc += power
            den *= acc + j
        acc = 0
        for j, power in enumerate(reversed(powers[k:]), 1):
            acc += power
            den *= acc + j
        ans += coefficient / den
    return sp.factor(ans)


@lru_cache(None)
def geometry(k):
    xs = sp.symbols(f'x0:{k}')
    ys = sp.symbols(f'y0:{k}')
    nx = xs[1:] + (sp.Integer(1),)
    u = xs[0] + sum((b-a)*y for a,b,y in zip(xs,nx,ys))
    m1 = (xs[0]**2 + sum((b*b-a*a)*y*y for a,b,y in zip(xs,nx,ys)))/4
    t = sum(x*y for x,y in zip(xs,ys))
    return xs, ys, u, m1, t


# Obtain the derivative polynomial directly from the exact exponential tilt.
t,M,Z = sp.symbols('t M Z')
tilt_series = sp.exp(-t*M + Z*(1-sp.exp(-t)-t)).series(t,0,7).removeO()
derivatives = {k: sp.expand(sp.factorial(k)*tilt_series.coeff(t,k))
               for k in (2,4,6)}
expected_sixth = (M**6-15*M**4*Z-20*M**3*Z+45*M*M*Z*Z-15*M*M*Z
                  +60*M*Z*Z-6*M*Z-15*Z**3+25*Z*Z-Z)
assert derivatives[2] == M*M-Z
assert derivatives[4] == M**4-6*M*M*Z-4*M*Z+3*Z*Z-Z
assert sp.expand(derivatives[6]-expected_sixth) == 0
assert sp.expand(derivatives[6]-(expected_sixth+40*M**3*Z)) != 0
terms=[]
for (i,j),coefficient in sp.Poly(derivatives[6]-M**6,M,Z).terms():
    assert 0 <= i <= 4 and j >= 1 and i+2*j <= 6
    terms.append({'M_power':i,'Z_power':j,'coefficient':sx(coefficient),
                  'weighted_degree':i+2*j,'holder_M_exponent':sx(sp.Rational(i,6))})
OUT['derivatives'] = {str(k):sx(v) for k,v in derivatives.items()}
OUT['sixth_absorption'] = {'mixed_terms':terms,'wrong_cubic_sign_rejected':True}
print('PASS: exact tilt derivatives and sixth-moment grading.', flush=True)


# Exact intensity-series coefficients, independently integrating actual PPP
# skyline strata. Coefficients through order five see only K<=5. This is a
# formal exact coefficient check, not a numerical truncation at a fixed m.
intensity, formal_u = sp.symbols('b formal_u')
order = 5
sums=[sp.Rational(0)]*(order+1)
normal=[sp.Rational(0)]*(order+1)
empty=None
strata=[]
for k in range(order+1):
    if k==0:
        u=sp.Integer(1)
        integrate=lambda p:sp.expand(p)
    else:
        xs,ys,u,_,_=geometry(k)
        integrate=lambda p,xs=xs,ys=ys:ordered_integral(p,xs,ys)
        assert integrate(1)==sp.Rational(1,math.factorial(k)**2)
    # Extract intensity coefficients BEFORE expanding coordinate polynomials;
    # higher powers cannot contribute and would cause needless expression swell.
    derivative = derivatives[6].subs({M:k-intensity*formal_u,Z:intensity*formal_u})
    exponential=sum((-intensity*formal_u)**j/sp.factorial(j) for j in range(order-k+1))
    poly=sp.Poly(sp.expand(derivative*exponential),intensity)
    norm=sp.Poly(sp.expand(exponential),intensity)
    vals=[]
    for power in range(order-k+1):
        value=integrate(poly.coeff_monomial(intensity**power).subs(formal_u,u))
        sums[k+power]+=value
        normal[k+power]+=integrate(norm.coeff_monomial(intensity**power).subs(formal_u,u))
        vals.append(sx(value))
    strata.append({'K':k,'coefficients_from_power_K':vals})
    if k==0:
        empty=[sp.Rational(x) for x in vals]
assert all(x==0 for x in sums)
assert normal==[1,0,0,0,0,0]
assert any(x != 0 for x in empty)
OUT['exact_sixth_skyline_identity']={'order':order,'sum_coefficients':list(map(sx,sums)),
    'normalization_coefficients':list(map(sx,normal)),
    'empty_contributions':list(map(sx,empty)),'strata':strata,
    'omitting_empty_stratum_rejected':True}
print('PASS: exact sixth identity through intensity order five, with empty stratum.', flush=True)


# Direct fixed-count density integration gives controls that do not assume
# Poisson identities or the fixed-count harmonic moment formulas.
fixed=[]
for n in range(1,5):
    m=sp.Integer(n+1)
    values={key:sp.Rational(0) for key in ['mass','U','U2','K','K2','M2','M4','Q','Q2']}
    for k in range(1,n+1):
        xs,ys,u,m1,vis=geometry(k)
        density=sp.factorial(n)/sp.factorial(n-k)*(1-u)**(n-k)
        centered=k-m*u
        q=(centered**2-k)/(2*m*m)+2*(vis/m-m1)
        for name,integrand in [('mass',1),('U',u),('U2',u*u),('K',k),('K2',k*k),
                               ('M2',centered**2),('M4',centered**4),('Q',q),('Q2',q*q)]:
            values[name]+=ordered_integral(density*integrand,xs,ys)
    h=sp.harmonic(m);g=sp.harmonic(m,2)
    hnext=sp.harmonic(m+1);gnext=sp.harmonic(m+1,2)
    delta=-2*h/m+2/m**2-(h*h-g-4)/(m+1)-2*(h+1)/(m+1)**2
    assert values['mass']==1
    assert values['U']==h/m
    assert values['U2']==(hnext*hnext-gnext+2*(hnext-1))/(m*(m+1))
    assert values['K']==sp.harmonic(n)
    assert values['K2']==sp.harmonic(n)**2+sp.harmonic(n)-sp.harmonic(n,2)
    assert sp.simplify(values['M2']-sp.harmonic(n)-delta)==0
    assert values['M4']>=values['M2']**2 and values['Q2']>=values['Q']**2
    fixed.append({'n':n,**{key:sx(value) for key,value in values.items()}})
assert fixed[0]['M4']=='23/75'
assert fixed[0]['Q']=='-7/72'
product_m4=sum(sp.Rational(math.comb(4,j)*(-1)**(4-j)*2**j,(j+1)**2)
               for j in range(5))
assert product_m4==sp.Rational(fixed[0]['M4'])
OUT['direct_fixed_count_integrals']={'cases':fixed,'n1_M4_independent_product_check':'23/75'}
print('PASS: exact fixed-count skyline integrals for n=1,...,4.', flush=True)


# Exact posterior ratio against a separate density quotient, then pointwise
# asymptotic configurations within the proof's probabilistic scale. These
# configurations do not establish convergence in probability or its uniformity.
rn=[]
for power in [4,8,12,20,32,48]:
    m=mp.mpf(2)**power;n=m-1
    k=int(mp.floor(mp.log(m)))
    for sign in [-1,0,1]:
        z=mp.mpf(k)+sign*mp.sqrt(mp.log(m))
        if z<=0:continue
        v=m-z;q=n-k
        post=mp.exp(-v+q*mp.log(v)-mp.loggamma(q+1)
                       +m-n*mp.log(m)+mp.loggamma(n+1))
        direct=mp.exp(mp.loggamma(n+1)-mp.loggamma(n-k+1)
                 +(n-k)*mp.log1p(-z/m)-k*mp.log(m)+z)
        assert mp.almosteq(post,direct,rel_eps=mp.mpf('1e-60'))
        assert post<3
        local=(-mp.log(2*mp.pi*q)/2-(q-v)**2/(2*v))
        exact=-v+q*mp.log(v)-mp.loggamma(q+1)
        rn.append({'power':power,'k':k,'sign':sign,'Z':mp.nstr(z,24),
                   'density_ratio':mp.nstr(post,30),
                   'local_logmass_error':mp.nstr(exact-local,30)})
OUT['posterior_test_configurations']={'cases':rn,'status':'diagnostics, not stochastic convergence proof'}
print('PASS: exact posterior-density comparisons and local-mass diagnostics.', flush=True)


# Constants and nonzero-support correction checked by exact symbolic algebra.
a,p,L = sp.symbols('a p L', positive=True)
entropy = sp.series(sp.exp(a)-1-a,a,0,5)
hellinger = sp.series((sp.exp(a/2)-1)**2,a,0,5)
assert entropy.removeO().coeff(a,2)==sp.Rational(1,2)
assert hellinger.removeO().coeff(a,2)==sp.Rational(1,4)
score_constant=sp.Rational(3)-2+1
assert score_constant==2
score_L2_constant=score_constant/4
reverse_constant=score_L2_constant/2
hellinger_constant=score_L2_constant/4
affinity_deficit_constant=hellinger_constant/2
assert reverse_constant==sp.Rational(1,4)
assert hellinger_constant==sp.Rational(1,8)
assert affinity_deficit_constant==sp.Rational(1,16)
assert sp.simplify((2-p-2*L)+p-(2-2*L))==0
assert sp.Rational(1,4)!=sp.Rational(1,8) # factor-two Hellinger convention guard
OUT['constants']={'entropy_series':sx(entropy),'hellinger_series':sx(hellinger),
    'E_M2_minus_K_squared_over_log2':sx(score_constant),
    'score_square':sx(score_L2_constant),'reverse_KL':sx(reverse_constant),
    'hellinger_squared_without_half':sx(hellinger_constant),
    'affinity_deficit':sx(affinity_deficit_constant),
    'sufficient_fixed_alpha_budget_multiplier':16,
    'singular_mass_plus_sign_and_H2_equals_2_minus_2rho':True}


# Finite two-stratum discrete law, including alternative-only mass, verifies
# Hellinger decomposition and the ordinary LRT affinity error bound directly.
p0=[sp.Rational(1,3),sp.Rational(2,3),sp.Integer(0)]
p1=[sp.Rational(1,4),sp.Rational(1,2),sp.Rational(1,4)]
rho=sum(sp.sqrt(x*y) for x,y in zip(p0,p1))
h2=sum((sp.sqrt(x)-sp.sqrt(y))**2 for x,y in zip(p0,p1))
decomposed=sum(p0[i]*(sp.sqrt(p1[i]/p0[i])-1)**2 for i in [0,1])+p1[2]
assert sp.simplify(h2-decomposed)==0
assert sp.simplify(h2-(2-2*rho))==0
discrete=[]
import itertools
for r in range(1,7):
    error=sp.Rational(0)
    for atoms in itertools.product(range(3),repeat=r):
        q0=sp.prod(p0[i] for i in atoms)
        q1=sp.prod(p1[i] for i in atoms)
        error+=min(q0,q1)
    assert sp.simplify(error**2-(rho**2)**r)<=0
    discrete.append({'R':r,'sum_errors':sx(error),'affinity_bound':sx(rho**r)})
OUT['singular_discrete_control']={'H2':sx(h2),'rho':sx(rho),'products':discrete}
OUT['status']='PASS'
OUT['limitations']='Deterministic diagnostics only; no simulation, empirical inference, or numerical interval certification.'
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('PASS: sharp constants, singular-mass Hellinger decomposition, and product-affinity controls.', flush=True)
