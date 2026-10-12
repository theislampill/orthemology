#!/usr/bin/env python3
"""Finite exact controls for the written energy-controlled reverse lift.

Does not formally verify the analytic/measure theorem. Reads old inputs only.
"""
import hashlib,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
checks=[]

def zero(name,expr):
    value=s.simplify(s.cancel(expr))
    assert value==0,(name,value)
    checks.append(name)

def true(name,condition):
    assert bool(condition),name
    checks.append(name)

for path,digest in json.loads((HERE/'INPUT_BINDINGS.json').read_text()).items():
    true('input preserved: '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest)

# SOS power comparison, with nonnegative factors supplied by the theorem.
h,r,c=s.symbols('h r c',real=True)
for n in range(1,13):
    zero(f'power difference factorization n={n}',h**(2*n)-(c*r)**n-(h*h-c*r)*sum(h**(2*(n-1-j))*(c*r)**j for j in range(n)))
for d in (1,2,3):
    xs=s.symbols('x0:'+str(d),real=True)
    R=sum(x*x for x in xs)
    for n in range(1,9):
        for i,x in enumerate(xs):
            coeffs=s.Poly(s.expand(R**n-x**(2*n)),*xs).terms()
            true(f'marginal difference SOS d={d},n={n},i={i}',all(co>=0 and all(e%2==0 for e in mon) for mon,co in coeffs))

# Nested integrations preserve the simplex factor 1/n!, unlike the radial proof.
t,u=s.symbols('t u',positive=True)
volume=s.Integer(1)
for n in range(1,13):
    volume=s.integrate(volume.subs(t,u),(u,0,t))
    zero(f'nested energy simplex n={n}',volume-t**n/s.factorial(n))
    zero(f'factorial resulting moment bound n={n}',1/(volume/t**n)-s.factorial(n))
    true(f'Carleman factorial elementary bound n={n}',s.factorial(2*n)<=(2*n)**(2*n))

# Faithful recurrences for several polynomial energies and vector fields.
x,y,z=s.symbols('x y z',real=True)
examples=[]
for d in (1,2,3):
    xs=(x,y,z)[:d];R=sum(v*v for v in xs)
    for label,F in [('quadratic',R),('quartic',R**2/4),('multiwell',(R-1)**2/4)]:
        H=F+1;b=[-s.diff(H,v) for v in xs]
        examples.append((f'{label},d={d}',xs,H,b))
F=(x-y*y)**2+y*y
examples.append(('curved valley',(x,y),F+1,[-s.diff(F,x),-s.diff(F,y)]))
examples.append(('factored mobility',(x,),1+x*x/2,[-x*(1+x*x)]))
examples.append(('rotation',(x,y),1+x*x+y*y,[-y,x]))
for label,xs,H,b in examples:
    S=-sum(bi*s.diff(H,xi) for bi,xi in zip(b,xs))
    for n in range(0,6):
        p=H**n
        actual=sum(bi*s.diff(p,xi) for bi,xi in zip(b,xs))-H*p
        expected=-H**(n+1) if n==0 else -n*H**(n-1)*S-H**(n+1)
        zero(f'energy recurrence {label},n={n}',actual-expected)

# Curved valley certificate: two independent exact SOS decompositions.
u=x-y*y;F=u*u+y*y;H=F+1;R=x*x+y*y
SOS=1+u**4+u*u+2*y*y*(u-s.Rational(1,2))**2+y*y/2
zero('curved valley displayed SOS',H*H-R-SOS)
zero('curved valley rational-square alternative',H*H-R-(1+u**4+u*u+(u*y)**2+((u-1)*y)**2))
radial=x*s.diff(F,x)+y*s.diff(F,y)
zero('curved valley radial expression',radial-(2*u*u-2*u*y*y+2*y*y))
zero('curved valley u=2 outward curve',radial.subs(x,y*y+2)-(8-2*y*y))
zero('curved valley scaled outward curve',radial.subs(x,3*y*y/2)-(-y**4/2+2*y*y))
k,lam,D,C=s.symbols('k lam D C',real=True)
old=(radial-k*R**2+lam*R+D).subs(x,y*y+2)
zero('old radial certificate negative leading coefficient',s.Poly(s.expand(old),y).LC()+k)
true('old radial certificate degree eight',s.Poly(s.expand(old),y).degree()==8)
linear=(F+C-c*R).subs(x,y*y)
zero('linear energy domination fails leading coefficient',s.Poly(s.expand(linear),y).LC()+c)
true('linear energy domination fails degree four',s.Poly(s.expand(linear),y).degree()==4)
for m in range(3,8):
    valley=(y*y+C)**2-c*(y**(2*m)+y*y)
    zero(f'future polynomial-coordinate route excluded m={m}',s.Poly(s.expand(valley),y).LC()+c)
    true(f'future polynomial-coordinate route leading degree m={m}',s.Poly(s.expand(valley),y).degree()==2*m)

