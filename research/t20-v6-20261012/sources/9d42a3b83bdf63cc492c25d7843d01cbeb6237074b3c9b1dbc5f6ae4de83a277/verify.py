#!/usr/bin/env python3
"""Exact finite controls; the ordinary proof is in RESULT.md."""
import sympy as s
Q=s.Rational
nchecks=0
def eq(a,b):
    if isinstance(a,s.MatrixBase): return a.shape==b.shape and all(s.simplify(z)==0 for z in a-b)
    return s.simplify(a-b)==0
def check(name,truth):
    global nchecks
    assert truth,name
    nchecks+=1
    print('PASS:',name)
def G(p): return s.diag(*p)-p*p.T
K=s.Matrix([[1,0,Q(1,2)],[0,1,Q(1,2)]])
p=s.Matrix([Q(1,4),Q(1,4),Q(1,2)])
r=s.Matrix([Q(3,8),Q(3,8),Q(1,4)])
q=s.Matrix([Q(1,2),Q(1,2)]);L=s.Matrix([[1,-1],[-1,1]])
check('positive normalized fine states share the same coarse state',sum(p)==sum(r)==1 and all(x>0 for x in list(p)+list(r)) and eq(K*p,q) and eq(K*r,q))
check('channel is column-stochastic and full row rank',eq(s.ones(1,2)*K,s.ones(1,3)) and K.rank()==2)
Ap=K*G(p)*K.T;Ar=K*G(r)*K.T
check('exact two distinct induced mobilities',eq(Ap,L/8) and eq(Ar,3*L/16))
g=s.Matrix([1,0]);v=-G(p)*K.T*g;vr=-G(r)*K.T*g
check('exact fine and projected objective velocities',eq(v,s.Matrix([-Q(1,8),Q(1,8),0])) and eq(vr,s.Matrix([-Q(3,16),Q(3,16),0])) and eq(K*v,s.Matrix([-Q(1,8),Q(1,8)])) and eq(K*vr,s.Matrix([-Q(3,16),Q(3,16)])))
check('canonical Fisher coarse velocity is a third value',eq(-G(q)*g,s.Matrix([-Q(1,4),Q(1,4)])))
check('each pointwise quotient metric is nondegenerate on the coarse tangent',Ap.rank()==Ar.rank()==1 and Ap[0,0]>0 and Ar[0,0]>0)
w=s.Matrix([1,-1])
check('same tangent displacement has different pointwise quotient energies',eq((w.T*Ap.pinv()*w)[0],8) and eq((w.T*Ar.pinv()*w)[0],Q(16,3)))
# Symbolic fibre: p=(x-z/2,1-x-z/2,z), 0<x<1 and 0<z<2 min(x,1-x).
x,z=s.symbols('x z',real=True);u=s.Matrix([x-z/2,1-x-z/2,z]);uu=K*u
check('symbolic fibre preserves coarse q=(x,1-x)',eq(uu,s.Matrix([x,1-x])))
check('symbolic mobility varies with hidden fibre coordinate',eq(K*G(u)*K.T,(x*(1-x)-z/4)*L))
# Exact positive global linear-objective solution via exponential tilting.
t=s.symbols('t',real=True);a=K.T*g
for name,start in [('p',p),('r',r)]:
    raw=s.Matrix([start[i]*s.exp(-a[i]*t) for i in range(3)])
    pt=raw/sum(raw)
    check(name+' explicit solution satisfies fine Fisher-gradient ODE',eq(pt.diff(t),-G(pt)*a) and eq(pt.subs(t,0),start) and eq(sum(pt),1))
# A deterministic lumping with symbolic simplex state.
x,y=s.symbols('x y',positive=True);u=s.Matrix([x,y,1-x-y]);Kd=s.Matrix([[1,1,0],[0,0,1]])
check('deterministic lumping exactly preserves Fisher cometric',eq(Kd*G(u)*Kd.T,G(Kd*u)))
# Entropy belongs to the earlier nonseparable perspective family.
b=s.Matrix(s.symbols('b1 b2 b3',positive=True));mass=sum(b);F=sum(b[i]*s.log(b[i]/mass) for i in range(3))+(mass-1)**2/2
H=s.hessian(F,list(b));E=(mass-1)**2/2+(K*(b/mass))[0]
subs=dict(zip(b,p));vel=-H.subs(subs).inv()*s.Matrix([s.diff(E,bi) for bi in b]).subs(subs)
check('full perspective-Hessian flow agrees at coherent starting state',eq(vel,v))
# Symmetric graded-moment identity, componentwise, under symbolic numerical control.
from itertools import product
u1,u2,g1,g2=s.symbols('u1 u2 g1 g2',real=True)
u=s.Matrix([u1,u2,1-u1-u2]);control=s.Matrix([g1,g2]);qq=K*u
udot=-G(u)*K.T*control
for order in range(5):
    for indices in product(range(2),repeat=order):
        monomial=lambda i:s.prod(K[j,i] for j in indices)
        moment=sum(u[i]*monomial(i) for i in range(3))
        lhs=sum(udot[i]*monomial(i) for i in range(3))
        contracted=sum(control[j]*sum(u[i]*monomial(i)*K[j,i] for i in range(3)) for j in range(2))
        rhs=-contracted+(qq.T*control)[0]*moment
        assert eq(lhs,rhs)
    check('symmetric moment identity at order '+str(order),True)
check('first-moment dynamics are covariance action',eq(K*udot,-(K*s.diag(*u)*K.T-qq*qq.T)*control))

print(f'\n{nchecks} exact control groups passed; no statistical sampling or numerical integration.')
