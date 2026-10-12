#!/usr/bin/env python3
"""Exact supplementary controls; ordinary proofs in RESULT.md."""
import argparse,hashlib,json,platform
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'author-run');ap.add_argument('--original-root',type=Path);args=ap.parse_args()
root=Path(__file__).resolve().parent;args.output_dir.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,expr):
    if isinstance(expr,bool):ok=expr
    elif isinstance(expr,S.MatrixBase):ok=all(S.simplify(e)==0 for e in expr)
    else:ok=S.simplify(expr)==0
    checks.append({'name':name,'pass':bool(ok)})
    if not ok:raise AssertionError((name,expr))
b,beta,y,z,e=S.symbols('b beta y z e',real=True);s,tau=S.symbols('s tau',positive=True)
Sig=S.Matrix([[1,b],[b,b*b+s]]);Gam=S.Matrix([[1,beta],[beta,beta*beta+tau]])
P=Sig.inv();Q=Gam.inv();x=S.Matrix([y,z]);E11=S.diag(1,0);delta=b-beta
gamma=delta*(delta-2*beta)/tau
A=Q-P;C=A-gamma*E11/3
q=(x.T*A*x)[0]/2+S.log(tau/s)/2
qexplicit=S.log(tau/s)/2+(z-beta*y)**2/(2*tau)-(z-b*y)**2/(2*s)
check('target determinant',Gam.det()-tau)
check('current determinant',Sig.det()-s)
check('conditional score equals Gaussian log ratio',q-qexplicit)
def moment(n):
    if n%2:return S.Integer(0)
    return S.factorial2(n-1)*s**(n//2) if n else S.Integer(1)
def conditional(poly):
    return S.simplify(sum(coef*moment(n[0]) for n,coef in S.Poly(S.expand(poly),e).terms()))
qpoly=(q-S.log(tau/s)/2).subs(z,b*y+e)
h=conditional(qpoly)+S.log(tau/s)/2
hfull=(S.log(tau/s)+s/tau-1+delta*delta*y*y/tau)/2
check('conditional KL formula',h-hfull)
m=conditional(S.diff(q,y).subs(z,b*y+e))
check('conditional y score uses fixed z derivative',m+beta*delta*y/tau)
energy=(s+delta*delta)/(2*tau)-S.Rational(1,2)+S.log(tau/s)/2
check('energy Gaussian matrix KL',energy-(S.trace(Q*Sig)-2+S.log(tau/s))/2)
hcenter=delta*delta*(y*y-1)/(2*tau)
check('conditional score divergence and reaction',(-S.diff(m,y)+y*m)+hcenter-gamma*(y*y-1)/2)
phi=gamma*(y*y-1)/6
check('multiplier solves Gaussian coarse operator',-S.diff(phi,y,2)+y*S.diff(phi,y)+phi-gamma*(y*y-1)/2)
check('target stationarity gamma',gamma.subs(b,beta))
Vun=2*S.eye(2)+Sig-Q*Sig-Sig*Q-Sig*Q*Sig
V=-(C*Sig+Sig*C)-Sig*C*Sig
check('projected matrix covariance formula',V-Vun-gamma*(E11*Sig+Sig*E11+Sig*E11*Sig)/3)
check('unconstrained yy drift',Vun[0,0]+gamma)
check('full corrected yy tangent',V[0,0])
bd=(b*(s-tau)-delta*(1+2*s+b*b/3))/tau
sd=(2*b*s*delta-(s+2+2*b*b)*(s-tau))/tau
check('corrected b ODE',V[0,1]-bd)
check('corrected s ODE',V[1,1]-2*b*V[0,1]-sd)
M=S.Matrix([[1+2*s+b*b/3,-2*b*s],[-2*b*s,2*s*(s+2+2*b*b)]])
grad=S.Matrix([S.diff(energy,b),S.diff(energy,s)])
check('energy gradient coordinates',grad-S.Matrix([delta/tau,(s-tau)/(2*s*tau)]))
check('mobility gradient agrees with full field',-M*grad-S.Matrix([bd,sd]))
check('mobility determinant factorization',M.det()-2*s*(b*b+2*s+1)*(2*b*b+3*s+6)/3)
# Full density equality, not only Gaussian moment equality.
density_gaussian=(-S.trace(P*V)+(x.T*P*V*P*x)[0])/2
density_field=S.trace(C)-(x.T*P*C*x)[0]-(x.T*C*x)[0]/2+S.trace(C*Sig)/2
check('full Gaussian density tangent identity',density_gaussian-density_field)
D=(grad.T*M*grad)[0]
Dfield=S.trace(C*Sig*C)+S.trace((C*Sig)**2)/2
Du=S.trace(A*Sig*A)+S.trace((A*Sig)**2)/2
check('full minimum field action equals metric dissipation',Dfield-D)
check('KL chain rule',grad[0]*bd+grad[1]*sd+D)
check('horizontal correction squared cost',Du-D-gamma*gamma/6)
Cp=gamma*E11/3
cross=S.trace(A*Sig*Cp)+S.trace(A*Sig*Cp*Sig)/2
check('horizontal orthogonal pairing',cross-gamma*gamma/6)
# Blindly retaining only the h score gives the exact marginal leak.
Cwrong=A-delta*delta*E11/(3*tau)
Vwrong=-(Cwrong*Sig+Sig*Cwrong)-Sig*Cwrong*Sig
check('wrong product specialization leaks marginal',Vwrong[0,0]-2*beta*delta/tau)
check('wrong formula leak is nonzero rational control',Vwrong[0,0].subs({b:0,beta:S.Rational(1,2),tau:1,s:1})+S.Rational(1,2))
# Exact product-target recovery.
check('product multiplier recovery',gamma.subs({beta:0,tau:1})-b*b)
check('product b recovery',bd.subs({beta:0,tau:1})+b*(s+2+b*b/3))
check('product s recovery',sd.subs({beta:0,tau:1})-((1-s)*(s+2)+2*b*b))
# Target is stationary even when dependent.
check('correlated target potential zero',C.subs({b:beta,s:tau}))
check('target b stationary',bd.subs({b:beta,s:tau}))
check('target s stationary',sd.subs({b:beta,s:tau}))
check('cross covariance not extra invariant',bd.subs(b,beta)-beta*(s-tau)/tau)
# Positive creation control from I to Gamma=[[1,1],[1,2]].
sp={b:0,s:1,beta:1,tau:1}
check('control projected potential matrix',C.subs(sp)-S.Matrix([[0,-1],[-1,0]]))
check('control velocity',(-C*x).subs(sp)-S.Matrix([z,y]))
check('control reaction',(-(x.T*C*x)[0]/2+S.trace(C*Sig)/2).subs(sp)-y*z)
check('control full density derivative',density_field.subs(sp)-3*y*z)
check('control b creation',bd.subs(sp)-3)
check('control s unchanged initially',sd.subs(sp))
check('control y law unchanged',V[0,0].subs(sp))
check('control energy',energy.subs(sp)-S.Rational(1,2))
check('control dissipation',D.subs(sp)-3)
check('control wrong y variance',Vwrong[0,0].subs(sp)+2)
# Compact-sublevel decomposition is exact; its endpoint divergence is proved in prose.
u=S.symbols('u',positive=True)
check('energy sublevel split',energy-delta*delta/(2*tau)-(s/tau-1-S.log(s/tau))/2)
check('scalar entropy unique critical equation',S.diff(u-1-S.log(u),u)-(u-1)/u)
check('scalar entropy value at target',(u-1-S.log(u)).subs(u,1))
for row in json.loads((root/'INPUT_BINDINGS.json').read_text()):
    check('snapshot binding '+row['snapshot'],hashlib.sha256((root/row['snapshot']).read_bytes()).hexdigest()==row['sha256'])
    if args.original_root:
        check('original binding '+row['original'],hashlib.sha256((args.original_root/row['original']).read_bytes()).hexdigest()==row['sha256'])
freeze=json.loads((root/'inputs/fixed-marginal-correction-20261011--AUTHOR_FREEZE.json').read_text())
reviewfreeze=json.loads((root/'inputs/fixed-marginal-correction-independent-review-20261011--REVIEW_FREEZE.json').read_text())
check('earlier author result freeze preserved',hashlib.sha256((root/'inputs/fixed-marginal-correction-20261011--RESULT.md').read_bytes()).hexdigest()==freeze['result_sha256'])
check('earlier review result freeze preserved',hashlib.sha256((root/'inputs/fixed-marginal-correction-independent-review-20261011--REVIEW.md').read_bytes()).hexdigest()==reviewfreeze['review_sha256'])
out={'status':'PASS','verification_kind':'Exact author controls supplementary to ordinary proofs','python':platform.python_version(),'sympy':S.__version__,'check_count':len(checks),'checks':checks}
(args.output_dir/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','check_count','python','sympy')},indent=2))
