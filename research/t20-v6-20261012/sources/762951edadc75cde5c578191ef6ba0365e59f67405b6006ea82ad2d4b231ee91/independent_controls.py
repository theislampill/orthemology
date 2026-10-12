"""Independent exact controls. These supplement ordinary proof, not formal certification."""
import hashlib, json
from pathlib import Path
import sympy as S
R = S.Rational
checks=[]
def check(name, condition, detail=None):
    if not bool(condition): raise AssertionError(name)
    checks.append({'name':name,'passed':True, **({'detail':str(detail)} if detail is not None else {})})
def eq(a,b): return S.simplify(a-b)==0
def vec(*x): return S.Matrix(x)
def fisher(p,v): return sum(v[i]**2/p[i] for i in range(len(p)))
def brier(p,q,mu=None):
    mu=mu or S.ones(len(p),1)
    return sum((p[i]-q[i])**2/mu[i] for i in range(len(p)))/2
def radial(a,s,t):
    z=next(v for v in a.free_symbols if str(v)=="z")
    return S.expand(a.subs(z,s)-a.subs(z,t)-S.diff(a,z).subs(z,t)*(s-t))
def valid(K):
    return all(x>=0 for x in K) and all(sum(K[:,j])==1 for j in range(K.cols)) and all(sum(K[i,:])>0 for i in range(K.rows))
# Exact rational uniformizing refinement independent of author's controls.
k=[2,3,7]; N=sum(k); p=vec(*[R(x,N) for x in k]); u=vec(R(1,5),R(-3,7),R(8,35))
E=S.zeros(N,3); A=S.zeros(3,N); start=0
for i,count in enumerate(k):
    for j in range(start,start+count): E[j,i]=R(1,count); A[i,j]=1
    start+=count
check('rational tangent is sum zero',sum(u)==0)
check('refinement admissible',valid(E)); check('coarsening admissible',valid(A))
check('coarsening is stochastic left inverse',A*E==S.eye(3))
check('rational point uniformizes',E*p==S.ones(N,1)/N)
check('rational refinement Fisher equality',eq(fisher(p,u),fisher(E*p,E*u)),fisher(p,u))
check('uniform coefficient is N times common c',eq(N*((E*u).dot(E*u)),fisher(p,u)))
check('fixed uniform Euclidean coefficient would fail',u.dot(u)!=(E*u).dot(E*u))
# Two uniform sources are joined through common dimension nm.
n,m=2,5
v=vec(R(2,3),R(-2,3)); split=S.zeros(n*m,n)
for i in range(n):
    for j in range(m): split[m*i+j,i]=R(1,m)
check('equal splitting norm scales by inverse multiplicity',eq((split*v).dot(split*v),v.dot(v)/m))
check('dimension-scaled coefficients give equality',eq(n*v.dot(v),(n*m)*(split*v).dot(split*v)))
# Binary quadratic control works for the entire binary family by a symbolic factor.
a,b,d=S.symbols('a b d', real=True)
K=S.Matrix([[a,b],[1-a,1-b]]); delta=vec(d,-d)
check('binary channel scales tangent displacement exactly',all(eq(v,0) for v in K*delta-(a-b)*delta))
check('binary squared-distance deficit factor',eq(delta.dot(delta)-(K*delta).dot(K*delta),2*d*d*(1-(a-b)**2)))
for label,K in [('identity',S.eye(2)),('flip',S.Matrix([[0,1],[1,0]])),('erasure',S.ones(2,2)/2),('noise',S.Matrix([[R(3,4),R(1,5)],[R(1,4),R(4,5)]]))]:
    pp=vec(R(1,4),R(3,4)); qq=vec(R(2,3),R(1,3))
    check('binary '+label+' admissible',valid(K))
    check('binary '+label+' Brier contracts',brier(K*pp,K*qq)<=brier(pp,qq))
