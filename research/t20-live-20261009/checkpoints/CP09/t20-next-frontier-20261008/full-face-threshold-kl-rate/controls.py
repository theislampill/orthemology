"""Bounded deterministic diagnostics. No simulation and no proof by grid."""
from pathlib import Path
import hashlib
import json
import math
import mpmath as mp
import numpy as np
import sympy as sp
from scipy.special import roots_legendre

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 75
assertions = 0

def check(condition):
    global assertions
    assert condition
    assertions += 1

# Symbolic density and entropy-coefficient identities.
u, v = sp.symbols('u v', real=True)
H = sp.Function('H')(u, v)
expected = sp.exp(-u-v+H) * (1-sp.diff(H,u)-sp.diff(H,v)
             +sp.diff(H,u)*sp.diff(H,v)+sp.diff(H,u,v))
check(sp.simplify(sp.diff(sp.exp(-u-v+H),u,v)-expected) == 0)
check(sp.integrate(sp.exp(-u)*(1-u)**2, (u,0,sp.oo)) == 1)
z = sp.symbols('z', real=True)
psi_series = sp.series((1+z)*sp.log(1+z)-z,z,0,4).removeO()
check(sp.expand(psi_series - z*z/2 + z**3/6) == 0)
check(sp.integrate(sp.exp(-u)*(1-u),(u,0,sp.oo)) == 0)

def quantities(n, u, v):
    n=mp.mpf(n); m=n+1; c=n/m
    x=mp.exp(-u/n); y=mp.exp(-v/n); z=x+y-x*y
    S=x**c+y**c-z**c
    sx=c*(x**(c-1)-(1-y)*z**(c-1))
    sy=c*(y**(c-1)-(1-x)*z**(c-1))
    sxy=c*z**(c-2)*(1-c*(1-x)*(1-y))
    density=x*y/n**2*(m*(m-1)*S**(m-2)*sx*sy+m*S**(m-1)*sxy)
    h=m*mp.log(S)+u+v
    return S, density, h

def Hfunc(n, u, v):
    return quantities(n,u,v)[2]

max_density_error = mp.mpf(0)
max_marginal_error = mp.mpf(0)
for n in [1,2,8,32,128]:
    for a in ['0.01','0.3','1','4','12']:
        a=mp.mpf(a)
        max_marginal_error=max(max_marginal_error,abs(quantities(n,a,0)[0]**(n+1)-mp.exp(-a)))
        for b in ['0.03','0.7','3','10']:
            b=mp.mpf(b)
            S,dens,h=quantities(n,a,b)
            hu=mp.diff(lambda uu: Hfunc(n,uu,b),a)
            hv=mp.diff(lambda vv: Hfunc(n,a,vv),b)
            huv=mp.diff(lambda uu,vv: Hfunc(n,uu,vv),(a,b),(1,1))
            reconstructed=mp.exp(-a-b+h)*(1-hu-hv+hu*hv+huv)
            err=abs(dens-reconstructed)/dens
            max_density_error=max(max_density_error,err)
            check(err<mp.mpf('1e-65'))
            check(0<dens<=1+1/(mp.mpf(n)*(n+1)))
            check(h>=0)
check(max_marginal_error<mp.mpf('1e-65'))

# C2 error diagnostics at the origin, interior, and moving logarithmic edges.
# These are deliberately bounded checks, not a certification of a supremum.
c2_checks=[]
for n in [4,16,64,256,1024]:
    L=6*mp.log(n); p=1+L
    largest=mp.mpf(0)
    for a,b in [(0,0),(mp.mpf('0.3'),mp.mpf('1.7')),(L,0),(0,L),(L,L),(L,L/3)]:
        for i,j in [(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]:
            got=mp.diff(lambda uu,vv: Hfunc(n,uu,vv),(a,b),(i,j))
            target = {(0,0):a*b,(1,0):b,(0,1):a,(2,0):0,(1,1):1,(0,2):0}[(i,j)]/mp.mpf(n)**2
            normalized=abs(got-target)*n**3/p**4
            largest=max(largest,normalized)
            check(mp.isfinite(normalized))
    # The mathematical result needs only some uniform constant; this is a diagnostic.
    check(largest<1)
    c2_checks.append({'n':n,'L':float(L),'max_sampled_n3_error_over_(1+L)^4':float(largest)})

def bulk_entropy(n, order, L=50):
    # Tensor Gauss-Legendre quadrature of the nonnegative centered integrand.
    nodes, weights=roots_legendre(order)
    nodes=(nodes+1)*(L/2); weights=weights*(L/2)
    u=nodes[:,None]; v=nodes[None,:]
    m=n+1.; c=n/m
    x=np.exp(-u/n); y=np.exp(-v/n); z=x+y-x*y
    S=x**c+y**c-z**c
    sx=c*(x**(c-1)-(1-y)*z**(c-1))
    sy=c*(y**(c-1)-(1-x)*z**(c-1))
    sxy=c*z**(c-2)*(1-c*(1-x)*(1-y))
    logR=(np.log(x)+np.log(y)-2*np.log(n)+(m-2)*np.log(S)
          +np.log(m*(m-1)*sx*sy+m*S*sxy)+u+v)
    d=np.expm1(logR)
    # Stable power series psi(1+d)=sum_{k>=2}(-1)^k d^k/[k(k-1)].
    small=np.abs(d)<.1
    psi=np.empty_like(d)
    ds=d[small]
    value=np.zeros_like(ds)
    for k in range(18,1,-1):
        value=value*ds+((-1.)**k)/(k*(k-1))
    psi[small]=ds*ds*value
    psi[~small]=(1+d[~small])*logR[~small]-d[~small]
    check(np.all(psi>=-1e-24))
    integral=float(np.sum(weights[:,None]*weights[None,:]*np.exp(-u-v)*psi))
    return n**4*integral

quadrature=[]
for n in [8,16,32,64,128,256,512]:
    a=bulk_entropy(n,140); b=bulk_entropy(n,220)
    check(abs(a-b)<2e-7)
    tail=n**4*(4*(50+1)+2*math.log(1.5)+2)*math.exp(-50)
    quadrature.append({'n':n,'n4_centered_bulk_140_nodes':a,
                       'n4_centered_bulk_220_nodes':b,
                       'absolute_order_difference':abs(a-b),
                       'rigorous_n4_outside_box_upper_bound':tail})

result={'status':'PASS','kind':'Bounded symbolic identities and deterministic numerical diagnostics; no empirical sampling',
        'assertions':assertions,'result_sha256':hashlib.sha256((ROOT/'RESULT.md').read_bytes()).hexdigest(),
        'max_mp_relative_density_reconstruction_error':str(max_density_error),
        'max_mp_marginal_survival_error':str(max_marginal_error),
        'c2_sampled_checks':c2_checks,'bulk_quadrature':quadrature,
        'limitations':['No grid certifies the asymptotic theorem or a global derivative bound.',
                      'Quadrature errors are diagnosed by order comparison, not rigorous interval-enclosed.',
                      'The analytic tail bound is rigorous; the bulk quadrature values remain numerical diagnostics.',
                      'The sampled C2 diagnostic includes some small-n boxes outside the proof condition L<=n; those are checks only.']}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
