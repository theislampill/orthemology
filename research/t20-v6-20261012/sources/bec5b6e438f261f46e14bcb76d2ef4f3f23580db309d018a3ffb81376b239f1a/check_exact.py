#!/usr/bin/env python3
"""Finite exact controls supplementing an unrestricted-rank written proof.

No old input is written. Does not establish measure existence by enumeration.
"""
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
checks=[]

def zero(name,expr):
    value=s.simplify(s.cancel(expr))
    assert value==0,(name,value)
    checks.append(name)

def true(name,condition):
    assert bool(condition),name
    checks.append(name)

bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for p,h in bindings.items():
    true('input unchanged: '+p,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)

k,l,D,C=s.symbols('k l D C', positive=True)
# Exact generator decomposition for representative radial/nonradial potentials.
for d in (1,2,3):
    xs=s.symbols('x0:'+str(d),real=True)
    R=sum(x*x for x in xs)
    Fs=[R**2/4,(R-1)**2/4,(R-1)**2/4+xs[0]**2/2]
    for fi,F in enumerate(Fs):
        b=[-s.diff(F,x) for x in xs]
        xgrad=sum(x*s.diff(F,x) for x in xs)
        Q=xgrad-k*R**2+l*R+D
        V=F+C
        for n in range(1,7):
            p=R**n
            Gp=sum(bi*s.diff(p,x) for bi,x in zip(b,xs))-V*p
            expected=2*n*D*R**(n-1)+2*l*n*R**n-2*k*n*R**(n+1)-2*n*R**(n-1)*Q-V*R**n
            zero(f'generator-certificate decomposition d={d},F={fi},n={n}',Gp-expected)
        zero(f'gradient energy identity d={d},F={fi}',sum(bi*s.diff(F,x) for bi,x in zip(b,xs))+sum(s.diff(F,x)**2 for x in xs))
    for n in range(1,7):
        if n%2:
            j=(n-1)//2
            f,g=R**j,R**(j+1)
            zero(f'odd CS lower d={d},n={n}',f*f-R**(n-1))
            zero(f'odd CS centre d={d},n={n}',f*g-R**n)
            zero(f'odd CS upper d={d},n={n}',g*g-R**(n+1))
        else:
            j=n//2
            fs=[x*R**(j-1) for x in xs]
            gs=[x*R**j for x in xs]
            zero(f'even CS lower d={d},n={n}',sum(f*f for f in fs)-R**(n-1))
            zero(f'even CS centre d={d},n={n}',sum(f*g for f,g in zip(fs,gs))-R**n)
            zero(f'even CS upper d={d},n={n}',sum(g*g for g in gs)-R**(n+1))
        for i,x in enumerate(xs):
            p=s.Poly(s.expand(R**n-x**(2*n)),*xs)
            true(f'marginal difference SOS d={d},n={n},i={i}',all(c>=0 and all(e%2==0 for e in mon) for mon,c in p.terms()))

