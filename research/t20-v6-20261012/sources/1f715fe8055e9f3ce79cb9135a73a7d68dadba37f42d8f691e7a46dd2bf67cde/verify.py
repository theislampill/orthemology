#!/usr/bin/env python3
"""Exact author controls; these do not prove the all-L2 or arbitrary-degree claims."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from functools import lru_cache
import sympy as s

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', required=True)
parser.add_argument('--original-root')
args = parser.parse_args()
out = Path(args.output_dir).resolve()
out.mkdir(parents=True, exist_ok=True)
checks = []

def check(name, condition):
    if condition is not True and condition != s.true:
        raise AssertionError(f'{name}: {condition!r}')
    checks.append(name)

def zero(name, expression):
    if isinstance(expression, s.MatrixBase):
        check(name, all(s.simplify(e) == 0 for e in expression))
    else:
        check(name, s.simplify(s.expand(expression)) == 0)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

bindings = json.loads((ROOT/'INPUT_BINDINGS.json').read_text())
for row in bindings['inputs']:
    p = ROOT/row['snapshot']
    check('snapshot '+row['snapshot'], p.is_file() and sha(p) == row['sha256'])
    check('snapshot bytes '+row['snapshot'], p.stat().st_size == row['bytes'])
    if args.original_root:
        p = Path(args.original_root)/row['original']
        check('original '+row['original'], p.is_file() and sha(p) == row['sha256'])

manifest = ROOT/'MANIFEST.json'
if manifest.exists():
    for row in json.loads(manifest.read_text())['files']:
        p=ROOT/row['path']
        check('manifest '+row['path'], p.is_file() and sha(p)==row['sha256'])

x,m,M,V,a,b = s.symbols('x m M V a b', real=True)
v=s.symbols('v', positive=True)

def E(poly):
    p=s.Poly(s.expand(poly),x)
    ans=0
    for (n,),c in p.terms():
        if n%2==0:
            ans += c * (s.factorial2(n-1) if n else 1) * v**(n//2)
    return s.expand(ans)

def B(p,q):
    return E(s.diff(p,x)*s.diff(q,x))+E(p*q)-E(p)*E(q)

f=a*x+b*(x*x-v)
u=s.diff(f,x)
score=-s.diff(u,x)+x*u/v+f
target=M*x/v+V*(x*x-v)/(2*v*v)
subs={a:M/(1+v),b:V/(2*v*(v+2))}
zero('centred potential',E(f))
zero('full density tangent',score.subs(subs)-target)
norm=a*a*(1+v)+2*b*b*v*(v+2)
zero('potential action',E(u*u+f*f)-norm)
zero('metric from action',norm.subs(subs)-M*M/(1+v)-V*V/(2*v*(v+2)))
zero('cometric mean',B(x,x)-(1+v))
zero('cometric covariance',B(x*x-v,x*x-v)-2*v*(v+2))
zero('cometric cross',B(x,x*x-v))
zero('duality tangent pairing',E(f*target)-a*M-b*V)

# Finite null-field controls supplement the general cutoff/orthogonality proof.
for n in range(9):
    w=x**n
    eta=s.diff(w,x)-x*w/v
    zero(f'null divergence degree {n}',-s.diff(w,x)+x*w/v+eta)
    zero(f'centred null reaction degree {n}',E(eta))
    zero(f'orthogonality degree {n}',E(u*w+f*eta))
    zero(f'Pythagoras degree {n}',E((u+w)**2+(f+eta)**2)-norm-E(w*w+eta*eta))

uT=M+V*x/(2*v)
zero('pure transport full score',-s.diff(uT,x)+x*uT/v-target)
zero('pure transport metric',E(uT*uT)-M*M-V*V/(4*v))
zero('pure reaction metric',E(target*target)-M*M/v-V*V/(2*v*v))
zero('cometrics add mean',1+v-(1+v))
zero('cometrics add covariance',4*v+2*v*v-2*v*(v+2))
zero('channel mean split',a+a*v-a*(1+v))
zero('channel variance split',4*b*v+2*b*v*v-2*b*v*(v+2))
check('v1 shared mean cost', (M*M/(1+v)).subs({M:1,v:1})==s.Rational(1,2))
check('v1 naive sum wrong', (M*M+M*M/v).subs({M:1,v:1})==2)

k,beta,gamma=s.symbols('k beta gamma', real=True)
F=k*(x+m)**2/2+beta*(x+m)+gamma
energy=k*(m*m+v)/2+beta*m+gamma
mdot=-(1+v)*(k*m+beta)
vdot=-k*v*(v+2)
Fscore=s.diff(F,x,2)-x*s.diff(F,x)/v-F+E(F)
zero('quadratic full score',Fscore-mdot*x/v-vdot*(x*x-v)/(2*v*v))
zero('quadratic expected energy',E(F)-energy)
zero('quadratic dissipation',E(s.diff(F,x)**2)+E(F*F)-E(F)**2-(1+v)*(k*m+beta)**2-k*k*v*(v+2)/2)
zero('gradient energy derivative',s.diff(energy,m)*mdot+s.diff(energy,v)*vdot+E(s.diff(F,x)**2)+E(F*F)-E(F)**2)
for n in range(1,13):
    poly=(x+m)**n+3*(x+m)**(n-1)
    full=s.Poly(s.diff(poly,x,2)-x*s.diff(poly,x)/v-poly+E(poly),x)
    zero(f'leading degree coefficient {n}',full.coeff_monomial(x**n)+(1+s.Integer(n)/v))

F4=x**4/4
score4=s.diff(F4,x,2)-x*s.diff(F4,x)/v-F4+E(F4)
v4=-3*v*v*(v+2)
score4G=v4*(x*x-v)/(2*v*v)
residual=-(1/v+s.Rational(1,4))*(x**4-6*v*x*x+3*v*v)
zero('quartic invisible full residual',score4-score4G-residual)
for n in range(3): zero(f'quartic residual moment {n}',E(x**n*residual))
zero('quartic instantaneous variance',E(x*x*score4)-v4)

# Use z=e^{-k t}, so d/dt=-k z d/dz. This is exact for every real k.
z,v0,delta,C=s.symbols('z v0 delta C', positive=True)
D=1+v0*(1-z*z)/2
vt=v0*z*z/D
dt=delta*z/D
ddt=lambda e: -k*z*s.diff(e,z)
zero('quadratic variance solution',ddt(vt)+k*vt*(vt+2))
zero('quadratic mean solution',ddt(dt)+k*(1+vt)*dt)
zero('variance initial condition',vt.subs(z,1)-v0)
zero('mean initial condition',dt.subs(z,1)-delta)
q=(1-z*z)/4
zero('square completion precision',1/v0+2*q-D/v0)
zero('square completion shifted mean',delta/v0/(1/v0+2*q)-delta/D)
logZnoC=-s.log(D)/2-q*delta*delta/D
zero('normalizer log derivative',ddt(logZnoC)+k*(dt*dt+vt)/2)
zero('concave endpoint D',D.subs(z*s.Integer(1),s.sqrt(1+2/v0)))
zero('affine mean solution',s.diff(m-beta*(1+v)*x,x)+beta*(1+v))

r=s.symbols('r',positive=True)
vr=s.cosh(s.sqrt(2)*r)-1
A=s.sqrt(s.sech(s.sqrt(2)*r))
zero('radial change',s.diff(vr,r)**2/(2*vr*(vr+2))-1)
zero('warping function',1/(1+vr)-A*A)
curvature=s.simplify(-s.diff(A,r,2)/A)
check('curvature warping',s.trigsimp(curvature-(3*s.sech(s.sqrt(2)*r)**2-1)/2)==0)
zero('curvature zero variance',(3/(2*(v+1)**2)-s.Rational(1,2)).subs(v,s.sqrt(3)-1))
zero('fixed-coordinate Hessian failure',s.diff(1/(v+1),v)+1/(v+1)**2)
check('fixed-coordinate Hessian nonzero',s.diff(1/(v+1),v)!=0)

# Multivariate checks use exact rational, noncommuting 2x2 SPD matrices.
S=s.Matrix([[2,s.Rational(1,2)],[s.Rational(1,2),1]])
Sinv=S.inv()
I=s.eye(2)
y1,y2=s.symbols('y1 y2',real=True)
y=s.Matrix([y1,y2])
aa=s.Matrix([s.Rational(2,3),-s.Rational(1,4)])
AA=s.Matrix([[s.Rational(3,5),s.Rational(2,7)],[s.Rational(2,7),-s.Rational(1,3)]])
L=lambda X:2*(X*S+S*X+S*X*S)
BB=L(AA)
hh=(I+S)*aa
fm=(aa.T*y)[0]+(y.T*AA*y)[0]-s.trace(AA*S)
um=aa+2*AA*y

@lru_cache(None)
def wick(indices):
    if not indices: return s.Integer(1)
    if len(indices)%2: return s.Integer(0)
    i,tail=indices[0],indices[1:]
    return sum(S[i,j]*wick(tail[:n]+tail[n+1:]) for n,j in enumerate(tail))

def E2(poly):
    return s.expand(sum(c*wick((0,)*p+(1,)*q)
                        for (p,q),c in s.Poly(s.expand(poly),y1,y2).terms()))

scorem=-sum(s.diff(um[i],y[i]) for i in range(2))+(y.T*Sinv*um)[0]+fm
targetm=(hh.T*Sinv*y)[0]+((y.T*Sinv*BB*Sinv*y)[0]-s.trace(Sinv*BB))/2
zero('multivariate full tangent',scorem-targetm)
zero('multivariate potential centred',E2(fm))
zero('multivariate Wick action',E2((um.T*um)[0]+fm*fm)-(aa.T*(I+S)*aa)[0]-s.trace(AA*L(AA)))
for n in range(5):
    wm=s.Matrix([y1**n,y2**n])
    etam=sum(s.diff(wm[i],y[i]) for i in range(2))-(y.T*Sinv*wm)[0]
    zero(f'multivariate null reaction mean {n}',E2(etam))
    zero(f'multivariate full orthogonality {n}',E2((um.T*wm)[0]+fm*etam))
    zero(f'multivariate Pythagoras {n}',E2(((um+wm).T*(um+wm))[0]+(fm+etam)**2-(um.T*um)[0]-fm**2-(wm.T*wm)[0]-etam**2))
zero('multivariate scalar action identity',4*s.trace(AA*AA*S)+2*s.trace(AA*S*AA*S)-s.trace(AA*L(AA)))
CC=s.Matrix([[1,3],[3,-2]])
zero('multivariate self adjoint',s.trace(AA*L(CC))-s.trace(L(AA)*CC))
check('SPD covariance example',S[0,0]>0 and S.det()>0)
check('SPD nonzero operator energy',s.trace(AA*L(AA))>0)
zero('matrix channel addition',2*(AA*S+S*AA)+2*S*AA*S-L(AA))

l1,l2=s.symbols('l1 l2',positive=True)
t11,t12,t22=s.symbols('t11 t12 t22',real=True)
Sd=s.diag(l1,l2)
Ad=s.Matrix([[t11,t12],[t12,t22]])
Ld=2*(Ad*Sd+Sd*Ad+Sd*Ad*Sd)
for i,li in enumerate([l1,l2]):
    for j,lj in enumerate([l1,l2]):
        zero(f'eigenbasis multiplier {i}{j}',Ld[i,j]-2*(li+lj+li*lj)*Ad[i,j])
Bd=s.Matrix([[t11,t12],[t12,t22]])
LiBd=s.Matrix(2,2,lambda i,j:Bd[i,j]/(2*([l1,l2][i]+[l1,l2][j]+[l1,l2][i]*[l1,l2][j])))
expanded=t11*t11/(2*l1*(l1+2))+t22*t22/(2*l2*(l2+2))+t12*t12/(l1+l2+l1*l2)
zero('symmetric off diagonal factor',s.trace(Bd*LiBd)-expanded)

Q=s.Matrix([[1,s.Rational(1,3)],[s.Rational(1,3),2]])
mu=s.Matrix([s.Rational(1,2),-s.Rational(2,3)])
linear=s.Matrix([s.Rational(1,7),s.Rational(2,5)])
Fm=((y+mu).T*Q*(y+mu))[0]/2+(linear.T*(y+mu))[0]
EFm=(mu.T*Q*mu)[0]/2+s.trace(Q*S)/2+(linear.T*mu)[0]
gradFm=s.Matrix([s.diff(Fm,t) for t in y])
scoreFm=sum(s.diff(Fm,t,2) for t in y)-(y.T*Sinv*gradFm)[0]-Fm+EFm
mprime=-(I+S)*(Q*mu+linear)
Sprime=-(Q*S+S*Q+S*Q*S)
targetFm=(mprime.T*Sinv*y)[0]+((y.T*Sinv*Sprime*Sinv*y)[0]-s.trace(Sinv*Sprime))/2
zero('noncommuting matrix quadratic full flow',scoreFm-targetFm)
check('noncommutation is real',Q*S-S*Q!=s.zeros(2))
zero('matrix precision ODE',-Sinv*Sprime*Sinv-(Sinv*Q+Q*Sinv+Q))
zero('matrix duality covariance',s.trace((Q/2)*L(AA))-s.trace(L(Q/2)*AA))

# Independent-entry check of precision formula in eigenbasis, including Q=0.
time=s.symbols('t',real=True)
q1,q2=s.symbols('q1 q2',real=True)
p11,p12,p22=s.symbols('p11 p12 p22',real=True)
P0=s.Matrix([[p11,p12],[p12,p22]])
Qd=s.diag(q1,q2)
expQ=s.diag(s.exp(q1*time),s.exp(q2*time))
Pt=expQ*P0*expQ+(expQ*expQ-I)/2
zero('precision solution entrywise',Pt.diff(time)-Pt*Qd-Qd*Pt-Qd)
zero('precision initial matrix',Pt.subs(time,0)-P0)
zero('zero Q precision',Pt.subs({q1:0,q2:0})-P0)

result={'status':'PASS','kind':'author exact finite controls; not universal proof or independent review','assertions':len(checks),'groups':checks,'python':sys.version.split()[0],'sympy':s.__version__,'result_sha256':sha(ROOT/'RESULT.md'),'input_bindings_sha256':sha(ROOT/'INPUT_BINDINGS.json')}
(out/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','assertions','python','sympy','result_sha256']},indent=2))
