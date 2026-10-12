"""Independent exact controls; does not modify the reviewed source or ancestor."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess
import sys
import sympy as s

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE = WORKSPACE / 'asymptotic-gibbs-transport-20261010'
EXPECTED = {
    'AUTHOR_MANIFEST.json': '1e8b0c4553d9f81944ec717ceb33bbbd9a1c6ed7b75f7901ecb30e1a0d7c5f6d',
    'RESULT.md': '251d825754c3bcdc7611bf8e133759a87e9b763a1d90d3c3700d64e930b897e5',
    'check_exact.py': '6344132a4bfee6b40ffd70d0d0010c1643515f9fe13790ea499c04ca95c90436',
    'INPUT_BINDING.json': 'c79d35a12221458f75966dda8221404b5e176592aaf6654f512bb344db3bc928',
}
checks = []
def check(label, condition, category='symbolic'):
    if condition is not True and condition != s.true:
        raise AssertionError((label, condition))
    checks.append({'name': label, 'category': category, 'status': 'PASS'})
def eq(label, lhs, rhs=0):
    difference = (lhs-rhs).replace(s.log, lambda u: s.log(s.factor(u), evaluate=False))
    check(label, s.simplify(s.expand_log(difference, force=True)) == 0)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for name, expected in EXPECTED.items():
    check('reviewed_source_unchanged_' + name, digest(SOURCE/name) == expected, 'source_hash')
    check('review_snapshot_matches_' + name, digest(ROOT/'inputs'/name) == expected, 'snapshot_hash')
binding=json.loads((ROOT/'inputs'/'INPUT_BINDING.json').read_text())
check('accepted_ancestor_hash', digest(Path(binding['path'])) == binding['sha256'], 'ancestor_hash')

# Run the frozen source checker only in the independent snapshot directory.
proc=subprocess.run([sys.executable, str(ROOT/'inputs'/'check_exact.py')],capture_output=True,text=True)
(ROOT/'AUTHOR_REPLAY.log').write_text(proc.stdout+proc.stderr)
check('author_checker_exit_zero', proc.returncode == 0, 'execution')
author=json.loads(proc.stdout)
check('author_checker_reports_pass', author['status'] == 'PASS', 'execution')
tree=ast.parse((ROOT/'inputs'/'check_exact.py').read_text())
assertions=sorted((node for node in ast.walk(tree) if isinstance(node,ast.Assert)), key=lambda n:n.lineno)
hash_assertions=[node for node in assertions if 'hashlib.sha256' in ast.unparse(node)]
check('author_assertion_count_is_seven_algebra_plus_one_hash',
      len(assertions)==8 and len(hash_assertions)==1 and author['exact_algebra_controls']==7
      and author['predecessor_hash_controls']==1, 'count_audit')

x=s.symbols('x',positive=True)
t=s.symbols('t',nonnegative=True)
a=s.symbols('a',positive=True)
F=lambda u:(u*u-1)**2/4
velocity=lambda u:u*(1-u*u)
primitive=lambda u:(u*u-1-s.log(u*u))/8
X=2/s.sqrt(4-3*s.exp(-2*t))
check('double_well_stationary_particles_minus_one_and_one',velocity(-1)==velocity(1)==0)
eq('double_well_initial_particle_two',X.subs(t,0),2)
eq('double_well_exact_ode',s.diff(X,t),velocity(X))
eq('double_well_exact_endpoint',s.limit(X,t,s.oo),1)
eq('double_well_tail_primitive_derivative',s.diff(primitive(x),x)*velocity(x),-F(x))
I2=(3-s.log(4))/8
eq('double_well_total_transient_cost',s.integrate((x*x-1)/(4*x),(x,1,2)),I2)
check('double_well_cost_strictly_positive',s.simplify(I2>0))
actual_a=s.exp(-I2)
check('double_well_actual_factor_strictly_between_zero_and_one',s.simplify(s.And(actual_a>0,actual_a<1)))

A=(2+a)/3
prior=[s.Rational(1,3)]*3
P=[1/(2+a),1/(2+a),a/(2+a)]
endpoint_prior=[s.Rational(1,3),s.Rational(2,3)]
r=[1,(1+a)/2]
eq('actual_three_particle_partition',sum(m*f for m,f in zip(prior,[1,1,a])),A)
eq('correct_endpoint_mass',P[1]+P[2],(1+a)/(2+a))
wrong=2*s.sqrt(a)/(1+2*s.sqrt(a))
eq('arithmetic_mean_endpoint_mass',endpoint_prior[1]*s.sqrt(a)/(endpoint_prior[0]+endpoint_prior[1]*s.sqrt(a)),wrong)
eq('strict_endpoint_difference_numerator',((1+a)/(2+a)-wrong)*(2+a)*(1+2*s.sqrt(a)),(1-s.sqrt(a))**2)
eq('jensen_gap_in_nonconstant_fibre',(1+a)/2-s.sqrt(a),(1-s.sqrt(a))**2/2)

# A fourth stationary particle at zero is a genuinely losing basin for this F.
# This controls the support restriction and retains the original probability reference.
check('fourth_particle_is_stationary_at_strictly_higher_energy',velocity(0)==0 and F(s.Integer(0))==s.Rational(1,4))
mu4=[s.Rational(1,4)]*4
A4=(2+a)/4
pi=[s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)]
star=[1/(2+a),1/(2+a),a/(2+a)]
cost=[0,0,-s.log(a)]
kl=lambda p,q:sum(v*s.log(v/w) for v,w in zip(p,q))
eq('arbitrary_admissible_test_probability',sum(pi),1)
objective=kl(pi,mu4[:3])+sum(v*i for v,i in zip(pi,cost))
eq('finite_J_density_identity_with_excluded_basin',objective,kl(pi,star)-s.log(A4))
eq('selected_optimizer_value_with_excluded_basin',kl(star,mu4[:3])+sum(v*i for v,i in zip(star,cost)),-s.log(A4))
eq('zero_transient_support_penalty_for_stationary_winners',2*s.Rational(1,2)*s.log(s.Rational(1,2)/s.Rational(1,3)),-s.log(s.Rational(2,3)))

# Neither KL nor the arithmetic transient cost alone is preserved by endpoint merging.
conditional_star=[1/(1+a),a/(1+a)]
conditional_prior=[s.Rational(1,2)]*2
conditional_cost=conditional_star[1]*(-s.log(a))
effective=-s.log((1+a)/2)
eq('conditional_gibbs_objective_is_effective_cost',kl(conditional_star,conditional_prior)+conditional_cost,effective)
endpoint_star=[1/(2+a),(1+a)/(2+a)]
eq('relative_entropy_chain_rule_for_actual_merged_fibre',kl(P,prior),kl(endpoint_star,endpoint_prior)+endpoint_star[1]*kl(conditional_star,conditional_prior))

# Source-compatible arbitrary-law stress test: F(x)=x^2/2, q=0,
# I(x)=x^2/4, x_n=2 sqrt(n log 2), and mu_n=1/(n(n+1)).
n=s.symbols('n',integer=True,positive=True)
pm=1/(n*(n+1))
xn=2*s.sqrt(n*s.log(2))
quadratic_X=xn*s.exp(-t)
eq('heavy_tail_initial_probability',s.summation(pm,(n,1,s.oo)),1)
eq('heavy_tail_actual_quadratic_cost',s.integrate(quadratic_X**2/2,(t,0,s.oo)),n*s.log(2))
check('heavy_tail_unweighted_conditional_mean_infinite',s.summation(pm*n*s.log(2),(n,1,s.oo)) == s.oo)
R=1-s.log(2)
eq('heavy_tail_exact_exponential_conditional_mean',s.summation(pm*s.Rational(1,2)**n,(n,1,s.oo)),R)
check('heavy_tail_exponential_mean_strictly_between_zero_and_one',s.simplify(s.And(R>0,R<1)))
TI=s.log(2)*(2*s.log(2)-1)/R
eq('heavy_tail_exact_finite_tilted_mean',s.summation(pm*s.Rational(1,2)**n*n*s.log(2),(n,1,s.oo))/R,TI)
check('heavy_tail_tilted_mean_finite_positive',TI.is_finite is True and s.simplify(TI>0))
# By direct summation of the log-density identity; all displayed series converge.
K=-s.log(R)-TI
eq('heavy_tail_gibbs_decomposition',K+TI,-s.log(R))
check('heavy_tail_finite_effective_cost_despite_infinite_arithmetic_cost',(-s.log(R)).is_finite is True)

out={
    'status':'PASS',
    'independent_checks_total':len(checks),
    'counts_by_category':{cat:sum(c['category']==cat for c in checks) for cat in sorted({c['category'] for c in checks})},
    'author_symbolic_assertion_lines':[n.lineno for n in assertions if n not in hash_assertions],
    'author_hash_assertion_lines':[n.lineno for n in hash_assertions],
    'checks':checks,
    'scope':'Independent symbolic and source-identity controls complement a written mathematical review. No formal proof, external peer review, or closure authority is claimed.'
}
(ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
