from pathlib import Path
import sympy as s
x,y=s.symbols('x y',positive=True)
f=s.Function('f')
b=f(x)-f(y)-s.diff(f(y),y)*(x-y)
H=s.hessian(b,(x,y))
expected=s.Matrix([[s.diff(f(x),x,2),-s.diff(f(y),y,2)],[-s.diff(f(y),y,2),s.diff(f(y),y,2)-(x-y)*s.diff(f(y),y,3)]])
checks=0
def check(label,condition):
 global checks
 if not condition: raise AssertionError(label)
 checks+=1
 print('PASS',label)
check('C3 Hessian identity',s.simplify(H-expected)==s.zeros(2))
hx,hy,hpy=s.symbols('hx hy hpy',positive=True)
det=s.Matrix([[hx,-hy],[-hy,hy-(x-y)*hpy]]).det()
check('determinant reciprocal tangent identity',s.simplify(det/(hx*hy**2)-(1/hy-(x-y)*hpy/hy**2-1/hx))==0)
M=s.Matrix([[1,1,0],[0,0,1]])
R=s.Rational

def divergence(p,q,mu,phi):
 d=s.diff(phi,x)
 return s.simplify(sum(m*(phi.subs(x,a/m)-phi.subs(x,b/m)-d.subs(x,b/m)*(a-b)/m) for a,b,m in zip(p,q,mu)))
def gap(p,q,mu,phi,K=M):
 return s.simplify(divergence(p,q,mu,phi)-divergence(K*p,K*q,K*mu,phi))
mu=s.Matrix([1,1,1]);p=s.Matrix([R(19,100),R(1,100),R(4,5)]);q=s.Matrix([R(31,100),R(29,100),R(2,5)])
check('t4 inherited coarse increase',gap(p,q,mu,x**4)==-R(921,1562500))
mu=s.Matrix([R(1,16),R(1,16),1]);p=s.Matrix([R(1,4),R(1,16),R(11,16)]);q=s.Matrix([R(1,16),R(1,16),R(7,8)])
check('interior-power exact radical gap',gap(p,q,mu,x**R(3,2))==(18-5*s.sqrt(10))/32)
check('radical gap strictly positive',18**2>25*10)
lam,eps,x1,x2,y1,y2=s.symbols('lam eps x1 x2 y1 y2',positive=True)
X=lam*x1+(1-lam)*x2;Y=lam*y1+(1-lam)*y2
mu=s.Matrix([eps*lam,eps*(1-lam),1]);p=s.Matrix([eps*lam*x1,eps*(1-lam)*x2,1-eps*X]);q=s.Matrix([eps*lam*y1,eps*(1-lam)*y2,1-eps*Y])
check('buffer laws normalized',s.simplify(sum(p))==s.simplify(sum(q))==1)
check('merge recovers arbitrary convex combination',s.simplify((M*mu)[0]-eps)==0 and s.simplify((M*p)[0]/eps-X)==0 and s.simplify((M*q)[0]/eps-Y)==0)
# Independent polynomial control of exact buffer cancellation.
scalar=lambda a,b:s.expand(a**4-b**4-4*b**3*(a-b))
check('necessity cancellation exact',s.simplify(gap(p,q,mu,x**4)-eps*(lam*scalar(x1,y1)+(1-lam)*scalar(x2,y2)-scalar(X,Y)))==0)
K=s.Matrix([[1,1,0,0],[0,0,1,0],[0,0,0,1]])
p=s.Matrix([R(1,8),R(1,8),R(1,4),R(1,2)]);q=s.Matrix([R(1,8),R(1,8),R(1,2),R(1,4)]);mu=s.Matrix([R(1,8),R(3,8),R(1,4),R(1,4)])
A=s.Matrix.hstack(p,q,mu);B=K*A
check('recovery witness normalized and positive',sum(p)==sum(q)==sum(mu)==1 and all(a>0 for a in A))
check('coarse three-column determinant',B.det()==-R(1,16))
reverse=A*B.inv()
expected=s.Matrix([[R(1,8),R(1,8),R(1,8)],[R(7,8),-R(1,8),-R(1,8)],[0,1,0],[0,0,1]])
check('unique simultaneous linear reverse',reverse==expected and reverse*B==A)
check('no stochastic simultaneous reverse',any(a<0 for a in reverse))
for name,phi in [('quadratic',x*x/2),('entropy',x*s.log(x)),('interior power',x**R(3,2)),('quartic',x**4)]:
 check(name+' equality without recovery',gap(p,q,mu,phi,K)==0)
 check(name+' positive fine divergence',divergence(p,q,mu,phi)>0)
# Row equality contrasts; positive scalar pairs suffice for these row controls.
def jgap(phi,a,b,c,d):
 def bb(u,v):return phi.subs(x,u)-phi.subs(x,v)-s.diff(phi,x).subs(x,v)*(u-v)
 return s.simplify((bb(a,b)+bb(c,d))/2-bb((a+c)/2,(b+d)/2))
check('quadratic equal differences',jgap(x*x/2,s.Integer(2),s.Integer(1),s.Integer(3),s.Integer(2))==0)
check('entropy equal ratios',jgap(x*s.log(x),s.Integer(2),s.Integer(1),s.Integer(4),s.Integer(2)).equals(0))
check('interior power diagonal equality',jgap(x**R(3,2),s.Integer(1),s.Integer(1),s.Integer(2),s.Integer(2))==0)
mu=s.Matrix([1,1,1]);p=s.Matrix([R(4,10),R(3,10),R(3,10)]);q=s.Matrix([R(3,10),R(2,10),R(5,10)])
A=s.Matrix.hstack(p,q);B=M*A
check('quadratic pair-loss equal divergence',gap(p,q,mu,x*x/2)==0 and divergence(p,q,mu,x*x/2)==R(3,100))
check('quadratic coarse pair invertible',B.det()==R(1,5))
check('quadratic no pair reverse',A*B.inv()==s.Matrix([[R(11,20),R(1,20)],[R(9,20),-R(1,20)],[0,1]]))
print(f'ALL {checks} EXACT CHECKS PASSED')
