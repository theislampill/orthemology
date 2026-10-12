"""Exact symbolic/algebraic controls; not a proof of all analytic claims."""
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sympy as S

checks=[]
def check(name, condition):
    if not bool(condition):
        raise RuntimeError(name)
    checks.append(name)

t=S.symbols('t', positive=True)
s=S.symbols('s', positive=True)
eps,r=S.symbols('eps r', positive=True)
x=2*(S.exp(3*t)-1)/(2*S.exp(3*t)+1)
f=(s+2)*(1-s)
D=(s+2)*(1-s)**2/(2*s)
E=(s-1-S.log(s))/2
check('explicit variance solves actual specialised ODE',S.simplify(S.diff(x,t)-f.subs(s,x))==0)
check('initial variance zero',S.limit(x,t,0,dir='+')==0)
check('initial variance derivative two',S.limit(S.diff(x,t),t,0,dir='+')==2)
check('target variance one',S.limit(x,t,S.oo)==1)
check('energy dissipation identity',S.simplify(S.diff(E,s)*f+D)==0)
check('original time pole coefficient one half',S.limit(t*D.subs(s,x),t,0,dir='+')==S.Rational(1,2))
check('quadratic unit interval reparametrisation leading action two epsilon',S.limit(4*eps**2*r**2*D.subs(s,x.subs(t,eps*r*r)),r,0,dir='+')==2*eps)
check('variance exceeds zero',S.simplify(x/(S.exp(3*t)-1))==2/(2*S.exp(3*t)+1))
check('variance below target',S.simplify(1-x)==3/(2*S.exp(3*t)+1))

def gm(n):
    return S.Integer(0) if n%2 else S.factorial2(n-1) if n else S.Integer(1)
for m,n in product(range(9),repeat=2):
    moment=gm(m)*gm(n)*(s**(n//2) if n%2==0 else 1)
    expected=gm(m) if n==0 else 0
    check(f'Gaussian moment trace ({m},{n})', S.limit(moment,s,0,dir='+')==expected)

# Total variation control and positive reweighting on finite exact laws.
# This is deliberately not offered as an uncountable-family proof.
for raw in product(range(1,4),repeat=3):
    mu=tuple(F(z,sum(raw)) for z in raw)
    for weights in ((F(1),F(2),F(4)),(F(3),F(1,2),F(1))):
        z=sum(p*w for p,w in zip(mu,weights))
        nu=tuple(p*w/z for p,w in zip(mu,weights))
        tv=sum(abs(p-q) for p,q in zip(mu,nu))/2
        for mask in product((0,1),repeat=3):
            a=sum(p*b for p,b in zip(mu,mask)); b=sum(p*k for p,k in zip(nu,mask))
            check('declared-event TV bound',abs(a-b)<=tv)
            if a==1:
                check('positive-update conull preservation',b==1)
# Singular support control: a zero coordinate cannot be created by a tilt.
mu=(F(1,3),F(2,3),F(0)); weights=(F(7),F(1),F(99))
z=sum(p*w for p,w in zip(mu,weights)); nu=tuple(p*w/z for p,w in zip(mu,weights))
check('zero support preserved by actual multiplicative update',nu[-1]==0)
for source in json.loads((Path(__file__).parent/'SOURCE_BINDINGS.json').read_text()):
    p=Path(source['path'])
    check('source '+source['title'],hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'])
print(json.dumps({'status':'PASS','checks':len(checks),'claims_scope':'Exact finite and symbolic controls; analytic/measure/computability arguments are written proofs','names':checks},indent=2))
