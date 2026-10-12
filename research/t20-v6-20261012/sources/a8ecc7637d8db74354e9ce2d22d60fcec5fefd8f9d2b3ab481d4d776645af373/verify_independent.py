#!/usr/bin/env python3
"""Independent exact controls for the finite known-support moment bridge.
Finite checks supplement the written proof; they do not certify a theorem kernel.
"""
from itertools import product
from math import comb
import sympy as s
R = s.Rational
checks = []
def same(a,b):
    if isinstance(a,s.MatrixBase):
        return a.shape == b.shape and all(s.simplify(z)==0 for z in a-b)
    return s.simplify(a-b)==0
def check(name,value):
    assert value,name
    checks.append(name)
    print('PASS:',name)

# Four collinear probability columns; this tests a genuinely nontrivial top closure.
xs=[R(j,3) for j in range(4)]
ks=[s.Matrix([x,1-x]) for x in xs]
V=s.Matrix([[x**r for x in xs] for r in range(4)])
a,b,c=s.symbols('a b c',real=True)
w=s.Matrix([a,b,c,1-a-b-c]); g=s.Matrix(s.symbols('g1 g2',real=True))
q=sum((w[j]*ks[j] for j in range(4)),s.zeros(2,1))
wdot=s.Matrix([-w[j]*(g.dot(ks[j])-g.dot(q)) for j in range(4)])
check('separating Vandermonde is exactly invertible',V.det()!=0 and same(V.inv()*V,s.eye(4)))
z=V*w
check('scalar moments through N-1 recover all normalized weights',same(V.inv()*z,w))
x=s.symbols('x')
lagrange=[s.prod((x-xs[i])/(xs[j]-xs[i]) for i in range(4) if i!=j).expand() for j in range(4)]
check('Lagrange indicators recover weights',all(same(sum(lagrange[j].coeff(x,r)*z[r] for r in range(4)),w[j]) for j in range(4)))
for r in range(7):
    for ii in product(range(2),repeat=r):
        vals=s.Matrix([s.prod(ks[j][i] for i in ii) for j in range(4)])
        direct=(w.T*vals)[0]
        recovered=(z.T*V.inv().T*vals)[0]
        assert same(direct,recovered)
    check('full tensor reconstructed from scalar degrees 0..3 at order '+str(r),True)
for r in range(5):
    for ii in product(range(2),repeat=r):
        vals=[s.prod(ks[j][i] for i in ii) for j in range(4)]
        moment=sum(w[j]*vals[j] for j in range(4))
        lhs=sum(wdot[j]*vals[j] for j in range(4))
        rhs=-sum(w[j]*vals[j]*g.dot(ks[j]) for j in range(4))+g.dot(q)*moment
        assert same(lhs,rhs)
    check('componentwise hierarchy under arbitrary symbolic control at order '+str(r),True)
check('zeroth moment derivative is exactly zero',same(sum(wdot),0))

# Same M0,M1,M2, distinct M3: no first/second-moment universal closure for N=4.
w0=s.ones(4,1)/4
delta=s.Matrix([-1,3,-3,1])
w1=w0+delta/24
check('sharpness witnesses have strictly positive normalized weights',sum(w0)==sum(w1)==1 and all(v>0 for v in list(w0)+list(w1)))
check('full tensors through degree two coincide',all(same(sum((w1[j]-w0[j])*s.prod(ks[j][i] for i in ii) for j in range(4)),0) for r in range(3) for ii in product(range(2),repeat=r)))
raw3=sum((w1[j]-w0[j])*xs[j]**3 for j in range(4))
check('third directional moment separates by 1/108',raw3==R(1,108))
def cumulants(weights):
    m=[sum(weights[j]*xs[j]**r for j in range(4)) for r in range(4)]
    return m[1],m[2]-m[1]**2,m[3]-3*m[2]*m[1]+2*m[1]**3
c0,c1=cumulants(w0),cumulants(w1)
check('constant-control q and qdot agree, qddot differs by 1/108',c0[:2]==c1[:2] and c1[2]-c0[2]==R(1,108))
for N in range(2,8):
    nodes=[R(j,N-1) for j in range(N)]
    d=[(-1)**(N-1-j)*comb(N-1,j) for j in range(N)]
    assert all(sum(d[j]*nodes[j]**r for j in range(N))==0 for r in range(N-1))
    assert sum(d[j]*nodes[j]**(N-1) for j in range(N))!=0
    check('finite-difference universal-bound sharpness at N='+str(N),True)

