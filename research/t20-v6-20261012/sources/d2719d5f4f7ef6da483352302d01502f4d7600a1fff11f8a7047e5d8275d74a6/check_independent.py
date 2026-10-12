#!/usr/bin/env python3
"""Independent exact controls; these do not prove the universal analysis."""
import json
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
checks=[]
def ck(name,ok):
 v=bool(ok);checks.append({'name':name,'passed':v})
 if not v:raise AssertionError(name)
def zero(name,expr):ck(name,S.simplify(S.expand(expr))==0)
t,s,r,x,z,u,T,C,k,D,h,Q,P=S.symbols('t s r x z u T C k D h Q P',real=True)
# Work at polynomial coefficient level; time coefficients are never differentiated.
for n in range(8):
 actual=S.exp(-C*n*t)*((n*h**(n-1)*(C*h-Q) if n else 0)-(k*h+P)*h**n-C*n*h**n)
 remaining=-S.exp(-C*n*t)*((n*h**(n-1)*Q if n else 0)+P*h**n)
 zero(f'moving_clock_residual_n{n}',actual+k*S.exp(C*t)*S.exp(-C*(n+1)*t)*h**(n+1)-remaining)
cp,kp=S.symbols('cp kp',positive=True)
theta=kp*(S.exp(cp*t)-1)/cp
width=kp*(1-S.exp(-cp*t))/cp
zero('clock_derivative',S.diff(theta,t)-kp*S.exp(cp*t))
zero('clock_rescaling',S.exp(-cp*t)*theta-width)
zero('endpoint_width_ODE',S.diff(width,t)+cp*width-kp)
zero('zero_C_width_limit',S.limit(width,cp,0)-kp*t)
zero('zero_C_clock_limit',S.limit(theta,cp,0)-kp*t)
zero('endpoint_kernel_integral',S.integrate(kp*S.exp(-cp*(t-r)),(r,0,t))-width)
ck('reject_missing_exponential_clock',S.simplify(S.diff(kp*t,t)-kp*S.exp(cp*t))!=0)
ck('reject_wrong_width_sign',S.simplify(S.diff(kp*(S.exp(cp*t)-1)/cp,t)+cp*kp*(S.exp(cp*t)-1)/cp-kp)!=0)
# Uniform coefficient families: generic product identities cannot create time derivatives.
y=S.symbols('y',real=True)
for coords in [(x,),(x,y)]:
 H=S.Function('H')(*coords);p=S.Function('p')(*coords);chi=S.Function('chi')
 K=S.Function('K')(t,*coords);b=[S.Function('b'+str(i))(t,*coords) for i in range(len(coords))]
 bg=lambda f:sum(bb*S.diff(f,v) for bb,v in zip(b,coords))
 G=lambda f:bg(f)-K*f
 zero(f'fixed_energy_localization_d{len(coords)}',G(p*chi(H))-G(p)*chi(H)-p*bg(H)*S.diff(chi(H),H))
 U=S.Function('U')(t,*coords);cut=S.Function('cut')(*coords)
 zero(f'fixed_spatial_cutoff_d{len(coords)}',S.diff(cut*U,t)+G(cut*U)-cut*(S.diff(U,t)+G(U))-U*bg(cut))
 ck(f'no_coefficient_time_derivatives_d{len(coords)}',not any(v.expr==K or v.expr in b for v in (G(p*chi(H))).atoms(S.Derivative) if t in v.variables))
