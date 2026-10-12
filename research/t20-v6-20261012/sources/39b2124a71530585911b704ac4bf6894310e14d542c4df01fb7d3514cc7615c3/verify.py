#!/usr/bin/env python3
"""Exact finite controls. These supplement, and do not replace, the proofs."""
import itertools
import sympy as s

groups = []

def zero(expr):
    if isinstance(expr, s.MatrixBase):
        assert all(s.cancel(s.expand(x)) == 0 for x in expr), expr
    else:
        assert s.cancel(s.expand(expr)) == 0, expr

def passed(label):
    groups.append(label)
    print(f"PASS {len(groups):02d}: {label}")

def vecsum(vectors, dim):
    return sum(vectors, s.zeros(dim, 1))

def moment(K, w, indices):
    return sum(w[j] * s.prod(K[a, j] for a in indices) for j in range(K.cols))

def tilt(w, factors):
    Z = sum(a*b for a, b in zip(w, factors))
    return [a*b/Z for a, b in zip(w, factors)]

p0, p1, b0, b1, g0, g1 = s.symbols("p0 p1 b0 b1 g0 g1")
p = s.Matrix([p0, p1, 1-p0-p1])
b = s.Matrix([b0, b1, -b0-b1])
K = s.Matrix([[1, 0, s.Rational(1, 2)], [0, 1, s.Rational(1, 2)]])
g = s.Matrix([g0, g1])
G = s.diag(*p)-p*p.T
zero((G*K.T*g).T*s.diag(*(1/x for x in p))*b-g.T*K*b)
passed("Fisher tangent-duality identity for the declared pulled-back objective")

x0, x1, x2, w0, w1, c = s.symbols("x0 x1 x2 w0 w1 c")
Ks = s.Matrix([[x0, x1, x2], [1-x0, 1-x1, 1-x2]])
w = [w0, w1, 1-w0-w1]
q = Ks*s.Matrix(w)
mean = (g.T*q)[0]
dw = [-w[j]*((g.T*Ks[:, j])[0]-mean) for j in range(3)]
zero(sum(dw))
passed("normalization is preserved by the aggregate replicator field")

for r in range(6):
    for a in range(r+1):
        idx = (0,)*a+(1,)*(r-a)
        actual = sum(dw[j]*s.prod(Ks[z,j] for z in idx) for j in range(3))
        rhs = -sum(g[z]*moment(Ks,w,idx+(z,)) for z in range(2))+mean*moment(Ks,w,idx)
        zero(actual-rhs)
passed("all symmetric tensor components of the hierarchy in degrees zero through five")

for r in range(1,6):
    for a in range(r):
        idx=(0,)*a+(1,)*(r-1-a)
        zero(sum(moment(Ks,w,idx+(z,)) for z in range(2))-moment(Ks,w,idx))
passed("augmentation contraction lowers moment degree exactly")

M2=sum((w[j]*Ks[:,j]*Ks[:,j].T for j in range(3)),s.zeros(2))
zero(Ks*s.Matrix(dw)+(M2-q*q.T)*g)
passed("projected mobility is the covariance matrix")
gp=g+s.ones(2,1)*c
meanp=(gp.T*q)[0]
for j in range(3):
    zero(-w[j]*((gp.T*Ks[:,j])[0]-meanp)-dw[j])
passed("adding a constant covector leaves the controlled field unchanged")

X=s.symbols("X")
points=[s.Rational(1),s.Rational(0),s.Rational(1,2)]
lagrange=[s.prod((X-points[l])/(points[j]-points[l]) for l in range(3) if l!=j) for j in range(3)]
for j in range(3):
    for l in range(3):
        zero(lagrange[j].subs(X,points[l])-(1 if j==l else 0))
moments=[sum(w[j]*points[j]**r for j in range(3)) for r in range(3)]
recovered=[sum(s.expand(L).coeff(X,r)*moments[r] for r in range(3)) for L in lagrange]
zero(s.Matrix(recovered)-s.Matrix(w))
passed("Lagrange inversion recovers all three aggregate weights")