# Time interval away from zero: tilted exponential coefficient matrix remains full rank.
# At t0=3 log 2 and these lambda_j, exponentials are exactly 2^(-j).
tilts=s.diag(*[R(1,2**j) for j in range(4)])
D=s.diag(*[(-1)**r for r in range(4)])
W=D*V*tilts
check('derivatives 0..N-1 at positive interior time identify exponential coefficients',W.det()!=0)
scale=s.symbols('scale')
check('normalization removes response proportionality scale',same(sum(scale*w)-1,scale-1))

# N=1 contains no dynamical weight freedom; M0 reconstructs every known tensor.
single=s.Matrix([R(2,5),R(3,5)])
check('N=1 control is stationary and needs only M0',same(-g.dot(single)+g.dot(single),0) and sum(single)==1)

# Duplicate columns: different fine weights cannot be distinguished after aggregation.
Kdup=s.Matrix([[1,1,0,R(1,2)],[0,0,1,R(1,2)]])
u=s.Matrix([R(1,10),R(3,10),R(1,5),R(2,5)])
v=s.Matrix([R(1,5),R(1,5),R(1,5),R(2,5)])
B=s.Matrix([[1,1,0,0],[0,0,1,0],[0,0,0,1]])
check('distinct positive fine states can have identical duplicate-group weights',u!=v and same(B*u,B*v) and all(t>0 for t in list(u)+list(v)))
for r in range(6):
    assert all(same(sum((u[j]-v[j])*s.prod(Kdup[i,j] for i in ii) for j in range(4)),0) for ii in product(range(2),repeat=r))
check('duplicate-group equivalence preserves every tested full moment',True)

# Nongeneric all-ones control cannot distinguish any weights on probability columns.
ones=s.ones(2,1)
check('all-ones control has identical projection on every column',all(ones.dot(k)==1 for k in ks))
check('all-ones control leaves every weight stationary',all(same(-w[j]*(ones.dot(ks[j])-ones.dot(q)),0) for j in range(4)))

# A genuinely noisy two-column map still has a q-only field, but not canonical Fisher.
qx=s.symbols('qx',real=True)
noisy=[R(1,4),R(3,4)]
weights=[R(3,2)-2*qx,2*qx-R(1,2)]
second=sum(weights[j]*noisy[j]**2 for j in range(2))
variance=s.factor(second-qx*qx)
check('affinely independent noisy support has polynomial q-only mobility',same(variance,(qx-R(1,4))*(R(3,4)-qx)))
check('q-only descent does not imply canonical coarse Fisher mobility',same(qx*(1-qx)-variance,R(3,16)))

# Unknown support: same scalar response in a fixed direction need not recover full vectors.
K_A=s.Matrix([[1,0],[0,1],[0,0]])
K_B=s.Matrix([[1,R(1,2)],[0,0],[0,R(1,2)]])
probe=s.Matrix([0,1,2])
check('different supports have identical distinct projected support values',same(K_A.T*probe,K_B.T*probe) and list(K_A.T*probe)==[0,1] and K_A!=K_B)
r=s.symbols('r',positive=True)
wt=s.Matrix([1,r])/(1+r)
check('unknown-support scalar responses agree but vector responses differ',same(probe.dot(K_A*wt),probe.dot(K_B*wt)) and not same(K_A*wt,K_B*wt))

# Successive fixed-column controls depend on cumulative exponential factors.
factors=s.symbols('f0:4',positive=True)
factors2=s.symbols('h0:4',positive=True)
def tilt(weights,fs):
    raw=s.Matrix([weights[j]*fs[j] for j in range(4)])
    return raw/sum(raw)
check('normalized exponential tilts compose exactly',same(tilt(tilt(w0,factors),factors2),tilt(w0,[factors[j]*factors2[j] for j in range(4)])))
print('\n'+str(len(checks))+' independent exact control groups passed.')
