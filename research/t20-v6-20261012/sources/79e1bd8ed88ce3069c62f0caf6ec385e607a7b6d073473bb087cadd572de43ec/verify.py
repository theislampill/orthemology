#!/usr/bin/env python3
"""Exact controls only. Universal theorems are proved in RESULT.md."""
from pathlib import Path
import hashlib
import json
import itertools
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
checks = []

def record(name, ok, detail=None):
    if not bool(ok):
        raise AssertionError(name + (": " + str(detail) if detail is not None else ""))
    checks.append({"name": name, "status": "PASS", "detail": str(detail) if detail is not None else None})

def zero(name, expression):
    expression = S.simplify(S.expand_log(expression, force=True))
    record(name, expression == 0, expression)

def matrix_zero(name, expression):
    record(name, all(S.simplify(x) == 0 for x in expression), str(expression))

def simplex(p):
    return sum(p) == 1 and all(x > 0 for x in p)

def admissible(K):
    return all(x >= 0 for x in K) and all(sum(K[:, j]) == 1 for j in range(K.cols)) and all(sum(K[i, :]) > 0 for i in range(K.rows))

def kl(p, q):
    return sum(a*S.log(a/b) for a, b in zip(p, q))

def quadratic(p, q, mu=None):
    mu = mu if mu is not None else S.ones(len(p), 1)
    return sum((a-b)**2/w for a, b, w in zip(p, q, mu))/2

def fisher(p, v):
    return sum(x*x/a for a, x in zip(p, v))

def split(sizes):
    E = S.zeros(sum(sizes), len(sizes))
    R = S.zeros(len(sizes), sum(sizes))
    offset = 0
    for i, count in enumerate(sizes):
        for j in range(offset, offset+count):
            E[j,i] = S.Rational(1,count)
            R[i,j] = 1
        offset += count
    return E,R

# Baseline preservation and inherited pin bindings.
baseline = json.loads((HERE/'INPUT_BASELINE.json').read_text())
for row in baseline:
    b = (ROOT/row['path']).read_bytes()
    record('preserved input: '+row['path'], hashlib.sha256(b).hexdigest() == row['sha256'])
    blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    record('input blob recomputation: '+row['path'], blob == row['git_blob_sha_of_local_bytes'])
record('pinned Hessian source blob', baseline[2]['git_blob_sha_of_local_bytes'] == '0b7f307cabd85b4d73215f024d70112a5dcd07c4')
record('pinned sound-descent source blob', baseline[4]['git_blob_sha_of_local_bytes'] == '0929ef49e847b3bcfd5847600a6a80c46283f2f7')

# Arbitrary rational law embedded into a uniform law.
E,R = split((2,3,1))
p = S.Matrix([S.Rational(1,3), S.Rational(1,2), S.Rational(1,6)])
q = S.Matrix([S.Rational(1,4), S.Rational(1,4), S.Rational(1,2)])
v = S.Matrix([S.Rational(1,6),-S.Rational(1,4), S.Rational(1,12)])
record('rational laws interior and tangent sum zero', simplex(p) and simplex(q) and sum(v) == 0)
record('split and coarsen admissible', admissible(E) and admissible(R))
matrix_zero('split has stochastic left inverse', R*E-S.eye(3))
matrix_zero('rational law splits to uniform', E*p-S.ones(6,1)/6)
zero('Fisher split isometry', fisher(E*p,E*v)-fisher(p,v))
zero('KL split isometry', kl(E*p,E*q)-kl(p,q))
zero('uniform curvature at N gives rational Fisher', 6*(E*v).dot(E*v)-fisher(p,v))
E23,R23 = split((3,3))
u = S.Matrix([S.Rational(1,2)]*2)
w = S.Matrix([S.Rational(2,7),-S.Rational(2,7)])
matrix_zero('uniform splitting maps barycenter', E23*u-S.ones(6,1)/6)
zero('uniform splitting divides Euclidean norm by k', (E23*w).dot(E23*w)-w.dot(w)/3)
zero('uniform alpha_n equals c n', 2*w.dot(w)-6*(E23*w).dot(E23*w))

# Fixed-binary contraction algebra, not a sampling experiment.
a,b,r,t = S.symbols('a b r t', real=True)
Kb = S.Matrix([[a,b],[1-a,1-b]])
pb,qb = S.Matrix([r,1-r]),S.Matrix([t,1-t])
zero('binary quadratic exact contraction factor', quadratic(Kb*pb,Kb*qb)-(a-b)**2*quadratic(pb,qb))
zero('binary square distance expression', quadratic(pb,qb)-(r-t)**2)
z = S.symbols('z',positive=True)
Hb = z*S.log(z)+(1-z)*S.log(1-z)
zero('binary entropy Hessian', S.diff(Hb,z,2)-1/(z*(1-z)))
record('binary quadratic not a common KL scaling', S.diff(Hb,z,2).subs(z,S.Rational(1,2)) != S.diff(Hb,z,2).subs(z,S.Rational(1,4)))

