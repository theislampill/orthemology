#!/usr/bin/env python3
"""Independent finite exact controls; not a proof of the general theorems."""
import argparse, hashlib, json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, default=ROOT/'independent-run')
parser.add_argument('--original-root', type=Path)
args = parser.parse_args()
if args.output_dir.exists():
    parser.error('output directory already exists; provide a fresh path')
args.output_dir.mkdir(parents=True)
checks = []
def eq(name, expr):
    residual = s.simplify(s.expand(expr))
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append({'name': name, 'residual': '0'})
def truth(name, statement):
    if not bool(statement):
        raise AssertionError(name)
    checks.append({'name': name, 'verified': True})

# Independent constrained-coordinate differentiation, two moving scalar atoms.
u, a, b, x = s.symbols('u a b x', real=True)
G = s.diag(1/u+1/(1-u),u,1-u)
Ginv = s.diag(u*(1-u),1/u,1/(1-u))
eq('constrained simplex inverse metric', (G*Ginv-s.eye(3)).norm()**2)
F = x**4/4 + x**2/2 + 3*x
Fa,Fb = F.subs(x,a),F.subs(x,b)
E = u*Fa+(1-u)*Fb
gradE = Ginv*s.Matrix([s.diff(E,z) for z in [u,a,b]])
expected = s.Matrix([u*(Fa-E),s.diff(F,x).subs(x,a),s.diff(F,x).subs(x,b)])
for j in range(3): eq(f'gradient component {j}',gradE[j]-expected[j])
vel = -gradE
for j in range(3): eq(f'negative gradient sign {j}',vel[j]+expected[j])
D = (s.Matrix([s.diff(E,z) for z in [u,a,b]]).T*vel)[0]
VarF = u*Fa**2+(1-u)*Fb**2-E**2
sqgrad = u*s.diff(F,x).subs(x,a)**2+(1-u)*s.diff(F,x).subs(x,b)**2
eq('energy dissipation including selection variance',D+sqgrad+VarF)
eq('squared gradient norm equals dissipation',(gradE.T*G*gradE)[0]-sqgrad-VarF)

mom = [u*a**k+(1-u)*b**k for k in [1,2,3]]
J = s.Matrix(mom).jacobian([u,a,b])
eq('rank-three moment Jacobian determinant',J.det()-u*(1-u)*(a-b)**4)
C = J*Ginv*J.T
for i in range(3):
    for j in range(3):
        p,q=x**(i+1),x**(j+1)
        L=lambda z: u*z.subs(x,a)+(1-u)*z.subs(x,b)
        expected_B=L(s.diff(p,x)*s.diff(q,x))+L(p*q)-L(p)*L(q)
        eq(f'full cometric ({i+1},{j+1})',C[i,j]-expected_B)
truth('mixed moment cometric is not diagonal',C[0,1].subs({u:s.Rational(1,3),a:0,b:2})==s.Rational(40,9))
# A constant polynomial is in the cotangent radical.
eq('constant cotangent radical', u*Fa+(1-u)*Fb-E)

# Multivariate degree-(2r-1) frozen Hermite jets, r=3, d=2.
x,y=s.symbols('x y',real=True)
points=[(0,0),(1,2),(3,1)]
ell=x+3*y
lams=[ell.subs({x:p[0],y:p[1]}) for p in points]
truth('separating projection',len(set(lams))==3)
for i, point in enumerate(points):
    e=s.prod((ell-lams[k])/(lams[i]-lams[k]) for k in range(3) if k!=i)
    de=s.Matrix([s.diff(e,z).subs({x:point[0],y:point[1]}) for z in [x,y]])
    h=s.expand((1-2*(de[0]*(x-point[0])+de[1]*(y-point[1])))*e**2)
    tests=[h,s.expand((x-point[0])*e**2),s.expand((y-point[1])*e**2)]
    for k,p in enumerate(tests):
        truth(f'Hermite degree bound atom {i} jet {k}',s.Poly(p,x,y).total_degree()<=5)
        for j,other in enumerate(points):
            sub={x:other[0],y:other[1]}
            eq(f'Hermite value atom {i} jet {k} node {j}',p.subs(sub)-(1 if k==0 and i==j else 0))
            for d,z in enumerate([x,y]):
                eq(f'Hermite gradient atom {i} jet {k} node {j} dim {d}',s.diff(p,z).subs(sub)-(1 if i==j and k==d+1 else 0))

# Unknown-support discrimination. Through degree 2r-2 can fail already r=2.
x=s.symbols('x',real=True)
L1=lambda p: (p.subs(x,-1)+p.subs(x,1))/2
L2=lambda p: s.Rational(1,5)*p.subs(x,2)+s.Rational(4,5)*p.subs(x,-s.Rational(1,2))
for k in range(3): eq(f'insufficient degree-two two-atom prefix {k}',L1(x**k)-L2(x**k))
truth('degree-three distinguishes positive two-atom laws',L1(x**3)!=L2(x**3))
V=s.Matrix([[s.Integer(z)**k for z in range(6)] for k in range(6)])
truth('six-node signed difference test degrees zero through five',V.det()!=0)

