#!/usr/bin/env python3
"""Independent algebra and rejection controls for the scalar-energy residual bridge."""
import json,math
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
checks=[]
def ck(name,ok):
    good=bool(ok);checks.append({'name':name,'passed':good})
    if not good:raise AssertionError(name)
def zero(name,expr):ck(name,S.simplify(S.expand(expr))==0)
x,y,z,h,xi=S.symbols('x y z h xi',real=True)
# SOS energy factorial bounds supply a common width for every polynomial weight.
for n in range(81):
    ck(f'CS_weighted_factorial_radius_n{n}',math.factorial(4*n)<=2**(4*n)*math.factorial(2*n)**2)
# The actual cubic valley beyond the narrow certificate.
u=x-y**3;H=1+u*u+y*y;R=x*x+y*y
b=(-S.diff(H,x),-S.diff(H,y))
def bg(p):return sum(v*S.diff(p,q) for v,q in zip(b,(x,y)))
def G(p):return bg(p)-H*p
Senergy=4*u*u+(-6*y*y*u+2*y)**2
zero('m3_energy_SOS',-bg(H)-Senergy)
for n in range(6):
    zero(f'abstract_energy_recursion_n{n}',G(H**n)+H**(n+1)+(n*H**(n-1)*Senergy if n else 0))
cc,C=S.symbols('cc C',positive=True)
old=((H-1+C)**2-cc*R).subs(x,y**3)
zero('m3_old_certificate_negative_lead',S.Poly(old,y).coeff_monomial(y**6)+cc)
zero('m3_polynomial_radius_elementary_square',2*u*u+2*y**6+y*y-R-(x-2*y**3)**2)
U,V=S.symbols('U V',real=True)
rem=S.Poly(S.expand(3*(1+U**2+V**2)+2*(1+U**2+V**2)**3-2*U**2-2*V**6-V**2),U,V)
ck('m3_radius_envelope_SOS_remainder',all(co>=0 and all(k%2==0 for k in mon) for mon,co in rem.terms()))
# Product rule and scalar Fourier identity: generic first-order coefficients.
for d in (1,2,3):
    X=(x,y,z)[:d]
    hh=S.Function('energy')(*X);p=S.Function('polynomial_test')(*X)
    chi=S.Function('cutoff');q=S.Function('coordinate_test')(*X)
    c0=S.symbols('c0');cs=S.symbols('c1:'+str(d+1))
    DD=lambda f:c0*f+sum(ci*S.diff(f,xx) for ci,xx in zip(cs,X))
    alpha=c0*p+sum(ci*S.diff(p,xx) for ci,xx in zip(cs,X))
    beta=p*sum(ci*S.diff(hh,xx) for ci,xx in zip(cs,X))
    zero(f'alpha_beta_product_d{d}',DD(p*chi(hh))-alpha*chi(hh)-beta*S.diff(chi(hh),hh))
    zero(f'alpha_beta_Fourier_d{d}',DD(p*S.exp(S.I*xi*hh))-S.exp(S.I*xi*hh)*(alpha+S.I*xi*beta))
    zero(f'localized_order_one_d{d}',DD(chi(hh)*q)-chi(hh)*DD(q)-q*sum(ci*S.diff(chi(hh),xx) for ci,xx in zip(cs,X)))
# A nontrivial scalar alpha/beta pair can cancel: neither need be zero.
# alpha=delta_0-delta_1, beta=Lebesgue[0,1].
for n in range(10):
    test=h**n
    av=test.subs(h,0)-test.subs(h,1)
    bv=S.integrate(S.diff(test,h),(h,0,1))
    zero(f'nonzero_scalar_pair_cancels_n{n}',av+bv)
ck('scalar_alpha_is_nonzero', (h.subs(h,0)-h.subs(h,1))==-1)
ck('scalar_beta_is_nonzero',S.integrate(1,(h,0,1))==1)
zero('scalar_pair_Fourier_cancellation',1-S.exp(S.I*xi)+(S.exp(S.I*xi)-1))
# Missing beta and wrong signs are genuine detectable errors.
ptest=1+x*x
chi_poly=lambda v:v**2
correct=G(ptest*chi_poly(H))
alpha_only=G(ptest)*chi_poly(H)
beta_term=ptest*bg(H)*2*H
zero('actual_m3_scalar_product',correct-alpha_only-beta_term)
ck('reject_missing_beta',S.expand(correct-alpha_only)!=0)
ck('reject_beta_sign_flip',S.expand(correct-alpha_only+beta_term)!=0)
ck('reject_killing_sign_flip',S.expand(correct-(bg(ptest)+H*ptest)*chi_poly(H)-beta_term)!=0)
# First-order compact distribution requires C1 control, not just uniform control.
for n in range(2,10):
    polynomial=S.chebyshevt(n,x)/n
    zero(f'Chebyshev_derivative_endpoint_n{n}',S.diff(polynomial,x).subs(x,1)-n)
    zero(f'Chebyshev_supnorm_scale_n{n}',polynomial.subs(x,1)-S.Rational(1,n))
# Coordinate Fourier polynomials do converge with derivatives on compact sets.
for n in range(1,11):
    P=sum((S.I*xi*x)**j/S.factorial(j) for j in range(n+1))
    Pprev=sum((S.I*xi*x)**j/S.factorial(j) for j in range(n))
    zero(f'compact_Fourier_derivative_n{n}',S.diff(P,x)-S.I*xi*Pprev)
# Energy localization polynomial Taylor has the distinct chain factor b.gradH.
for n in range(5):
    P=sum((S.I*xi*H)**j/S.factorial(j) for j in range(n+1))
    prev=sum((S.I*xi*H)**j/S.factorial(j) for j in range(n))
    zero(f'energy_Fourier_generator_n{n}',G(ptest*P)-G(ptest)*P-S.I*xi*ptest*bg(H)*prev)
# Nongradient energy control remains within scope; no convergence is inferred.
HR=1+x*x+y*y;rot=(-y,x)
zero('general_drift_rotation_S_zero',sum(v*S.diff(HR,q) for v,q in zip(rot,(x,y))))
ck('rotation_nonstationary_at_unit_point',[v.subs({x:1,y:0}) for v in rot]==[0,1])
# Scalar root-bound denominator zeros are isolated, so a threshold is required.
s,mm=S.symbols('s mm',real=True)
P=(s-1)*mm-(s*s+1)
zero('root_coefficient_ratio',(P.subs(mm,(s*s+1)/(s-1))))
ck('reject_all_s_denominator_nonzero',(s-1).subs(s,1)==0)
zero('polynomial_ratio_division',(s*s+1)/(s-1)-(s+1+2/(s-1)))
# Fixed spatial cutoff leaves no global derivative of the backward test.
N,K=S.symbols('N K',positive=True)
zero('spatial_cutoff_error_limit',S.limit(K/N,N,S.oo))
out={'status':'PASS','checks':len(checks),'scope':'Finite independent controls; universal measure/distribution proof reviewed in REVIEW.md, not mechanically proved.','results':checks}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks)}))
