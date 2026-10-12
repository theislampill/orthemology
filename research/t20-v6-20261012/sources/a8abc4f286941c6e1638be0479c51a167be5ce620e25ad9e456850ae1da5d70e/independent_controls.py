"""Independent review controls: no execution/import of the author's checker.
Finite algebra cannot establish arbitrary-intersection or Type-2 theorems.
"""
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
checks = []
def require(label, value):
    if not bool(value):
        raise RuntimeError(label)
    checks.append(label)
def zero(label, expression):
    require(label, S.simplify(expression) == 0)

s, z, t, eps, r = S.symbols('s z t eps r', positive=True)
b, beta, tau = S.symbols('b beta tau', real=True)
# Independently specialise the source's polynomial vector field.
bdot = (b*(s-tau)-(b-beta)*(1+2*s+b*b/3))/tau
sdot = (2*b*s*(b-beta)-(s+2+2*b*b)*(s-tau))/tau
zero('invariant zero-regression slice', bdot.subs({b:0,beta:0,tau:1}))
f = S.expand(sdot.subs({b:0,beta:0,tau:1}))
zero('scalar vector field from source',f-(2-s-s*s))
# Separation gives d log((s+2)/(1-s))/dt=3.
zero('separated logarithmic invariant', (1/(s+2)+1/(1-s))*f-3)
q = 2*S.exp(3*t)
solution = S.solve(S.Eq((s+2)/(1-s), q), s)[0]
zero('closed variance from invariant',solution-2*(S.exp(3*t)-1)/(2*S.exp(3*t)+1))
zero('independently derived solution ODE',S.diff(solution,t)-f.subs(s,solution))
require('initial condition',solution.subs(t,0)==0)
wrong = 2*(S.exp(3*t)-1)/(S.exp(3*t)+2)
require('reject original wrong-denominator regression',S.simplify(S.diff(wrong,t)-f.subs(s,wrong)) != 0)

# Density tangent for rho_s(z) and inherited potential fields.
k = 1/s-1
v = k*z
alpha = k*(z*z-s)/2
logrho = -S.log(s)/2-z*z/(2*s)
density_tangent = S.diff(logrho,s)*f
transport_reaction = -S.diff(v,z)-v*S.diff(logrho,z)+alpha
zero('full density continuity equation',density_tangent-transport_reaction)
def gaussian_expectation(poly):
    result = 0
    for (n,), coeff in S.Poly(S.expand(poly),z).terms():
        if n % 2 == 0:
            result += coeff*(S.factorial2(n-1) if n else 1)*s**(n//2)
    return S.simplify(result)
zero('centred reaction at each retained y',gaussian_expectation(alpha))
zero('conditional density mass tangent zero',gaussian_expectation(density_tangent))
D = gaussian_expectation(v*v+alpha*alpha)
zero('action from actual field norms',D-(s+2)*(1-s)**2/(2*s))
E = (s-1-S.log(s))/2
zero('energy-action identity',S.diff(E,s)*f+D)
Dt = S.simplify(D.subs(s,solution))
# Removable analytic F=tD proves uniform Taylor control after t=eps*r^2.
F = t*Dt
for degree, expected in [(0,S.Rational(1,2)),(1,-S.Rational(5,4)),(2,S.Rational(3,8))]:
    coefficient = S.expand(S.series(F,t,0,3).removeO()).coeff(t,degree)
    zero('analytic boundary coefficient '+str(degree),coefficient-expected)
truncated_D = S.Rational(1,2)/t-S.Rational(5,4)+S.Rational(3,8)*t
changed = S.expand(4*eps**2*r**2*truncated_D.subs(t,eps*r*r))
action_expansion = S.integrate(changed,(r,0,1))
zero('integrated unit-time action through cubic order',action_expansion-(2*eps-S.Rational(5,3)*eps**2+S.Rational(3,10)*eps**3))
# Independent normalised variance and moment controls.
for n in range(14):
    moment = gaussian_expectation(z**n)
    expected = 1 if n==0 else 0
    require('moment endpoint '+str(n),S.limit(moment,s,0,dir='+')==expected)

binding = json.loads((HERE/'INPUT_DIGESTS.json').read_text())
for item in binding:
    require('digest '+item['path'],hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'])
print(json.dumps({'status':'PASS','checks':len(checks),'names':checks,
 'ceiling':'Exact algebra and hash controls only; no enumeration proof of measure or computability claims.'},indent=2))
