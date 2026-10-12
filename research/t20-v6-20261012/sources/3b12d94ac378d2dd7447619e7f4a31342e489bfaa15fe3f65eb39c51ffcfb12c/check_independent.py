#!/usr/bin/env python3
"""Independent finite algebra/discriminator controls, not a theorem prover."""
import json, math
from pathlib import Path
import sympy as S
ROOT = Path(__file__).resolve().parent
checks = []
def check(name, value):
    ok = bool(value)
    checks.append({'name': name, 'passed': ok})
    if not ok: raise AssertionError(name)
def zero(name, expr): check(name, S.simplify(S.expand(expr)) == 0)
x,y,z,t,h,c = S.symbols('x y z t h c', real=True)
r = x*x+y*y
u = x-y*y
F = u*u+y*y
H = F+1
coords=(x,y)
b = [-S.diff(F,v) for v in coords]
def drift(p, field=b): return sum(bi*S.diff(p, v) for bi,v in zip(field,coords))
grad2 = sum(S.diff(F,v)**2 for v in coords)
zero('curved_energy_SOS', H**2-r-(u**4+u**2+(u*y)**2+((u-1)*y)**2+1))
zero('curved_gradient_energy_dissipation', -drift(H)-grad2)
for n in range(7):
    expected = -H**(n+1) if n==0 else -n*H**(n-1)*grad2-H**(n+1)
    zero(f'energy_generator_n{n}', drift(H**n)-H**(n+1)-expected)
    if n:
        factor = sum((H**2)**(n-1-j)*r**j for j in range(n))
        zero(f'SOS_power_difference_n{n}', H**(2*n)-r**n-(H**2-r)*factor)
# The generic power identity requires SOS factors, not positivity of all nonnegative polynomials.
U,V = S.symbols('U V')
for n in range(1,13):
    zero(f'generic_power_difference_n{n}', U**n-V**n-(U-V)*sum(U**(n-1-j)*V**j for j in range(n)))
radial = x*S.diff(F,x)+y*S.diff(F,y)
zero('curved_radial_outward_region', radial.subs(x,S.Rational(3,2)*y*y)-(-y**4/S.Integer(2)+2*y*y))
kappa,lam,D = S.symbols('kappa lam D')
Q = (radial-kappa*r*r+lam*r+D).subs(x,S.Rational(3,2)*y*y).expand()
zero('old_radial_certificate_leading_obstruction', Q.coeff(y,8)+S.Rational(81,16)*kappa)
check('negative_radial_witness_y3', radial.subs({x:S.Rational(27,2),y:3})<0)
# General polynomial drift with exact Lyapunov SOS; skew motion is admitted.
HR=1+r
rot=(-y,x)
zero('rotation_D_zero',drift(HR,rot))
zero('rotation_coercive_certificate',HR**2-r-(r*r+r+1))
phirot=(x*S.cos(t)-y*S.sin(t), x*S.sin(t)+y*S.cos(t))
zero('rotation_radius_preserved',sum(q*q for q in phirot)-r)
zero('rotation_flow_first',S.diff(phirot[0],t)+phirot[1])
zero('rotation_flow_second',S.diff(phirot[1],t)-phirot[0])
check('rotation_nonstationary_circle_witness', [S.diff(q,t).subs({x:1,y:0,t:0}) for q in phirot]==[0,1])
for n in range(7): zero(f'rotation_energy_chain_n{n}', drift(HR**n,rot)-HR**(n+1)+HR**(n+1))
# Mobility uses M=B^T B, which certifies D as a sum of actual polynomial squares.
B=S.Matrix([[1,x],[0,1]])
M=B.T*B
grad=S.Matrix([S.diff(F,x),S.diff(F,y)])
bm=-M*grad
DM=-(grad.T*bm)[0]
zero('mobility_D_SOS',DM-sum(v*v for v in B*grad))
zero('mobility_det_one',M.det()-1)
zero('mobility_positive_leading_minor',M[0,0]-1)
# Exact unnormalization and quotient-rule cancellation, including the constant shift.
Ap,AFp,AHp,Abp,Apprime,a,LF,C=S.symbols('Ap AFp AHp Abp Apprime a LF C', nonzero=True)
zero('quotient_shift_cancellation',(Abp-AFp-C*Ap)/a+(LF+C)*Ap/a-(Abp/a-AFp/a+LF*Ap/a))
# Finite simplex volume is h^n/n!, with no fake factorial cancellation.
for n in range(1,30):
    zero(f'iterated_energy_simplex_n{n}',S.integrate(h**(n-1)/S.factorial(n-1),(h,0,t))-t**n/S.factorial(n))
    check(f'factorial_Carleman_bound_n{n}',math.factorial(2*n)<=(2*n)**(2*n))
