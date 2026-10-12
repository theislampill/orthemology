#!/usr/bin/env python3
"""Independent exact correlated-target review; imports no author/root code."""
import argparse
import json
from pathlib import Path
import sympy as S

p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args()
args.output_dir.mkdir(parents=True,exist_ok=True)
y,e,b,beta=S.symbols('y e b beta',real=True)
s,tau=S.symbols('s tau',positive=True)
d=b-beta
checks=[]
def equal(name,lhs,rhs=0):
    residual=S.simplify(S.expand(lhs-rhs))
    if residual!=0: raise RuntimeError(f'{name}: {residual}')
    checks.append({'name':name,'passed':True})
def dy(f):return S.diff(f,y)-b*S.diff(f,e)
def dz(f):return S.diff(f,e)
def moment(f):
    poly=S.Poly(S.expand(f),y,e);out=0
    for (iy,ie),c in poly.terms():
        if iy%2==0 and ie%2==0:
            out+=c*(S.factorial2(iy-1) if iy else 1)*(S.factorial2(ie-1) if ie else 1)*s**(ie//2)
    return S.simplify(out)
def cond(f):
    out=0
    for (ie,),c in S.Poly(S.expand(f),e).terms():
        if ie%2==0:out+=c*(S.factorial2(ie-1) if ie else 1)*s**(ie//2)
    return S.simplify(out)
q=S.log(tau/s)/2+(e+d*y)**2/(2*tau)-e**2/(2*s)
energy=(s+d*d)/ (2*tau)-S.Rational(1,2)+S.log(tau/s)/2
h=cond(q)
score=cond(dy(q))
equal('conditional_KL_formula',h,(s+d*d*y*y)/(2*tau)-S.Rational(1,2)+S.log(tau/s)/2)
equal('conditional_y_score_nonzero',score,-beta*d*y/tau)
equal('joint_KL_conditional_average',moment(q),energy)
phi=d*(b-3*beta)*(y*y-1)/(6*tau)
rg=-S.diff(score,y)+y*score+h-energy
Knu_phi=-S.diff(phi,y,2)+y*S.diff(phi,y)+phi
equal('coarse_positive_gradient',rg,d*(b-3*beta)*(y*y-1)/(2*tau))
equal('horizontal_multiplier_equation',Knu_phi,rg)
equal('horizontal_multiplier_centered',moment(phi))
ly=-y+b*e/s;lz=-e/s
vy=-dy(q)+S.diff(phi,y);vz=-dz(q);alpha=-(q-energy)+phi
rate=-dy(vy)-dz(vz)-vy*ly-vz*lz+alpha
M=S.Matrix([[1+2*s+b*b/3,-2*b*s],[-2*b*s,2*s*(s+2+2*b*b)]])
grad=S.Matrix([S.diff(energy,b),S.diff(energy,s)])
flow=-M*grad
bp=S.factor(flow[0]);sp=S.factor(flow[1])
equal('coordinate_b_equation',bp,(-(1+2*s+b*b/3)*d+b*(s-tau))/tau)
equal('coordinate_s_equation',sp,(2*b*s*d-(s+2+2*b*b)*(s-tau))/tau)
tangent=bp*y*e/s+sp*(e*e-s)/(2*s*s)
equal('full_density_PDE_not_only_moments',rate,tangent)
equal('full_marginal_density_derivative',cond(rate))
equal('density_mass_derivative',moment(rate))
equal('density_y_variance_derivative',moment(y*y*rate))
equal('density_covariance_derivative',moment(y*(b*y+e)*rate),bp)
equal('density_s_variance_derivative',moment(e*e*rate),sp)
Sig=S.Matrix([[1,b],[b,b*b+s]]);Star=S.Matrix([[1,beta],[beta,beta*beta+tau]])
B=Star.inv()-Sig.inv()-S.diag(d*(b-3*beta)/(3*tau),0)
dSig=-B*Sig-Sig*B-Sig*B*Sig
expected=S.Matrix([[0,bp],[bp,2*b*bp+sp]])
for i in range(2):
    for j in range(i,2):equal(f'full_covariance_matrix_{i}_{j}',dSig[i,j],expected[i,j])
D=moment(vy*vy+vz*vz+alpha*alpha)
equal('full_field_action_matches_mobility',D,(grad.T*M*grad)[0])
equal('KL_chain_rule_negative_action',S.diff(energy,b)*bp+S.diff(energy,s)*sp,-D)
equal('mobility_positive_determinant_decomposition',M.det(),2*s*(2*s*s+5*s+2+(7*s+8)*b*b/3+2*b**4/3))
Du=moment(dy(q)**2+dz(q)**2+(q-energy)**2)
Dh=moment(S.diff(phi,y)**2+phi**2)
equal('orthogonal_horizontal_action_decomposition',Du-D,Dh)
equal('explicit_horizontal_action',Dh,d*d*(b-3*beta)**2/(6*tau*tau))
wrong=d*d*(y*y-1)/(6*tau)
vw=-dy(q)+S.diff(wrong,y);aw=-(q-energy)+wrong
wrongrate=-dy(vw)-dz(vz)-vw*ly-vz*lz+aw
equal('product_h_only_variance_leak',moment(y*y*wrongrate),2*beta*d/tau)
equal('target_stationary_b',bp.subs({b:beta,s:tau}))
equal('target_stationary_s',sp.subs({b:beta,s:tau}))
equal('correlation_created_from_product',bp.subs({b:0,s:tau}),beta*(1+2*tau)/tau)
equal('product_initial_s_derivative',sp.subs({b:0,s:tau}))
equal('predecessor_b_equation_at_product_target',bp.subs({beta:0,tau:1}),-b*(s+2+b*b/3))
equal('predecessor_s_equation_at_product_target',sp.subs({beta:0,tau:1}),(1-s)*(s+2)+2*b*b)
equal('general_tau_product_target_b_zero_invariance',bp.subs({beta:0,b:0}))
# Correlated example whose missing score term is nonzero, using exact rationals.
witness={b:S.Rational(1,2),beta:S.Rational(1,3),s:S.Rational(3,4),tau:S.Rational(5,4)}
equal('rational_wrong_variance_leak_nonzero',moment(y*y*wrongrate).subs(witness),S.Rational(4,45))
if S.simplify(D.subs(witness)) <= 0:raise RuntimeError('nonstationary positive action witness failed')
checks.append({'name':'rational_nonstationary_positive_action','passed':True})
equal('matched_cross_covariance_not_conserved',bp.subs({b:beta}),beta*(s-tau)/tau)
equal('factored_positive_determinant',M.det(),2*s*(b*b+2*s+1)*(2*b*b+3*s+6)/3)
creation={b:0,beta:1,s:1,tau:1}
equal('standard_independent_correlation_creation_density',rate.subs(creation),3*y*e)
equal('standard_independent_correlation_creation_dissipation',D.subs(creation),3)
result={'status':'PASS','checks':checks,'count':len(checks),'scope':'Exact algebraic controls. Analytic compactness and convergence require the separate ordinary proof. No general PDE theorem or rate claim.'}
(args.output_dir/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
(args.output_dir/'verification.txt').write_text(f"PASS: {len(checks)} independent exact controls.\n")
print(f"PASS: {len(checks)} independent exact controls.")
