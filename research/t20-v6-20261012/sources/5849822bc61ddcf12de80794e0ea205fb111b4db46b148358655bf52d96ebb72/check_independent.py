#!/usr/bin/env python3
"""Independent finite exact controls, not a universal mathematical proof."""
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
counts = {}

def check(condition, group):
    if not bool(condition):
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

def eq(lhs, rhs, group):
    check(S.cancel(S.expand(lhs-rhs)) == 0, group)

rows = json.loads((ROOT/'author-snapshot/INPUT_BINDINGS.json').read_text())
for row in rows:
    original = (WORKSPACE/row['source']).read_bytes()
    frozen = (ROOT/'author-snapshot'/row['copy']).read_bytes()
    check(original == frozen, 'original_equals_frozen')
    check(hashlib.sha256(original).hexdigest() == row['sha256'], 'original_hash')
    check(len(original) == row['bytes'], 'original_size')

x,y,z,r = S.symbols('x y z r', real=True)
variables = (x,y,z)
support = [(-1,2,0),(0,-1,1),(2,0,-1)]
weights = [S.Rational(1,7),S.Rational(2,7),S.Rational(4,7)]
h = x*x+y*y+z*z
observables = [S.Integer(1),x,y,z,x*y,y*z,x*z,x-y-2*z,
               x*x*y+z, (x+y-z)**2, x*x*y*y*z*z, -(1+x*x)]

def raw(poly, energy=h):
    return sum(w*poly.subs(dict(zip(variables,point)), simultaneous=True)*
               r**energy.subs(dict(zip(variables,point)), simultaneous=True)
               for w,point in zip(weights,support))

mass = raw(S.Integer(1))
for p in observables:
    ap = raw(p)
    eq(-r*S.diff(ap,r), -raw(h*p), 'three_dimensional_unnormalized')
    eq(-r*S.diff(ap,r)*mass+r*ap*S.diff(mass,r),
       -raw(h*p)*mass+raw(h)*ap, 'three_dimensional_normalized')
    eq(raw(p,h-7)*mass, raw(p)*raw(S.Integer(1),h-7), 'constant_shift_cancels')
    eq(p, ((p+1)**2-(p-1)**2)/4, 'signed_polynomial_polarization')

# Catch an incorrect one-grade shift under quadratic damping.
check(S.cancel(raw(h*x)-raw(x*x)) != 0, 'wrong_grade_shift_detected')
check(raw(-(1+x*x)).subs(r,S.Rational(1,2)) < 0,
      'signed_observable_not_positive')

# Independent three-coordinate SOS decompositions, with nonmonomial square q.
q = 1-x+y*z
for n in range(1,7):
    rhs = 0
    for a in range(n+1):
        for b in range(n-a+1):
            c = n-a-b
            coefficient = S.factorial(n)/(S.factorial(a)*S.factorial(b)*S.factorial(c))
            rhs += coefficient*(q*x**a*y**b*z**c)**2
    eq(q*q*h**n,rhs,'joint_square_multinomial')
    for coordinate in variables:
        poly = S.Poly(h**n-coordinate**(2*n),*variables)
        check(all(coefficient >= 0 and all(e%2 == 0 for e in exponent)
                  for exponent,coefficient in poly.terms()), 'coordinate_sos_comparison')
    # This pointwise coefficient comparison is what enters the Carleman bound.
    check(S.factorial(n) <= n**n, 'factorial_bound')

# Polynomial inverse transport in BOTH directions and for mixed observables.
u,v = S.symbols('u v', real=True)
for k in (3,4,6):
    phi = {u:x, v:y-x**k}
    psi = {x:u, y:v+u**k}
    for p in (x,y,x*y,x*x-y,x*y*y+1):
        eq(p.subs(psi,simultaneous=True).subs(phi,simultaneous=True),p,
           'full_observable_inverse')
    eq((x*x+(y-x**k)**2).subs(psi,simultaneous=True),u*u+v*v,
       'polynomial_energy_transport')
    eq((v+u**k).subs(phi,simultaneous=True),y,'inverse_left')
    eq((y-x**k).subs(psi,simultaneous=True),v,'inverse_right')

# Exact tilt recovery; replacing the inverse weight by a second forward tilt fails.
for a in (S.Rational(1,2),S.Rational(3,5)):
    energies = [h.subs(dict(zip(variables,p))) for p in support]
    post = [w*a**e for w,e in zip(weights,energies)]
    post = [w/sum(post) for w in post]
    recovered = [w*a**(-e) for w,e in zip(post,energies)]
    recovered = [w/sum(recovered) for w in recovered]
    wrong = [w*a**e for w,e in zip(post,energies)]
    wrong = [w/sum(wrong) for w in wrong]
    for lhs,rhs in zip(recovered,weights):
        eq(lhs,rhs,'inverse_tilt_recovers_mass')
    check(wrong != weights,'wrong_untwisting_sign_detected')

# A scalar energy retains only the pushforward: sphere points already separate it.
atom_a = {x:1,y:0,z:0}
atom_b = {x:0,y:1,z:0}
for n in range(8):
    eq((h**n).subs(atom_a),(h**n).subs(atom_b),'scalar_energy_collision')
check(x.subs(atom_a) != x.subs(atom_b),'full_record_separates_energy_fibre')

# The universal Gaussian integral identity used by the signed-lognormal control.
w = S.symbols('w',real=True)
complex_mgf = S.exp((w+2*S.pi*S.I)**2/2)
eq(S.im(S.expand_complex(complex_mgf)),
   S.exp(w*w/2-2*S.pi**2)*S.sin(2*S.pi*w), 'gaussian_imaginary_mgf')
n = S.symbols('n',integer=True,nonnegative=True)
eq(S.sin(2*S.pi*n),0,'all_integer_cancellation')

# A rational-time rational-square certificate, including its exact value.
t = S.symbols('t',positive=True)
b = 1-S.exp(-1/t)/2
fourth = S.diff(b,t,2)/b
eq(fourth.subs(t,S.Rational(1,4)), -128/(2*S.exp(4)-1),
   'rational_time_square_certificate')
check(fourth.subs(t,S.Rational(1,4)) < 0,'strict_negative_certificate')
eq(S.diff(-S.diff(b,t)/b,t),-fourth+(-S.diff(b,t)/b)**2,
   'certificate_has_promised_quadratic_hierarchy')

report = {'status':'PASS','total_exact_checks':sum(counts.values()),
          'checks_by_group':counts,'sympy_version':S.__version__,
          'scope':'Finite exact controls; universal proof review is in REVIEW.md.'}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