# General Riccati formula using its two roots, avoiding hyperbolic simplifier heuristics.
a,be,r,q=s.symbols('alpha beta r q',real=True)
den=(r-be)-(r-a)*q
num=a*(r-be)-be*(r-a)*q
y=num/den
Y=(a-be*q)/(1-q)
# Δ=k(alpha-beta); f(z)=-2k(z-alpha)(z-beta).
zero('finite Riccati initial datum',y.subs(q,1)-r)
zero('finite Riccati ODE',-2*k*(a-be)*q*s.diff(y,q)+2*k*(y-a)*(y-be))
zero('infinite envelope ODE',-2*k*(a-be)*q*s.diff(Y,q)+2*k*(Y-a)*(Y-be))
zero('strict envelope gap',Y-y-(a-be)**2*q/((1-q)*den))
zero('finite denominator positive decomposition',den-((r-be)*(1-q)+(a-be)*q))
zero('infinite initial limit',s.limit(y,r,s.oo)-Y)
zero('zero initial nonnegative flow formula',y.subs(r,0)-a*be*(q-1)/(-be+a*q))
Delta=s.symbols('Delta',positive=True)
alpha=(l+Delta)/(2*k); beta=(l-Delta)/(2*k)
zero('Riccati sum of roots',alpha+beta-l/k)
zero('Riccati product with discriminant',((alpha*beta+D/k)*4*k*k).subs(Delta**2,l*l+4*k*D))
z=s.symbols('z',real=True)
zero('root-factor coefficient identity',(-2*k*(z-alpha)*(z-beta)-(2*D+2*l*z-2*k*z*z)).subs(Delta**2,l*l+4*k*D))
t=s.symbols('t',positive=True)
Y_h=(l+Delta*(1+s.exp(-2*Delta*t))/(1-s.exp(-2*Delta*t)))/(2*k)
zero('coth exponential envelope',Y.subs({a:alpha,be:beta,q:s.exp(-2*Delta*t)})-Y_h)
zero('D zero lambda positive envelope',Y_h.subs(Delta,l)-l/(k*(1-s.exp(-2*l*t))))
Y0=1/(2*k*t); y0=r/(1+2*k*r*t)
zero('zero-discriminant envelope ODE',s.diff(Y0,t)+2*k*Y0**2)
zero('zero-discriminant finite ODE',s.diff(y0,t)+2*k*y0**2)
zero('zero-discriminant strict gap',Y0-y0-1/(2*k*t*(1+2*k*r*t)))
zero('small lambda zero-D limit',s.limit(l/(k*(1-s.exp(-2*l*t))),l,0)-Y0)

# The narrow clock route is retained, not mistaken for the D>0 proof.
u=(s.exp(2*l*t)-1)/(2*l)
zero('clock derivative',s.diff(u,t)-s.exp(2*l*t))
zero('clock lambda zero limit',s.limit(u,l,0)-t)
zero('clock support envelope',s.exp(2*l*t)/(2*k*u)-l/(k*(1-s.exp(-2*l*t))))
for n in range(1,13):
    zero(f'clock recurrence coefficient n={n}',s.exp(-2*l*n*t)*s.exp(2*l*(n+1)*t)/s.exp(2*l*t)-1)
    zero(f'simplex factorial cancellation n={n}',s.prod(2*k*j for j in range(1,n))*u**(n-1)/s.factorial(n-1)-(2*k*u)**(n-1))
    zero(f'clock moment bound rewrite n={n}',s.exp(2*l*n*t)*(2*k*u)**(1-n)-s.exp(2*l*t)*(s.exp(2*l*t)/(2*k*u))**(n-1))

# Main multiwell exact flow. Use z=e^(2t) for exact rational identities.
z,v=s.symbols('z v',positive=True)
r=s.symbols('r',nonnegative=True)
H=1+(z-1)*r
rt=z*r/H
scale2=z/H
K=t/4-s.log(H)/8-(rt-r)/8
Dt=lambda expression: s.diff(expression,t)+2*z*s.diff(expression,z)
zero('multiwell radius ODE',Dt(rt)-2*rt+2*rt**2)
zero('multiwell coordinate log scale ODE',z*s.diff(s.log(scale2),z)-(1-rt))
zero('multiwell killing derivative',Dt(K)-(rt-1)**2/4)
zero('multiwell initial radius',rt.subs(z,1)-r)
zero('multiwell initial scale',scale2.subs(z,1)-1)
zero('multiwell initial killing',K.subs({t:0,z:1}))
zero('multiwell origin killing',K.subs(r,0)-t/4)
zero('multiwell well radius',rt.subs(r,1)-1)
zero('multiwell well killing',K.subs(r,1).subs(z,s.exp(2*t)))
rv=v*r/(1+(v-1)*r)
zero('multiwell radial cocycle',rt.subs(r,rv)-rt.subs(z,z*v))
zero('multiwell squared scale cocycle',(v/(1+(v-1)*r))*scale2.subs(r,rv)-scale2.subs(z,z*v))
zero('multiwell killing log argument cocycle',(1+(v-1)*r)*H.subs(r,rv)-(1+(z*v-1)*r))
zero('multiwell killing radius increment cocycle',(rv-r)+(rt.subs(r,rv)-rv)-(rt.subs(z,z*v)-r))
cap=z/(z-1)
zero('multiwell strict cap gap',cap-rt-z/((z-1)*H))
q=s.symbols('q',nonnegative=True)
inv_r=q/(z-(z-1)*q)
zero('multiwell inverse radius after forward',inv_r.subs(q,rt)-r)
zero('multiwell forward radius after inverse',rt.subs(r,inv_r)-q)
zero('multiwell coordinate inverse squared',scale2/(z-(z-1)*rt)-1)

