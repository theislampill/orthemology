"""Independent bounded deterministic diagnostics. Not empirical evidence or proof."""
from pathlib import Path
import hashlib
import json
import math
import mpmath as mp
import numpy as np
from scipy.special import roots_legendre
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = '1c2fd5cf4e8006205cbd61562d88eb5da72d4952f335b17952540ec9f1a1d544'
TARGET = ROOT / 'full-face-threshold-kl-rate' / 'RESULT.md'
assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == EXPECTED

# Differentiate the original route-tail function, not the target H formula.
x, y, c = sp.symbols('x y c', positive=True)
z = x + y - x*y
S = x**c + y**c - z**c
sx = c * (x**(c-1) - (1-y)*z**(c-1))
sy = c * (y**(c-1) - (1-x)*z**(c-1))
sxy = c * z**(c-2) * (1-c*(1-x)*(1-y))
def canonical_residual(expr):
    # On the audited domain 0<x,y<1, all x,y,z are strictly positive.
    # Explicitly normalize integer power shifts: plain simplify did not
    # recognize the first-derivative identity on its first diagnostic run.
    shifts={x**(c-1):x**c/x, y**(c-1):y**c/y,
            z**(c-1):z**c/z, z**(c-2):z**c/z**2}
    return str(sp.simplify(expr.xreplace(shifts)))
symbolic = {
    'S_x_residual': canonical_residual(sp.diff(S, x)-sx),
    'S_y_residual': canonical_residual(sp.diff(S, y)-sy),
    'S_xy_residual': canonical_residual(sp.diff(S, x, y)-sxy),
}
assert all(v == '0' for v in symbolic.values())
u,v=sp.symbols('u v', real=True)
H=sp.Function('H')(u,v)
surv=sp.exp(-u-v+H)
bracket=1-sp.diff(H,u)-sp.diff(H,v)+sp.diff(H,u)*sp.diff(H,v)+sp.diff(H,u,v)
symbolic['density_ratio_residual']=str(sp.simplify(sp.diff(surv,u,v)/sp.exp(-u-v)-sp.exp(H)*bracket))
assert symbolic['density_ratio_residual']=='0'
symbolic['leading_squared_kernel_integral']=str(sp.integrate(sp.exp(-u)*(1-u)**2,(u,0,sp.oo))**2)
assert symbolic['leading_squared_kernel_integral']=='1'

mp.mp.dps=70
def direct_ratio(n,u,v):
    n=mp.mpf(n); m=n+1; c=n/m
    x=mp.exp(-u/n); y=mp.exp(-v/n); z=x+y-x*y
    S=x**c+y**c-z**c
    sx=c*(x**(c-1)-(1-y)*z**(c-1))
    sy=c*(y**(c-1)-(1-x)*z**(c-1))
    sxy=c*z**(c-2)*(1-c*(1-x)*(1-y))
    fxy=m*(m-1)*S**(m-2)*sx*sy+m*S**(m-1)*sxy
    return fxy*x*y/n**2*mp.exp(u+v)

