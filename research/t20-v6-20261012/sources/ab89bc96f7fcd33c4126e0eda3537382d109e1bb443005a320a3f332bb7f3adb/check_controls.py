#!/usr/bin/env python3
"""Exact finite corroboration, not a universal theorem/computability checker."""
from fractions import Fraction as F
from math import factorial, comb
import json

counts = {}
def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

def exp_interval(x, n=160):
    """Rational certified exp enclosure, using a positive Taylor series.
    For x>=0, tail after n is <= next_term/(1-x/(n+2)).
    Negative x uses reciprocal bounds. Tested arguments have |x|<=15.
    """
    if x == 0:
        return F(1), F(1)
    if x < 0:
        lo, hi = exp_interval(-x, n)
        return 1/hi, 1/lo
    assert x < n+2
    term = F(1)
    total = term
    for i in range(1,n+1):
        term *= x/i
        total += term
    next_term = term*x/(n+1)
    tail = next_term/(1-x/(n+2))
    return total, total+tail

models = [
    ([F(0),F(1),F(3)], [F(1,4),F(1,2),F(1,4)]),
    ([F(0),F(1,2),F(2)], [F(1,7),F(2,7),F(4,7)]),
]
for xs, ps in models:
    check('finite_model_mass',sum(ps)==1)
    moment = lambda r: sum(p*x**r for p,x in zip(ps,xs))
    for b in [F(1),F(2),F(3)]:
        C = sum(p*exp_interval(b*x)[1] for p,x in zip(ps,xs))
        for h in [-b/4, b/4, b/3]:
            c=b/2; q=abs(h)/c
            check('local_ratio',0<q<1)
            for r in range(6):
                blo=sum(p*x**r*exp_interval(-h*x)[0] for p,x in zip(ps,xs))
                bhi=sum(p*x**r*exp_interval(-h*x)[1] for p,x in zip(ps,xs))
                for R in [0,1,3,7,12]:
                    partial=sum((-h)**n*moment(r+n)/factorial(n) for n in range(R+1))
                    bound=C*factorial(r)/(b-c)**r*q**(R+1)
                    check('local_geometric_remainder',partial-bound<=blo<=bhi<=partial+bound)

# Signed segment, strict rational margins and common finite-step ratio.
for a in [F(1,3),F(1),F(5,2)]:
    for u in [-a+F(1,10),-a/2,F(0),F(1,4),F(4),F(17)]:
        if u<=-a: continue
        d=min(a,a+u)/2
        B=abs(u)+1
        N=int(2*B/d)+1
        h=u/N; q=2*B/(N*d)
        check('finite_step_margin',0<q<1)
        for j in range(N+1):
            b=a+j*h
            check('signed_segment_radius',b>d and abs(h)<b/2)

# Exact finite normalized semigroup controls. a=4 log 2, h=+/- log 2.
for ps in [[F(1,2),F(1,3),F(1,6)],[F(1,5),F(2,5),F(2,5)]]:
    xs=[0,1,2]
    def tilt(p,k):
        w=[p_i*F(2)**(-k*x) for p_i,x in zip(p,xs)]
        Z=sum(w)
        return [z/Z for z in w], Z
    for k in [-3,-2,-1,0,1,2,5,11]:
        direct,Z=tilt(ps,k)
        current=ps; prod=F(1)
        step=1 if k>=0 else -1
        for _ in range(abs(k)):
            current,z=tilt(current,step)
            prod*=z
        check('exact_tilt_semigroup',current==direct and prod==Z)
        for r in range(7):
            normalized=sum(p*x**r for p,x in zip(current,xs))
            raw=sum(p*x**r*F(2)**(-k*x) for p,x in zip(ps,xs))
            check('exact_raw_moment_transport',normalized==raw/Z)

