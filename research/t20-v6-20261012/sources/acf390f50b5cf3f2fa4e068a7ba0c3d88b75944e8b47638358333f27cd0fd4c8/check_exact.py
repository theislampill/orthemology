#!/usr/bin/env python3
"""Exact finite controls for complete-flow repair, not a formal universal proof."""
import hashlib
import json
from pathlib import Path
import sympy as S

BASE = Path(__file__).resolve().parent
checks = []
def zero(label, value):
    value = S.trigsimp(S.simplify(S.expand(value)))
    assert value == 0, (label, value)
    checks.append(label)
def truth(label, value):
    assert value, label
    checks.append(label)

x, y, t = S.symbols('x y t', real=True)
r2 = x*x+y*y
bx, by = -r2*y, r2*x
zero('conserved coercive radius', 2*x*bx+2*y*by)
zero('rotation divergence', S.diff(bx,x)+S.diff(by,y))
# Hermite controls at arbitrary distinct, explicit multidimensional atoms.
pts = [(S.Integer(0),S.Integer(0)), (S.Integer(1),S.Integer(0)), (S.Integer(0),S.Integer(2))]
ell = x+2*y
lam = [ell.subs({x:a,y:b}) for a,b in pts]
for j, (a,b) in enumerate(pts):
    e = S.prod((ell-lam[l])/(lam[j]-lam[l]) for l in range(3) if l!=j)
    for i, coordinate in enumerate((x,y)):
        test = (coordinate-pts[j][i])*e**2
        for l,(c,d) in enumerate(pts):
            sub={x:c,y:d}
            zero(f'Hermite value {j},{i},{l}', test.subs(sub))
            for q, variable in enumerate((x,y)):
                zero(f'Hermite gradient {j},{i},{l},{q}',S.diff(test,variable).subs(sub)-int(j==l and i==q))
# Genuine cubic complete transport with a signed time-dependent k.
traj = [(S.Integer(0),S.Integer(0)),(S.cos(t),S.sin(t)),(-2*S.sin(4*t),2*S.cos(4*t))]
K = [S.Integer(0), t*t/2+S.sin(t),2*t*t+(S.cos(4*t)-1)/2]
radii=[0,1,4]
k=t*r2+x
for j, (a,b) in enumerate(traj):
    sub={x:a,y:b}
    zero(f'trajectory x {j}',S.diff(a,t)-bx.subs(sub))
    zero(f'trajectory y {j}',S.diff(b,t)-by.subs(sub))
    zero(f'radius {j}',a*a+b*b-radii[j])
    zero(f'integrated killing derivative {j}',S.diff(K[j],t)-k.subs(sub))
    zero(f'integrated killing zero {j}',K[j].subs(t,0))
# The raw atom mass is a_j exp(-K_j); divide the identity by this positive mass.
# Checking the polynomial product rule this way avoids fragile giant exponential simplification.
for j,(a,b) in enumerate(traj):
    sub={x:a,y:b}
    for degree in range(5):
        for n in range(degree+1):
            p=x**n*y**(degree-n)
            pv=p.subs(sub)
            generator=(bx*S.diff(p,x)+by*S.diff(p,y)-k*p).subs(sub)
            zero(f'raw generator atom {j}, monomial {n},{degree-n}',S.diff(pv,t)-S.diff(K[j],t)*pv-generator)
# Universal quotient algebra: A'=D-B, Z'=-C, L=A/Z, D/Z=L(b.grad p), etc.
A,D,B,Z,C=S.symbols('A D B Z C', real=True, nonzero=True)
zero('normalized hierarchy quotient',(D-B)/Z+A*C/Z**2-(D/Z-B/Z+(C/Z)*(A/Z)))
# General conserved-radius rotation matrix inverse and norm identity.
q,ang = S.symbols('q ang',real=True)
Rot=S.Matrix([[S.cos(ang),-S.sin(ang)],[S.sin(ang),S.cos(ang)]])
for i in range(2):
    for j in range(2): zero(f'rotation inverse {i},{j}',(Rot.T*Rot-S.eye(2))[i,j])
