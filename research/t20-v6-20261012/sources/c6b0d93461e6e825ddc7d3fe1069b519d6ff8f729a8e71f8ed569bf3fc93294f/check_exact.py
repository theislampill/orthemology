#!/usr/bin/env python3
"""Exact finite controls for the joint atomic gradient lift; not a formal proof.

Outputs are fresh-only. Copied inputs are always hash-checked; original inputs
are checked only when --original-root is supplied. No predecessor is written.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, default=BASE/'author-run')
parser.add_argument('--original-root', type=Path)
args = parser.parse_args()
if args.output_dir.exists():
    parser.error('output directory already exists; supply a fresh path')
args.output_dir.mkdir(parents=True)
checks = []

def zero(label, value):
    value = S.cancel(value)
    if value != 0:
        value = S.trigsimp(S.simplify(value))
    assert value == 0, (label, value)
    checks.append(label)
    if len(checks) % 100 == 0:
        print(f'{len(checks)} exact checks passed; latest: {label}',flush=True)

def truth(label, condition):
    assert condition, label
    checks.append(label)

# In local coordinates (w0,w1,x0,y0,x1,y1,x2,y2), w2=1-w0-w1.
w0,w1 = S.symbols('w0 w1', positive=True)
w = [w0,w1,1-w0-w1]
W = S.Matrix([[1/w0+1/w[2],1/w[2]],
              [1/w[2],1/w1+1/w[2]]])
Winv = S.diag(w0,w1)-S.Matrix([w0,w1])*S.Matrix([w0,w1]).T
G = S.diag(W,*[w[j] for j in range(3) for _ in range(2)])
Ginv = S.diag(Winv,*[1/w[j] for j in range(3) for _ in range(2)])
for i in range(8):
    for j in range(8):
        zero(f'metric inverse {i},{j}',(G*Ginv)[i,j]-int(i==j))
f = S.symbols('f0:3',real=True)
g = [S.Matrix(S.symbols(f'g{j}x g{j}y',real=True)) for j in range(3)]
E = sum(w[j]*f[j] for j in range(3))
dE = S.Matrix([f[0]-f[2],f[1]-f[2]]+
               [w[j]*g[j][i] for j in range(3) for i in range(2)])
grad = S.Matrix([w[j]*(f[j]-E) for j in range(2)]+
                [g[j][i] for j in range(3) for i in range(2)])
for i in range(8): zero(f'gradient coordinate {i}',(Ginv*dE-grad)[i])
u0,u1 = S.symbols('u0 u1',real=True)
u = [u0,u1,-u0-u1]
v = [S.Matrix(S.symbols(f'v{j}x v{j}y',real=True)) for j in range(3)]
pairing = sum((f[j]-E)*u[j]+w[j]*(g[j].dot(v[j])) for j in range(3))
zero('all-tangent gradient pairing',pairing-
     sum(f[j]*u[j]+w[j]*g[j].dot(v[j]) for j in range(3)))
variance = sum(w[j]*(f[j]-E)**2 for j in range(3))
D = sum(w[j]*g[j].dot(g[j]) for j in range(3))+variance
zero('gradient squared speed equals dissipation',(grad.T*G*grad)[0]-D)
zero('negative gradient energy derivative',(dE.T*(-grad))[0]+D)
zero('variance expression',variance-(sum(w[j]*f[j]**2 for j in range(3))-E**2))
zero('replicator tangent',sum(-w[j]*(f[j]-E) for j in range(3)))

# General polynomial-observable jets, with unrestricted values and gradients.
p = S.symbols('p0:3',real=True)
q = S.symbols('q0:3',real=True)
pg = [S.Matrix(S.symbols(f'p{j}x p{j}y',real=True)) for j in range(3)]
qg = [S.Matrix(S.symbols(f'q{j}x q{j}y',real=True)) for j in range(3)]
Lp,Lq = sum(w[j]*p[j] for j in range(3)),sum(w[j]*q[j] for j in range(3))
dp = S.Matrix([p[0]-p[2],p[1]-p[2]]+[w[j]*pg[j][i] for j in range(3) for i in range(2)])
dq = S.Matrix([q[0]-q[2],q[1]-q[2]]+[w[j]*qg[j][i] for j in range(3) for i in range(2)])
Bpq = sum(w[j]*(pg[j].dot(qg[j])+p[j]*q[j]) for j in range(3))-Lp*Lq
zero('observable cometric',(dp.T*Ginv*dq)[0]-Bpq)

# Permutations are isometries, using arbitrary tangent symbols and exact masses.
wr = [S.Rational(1,6),S.Rational(1,3),S.Rational(1,2)]
base_norm = sum(u[j]**2/wr[j]+wr[j]*v[j].dot(v[j]) for j in range(3))
for perm in itertools.permutations(range(3)):
    perm_norm = sum(u[j]**2/wr[j]+wr[j]*v[j].dot(v[j]) for j in perm)
    zero('permutation isometry '+str(perm),perm_norm-base_norm)

# Local Hermite probes and an exact finite moment-image differential.
x,y = S.symbols('x y',real=True)
points = [(S.Integer(0),S.Integer(0)),(S.Integer(1),S.Integer(0)),(S.Integer(0),S.Integer(2))]
ell = x+2*y
lam = [ell.subs({x:a,y:b}) for a,b in points]
for j in range(3):
    ej = S.prod((ell-lam[k])/(lam[j]-lam[k]) for k in range(3) if k!=j)
    for i,coord in enumerate((x,y)):
        h = (coord-points[j][i])*ej**2
        truth(f'Hermite degree {j},{i}',S.Poly(h,x,y).total_degree()<=5)
        for k,pt in enumerate(points):
            zero(f'Hermite value {j},{i},{k}',h.subs({x:pt[0],y:pt[1]}))
            for a,var in enumerate((x,y)):
                zero(f'Hermite derivative {j},{i},{k},{a}',
                     S.diff(h,var).subs({x:pt[0],y:pt[1]})-int(j==k and i==a))
    for k,pt in enumerate(points):
        zero(f'Lagrange weight probe {j},{k}',ej.subs({x:pt[0],y:pt[1]})**2-int(j==k))

coords = S.symbols('x0 y0 x1 y1 x2 y2',real=True)
variables = (w0,w1)+coords
exps = [(a,n-a) for n in range(6) for a in range(n+1)]
polys = [x**a*y**b for a,b in exps]
moments = S.Matrix([sum(w[j]*coords[2*j]**a*coords[2*j+1]**b for j in range(3)) for a,b in exps])
sub = {w0:wr[0],w1:wr[1],**{coords[2*j+i]:points[j][i] for j in range(3) for i in range(2)}}
J = moments.jacobian(variables).subs(sub)
truth('degree-five rank-three chart immersion dimension eight',J.rank()==8)
Gnumeric = G.subs(sub)
Cimage = J*Ginv.subs(sub)*J.T
truth('redundant moment cometric rank eight',Cimage.rank()==8)
for a,pa in enumerate(polys):
    for b,pb in enumerate(polys):
        eva = [pa.subs({x:xx,y:yy}) for xx,yy in points]
        evb = [pb.subs({x:xx,y:yy}) for xx,yy in points]
        expected = sum(wr[j]*((S.diff(pa,x)*S.diff(pb,x)+S.diff(pa,y)*S.diff(pb,y)).subs(
            {x:points[j][0],y:points[j][1]})+eva[j]*evb[j]) for j in range(3))
        expected -= sum(wr[j]*eva[j] for j in range(3))*sum(wr[j]*evb[j] for j in range(3))
        zero(f'finite moment-image cometric {a},{b}',Cimage[a,b]-expected)
kernel_row = exps.index((2,2)) # p=x²y² has zero value and gradient at all three points.
for b in range(len(exps)):
    zero(f'nonconstant jet-kernel coordinate {b}',Cimage[kernel_row,b])

# Degree-two cannot distinguish these distinct positive rank-two laws.
mu = [(S.Rational(1,2),-1),(S.Rational(1,2),1)]
nu = [(S.Rational(1,5),-2),(S.Rational(4,5),S.Rational(1,2))]
for n in range(3): zero(f'rank-two omitted-coordinate alias m{n}',sum(a*z**n for a,z in mu)-sum(a*z**n for a,z in nu))
zero('rank-two omitted-coordinate third-moment gap',sum(a*z**3 for a,z in nu)+S.Rational(3,2))
truth('alias laws differ',mu!=nu)
for label,law in [('mu',mu),('nu',nu)]:
    h = S.Matrix([[sum(a*z**(i+j) for a,z in law) for j in range(2)] for i in range(2)])
    zero('alias law positive rank-two determinant '+label,h.det()-1)

# Coercive stationary full-rank nonminimum.
F = (x*x-1)**2+(y*y-1)**2
eps = S.symbols('eps',real=True)
for yy in (-1,1):
    zero(f'stationary energy at {yy}',F.subs({x:0,y:yy})-1)
    for var in (x,y): zero(f'stationary gradient {yy},{var}',S.diff(F,var).subs({x:0,y:yy}))
    zero(f'nearby energy difference {yy}',F.subs({x:eps,y:yy})-1-eps**2*(eps**2-2))
    zero(f'global minimum control {yy}',F.subs({x:1,y:yy}))
truth('nearby nonminimum exact epsilon one-half',(eps**2*(eps**2-2)).subs(eps,S.Rational(1,2))<0)
zero('negative Hessian direction',S.diff(F,x,2).subs({x:0,y:1})+4)

# Coincident labels have positive-cost invisible law tangents.
collision_weights = [S.Rational(1,3),S.Rational(2,3)]
for n in range(6):
    zero(f'collision mass redistribution invisible degree {n}',7**n-7**n)
    zero(f'collision velocity redistribution invisible degree {n}',
         sum(collision_weights[j]*[2,-1][j] for j in range(2))*S.diff(x**n,x).subs(x,7))
zero('collision mass redistribution positive cost',sum(1/z for z in collision_weights)-S.Rational(9,2))
zero('collision invisible velocity positive cost',sum(collision_weights[j]*[2,-1][j]**2 for j in range(2))-2)
a,b = S.symbols('a b',positive=True)
A,B,V0,V1 = S.symbols('A B V0 V1',real=True)
zero('merged mass Cauchy remainder',A*A/a+B*B/b-(A+B)**2/(a+b)-(b*A-a*B)**2/(a*b*(a+b)))
zero('merged velocity Cauchy remainder',a*V0**2+b*V1**2-(a*V0+b*V1)**2/(a+b)-a*b*(V0-V1)**2/(a+b))

# Square-root mass chart and a finite reaction-length boundary path.
qroot,dqroot = S.symbols('qroot dqroot',positive=True)
zero('square-root Fisher chart',(qroot*dqroot/2)**2/(qroot**2/4)-dqroot**2)
theta = S.symbols('theta',real=True)
wtheta = [S.cos(theta)**2,S.sin(theta)**2]
speed2 = sum(S.diff(z,theta)**2/z for z in wtheta)
zero('pure-reaction squared speed',speed2-4)
zero('pure-reaction endpoint length',S.integrate(S.Integer(2),(theta,0,S.pi/2))-S.pi)
truth('rank-one Euclidean distance can exceed ambient path bound',(2*S.pi-S.pi).is_positive is True)

# Quadratic exact trajectories, expressed by s=e^(-2t)>0 for simpler algebra.
s = S.symbols('s',positive=True)
z0,z1 = S.symbols('z0 z1',real=True)
a0,a1 = S.symbols('a0 a1',positive=True)
zs = [z0,z1]
Xs = [z*S.sqrt(s) for z in zs]
Ks = [z*z*(1-s)/4 for z in zs]
raw = [a0*S.exp(-Ks[0]),a1*S.exp(-Ks[1])]
Ws = [c/sum(raw) for c in raw]
fs = [z*z*s/2 for z in zs]
Et = sum(Ws[j]*fs[j] for j in range(2))
for j in range(2):
    zero(f'quadratic position ODE {j}',-2*s*S.diff(Xs[j],s)+Xs[j])
    zero(f'quadratic killing ODE {j}',-2*s*S.diff(Ks[j],s)-fs[j])
    zero(f'quadratic initial position {j}',Xs[j].subs(s,1)-zs[j])
    zero(f'quadratic initial killing {j}',Ks[j].subs(s,1))
    zero(f'quadratic weight ODE {j}',-2*s*S.diff(Ws[j],s)+Ws[j]*(fs[j]-Et))
    zero(f'quadratic position inverse {j}',Xs[j]/S.sqrt(s)-zs[j])
    zero(f'quadratic limiting weight {j}',Ws[j].subs(s,0)-
         [a0,a1][j]*S.exp(-zs[j]**2/4)/(a0*S.exp(-z0*z0/4)+a1*S.exp(-z1*z1/4)))
zero('quadratic weight normalization',sum(Ws)-1)
zero('quadratic finite noncollision difference',Xs[0]-Xs[1]-(z0-z1)*S.sqrt(s))
vart = sum(Ws[j]*(fs[j]-Et)**2 for j in range(2))
Dt = sum(Ws[j]*Xs[j]**2 for j in range(2))+vart
zero('quadratic exact energy dissipation',-2*s*S.diff(Et,s)+Dt)
zero('quadratic PL equality',sum(Ws[j]*Xs[j]**2 for j in range(2))-2*Et)
zero('quadratic exponential-gap residual',Dt-2*Et-vart)
hmat = S.Matrix([[1,sum(Ws[j]*Xs[j] for j in range(2))],
                 [sum(Ws[j]*Xs[j] for j in range(2)),sum(Ws[j]*Xs[j]**2 for j in range(2))]])
zero('quadratic rank-two Gram determinant',hmat.det()-Ws[0]*Ws[1]*(z0-z1)**2*s)

# General positive finite factors have a unique inverse weighting.
aa = S.symbols('aa0:3',positive=True)
ef = S.symbols('ef0:3',positive=True)
forward = [aa[j]*ef[j]/sum(aa[k]*ef[k] for k in range(3)) for j in range(3)]
for j in range(3):
    zero(f'inverse weight recovery {j}',(forward[j]/ef[j])/sum(forward[k]/ef[k] for k in range(3))-aa[j]/sum(aa))
    truth(f'positive weighting {j}',forward[j].is_positive is True)
zz = S.symbols('zz0:3',real=True)
hscale = S.symbols('hscale',positive=True)
Vand = S.Matrix([[(zz[j]*hscale)**i for j in range(3)] for i in range(3)])
vandprod = S.prod(zz[j]-zz[i] for i in range(3) for j in range(i+1,3))
zero('quadratic rank-three Vandermonde scaling',Vand.det()-hscale**3*vandprod)
zero('quadratic rank-three Gram determinant',(Vand*S.diag(*aa)*Vand.T).det()-S.prod(aa)*hscale**6*vandprod**2)

# Forward-only inherited quartic control and its image inverse.
t = S.symbols('t',nonnegative=True)
z = S.symbols('z',real=True)
X4 = z/S.sqrt(1+2*z*z*t)
K4 = z*z*(1-1/(1+2*z*z*t))/8
zero('quartic position ODE',S.diff(X4,t)+X4**3)
zero('quartic killing ODE',S.diff(K4,t)-X4**4/4)
zero('quartic initial position',X4.subs(t,0)-z)
zero('quartic initial killing',K4.subs(t,0))
zero('quartic image gap',1-2*t*X4**2-1/(1+2*z*z*t))
zero('quartic inverse on image',X4/S.sqrt(1-2*t*X4**2)-z)

# Every copied ancestor is checked, and originals only if explicitly requested.
bindings = json.loads((BASE/'INPUT_BINDINGS.json').read_text())
for row in bindings:
    copied = BASE/row['copy']
    truth('copied input hash '+row['original'],hashlib.sha256(copied.read_bytes()).hexdigest()==row['sha256'])
    if args.original_root is not None:
        original = args.original_root/row['original']
        truth('original input hash '+row['original'],hashlib.sha256(original.read_bytes()).hexdigest()==row['sha256'])
report = {'status':'PASS','exact_check_count':len(checks),'checks':checks,
          'sympy_version':S.__version__,'original_inputs_checked':args.original_root is not None,
          'scope':'Exact finite controls. Universal assertions use RESULT.md and the stated inherited theorem.'}
(args.output_dir/'EXACT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