# Exact inherited reset/transported-reference comparison.
K = S.Matrix([[1,1,0],[0,0,1]])
R = S.Matrix([[S.Rational(1,2),0],[S.Rational(1,2),0],[0,1]])
p = S.Matrix([S.Rational(3,8),S.Rational(3,8),S.Rational(1,4)])
q = S.Matrix([S.Rational(1,4),S.Rational(1,4),S.Rational(1,2)])
record('inherited channels admissible', admissible(K) and admissible(R))
matrix_zero('inherited pair recovery p', R*K*p-p)
matrix_zero('inherited pair recovery q', R*K*q-q)
zero('fine half-Brier 3/64', quadratic(p,q)-S.Rational(3,64))
zero('reset coarse half-Brier 1/16', quadratic(K*p,K*q)-S.Rational(1,16))
record('reset Brier strict increase', quadratic(K*p,K*q) > quadratic(p,q))
mu=S.ones(3,1)
matrix_zero('reference transports to block weights', K*mu-S.Matrix([2,1]))
zero('transported reference preserves divergence', quadratic(K*p,K*q,K*mu)-quadratic(p,q,mu))
zero('recoverable pair preserves KL', kl(K*p,K*q)-kl(p,q))

# Fisher contraction matrix is positive semidefinite: every principal minor exact.
J=S.Matrix([[S.Rational(1,2),S.Rational(1,3),S.Rational(1,4)],
            [S.Rational(1,2),S.Rational(2,3),S.Rational(3,4)]])
record('genuinely stochastic channel admissible', admissible(J))
M=S.diag(*[1/x for x in q])-J.T*S.diag(*[1/x for x in J*q])*J
matrix_zero('Fisher defect annihilates radial law',M*q)
for count in range(1,4):
    for indices in itertools.combinations(range(3),count):
        d=S.factor(M.extract(indices,indices).det())
        record('Fisher defect principal minor '+str(indices),d >= 0,d)

# Cone entropy-perspective plus arbitrary radial term, with symbolic two-state probabilities.
s,t,c=S.symbols('s t c',positive=True)
p1,q1=S.symbols('p1 q1',positive=True)
aa=S.Function('a')
x1,x2,y1,y2=S.symbols('x1 x2 y1 y2',positive=True)
sx=x1+x2
F=c*(x1*S.log(x1)+x2*S.log(x2)-sx*S.log(sx))+aa(sx)
Fy=F.subs({x1:y1,x2:y2})
D=F-Fy-S.diff(F,x1).subs({x1:y1,x2:y2})*(x1-y1)-S.diff(F,x2).subs({x1:y1,x2:y2})*(x2-y2)
sub={x1:s*p1,x2:s*(1-p1),y1:t*q1,y2:t*(1-q1)}
target=c*s*(p1*S.log(p1/q1)+(1-p1)*S.log((1-p1)/(1-q1)))+aa(s)-aa(t)-S.diff(aa(t),t)*(s-t)
zero('symbolic full-cone divergence split',D.subs(sub)-target)
zero('mixed Hessian radial restriction',S.diff(F,x1,x2)-(S.Subs(S.diff(aa(z),z,2),z,sx)-c/sx))

# Affine radial gauges and normalized-only counterexample.
lam,beta=S.symbols('lam beta',real=True)
rad=lambda expr:S.expand(expr.subs(z,s)-expr.subs(z,t)-S.diff(expr,z).subs(z,t)*(s-t))
zero('affine radial gauges cancel',rad(z**2/2+lam*z+beta)-rad(z**2/2))
zero('quadratic radial divergence',rad(z**2/2)-(s-t)**2/2)
zero('normalized radial divergence vanishes',rad(z**2).subs({s:1,t:1}))
record('dimension-dependent radial cone violation',rad(z**2).subs({s:2,t:1})-rad(z**2/2).subs({s:2,t:1}) == S.Rational(1,2))
zero('entropy radial curvature required for additivity',S.diff(c*z*S.log(z),z,2)-c/z)
Fadd=F.replace(aa(sx),c*sx*S.log(sx))
zero('additive radial entropy cancels perspective coupling',Fadd-c*(x1*S.log(x1)+x2*S.log(x2)))
Fquad=F.replace(aa(sx),sx**2/2)
zero('quadratic radial mixed derivative',S.diff(Fquad,x1,x2)-(1-c/sx))
record('quadratic radial not coordinate additive', S.diff(Fquad,x1,x2).subs({x1:1,x2:1,c:1}) == S.Rational(1,2))
zero('strictly convex quartic has degenerate radial Hessian at one',S.diff((z-1)**4,z,2).subs(z,1))

# Positive-definite Hessian decomposition for quadratic radial shape.
h1,h2=S.symbols('h1 h2',real=True)
h=S.Matrix([h1,h2]); xx=S.Matrix([x1,x2]); tau=h1+h2
vv=h-xx*tau/sx
H=S.hessian(Fquad,(x1,x2))
zero('quadratic-radial cone Hessian decomposition',(h.T*H*h)[0]-(c*sum(vv[i]**2/xx[i] for i in range(2))+tau**2))
zero('quadratic-radial Hessian determinant',H.det()-c*sx/(x1*x2))

# Recoverable refinements preserve KL without preserving absolute logarithmic risk.
E,R=split((2,1))
p=S.Matrix([S.Rational(3,4),S.Rational(1,4)])
q=S.Matrix([S.Rational(1,2),S.Rational(1,2)])
entropy=lambda p:-sum(x*S.log(x) for x in p)
zero('split absolute entropy risk offset',entropy(E*p)-entropy(p)-p[0]*S.log(2))
zero('same split nevertheless preserves KL',kl(E*p,E*q)-kl(p,q))

out={'status':'PASS','check_count':len(checks),'method':'Exact SymPy symbolic/rational checks; no sampling, numerical optimisation, or proof-assistant certification.','checks':checks}
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'check_count':len(checks),'method':out['method']},indent=2))