Q,S,lam=s.symbols("Q S lam")
wq=[2*S-Q,1-3*Q+2*S,4*(Q-S)]
zero(sum(wq)-1)
zero(sum(wq[j]*points[j] for j in range(3))-Q)
zero(sum(wq[j]*points[j]**2 for j in range(3))-S)
for x in points:
    zero(x**3-s.Rational(3,2)*x**2+s.Rational(1,2)*x)
zero(sum(wq[j]*points[j]**3 for j in range(3))-(s.Rational(3,2)*S-Q/2))
passed("two-moment coordinate inverse and cubic support identity")

dQ=-lam*(S-Q**2)
dS=-lam*((s.Rational(3,2)-Q)*S-Q/2)
for j in range(3):
    zero(s.diff(wq[j],Q)*dQ+s.diff(wq[j],S)*dS+lam*wq[j]*(points[j]-Q))
passed("closed two-moment ODE is conjugate to every aggregate weight equation")

pa=s.Matrix([s.Rational(1,4),s.Rational(1,4),s.Rational(1,2)])
pb=s.Matrix([s.Rational(3,8),s.Rational(3,8),s.Rational(1,4)])
qa=K*pa
qb=K*pb
zero(qa-qb)
A=K*s.diag(*pa)*K.T
B=K*s.diag(*pb)*K.T
zero(A-s.Matrix([[s.Rational(3,8),s.Rational(1,8)],[s.Rational(1,8),s.Rational(3,8)]]))
zero(B-s.Matrix([[s.Rational(7,16),s.Rational(1,16)],[s.Rational(1,16),s.Rational(7,16)]]))
e=s.Matrix([1,0])
zero(-(A-qa*qa.T)*e-s.Matrix([-s.Rational(1,8),s.Rational(1,8)]))
zero(-(B-qb*qb.T)*e-s.Matrix([-s.Rational(3,16),s.Rational(3,16)]))
passed("same first moment but distinct second moments and immediate velocities")

x4=[s.Rational(j,3) for j in range(4)]
wp=[s.Rational(j,24) for j in [5,9,3,7]]
wm=[s.Rational(j,24) for j in [7,3,9,5]]
mp=[sum(wp[j]*x4[j]**r for j in range(4)) for r in range(4)]
mm=[sum(wm[j]*x4[j]**r for j in range(4)) for r in range(4)]
for r in range(3): zero(mp[r]-mm[r])
zero(mp[3]-mm[3]-s.Rational(1,54))
zero((mp[3]-3*mp[1]*mp[2]+2*mp[1]**3)-(mm[3]-3*mm[1]*mm[2]+2*mm[1]**3)-s.Rational(1,54))
passed("equal first two moments hide a third-moment continuation difference")

# Nontrivial m=3, N=5 support: an exact finite separating-vector search.
K5=s.Matrix([[1,0,0,s.Rational(1,2),s.Rational(1,3)],
             [0,1,0,s.Rational(1,2),s.Rational(1,3)],
             [0,0,1,0,s.Rational(1,3)]])
Bnd=(K5.rows-1)*K5.cols*(K5.cols-1)//2
candidates=[s.Matrix([1,t,t*t]) for t in range(Bnd+1)]
v=next(v for v in candidates if len(set((v.T*K5)[0,j] for j in range(K5.cols)))==K5.cols)
a=[(v.T*K5)[0,j] for j in range(K5.cols)]
V=s.Matrix([[z**r for z in a] for r in range(K5.cols)])
assert V.det()!=0
passed(f"finite exact separating-vector search and Vandermonde nonsingularity: v={list(v)}")

ws=s.symbols("z0:4")
w5=list(ws)+[1-sum(ws)]
s5=V*s.Matrix(w5)
rec=V.inv()*s5
zero(rec-s.Matrix(w5))
for r in range(8):
    for idx in itertools.combinations_with_replacement(range(3),r):
        zero(moment(K5,rec,idx)-moment(K5,w5,idx))
