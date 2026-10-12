#!/usr/bin/env python3
"""A small discriminating exact check set; not a universal representation proof."""
from pathlib import Path
import sympy as S
import hashlib,json
ROOT=Path(__file__).resolve().parent
checks=[]
def check(ok,label):
    assert bool(ok),label
    checks.append(label)
def zero(expr,label):check(S.simplify(expr)==0,label)
for row in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    data=(ROOT/row['copy']).read_bytes()
    check(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'input: '+row['source'])
x,t,s,v,delta,H=S.symbols('x t s v delta H',real=True)
h=(x-t)**2
zero(h+H**2-x*x/2-((x-2*t)**2/2+H**2-t*t),'moving quadratic SOS certificate')
for n in range(1,5):
    zero(S.integrate((delta-v)**(n-1),(v,0,delta))/S.factorial(n-1)-delta**n/S.factorial(n),'Volterra simplex factor n='+str(n))
# Scalar window H=1/5 has uniform certificate c=1/2,C=1/25.
C=S.Rational(1,25);c=S.Rational(1,2);g=h+C
U=t*x*x-t*t*x+t**3/3+C*t
zero(S.diff(U,t)-g,'integrated time-dependent energy')
pts=[-1,0];weights=[S.Rational(1,2),S.Rational(1,2)]
for n in range(3):
    an=sum(w*S.Integer(a)**(2*n)*S.exp(-U.subs(x,a)) for a,w in zip(pts,weights))
    anext=sum(w*S.Integer(a)**(2*n+2)*S.exp(-U.subs(x,a)) for a,w in zip(pts,weights))
    slack=sum(w*S.Integer(a)**(2*n)*(g.subs(x,a)-c*a*a)*S.exp(-U.subs(x,a)) for a,w in zip(pts,weights))
    zero(-S.diff(an,t)-c*anext-slack,'radial derivative inequality slack n='+str(n))
for a,target in [(-1,-S.Rational(51,80)),(0,-S.Rational(79,400))]:
    zero((g*g-S.diff(g,t)).subs({x:a,t:S.Rational(1,10)})-target,'negative shifted even derivative at x='+str(a))
    check(target<0,'strict sign at x='+str(a))
Z=sum(w*S.exp(-U.subs(x,a)) for a,w in zip(pts,weights))
want=sum(w*(g*g-S.diff(g,t)).subs({x:a,t:S.Rational(1,10)})*S.exp(-U.subs({x:a,t:S.Rational(1,10)})) for a,w in zip(pts,weights))
zero(S.diff(Z,t,2).subs(t,S.Rational(1,10))-want,'actual second derivative equals negative atom sum')
ratio=S.exp(-t-t*t)
zero(S.diff(ratio,t).subs(t,0)+1,'genuinely changing normalized weight ratio')
# The compact-support condition is analytic; this checks the pointwise product identity.
zero(S.diff(S.exp(-U)*S.exp(U-U.subs(t,s)),t),'integrating-factor cancellation')
zero(S.exp(-U)*S.exp(U-U.subs(t,s))-S.exp(-U.subs(t,s)),'two-time density identity')
# Squared Fourier remainder ratio, exact for general integer n and degree D.
n,D=S.symbols('n D',integer=True,nonnegative=True)
M,r=S.symbols('M r',positive=True)
Tn=M**(2*n)*S.factorial(n+D)/(S.factorial(n)**2*r**(n+D))
zero(Tn.subs(n,n+1)/Tn-M*M*(n+D+1)/(r*(n+1)**2),'Fourier weighted remainder squared ratio')
result={'status':'PASS','total_exact_checks':len(checks),'checks':checks,'sympy_version':S.__version__,
        'scope':'Small exact algebraic controls supplement the universal proof; no generic measure reconstruction or detector implementation.'}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
