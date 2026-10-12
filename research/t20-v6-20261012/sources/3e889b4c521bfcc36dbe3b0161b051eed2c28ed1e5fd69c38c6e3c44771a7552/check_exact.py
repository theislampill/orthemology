#!/usr/bin/env python3
"""Exact nonautonomous clock, localization and moving-quadratic controls.

Finite algebra supplements the written proof. No formal-kernel claim.
"""
from pathlib import Path
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE/'inputs'
checks=[]
def zero(group,name,expr):
    v=s.simplify(s.cancel(expr));assert v==0,(name,v)
    checks.append({'group':group,'name':name})
def true(group,name,c):
    assert bool(c),name
    checks.append({'group':group,'name':name})
for f,h in json.loads((HERE/'INPUT_BINDINGS.json').read_text()).items():
    true('input_integrity',f,hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h)
base=ROOT/'general-coercive-energy-drift-20261010'
for f,h in json.loads((base/'AUTHOR_MANIFEST.json').read_text())['files'].items():
    true('autonomous_frozen_integrity',f,hashlib.sha256((base/f).read_bytes()).hexdigest()==h)

C,k,t,r,H,Q,P=s.symbols('C k t r H Q P',positive=True)
K=P+k*H
for n in range(0,10):
    transport=0 if n==0 else n*H**(n-1)*(C*H-Q)
    lhs=-C*n*s.exp(-C*n*t)*H**n+s.exp(-C*n*t)*(transport-K*H**n)
    rhs=-s.exp(-C*n*t)*(K*H**n+(n*H**(n-1)*Q if n else 0))
    zero('moving_energy',f'moving-test exact recurrence n={n}',lhs-rhs)
    zero('moving_energy',f'SOS inequality residual n={n}',lhs+k*s.exp(C*t)*s.exp(-C*(n+1)*t)*H**(n+1)+s.exp(-C*n*t)*(P*H**n+(n*H**(n-1)*Q if n else 0)))
theta=k*(s.exp(C*t)-1)/C
rho=k*(1-s.exp(-C*t))/C
zero('clock','clock derivative',s.diff(theta,t)-k*s.exp(C*t))
zero('clock','clock and energy width',s.exp(-C*t)*theta-rho)
zero('clock','width derivative',s.diff(rho,t)-k*s.exp(-C*t))
zero('clock','width linear ODE',s.diff(rho,t)+C*rho-k)
zero('clock','clock C zero limit',s.limit(theta,C,0)-k*t)
zero('clock','width C zero limit',s.limit(rho,C,0)-k*t)
zero('clock','endpoint energy kernel integral',s.integrate(k*s.exp(-C*(t-r)),(r,0,t))-rho)
for n in range(1,9):
    zero('inherited_regression',f'clock simplex factorial n={n}',theta**n/s.factorial(n)*s.factorial(n)/theta**n-1)

# Generic time-dependent generator, with H fixed in time.
x,y,z=s.symbols('x y z',real=True)
for d in (1,2,3):
    xs=(x,y,z)[:d]
    HH=s.Function('H')(*xs);p=s.Function('p')(*xs)
    Kt=s.Function('K')(t,*xs);bs=[s.Function('b'+str(i))(t,*xs) for i in range(d)]
    bg=lambda f:sum(bi*s.diff(f,xi) for bi,xi in zip(bs,xs))
    G=lambda f:bg(f)-Kt*f
    chi=s.Function('chi');xi=s.symbols('xi',real=True)
    zero('time_dependent_localization',f'energy cutoff generator d={d}',G(p*chi(HH))-(bg(p)-Kt*p)*chi(HH)-p*bg(HH)*s.diff(chi(HH),HH))
    zero('time_dependent_localization',f'energy Fourier generator d={d}',G(p*s.exp(s.I*xi*HH))-s.exp(s.I*xi*HH)*(bg(p)-Kt*p+s.I*xi*p*bg(HH)))
    zero('time_dependent_localization',f'alpha beta residual sign d={d}',-G(p*chi(HH))-(-(bg(p)-Kt*p)*chi(HH)-p*bg(HH)*s.diff(chi(HH),HH)))
    U=s.Function('U')(t,*xs);cut=s.Function('cut')(*xs)
    op=lambda f:s.diff(f,t)+G(f)
    zero('time_dependent_localization',f'spatial cutoff cancellation d={d}',op(cut*U)-cut*op(U)-U*bg(cut))