# Reset Brier fails in a recoverable dimension change; transported reference succeeds.
K=S.Matrix([[1,1,0],[0,0,1]]); rev=S.Matrix([[R(1,2),0],[R(1,2),0],[0,1]])
p=vec(R(3,8),R(3,8),R(1,4)); q=vec(R(1,4),R(1,4),R(1,2)); mu=vec(1,1,1)
check('dimension-change channel admissible',valid(K)); check('pair recoverability',rev*K*p==p and rev*K*q==q)
check('reference recoverability',rev*K*mu==mu)
check('reset Brier increase',eq(brier(K*p,K*q)-brier(p,q),R(1,64)))
check('transported reference equality',eq(brier(K*p,K*q,K*mu),brier(p,q,mu)))
check('reset reference differs from transported reference',K*mu!=S.ones(2,1))
# Fisher contraction for a nontrivial rational noisy channel, all tangent vectors via PSD minors.
K=S.Matrix([[R(1,2),R(1,3),R(1,4)],[R(1,3),R(1,3),R(1,4)],[R(1,6),R(1,3),R(1,2)]])
q=vec(R(1,7),R(2,7),R(4,7)); B=S.Matrix([[1,0],[0,1],[-1,-1]])
M=B.T*(S.diag(*[1/x for x in q])-K.T*S.diag(*[1/x for x in K*q])*K)*B
check('noisy rational channel admissible',valid(K))
check('Fisher deficit symmetric',M==M.T)
check('Fisher deficit PSD via principal minors',M[0,0]>=0 and M[1,1]>=0 and M.det()>=0, M)
# Exact Hessian and forward Bregman decomposition on the positive binary cone.
x,y,r,t,c=S.symbols('x y r t c',positive=True); z=S.symbols('z',positive=True)
s=x+y; F=c*(x*S.log(x/s)+y*S.log(y/s))+s*s/2
H=S.hessian(F,(x,y)); J=S.ones(2,2)
check('cone Hessian diagonal plus rank-one form',all(eq(H[i,j],(c/(x if i==0 else y) if i==j else 0)+1-c/s) for i in range(2) for j in range(2)))
check('coordinate-additive obstruction',eq(H[0,1],1-c/s))
G=c*(x*S.log(x)+y*S.log(y)); HG=S.hessian(G,(x,y))
check('entropy radial shape cancels mixed Hessian',HG[0,1]==0)
check('unnormalized KL forward orientation',eq(G-G.subs({x:r,y:t})-(S.diff(G,x).subs({x:r,y:t})*(x-r)+S.diff(G,y).subs({x:r,y:t})*(y-t)),c*(x*S.log(x/r)+y*S.log(y/t)-x-y+r+t)))
# Evaluate general split identity with independent symbolic simplex parameters.
pv,qv,sm,tm=S.symbols('pv qv sm tm',positive=True)
ff=lambda w: c*(w*S.log(w)+(1-w)*S.log(1-w))
fz=ff(z); Df=ff(pv)-ff(qv)-S.diff(fz,z).subs(z,qv)*(pv-qv)
subs_y={x:tm*qv,y:tm*(1-qv)}; subs_x={x:sm*pv,y:sm*(1-pv)}
DF=F.subs(subs_x)-F.subs(subs_y)-S.diff(F,x).subs(subs_y)*(sm*pv-tm*qv)-S.diff(F,y).subs(subs_y)*(sm*(1-pv)-tm*(1-qv))
# Logs only expanded after all ratios of equal positive total masses cancel.
check('forward cone decomposition mass coefficient is first mass',S.simplify(S.expand_log(DF-sm*Df-(sm-tm)**2/2,force=True))==0)
# Strict convexity need not give an everywhere positive radial Hessian.
quart=(z-1)**4
check('quartic radial Hessian degenerates at one',S.diff(quart,z,2).subs(z,1)==0)
check('quartic radial second derivative nonnegative',S.diff(quart,z,2)==12*(z-1)**2)
check('quartic forward divergence separates 1 and 2',radial(quart,2,1)>0 and radial(quart,1,2)>0)
# Normalized-only contraction cannot constrain dimension-dependent radial terms.
a2=z*z/2; a3=z**3/3
check('all radial divergences vanish on normalized pair',radial(a2,1,1)==0 and radial(a3,1,1)==0)
check('different radial shapes violate full cone contraction',eq(radial(a3,2,1)-radial(a2,2,1),R(5,6)))
check('quadratic radial differs from unnormalized KL radial curvature',S.diff(a2,z,2)!=c/z)
# Affine ambiguities never change divergence, including literal a(1)=0 gauges.
alpha,beta=S.symbols('alpha beta',real=True)
check('radial affine gauge leaves divergence',eq(radial(a2+alpha*z+beta,sm,tm),radial(a2,sm,tm)))
check('literal restriction radial gauge stays normalized',((beta*(1-z)).subs(z,1))==0)
check('one-state tangent has no nonzero direction',S.zeros(1,1).rank()==0)
result={'status':'PASS','check_count':len(checks),'checks':checks,'method':'SymPy exact rational/symbolic arithmetic; ordinary proof remains separate.'}
Path(__file__).with_name('INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks)},indent=2))
