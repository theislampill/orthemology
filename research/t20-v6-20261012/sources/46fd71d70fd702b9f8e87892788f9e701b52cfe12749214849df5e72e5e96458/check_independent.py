#!/usr/bin/env python3
"""Independent exact finite controls; not a proof of the universal theorem."""
import hashlib, json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
results=[]

def zero(name, expression):
    value=s.factor(s.together(expression))
    assert value==0, (name, str(value))
    results.append({'name':name,'status':'pass'})

def nonzero(name, expression):
    value=s.factor(s.together(expression))
    assert value!=0, (name, str(value))
    results.append({'name':name,'status':'pass','nonzero_residual':str(value)})

# Algebra of the full SOS radial drift inequality, independently derived.
n=s.symbols('n', integer=True, positive=True)
r, V, Q=s.symbols('r V Q', positive=True)
k, lam, D=s.symbols('kappa lambda D', positive=True)
C=s.symbols('C', nonnegative=True)
xgrad=Q+k*r**2-lam*r-D
gen=-2*n*r**(n-1)*xgrad-V*r**n
upper=2*n*D*r**(n-1)+2*lam*n*r**n-2*k*n*r**(n+1)
zero('SOS generator deficit',gen-upper+2*n*r**(n-1)*Q+V*r**n)
nonzero('reject missing factor two in inward drift',gen-(2*n*D*r**(n-1)+2*lam*n*r**n-k*n*r**(n+1))+2*n*r**(n-1)*Q+V*r**n)
nonzero('reject dropping positive D contribution',gen-(2*lam*n*r**n-2*k*n*r**(n+1))+2*n*r**(n-1)*Q+V*r**n)

# Check multivariate Euler and log-convexity inner-product identities.
for dim in (1,2,3):
    xs=s.symbols('x0:'+str(dim))
    R=sum(x*x for x in xs)
    F=sum(x**6/s.Integer(6)+x**4/s.Integer(4) for x in xs)+sum(xs)**2
    xF=sum(x*s.diff(F,x) for x in xs)
    for j in range(1,7):
        lhs=-sum(s.diff(F,x)*s.diff(R**j,x) for x in xs)-(F+C)*R**j
        rhs=-2*j*R**(j-1)*xF-(F+C)*R**j
        zero(f'gradient radial recurrence d={dim} n={j}',lhs-rhs)
        if j%2:
            h=(j-1)//2
            f,g=R**h,R**(h+1)
            zero(f'odd CS product d={dim} n={j}',f*g-R**j)
            zero(f'odd CS lower d={dim} n={j}',f*f-R**(j-1))
            zero(f'odd CS upper d={dim} n={j}',g*g-R**(j+1))
        else:
            h=j//2
            fs=[x*R**(h-1) for x in xs]
            gs=[x*R**h for x in xs]
            zero(f'even CS product d={dim} n={j}',sum(f*g for f,g in zip(fs,gs))-R**j)
            zero(f'even CS lower d={dim} n={j}',sum(f*f for f in fs)-R**(j-1))
            zero(f'even CS upper d={dim} n={j}',sum(g*g for g in gs)-R**(j+1))

u=s.symbols('u', positive=True)
zero('positive-root Riccati cancellation',(2*n*D*u**(n-1)+2*lam*n*u**n-2*k*n*u**(n+1))/(n*u**(n-1))-(2*D+2*lam*u-2*k*u**2))

# Riccati flow uses h=tanh(delta*t), h'=delta*(1-h^2).
delta,h,y0=s.symbols('delta h y0', positive=True)
Dsub=(delta**2-lam**2)/(4*k)
den=delta+(2*k*y0-lam)*h
finite=(delta*y0+(lam*y0+2*Dsub)*h)/den
Y=(lam+delta/h)/(2*k)
zero('finite Riccati flow differential equation',s.diff(finite,h)*delta*(1-h**2)-(2*Dsub+2*lam*finite-2*k*finite**2))
zero('finite Riccati flow initial value',finite.subs(h,0)-y0)
zero('infinite-initial Riccati envelope',s.diff(Y,h)*delta*(1-h**2)-(2*Dsub+2*lam*Y-2*k*Y**2))
zero('strict envelope gap formula',Y-finite-delta**2*(1-h**2)/(2*k*h*den))
zero('envelope as initial value tends to infinity',s.limit(finite,y0,s.oo)-Y)
zero('envelope equilibrium root',(2*Dsub+2*lam*((lam+delta)/(2*k))-2*k*((lam+delta)/(2*k))**2))
nonzero('reject discriminant lambda squared plus 2 kappa D',(2*Dsub+2*lam*Y-2*k*Y**2)-s.diff(Y,h)*(s.sqrt(lam**2+2*k*Dsub))*(1-h**2))

t=s.symbols('t', positive=True)
Yzero=1/(2*k*t)
zero('zero-discriminant envelope',s.diff(Yzero,t)+2*k*Yzero**2)
finitezero=y0/(1+2*k*y0*t)
zero('zero-discriminant finite flow',s.diff(finitezero,t)+2*k*finitezero**2)
zero('zero-discriminant strict gap',Yzero-finitezero-1/(2*k*t*(1+2*k*y0*t)))

