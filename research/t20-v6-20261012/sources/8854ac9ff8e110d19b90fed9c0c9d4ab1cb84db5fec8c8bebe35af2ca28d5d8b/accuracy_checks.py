"""Exact arithmetic probes, not a normative decision service.

Inputs to these mathematical helpers are exact Fraction values in the stated
unit-interval domains; no external parser or deployment API is provided.
"""
from fractions import Fraction as F


def brier(b,v,alpha):
    return alpha*(b[0]-v[0])**2+(1-alpha)*(b[1]-v[1])**2


def project_complements(b,alpha):
    t=alpha*b[0]+(1-alpha)*(1-b[1])
    return (t,1-t)


def uniform_coherent_repair(b,lower,upper,strict=True):
    assert len(b)==2 and all(0<=x<=1 for x in b)
    assert 0<lower<=upper<1
    m1=min(brier(b,(1,0),a) for a in [lower,upper])
    m0=min(brier(b,(0,1),a) for a in [lower,upper])
    total=m1+m0
    if total>1:exists=True
    elif total==1:exists=(m1*m0>0) if strict else True
    else:
        difference=4*m1*m0-(1-total)**2
        exists=(difference>0) if strict else (difference>=0)
    return {'exists':exists,'m_true':m1,'m_false':m0}


def convex_regret(p,q,generator):
    if generator=='quadratic':
        g=lambda x:x*x; derivative=lambda x:2*x
    elif generator=='complement_quartic':
        g=lambda x:(1-x)**4; derivative=lambda x:-4*(1-x)**3
    elif generator=='symmetric_quadratic':
        g=lambda x:x*x+(1-x)**2; derivative=lambda x:4*x-2
    elif generator=='symmetric_quartic':
        g=lambda x:x**4+(1-x)**4; derivative=lambda x:4*x**3-4*(1-x)**3
    else:raise ValueError('Unsupported generator')
    return g(p)-g(q)-derivative(q)*(p-q)
