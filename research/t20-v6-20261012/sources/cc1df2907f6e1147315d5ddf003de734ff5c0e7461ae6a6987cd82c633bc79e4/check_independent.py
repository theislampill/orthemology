#!/usr/bin/env python3
"""Independent exact controls; no author or participating-root imports."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', default='.')
args = parser.parse_args()
out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)
checks = []


def zero(name, value):
    items = list(value) if isinstance(value, S.MatrixBase) else [value]
    residuals = [S.factor(S.together(v)) for v in items]
    checks.append({'name': name, 'passed': all(v == 0 for v in residuals),
                   'residuals': [str(v) for v in residuals]})


b, y, e, z, B, V = S.symbols('b y e z B V', real=True)
s = S.symbols('s', positive=True)


def average(poly):
    """Exact independent Y~N(0,1), E~N(0,s) moments."""
    ans = 0
    for (i, j), coefficient in S.Poly(S.expand(poly), y, e).terms():
        if i % 2 or j % 2:
            continue
        mi = S.factorial2(i - 1) if i else 1
        mj = S.factorial2(j - 1) * s ** (j // 2) if j else 1
        ans += coefficient * mi * mj
    return S.factor(ans)


# Spatial derivatives use z fixed: e=z-b*y.
def dy(poly):
    return S.diff(poly, y) - b * S.diff(poly, e)


def dz(poly):
    return S.diff(poly, e)


log_rho_y = -y + b * e / s
log_rho_z = -e / s


def density_score(vy, vz, alpha):
    return S.expand(-dy(vy) - dz(vz) - log_rho_y * vy
                    - log_rho_z * vz + alpha)


score = b*b*(y*y-1)/2 + b*y*e + (s-1)*(e*e-s)/(2*s)
phi = b*b*(y*y-1)/6
F = score-phi
vy, vz, alpha = -dy(F), -dz(F), -F
bdot = -b*(s+2+b*b/3)
sdot = (1-s)*(s+2)+2*b*b
gaussian_score = bdot*y*e/s + sdot*(e*e-s)/(2*s*s)
zero('full_constrained_density_tangent_not_only_moments',
     density_score(vy, vz, alpha)-gaussian_score)
zero('constrained_y_velocity', vy-(-b*e/s+b*b*y/3))
zero('constrained_z_velocity', vz-(-b*y-(1-1/s)*e))
zero('constrained_reaction',
     alpha-(-b*b*(y*y-1)/3-b*y*e-(s-1)*(e*e-s)/(2*s)))
zero('constrained_total_mass',average(alpha))
zero('coarse_potential_equation',-S.diff(phi,y,2)+y*S.diff(phi,y)+phi-b*b*(y*y-1)/2)
zero('marginal_flux_reaction_cancel',
     -S.diff(b*b*y/3,y)+y*b*b*y/3-b*b*(y*y-1)/3)
zero('covariance_y_variance_stationary',average(y*y*gaussian_score))
zero('covariance_cross_derivative',average(y*(b*y+e)*gaussian_score)-bdot)
zero('conditional_variance_derivative',average(e*e*gaussian_score)-sdot)

Dc = average(vy*vy+vz*vz+alpha*alpha)
Dc_formula=(s-1)**2*(1/s+S.Rational(1,2))+b*b*(s+1+1/s)+b**4/3
zero('constrained_exact_dissipation',Dc-Dc_formula)
Df=average(dy(score)**2+dz(score)**2+score**2)
zero('full_exact_dissipation',Df-(Dc_formula+b**4/6))
zero('normal_projection_action',average(S.diff(phi,y)**2+phi**2)-b**4/6)
zero('gradient_normal_orthogonality',average(vy*S.diff(phi,y)+alpha*phi))
zero('Pythagorean_full_constrained_gap',Df-Dc-b**4/6)
KL=(b*b+s-1-S.log(s))/2
zero('KL_chain_rule_exact',S.diff(KL,b)*bdot+S.diff(KL,s)*sdot+Dc)

fvy=0
fvz=-dz(score)
falpha=-(score-b*b*(y*y-1)/2)
fbdot=-(1+s)*b
fsdot=(1-s)*(s+2)
fscore=fbdot*y*e/s+fsdot*(e*e-s)/(2*s*s)
zero('fibrewise_full_density_tangent',density_score(fvy,fvz,falpha)-fscore)
Dfib=average(fvz*fvz+falpha*falpha)
zero('fibrewise_exact_dissipation',
     Dfib-((s-1)**2*(1/s+S.Rational(1,2))+b*b*(1+s)))
zero('fibrewise_KL_chain_rule',S.diff(KL,b)*fbdot+S.diff(KL,s)*fsdot+Dfib)
zero('constrained_fibrewise_exact_gap',Dc-Dfib-b*b/s-b**4/3)
zero('reaction_recentering_difference_from_true_gradient',
     density_score(-dy(score),-dz(score),falpha)-
     (density_score(vy,vz,alpha)+density_score(-S.diff(phi,y),0,2*phi)))
naive_score=density_score(-dy(score),-dz(score),falpha)
naive_bdot=-b*(s+2)
zero('reaction_recentering_is_marginal_feasible',average(y*y*naive_score))
zero('reaction_recentering_exact_density_tangent',
     naive_score-naive_bdot*y*e/s-sdot*(e*e-s)/(2*s*s))
Dnaive=average(dy(score)**2+dz(score)**2+falpha**2)
zero('reaction_recentering_exact_dissipation_gap',Dc-Dnaive-b**4/3)
zero('reaction_recentering_KL_chain_rule',
     S.diff(KL,b)*naive_bdot+S.diff(KL,s)*sdot+Dnaive)

# Gaussian full constrained tangent metric for arbitrary (b_dot,s_dot).
c,d = S.symbols('c d', real=True)
potential=b*c*(y*y-1)/3+c*y*e+d*(e*e-s)/2
generic_score=density_score(dy(potential),dz(potential),potential)
generic_bdot=(1+2*s+b*b/3)*c-b*s*d
generic_sdot=-2*b*s*c+s*(s+2+2*b*b)*d
zero('all_gaussian_constrained_tangents_exact_density',
     generic_score-generic_bdot*y*e/s-generic_sdot*(e*e-s)/(2*s*s))
M=S.Matrix([[1+2*s+b*b/3,-2*b*s],[-2*b*s,2*s*(s+2+2*b*b)]])
Mf=S.diag(1+s,2*s*(s+2))
lam=S.Matrix([c,d/2])
zero('full_gaussian_tangent_mobility',M*lam-S.Matrix([generic_bdot,generic_sdot]))
zero('full_gaussian_tangent_action',
     average(dy(potential)**2+dz(potential)**2+potential**2)-(lam.T*M*lam)[0])
zero('full_mobility_determinant_positive_form',
     M.det()-2*s*(2*s*s+5*s+2+(7*s+8)*b*b/3+2*b**4/3))
zero('mobility_difference_first_diagonal',(M-Mf)[0,0]-(s+b*b/3))
zero('mobility_difference_determinant',(M-Mf).det()-4*s*b**4/3)
zero('mobility_gap_recovers_KL_gap',
     (S.Matrix([b,(s-1)/(2*s)]).T*(M-Mf)*S.Matrix([b,(s-1)/(2*s)]))[0]-b*b/s-b**4/3)

# The same tangent has distinct full and fibrewise minimum costs at identity.
zero('identity_full_same_density_tangent',
     density_score(B*e/3,B*y/3,B*y*e/3).subs({b:0,s:1})-B*y*e)
zero('identity_fibrewise_same_density_tangent',
     density_score(0,B*y/2,B*y*e/2).subs({b:0,s:1})-B*y*e)
zero('identity_full_minimum_cost',average((B*e/3)**2+(B*y/3)**2+(B*y*e/3)**2).subs(s,1)-B*B/3)
zero('identity_fibrewise_minimum_cost',average((B*y/2)**2+(B*y*e/2)**2).subs(s,1)-B*B/2)

# Author's rational nonminimal field-representation witness is checked directly.
Sigma0=S.Matrix([[1,S.Rational(1,2)],[S.Rational(1,2),1]])
Bf=S.Matrix([[-S.Rational(235,924),S.Rational(17,42)],
             [S.Rational(17,42),-S.Rational(43,231)]])
Vf=S.Matrix([[0,-S.Rational(7,8)],[-S.Rational(7,8),-S.Rational(3,16)]])
zero('author_rational_witness_full_tangent',-(Bf*Sigma0+Sigma0*Bf)-Sigma0*Bf*Sigma0-Vf)
Af=S.trace(Bf*Bf*Sigma0)+S.trace(Bf*Sigma0*Bf*Sigma0)/2
zero('author_rational_witness_minimum_action',Af-S.Rational(2489,7392))
zero('author_rational_witness_nonminimality_gap',S.Rational(53,96)-Af-S.Rational(199,924))

# Closed-form fibrewise correlated comparator.
c0,t=S.symbols('c0 t',real=True)
q=S.symbols('q',positive=True)
sf=(3-c0*c0-2*c0*c0*q)/(3-c0*c0+c0*c0*q)
bf=3*c0*S.exp(-2*t)/(3-c0*c0+c0*c0*S.exp(-3*t))
zero('fibrewise_closed_variance_ODE',-3*q*S.diff(sf,q)-(1-sf)*(sf+2))
zero('fibrewise_closed_variance_initial',sf.subs(q,1)-(1-c0*c0))
zero('fibrewise_closed_correlation_ODE',S.diff(bf,t)+(1+sf.subs(q,S.exp(-3*t)))*bf)
zero('fibrewise_closed_correlation_initial',bf.subs(t,0)-c0)

# Reviewer-participating sharp global KL rate; calculus sign proof is in review.
R=(s-1)**2*(1/s+S.Rational(1,2))-3*(s-1-S.log(s))
zero('global_rate_scalar_remainder_derivative',S.diff(R,s)-(s-1)**3/s**2)
zero('global_rate_scalar_remainder_minimum',R.subs(s,1))
zero('global_rate_six_exact_decomposition',Dc-6*KL-R-b*b*(s-1)**2/s-b**4/3)
zero('global_rate_six_linearization_sharp',S.limit(Dc.subs(s,1)/KL.subs(s,1),b,0)-6)
zero('positive_boundary_inward',sdot.subs(s,0)-(2+2*b*b))
u0=S.symbols('u0',nonnegative=True)
r=(-1+S.sqrt(9+8*u0))/2
zero('upper_barrier_root',(1-r)*(r+2)+2*u0)
zero('squared_correlation_derivative',2*b*bdot+2*b*b*(s+2+b*b/3))

receipt={'scope':'Independent exact controls and reviewer-participating extensions, supplemented by written proofs.',
         'sympy_version':S.__version__, 'passed':all(v['passed'] for v in checks),
         'check_count':len(checks),'checks':checks,
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'limits':'Symbolic equalities do not prove abstract Hilbert projection, cutoff limits, general PDE existence or uniqueness, inequality signs, or historical priority.'}
(out/'INDEPENDENT_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':receipt['passed'],'check_count':len(checks),
                  'output':str(out/'INDEPENDENT_CHECKS.json')}))
raise SystemExit(0 if receipt['passed'] else 1)
