#!/usr/bin/env python3
"""Exact finite algebraic controls, not a proof of the analytic theorem."""
from pathlib import Path
from fractions import Fraction
import hashlib, json, math, sys
import sympy as s

ROOT=Path(__file__).resolve().parent
checks=[]
def check(name, condition):
    if condition is not True and condition != s.true:
        raise AssertionError(name + ': ' + repr(condition))
    checks.append(name)
def zero(name, expr):
    check(name, s.expand(expr)==0)

for row in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    blob=(ROOT/row['snapshot']).read_bytes()
    check('snapshot hash '+row['source'], hashlib.sha256(blob).hexdigest()==row['sha256'])
    current=ROOT.parent/row['source']
    check('unchanged inherited '+row['source'], hashlib.sha256(current.read_bytes()).hexdigest()==row['sha256'])

for row in json.loads((ROOT/'SOURCE_MANIFEST.json').read_text()):
    source=ROOT/row['local_file']
    check('source hash '+row['version'],hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'])

# Actual multivariate polynomial identities, including the n=1 edge.
for d in range(1,5):
    x=s.symbols('x:'+str(d)); R=sum(z*z for z in x)
    for n in range(1,7):
        zero(f'radial Laplacian d={d},n={n}',sum(s.diff(R**n,z,2) for z in x)-2*n*(2*n+d-2)*R**(n-1))
        for z in x:
            coeffs=s.Poly(s.expand(R**n-z**(2*n)),*x).terms()
            check(f'radial marginal SOS d={d},n={n},z={z}',all(c>=0 and all(k%2==0 for k in powers) for powers,c in coeffs))
    for k in range(1,5):
        f=[z*R**(k-1) for z in x]; g=[z*R**k for z in x]
        zero(f'even CS left d={d},k={k}',sum(z*z for z in f)-R**(2*k-1))
        zero(f'even CS middle d={d},k={k}',sum(z*w for z,w in zip(f,g))-R**(2*k))
        zero(f'even CS right d={d},k={k}',sum(z*z for z in g)-R**(2*k+1))
    for k in range(0,5):
        zero(f'odd CS middle d={d},k={k}',R**k*R**(k+1)-R**(2*k+1))

# Rational radial measures are controls only, never the general existence proof.
for atoms,weights in [([0,1,3],[Fraction(1,5),Fraction(1,7),Fraction(1,9)]),([2,5],[Fraction(1,3),Fraction(1,3)]),([0],[Fraction(1)]),([7],[Fraction(1,2)])]:
    a=[sum(w*r**n for r,w in zip(atoms,weights)) for n in range(13)]
    for n in range(1,11):
        label=f'{atoms},n={n}'
        check('rational logconvex '+label,a[n]**2<=a[n-1]*a[n+1])
        check('rational lower interpolation '+label,a[n-1]**n<=a[0]*a[n]**(n-1))
        check('rational upper interpolation '+label,a[n]**(n+1)<=a[0]*a[n+1]**n)

# Riccati envelope and scalar monotonicity identities.
t,k,n=s.symbols('t k n',positive=True)
U=k*s.coth(k*t/n)
check('Riccati coth identity',s.simplify(s.diff(U,t)-(k*k-U*U)/n)==0)
w=s.symbols('w',real=True)
check('coth monotonic numerator derivative',s.simplify(s.diff(s.sinh(w)*s.cosh(w)-w,w)-2*s.sinh(w)**2)==0)
for d in range(1,13):
    for m in range(1,31):
        check(f'M bound d={d},n={m}',Fraction(2*m*(2*m+d-2),m*m)<=max(4,2*d))

# Fourier Mehler PDE with c^2+v^2=1, keeping all independent geometric terms.
d,v,c,Y,X,Z=s.symbols('d v c Y X Z',real=True)
# Y=|y|^2, X=|xi|^2, Z=xi.y. Compare logarithmic time and space derivatives.
time_log=-d*v-c*c*(Y+X)-2*s.I*c*v*Z
space_ratio=-d*v+v*v*X-2*s.I*v*c*Z-c*c*Y-X
zero('Fourier Mehler PDE modulo c2+v2',s.rem(s.Poly(time_log-space_ratio,c),s.Poly(c*c+v*v-1,c)).as_expr())
# Maximum-principle barrier divided by its positive prefactor.
r=s.symbols('r',nonnegative=True)
zero('quadratic barrier residual',2*d*(1+r)-2*d+r*(1+r)-((2*d+1)*r+r*r))

# Mehler density PDE in one dimension, via logarithmic derivatives.
u,w,x,y=s.symbols('u w x y',real=True)
# u=sinh(2t), w=cosh(2t), u'=2w,w'=2u.
time_density=-w/u+(x*x+y*y-2*w*x*y)/u**2
space_density=-w/u+(-w*x+y)**2/u**2-x*x
num=s.together(time_density-space_density)*u*u
zero('density Mehler PDE modulo w2-u2',s.rem(s.Poly(s.expand(num),w),s.Poly(w*w-u*u-1,w)).as_expr())
# Completing the square for the conditional Gaussian, denominator identities excluded from source assumptions.
zero('Gaussian square-completion exponent',s.expand((w*(x*x+y*y)-2*x*y)*w-(w*x-y)**2-u*u*y*y).subs(w*w,u*u+1))

# One-dimensional Gaussian monomial moments and exact semigroup recurrence.
c,v,y=s.symbols('c v y',real=True)
def Q(m):
    if m<0:return s.Integer(0)
    return sum(s.factorial(m)/(s.factorial(m-2*j)*2**j*s.factorial(j))*(c*y)**(m-2*j)*v**j for j in range(m//2+1))
for m in range(17):
    q=Q(m)
    dt=(-v-c*c*y*y)*q-2*c*v*s.diff(q,c)+2*c*c*s.diff(q,v)
    generator=m*(m-1)*Q(m-2)-Q(m+2)
    rem=s.rem(s.Poly(s.expand(dt-generator),c),s.Poly(c*c+v*v-1,c)).as_expr()
    zero(f'Gaussian monomial evolution degree={m}',rem)
    zero(f'Gaussian origin monomial degree={m}',q.subs({c:1,v:0})-y**m)

# Exact failed transplant for actual delta_0 initial data, arbitrary d.
d=s.symbols('d',positive=True,integer=True)
# A'_0(R)=A_0(2d-R^2)=2d, A''_0(1)=A_0(R^2-2d)=-2d.
zero('failed radial monotonicity delta0',2*d-2*d)
check('failed radial monotonicity is positive',(2*d).is_positive)
check('failed even derivative is negative',(-2*d).is_negative)

result={'status':'passed','exact_checks':len(checks),'python':sys.version.split()[0],'sympy':s.__version__,'checks':checks,'scope':'Finite exact algebraic controls only; not a formal proof or universal analytic verification.'}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checks)} exact controls')
print(result['scope'])