# Cutoff cancellation is exact; derivatives of U do not survive globally.
for d in (1,2,3):
    xs=(x,y,z)[:d]
    chi=s.Function('chi')(*xs); U=s.Function('U')(t,*xs)
    bs=[s.Function('b'+str(i))(*xs) for i in range(d)]
    Hfun=s.Function('H')(*xs)
    op=lambda p:s.diff(p,t)+sum(bi*s.diff(p,xi) for bi,xi in zip(bs,xs))-Hfun*p
    zero(f'cutoff exact cancellation d={d}',op(chi*U)-chi*op(U)-U*sum(bi*s.diff(chi,xi) for bi,xi in zip(bs,xs)))
    for m in range(0,8):
        q=2*((m+2)//2+1)
        true(f'cutoff polynomial tail exponent d={d},m={m}',q>m+1 and m-q-1<0)

# Quotient unnormalization cancels the additive constant.
a,Lp,LF,LG,C=s.symbols('a Lp LF LG C',real=True)
zero('shifted unnormalization',( -(LF+C)*a*Lp+a*(LG-LF*Lp+LF*Lp) ) - a*(LG-(LF+C)*Lp))
# Direct quotient derivative: nu'=transport-killing and a'=-a L(H).
P,V,W,A=s.symbols('P V W A',real=True)
zero('normalized quotient generator',(V*A+P*W)/A**2-(V/A+(W/A)*(P/A)))

# General drift / polynomial mobility S certificate.
M=s.Matrix([[1+x*x,x*y],[x*y,1+y*y]])
B=s.Matrix([[1,0],[0,1],[x,y]])
for i in range(2):
    for j in range(2): zero(f'matrix factorization entry {i},{j}',(B.T*B-M)[i,j])
g=s.Matrix([2*x,4*y**3]);bb=-M*g
zero('mobility energy SOS',-(bb.dot(g))-(B*g).dot(B*g))
rotH=1+x*x+y*y
zero('rotation S zero',-(-y*s.diff(rotH,x)+x*s.diff(rotH,y)))
zero('rotation radial certificate',rotH**2-(x*x+y*y)-(1+(x*x+y*y)+(x*x+y*y)**2))

# Finite metric pairings and cometric, tested with symbolic finite weights.
w1,w2=s.symbols('w1 w2',positive=True)
u1=s.symbols('u1',real=True)
f1,f2,p1,p2,q1,q2=s.symbols('f1 f2 p1 p2 q1 q2',real=True)
w=[w1,1-w1];f=[f1,f2];p=[p1,p2];qq=[q1,q2]
E=sum(wi*fi for wi,fi in zip(w,f))
zero('finite metric weight gradient pairing',sum(ui*(fi-E) for ui,fi in zip([u1,-u1],f))-u1*(f1-f2))
Lp=sum(wi*pi for wi,pi in zip(w,p));Lq=sum(wi*qi for wi,qi in zip(w,qq))
zero('finite moment cometric covariance',sum(wi*(pi-Lp)*(qi-Lq) for wi,pi,qi in zip(w,p,qq))-(sum(wi*pi*qi for wi,pi,qi in zip(w,p,qq))-Lp*Lq))
v=s.Matrix(s.symbols('v0:2'));gp=s.Matrix(s.symbols('gp0:2'));gq=s.Matrix(s.symbols('gq0:2'))
zero('metric mobility gradient cancellation',(M*gp).dot(M.inv()*v)-gp.dot(v))
zero('metric mobility cometric',(M*gp).dot(M.inv()*M*gq)-gp.dot(M*gq))

# One-dimensional mobility flow and Hessian/Bregman realization.
q=s.symbols('q',positive=True)
D=1+z*z*(1-q)
X=z*s.sqrt(q)/s.sqrt(D)
zero('mobility flow ODE',-2*q*s.diff(X,q)+X*(1+X*X))
zero('mobility initial point',X.subs(q,1)-z)
zero('mobility integrated original killing',-2*q*s.diff(s.log(D)/4,q)-X*X/2)
EH=s.sqrt(q)*D**(-s.Rational(1,4))
zero('mobility shifted weight equation',-2*q*s.diff(EH,q)+(1+X*X/2)*EH)
zero('mobility weight initial',EH.subs(q,1)-1)
zero('mobility radius',X*X-z*z*q/D)
zero('mobility image positive gap',q/(1-q)-X*X-q/((1-q)*D))
zero('mobility image finite endpoint limit',s.limit(X*X,z,s.oo)-q/(1-q))
psi=x*s.atan(x)-s.log(1+x*x)/2
zero('Hessian potential first derivative',s.diff(psi,x)-s.atan(x))
zero('Hessian potential second derivative',s.diff(psi,x,2)-1/(1+x*x))
zero('geodesic coordinate derivative',s.diff(s.asinh(x),x)-1/s.sqrt(1+x*x))
zero('dual coordinate motion',s.diff(s.atan(x),x)*(-x*(1+x*x))+x)
zero('sine dual coordinate motion',s.diff(x/s.sqrt(1+x*x),x)*(-x*(1+x*x))+x/s.sqrt(1+x*x))
zero('mobility SOS energy certificate',(1+x*x/2)**2-x*x-(1+x**4/4))
zero('mobility dissipation certificate',x*x*(1+x*x)-(x*x+x**4))

# Lower energy killing and full-support affine scope control.
R=s.symbols('R',nonnegative=True)
zero('quadratic full-support certificate',(1+R)**2-R-(1+R+R*R))
q=s.symbols('q',positive=True)
zero('quadratic linear flow ODE',s.diff(z*s.exp(-2*t),t)+2*z*s.exp(-2*t))
zero('quadratic inverse map',(z*s.exp(-2*t))*s.exp(2*t)-z)

# Exponential tails alone do not justify all-frequency Taylor passage.
xi=s.symbols('xi',real=True)
for n in range(1,9):
    val=s.integrate(x**(2*n)*s.exp(-x),(x,0,s.oo))
    zero(f'Laplace even moment factorial n={n}',val-s.factorial(2*n))
    true(f'Laplace Taylor at frequency two diverges n={n}',4**n>4**(n-1))
for N in range(0,8):
    partial=sum((-xi*xi)**j for j in range(N+1))
    zero(f'Laplace Fourier Taylor residual N={N}',1/(1+xi*xi)-partial-(-xi*xi)**(N+1)/(1+xi*xi))

result={'status':'passed','checks':len(checks),'limits':'Finite exact controls supplement the written universal proof; no formal-kernel or measure-reconstruction claim.','names':checks}
(HERE/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