# Explicit quotient error allocation inequality (equation 10).
for D in [F(1,10),F(1),F(3)]:
    for K in [F(0),F(1,4),F(5)]:
        eta=D/8
        for z in [D,2*D,7*D]:
            for n in [-K,F(0),K]:
                for dn in [-eta,F(0),eta]:
                    for dz in [-eta,F(0),eta]:
                        actual=abs((n+dn)/(z+dz)-n/z)
                        bound=2*eta/D+2*K*eta/D**2
                        check('quotient_error',actual<=bound)

# Cantor event coding and finite analogues of endpoint formulas.
def pair(e,t): return (e+t)*(e+t+1)//2+t
codes={}
for e in range(18):
    for t in range(18):
        j=1+pair(e,t)
        check('cantor_event_coding',j not in codes and j>=t)
        codes[j]=(e,t)
for events in [[],[(0,0)],[(0,3),(2,0),(4,7)],[(e,2*e+1) for e in range(10)]]:
    p={1+pair(e,t):F(1,4**(e+1))*F(2)**(-(1+pair(e,t))) for e,t in events}
    alpha=sum((F(1,4**(e+1)) for e,t in events),F(0))
    p0=1-sum(p.values())
    Z=p0+alpha
    check('endpoint_finite_normalizer',p0>=F(2,3) and 1<=Z<=F(4,3))
    check('endpoint_weight_cancellation',Z==p0+sum((mass*2**j for j,mass in p.items()),F(0)))
    check('endpoint_test_function',p0/Z>0 and p0/(p0/Z)==Z)
    for J in [1,3,7,15,31,63]:
        for r in range(7):
            tail=sum((F(j**r)*mass for j,mass in p.items() if j>J),F(0))
            # b=log 2>1/2; J odd makes the half-exponent dyadic.
            bound=F(factorial(r),3)*4**r*F(2)**(-(J+1)//2)
            check('damped_original_tail',tail<=bound)

# Digits 0 and 1 in base 4 are separated by a certified gap.
for e in range(14):
    w=F(1,4**(e+1)); later=w/3; precision=w/12; threshold=2*w/3
    check('halting_digit_gap',later+precision<threshold<w-precision)

# Finite-support endpoint family, with a=log 2 for exact arithmetic.
for j in range(2,81):
    D=1-F(1,j)+F(1,j*2**j)
    Z=1/D
    p=F(1,j*2**j)/D
    p0=1-p
    check('finite_support_D_Z',F(1,2)<=D<=1 and 1<=Z<=2)
    check('late_normalizer_error',abs(Z-1)<=F(2,j))
    check('finite_support_endpoint_mean',p*2**j*j/Z==1)
    check('finite_support_endpoint_law',p*2**j/Z==F(1,j) and p0/Z==1-F(1,j))
    for r in range(1,9):
        original=p*j**r
        bound=2*factorial(r-1)*4**(r-1)*F(2)**(-(j//2))
        check('finite_support_original_damping',original<=bound)
        check('finite_support_endpoint_moments',p*2**j*j**r/Z==j**(r-1))

# Bernstein mean and variance identities used for compact test integration.
for N in range(1,17):
    for y in [F(0),F(1,7),F(1,2),F(5,7),F(1)]:
        weights=[F(comb(N,i))*y**i*(1-y)**(N-i) for i in range(N+1)]
        check('bernstein_probability',sum(weights)==1)
        check('bernstein_mean',sum(w*F(i,N) for i,w in enumerate(weights))==y)
        variance=sum(w*(F(i,N)-y)**2 for i,w in enumerate(weights))
        check('bernstein_variance',variance==y*(1-y)/N and variance<=F(1,4*N))

report={'status':'PASS','checks':sum(counts.values()),'groups':counts,
        'arithmetic':'Exact Python fractions and rigorous rational exponential enclosures.',
        'scope':'Finite corroboration only. Does not prove universal effectivity, solve halting, or constitute kernel verification.'}
print(json.dumps(report,indent=2))
