import sympy as S
import json
from pathlib import Path
checks={}
def check(n,b):
 b=bool(b); checks[n]=b
 if not b: raise RuntimeError(n)
a=S.Rational(1,2)
p=S.Matrix([S.Rational(1,2),S.Rational(1,4),S.Rational(1,4)])
q=S.Matrix([S.Rational(1,4),S.Rational(1,2),S.Rational(1,4)])
def F(v):
 w=v.applyfunc(S.sqrt); return w/sum(w)
y0,y1,ym=F(p),F(q),F((p+q)/2)
check('endpoint third coordinates equal',S.simplify(y0[2]-y1[2])==0)
check('midpoint outside endpoint hull',bool(S.simplify(y0[2]-ym[2])>0))
d=S.symbols('d',real=True)
f=(S.sqrt(6+5*d*d)-1)/5
check('arc inverse-square equation',S.simplify(5*f*f+2*f-1-d*d)==0)
check('strict curvature formula',S.simplify(S.diff(f,d,2)-6/(6+5*d*d)**S.Rational(3,2))==0)
# Parameter d increases from q toward p: A=sqrt(1+t), B=sqrt(2-t).
A,B=S.symbols('A B',positive=True)
Ap,Bp=S.symbols('Ap Bp',real=True)
D=(A-B)/(A+B+1)
check('arc monotone parameter derivative',S.simplify(S.diff(D,A)*Ap+S.diff(D,B)*Bp-((2*B+1)*Ap-(2*A+1)*Bp)/(A+B+1)**2)==0)
# General positive endpoints: local logarithmic slopes u_i are injective functions of endpoint ratios.
u,v,w,b=S.symbols('u v w b',real=True)
V=S.Matrix([[1,b*u,b*(b-1)*u*u],[1,b*v,b*(b-1)*v*v],[1,b*w,b*(b-1)*w*w]])
check('three-ratio derivative rank',S.simplify(V.det()-b*b*(b-1)*(v-u)*(w-u)*(w-v))==0)
r,t=S.symbols('r t',positive=True)
check('ratio slope injectivity',S.simplify(S.diff((r-1)/(1+t*(r-1)),r)-1/(1+t*(r-1))**2)==0)
# Exact audit conjugacy sample; alpha=1/2, nonuniform target, nonconstant likelihood.
x=[S.Rational(1,2),S.Rational(1,3),S.Rational(1,6)]
pi=[S.Rational(1,4),S.Rational(1,2),S.Rational(1,4)]
L=[S.Integer(1),S.Integer(4),S.Integer(9)]
def norm(v): return [S.simplify(z/sum(v)) for z in v]
def R(v): return norm([S.sqrt(z*c) for z,c in zip(v,pi)])
def audit(v,ls): return norm([z*l for z,l in zip(v,ls)])
left=R(audit(x,L)); right=audit(R(x),[S.sqrt(l) for l in L])
check('tempered-likelihood conjugacy',all(S.simplify(z-w)==0 for z,w in zip(left,right)))
check('same-likelihood noncommutation',any(S.simplify(z-w)!=0 for z,w in zip(left,audit(R(x),L))))
# Actual full split: pi=N(0,1), h=log2, initial delta +/-2 -> N(+/-1,3/4).
z=S.symbols('z',real=True)
actual=S.exp(-7*z*z/12)*S.sqrt(S.cosh(4*z/3))
endpoint_mix=S.exp(-7*z*z/12)*S.cosh(2*z/3)
check('full split density envelopes differ',S.simplify(S.diff(actual/endpoint_mix,z,2).subs(z,0)-S.Rational(4,9))==0)
# Equal-weight mixture is the sole reflection-symmetric point on the endpoint line.
plus=S.exp(-7*z*z/12+2*z/3)
minus=S.exp(-7*z*z/12-2*z/3)
lam=S.symbols('lam',real=True)
mix=lam*plus+(1-lam)*minus
check('reflection forces equal mixture',S.simplify(mix-mix.subs(z,-z)-(2*lam-1)*(plus-minus))==0)
# Match the report's inherited delta +/-1 fixture separately.
actual1=S.exp(-7*z*z/12)*S.sqrt(S.cosh(2*z/3))
mix1=S.exp(-7*z*z/12)*S.cosh(z/3)
check('report full split log curvature',S.simplify(S.diff(S.log(actual1),z,2).subs(z,0)+S.Rational(17,18))==0)
check('report endpoint mixture log curvature',S.simplify(S.diff(S.log(mix1),z,2).subs(z,0)+S.Rational(19,18))==0)
y=R(x)
back=norm([v*v/c for v,c in zip(y,pi)])
check('nonuniform inverse reaction',all(S.simplify(v-w)==0 for v,w in zip(x,back)))
# The original inequality x_1 <= 1/2 is equivalent after squaring with the same normalizer.
check('inverse homogeneous inequality on boundary',S.simplify(sum(((1 if i==0 else 0)-S.Rational(1,2))*y[i]**2/pi[i] for i in range(3)))==0)
# Same-outcome instrument obstruction, optional composition guard.
c0,c1=S.symbols('c0 c1',real=True)
M=S.Matrix([[S.sqrt(3)/2,S.Rational(1,2)],[1/S.sqrt(2),1/S.sqrt(2)],[S.Rational(1,2),S.sqrt(3)/2]])
check('escort audit instrument inconsistency',M.row_join(S.ones(3,1)).det()!=0)
Path(__file__).with_name('INDEPENDENT_CONTROLS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
