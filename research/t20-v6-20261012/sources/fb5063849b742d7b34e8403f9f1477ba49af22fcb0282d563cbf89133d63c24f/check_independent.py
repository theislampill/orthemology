#!/usr/bin/env python3
"""Independent exact controls. No author/root checker imports or mutations."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

p = argparse.ArgumentParser()
p.add_argument('--output-dir', default='.')
args = p.parse_args()
out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)
checks = []

def zero(name, expression):
    entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    residuals = [s.simplify(s.together(x)) for x in entries]
    ok = all(x == 0 for x in residuals)
    checks.append({'name': name, 'passed': ok,
                   'residuals': [str(x) for x in residuals]})

c, q, a, b, x, y, z = s.symbols('c q a b x y z', real=True)
I = s.eye(2)
S = s.Matrix([[a,b],[b,a]])
Sd = 2*I-S-S*S
X = s.Matrix([y,z])
Sinv = S.inv()
Q = I-Sinv
score = (X.dot(Q*X)-s.trace(Q*S))/2
gaussian_density_tangent = (X.dot(Sinv*Sd*Sinv*X)-s.trace(Sinv*Sd))/2
transport_density_tangent = s.trace(Q)-(Sinv*X).dot(Q*X)
zero('full_gaussian_density_PDE_not_only_moments',
     gaussian_density_tangent-(transport_density_tangent-score))

S0 = s.Matrix([[1,c],[c,1]])
S0d = 2*I-S0-S0*S0
zero('initial_covariance_derivative', S0d-s.Matrix([[-c*c,-3*c],[-3*c,-c*c]]))
Q0 = I-S0.inv()
transport_action = s.trace(Q0*Q0*S0)
reaction_action = s.trace(Q0*S0*Q0*S0)/2
zero('initial_transport_action',transport_action-2*c*c/(1-c*c))
zero('initial_reaction_action',reaction_action-c*c)
full_KL_derivative = s.trace((I-S0.inv())*S0d)/2
zero('correct_initial_full_KL_dissipation',
     full_KL_derivative+c*c*(3-c*c)/(1-c*c))
zero('dissipation_equals_both_action_channels',
     full_KL_derivative+transport_action+reaction_action)

den=9-c*c*(1-q)**2
at=1-3*c*c*q*(1-q)/den
bt=9*c*q/den
St=s.Matrix([[at,bt],[bt,at]])
zero('all_time_covariance_Riccati_identity',-3*q*St.diff(q)-(2*I-St-St*St))
zero('all_time_initial_condition',St.subs(q,1)-S0)
zero('all_time_limit_condition',St.subs(q,0)-I)
plus=(3+c+2*c*q)/(3+c-c*q)
minus=(3-c-2*c*q)/(3-c+c*q)
zero('all_time_positive_eigenvalue_formulas',s.Matrix([at+bt-plus,at-bt-minus]))
zero('all_time_marginal_initial_velocity',(-3*q*s.diff(at,q)).subs(q,1)+c*c)
zero('exact_positive_variance_deficit',1-at-3*c*c*q*(1-q)/den)
G=(at-1-s.log(at))/2
Gdot=-3*q*s.diff(G,q)
Gddot=-3*q*s.diff(Gdot,q)
zero('initial_marginal_KL_first_derivative',Gdot.subs(q,1))
zero('initial_marginal_KL_second_derivative',Gddot.subs(q,1)-c**4/2)

# Normal conditional N(c*y,1-c^2) to standard Gaussian.
h=(c*c*y*y-c*c-s.log(1-c*c))/2
mean_h=-s.log(1-c*c)/2
zero('conditional_KL_centering',h-mean_h-c*c*(y*y-1)/2)
zero('conditional_reaction_variance_derivative',-c*c*(3-1)/2+c*c)

# Strict coarse representation/minimum gap: f(y,z)=z^2/2.
# At coarse N(0,1), variance tangent V=c^2 has potential V*(y^2-1)/6.
V=c*c
coarse_potential=V*(y*y-1)/6
coarse_velocity=s.diff(coarse_potential,y)
coarse_reaction=coarse_potential
coarse_score= -s.diff(coarse_velocity,y)+y*coarse_velocity+coarse_reaction
zero('coarse_minimum_realizes_full_score',coarse_score-c*c*(y*y-1)/2)
def std_moment(poly):
    ans=0
    for (power,), coefficient in s.Poly(s.expand(poly),y).terms():
        ans += coefficient*(0 if power%2 else (s.factorial2(power-1) if power else 1))
    return s.simplify(ans)
represented_cost=std_moment((c*c*(y*y-1)/2)**2)
minimum_cost=std_moment(coarse_velocity**2+coarse_reaction**2)
residual_cost=std_moment(coarse_velocity**2+(c*c*(y*y-1)/2-coarse_reaction)**2)
zero('strict_projected_representation_cost',represented_cost-c**4/2)
zero('strict_coarse_minimum_cost',minimum_cost-c**4/6)
zero('strict_nonminimality_residual_cost',residual_cost-c**4/3)
zero('strict_Pythagorean_coarse_identity',represented_cost-minimum_cost-residual_cost)
zero('full_four_term_norm_loss',s.Rational(3,2)-minimum_cost-(1+(1-c**4)/2+residual_cost))

# A 1/2 spatial contraction changes transport and reaction differently.
# Fine initial mean 2, variance 4, potential x^2/8.
fine_mdot=-(1+4)*s.Rational(1,4)*2
fine_vdot=-s.Rational(1,4)*4*(4+2)
projected=s.Matrix([fine_mdot/2,fine_vdot/4])
canonical=s.Matrix([-2,-3])
zero('contracting_map_projected_gaussian_vector',projected-s.Matrix([-s.Rational(5,4),-s.Rational(3,2)]))
zero('contracting_map_noncollinearity_determinant',s.Matrix.hstack(projected,canonical).det()-s.Rational(3,4))

# Same observed point, different hidden differential mobility.
T=s.Rational(2,3)*s.sin(x)+s.Rational(1,6)*s.sin(2*x)
zero('nonlinear_map_same_fibre',T.subs(x,0)-T.subs(x,s.pi))
zero('nonlinear_map_first_mobility',s.diff(T,x).subs(x,0)**2-1)
zero('nonlinear_map_second_mobility',s.diff(T,x).subs(x,s.pi)**2-s.Rational(1,9))

# Finite exact conditional variance check, including a contracting spatial map.
weights=[s.Rational(1,6),s.Rational(1,3),s.Rational(1,2)]
groups=[0,0,1]
vel=[s.Matrix([2,3]),s.Matrix([-1,4]),s.Matrix([5,-2])]
alpha=[s.Rational(2),s.Rational(2),s.Rational(-2)]
DT=s.Matrix([[s.Rational(1,2),0]])
nu={g:sum(w for w,h in zip(weights,groups) if h==g) for g in set(groups)}
vb={g:sum((w*(DT*v)[0] for w,h,v in zip(weights,groups,vel) if h==g),s.S(0))/nu[g] for g in nu}
ab={g:sum((w*r for w,h,r in zip(weights,groups,alpha) if h==g),s.S(0))/nu[g] for g in nu}
fine_cost=sum(w*(v.dot(v)+r*r) for w,v,r in zip(weights,vel,alpha))
coarse_cost=sum(nu[g]*(vb[g]**2+ab[g]**2) for g in nu)
spatial=sum(w*(v.dot(v)-(DT*v)[0]**2) for w,v in zip(weights,vel))
vv=sum(w*((DT*v)[0]-vb[g])**2 for w,g,v in zip(weights,groups,vel))
rr=sum(w*(r-ab[g])**2 for w,g,r in zip(weights,groups,alpha))
zero('finite_control_reaction_centered',sum(w*r for w,r in zip(weights,alpha)))
zero('finite_control_conditional_action_decomposition',fine_cost-coarse_cost-spatial-vv-rr)

receipt={'scope':'Independent exact algebraic controls, supplementary to written proof review.',
         'sympy_version':s.__version__, 'passed':all(v['passed'] for v in checks),
         'check_count':len(checks),'checks':checks,
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'analytical_limits':'Finite symbolic checks do not establish Hilbert projection, cutoff limits, path well-posedness, or historical priority.'}
(out/'INDEPENDENT_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':receipt['passed'],'check_count':len(checks),'output':str(out/'INDEPENDENT_CHECKS.json')}))
raise SystemExit(0 if receipt['passed'] else 1)