# Moving quadratic coefficients and exact pointwise SOS certificates.
T=s.symbols('T',positive=True);tt=s.symbols('tt',nonnegative=True)
V=(x-tt)**2;b=-2*(x-tt);HH=1+x*x;Cq=T*T;D=T*T+s.Rational(1,2);kk=s.Rational(1,2)
zero('moving_quadratic','drift growth certificate',Cq*HH-b*s.diff(HH,x)-(4*(x-tt/2)**2+T*T*x*x+T*T-tt*tt))
zero('moving_quadratic','killing domination certificate',V+D-kk*HH-((x-2*tt)**2/2+T*T-tt*tt))
zero('moving_quadratic','nonnegative scalar certificate factorization',T*T-tt*tt-(T-tt)*(T+tt))
zero('moving_quadratic','H SOS',HH-(1+x*x))

s0,t0,z0=s.symbols('s0 t0 z0',real=True)
tau=t0-s0;A=z0-s0+s.Rational(1,2)
phi=t0-s.Rational(1,2)+A*s.exp(-2*tau)
I=tau/4+A*A*(1-s.exp(-4*tau))/4-A*(1-s.exp(-2*tau))/2
IK=I+D*tau
zero('moving_quadratic','characteristic forward ODE',s.diff(phi,t0)+2*(phi-t0))
zero('moving_quadratic','characteristic initial value',phi.subs(t0,s0)-z0)
zero('moving_quadratic','characteristic initial-time equation',s.diff(phi,s0)-2*(z0-s0)*s.diff(phi,z0))
zero('moving_quadratic','integrated original killing derivative',s.diff(I,t0)-(phi-t0)**2)
zero('moving_quadratic','integrated killing initial value',I.subs(t0,s0))
zero('moving_quadratic','integrated shifted killing derivative',s.diff(IK,t0)-((phi-t0)**2+D))
zero('moving_quadratic','integrated killing start-time equation',s.diff(IK,s0)-2*(z0-s0)*s.diff(IK,z0)+(z0-s0)**2+D)
zero('moving_quadratic','positive affine slope',s.diff(phi,z0)-s.exp(-2*tau))
q,w,rr,ta,tb=s.symbols('q w rr ta tb',real=True)
f=lambda q,rr:q*(rr+s.Rational(1,2))-s.Rational(1,2)
J=lambda dur,q,A:dur/4+A*A*(1-q*q)/4-A*(1-q)/2
zero('moving_quadratic','relative two-time flow cocycle',f(q*w,rr)-f(q,f(w,rr)))
zero('moving_quadratic','two-time integrated killing cocycle',J(ta+tb,q*w,rr+s.Rational(1,2))-J(tb,w,rr+s.Rational(1,2))-J(ta,q,w*(rr+s.Rational(1,2))))
zero('moving_quadratic','two-atom log weight ratio',J(ta,q,-s.Rational(1,2))-J(ta,q,s.Rational(1,2))-(1-q)/2)
zero('moving_quadratic','two moving atom gap',f(q,-1)-f(q,0)+q)

# Retained proof-route obstruction, now for transported original killing.
zero('even_derivative_boundary','general transported quadratic integrand',V*V-b*s.diff(V,x)-s.diff(V,tt)-((x-tt)**4+4*(x-tt)**2+2*(x-tt)))
r0=-s.Rational(3,8)
zero('even_derivative_boundary','exact negative value',r0**4+4*r0*r0+2*r0+s.Rational(687,4096))
zero('even_derivative_boundary','chosen trajectory relative state',f(s.Rational(1,2),-s.Rational(1,4))-r0)
zero('even_derivative_boundary','interior time exponential',s.exp(-2*s.log(2)/2)-s.Rational(1,2))
true('even_derivative_boundary','interior time lies in horizon one',0<s.log(2)/2<1)

out={'status':'passed','checks':len(checks),'groups':{},'limits':'Finite exact controls supplement the ordinary universal proof; inherited regressions and integrity checks are explicitly separate.','details':checks}
for item in checks:out['groups'][item['group']]=out['groups'].get(item['group'],0)+1
(HERE/'EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
