#!/usr/bin/env python3
"""Exact controls for the ordinary proofs in RESULT.md; no formal-kernel claim."""
from pathlib import Path
import argparse, hashlib, json, platform, sys
import sympy as S

ap=argparse.ArgumentParser()
ap.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'author-run')
ap.add_argument('--original-root',type=Path)
args=ap.parse_args()
ROOT=Path(__file__).resolve().parent
args.output_dir.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,expr):
    if isinstance(expr,S.MatrixBase):
        ok=all(S.simplify(x)==0 for x in expr)
    elif isinstance(expr,bool): ok=expr
    else: ok=S.simplify(expr)==0
    checks.append({'name':name,'pass':bool(ok)})
    if not ok: raise AssertionError((name,expr))

b=S.symbols('b',real=True)
s=S.symbols('s',positive=True)
y,z=S.symbols('y z',real=True)
x=S.Matrix([y,z]); E11=S.diag(1,0)
Sig=S.Matrix([[1,b],[b,s+b*b]])
P=Sig.inv(); A=S.eye(2)-P
B=A-b*b*S.Rational(1,3)*E11
V=-(B*Sig+Sig*B)-Sig*B*Sig
V=S.simplify(V)
bd=-b*(s+2+b*b/3)
sd=(1-s)*(s+2)+2*b*b
check('fixed marginal covariance derivative',V[0,0])
check('constrained covariance b equation',V[0,1]-bd)
check('constrained conditional variance equation',V[1,1]-2*b*bd-sd)
check('covariance determinant equals conditional variance',Sig.det()-s)
# Full density tangent of Gaussian, not only covariance matching.
gdensity=(-S.trace(P*V)+(x.T*P*V*P*x)[0])/2
fielddensity=S.trace(B)-(x.T*P*B*x)[0]-(x.T*B*x)[0]/2+S.trace(B*Sig)/2
check('full Gaussian density derivative identity',gdensity-fielddensity)
phi=b*b*(y*y-1)/6
OU=lambda f: -S.diff(f,y,2)+y*S.diff(f,y)
check('Gaussian weak resolvent exact polynomial',OU(phi)+phi-b*b*(y*y-1)/2)
# Gaussian expectation of polynomial using independent standard y and e.
e=S.symbols('e',real=True)
def normal_moment(n): return 0 if n%2 else S.factorial2(n-1) if n else S.Integer(1)
def expect(poly):
    out=0
    for powers,coef in S.Poly(S.expand(poly),y,e).terms():
        out+=coef*normal_moment(powers[0])*normal_moment(powers[1])
    return S.simplify(out)
