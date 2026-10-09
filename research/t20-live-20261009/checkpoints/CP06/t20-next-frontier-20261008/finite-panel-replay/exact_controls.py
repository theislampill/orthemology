#!/usr/bin/env python3
"""Exact arithmetic controls, not a formal or exhaustive verification of the proof."""
from hashlib import sha256
from pathlib import Path
import sys
import sympy as S

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
FROZEN = {
    HERE / 'RESULT.md': '327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243',
    HERE / 'SHARED_MARGINAL_BOUNDARY.md': '3d55f739d398ed1b4b28253cdb5db34ec9b32d46415e14750a612e35f43b4788',
    BASE / 'finite-panel-replay-review' / 'REVIEW.md': '812eb02988e1e2e695e71fcdead1debbd20a9525570b5f3eb68c26b601af208e',
}

checks = 0

def identity(label, lhs, rhs):
    global checks
    residual = S.factor(S.cancel(lhs-rhs))
    assert residual == 0, (label, residual)
    checks += 1
    print(f'PASS {label}: residual = 0')

print('Exact symbolic arithmetic controls only; not kernel verification or a check of the entire proof.')
print(f'Python {sys.version.split()[0]}; SymPy {S.__version__}')
for path, expected in FROZEN.items():
    actual = sha256(path.read_bytes()).hexdigest()
    assert actual == expected, (str(path), actual)
    print(f'PASS frozen SHA256 {path.relative_to(BASE)} = {actual}')

n = S.symbols('n', integer=True, positive=True)
t = 1/(3*(n+1))
c = n/(n+1)
D = (1-t)**2-c*(1+2*n*t**2)
D_closed = (n**2+7*n+4)/(9*(n+1)**3)
A_star = n*c*t**2/(1-t)**2
W = n*t**2/(1+n*t**2)
delta = n*(n**2+7*n+4)/((n+1)*(9*(n+1)**2+n)*(3*n+2)**2)
identity('sufficient-condition gap D', D, D_closed)
identity('uniform A_star', A_star, n**2/((n+1)*(3*n+2)**2))
identity('uniform W', W, n/(9*(n+1)**2+n))
identity('relative excess delta_n', (1-A_star)*(1+W)-1, delta)
identity('n=1 t', t.subs(n,1), S.Rational(1,6))
identity('n=1 A_star', A_star.subs(n,1), S.Rational(1,50))
identity('n=1 W', W.subs(n,1), S.Rational(1,37))
identity('n=1 delta', delta.subs(n,1), S.Rational(6,925))
print('delta_n =', S.factor(delta))
print('Positivity and uniformity over all integer m are established by the written inequalities, not a numerical grid.')

z, a, b, tau = S.symbols('z a b tau', real=True)
f = z*(1-z)*(z-tau)
epsilon = S.Rational(1,100)
C = a*b+epsilon*f.subs(z,a)*f.subs(z,b)
for label, lhs, rhs in [
    ('f(0)',f.subs(z,0),0), ('f(1)',f.subs(z,1),0),
    ('f(tau)',f.subs(z,tau),0),
    ('copula zero A boundary',C.subs(a,0),0),
    ('copula zero B boundary',C.subs(b,0),0),
    ('copula A margin',C.subs(b,1),a),
    ('copula B margin',C.subs(a,1),b),
    ('copula sampled A row',C.subs(a,tau),tau*b),
    ('copula sampled B column',C.subs(b,tau),a*tau),
    ('copula mixed density',S.diff(C,a,b),1+epsilon*S.diff(f,z).subs(z,a)*S.diff(f,z).subs(z,b)),
    ('copula nonzero off-panel perturbation',C.subs({a:tau/2,b:tau/2})-tau**2/4,epsilon*tau**4*(2-tau)**2/64),
    ('local independent 00 cell',1-2*tau+tau**2,(1-tau)**2),
]:
    identity(label,lhs,rhs)
identity('written loose density floor 1-64/100',1-64*epsilon,S.Rational(9,25))
print('Density positivity uses the written derivative bound |f\'| < 8 for 0 < tau <= 1/6; this script checks its resulting rational floor only.')

I = (tau**2,0,0,1-tau**2)
II = (0,tau/(1+tau),tau/(1+tau),(1-tau)/(1+tau))
identity('Type I table sum',sum(I),1)
identity('Type II table sum',sum(II),1)
identity('route-specific A-face product',(1-tau**2)*(1-tau/(1+tau)),1-tau)
identity('route-specific B-face product',(1-tau**2)*(1-tau/(1+tau)),1-tau)
identity('route-specific diagonal product',(1-I[0])*(1-II[0]),1-tau**2)
identity('route-specific replay product',I[3]*II[3],(1-tau)**2)
for tag,w in [('I',tau**2),('II',tau/(1+tau))]:
    left = w*z/tau
    right = w+(1-w)*(z-tau)/(1-tau)
    identity(f'Type {tag} homeomorphism left endpoint',left.subs(z,0),0)
    identity(f'Type {tag} homeomorphism join',left.subs(z,tau),right.subs(z,tau))
    identity(f'Type {tag} homeomorphism right endpoint',right.subs(z,1),1)
    print(f'Type {tag} slopes = {S.factor(S.diff(left,z))}, {S.factor(S.diff(right,z))}')
print('Table nonnegativity, positive slopes on 0 < tau < 1, fixed-threshold interpretation, and independence of all occurrences are justified in the written addendum.')
print(f'PASS: {checks} exact algebraic identities and all 3 frozen SHA256 bindings.')
