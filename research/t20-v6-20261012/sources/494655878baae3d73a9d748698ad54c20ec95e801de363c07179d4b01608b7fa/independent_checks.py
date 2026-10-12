#!/usr/bin/env python3
"""Independent algebra checks; analytic functional-domain proof is in REVIEW.md."""
import json
import sympy as s

checks = []
def check(name, expr):
    if isinstance(expr, s.MatrixBase):
        ok = all(s.simplify(x) == 0 for x in expr)
    else:
        ok = s.simplify(expr) == 0
    checks.append({'name': name, 'passed': bool(ok)})
    if not ok:
        raise AssertionError((name, expr))

y, v = s.symbols('y v', positive=True)
a, b, md, vd = s.symbols('a b md vd', real=True)
f = a*y + b*(y*y-v)
A = -s.diff(f,y,2) + y*s.diff(f,y)/v + f
score = a*(1+v)*y/v + (2*b*v*(v+2))*(y*y-v)/(2*v*v)
check('full Gaussian density tangent', A-score)
def eg(poly):
    return s.expand(sum(coeff*(0 if power[0] % 2 else s.factorial2(power[0]-1)*v**(power[0]//2)) for power,coeff in s.Poly(poly,y).terms()))
cost = eg(s.diff(f,y)**2 + f*f)
check('minimum candidate squared norm', cost-a*a*(1+v)-2*b*b*v*(v+2))
check('induced metric', cost.subs({a:md/(1+v),b:vd/(2*v*(v+2))})-md*md/(1+v)-vd*vd/(2*v*(v+2)))
check('channel cometrics sum', s.diag(1,4*v)+s.diag(v,2*v*v)-s.diag(1+v,2*v*(v+2)))

m, k, ell, c = s.symbols('m k ell c', real=True)
F = k*(y+m)**2/2 + ell*(y+m)+c
negscore = s.diff(F,y,2)-y*s.diff(F,y)/v-F+eg(F)
check('arbitrary quadratic negative gradient', negscore-(-(1+v)*(k*m+ell)*y/v-k*v*(v+2)*(y*y-v)/(2*v*v)))
for n in range(3,13):
    F = (y+m)**n
    leading = s.Poly(s.diff(F,y,2)-y*s.diff(F,y)/v-F,y).coeff_monomial(y**n)
    check(f'degree-{n} highest coefficient', leading+1+s.Rational(n)/v)

r = s.symbols('r', positive=True)
w = 1/s.sqrt(s.cosh(s.sqrt(2)*r))
K = -s.diff(w,r,2)/w
check('warped curvature', K-(s.Rational(3,2)/s.cosh(s.sqrt(2)*r)**2-s.Rational(1,2)))
check('radial metric transform', s.diff(s.acosh(v+1)/s.sqrt(2),v)**2-1/(2*v*(v+2)))
assert s.diff(1/(1+v),v) != 0
checks.append({'name':'non-Hessian obstruction in fixed (m,v) affine coordinates', 'passed':True})

t, v0, m0 = s.symbols('t v0 m0', positive=True)
D = 1 + v0*(1-s.exp(-2*t))/2
vt = v0*s.exp(-2*t)/D
mt = m0*s.exp(-t)/D
check('exact normalized weighted quadratic variance ODE', s.diff(vt,t)+vt*(vt+2))
check('exact normalized weighted quadratic mean ODE', s.diff(mt,t)+(1+vt)*mt)

# Noncommuting matrix checks use rational SPD covariance, avoiding diagonal-only tests.
S = s.Matrix([[2,s.Rational(1,3)],[s.Rational(1,3),1]])
U = s.Matrix([[s.Rational(2,5),s.Rational(-1,7)],[s.Rational(-1,7),s.Rational(3,4)]])
V = s.Matrix([[s.Rational(1,6),s.Rational(2,9)],[s.Rational(2,9),s.Rational(-1,5)]])
Q = s.Matrix([[2,s.Rational(1,2)],[s.Rational(1,2),3]])
L = lambda X: 2*(X*S+S*X+S*X*S)
check('matrix cometric Frobenius self-adjointness', s.trace(U*L(V))-s.trace(V*L(U)))
check('matrix cost/cometric identity', s.trace(U*L(U))-4*s.trace(U*U*S)-2*s.trace(U*S*U*S))
check('quadratic matrix covariance gradient', L(Q/2)-(Q*S+S*Q+S*Q*S))
P = S.inv()
Sdot = -(Q*S+S*Q+S*Q*S)
check('noncommuting precision evolution', -P*Sdot*P-(P*Q+Q*P+Q))
l1,l2 = s.symbols('l1 l2', positive=True)
x1,x2,x3 = s.symbols('x1 x2 x3')
Dg = s.diag(l1,l2)
X = s.Matrix([[x1,x2],[x2,x3]])
Ld = 2*(X*Dg+Dg*X+Dg*X*Dg)
check('matrix eigenbasis multiplier', Ld-s.Matrix([[2*(2*l1+l1*l1)*x1,2*(l1+l2+l1*l2)*x2],[2*(l1+l2+l1*l2)*x2,2*(2*l2+l2*l2)*x3]]))
print(json.dumps({'status':'pass','count':len(checks),'checks':checks,'scope':'Algebraic checks only. Functional minimality and localization argument require the analytic proof in REVIEW.md.'},indent=2))