q=(x.T*A*x)[0]/2  # constant omitted
qye=S.expand(q.subs(z,b*y+S.sqrt(s)*e))
h=expect(qye)-b*b/2+b*b*y*y/2 # unused normalization gauge but correct y quadratic part
# Explicit conditional centering in (y,e).
condmean=0
for (yp,ep),coef in S.Poly(qye,y,e).terms(): condmean+=coef*y**yp*normal_moment(ep)
check('conditional hidden KL centered part',condmean-expect(qye)-b*b*(y*y-1)/2)
check('zero conditional y score',S.expand(S.diff(q,y).subs(z,b*y+S.sqrt(s)*e)).coeff(e,0))
Du=S.trace(A*Sig*A)+S.trace((A*Sig)**2)/2
Dc=S.trace(B*Sig*B)+S.trace((B*Sig)**2)/2
Df=b*b+(s-1)**2/s+b*b*s+(s-1)**2/2
horizontal=b**4/6
check('horizontal compensation action',expect(S.diff(phi,y)**2+phi**2)-horizontal)
# Bilinear gradient potential covariance identity.
Bp=b*b*S.Rational(1,3)*E11
cross=S.trace(A*Sig*Bp)+S.trace(A*Sig*Bp*Sig)/2
check('full-horizontal orthogonality pairing',cross-horizontal)
check('full minus constrained action',Du-Dc-horizontal)
check('constrained minus fibrewise action',Dc-Df-b*b/s-b**4/3)
check('fibrewise field action from direct expectation',expect(S.diff(q,z).subs(z,b*y+S.sqrt(s)*e)**2+(qye-condmean)**2)-Df)
energy=(b*b+s-1-S.log(s))/2
check('full constrained KL chain rule',S.diff(energy,b)*bd+S.diff(energy,s)*sd+Dc)
fbd=-(1+s)*b
fsd=(1-s)*(s+2)
check('fibrewise KL chain rule',S.diff(energy,b)*fbd+S.diff(energy,s)*fsd+Df)
R=(s-1)**2*(1/s+S.Rational(1,2))-3*(s-1-S.log(s))
check('sharp entropy remainder derivative',S.diff(R,s)-(s-1)**3/s**2)
check('sharp entropy remainder zero',R.subs(s,1))
check('sharp entropy dissipation decomposition',Dc-6*energy-R-b*b*(s-1)**2/s-b**4/3)
# Initial c family.
c=S.symbols('c',real=True); r=c*c
subs={b:c,s:1-r}
check('initial full dissipation',Du.subs(subs)-(2*r/(1-r)+r))
check('initial constrained dissipation',Dc.subs(subs)-(2*r/(1-r)+r-r*r/6))
check('initial fibrewise dissipation',Df.subs(subs)-(r/(1-r)+r-r*r/2))
Vun=2*S.eye(2)-Sig-Sig*Sig
check('unconstrained marginal failure',Vun[0,0]+b*b)
check('initial constrained covariance rate',bd.subs(subs)+c*(3-2*r/3))
# Exact c=1/2 witness: fibrewise representation versus ambient minimum.
Sc=Sig.subs({b:S.Rational(1,2),s:S.Rational(3,4)})
Bf=S.Matrix([[-S.Rational(235,924),S.Rational(17,42)],[S.Rational(17,42),-S.Rational(43,231)]])
Vf=S.Matrix([[0,-S.Rational(7,8)],[-S.Rational(7,8),-S.Rational(3,16)]])
check('ambient minimum fields realize fibrewise Gaussian tangent',-(Bf*Sc+Sc*Bf)-Sc*Bf*Sc-Vf)
fmin=S.trace(Bf*Sc*Bf)+S.trace((Bf*Sc)**2)/2
check('fibrewise tangent ambient minimum cost',fmin-S.Rational(2489,7392))
check('fibrewise representation strict excess',S.Rational(53,96)-fmin-S.Rational(199,924))
check('c one-half full rate',Du.subs({b:S.Rational(1,2),s:S.Rational(3,4)})-S.Rational(11,12))
check('c one-half constrained rate',Dc.subs({b:S.Rational(1,2),s:S.Rational(3,4)})-S.Rational(29,32))
check('c one-half fibre rate',Df.subs({b:S.Rational(1,2),s:S.Rational(3,4)})-S.Rational(53,96))
# Closed-form fibrewise ODE; q=e^-3t represented symbolically.
t=S.symbols('t',real=True)
qt=S.exp(-3*t)
sf=(3-r-2*r*qt)/(3-r+r*qt)
bf=3*c*S.exp(-2*t)/(3-r+r*qt)
check('closed fibrewise variance initial',sf.subs(t,0)-(1-r))
check('closed fibrewise mean initial',bf.subs(t,0)-c)
check('closed fibrewise variance ODE',S.diff(sf,t)-(1-sf)*(sf+2))
check('closed fibrewise mean ODE',S.diff(bf,t)+(1+sf)*bf)
# Barrier algebra and rescaled-variable identities used in the ordinary proof.
u=S.symbols('u',nonnegative=True)
M=(-1+S.sqrt(9+8*u))/2
check('Gaussian upper-barrier root',(1-M)*(M+2)+2*u)
w=S.symbols('w',real=True)
check('Gaussian linear-plus-forcing w identity',sd.subs(s,w+1)-(-3*w-w*w+2*b*b))
check('Gaussian b logarithmic correction',bd/b+3+(s-1)+b*b/3)
# Checked bound identity: (s-1)-log s <= (s-1)^2/s is log s >=1-1/s.
check('Gaussian elementary entropy bound identity',(s-1)**2/s-(s-1-S.log(s))-(S.log(s)-1+1/s))
# Inherited bindings protect input identity without editing the originals.
for row in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    check('snapshot binding: '+row['snapshot'],hashlib.sha256((ROOT/row['snapshot']).read_bytes()).hexdigest()==row['sha256'])
    if args.original_root:
        check('original binding: '+row['original'],hashlib.sha256((args.original_root/row['original']).read_bytes()).hexdigest()==row['sha256'])
out={'status':'PASS','verification_kind':'Exact SymPy author controls plus input bindings; ordinary proofs are in RESULT.md','python':platform.python_version(),'sympy':S.__version__,'check_count':len(checks),'checks':checks}
(args.output_dir/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','check_count','python','sympy')},indent=2))