# The D=0 clock reduction and bound have the stated coefficient.
z=s.symbols('z', positive=True) # z = exp(2 lambda t)
clock=(z-1)/(2*lam)
B=lam*z/(k*(z-1))
zero('D-zero envelope equals clock bound',(lam+lam*(z+1)/(z-1))/(2*k)-B)
for j in range(1,9):
    zero(f'D-zero transformed geometric bound n={j}',z**j*(2*k*clock)**(1-j)-z*B**(j-1))
    zero(f'nested simplex factorial n={j}',s.prod(2*k*i for i in range(1,j))/s.factorial(j-1)-(2*k)**(j-1))
zero('D-zero B solves Riccati',s.diff(B,z)*(2*lam*z)-(2*lam*B-2*k*B**2))
nonzero('reject lost exponential prefactor',z**2/(2*k*clock)-B)

# Explicit shifted well requires the newly allowed constant D.
x=s.symbols('x', real=True)
Fshift=(x-1)**4/4
Qshift=x*s.diff(Fshift,x)-x**4/4+x**2+s.Rational(1,4)
zero('shifted well F SOS',Fshift-((x-1)**2/2)**2)
zero('shifted well radial SOS',Qshift-s.Rational(3,4)*(x*x-2*x)**2-(x-s.Rational(1,2))**2)
zero('shifted well nonstationary origin',s.diff(Fshift,x).subs(x,0)+1)
nonzero('D-zero obstruction linear coefficient',s.diff(x*s.diff(Fshift,x)-k*x**4+lam*x*x,x).subs(x,0))
phi=1+(x-1)/s.sqrt(1+2*t*(x-1)**2)
zero('shifted quartic characteristic equation',s.diff(phi,t)+(phi-1)**3)
zero('shifted quartic characteristic initial value',phi.subs(t,0)-x)
phi0=phi.subs(x,0)
zero('moving zero-atom initial position',phi0.subs(t,0))
zero('moving zero-atom initial velocity',s.diff(phi0,t).subs(t,0)-1)
zero('moving zero-atom radial derivative at zero',s.diff(phi0**2,t).subs(t,0))
zero('moving zero-atom radial second derivative',s.diff(phi0**2,t,2).subs(t,0)-2)

# Nonconvex sphere-well discriminator and exact logistic flow radius.
R=s.symbols('R', nonnegative=True)
Fm=(R-1)**2/4
zero('sphere well energy SOS',Fm-((R-1)/2)**2)
zero('sphere well radial certificate',2*R*s.diff(Fm,R)-R**2+R)
rflow=z*R/(1+(z-1)*R)
zero('sphere well logistic radius',s.diff(rflow,z)*2*z-2*rflow*(1-rflow))
zero('sphere well radius initial',rflow.subs(z,1)-R)
zero('stationary nonoptimal energy',Fm.subs(R,0)-s.Rational(1,4))
zero('sphere minimizer energy',Fm.subs(R,1))
nonzero('stationary origin excludes generic global optimality',Fm.subs(R,0)-Fm.subs(R,1))

# Independently check the multiwell killing formula and nonlinear image algebra.
H=1+(z-1)*R
K=s.log(z)/8-s.log(H)/8-(rflow-R)/8
zero('sphere well integrated killing derivative',2*z*s.diff(K,z)-(rflow-1)**2/4)
zero('sphere well killing initial value',K.subs(z,1))
zs,zt=s.symbols('zs zt', positive=True)
Hs=1+(zs-1)*R
rs=zs*R/Hs
Hts=1+(zt-1)*rs
zero('sphere well flow radius semigroup',zt*rs/Hts-zs*zt*R/(1+(zs*zt-1)*R))
zero('sphere well logarithmic cocycle factor',Hs*Hts-(1+(zs*zt-1)*R))
yR=s.symbols('yR', nonnegative=True)
rinverse=yR/(z-(z-1)*yR)
zero('sphere well inverse radial left identity',s.cancel(rinverse.subs(yR,rflow))-R)
zero('sphere well inverse radial right identity',s.cancel(rflow.subs(R,rinverse))-yR)
zero('sphere well image gap',z/(z-1)-rflow-z/((z-1)*H))
x1,x2=s.symbols('x1 x2', real=True)
R2=x1*x1+x2*x2
Fnr=(R2-1)**2/4+x1*x1/2
zero('nonradial explicit killing SOS',Fnr-((R2-1)/2)**2-x1*x1/2)
zero('nonradial radial certificate',x1*s.diff(Fnr,x1)+x2*s.diff(Fnr,x2)-R2**2+R2-x1*x1)

# Killing shifts cancel only after normalization, not in unnormalized mass.
Ap,AFp,LF,LV,LP,A1=s.symbols('Ap AFp LF LV LP A1')
zero('constant killing shift cancels in normalized hierarchy',(-AFp-C*Ap)/A1+(LF+C)*(Ap/A1)-(-AFp/A1+LF*Ap/A1))
Lgrad2,LF2=s.symbols('Lgrad2 LF2')
zero('gradient energy dissipation',(-Lgrad2-LF2+LF**2)-(-Lgrad2-(LF2-LF**2)))

# Replay inherited input preservation without modifying any old file.
for rel,want in json.loads((HERE/'ANCESTOR_PINS.json').read_text()).items():
    got=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
    assert got==want,(rel,want,got)
    results.append({'name':'ancestor unchanged: '+rel,'status':'pass'})

output={'status':'pass','scope':'Finite exact algebra and source preservation only; the universal analytical proof is reviewed in REVIEW.md.','sympy_version':s.__version__,'checks':len(results),'results':results}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