# Moving quadratic certificates, including all constant shifts.
Hq=1+x*x;V=(x-t)**2;bq=-2*(x-t)
Cq=T*T;Dq=T*T+S.Rational(1,2);kq=S.Rational(1,2)
zero('quadratic_drift_SOS',Cq*Hq-bq*S.diff(Hq,x)-(4*(x-t/2)**2+T*T*x*x+T*T-t*t))
zero('quadratic_killing_SOS',V+Dq-kq*Hq-((x-2*t)**2/2+T*T-t*t))
ck('reject_horizonless_certificate', (T*T-t*t).subs({T:1,t:2})<0)
# Independently write flow as a homogeneous part plus a forced integral.
X=lambda end,start,a:end-S.Rational(1,2)+(a-start+S.Rational(1,2))*S.exp(-2*(end-start))
A=z-s+S.Rational(1,2);tau=t-s
J=lambda end,start,a:(end-start)/4+(a-start+S.Rational(1,2))**2*(1-S.exp(-4*(end-start)))/4-(a-start+S.Rational(1,2))*(1-S.exp(-2*(end-start)))/2
ph=X(t,s,z);j=J(t,s,z)
zero('quadratic_two_time_ODE',S.diff(ph,t)+2*(ph-t))
zero('quadratic_initial_point',ph.subs(t,s)-z)
zero('quadratic_start_time_derivative',S.diff(ph,s)+(-2*(z-s))*S.diff(ph,z))
zero('quadratic_spatial_jacobian',S.diff(ph,z)-S.exp(-2*(t-s)))
zero('quadratic_two_time_cocycle',X(t,r,X(r,s,z))-ph)
zero('quadratic_killing_endpoint',S.diff(j,t)-(ph-t)**2)
zero('quadratic_killing_start',S.diff(j,s)-2*(z-s)*S.diff(j,z)+(z-s)**2)
zero('quadratic_killing_cocycle',J(r,s,z)+J(t,r,X(r,s,z))-j)
zero('quadratic_shifted_killing_start',S.diff(j+Dq*(t-s),s)-2*(z-s)*S.diff(j+Dq*(t-s),z)+(z-s)**2+Dq)
for degree in range(3):
 # Exact U_s calculation through its log weight, avoiding exponential simplification.
 f=ph**degree
 logweight=-j-Dq*(t-s)
 residual=S.diff(f,s)+f*S.diff(logweight,s)-2*(z-s)*(S.diff(f,z)+f*S.diff(logweight,z))-((z-s)**2+Dq)*f
 zero(f'quadratic_backward_test_degree{degree}',residual)
zero('transported_weight_log_ratio',J(t,0,-1)-J(t,0,0)-(1-S.exp(-2*t))/2)
zero('fixed_position_pure_killing_log_ratio',S.integrate(((-1-r)**2-(-r)**2),(r,0,t))-(t+t*t))
ck('transport_differs_from_pure_killing',S.simplify(J(t,0,-1)-J(t,0,0)-(t+t*t))!=0)
# The original unshifted mass fails even-derivative positivity at an interior time.
expr=V**2-bq*S.diff(V,x)-S.diff(V,t)
zero('transported_mass_second_derivative',expr-((x-t)**4+4*(x-t)**2+2*(x-t)))
zero('interior_negative_mass_curvature',expr.subs(x,t-S.Rational(3,8))+S.Rational(687,4096))
zero('negative_control_trajectory',X(S.log(2)/2,0,-S.Rational(1,4))-S.log(2)/2+S.Rational(3,8))
shifted=(V+Dq)**2-bq*S.diff(V+Dq,x)-S.diff(V+Dq,t)
ck('negative_control_does_not_transfer_to_shifted_mass',shifted.subs({T:1,x:t-S.Rational(3,8)})>0)
# A genuine continuous-only schedule: b_t=a(t)x, a(t)=|t-1/2| on [0,1].
# H=1+x², K=H, C=k=1, D=0, Q=1+(1-2a(t))x², P=0.
aL=S.Rational(1,2)-t;aR=t-S.Rational(1,2)
gL=t/2-t*t/2;gR=t*t/2-t/2+S.Rational(1,4)
zero('kink_integrated_coefficient_left',S.diff(gL,t)-aL)
zero('kink_integrated_coefficient_right',S.diff(gR,t)-aR)
zero('kink_integral_continuity',(gL-gR).subs(t,S.Rational(1,2)))
zero('kink_coefficient_continuity',(aL-aR).subs(t,S.Rational(1,2)))
for side,aa,gg in [('left',aL,gL),('right',aR,gR)]:
 zero(f'kink_flow_{side}',S.diff(z*S.exp(gg),t)-aa*z*S.exp(gg))
 zero(f'kink_SOS_certificate_{side}',Hq-aa*x*S.diff(Hq,x)-(1+(1-2*aa)*x*x))
zero('kink_flow_C1_matching',(S.diff(z*S.exp(gL),t)-S.diff(z*S.exp(gR),t)).subs(t,S.Rational(1,2)))
zero('kink_flow_second_derivative_jump',(S.diff(z*S.exp(gR),t,2)-S.diff(z*S.exp(gL),t,2)).subs(t,S.Rational(1,2))-2*z*S.exp(S.Rational(1,8)))
ck('kink_schedule_not_C1',S.diff(aL,t)!=S.diff(aR,t))
ck('kink_moment_path_not_C2_for_nonzero_initial_point',2*S.exp(S.Rational(1,8))>0)
out={'status':'PASS','checks':len(checks),'scope':'Finite independently written controls, including a continuous-coefficient C1/non-C2 discriminator; not a formal proof.','results':checks}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks)}))
