#!/usr/bin/env python3
"""Independent exact controls; no numerical trajectory or universal-proof claim."""
import json, sympy as s
x,t,z,u=s.symbols('x t z u', real=True)
m=s.symbols('m', integer=True, positive=True)
eps=s.symbols('epsilon', positive=True)
checks={}
def check(name, expression):
    reduced=s.simplify(expression)
    checks[name]=str(reduced)
    assert reduced==0, (name,reduced)
# Integrable excess-energy primitive for every even monomial.
F=x**(2*m)/(2*m)
check('even_monomial_excess_primitive', s.diff(x*x/(4*m),x)*(-s.diff(F,x))+F)
# Double-well primitive on either open half-line (write log(x^2)).
F=(x*x-1)**2/4
J=(x*x-1-s.log(x*x))/8
check('double_well_excess_primitive', s.diff(J,x)*(-s.diff(F,x))+F)
# Nonglobal selected well and mixture crossover.
F=x**4/4-x**3/3-x*x
check('unequal_well_factorization',s.diff(F,x)-x*(x-2)*(x+1))
c_hi=F.subs(x,-1); c_lo=F.subs(x,2); gap=c_hi-c_lo
check('critical_gap',gap-s.Rational(9,4))
p=eps*s.exp(gap*t)/(1-eps+eps*s.exp(gap*t))
check('mixture_reaction_equation',s.diff(p,t)-gap*p*(1-p))
check('mixture_crossover',p.subs(t,s.log((1-eps)/eps)/gap)-s.Rational(1,2))
# A genuinely non-atomic stationary winning law is allowed: unit circle.
a,b=s.symbols('a b', real=True)
F_circle=(a*a+b*b-1)**2/4
check('circle_gradient_a',s.diff(F_circle,a)-a*(a*a+b*b-1))
check('circle_gradient_b',s.diff(F_circle,b)-b*(a*a+b*b-1))
# Degenerate coercive growth need not be linear in energy.
F_valley=(a-b*b)**2+b*b
check('coercive_valley_energy',F_valley.subs(a,b*b)-b*b)
check('coercive_valley_radius', (a*a+b*b).subs(a,b*b)-(b**4+b*b))
print(json.dumps({'status':'PASS','controls':checks,'scope':'Exact algebraic controls only; universal analytic and semialgebraic claims require written proof.'},indent=2))
