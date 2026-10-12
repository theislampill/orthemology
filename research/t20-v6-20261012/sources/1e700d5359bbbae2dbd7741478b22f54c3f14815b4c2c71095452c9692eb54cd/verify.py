#!/usr/bin/env python3
"""Exact supplemental controls, not a proof assistant or analytic existence proof."""
from pathlib import Path
import argparse,hashlib,json
import sympy as S
P=argparse.ArgumentParser();P.add_argument('--output-dir');P.add_argument('--original-root');args=P.parse_args()
root=Path(__file__).resolve().parent; out=Path(args.output_dir) if args.output_dir else root;out.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,value):
 if isinstance(value,S.MatrixBase): ok=all(S.simplify(x)==0 for x in value)
 elif isinstance(value,bool):ok=value
 else:ok=S.simplify(value)==0
 if not ok:raise RuntimeError('FAILED '+name+': '+str(value))
 checks.append(name)
b,s,beta,tau=S.symbols('b s beta tau', real=True, nonzero=True)
d=b-beta
F=(b*(s-tau)-d*(1+2*s+b*b/3))/tau
H=(2*b*s*d-(s+2+2*b*b)*(s-tau))/tau
M=S.Matrix([[1+2*s+b*b/3,-2*b*s],[-2*b*s,2*s*(s+2+2*b*b)]])
g=S.Matrix([d/tau,(s-tau)/(2*s*tau)])
check('mobility reproduces polynomial ODE',S.Matrix([F,H])+M*g)
check('positive boundary derivative',H.subs(s,0)-2*(1+b*b))
check('boundary b derivative',F.subs(s,0)+b+d*(1+b*b/3)/tau)
D=S.expand((g.T*M*g)[0])
R=(1+2*s+b*b/3)*d*d/tau**2-2*b*d*(s-tau)/tau**2+(s*s+(2+2*b*b-2*tau)*s+tau*tau-4*tau*(1+b*b))/(2*tau*tau)
check('exact pole decomposition',D-(1+b*b)/s-R)
check('energy dissipation',g.dot(S.Matrix([F,H]))+D)
Sigma=S.Matrix([[1,b],[b,b*b+s]]);Gamma=S.Matrix([[1,beta],[beta,beta*beta+tau]])
gamma=d*(b-3*beta)/tau;E11=S.diag(1,0);C=Gamma.inv()-Sigma.inv()-gamma*E11/3
SD=-(C*Sigma+Sigma*C)-Sigma*C*Sigma
check('full covariance versus parameter tangent',SD-Sigma.diff(b)*F-Sigma.diff(s)*H)
check('whole y variance fixed',SD[0,0])
check('field action equals minimum dissipation',S.trace(C*Sigma*C)+S.trace(C*Sigma*C*Sigma)/2-D)
check('reaction action has no pole',S.cancel(S.trace(C*Sigma*C*Sigma)/2).as_numer_denom()[1].has(s)==False)
# Nonzero z-mean control: full projected mean and centered covariance.
c,y,z=S.symbols('c y z',real=True);k=c*(b-2*beta)/(2*tau)
ell=Gamma.inv()*S.Matrix([0,c])-S.Matrix([k,0])
md=-(S.eye(2)+Sigma)*ell
check('Gaussian y mean fixed',md[0])
check('Gaussian hidden mean homogeneous ODE',md[1]+c*(1+s+b*b/2)/tau)
check('linear multiplier solves observed projection',2*k-c*(b-2*beta)/tau)
# Exact Taylor coefficients and rational leading limits.
B,p,q,t,u,eps=S.symbols('B p q t u eps', real=True)
a=2*(1+B*B)
series_sub={b:B+p*t,s:a*t+q*t*t}
check('universal dissipation residue',S.limit(t*D.subs(series_sub),t,0)-S.Rational(1,2))
E=(s+d*d)/ (2*tau)-S.Rational(1,2)+S.log(tau/s)/2
# The nonlog constant after extracting -log(t)/2 is explicit.
reg=(a*t+q*t*t+(B+p*t-beta)**2)/(2*tau)-S.Rational(1,2)+S.log(tau/(a+q*t))/2
C0=((B-beta)**2/tau-1+S.log(tau/a))/2
check('regularized energy boundary constant',reg.subs(t,0)-C0)
lead=S.Rational(1,2)/t
check('square time change action density',4*u*u*lead.subs(t,u*u)-2)
check('unit interval time change action density',4*eps*eps*u*u*lead.subs(t,eps*u*u)-2*eps)
check('length coefficient squared',S.integrate(1/S.sqrt(2*t),(t,0,eps))**2-2*eps)
check('trace covariance determinant',Sigma.det()-s)
check('stationary supplied target',S.Matrix([F,H]).subs({b:beta,s:tau}))
check('boundary not stationary',H.subs({b:0,s:0})-2)
for rec in json.loads((root/'INPUT_BINDINGS.json').read_text()):
 check('snapshot '+rec['snapshot'],hashlib.sha256((root/rec['snapshot']).read_bytes()).hexdigest()==rec['sha256'])
 if args.original_root:
  check('original '+rec['original'],hashlib.sha256((Path(args.original_root)/rec['original']).read_bytes()).hexdigest()==rec['sha256'])
result={'status':'PASS','count':len(checks),'checks':checks,'scope':'Exact supplemental identities and hash bindings; analytic arguments remain ordinary mathematics.'}
(out/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