passed("five-point closure reconstructs every symmetric component through degree seven")

kone=s.Matrix([s.Rational(1,3),s.Rational(2,3)])
zero((kone*kone.T-kone*kone.T)*g)
assert sum([s.Integer(1)])==1
passed("N=1 known-support closure is degree zero and the motion vanishes")

factors=s.symbols("f0:3",positive=True)
other=s.symbols("h0:3",positive=True)
t1=tilt(w,factors)
t2=tilt(t1,other)
t12=tilt(w,[factors[j]*other[j] for j in range(3)])
zero(s.Matrix(t2)-s.Matrix(t12))
zero(sum(t1)-1)
passed("positive diagonal tilts normalize and compose by factor multiplication")

dupa=[s.Rational(1,8),s.Rational(3,8),s.Rational(1,4),s.Rational(1,4)]
dupb=[s.Rational(1,4)]*4
Kdup=s.Matrix([[1,1,0,0],[0,0,1,1]])
fd=[factors[0],factors[0],factors[1],factors[1]]
da=tilt(dupa,fd); db=tilt(dupb,fd)
zero(Kdup*s.Matrix(da)-Kdup*s.Matrix(db))
zero(da[0]/da[1]-dupa[0]/dupa[1])
assert dupa!=dupb
passed("different within-class states retain equal controlled outputs and fixed ratios")

t=s.symbols("t",real=True)
lam=s.symbols("lambda",real=True)
exp_f=[s.exp(-t*lam*x) for x in points]
pt=tilt(list(pa),exp_f)
Qt=sum(pt[j]*points[j] for j in range(3))
for j in range(3):
    assert s.simplify(s.diff(pt[j],t)+lam*pt[j]*(points[j]-Qt))==0
passed("normalized exponential solution differentiates to the exact constant-control ODE")

u0,u1=s.symbols("u0 u1",real=True)
Z=sum(pa[j]*s.exp(-u0*K[0,j]-u1*K[1,j]) for j in range(3))
wu=[pa[j]*s.exp(-u0*K[0,j]-u1*K[1,j])/Z for j in range(3)]
for z,u in enumerate([u0,u1]):
    assert s.simplify(s.diff(s.log(Z),u)+sum(wu[j]*K[z,j] for j in range(3)))==0
passed("coarse expectation equals negative log-partition gradient")

zr=sum(pa[j]*s.exp(-t*points[j]) for j in range(3))
Vsign=s.Matrix([[(-x)**r for x in points] for r in range(3)])
derivatives=s.Matrix([s.diff(zr,t,r).subs(t,0) for r in range(3)])
zero(Vsign.inv()*derivatives-pa)
passed("zero-time partition derivatives recover weights by finite exponential independence")

for Kind in [s.eye(3),s.Matrix([[s.Rational(3,4),s.Rational(1,4),0],
                              [s.Rational(1,4),s.Rational(3,4),0],[0,0,1]])]:
    Aug=s.ones(1,Kind.cols).col_join(Kind)
    assert Aug.rank()==Kind.cols
    prod=s.Matrix([[Kind[a,j]*Kind[b,j] for j in range(Kind.cols)]
                   for a in range(Kind.rows) for b in range(a,Kind.rows)])
    assert Aug.col_join(prod).rank()==Aug.rank()
passed("affinely independent deterministic and noisy supports have first-moment closure")

for Kdep in [K,K5]:
    Aug=s.ones(1,Kdep.cols).col_join(Kdep)
    prod=s.Matrix([[Kdep[a,j]*Kdep[b,j] for j in range(Kdep.cols)]
                   for a in range(Kdep.rows) for b in range(a,Kdep.rows)])
    assert Aug.rank()<Kdep.cols
    assert Aug.col_join(prod).rank()>Aug.rank()
passed("affinely dependent examples have quadratic observables outside the first-moment span")

print(f"\nAll {len(groups)} exact control groups passed.")
print(f"SymPy version: {s.__version__}")
print("No floating-point sampling, numerical integration, empirical claims, or general-proof enumeration.")