# A quadratic member has unbounded positive-time support, despite all certificates.
Fq=x*x; Hq=1+x*x; phiq=S.exp(-2*t)*x
Kq=t+(1-S.exp(-4*t))*x*x/4
zero('quadratic_coercive_SOS',Hq**2-x*x-(x**4+x*x+1))
zero('quadratic_flow',S.diff(phiq,t)+2*phiq)
zero('quadratic_killing_integral',S.diff(Kq,t)-(1+phiq**2))
for j in range(5):
    Uq=S.exp(-Kq)*phiq**j
    # U(t,x) is the forward semigroup, so d_t U = b.d_x U-H U.
    zero(f'quadratic_backward_test_j{j}',S.diff(Uq,t)-(-2*x*S.diff(Uq,x)-Hq*Uq))
# Exact controls discriminate frequently tempting incorrect variants.
check('reject_missing_dissipation',S.expand(drift(H)-H**2+H**2)!=0)
check('reject_wrong_energy_chain_sign',S.expand(drift(H)-H**2-(-grad2+H**2))!=0)
check('reject_wrong_backward_sign',S.simplify(S.diff(S.exp(-Kq),t)+(-2*x*S.diff(S.exp(-Kq),x)-Hq*S.exp(-Kq)))!=0)
check('reject_wrong_shift_cancellation',S.simplify((Abp-AFp-C*Ap)/a+LF*Ap/a-(Abp/a-AFp/a+LF*Ap/a))!=0)
check('reject_wrong_mobility_factor',S.expand(DM-sum(v*v for v in B.T*grad))!=0)
check('quadratic_flow_has_nonzero_slope', S.simplify(S.diff(phiq,x)).is_positive is True)
# Cutoff residual scaling: any uniform polynomial-drift moment suffices.
N,Kb,Kf,Kchi=S.symbols('N Kb Kf Kchi', positive=True)
zero('cutoff_residual_limit',S.limit(Kf*Kchi*Kb/N,N,S.oo))
# Independent checks for the frozen mobility/Hessian appendix.
energy1=x*x/2
H1=1+energy1
M1=1+x*x
phase=z*S.exp(-t)/S.sqrt(1+z*z*(1-S.exp(-2*t)))
D1=1+z*z*(1-S.exp(-2*t))
zero('appendix_mobility_ODE',S.diff(phase,t)+phase*(1+phase**2))
zero('appendix_mobility_integrated_F',S.diff(S.log(D1)/4,t)-phase**2/2)
zero('appendix_mobility_H_weight',S.diff(S.exp(-t)*D1**(-S.Rational(1,4)),t)+(1+phase**2/2)*S.exp(-t)*D1**(-S.Rational(1,4)))
psi=x*S.atan(x)-S.log(1+x*x)/2
zero('appendix_Hessian_inverse_mobility',S.diff(psi,x,2)*M1-1)
zero('appendix_geodesic_coordinate',S.diff(S.asinh(x),x)**2*M1-1)
zero('appendix_dual_gradient_ODE',S.diff(S.atan(x),x)*(-x*M1)+x)
zero('appendix_sine_dual_decay',S.diff(x/S.sqrt(1+x*x),x)*(-x*M1)+x/S.sqrt(1+x*x))
a1,a2,v1,v2,g1,g2,p1,p2=S.symbols('a1 a2 v1 v2 g1 g2 p1 p2',real=True)
w=S.symbols('w',positive=True)
fp,fq=S.symbols('fp fq',real=True)
E=w*fp+(1-w)*fq
zero('appendix_Fisher_weight_pairing',a1*(fp-E)-a1*(fq-E)-a1*(fp-fq))
vect=S.Matrix([v1,v2]);gg=S.Matrix([g1,g2]);pg=S.Matrix([p1,p2])
zero('appendix_M_metric_pairing',(M*gg).dot(M.inv()*vect)-gg.dot(vect))
zero('appendix_M_cometric',(M*gg).dot(M.inv()*M*pg)-gg.dot(M*pg))
result={'scope':'Finite exact algebra and adversarial controls; universal analysis reviewed in REVIEW.md, not mechanically proved here.', 'count':len(checks),'passed':all(q['passed'] for q in checks),'checks':checks}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'count':len(checks),'passed':result['passed']}))
