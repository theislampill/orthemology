#!/usr/bin/env python3
"""Independent exact escape and scope controls; Gronwall universality is a written proof."""
import json
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
checks=[]
def ck(name,ok):
 yes=bool(ok);checks.append({'name':name,'passed':yes})
 if not yes:raise AssertionError(name)
def zero(name,e):ck(name,S.simplify(S.expand(e))==0)
s=S.symbols('s',positive=True);x,t,y=S.symbols('x t y',real=True)
V=x*x/S.Integer(2)-(3*s+s*s)*x**3/3+s**3*x**4/4
b=-S.diff(V,x);X=s**-2
zero('negative_gradient_identity',b-((3*s+s*s)*x*x-s**3*x**3-x))
zero('exact_escape_ODE',-S.diff(X,s)-b.subs(x,X))
zero('escape_initial_condition',X.subs(s,1)-1)
# Independent scaled-coordinate invariant: Y=s²X solves this equation.
Yprime=(-2*s*x+s*s*b).subs(x,y/s**2)
zero('scaled_coordinate_equation',Yprime-y*(y-1)*(1+(2-y)/s))
zero('scaled_invariant_Y_one',Yprime.subs(y,1))
zero('endpoint_potential_degree_drop',V.subs(s,0)-x*x/2)
zero('endpoint_drift_is_stable',b.subs(s,0)+x)
ck('positive_frozen_quartic_lead',S.Poly(V,x).LC().is_positive)
ck('degree_uniformly_at_most_four',S.Poly(V,x).degree()==4)
ck('all_time_coefficients_polynomial',all(S.Poly(a.subs(s,1-t),t).degree()<=3 for a in S.Poly(V,x).all_coeffs()))
zero('frozen_energy_dissipation',S.diff(V,x)*b+S.diff(V,x)**2)
# Total moving energy and explicit work have opposite relevant signs.
energy=S.factor(V.subs(x,X))
zero('moving_energy_factored',energy-(2*s-9)/(12*s**5))
zero('total_energy_derivative_factored',-S.diff(energy,s)-(8*s-45)/(12*s**6))
zero('external_work_factored',(-S.diff(V,s)).subs(x,X)-(8*s+3)/(12*s**6))
zero('gradient_square',S.diff(V,x).subs(x,X)**2-4/s**6)
zero('full_energy_chain_rule',-S.diff(energy,s)-((-S.diff(V,s)).subs(x,X)-S.diff(V,x).subs(x,X)**2))
zero('negative_energy_interval_certificate',9-2*s-(7+2*(1-s)))
zero('negative_derivative_interval_certificate',45-8*s-(37+8*(1-s)))
ck('external_work_strictly_positive',(8*s+3)/(12*s**6)>0)
ck('moving_energy_diverges_negative',S.limit(energy,s,0,dir='+')==-S.oo)
ck('frozen_initial_energy_diverges_positive',S.limit(V.subs(s,1).subs(x,X),s,0,dir='+')==S.oo)
ck('first_moment_has_no_finite_endpoint',S.limit(X,s,0,dir='+')==S.oo)
# Killing integrates to unbounded positive mass, but normalized covariance still cancels.
J=S.integrate(-energy,s)
J=J-J.subs(s,1)
zero('integrated_killing_closed_form',J-(S.Rational(19,144)+S.Rational(1,18)*s**-3-S.Rational(3,16)*s**-4))
zero('integrated_killing_derivative',-S.diff(J,s)-energy)
ck('integrated_killing_diverges_negative',S.limit(J,s,0,dir='+')==-S.oo)
zero('mass_log_derivative',S.diff(J,s)+energy)
for p,name in [(S.Integer(1),'mass'),(x,'first'),(x*x,'second'),(x**5-3*x**2+7,'mixed')]:
 moment=p.subs(x,X)
 reaction=-(V*p).subs(x,X)+V.subs(x,X)*moment
 zero(f'Dirac_reaction_covariance_{name}',reaction)
 zero(f'normalized_hierarchy_{name}',-S.diff(moment,s)-(b*S.diff(p,x)).subs(x,X)-reaction)
# Every nonempty Hankel truncation has one-dimensional image and nonzero mass.
for n in (1,2,3):
 vec=S.Matrix([X**j for j in range(n+1)])
 matrix=S.Matrix(n+1,n+1,lambda i,j:X**(i+j))
 ck(f'Hankel_outer_product_{n}',matrix==vec*vec.T)
 ck(f'Hankel_rank_{n}',matrix.rank()==1)
# Representative ratios support, but do not replace, the universal Gronwall proof.
for m in (1,2,3):
 H=1+x**(2*m)
 ratio=(b*S.diff(H,x)/H).subs(x,X)
 zero(f'polynomial_common_control_ratio_m{m}',ratio-4*m/(s*(1+s**(4*m))))
 ck(f'polynomial_common_control_ratio_unbounded_m{m}',S.limit(ratio,s,0,dir='+')==S.oo)
# Reject common misunderstandings with exact nonzero residuals.
ck('reject_autonomous_energy_derivative_formula',S.simplify(-S.diff(energy,s)+S.diff(V,x).subs(x,X)**2)!=0)
ck('reject_negative_external_work_explanation',S.simplify((-S.diff(V,s)).subs(x,X))>0)
ck('reject_wrong_escape_power',S.simplify(-S.diff(1/s,s)-b.subs(x,1/s))!=0)
ck('reject_wrong_gradient_sign',S.simplify(-S.diff(X,s)+b.subs(x,X))!=0)
out={'status':'PASS','checks':len(checks),'scope':'Independent finite identities and rejection controls; C1 common-control impossibility rests on the reviewed Gronwall proof.','results':checks}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks)}))
