#!/usr/bin/env python3
"""Supplementary exact algebra, not kernel or whole-proof verification."""
from hashlib import sha256
from pathlib import Path
import sys
import sympy as S

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
FROZEN={
    BASE/'finite-panel-replay-robustness-review/REVIEW.md':'946c743737420ff5485cfddfa504680a88400c07a2827bedb064a64ca1df7fcf',
    HERE/'RESULT.md':'3f12f86b3c1699448c350de05add930e67a3ccacc0c54d6dd3e134edb3c92ebe',
    BASE/'finite-panel-replay/RESULT.md':'327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243',
    BASE/'finite-panel-replay/SHARED_MARGINAL_BOUNDARY.md':'3d55f739d398ed1b4b28253cdb5db34ec9b32d46415e14750a612e35f43b4788',
    BASE/'finite-panel-replay-review/REVIEW.md':'812eb02988e1e2e695e71fcdead1debbd20a9525570b5f3eb68c26b601af208e',
    BASE/'finite-panel-replay/MANIFEST.sha256':'03a2b836250eb1b77eb99e3214ebcaff8ecf2e2748442d28bca6851c6a5b46d3',
}
checks=0

def check(label,lhs,rhs):
    global checks
    residual=S.factor(S.cancel(lhs-rhs))
    assert residual==0,(label,residual)
    checks+=1
    print(f'PASS {label}: residual = 0')

print('Exact algebraic controls only; not kernel verification, whole-proof checking, or empirical validation.')
print(f'Python {sys.version.split()[0]}; SymPy {S.__version__}')
for path,expected in FROZEN.items():
    actual=sha256(path.read_bytes()).hexdigest()
    assert actual==expected,(str(path),actual)
    print(f'PASS frozen SHA256 {path.relative_to(BASE)} = {actual}')

n,m=S.symbols('n m',integer=True,positive=True)
k=n+1
t=1/(3*k)
eps=1/(10000*k**2)
delta=n*(n**2+7*n+4)/(k*(9*k**2+n)*(3*n+2)**2)
Astar=n**2/(k*(3*n+2)**2)
W=n/(9*k**2+n)
check('inherited delta identity',(1-Astar)*(1+W)-1,delta)
check('baseline A Bernoulli margin',1-n*t-S.Rational(2,3),1/(3*k))
check('baseline Q Bernoulli margin',S.Rational(1,36)-n*t*t,(n-1)**2/(36*k**2))
check('delta numerator bound margin',n**2+7*n+4-k**2,5*n+3)
check('delta denominator first-factor margin',10*k*k-(9*k*k+n),n*n+n+1)
check('delta denominator second-factor margin',9*k*k-(3*n+2)**2,6*n+5)
check('delta n/k lower-bound margin',n/k-S.Rational(1,2),(n-1)/(2*k))
check('large-count baseline gap constant',S.Rational(1,180)*S.Rational(4,9),S.Rational(1,405))
check('large-count final residual',1/(405*k*k)-10*eps,S.Rational(119,81000)/(k*k))
check('small-count final scaled residual',-4/(81*k*k)+12*eps,-S.Rational(9757,202500)/(k*k))

s,A,Q=S.symbols('s A Q',positive=True)
F=s**m+(1-Q)*s**(m-1)
chain=S.diff(F,s)*A**(1/m-1)/m
expected=A**(1/m-1)*(s**(m-1)+(1-Q)*(1-1/m)*s**(m-2))
check('F derivative via root chain rule',chain,expected)
check('F Q derivative',S.diff(F,Q),-s**(m-1))
x=S.symbols('x',positive=True)
check('scaled Holder coordinate derivative',S.diff(m*x**(1/m),x),x**(1/m-1))
c=n/m
check('scaled convexity factor',m*c*(c-1),n*(n-m)/m)
check('scaled convexity minimum margin',n*(n-m)/m-n/(n-1),n*n*(n-1-m)/(m*(n-1)))
p=1-t
xp=1-t*t
xm=(1-t)**2
check('convexity interval midpoint',(xp+xm)/2,p)
check('convexity interval half-gap',(xp-xm)/2,t*(1-t))
check('Bernoulli powered midpoint base',1-(n+1)*t,S.Rational(2,3))
check('small-count baseline gap constant',t*t*S.Rational(4,9),4/(81*k*k))

alpha=S.symbols('alpha',positive=True)
Nstar=2*eps**(-2)*S.log(8/alpha)
check('sample coefficient',2*eps**(-2),200000000*k**4)
assert S.simplify(8*S.exp(-Nstar*eps**2/2)-alpha)==0
checks+=1
print('PASS Hoeffding union-bound equality at unrounded Nstar: residual = 0')
check('acceptance triangle radius',eps/2+eps/2,eps)
for label,expr,value in [
    ('n=1 t',t,S.Rational(1,6)),
    ('n=1 epsilon',eps,S.Rational(1,40000)),
    ('n=1 delta',delta,S.Rational(6,925)),
    ('n=1 A0',(1-t)**n,S.Rational(5,6)),
    ('n=1 Q0',(1-t*t)**n,S.Rational(35,36)),
    ('n=1 J0',(1-t)**(2*n),S.Rational(25,36)),
    ('n=1 sample log coefficient',2*eps**(-2),S.Integer(3200000000)),
]:
    check(label,expr.subs(n,1),value)
print('Analytic derivative bounds, convexity, Hoeffding concentration, stationarity/replay semantics, and all-count quantifiers are supplied by the written proof and mathematical review, not this script.')
print(f'PASS: {checks} exact algebraic controls and all {len(FROZEN)} frozen SHA256 bindings.')
