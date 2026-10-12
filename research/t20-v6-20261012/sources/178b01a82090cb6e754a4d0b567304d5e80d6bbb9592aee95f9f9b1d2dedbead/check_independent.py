#!/usr/bin/env python3
"""Independent exact controls for the nonnegative-SOS moving-well escape."""
import json
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
checks=[]
def ck(name,ok):
 v=bool(ok);checks.append({'name':name,'passed':v})
 if not v:raise AssertionError(name)
def zero(name,e):ck(name,S.factor(e)==0)
s=S.symbols('s',positive=True);x,z=S.symbols('x z',real=True)
f=1-5*s**5;a=s-s**6;W=x**4-a*x**5;V=W**2/2;b=-S.diff(V,x);X=1/s
zero('common_spatial_basis_expansion',V-(x**8/2-a*x**9+a*a*x**10/2))
zero('explicit_negative_gradient',b+x**7*(1-a*x)*(4-5*a*x))
zero('escape_ODE_direct',-f*S.diff(X,s)-b.subs(x,X))
zero('initial_state',X.subs(s,S.Rational(1,2))-2)
zero('polynomial_square_on_orbit',W.subs(x,X)-s)
zero('nonnegative_loss_on_orbit',V.subs(x,X)-s*s/2)
zero('total_energy_change',-f*S.diff(V.subs(x,X),s)+s*f)
zero('gradient_on_orbit',S.diff(V,x).subs(x,X)+f/s**2)
zero('gradient_square',S.diff(V,x).subs(x,X)**2-f*f/s**4)
zero('external_work',(-f*S.diff(V,s)).subs(x,X)-f*(1-6*s**5)/s**4)
zero('full_moving_energy_chain_rule',(-f*S.diff(V,s)).subs(x,X)-S.diff(V,x).subs(x,X)**2+s*f)
# Exact sign certificates on 0<=s<=1/2, written using 0<=z<=1.
zero('speed_lower_bound_factorization',f.subs(s,z/2)-S.Rational(27,32)-S.Rational(5,32)*(1-z)*sum(z**i for i in range(5)))
zero('positive_a_factorization',a-s*(1-s**5))
zero('work_second_factor_lower_bound', (1-6*s**5).subs(s,z/2)-S.Rational(13,16)-S.Rational(3,16)*(1-z)*sum(z**i for i in range(5)))
zero('endpoint_schedule_speed',(-f).subs(s,0)+1)
zero('endpoint_a_time_derivative',(-f*S.diff(a,s)).subs(s,0)+1)
zero('duration_upper_bound',S.Rational(1,2)/S.Rational(27,32)-S.Rational(16,27))
# Both zero branches are important: the common minimizer at 0 and the moving well.
zero('fixed_global_minimizer',V.subs(x,0))
zero('moving_global_minimizer',V.subs(x,1/a))
zero('distance_to_moving_minimizer',1/a-X-s**4/(1-s**5))
ck('distance_to_moving_minimizer_tends_zero',S.limit(1/a-X,s,0,dir='+')==0)
ck('moving_global_minimizer_escapes',S.limit(1/a,s,0,dir='+')==S.oo)
zero('endpoint_potential',V.subs(s,0)-x**8/2)
ck('frozen_endpoint_loss_on_orbit_diverges',S.limit((x**8/2).subs(x,X),s,0,dir='+')==S.oo)
ck('frozen_initial_loss_on_orbit_diverges',S.limit(V.subs(s,S.Rational(1,2)).subs(x,X),s,0,dir='+')==S.oo)
ck('moving_loss_tends_zero',S.limit(V.subs(x,X),s,0,dir='+')==0)
ck('first_moment_diverges',S.limit(X,s,0,dir='+')==S.oo)
# The exact killing is finite by an elementary common-integrand bound.
zero('killing_integrand',V.subs(x,X)/f-s*s/(2*f))
zero('killing_integral_lower_bound',S.integrate(s*s/2,(s,0,S.Rational(1,2)))-S.Rational(1,48))
zero('killing_integral_upper_bound',S.Rational(32,27)*S.Rational(1,48)-S.Rational(2,81))
# Direct generic-observable identity, not merely a list of monomials.
p=S.Function('p')
zero('generic_Dirac_chain_rule',-f*S.diff(p(1/s),s)-b.subs(x,X)*S.Subs(S.diff(p(x),x),x,1/s))
for poly in [S.Integer(1),x,x*x,1-2*x+3*x**4]:
 moment=poly.subs(x,X)
 zero('Dirac_covariance_'+str(poly),-(V*poly).subs(x,X)+V.subs(x,X)*moment)
# Representative fixed control ratios diverge; the universal claim is Gronwall.
H=1+x*x
ratio=(b*S.diff(H,x)/H).subs(x,X)
zero('fixed_quadratic_control_ratio',ratio-2*f/(s*(1+s*s)))
ck('fixed_quadratic_control_ratio_diverges',S.limit(ratio,s,0,dir='+')==S.oo)
D,k=S.symbols('D k',real=True)
zero('fixed_quadratic_killing_comparison',((V+D-k*H).subs(x,X))-(s*s/2+D-k*(1+s**-2)))
# Rejection controls guard against misleading energy/normalization interpretations.
ck('reject_frozen_energy_derivative',S.factor(-f*S.diff(V.subs(x,X),s)+S.diff(V,x).subs(x,X)**2)!=0)
ck('reject_orbit_is_exact_minimizer_before_endpoint',S.factor(V.subs(x,X))!=0)
ck('reject_endpoint_loss_can_follow_moving_limit',S.limit((x**8/2).subs(x,X),s,0,dir='+')!=S.limit(V.subs(x,X),s,0,dir='+'))
ck('negative_C_needs_max_in_uniform_Gronwall_bound',S.exp(-S.Rational(1,2))>S.exp(-1))
out={'status':'PASS','checks':len(checks),'scope':'Independent exact algebra/sign/discriminator controls; inverse-schedule regularity, coercivity and universal Gronwall are reviewed in writing.','results':checks}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks)}))
