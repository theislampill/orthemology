#!/usr/bin/env python3
"""Exact supplementary algebra controls; not an infinite-dimensional proof checker."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
x, y, z, t, a, u = s.symbols('x y z t a u', real=True)
xyz = (x, y, z)
results = []


def check(name, condition):
    ok = bool(condition)
    results.append({'name': name, 'pass': ok})
    if not ok:
        raise AssertionError(name)


def equal(name, lhs, rhs):
    check(name, s.cancel(s.expand(lhs-rhs)) == 0)


def lap(p, variables):
    return s.expand(sum(s.diff(p, v, 2) for v in variables))


def heat(p, tau, variables):
    p = s.expand(p)
    result, k, current = 0, 0, p
    while current != 0:
        result += tau**k * current / s.factorial(k)
        current = lap(current, variables)
        k += 1
    return s.expand(result)


def scale(p, factor, variables):
    return s.expand(p.subs({v: factor*v for v in variables}, simultaneous=True))


def square_heat_formula(q, tau, variables):
    degree = s.Poly(q, *variables).total_degree()
    out = 0
    for alpha in itertools.product(range(degree+1), repeat=len(variables)):
        if sum(alpha) > degree:
            continue
        dq = q
        for v, j in zip(variables, alpha):
            dq = s.diff(dq, v, j)
        if dq == 0:
            continue
        out += ((2*tau)**sum(alpha) / s.prod(s.factorial(j) for j in alpha)
                * heat(dq, tau, variables)**2)
    return s.expand(out)


f = 1-4*x*y*z+x*x*y*y+x*x*z*z+y*y*z*z
radial = x*x+y*y+z*z
equal('Choi-Lam heat formula', heat(f,t,xyz), f+4*t*radial+12*t*t)
threshold = s.Rational(1,9)
sos_entry = s.Rational(31,27)+(x*y-s.Rational(2,3)*z)**2+(x*z-s.Rational(2,3)*y)**2+(y*z-s.Rational(2,3)*x)**2
equal('Choi-Lam exact threshold SOS', heat(f,threshold,xyz), sos_entry)
equal('Above-threshold SOS remainder', heat(f,t,xyz)-sos_entry,
      4*(t-threshold)*radial+12*(t*t-threshold**2))
fa = scale(f,a,xyz)
equal('Dilation covariance Choi-Lam', heat(fa,t,xyz), scale(heat(f,a*a*t,xyz),a,xyz))
equal('Scaled Choi-Lam heat polynomial', heat(fa,t,xyz),
      fa+4*a**4*t*radial+12*a**4*t*t)
equal('Scaled threshold SOS identity', heat(fa,1/(9*a*a),xyz),
      s.Rational(31,27)+(a*a*x*y-s.Rational(2,3)*a*z)**2
      +(a*a*x*z-s.Rational(2,3)*a*y)**2+(a*a*y*z-s.Rational(2,3)*a*x)**2)
check('Scaled threshold tends to infinity along a=1/k',
      all(1/(9*s.Rational(1,k)**2) == s.Rational(k*k,9) for k in range(1,13)))
equal('Dilation family coefficient limit', fa.subs(a,0),1)
equal('Unit squared coefficient norm', sum(c*c for c in s.Poly(fa,*xyz).coeffs()),
      1+16*a**6+3*a**8)
equal('Dual dilation stretches witness time',
      scale(heat(scale(f,1/a,xyz),t,xyz),a,xyz), heat(f,t/(a*a),xyz))

samples = [1, x, x*x, x*y, 1+x*x+2*x*y-y**3,
           3+x*y*z+x*x*y-z**3, x**4+2*x*x*y*y-y**4+x]
for index, q in enumerate(samples):
    equal(f'Finite square heat identity {index}', heat(q*q,t,xyz),
          square_heat_formula(q,t,xyz))
    equal(f'Heat hierarchy identity {index}', s.diff(heat(q,t,xyz),t),
          heat(lap(q,xyz),t,xyz))
    equal(f'Heat semigroup identity {index}', heat(heat(q,t,xyz),u,xyz),
          heat(q,t+u,xyz))

q=3*x*x*y+2*x*y*y+z*z
dq=s.diff(q,x,2,y,1)
equal('Highest-degree derivative is nonzero constant',dq,6)
equal('Strict square-positive lower-bound term',
      (2*t)**3/s.factorial(2)*dq*dq,144*t**3)

# Verify that symbolic initial moments enter heat coordinates only through
# their finite initial degree prefix, with no extra distributional assumption.
def symbolic_functional(p):
    out=0
    for alpha,c in s.Poly(p,*xyz).terms():
        out += c*s.Symbol('m_'+'_'.join(map(str,alpha)))
    return s.expand(out)

p=2+x**6+y**4*z**2-3*x*y*z
equal('Functional heat hierarchy with symbolic moments',
      s.diff(symbolic_functional(heat(p,t,xyz)),t),
      symbolic_functional(heat(lap(p,xyz),t,xyz)))
equal('Degree-six heat coordinate formula',heat(x**6,t,xyz),
      x**6+30*t*x**4+180*t*t*x*x+120*t**3)
equal('Moment equivalence survives degree-six heat coordinate',
      symbolic_functional(heat(x**6,t,xyz)),
      s.Symbol('m_6_0_0')+30*t*s.Symbol('m_4_0_0')
      +180*t*t*s.Symbol('m_2_0_0')+120*t**3*s.Symbol('m_0_0_0'))

eta,B=s.symbols('eta B', positive=True)
epsilon=eta/(2*(B+eta))
equal('Witness continuity margin exact identity',
      -eta+B*epsilon,
      -eta/s.Integer(2)-eta**2/(2*(B+eta)))

# Independent finite truncated reconstruction, distinct from a full functional.
def truncated_moment(alpha):
    if alpha == (0,0,0):
        return s.Integer(1)
    if alpha == (1,1,1):
        return s.Rational(3,2)
    if sorted(alpha) == [0,0,2]:
        return s.Integer(4)
    if sorted(alpha) == [0,0,4]:
        return s.Integer(50)
    if sorted(alpha) == [0,2,2]:
        return s.Integer(1)
    return s.Integer(0)


def truncated_lambda(p):
    terms=s.Poly(s.expand(p),*xyz).terms()
    if any(sum(alpha)>4 for alpha,_ in terms):
        raise ValueError('The diagnostic is only defined through degree four.')
    return s.expand(sum(c*truncated_moment(alpha) for alpha,c in terms))


basis=(1,x*x,y*y,z*z,x,y*z,y,x*z,z,x*y)
moment=s.Matrix([[truncated_lambda(v*w) for w in basis] for v in basis])
E=s.Matrix([[1,4,4,4],[4,50,1,1],[4,1,50,1],[4,1,1,50]])
O=s.Matrix([[4,s.Rational(3,2)],[s.Rational(3,2),1]])
check('Truncated moment matrix exact block reconstruction', moment==s.diag(E,O,O,O))
schur=E[1:,1:]-E[1:,:1]*E[:1,1:]
check('Even block Schur spectrum', schur.eigenvals()=={s.Integer(4):1,s.Integer(49):2})
check('Odd block positivity', O[0,0]>0 and O.det()==s.Rational(7,4))
check('Truncated all leading minors positive', all(moment[:j,:j].det()>0 for j in range(1,11)))
check('Truncated exact determinant',moment.det()==s.Rational(823543,16))
equal('Truncated nonnegative witness at zero',truncated_lambda(f),-2)
equal('Truncated nonnegative witness heat formula',truncated_lambda(heat(f,t,xyz)),-2+48*t+12*t*t)
equal('Truncated witness at t=1/100',truncated_lambda(heat(f,s.Rational(1,100),xyz)),s.Rational(-3797,2500))
equal('Truncated dual-scaled heat witness',
      truncated_lambda(scale(heat(scale(f,1/a,xyz),t,xyz),a,xyz)),
      -2+48*t/(a*a)+12*t*t/a**4)
polynomial_basis=[x**i*y**j*z**k for i in range(5) for j in range(5-i) for k in range(5-i-j)]
check('Degree-four full monomial basis count',len(polynomial_basis)==35)
check('Truncated inverse heat on all 35 monomials',all(
    s.cancel(truncated_lambda(scale(heat(heat(p,-t,xyz),t,xyz),a,xyz))
             -truncated_lambda(scale(p,a,xyz)))==0 for p in polynomial_basis))

# Bounded affine extension controls.
w1,w2,d1,d2,c,C,D,sigma,Y1,Y2,h=s.symbols('w1 w2 d1 d2 c C D sigma Y1 Y2 h',real=True)
w_sq=w1*w1+w2*w2
dy_sq=d1*d1+d2*d2
Y_sq=Y1*Y1+Y2*Y2
rhs=(h+C-c*((w1+d1)**2+(w2+d2)**2)
     +c/s.Integer(2)*((w1+2*d1)**2+(w2+2*d2)**2)
     +c/s.Integer(2)*(w_sq-sigma*sigma*Y_sq)+c*(D*D-dy_sq))
equal('Affine transferred radial SOS expansion',rhs,h+C+c*D*D-c*sigma*sigma*Y_sq/2)
q1=1+x+2*x*x+x**3
inverse=s.exp(-t)*(x-t)
pulled=q1.subs(x,inverse)
velocity=x+1-t
check('Nontrivial affine inverse-flow cancellation',
      s.simplify(s.diff(pulled,t)+velocity*s.diff(pulled,x))==0)
location=s.exp(t)*y+t
killing=(x-t)**2+1
K=(s.exp(2*t)-1)*y*y/2+t
check('Characteristic integrated killing derivative',
      s.simplify(s.diff(K,t)-killing.subs(x,location))==0)
atom=s.exp(-K)*q1.subs(x,location)
atom_rhs=s.exp(-K)*(velocity*s.diff(q1,x)-killing*q1).subs(x,location)
check('Moving-atom unnormalized hierarchy',s.simplify(s.diff(atom,t)-atom_rhs)==0)

bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for row in bindings['inputs']:
    check('Unchanged input '+row['path'],
          hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'])

output={'kind':'exact supplementary symbolic controls',
        'sympy_version':s.__version__, 'passed':sum(r['pass'] for r in results),
        'failed':sum(not r['pass'] for r in results), 'results':results,
        'limits':'Finite algebra tests do not prove the universal positivity, classical functional-existence inputs, or a formal proof kernel.'}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'passed':output['passed'],'failed':output['failed'],
                  'sympy_version':s.__version__},indent=2))
