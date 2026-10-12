#!/usr/bin/env python3
"""Independent exact controls and separately labelled floating point probes."""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.special import logsumexp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'correction-audit-transport-20261011'
p=argparse.ArgumentParser(); p.add_argument('--output',default='CONTROL_RESULTS.json'); args=p.parse_args()
rows=[]
def ck(name,condition,detail=None,kind='exact'):
    rows.append(dict(name=name,passed=bool(condition),detail=detail,kind=kind))
    if not condition: raise RuntimeError(name)
def ze(name,expr):
    entries=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    ck(name,all(s.simplify(v)==0 for v in entries))
def norm(x):return x/sum(x)
def audit(x,L):return norm(x.multiply_elementwise(L))
def power(x,pi,a):return norm(s.Matrix([x[i]**a*pi[i]**(1-a) for i in range(len(x))]))
R=s.Rational
K=s.Matrix([[R(1,2),R(1,4),R(1,5)],[R(1,3),R(1,2),R(1,5)],[R(1,6),R(1,4),R(3,5)]])
pi=s.Matrix([R(1,6),R(1,3),R(1,2)]); r=s.Matrix([R(1,5),R(3,10),R(1,2)]); L=s.Matrix([1,3,2]); a=R(1,3)
ck('independent positive invertible stochastic kernel',K.det()!=0 and all(v>0 for v in K) and list(s.ones(1,3)*K)==[1,1,1])
f=K*r; ell=s.Matrix([(K*r.multiply_elementwise(L))[i]/f[i] for i in range(3)])
q=power(f,pi,a); expected=power(K*audit(r,L),pi,a)
ck('cube-power conditional transport',max(abs(float(s.N(v,30))) for v in expected-audit(q,ell.applyfunc(lambda z:z**a)))<1e-25,kind='high precision numerical')
for i in range(1,3):
    ze('exact powered transport odds cubed '+str(i),(K*audit(r,L))[i]/(K*audit(r,L))[0]-f[i]*ell[i]/(f[0]*ell[0]))
ck('inverse power and kernel recover prior',max(abs(float(s.N(v,30))) for v in K.inv()*power(q,pi,1/a)-r)<1e-25,kind='high precision numerical')
ck('wrong exponent rejected',max(abs(float(s.N(v,30))) for v in expected-audit(q,ell))>1e-3,kind='high precision numerical')
# General joint normalizers on two genuinely different conditionals, not constants.
r2=s.Matrix([R(1,2),R(1,4),R(1,4)]); L2=s.Matrix([R(1,2),2,4]); nu=s.Matrix([R(2,5),R(3,5)])
qs=[]; ells=[]; H=[]; Z=[]; targets=[]
for rr,ll in [(r,L),(r2,L2)]:
    ff=K*rr; ee=s.Matrix([(K*rr.multiply_elementwise(ll))[i]/ff[i] for i in range(3)])
    qq=power(ff,pi,a); hh=sum(qq[i]*ee[i]**a for i in range(3))
    qs.append(qq); ells.append(ee); H.append(hh); Z.append(sum(rr.multiply_elementwise(ll)))
    targets.append(power(K*audit(rr,ll),pi,a))
# Confirm exact identity within each fibre; compare only marginal determinants for naive failure.
for j in range(2):
    ck('joint corrected conditional '+str(j),max(abs(float(s.N(v,30))) for v in audit(qs[j],ells[j].applyfunc(lambda z:z**a))-targets[j])<1e-25,kind='high precision numerical')
    ck('joint fibre integrated multiplier '+str(j),abs(float(s.N(sum(qs[j][i]*Z[j]*ells[j][i]**a/H[j] for i in range(3))-Z[j],30)))<1e-25,kind='high precision numerical')
