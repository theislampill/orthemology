#!/usr/bin/env python3
"""Deterministic quadrature controls, not sampling or certified error bounds."""
import json, math, hashlib, pathlib, platform
import numpy as np
import mpmath as mp
from numpy.polynomial.legendre import leggauss
mp.mp.dps=65

def density(x,y,c):
    t=x*y
    return c*np.exp((c-2)*np.log1p(-t))*(1-c*t)
def tail(x,y,c):
    return (1-x)**c+(1-y)**c-(1-x*y)**c

def integrate_strata(N,c,q):
    z,w=leggauss(q); z=(z+1)/2; w=w/2
    x=z[:,None]; y=z[None,:]
    k1=float(np.sum(w[:,None]*w[None,:]*N*density(x,y,c)*tail(x,y,c)**(N-1)))
    if N<2:return [k1]
    # x1=s, x2=s+(1-s)t, y2=u, y1=u+(1-u)v. Jacobian=(1-s)(1-u).
    t=z[:,None,None]; u=z[None,:,None]; v=z[None,None,:]
    ww=w[:,None,None]*w[None,:,None]*w[None,None,:]
    y2=u; y1=u+(1-u)*v
    k2=0.
    for s,ws in zip(z,w):
        x2=s+(1-s)*t
        # union mass = tail(s,y1)+tail(x2,y2)-tail(x2,y1)
        D=tail(s,y1,c)+tail(x2,y2,c)-tail(x2,y1,c)
        term=N*(N-1)*density(s,y1,c)*density(x2,y2,c)*D**(N-2)
        k2+=float(ws*np.sum(ww*term*(1-s)*(1-u)))
    return [k1,k2]

out={'kind':'deterministic quadrature and analytic controls; no random sampling',
     'python':platform.python_version(),'numpy':np.__version__, 'mpmath':mp.__version__,
     'quadrature':[]}
for N,c,label in [(1,1.,'uniform N=1'),(2,1.,'uniform N=2'),(3,1.,'uniform N=3'),(2,.5,'Joe hard pair n=1')]:
    for q in [12,24,48]:
        out['quadrature'].append({'law':label,'order':q,'stratum_masses_k1_k2':integrate_strata(N,c,q)})
exact_k2=mp.pi**2/12-mp.mpf('.5'); exact_k1=1-exact_k2
out['Joe_n1_exact']={'k1':str(exact_k1),'k2':str(exact_k2),'normalization':'1','conditional_K_on_common_support':'1 with probability 1'}
# Product integral identity int_square h(xy) = int_0^1 -log(t) h(t) dt.
I=mp.quad(lambda t: -mp.log(t)*(1-mp.mpf('.5')*t)/(2*(1-t)),[0,mp.mpf('.5'),1])
out['Joe_n1_independent_product_integral']={'E_F':str(1-I),'k1':str(2*(1-I)), 'abs_error':str(abs(2*(1-I)-exact_k1))}
# First moment from the actual N-route nondomination formula.
rows=[]
for n in [1,2,3,4,8,20]:
    c=mp.mpf(n)/(n+1); H=mp.harmonic(n)
    E=mp.quad(lambda t: -mp.log(t)*n*(1-t)**(n-2)*(1-c*t),[0,mp.mpf('.5'),1])
    delta=(mp.zeta(2)-1)/2 if n==1 else (H-1)/(n*n-1)
    rows.append({'n':n,'E0_K':str(H),'E1_K_quadrature':str(E),'delta_formula':str(delta),'abs_error':str(abs(E-H-delta)), 'singular_mass_upper':str(mp.mpf(1)/mp.factorial(n+1))})
out['first_moment']=rows
# Analytic conditional-hidden law: uniform N=2, K=1, skyline=(1/4,1/3).
# D rectangle area 1/2; remaining point uniform on D; upper subrectangle [1/2,1]x[1/2,1] mass 1/4.
out['conditional_hidden_control']={'law':'uniform N=2','skyline':['1/4','1/3'],'D_mass':'1/2','upper_half_square_conditional_probability':'1/2','density_ratio_integral':'(1/4)/(1/2)=1/2'}
# Compare direct strip and positive integrand formulas at deterministic points.
strip=[]
for c in [mp.mpf('.5'),mp.mpf(2)/3,mp.mpf(1)]:
    pts=[(mp.mpf('.1'),mp.mpf('.8')),(mp.mpf('.4'),mp.mpf('.5')),(mp.mpf('.8'),mp.mpf('.1'))]
    closed=mp.mpf(0); positive=mp.mpf(0); bounded=mp.mpf(0)
    for i,(a,y) in enumerate(pts):
        b=pts[i+1][0] if i+1<len(pts) else mp.mpf(1)
        closed+=(1-a)**c-(1-b)**c+(1-b*y)**c-(1-a*y)**c
        def fun(t):
            return c*(1-t)**(c-1)*(-mp.expm1(mp.log(y)+(1-c)*(mp.log1p(-t)-mp.log1p(-t*y))))
        positive+=mp.quad(fun,[a,b])
        lo=(1-b)**c; hi=(1-a)**c
        def bounded_fun(v):
            if c==1:return 1-y
            if v==0:return mp.mpf(1)
            r=v**(1/c)
            return -mp.expm1(mp.log(y)+(1-c)*(mp.log(v)/c-mp.log(1-y+y*r)))
        bounded+=mp.quad(bounded_fun,[lo,hi])
    strip.append({'c':str(c),'closed':str(closed),'positive_integral':str(positive),'abs_error':str(abs(closed-positive)),'bounded_integral':str(bounded),'bounded_abs_error':str(abs(closed-bounded))})
out['strip_controls']=strip
# Bounded controls: assertions are numerical formula checks, never proofs of error bounds.
for row in out['quadrature']:
    if row['law'].startswith('uniform'):
        N=int(row['law'][-1]); targets={1:[1.],2:[.5,.5],3:[1/3,.5]}[N]
        assert all(abs(a-b)<5e-13 for a,b in zip(row['stratum_masses_k1_k2'],targets))
joe=[r for r in out['quadrature'] if r['law']=='Joe hard pair n=1']
errors=[sum(abs(mp.mpf(v)-t) for v,t in zip(r['stratum_masses_k1_k2'],[exact_k1,exact_k2])) for r in joe]
assert errors[0]>errors[1]>errors[2] and errors[2]<mp.mpf('1e-4')
assert all(mp.mpf(r['abs_error'])<mp.mpf('1e-50') for r in rows)
assert all(mp.mpf(r['bounded_abs_error'])<mp.mpf('1e-50') for r in strip)
out['assertions']='PASS: uniform strata, retained Joe quadrature discrepancies, mean identities, bounded strip identities'
path=pathlib.Path(__file__).with_name('CONTROL_RESULTS.json'); path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
