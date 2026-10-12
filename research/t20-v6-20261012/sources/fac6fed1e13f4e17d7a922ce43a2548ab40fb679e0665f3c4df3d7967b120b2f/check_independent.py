#!/usr/bin/env python3
"""Exact finite controls, not formal verification of the general theorem."""
import json
from pathlib import Path
import sympy as s
x,y,t,a,c,u,v,w,z=s.symbols('x y t a c u v w z', real=True)
r=x*x+y*y
b=s.Matrix([-y*r,x*r])
checks={}
def ck(name, expr):
    assert s.simplify(expr)==0, (name,expr)
    checks[name]=True
ck('cubic_rotation_radius', 2*x*b[0]+2*y*b[1])
ck('cubic_rotation_divergence', s.diff(b[0],x)+s.diff(b[1],y))
# r is invariant; rotation angular speed is r0.
r0=a*a+c*c
X=a*s.cos(r0*t)-c*s.sin(r0*t)
Y=a*s.sin(r0*t)+c*s.cos(r0*t)
ck('rotation_flow_x', s.diff(X,t)+Y*(X*X+Y*Y))
ck('rotation_flow_y', s.diff(Y,t)-X*(X*X+Y*Y))
ck('rotation_flow_radius',X*X+Y*Y-r0)
# An affine example x'=2x+3 with nonconstant polynomial killing k=x².
F=(a+s.Rational(3,2))*s.exp(2*t)-s.Rational(3,2)
K=(a+s.Rational(3,2))**2*(s.exp(4*t)-1)/4 -s.Rational(3,2)*(a+s.Rational(3,2))*(s.exp(2*t)-1)+s.Rational(9,4)*t
ck('affine_flow',s.diff(F,t)-2*F-3)
ck('affine_killing_integral',s.diff(K,t)-F*F)
ck('affine_source_reaction',(-x*x-2)+s.diff(2*x+3,x)+x*x)
# Normalized two-atom invertibility with symbolic positive weights and factors.
D=w*u+(1-w)*v
q=w*u/D
ck('normalized_inverse', (q/u)/(q/u+(1-q)/v)-w)
# Jet cardinal polynomials for 0,1,3, exercising the Hermite forcing tests.
nodes=[s.Integer(0),s.Integer(1),s.Integer(3)]
for i,xi in enumerate(nodes):
    ell=s.prod((z-xj)/(xi-xj) for j,xj in enumerate(nodes) if j!=i)
    h=(1-2*s.diff(ell,z).subs(z,xi)*(z-xi))*ell**2
    g=(z-xi)*ell**2
    for j,xj in enumerate(nodes):
        ck(f'value_cardinal_{i}_{j}',h.subs(z,xj)-int(i==j))
        ck(f'value_zero_derivative_{i}_{j}',s.diff(h,z).subs(z,xj))
        ck(f'jet_zero_value_{i}_{j}',g.subs(z,xj))
        ck(f'jet_cardinal_derivative_{i}_{j}',s.diff(g,z).subs(z,xj)-int(i==j))
# Exact two-atom normalized transport/selection derivative for general monomial n.
# Formal velocities X'=B,Y'=C and weight q'=(q*kX+(1-q)*kY-kX)*q.
X,Y,B,C,kX,kY,q=s.symbols('X Y B C kX kY q')
for n in range(13):
    m=q*X**n+(1-q)*Y**n
    qdot=((q*kX+(1-q)*kY)-kX)*q
    lhs=s.diff(m,q)*qdot+s.diff(m,X)*B+s.diff(m,Y)*C
    transport=q*B*s.diff(z**n,z).subs(z,X)+(1-q)*C*s.diff(z**n,z).subs(z,Y)
    rhs=transport-q*kX*X**n-(1-q)*kY*Y**n+(q*kX+(1-q)*kY)*m
    ck(f'normalized_transport_monomial_{n}',lhs-rhs)
# Forward-complete but not backward-complete coercive gradient example F=x^4/4.
Xg=a/s.sqrt(1+2*t*a*a)
Kg=a*a/s.Integer(8)*(1-1/(1+2*t*a*a))
ck('coercive_gradient_forward_ode',s.diff(Xg,t)+Xg**3)
ck('coercive_gradient_killing_integral',s.diff(Kg,t)-Xg**4/4)
ck('coercive_gradient_energy_descent',s.diff(x**4/4,x)*(-x**3)+x**6)
ck('coercive_gradient_image_gap',1-2*t*Xg**2-1/(1+2*t*a*a))
result={'status':'PASS','checks':len(checks),'scope':'Exact finite algebra controls only; general lifting/globalization is ordinary mathematics, not kernel-checked.', 'results':checks}
Path(__file__).with_name('INDEPENDENT_EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks)}))