ck('naive joint powered factors change marginal',abs(float(s.N(H[0]*Z[1]-H[1]*Z[0],30)))>1e-3,kind='numerical discrimination of exact expressions')
# Pointwise null-set likelihood: L(0)=2, otherwise 1. r=(delta_0+delta_1)/2.
# OU h=log2 yields ratio k1/k0=exp((4z-1)/6); at z=1/4 it is 1.
u=s.symbols('u',positive=True); ee=(2+u)/(1+u)
ze('singleton-exception likelihood conditional at equal kernels',ee.subs(u,1)-R(3,2))
ze('singleton-exception likelihood conditional at ratio three',ee.subs(u,3)-R(5,4))
ck('pointwise-null exception remains detectable',s.sqrt(R(5,6))!=1)
# Independent exact noncommuting 2D fixture with a rotated target eigenbasis.
U=s.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]]); T=U*s.diag(1,2)*U.T; A=U*s.diag(R(1,4),R(1,2))*U.T
Q=T-A*T*A; S=s.Matrix([[3,-1],[-1,2]]); a=R(1,4); m=s.Matrix([2,-3]); g=s.Matrix([-2,1]); theta=s.Matrix([-1,3]); V=A*S*A+Q
C=(a*V.inv()+(1-a)*T.inv()).inv(); mp=g+C*a*V.inv()*A*(m-g); b=a*V.inv()*A*S*theta
ck('rotated target noncommuting covariance',A*S!=S*A and T[0,1]!=0)
ze('direct precision natural-parameter audit shift',C*a*V.inv()*A*S*theta-C*b)
ze('conditional expectation transpose orientation',a*(theta.T*S*A*V.inv()).T-b)
ck('wrong order has nonzero residual',a*V.inv()*S*A*theta!=b)
P=C.inv()-(1-a)*T.inv(); Vr=a*P.inv()
ze('independent exact covariance inverse',A.inv()*(Vr-Q)*A.inv()-S)
ze('independent exact mean inverse',g+A.inv()*(Vr/a)*C.inv()*(mp-g)-m)
# PSD image boundary generalized to rotated anisotropic target.
Cmin=(a*Q.inv()+(1-a)*T.inv()).inv()
ze('anisotropic boundary corresponds to Dirac',a*(Cmin.inv()-(1-a)*T.inv()).inv()-Q)
# Numerical whole-mixture OU/reaction audit identity with integrated normalizers.
w=np.array([.2,.35,.45]); atoms=np.array([-2.,.25,3.]); lv=np.array([.7,2.,1.3]); h=.6; aa=np.exp(-h); A0=aa; Q0=1-A0*A0
logpi=lambda z:-.5*z*z-.5*np.log(2*np.pi)
def logf(z,weights):return logsumexp(np.log(weights)-.5*(z-A0*atoms)**2/Q0-.5*np.log(2*np.pi*Q0))
def density(z,weights):return np.exp(aa*logf(z,weights)+(1-aa)*logpi(z))
wa=w*lv/(w@lv); n0=quad(lambda z:density(z,w),-15,15,epsabs=1e-12)[0]; n1=quad(lambda z:density(z,wa),-15,15,epsabs=1e-12)[0]
def ellnum(z):return np.exp(logf(z,w*lv)-logf(z,w))
Hn=quad(lambda z:density(z,w)/n0*ellnum(z)**aa,-15,15,epsabs=1e-12)[0]
errs=[abs(density(z,wa)/n1-density(z,w)/n0*ellnum(z)**aa/Hn) for z in np.linspace(-8,8,81)]
ck('actual OU mixture powered transport quadrature',max(errs)<2e-12,max(errs),'numerical, truncated integration')
wrongH=quad(lambda z:density(z,w)/n0*ellnum(z),-15,15,epsabs=1e-12)[0]
wrong=max(abs(density(z,wa)/n1-density(z,w)/n0*ellnum(z)/wrongH) for z in np.linspace(-4,4,41))
ck('actual OU mixture rejects unpowered multiplier',wrong>1e-3,wrong,'numerical, truncated integration')
ck('actual OU mixture distinguishes original evidence',abs(Hn-w@lv)>1e-2,{'H':Hn,'Z':float(w@lv)},'numerical, truncated integration')
# Actual inherited function at rotated target plus full-rank and partial-rank inputs.
spec=importlib.util.spec_from_file_location('split',SOURCE/'inputs/gaussian_step.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
for label,ss in [('full',S),('rank_one',s.Matrix([[4,2],[2,1]])),('dirac',s.zeros(2))]:
    sn=np.array(ss,dtype=float); tn=np.array(T,dtype=float); mn=np.array(m,dtype=float).ravel(); gn=np.array(g,dtype=float).ravel(); th=np.array(theta,dtype=float).ravel()
    base=mod.gaussian_step(mn,sn,gn,tn,float(np.log(4))); out=mod.gaussian_step(mn+sn@th,sn,gn,tn,float(np.log(4)))
    bn=base['reaction_exponent']*np.linalg.solve(base['diffusion_covariance'],base['diffusion_matrix']@sn@th)
    err=float(np.max(abs(out['mean']-base['mean']-base['covariance']@bn)))
    ck('actual implementation rotated '+label,err<2e-12,err,'numerical floating-point')
# Parent-supplied countable-fibre integrated-domain discriminator.
e=s.symbols('e',positive=True); n=s.symbols('n',integer=True,positive=True)
ze('countable conditional high mass formula',e/(e+(1-e)*e**2)-1/(1+e-e**2))
ze('countable high mass denominator bound identity',s.Rational(5,4)-(1+e-e**2)-(e-s.Rational(1,2))**2)
ze('countable initial integrated second moment',s.summation(2**(-n),(n,1,s.oo))-1)
ze('countable global evidence',s.summation(2**(-2*n)+2**(-3*n)-2**(-4*n),(n,1,s.oo))-s.Rational(43,105))
ze('countable global audited second moment',1/s.Rational(43,105)-s.Rational(105,43))
source_hashes={str(f.relative_to(SOURCE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(SOURCE.rglob('*')) if f.is_file()}
result=dict(status='PASS',count=len(rows),checks=rows,source_hashes=source_hashes,versions=dict(python=sys.version.split()[0],sympy=s.__version__,numpy=np.__version__),limits=['Finite controls do not prove universal assertions.','Quadrature is truncated and numerical, not certified.','No stability, arbitrary-law finite computation, field novelty, or closure claim.'])
(HERE/args.output).write_text(json.dumps(result,indent=2)+'\n'); print('PASS',len(rows),'independent controls')
