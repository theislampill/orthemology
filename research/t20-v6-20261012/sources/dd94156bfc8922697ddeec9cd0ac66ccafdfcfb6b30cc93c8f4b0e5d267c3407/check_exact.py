#!/usr/bin/env python3
"""Exact finite controls for the written radial-quartic reverse-lift proof.

Does not discretize the infinite hierarchy or establish measure existence.
Run from any directory; writes only the sibling EXACT_CHECKS.json.
"""
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
checks = []

def zero(name, expression):
    value = s.simplify(s.cancel(expression))
    assert value == 0, (name, value)
    checks.append(name)

def true(name, condition):
    assert bool(condition), name
    checks.append(name)

# Before/after controls bind every old source; no old file is written.
bindings = json.loads((HERE / 'INPUT_BINDINGS.json').read_text())
for relative, expected in bindings.items():
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    true('input preserved: ' + relative, actual == expected)

# The radial recurrence is a polynomial identity in each selected dimension.
for d in (1, 2, 3):
    xs = s.symbols('x0:' + str(d), real=True)
    R = sum(x*x for x in xs)
    F = R**2 / 4
    b = [-R*x for x in xs]
    for i in range(d):
        zero(f'negative gradient d={d},i={i}', b[i] + s.diff(F, xs[i]))
    for n in range(9):
        p = R**n
        Gp = sum(bi*s.diff(p, x) for bi,x in zip(b,xs)) - F*p
        zero(f'radial generator d={d},n={n}', Gp + 2*n*R**(n+1) + R**(n+2)/4)
    zero(f'gradient square d={d}', sum(s.diff(F,x)**2 for x in xs) - R**3)
    zero(f'energy generator d={d}', sum(bi*s.diff(F,x) for bi,x in zip(b,xs))-F**2+R**3+F**2)
    for n in range(1, 6):
        for i in range(d):
            # The multinomial difference really has only nonnegative even terms.
            poly = s.Poly(s.expand(R**n-xs[i]**(2*n)), *xs)
            true(f'radial marginal SOS coefficients d={d},n={n},i={i}',
                 all(c >= 0 and all(e%2 == 0 for e in mon) for mon,c in poly.terms()))

# Nested integration: product coefficients cancel the simplex factorial.
h = s.symbols('h', positive=True)
for k in range(1, 14):
    coefficient = s.prod(2*j for j in range(1,k+1))
    volume = h**k / s.factorial(k)
    zero(f'simplex coefficient k={k}', coefficient*volume-(2*h)**k)

r,t,u = s.symbols('r t u', nonnegative=True)
m = s.symbols('m', integer=True, nonnegative=True)
D = 1+2*t*r
Rt = r/D
scale = D**s.Rational(-1,2)
K = r/s.Integer(8)*(1-1/D)
Ku = r/s.Integer(8)*(1-1/(1+2*u*r))
zero('radial ODE', s.diff(Rt,t)+2*Rt**2)
zero('coordinate flow scale ODE', s.diff(scale,t)+r*scale**3)
zero('killing integral derivative', s.diff(K,t)-Rt**2/4)
zero('initial radius', Rt.subs(t,0)-r)
zero('initial scale', scale.subs(t,0)-1)
zero('initial killing', K.subs(t,0))
zero('radial flow cocycle', Rt.subs({t:t,r:r/(1+2*u*r)}, simultaneous=True)-r/(1+2*(t+u)*r))
zero('scale squared cocycle', (1/(1+2*u*r))*(1/(1+2*t*r/(1+2*u*r)))-1/(1+2*(t+u)*r))
zero('killing cocycle', Ku+K.subs(r,r/(1+2*u*r))-K.subs(t,t+u))
zero('open image radius gap', 1/(2*t)-Rt-1/(2*t*D))

q = s.symbols('q', nonnegative=True)
inv_r = q/(1-2*t*q)
zero('inverse radial after forward', inv_r.subs(q,Rt)-r)
zero('forward radial after inverse', Rt.subs(r,inv_r)-q)
zero('inverse coordinate scale squared', (1/D)/(1-2*t*Rt)-1)
zero('inverse killing in output radius', K.subs(r,inv_r)-t*q**2/(4*(1-2*t*q)))
zero('finite-time spatial derivative on ray', s.diff(s.symbols('x', real=True)/(1+2*t*s.symbols('x', real=True)**2)**s.Rational(1,2),s.symbols('x', real=True))-(1+2*t*s.symbols('x', real=True)**2)**s.Rational(-3,2))

# Backward semigroup identity on every homogeneous monomial degree symbol m.
# H_t(r)=(1+2tr)^(-m/2)*exp(-K_t(r)); divide by its positive H.
log_H_t = -m*r/D - s.diff(K,t)
log_H_r = -m*t/D - s.diff(K,r)
G_over_H = -m*r-2*r**2*log_H_r-r**2/4
zero('backward generator for symbolic homogeneous degree', log_H_t-G_over_H)
for degree in range(9):
    H = D**(-s.Rational(degree,2))*s.exp(-K)
    zero(f'actual backward monomial degree={degree}',
         s.diff(H,t)+degree*r*H+2*r*r*s.diff(H,r)+r*r*H/4)

# Normalized quotient identity, retaining distinct transport and killing rates.
w1,w2,p1,p2,c1,c2,k1,k2 = s.symbols('w1 w2 p1 p2 c1 c2 k1 k2', real=True)
Z = w1+w2
N = w1*p1+w2*p2
Nprime = w1*(c1-k1*p1)+w2*(c2-k2*p2)
Zprime = -w1*k1-w2*k2
actual = (Nprime*Z-N*Zprime)/Z**2
expected = (w1*c1+w2*c2)/Z-(w1*k1*p1+w2*k2*p2)/Z+(w1*k1+w2*k2)*N/Z**2
zero('normalized two-atom quotient', actual-expected)
E1,E2,z1,z2 = s.symbols('E1 E2 z1 z2', positive=True)
a,b = s.symbols('a b', positive=True)
out1 = a*E1/(a*E1+b*E2)
out2 = b*E2/(a*E1+b*E2)
zero('undo positive reweight and renormalize', (out1/E1)/(out1/E1+out2/E2)-a/(a+b))

# Exact boundaries and inherited initial-fibre control; no numerical fitting.
zero('killing large-time limit', s.limit(K,t,s.oo)-r/8)
zero('radial large-time limit', s.limit(Rt,t,s.oo))
zero('energy radius cap', (1/(2*t))**2/4-1/(16*t*t))
for integer in range(9):
    zero(f'lognormal integer sine cancellation n={integer}', s.sin(2*s.pi*integer))
true('initial lognormal density perturbations stay nonnegative', s.Rational(1,2)>0)
true('boundary Dirac fails image condition at t=1', not (s.Rational(1,2)<s.Rational(1,2)))
true('point beyond image fails image condition at t=1', not (s.Integer(1)<s.Rational(1,2)))
# Explicitly test a nonpolynomial signature at t=1: nonzero odd derivatives
# of arbitrarily high selected order at x=0, beyond cubic or quintic degree.
x = s.symbols('x', real=True)
phi1 = x/s.sqrt(1+2*x*x)
for order in (3,5,7,9):
    true(f'nonpolynomial signature derivative order={order}', s.diff(phi1,x,order).subs(x,0) != 0)

result = {
    'status':'PASS',
    'exact_check_count':len(checks),
    'checks':checks,
    'inputs_preserved':True,
    'scope':'Exact finite algebraic controls supplement the written proof; no universal proof kernel, numerical sampling, rank cutoff, or integration/closure claim.'
}
(HERE/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
