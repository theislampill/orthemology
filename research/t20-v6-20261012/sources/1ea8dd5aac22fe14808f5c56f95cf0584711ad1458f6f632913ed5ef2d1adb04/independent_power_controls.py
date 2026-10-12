"""Small exact identities for the supplementary review, not its general proof."""
from pathlib import Path
import json
import sympy as s

x, u, u0, a = s.symbols('x u u0 a', positive=True)
f = s.Rational(4,15) * x**s.Rational(5,2)
checks = {}
checks['power_first_derivative'] = s.simplify(s.diff(f,x)-s.Rational(2,3)*x**s.Rational(3,2)) == 0
checks['power_curvature'] = s.simplify(s.diff(f,x,2)-s.sqrt(x)) == 0
c = [s.Integer(0),s.Rational(9,25),s.Rational(16,25)]
dual = [s.simplify(s.Rational(2,3)*v**s.Rational(3,2)) for v in c]
checks['boundary_sum'] = sum(c) == 1
checks['boundary_dual_values'] = dual == [0,s.Rational(18,125),s.Rational(128,375)]
checks['finite_time_comparison_integral'] = s.simplify(s.integrate((s.Rational(3,2)*u)**s.Rational(-2,3),(u,0,u0))-3*s.Rational(2,3)**s.Rational(2,3)*u0**s.Rational(1,3)) == 0
checks['shannon_curvature'] = s.simplify(s.diff(x*s.log(x)/a,x,2)-1/(a*x)) == 0
checks['singleton_finite_exit_field'] = s.simplify((1-x)/s.diff((1-x)**3/6,x,2)-1) == 0
mixed_state = [x,s.Rational(1,2)+x*x/2,s.Rational(1,2)+x*x/2]
mixed_r = sum(mixed_state)-1
mixed_field = [-mixed_r/x,-mixed_r,-mixed_r]
checks['mixed_cubic_curvature'] = s.diff(x**3/6,x,2) == x
checks['mixed_boundary_exact_state_field'] = all(s.simplify(s.diff(v,x)*(-1-x)-w) == 0 for v,w in zip(mixed_state,mixed_field))
checks['mixed_boundary_exact_lifetime'] = s.simplify(s.integrate(1/(1+x),(x,0,s.Rational(1,2)))-s.log(s.Rational(3,2))) == 0
checks['equal_initial_sums_distinct_arrival'] = sum([s.Rational(1,2),s.Rational(5,8),s.Rational(5,8)]) == sum([s.Rational(1,4),s.Rational(3,4),s.Rational(3,4)]) == s.Rational(7,4)
tau = s.log(s.Rational(3,4)/(x+x*x))
checks['mixed_boundary_normalized_clock_derivative'] = s.simplify(s.diff(tau,x)*(-1-x)-(1/x+2)) == 0
checks['mixed_boundary_normalized_clock_diverges'] = s.limit(tau,x,0,dir='+') == s.oo
assert all(checks.values())
result = {'status':'PASS','checks':checks,'count':len(checks),'scope':'Small exact symbolic identities; not the general ODE/admissibility theorem.'}
Path(__file__).with_name('INDEPENDENT_POWER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
