#!/usr/bin/env python3
"""Reproducible algebraic and numerical controls, not an all-dimension proof."""
import argparse, hashlib, json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=ROOT/'VERIFICATION.json')
parser.add_argument('--require-source-custody',action='store_true',help='Fail if the raw primary PDF is unavailable; omitted from portable package by design.')
args=parser.parse_args()
checks=[]
def zero(name, expr):
    vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    ok=all(s.simplify(v)==0 for v in vals)
    checks.append({'name':name,'passed':bool(ok)})
    if not ok: raise AssertionError(name)
def truth(name, b):
    checks.append({'name':name,'passed':bool(b)})
    if not b: raise AssertionError(name)

v,al,be,ep,k,m,n,x=s.symbols('v alpha beta epsilon k m n x',positive=True)
scalar_cometric=4*al*v+2*be*v*v
zero('unit variance metric matches accepted',1/scalar_cometric.subs({al:1,be:1})-1/(2*v*(v+2)))
zero('unit mean metric matches accepted',1/(al+be*v).subs({al:1,be:1})-1/(1+v))
scalar_cov=-(scalar_cometric*(k-ep/v)/2)
zero('weighted entropy covariance drift',scalar_cov-(2*al*ep+be*ep*v-2*al*k*v-be*k*v*v))
zero('unit entropy covariance drift',scalar_cov.subs({al:1,be:1})-(2*ep+ep*v-2*k*v-k*v*v))
zero('scalar equilibrium',scalar_cov.subs(v,ep/k))

# Symbolic noncommuting two-dimensional matrices.
a,b,c,p,q,r=s.symbols('a b c p q r',real=True)
S=s.Matrix([[a,b],[b,c]])
Q=s.Matrix([[p,q],[q,r]])
I=s.eye(2)
K=lambda A:2*(A*S+S*A+S*A*S)
H=(Q-ep*S.inv())/2
cov=2*ep*I+ep*S-Q*S-S*Q-S*Q*S
zero('general symmetric 2D cotangent-to-drift',-K(H)-cov)
zero('entropy-only map',-K(-S.inv()/2)-(2*I+S))
zero('source target and time scaling',ep*(2*I-Q*S/ep-S*Q/ep+S-S*Q*S/ep)-cov)
zero('positive epsilon equilibrium',cov.subs({a:(ep*Q.inv())[0,0],b:(ep*Q.inv())[0,1],c:(ep*Q.inv())[1,1]}))

# Exact full Gaussian density score at a noncommuting rational state.
S=s.Matrix([[s.Rational(3,2),s.Rational(1,3)],[s.Rational(1,3),s.Rational(4,5)]])
Q=s.Matrix([[2,s.Rational(1,4)],[s.Rational(1,4),1]])
e=s.Matrix([s.Rational(2,3),-s.Rational(1,2)])
z=s.Matrix(s.symbols('z1 z2'))
P=S.inv()
truth('test matrices do not commute',Q*S!=S*Q)
C=Q-ep*P
aa=Q*e
mean=-(I+S)*aa
cov=2*ep*I+ep*S-Q*S-S*Q-S*Q*S
score=-(s.trace(P*cov))/2+(z.T*P*mean)[0]+(z.T*P*cov*P*z)[0]/2
phi=(z.T*C*z)[0]/2+(aa.T*z)[0]-s.trace(C*S)/2
pde=s.trace(C)-(z.T*P*(C*z+aa))[0]-phi
zero('full 2D Gaussian density tangency with symbolic epsilon',score-pde)

# The exact perturbation equations used in the proof.
aa,bb,cc=s.symbols('aa bb cc',real=True)
S0=s.Matrix([[aa,bb],[bb,cc]])
D=S-S0
ff=lambda sig,eps:2*eps*I+eps*sig-Q*sig-sig*Q-sig*Q*sig
zero('covariance perturbation identity',ff(S,ep)-ff(S0,0)-(-Q*D-D*Q-D*Q*S-S0*Q*D+ep*(2*I+S)))
e0=s.Matrix(s.symbols('e01 e02'))
z=e-e0
zero('mean perturbation identity',-(I+S)*Q*e+(I+S0)*Q*e0-(-(I+S)*Q*z-D*Q*e0))

# Verify full-density scalar drift-sign discriminator at its own target.
xx=s.symbols('xx',real=True)
pi=s.exp(-xx**2/2)/s.sqrt(2*s.pi)
minus=s.diff(s.diff(pi,xx)-pi*s.diff(s.log(pi),xx),xx)
plus=s.diff(s.diff(pi,xx)+pi*s.diff(s.log(pi),xx),xx)
zero('correct minus drift preserves own Gaussian target',minus)
truth('printed plus drift fails stationarity at target',s.simplify(plus)!=0)

