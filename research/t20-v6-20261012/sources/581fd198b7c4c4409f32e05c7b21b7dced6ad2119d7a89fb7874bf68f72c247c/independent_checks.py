"""Independent generalized-weight algebra and negative controls; not a formal proof."""
import sympy as S, json
from pathlib import Path
x,z,a,b=S.symbols('x z a b', positive=True)
k=S.symbols('k', integer=True, nonnegative=True)
D=lambda F:S.expand(x*x*S.diff(F,x)-x**4*z*S.diff(F,z))
N=a+b*z
moving=b*z*x**k
checks={
'generalized_moving_moment': S.simplify(D(moving)-(k*b*z*x**(k+1)-b*z*x**(k+4)))==0,
'generalized_total_mass': S.simplify(D(N)+b*z*x**4)==0,
'generalized_rank_minor': S.simplify(N*b*z*x*x-(b*z*x)**2-a*b*z*x*x)==0,
'reaction_integral': S.simplify(S.diff(x**3/S.Integer(3),x)-x*x)==0,
'wrong_nondivergence_reaction_detected': S.simplify((-x**4+2*x)-(-x**4))!=0,
'wrong_normalization_detected': S.simplify(-b*z*x**4/N)!=0,
}
for j in range(10):
 m=lambda n:(a if n==0 else S.Integer(0))+b*z*x**n
 q=lambda n:m(n)/N
 checks[f'generalized_normalized_moment_{j}']=S.simplify(D(q(j))-(j*q(j+1)-q(j+4)+q(4)*q(j)))==0
t=S.symbols('t', positive=True)
rx=1/t
rc=S.exp(-1/(3*t**3))
checks['reverse_direct_characteristic']=S.simplify(S.diff(rx,t)+rx**2)==0
checks['reverse_direct_weight']=S.simplify(S.diff(rc,t)-rx**4*rc)==0
checks['reverse_nondivergence_sign']=S.simplify((x**4+2*x)+S.diff(-x*x,x)-x**4)==0
for j in range(10):
 m=lambda n:(a if n==0 else S.Integer(0))+b*z*x**n
 q=lambda n:m(n)/N
 checks[f'reverse_generalized_normalized_moment_{j}']=S.simplify(-D(q(j))-(-j*q(j+1)+q(j+4)-q(4)*q(j)))==0
checks['all_pass']=all(checks.values())
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
assert checks['all_pass']
