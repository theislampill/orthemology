#!/usr/bin/env python3
"""Exact candidate validation and finite boundary controls, not a proof kernel."""
from pathlib import Path
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent
checks=[]
def zero(name,expr):
    v=s.simplify(s.cancel(expr));assert v==0,(name,v);checks.append(name)
def true(name,condition):
    assert bool(condition),name;checks.append(name)
for f,h in json.loads((HERE/'INPUT_BINDINGS.json').read_text()).items():
    true('inherited input copied intact: '+f,hashlib.sha256((HERE/'inputs'/f).read_bytes()).hexdigest()==h)
u=s.symbols('s',positive=True);x=s.symbols('x',real=True);t=s.symbols('t',real=True)
V=x*x/2-(3*u+u*u)*x**3/3+u**3*x**4/4
b=(3*u+u*u)*x*x-u**3*x**3-x
X=u**-2
zero('gradient relation',b+s.diff(V,x))
zero('characteristic equation',-s.diff(X,u)-b.subs(x,X))
zero('initial point',X.subs(u,1)-1)
zero('endpoint potential',V.subs(u,0)-x*x/2)
zero('endpoint drift',b.subs(u,0)+x)
zero('positive quartic leading coefficient',s.Poly(V,x).LC()-u**3/4)
true('frozen quartic coercive coefficient',u**3/4>0)
true('common finite spatial degree',s.Poly(V,x).degree()==4 and s.Poly(b,x).degree()==3)
true('time polynomial coefficients',all(s.Poly(co.subs(u,1-t),t).degree()<=3 for co in s.Poly(V,x).all_coeffs()))
zero('frozen energy dissipation identity',s.diff(V,x)*b+s.diff(V,x)**2)
for n in range(0,9):
    p=x**n
    moment=p.subs(x,X)
    rhs=(b*s.diff(p,x)-V*p).subs(x,X)+V.subs(x,X)*moment
    zero(f'normalized all-monomial identity sample n={n}',-s.diff(moment,u)-rhs)
zero('Dirac covariance cancellation for generic polynomial',(-V*(1+2*x-x**3)+V*(1+2*x-x**3)).subs(x,X))
i,j=s.symbols('i j',integer=True,nonnegative=True)
zero('full Hankel outer-product factorization',u**(-2*(i+j))-u**(-2*i)*u**(-2*j))
zero('rank one nonzero mass',u**0-1)
true('first moment diverges',s.limit(X,u,0,dir='+')==s.oo)
v=s.Rational(1,6)*u**-4-s.Rational(3,4)*u**-5
zero('energy along escape',V.subs(x,X)-v)
zero('gradient along escape',s.diff(V,x).subs(x,X)+2*u**-3)
zero('gradient square along escape',s.diff(V,x).subs(x,X)**2-4*u**-6)
partial=-s.diff(V,u).subs(x,X)
zero('external work exact positive formula',partial-(s.Rational(2,3)*u**-5+s.Rational(1,4)*u**-6))
true('external work positive',s.Rational(2,3)*u**-5+s.Rational(1,4)*u**-6>0)
total=-s.diff(v,u)
zero('total energy derivative formula',total-(s.Rational(2,3)*u**-5-s.Rational(15,4)*u**-6))
zero('chain rule including time dependence',total-(partial-s.diff(V,x).subs(x,X)**2))
# On 0<s<=1, 15/4-2s/3 = 37/12+2(1-s)/3 >0.
zero('negative total derivative interval certificate',s.Rational(15,4)-s.Rational(2,3)*u-(s.Rational(37,12)+s.Rational(2,3)*(1-u)))
true('energy unbounded below along escape',s.limit(v,u,0,dir='+')==-s.oo)
J=s.Rational(19,144)+s.Rational(1,18)*u**-3-s.Rational(3,16)*u**-4
zero('integrated killing derivative',-s.diff(J,u)-v)
zero('integrated killing initial value',J.subs(u,1))
true('integrated killing unbounded below',s.limit(J,u,0,dir='+')==-s.oo)
HH=1+x*x
ratio=(b*s.diff(HH,x)/HH).subs(x,X)
zero('quadratic common-control ratio',ratio-4/(u*(1+u**4)))
true('quadratic common-control ratio diverges',s.limit(ratio,u,0,dir='+')==s.oo)
# General nonnegative coercive C1 impossibility is the written Gronwall proof,
# not a finite search over candidate H or a computer-certified universal claim.
result={'status':'passed','checks':len(checks),'limit':'Finite symbolic controls supplement the written coercivity, Gronwall and endpoint proof; no formal-kernel verification.','names':checks}
(HERE/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
