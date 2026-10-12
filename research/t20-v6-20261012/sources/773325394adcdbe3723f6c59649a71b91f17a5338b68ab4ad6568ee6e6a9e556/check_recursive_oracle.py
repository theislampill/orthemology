#!/usr/bin/env python3
"""One composed approximate moment-oracle test outside the origin Taylor radius.

Exp(1): m_r=r!, a=5/6, M=6. Two steps h=2/3 reach u=4/3.
Only original-law moments are used as exact oracle inputs; intermediate
moments are computed recursively through certified finite series and division.
Analytic tilted moments are used only for final validation and the explicit
finite-test C_j, D certificates. This is corroboration, not a generic engine.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
import json
h=F(2,3); a=F(5,6); M=F(6); D=F(1,2)
stats={'oracle_calls':0,'series_evaluations':0,'largest_original_grade':0,'largest_R':0,'original_queries':0}

@lru_cache(None)
def fact(r): return factorial(r)

def bits_below(eps):
    k=0
    while F(1,2**k)>eps: k+=1
    return k

@lru_cache(None)
def oracle(stage,r,k):
    """Return a rational within 2^-k of the normalized stage moment."""
    stats['oracle_calls']+=1
    if stage==0:
        stats['original_queries']+=1
        stats['largest_original_grade']=max(stats['largest_original_grade'],r)
        return F(fact(r))
    eps=F(1,2**k)
    b=a+(stage-1)*h
    C=M*(1+(stage-1)*h)  # E_exp(bX) for the prior exact stage law.
    K=C*fact(r)/(b-h)**r
    eta=min(D/8,eps/(16*(1+K)))
    numerator=series(stage-1,r,eta)
    denominator=series(stage-1,0,eta)
    assert denominator>D/2
    # Equation (10), with errors strictly less than eta.
    assert 2*eta/D+2*K*eta/D**2<eps
    return numerator/denominator

@lru_cache(None)
def series(prior,r,eta):
    stats['series_evaluations']+=1
    b=a+prior*h
    C=M*(1+prior*h)
    c=(b+h)/2
    q=h/c
    assert 0<q<1
    coefficient=C*fact(r)/(b-c)**r
    R=0
    bound=coefficient*q
    while bound>eta/4:
        R+=1
        bound*=q
    stats['largest_R']=max(stats['largest_R'],R)
    # Sum of |(-h)^n/n!| is <2, since exp(2/3)<2.
    # This strict inequality follows, e.g., from log 2>2/3;
    # verify it below using an exact positive log series lower sum.
    upstream_k=bits_below(eta/8)
    partial=F(0)
    coefficient_n=F(1)
    absolute_sum=F(0)
    for n in range(R+1):
        partial+=coefficient_n*oracle(prior,r+n,upstream_k)
        absolute_sum+=abs(coefficient_n)
        coefficient_n*=(-h)/(n+1)
    assert absolute_sum<2
    assert bound+absolute_sum*F(1,2**upstream_k)<eta
    return partial

# log 2 = 2 sum_{n>=0} (1/3)^(2n+1)/(2n+1); two positive terms exceed 2/3.
assert 2*(F(1,3)+F(1,81))>h
# All actual stage local denominators (1+v)/(1+v+h) are >=D.
for prior in [0,1]:
    rate=1+prior*h
    assert rate/(rate+h)>D
    assert M*rate==rate/(rate-(a+prior*h))

cases=[]
for r,k in [(1,3),(2,3)]:
    approx=oracle(2,r,k)
    exact=F(fact(r))/(1+2*h)**r
    error=abs(approx-exact)
    assert error<F(1,2**k)
    cases.append({'grade':r,'requested_absolute_error':str(F(1,2**k)),
                  'verified_exact_answer':str(exact),'actual_error_less_than_requested':True,
                  'approximation_decimal_for_display':float(approx)})
report={'status':'PASS','model':'Exp(1), original m_r=r!, a=5/6, M=6',
        'steps':['2/3','2/3'],'target_u':'4/3','origin_actual_Taylor_radius':1,
        'intermediate_oracles':'Recursive approximate normalized moment names, with explicit rational series and division error budgets.',
        'cases':cases,'stats':stats,
        'claim_limit':'One finite corroboration of composition; no universal engine, complexity bound, or kernel claim.'}
print(json.dumps(report,indent=2))