# Input immutability is independently checkable.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='67577bc185c3190cbf131993fdfdd36aa67c605435fd225eb6f29b2cc6c21efa'
truth('accepted snapshot matches supplied hash',sha(ROOT/'inputs/accepted-gaussian-RESULT.md')==expected)
original=ROOT.parent/'gaussian-correction-geometry-20261011/RESULT.md'
if original.exists(): truth('frozen accepted original remains unchanged',sha(original)==expected)
source_file=ROOT/'wias_preprints_3198.pdf'
source_custody={'status':'unavailable','reason':'Raw third-party manuscript omitted from portable package. Formula/proof controls still run; URL and expected hash are recorded in SOURCE_READING.json.'}
if source_file.exists():
 truth('primary PDF identity',sha(source_file)=='f7d34fed7f0c9be50564b0a931e1c9a3ed4b34d59c0323cdd2ce940e4a5d2e29')
 source_custody={'status':'verified','sha256':sha(source_file)}
elif args.require_source_custody:
 raise SystemExit('Source custody unavailable: provide the exact primary PDF or omit --require-source-custody to run mathematical controls only.')

numerical=[]
try:
 import numpy as np
 from scipy.integrate import solve_ivp
 Qn=np.array(Q,dtype=float)
 Sn=np.array(S,dtype=float)
 en=np.array(e,dtype=float).reshape(2)
 qmin,qmax=np.linalg.eigvalsh(Qn)[[0,-1]]
 epsbar=0.5
 M=max(np.linalg.eigvalsh(Sn)[-1],epsbar/qmin)
 R=float(np.sqrt(en@Qn@en/qmin))
 L=qmax*(2*(1+M)+R)
 A=np.sqrt(2)*(2+M)
 T=1.0
 ts=np.linspace(0,T,101)
 init=np.r_[en,Sn.reshape(-1)]
 def rhs(t,y,eps):
  ee=y[:2]; sig=y[2:].reshape(2,2)
  return np.r_[-(np.eye(2)+sig)@Qn@ee,(2*eps*np.eye(2)+eps*sig-Qn@sig-sig@Qn-sig@Qn@sig).reshape(-1)]
 base=solve_ivp(lambda t,y:rhs(t,y,0),(0,T),init,t_eval=ts,rtol=1e-11,atol=1e-13)
 truth('numerical zero-entropy solve completed',base.success)
 for eps in [0.5,0.1,0.01,0.001]:
  sol=solve_ivp(lambda t,y:rhs(t,y,eps),(0,T),init,t_eval=ts,rtol=1e-11,atol=1e-13)
  truth(f'numerical epsilon={eps} solve completed',sol.success)
  energies=[]; min_eig=float('inf'); max_eig=0; max_error=0; max_bound_violation=-float('inf')
  for j,t in enumerate(ts):
   ee=sol.y[:2,j]; sig=sol.y[2:,j].reshape(2,2)
   vals=np.linalg.eigvalsh(sig)
   min_eig=min(min_eig,float(vals[0])); max_eig=max(max_eig,float(vals[-1]))
   energies.append(0.5*(ee@Qn@ee+np.trace(Qn@sig)-eps*np.linalg.slogdet(sig)[1]))
   err=np.linalg.norm(ee-base.y[:2,j])+np.linalg.norm(sig-base.y[2:,j].reshape(2,2),'fro')
   bound=eps*A*np.expm1(L*t)/L
   max_error=max(max_error,float(err)); max_bound_violation=max(max_bound_violation,float(err-bound))
  ell=float(np.linalg.eigvalsh(Sn)[0]*np.exp(-qmax*(2+M)*T))
  truth(f'numerical epsilon={eps} shared eigenvalue bounds',min_eig>=ell-1e-10 and max_eig<=M+1e-10)
  truth(f'numerical epsilon={eps} energy decrease',np.max(np.diff(energies))<1e-9)
  truth(f'numerical epsilon={eps} perturbation bound',max_bound_violation<1e-9)
  numerical.append(dict(epsilon=eps,max_state_error=max_error,min_covariance_eigenvalue=min_eig,max_covariance_eigenvalue=max_eig,max_bound_violation=max_bound_violation))
except ImportError as ex:
 numerical=[{'not_run':str(ex)}]

result={'status':'all controls passed','proof_scope':'Finite controls only; see RESULT.md for all-dimension proof and assumptions. No formal-kernel certification or independent review.','checks':checks,'check_count':len(checks),'numerical_controls':numerical,'source_custody':source_custody,'source_pdf_sha256':sha(source_file) if source_file.exists() else None,'result_sha256':sha(ROOT/'RESULT.md')}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'output':str(args.output),'source_custody':source_custody,'numerical_controls':numerical},indent=2))
