#!/usr/bin/env python3
"""Independent exact controls for scoped singular Gaussian entrance."""
import sympy as S
import json
from pathlib import Path
b,B,y,z=S.symbols('b B y z',real=True)
s,T=S.symbols('s T',positive=True)
Sig=S.Matrix([[1,b],[b,b*b+s]])
Gam=S.Matrix([[1,B],[B,B*B+T]])
x=S.Matrix([y,z])
M=S.Matrix([[1+2*s+b*b/3,-2*b*s],[-2*b*s,2*s*(s+2+2*b*b)]])
g=S.Matrix([(b-B)/T,(s-T)/(2*s*T)])
f=S.simplify(-M*g)
C=Gam.inv()-Sig.inv()-(b-B)*(b-3*B)/T*S.diag(1,0)/3
V=-(C*Sig+Sig*C)-Sig*C*Sig
checks=[]
def ck(name,expr):
    es=list(expr) if isinstance(expr,S.MatrixBase) else [expr]
    ok=all(S.simplify(e)==0 for e in es)
    checks.append({'name':name,'pass':ok})
    if not ok: raise AssertionError((name,expr))
ck('covariance full tangent matches polynomial coordinates',V-S.Matrix([[0,f[0]],[f[0],2*b*f[0]+f[1]]]))
ck('full density continuity equation',(-S.trace(Sig.inv()*V)+(x.T*Sig.inv()*V*Sig.inv()*x)[0])/2-(S.trace(C)-(x.T*Sig.inv()*C*x)[0]-(x.T*C*x)[0]/2+S.trace(C*Sig)/2))
ck('positive boundary normal velocity',f[1].subs(s,0)-2*(1+b*b))
D=S.expand((g.T*M*g)[0])
ck('minimum field dissipation',D-S.trace(C*Sig*C)-S.trace((C*Sig)**2)/2)
R=S.cancel(D-(1+b*b)/s)
if S.denom(R).has(s): raise RuntimeError('regular remainder contains s denominator')
checks.append({'name':'remaining dissipation has no s pole','pass':True})
ck('energy derivative', (g.T*f)[0]+D)
a=2*(1+b*b)
ck('universal original time dissipation coefficient',S.limit(s*D,s,0)/a-S.Rational(1,2))
ck('universal square-root time action coefficient',4*S.limit(s*D,s,0)/a-2)
ck('singular covariance determinant',Sig.det().subs(s,0))
ck('singular covariance positive direction',Sig.subs(s,0)-S.Matrix([1,b])*S.Matrix([[1,b]]))
t=S.symbols('t',positive=True)
sex=2*(S.exp(3*t)-1)/(2*S.exp(3*t)+1)
ck('exact product singular entrance initial value',S.limit(sex,t,0))
ck('exact product singular entrance ODE',S.diff(sex,t)-(sex+2)*(1-sex))
ck('exact product dissipation coefficient',S.limit(t*D.subs({b:0,B:0,T:1,s:sex}),t,0)-S.Rational(1,2))
c,e=S.symbols('c e',real=True)
q=(z-B*y)**2/(2*T)-(z-c-b*y)**2/(2*s)
def cond(p):
    p=S.Poly(S.expand(p.subs(z,c+b*y+e)),e)
    return S.expand(sum(v*(s if mon[0]==2 else 1 if mon[0]==0 else 0) for mon,v in p.terms()))
h=cond(q); my=cond(S.diff(q,y))
rhs=-S.diff(my,y)+y*my+h-(h.coeff(y,0)+h.coeff(y,2))
phi=(b-B)*(b-3*B)*(y*y-1)/(6*T)+c*(b-2*B)*y/(2*T)
ck('noncentered multiplier derived by conditional averaging',-S.diff(phi,y,2)+y*S.diff(phi,y)+phi-rhs)
ell=Gam.inv()*S.Matrix([0,c])-S.Matrix([c*(b-2*B)/(2*T),0])
md=-(S.eye(2)+Sig)*ell
ck('noncentered mean dynamics',md-S.Matrix([0,-c*(1+s+b*b/2)/T]))
w=x-S.Matrix([0,c]); P=Sig.inv()
logdot=(-S.trace(P*V)+(w.T*P*V*P*w)[0])/2+(md.T*P*w)[0]
field=S.trace(C)-(w.T*P*(C*w+ell))[0]-(w.T*C*w)[0]/2+S.trace(C*Sig)/2-(ell.T*w)[0]
ck('noncentered full Gaussian density identity',logdot-field)
print(json.dumps({'status':'PASS','checks':checks,'regular_dissipation':str(R),'sympy':S.__version__},indent=2))
