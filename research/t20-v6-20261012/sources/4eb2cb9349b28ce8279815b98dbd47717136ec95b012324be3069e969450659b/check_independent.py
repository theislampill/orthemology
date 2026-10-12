#!/usr/bin/env python3
"""Independent exact finite controls; not a proof of the all-polynomial theorem."""
import argparse, hashlib, json
from pathlib import Path
import sympy as S

r,t,s,y,n,m = S.symbols('r t s y n m', positive=True)
q = r/(1+2*t*r)
K = r/S.Integer(8)*(1-1/(1+2*t*r))
checks=[]
def zero(name, expr):
    reduced = S.factor(S.together(expr))
    passed = reduced == 0
    checks.append({'name':name,'pass':passed})
    if not passed: raise AssertionError((name,str(reduced)))
def nonzero(name,expr):
    reduced=S.factor(S.together(expr))
    passed = reduced != 0
    checks.append({'name':name,'pass':passed,'nonzero_residual':str(reduced)})
    if not passed: raise AssertionError(name)

zero('radial_flow_derivative',S.diff(q,t)+2*q**2)
zero('radial_flow_semigroup',q.subs(t,t+s)-q.subs(r,r/(1+2*s*r)))
zero('integrated_killing_derivative',S.diff(K,t)-q**2/4)
zero('integrated_killing_initial_value',K.subs(t,0))
zero('integrated_killing_cocycle',K.subs(t,t+s)-K.subs(t,s)-K.subs(r,r/(1+2*s*r)))
zero('inverse_radial_forward',q.subs(r,y/(1-2*t*y))-y)
zero('inverse_radial_backward',(y/(1-2*t*y)).subs(y,q)-r)
zero('inverse_killing_exponent',K.subs(r,y/(1-2*t*y))-t*y**2/(4*(1-2*t*y)))
zero('support_gap',1/(2*t)-q-1/(2*t*(1+2*t*r)))
zero('radial_all_n_unnormalized_generator',n*S.diff(q,t)/q-S.diff(K,t)-(-2*n*q-q**2/4))
zero('homogeneous_all_degree_generator',-m*r/(1+2*t*r)-S.diff(K,t)-(-m*q-q**2/4))
zero('backward_test_all_homogeneous_degrees',S.diff(K,t)+m*r/(1+2*t*r)-r*(m+2*r*(-S.diff(K,r)-m*t/(1+2*t*r)))-r**2/4)
for degree in range(1,15):
    zero(f'nested_simplex_factor_n{degree}',S.prod(2*j for j in range(1,degree))*t**(degree-1)/S.factorial(degree-1)-(2*t)**(degree-1))
for dim in (1,2,3):
    xs=S.symbols('x0:'+str(dim)); R=sum(x*x for x in xs); F=R**2/4
    for i,x in enumerate(xs): zero(f'gradient_d{dim}_i{i}',S.diff(F,x)-R*x)
    zero(f'dissipation_gradient_norm_d{dim}',sum(S.diff(F,x)**2 for x in xs)-R**3)
    for power in range(0,7):
        lhs=sum(-R*x*S.diff(R**power,x) for x in xs)-F*R**power
        zero(f'radial_generator_d{dim}_n{power}',lhs+2*power*R**(power+1)+R**(power+2)/4)
    for power in range(1,7):
        for i,x in enumerate(xs):
            terms=S.Poly(S.expand(R**power-x**(2*power)),*xs).terms()
            passed=all(c>=0 and all(e%2==0 for e in exps) for exps,c in terms)
            checks.append({'name':f'sos_marginal_comparison_d{dim}_n{power}_i{i}','pass':passed})
            assert passed
# Formal normalized two-atom controls. No exponential approximations enter.
w1,w2,r1,r2=S.symbols('w1 w2 r1 r2', positive=True)
Z=w1+w2; E=(w1*r1**2+w2*r2**2)/(4*Z)
for power in range(0,6):
    moment=(w1*r1**power+w2*r2**power)/Z
    derivative=sum(S.diff(moment,w)*(-w*rr**2/4)+S.diff(moment,rr)*(-2*rr**2) for w,rr in ((w1,r1),(w2,r2)))
    rhs=-2*power*(w1*r1**(power+1)+w2*r2**(power+1))/Z-(w1*r1**(power+2)+w2*r2**(power+2))/(4*Z)+E*moment
    zero(f'normalized_two_atom_radial_n{power}',derivative-rhs)
# Non-vacuous exact mutation controls.
nonzero('reject_drift_factor_one',S.diff(q,t)+q**2)
nonzero('reject_wrong_killing_coefficient',S.diff(K,t)-q**2/2)
nonzero('reject_wrong_killing_sign',S.diff(K,t)+q**2/4)
nonzero('reject_inverse_plus_sign',q.subs(r,y/(1+2*t*y))-y)
nonzero('reject_removed_replicator_normalizer',E*(w1*r1+w2*r2)/Z)
nonzero('reject_forgotten_factorial',S.prod(2*j for j in range(1,5))*t**4-(2*t)**4)
nonzero('reject_polynomial_inverse_identity',(y/(1-2*t*y))-y)
# Complete exact support benchmark for an atom, normalized killing cancels.
zero('atomic_normalized_support_limit',S.limit(q,r,S.oo)-1/(2*t))
args=argparse.ArgumentParser();args.add_argument('--output',default='INDEPENDENT_RESULTS.json');a=args.parse_args()
out={'kind':'finite exact controls, not universal theorem proof','sympy_version':S.__version__,'count':len(checks),'pass':all(c['pass'] for c in checks),'checks':checks}
Path(a.output).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(json.dumps({'count':len(checks),'pass':out['pass'],'output':a.output},sort_keys=True))