point_controls=[]
for n,u0,v0 in [(1,.125,2),(2,3,.5),(8,1,1),(32,2,5),(128,.25,7),(512,4,.125)]:
    u0=mp.mpf(str(u0));v0=mp.mpf(str(v0));nmp=mp.mpf(n);c=nmp/(nmp+1)
    def Hfun(uu,vv):
        xx=mp.exp(-uu/nmp); yy=mp.exp(-vv/nmp)
        ss=xx**c+yy**c-(xx+yy-xx*yy)**c
        return (nmp+1)*mp.log(ss/(xx*yy)**c)
    hval=Hfun(u0,v0)
    hu=mp.diff(lambda a:Hfun(a,v0),u0)
    hv=mp.diff(lambda b:Hfun(u0,b),v0)
    huv=mp.diff(lambda a,b:Hfun(a,b),(u0,v0),(1,1))
    ratio_h=mp.exp(hval)*(1-hu-hv+hu*hv+huv)
    ratio_original=direct_ratio(n,u0,v0)
    aa=mp.expm1(u0/nmp);bb=mp.expm1(v0/nmp);q=c-2
    I=mp.quad(lambda ss:((1+bb*ss+aa)**(q+1)-(1+bb*ss)**(q+1))/(aa*(q+1)),[0,1])
    h_integral=c*(1-c)*aa*bb*I
    h_original=mp.expm1(hval/(nmp+1))
    point_controls.append({
        'n':n,'u':str(u0),'v':str(v0),
        'density_ratio_absolute_discrepancy':mp.nstr(abs(ratio_h-ratio_original),8),
        'positive_integral_absolute_discrepancy':mp.nstr(abs(h_integral-h_original),8),
        'scaled_density_perturbation':mp.nstr(nmp**2*(ratio_original-1),16),
        'limiting_kernel':mp.nstr((1-u0)*(1-v0),16),
    })
    assert abs(ratio_h-ratio_original)<mp.mpf('1e-60')
    assert abs(h_integral-h_original)<mp.mpf('1e-60')

def numeric_bulk(n,order):
    """Tensor Gauss-Legendre quadrature of centered entropy on [0,10 log n]^2."""
    nd=np.longdouble(n);m=nd+1;c=nd/m
    L=np.longdouble(10)*np.log(nd)
    nodes,weights=roots_legendre(order)
    nodes=np.asarray(nodes,dtype=np.longdouble);weights=np.asarray(weights,dtype=np.longdouble)
    nodes=(nodes+1)*L/2;weights=weights*L/2
    u=nodes[:,None];v=nodes[None,:]
    x=np.exp(-u/nd);y=np.exp(-v/nd);z=x+y-x*y
    S=x**c+y**c-z**c
    sx=c*(x**(c-1)-(1-y)*z**(c-1))
    sy=c*(y**(c-1)-(1-x)*z**(c-1))
    sxy=c*z**(c-2)*(1-c*(1-x)*(1-y))
    R=np.exp(u+v+np.log(x)+np.log(y)+(m-2)*np.log(S))*m/nd**2*((m-1)*sx*sy+S*sxy)
    delta=R-1
    assert np.min(R)>0
    psi=(1+delta)*np.log1p(delta)-delta
    small=np.abs(delta)<np.longdouble('.02')
    d=delta[small]
    series=np.zeros_like(d)
    for power in range(2,13):
        series+=(-1)**power*d**power/(power*(power-1))
    psi[small]=series
    f0=np.exp(-u-v)
    scaled=nd**4*np.sum(weights[:,None]*weights[None,:]*f0*psi)
    # This is an analytic upper bound for the omitted tail, not quadrature error.
    tail=nd**4*(2*np.log(np.longdouble('1.5'))+4*(L+1)+2)*np.exp(-L)
    return {'n':n,'order':order,'L':float(L),'scaled_bulk_entropy':float(scaled),
            'analytic_scaled_tail_upper_bound':float(tail),'sample_min_ratio':float(np.min(R)),
            'sample_max_transformed_density':float(np.max(f0*R))}

quadrature=[numeric_bulk(n,order) for n in (8,16,32,64,128,256,512) for order in (80,140)]
inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (
    TARGET,
    ROOT/'full-face-threshold-information'/'RESULT.md',
    ROOT/'arbitrary-face-replay-design'/'RESULT.md',
    ROOT/'arbitrary-face-replay-design'/'ASYMPTOTIC_DESIGN.md',
)}
out={'target_sha256':EXPECTED,'source_hashes':inputs,'symbolic_checks':symbolic,
     'high_precision_point_controls':point_controls,'bounded_quadrature':quadrature,
     'limits':'Finite deterministic controls only. Quadrature has no rigorous numerical error certificate; analytic proof, not these samples, establishes the asymptotic or tail bound.'}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