# Backward semigroup cancellation for a symbolic homogeneous polynomial degree.
m=s.symbols('m',integer=True,nonnegative=True)
logh=m*s.log(scale2)/2-K
h_t=Dt(logh)
h_r=s.diff(logh,r)
expected=m*(1-r)+2*r*(1-r)*h_r-(r-1)**2/4
zero('multiwell symbolic homogeneous backward generator',h_t-expected)

# SOS, nonconvexity and zero-moment branch discriminators.
x=s.symbols('x',real=True)
F=(x*x-1)**2/4
zero('multiwell scalar dissipativity certificate',x*s.diff(F,x)-x**4+x*x)
zero('multiwell negative Hessian at origin',s.diff(F,x,2).subs(x,0)+1)
true('multiwell nonminimizing stationary origin',F.subs(x,0)>F.subs(x,1))
for point in (-1,0,1):
    zero(f'multiwell stationary point x={point}',s.diff(F,x).subs(x,point))
shift=(x-1)**4/4
Q=x*s.diff(shift,x)-x**4/4+x*x+s.Rational(1,4)
zero('shifted D positive SOS certificate',Q-s.Rational(3,4)*(x*x-2*x)**2-(x-s.Rational(1,2))**2)
zero('shifted origin gradient is nonzero',s.diff(shift,x).subs(x,0)+1)
phi=1+(x-1)/s.sqrt(1+2*t*(x-1)**2)
zero('shifted coordinate flow ODE',s.diff(phi,t)+(phi-1)**3)
zero('shifted initial flow',phi.subs(t,0)-x)
zero('shifted origin moves with unit initial velocity',s.diff(phi,t).subs({x:0,t:0})-1)
for n in range(1,7):
    zero(f'shifted initial radial moment zero n={n}',(phi**(2*n)).subs({x:0,t:0}))
    true(f'shifted later radius positive n={n}',(1-1/s.sqrt(3))**(2*n)>0)
x1,x2=s.symbols('x1 x2',real=True)
R=x1*x1+x2*x2
F=(R-1)**2/4+x1*x1/2
zero('nonradial SOS certificate',x1*s.diff(F,x1)+x2*s.diff(F,x2)-R**2+R-x1*x1)
zero('nonradial potential explicit SOS',F-((R-1)/2)**2-x1*x1/2)
for point in ((0,-1),(0,1)):
    zero('nonradial minimum '+str(point),F.subs({x1:point[0],x2:point[1]}))

# Finite-law normalization including constant-shift cancellation.
w1,w2,p1,p2,c1,c2,k1,k2=s.symbols('w1 w2 p1 p2 c1 c2 k1 k2',real=True)
Z=w1+w2; N=w1*p1+w2*p2
Np=w1*(c1-(k1+C)*p1)+w2*(c2-(k2+C)*p2)
Zp=-w1*(k1+C)-w2*(k2+C)
actual=(Np*Z-N*Zp)/Z**2
expected=(w1*c1+w2*c2)/Z-(w1*k1*p1+w2*k2*p2)/Z+(w1*k1+w2*k2)*N/Z**2
zero('normalized two-atom C cancellation',actual-expected)
E1,E2,a,b=s.symbols('E1 E2 a b',positive=True)
out1=a*E1/(a*E1+b*E2); out2=b*E2/(a*E1+b*E2)
zero('inverse positive weight normalization',(out1/E1)/(out1/E1+out2/E2)-a/(a+b))

result={'status':'PASS','exact_check_count':len(checks),'checks':checks,'inputs_preserved':True,
        'scope':'Finite exact algebra supplements the written universal proof. No kernel verification, numerical sampling, protected change, integration, review verdict, or closure claim.'}
(HERE/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