# Explicit nonautonomous affine flow b_t(x)=x+t; k_t(x)=x+t+1.
a=S.symbols('a',real=True)
X=S.exp(t)*(a+1)-t-1
Ka=(a+1)*(S.exp(t)-1)
zero('affine initial',X.subs(t,0)-a)
zero('affine velocity',S.diff(X,t)-(X+t))
zero('affine killing integral',S.diff(Ka,t)-(X+t+1))
zero('affine inverse',S.exp(-t)*(X+t+1)-1-a)
for n in range(7):
    zero(f'affine raw generator {n}',S.diff(X**n,t)-S.diff(Ka,t)*X**n-((x+t)*S.diff(x**n,x)-(x+t+1)*x**n).subs(x,X))
# Positive weighting and inverse normalization, for generic positive factors.
w=S.symbols('w0:3',positive=True)
e=S.symbols('e0:3',positive=True)
normalizer=sum(w[i]*e[i] for i in range(3))
v=[w[i]*e[i]/normalizer for i in range(3)]
backnormalizer=sum(v[i]/e[i] for i in range(3))
for i in range(3):
    truth(f'positive finite weight {i}',v[i].is_positive is True)
    zero(f'inverse weight {i}',(v[i]/e[i])/backnormalizer-w[i]/sum(w))
zero('forward normalization',sum(v)-1)
# Three-atom full-rank witness from conserved radius: projections 0,1,4.
V=S.Matrix([[S.Integer(r)**m for r in radii] for m in range(3)])
zero('radial Vandermonde determinant',V.det()-12)
zero('positive rank-three Gram determinant',(V*S.diag(*w)*V.T).det()-144*S.prod(w))
# Exploding characteristic and divergence reaction bookkeeping.
Xe=1/(1-t)
zero('exploding x squared characteristic',S.diff(Xe,t)-Xe**2)
zero('source h plus divergence equals minus k',(-x**4-2*x)+S.diff(x*x,x)+x**4)
zero('reverse inflow x squared characteristic',S.diff(1/t,t)+(1/t)**2)
# Forward-only coercive quartic gradient criterion, with inverse on image only.
h=S.symbols('h',nonnegative=True)
Xg=a/S.sqrt(1+2*a*a*h)
Kg=a*a/S.Integer(8)*(1-1/(1+2*a*a*h))
zero('quartic gradient forward velocity',S.diff(Xg,h)+Xg**3)
zero('quartic integrated killing',S.diff(Kg,h)-Xg**4/4)
zero('quartic initial',Xg.subs(h,0)-a)
zero('quartic killing initial',Kg.subs(h,0))
zero('quartic forward strict derivative',S.diff(Xg,a)-(1+2*a*a*h)**S.Rational(-3,2))
zero('quartic image gap identity',1-2*h*Xg**2-1/(1+2*a*a*h))
zero('quartic inverse on image',Xg/S.sqrt(1-2*h*Xg**2)-a)
zero('gradient energy dissipation',S.diff(x**4/4,x)*(-x**3)+x**6)
# Lower-bound endpoint inequality is analytic; algebra checks its scalar exponent form.
C0,dt,c0=S.symbols('C0 dt c0',positive=True)
truth('backward lower mass bound stays positive',(c0*S.exp(-C0*dt)).is_positive is True)
# Check all retained input hashes; do not modify predecessors.
bindings=json.loads((BASE/'INPUT_BINDINGS.json').read_text())
for name,digest in bindings.items():
    truth('input unchanged '+name,hashlib.sha256((BASE.parent/name).read_bytes()).hexdigest()==digest)
report={'status':'PASS','exact_check_count':len(checks),'checks':checks,'sympy_version':S.__version__,'scope':'Finite exact controls; general theorem rests on RESULT.md proof.','input_preservation':'All bound predecessor hashes unchanged.'}
(BASE/'EXACT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
