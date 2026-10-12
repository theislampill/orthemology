import numpy as np, json, datetime
from scipy.integrate import solve_ivp
from pathlib import Path

def phi(u):
 q,x,y=u
 return .5*q*q+.5*(y-x)**2+.1*np.sum(u**4)
def grad(u):
 q,x,y=u
 return np.array([q,x-y,y-x])+.4*u**3
def K(u):
 q=u[0]
 return np.array([2+2*np.cosh(q),1+np.exp(-q),1+np.exp(q)])
def dg(u,v):
 d=v-u;a=(u+v)/2;s=np.dot(d,d)
 return grad(a) if s==0 else grad(a)+.1*np.sum(a*d**3)*d/s

def internal(u,h):
 d=np.zeros(3)
 for j in range(100):
  dn=-h*K(u+d/2)*dg(u,u+d)
  if np.linalg.norm(dn-d)<1e-14:
   d=dn;break
  d=dn
 else:raise RuntimeError('Picard fail')
 D=dg(u,u+d);rho=d+h*K(u+d/2)*D
 if phi(u+d)>phi(u)+1e-14:raise RuntimeError('descent fail')
 return u+d,np.linalg.norm(rho),j+1

def step(z,h,endpoint=False):
 u=z[:3];v=z[3];m=z[4]
 up,res,it=internal(u,h);vp=v*(1-h/2)/(1+h/2)
 old=np.array([phi(u),v*v/2]);new=np.array([phi(up),vp*vp/2]);c=new if endpoint else (old+new)/2
 a=1/(1+h*(c-min(c))+.5*h*h*(c-min(c))**2)
 w=np.array([m,1-m])*a;w/=sum(w)
 return np.r_[up,vp,w[0]],res,it

def rhs(t,z):
 u=z[:3];v=z[3];m=z[4]
 return np.r_[-K(u)*grad(u),-v,-m*(1-m)*(phi(u)-v*v/2)]
z0=np.array([.4,-.3,.7,.8,.4]);T=.25
ref=solve_ivp(rhs,[0,T],z0,method='DOP853',rtol=3e-14,atol=1e-15).y[:,-1]
rows=[]
for endpoint in [False,True]:
 runs=[]
 for n in [32,64,128,256]:
  z=z0.copy();maxres=0;maxit=0
  for j in range(n):
   z,res,it=step(z,T/n,endpoint);maxres=max(res,maxres);maxit=max(it,maxit)
  runs.append(dict(n=n,error=float(max(abs(z-ref))),mass_error=float(abs(z[4]-ref[4])),max_residual=maxres,max_iterations=maxit))
 rates=[float(np.log2(a['error']/b['error'])) for a,b in zip(runs,runs[1:])]
 if not endpoint and not all(1.95<r<2.05 for r in rates):raise RuntimeError(rates)
 if endpoint and not .9<rates[-1]<1.1:raise RuntimeError(rates)
 rows.append(dict(endpoint_only=endpoint,runs=runs,rates=rates))
# Independent non-quadratic chart check: group audit does not change internal work.
z1,_,_=step(z0,.01);a,b=2.,.3;za=z0.copy();za[4]=a*z0[4]/(a*z0[4]+b*(1-z0[4]));z2,_,_=step(za,.01)
err=max(max(abs(z1[:4]-z2[:4])),abs(z2[4]-a*z1[4]/(a*z1[4]+b*(1-z1[4]))))
if err>1e-14:raise RuntimeError(err)
# Exact counterexample to unqualified stationary-input preservation: phi=-x^2/2,h=2,u=0,v=1.
stationary=dict(u=0,v=1,h=2,residual=1-2*.5,energy_change=-.5)
# Verify quartic Gonzalez chain identity numerically across unrelated chords.
rng=np.random.default_rng(4280);chain=max(abs(np.dot(dg(u,v),v-u)-(phi(v)-phi(u))) for u,v in [(rng.normal(size=3),rng.normal(size=3)) for _ in range(100)])
if chain>1e-12:raise RuntimeError(chain)
out=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Independent floating-point controls, not interval-certified proof; no author code imported',potential='q^2/2+(x2-x1)^2/2+0.1(q^4+x1^4+x2^4)',reference=ref.tolist(),runs=rows,audit_error=err,max_chain_error=chain,stationary_nonlocal_root_counterexample=stationary)
Path('t20-depth-reassessment-20261011/joint_correction_review/INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