# The full-polynomial cotangent radical is larger than constants.
z=s.symbols('z',real=True)
pnull=z**2*(z-2)**2
for node in [0,2]:
    eq(f'nonconstant conormal value at {node}',pnull.subs(z,node))
    eq(f'nonconstant conormal derivative at {node}',s.diff(pnull,z).subs(z,node))
truth('conormal polynomial is genuinely nonconstant',s.degree(pnull,z)==4)

# Distinctive two-atom chart reconstruction and inadmissible Euclidean boundary.
a,b,c=s.symbols('a b c',real=True)
D=b-a*a
sigma=(c-a*b)/D
product=(a*c-b*b)/D
central3=c-3*a*b+2*a**3
eq('two-atom discriminant positivity decomposition',sigma**2-4*product-central3**2/D**2-4*D)
eq('mean strictly between roots test',a*a-sigma*a+product+D)
M4=sigma*c-product*b
eq('fourth moment selection variance square',M4-b*b-(c-a*b)**2/D)
epsilon=s.symbols('epsilon',positive=True)
eq('boundary sequence fourth moment divergence',M4.subs({a:0,b:epsilon,c:1})-(1/epsilon+epsilon**2))

# Exact full normalized transport-selection hierarchy, nonquadratic F.
a,b,u,x=s.symbols('a b u x',real=True)
F=x**4/4+x**2/2
Fa,Fb=F.subs(x,a),F.subs(x,b)
E=u*Fa+(1-u)*Fb
velocity=[-u*(Fa-E),-s.diff(F,x).subs(x,a),-s.diff(F,x).subs(x,b)]
L=lambda p:u*p.subs(x,a)+(1-u)*p.subs(x,b)
for k in range(11):
    p=x**k; moment=L(p)
    lhs=sum(s.diff(moment,z)*v for z,v in zip([u,a,b],velocity))
    rhs=-L(s.diff(p,x)*s.diff(F,x))-L(p*F)+L(p)*E
    eq(f'normalized hierarchy degree {k}',lhs-rhs)

# Strongly convex quadratic: exact convergence, positive limiting weights,
# and asymptotic support collapse without finite-time merging.
z=s.symbols('z',positive=True)
w2=2*s.exp(z-1)/(1+2*s.exp(z-1))
E=2*z*w2
Var=4*z*z*w2*(1-w2)
eq('quadratic objective dissipation',-2*z*s.diff(E,z)+2*E+Var)
truth('limiting second weight is strictly between zero and one',0<w2.subs(z,0)<1)
a,t=s.symbols('a t',real=True)
X=a*s.exp(-t)
eq('quadratic characteristic',s.diff(X,t)+X)
truth('quadratic finite-time derivative positive',s.diff(X,a).is_positive)
h,a=s.symbols('h a',positive=True)
X=a/s.sqrt(1+2*a*a*h)
K=a*a*(1-1/(1+2*a*a*h))/8
eq('coercive quartic forward characteristic',s.diff(X,h)+X**3)
eq('coercive quartic killing integral',s.diff(K,h)-X**4/4)

# Finite-distance weight and collision boundaries, and ambient reaction bound.
theta=s.symbols('theta',positive=True)
w=s.cos(theta)**2
reaction=s.diff(w,theta)**2/w+s.diff(1-w,theta)**2/(1-w)
eq('two-point reaction metric speed squared',s.trigsimp(reaction)-4)
eq('reaction-only endpoint path length',s.integrate(s.Integer(2),(theta,0,s.pi/2))-s.pi)
a=s.symbols('a',positive=True)
eq('equal-weight collision path speed squared',s.Rational(1,2)*s.diff(a,a)**2+s.Rational(1,2)*s.diff(-a,a)**2-1)
# LM unit sphere metric versus the Fisher factor used here.
eq('weight unit sphere normalization ratio',s.trigsimp(s.diff(s.cos(theta),theta)**2+s.diff(s.sin(theta),theta)**2)-1)

bindings=json.loads((ROOT/'PREDECESSOR_BINDINGS.json').read_text())
for relative,meta in bindings.items():
    path=ROOT/'inputs'/relative
    truth('copied predecessor '+relative,hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'])
    if args.original_root is not None:
        path=args.original_root/relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'], relative

result={'status':'PASS','evidence_tier':'finite exact symbolic controls, not formal-kernel proof','checks':len(checks),'check_details':checks,'sympy_version':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'copied_predecessors_verified':True,'original_predecessors_preserved':True if args.original_root is not None else None}
(args.output_dir/'INDEPENDENT_EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='check_details'},indent=2))
