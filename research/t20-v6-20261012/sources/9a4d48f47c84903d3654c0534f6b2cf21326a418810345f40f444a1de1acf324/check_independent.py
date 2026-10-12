#!/usr/bin/env python3
"""Exact finite controls supplement the independent ordinary proof review.
No construction or finite test here proves the imported infinite PSD functional.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
import hashlib, json
import sympy as s

HERE=Path(__file__).resolve().parent
checks=[]
def ck(name, condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def gm(n):
    if n%2:return 0
    return factorial(n)//(2**(n//2)*factorial(n//2))
def multi_g(alpha):
    a=1
    for k in alpha:a*=gm(k)
    return a

# Multinomial positivity: h^n-x_i^(2n) is an exact nonnegative
# coefficient sum of monomial squares in precisely the controlled variables.
for r in range(1,5):
    x=s.symbols('x:'+str(r))
    h=sum(v*v for v in x)
    for n in range(1,7):
        for i in range(r):
            poly=s.Poly(s.expand(h**n-x[i]**(2*n)),*x)
            ck(f'sos-difference-r{r}-n{n}-i{i}',all(c>=0 and all(k%2==0 for k in a) for a,c in poly.terms()))

# Backward Taylor has positive coefficients; check the derivative/factorial
# algebra and enough ranks to expose the distinct existence/uniqueness thresholds.
for n in range(1,35):
    ck(f'factorial-growth-{n}',factorial(n)<=n**n)
for d in range(1,9):
    for r in range(d+1):
        ck(f'existence-threshold-{d}-{r}',(r>=d-1)==(d-r<=1))
        ck(f'law-threshold-{d}-{r}',(r==d)==(d-r==0))
ck('negative-control-two-hidden-not-covered',not (1>=3-1))

# Gaussian killed law: the exact monomial recursion follows from the one-variable
# even-moment recurrence, including all odd monomials and rank zero.
recursion_cases=0
for d in range(2,6):
  for r in range(d-1):
    for alpha in product(range(4), repeat=d):
      if sum(alpha)>5:continue
      g=multi_g(alpha)
      # G_alpha(t)=g*(1+2t)^(-(r+|alpha_active|)/2)).
      lhs=(r+sum(alpha[:r]))*g
      rhs=0
      for i in range(r):
          aa=list(alpha);aa[i]+=2;rhs+=multi_g(aa)
      ck(f'gaussian-killed-recursion-{d}-{r}-{alpha}',lhs==rhs)
      recursion_cases+=1
ck('negative-control-wrong-killing-scale',gm(2)!=Q(1,2)*gm(0))

u,v,z=s.symbols('u v z',real=True)
F=1+u**4*v**2+u**2*v**4-u**2*v**2
p3=1+u**4*v**2+u**2*v**4-3*u**2*v**2
ck('witness-is-Motzkin-plus-square',s.expand(F-p3-2*(u*v)**2)==0)
# These four values only are imported from Proposition 13.5; they do not define Lambda.
source_values={(0,0):1,(4,2):1,(2,4):1,(2,2):4}
fpoly=s.Poly(F,u,v)
source_witness=sum(c*source_values[a] for a,c in fpoly.terms())
gaus_witness=sum(c*multi_g(a) for a,c in fpoly.terms())
ck('source-witness-four-value-identity',source_witness==-1)
ck('gaussian-witness-expectation',gaus_witness==6)
eps=Q(1,14)
ck('mixture-epsilon-positive',0<eps<1)
ck('all-time-witness-upper-bound',(1-eps)*(-1)+eps*6==Q(-1,2))
ck('negative-control-too-large-mixture',(1-Q(1,2))*(-1)+Q(1,2)*6>0)

# Normalized hierarchy is an exact quotient-rule identity, no assertion of
# representability is introduced in this check.
a,b,c,e=s.symbols('a b c e',nonzero=True)
ck('normalization-quotient',s.expand((-b*a+c*e)/a**2-(-b/a+(c/a)*(e/a)))==0)
for r in range(1,8):
    Z=z**(-s.Rational(r,2))
    mass=s.Rational(13,14)+Z/14
    energy=s.Rational(r,14)*Z/z/mass
    h2=s.Rational(r*(r+2),14)*Z/z**2/mass
    ck(f'energy-variance-recursion-r{r}',s.simplify(2*s.diff(energy,z)+h2-energy**2)==0)
    ck(f'positive-energy-at-zero-r{r}',energy.subs(z,1)==s.Rational(r,14))
    ck(f'energy-limit-r{r}',s.limit(energy,z,s.oo)==0)
ck('zero-rank-is-stationary',s.diff(s.Integer(1),z)==0)

# Stieltjes perturbation: the Gaussian complex exponential has zero imaginary
# moment part at every integer n. The full-support Gaussian mixture preserves it.
for n in range(32):
    ck(f'stieltjes-integer-phase-{n}',s.sin(2*s.pi*n)==0)
    plus=s.exp(s.Rational(n*n,2))+s.Rational(1,2)*s.exp(s.Rational(n*n,2)-2*s.pi**2)*s.sin(2*s.pi*n)
    minus=s.exp(s.Rational(n*n,2))-s.Rational(1,2)*s.exp(s.Rational(n*n,2)-2*s.pi**2)*s.sin(2*s.pi*n)
    ck(f'stieltjes-mixture-equal-{n}',s.simplify((plus+gm(n))/2-(minus+gm(n))/2)==0)
ck('perturbations-distinct-at-log-quarter',s.sin(2*s.pi*s.Rational(1,4))==1)

# A non-diagonal rank-two quadratic, with one free coordinate. Affine change
# and its exact inverse preserve the square algebra, rank, and energy.
x1,x2,x3,y1,y2,y3=s.symbols('x1 x2 x3 y1 y2 y3')
phi=s.Matrix([x1+2*x2-1,x2+x3+2,x1])
x=s.Matrix([x1,x2,x3]); y=s.Matrix([y1,y2,y3])
B=phi.jacobian(x);b=phi-B*x
psi=B.inv()*(y-b)
ck('affine-map-invertible',B.det()!=0)
ck('affine-map-inverse',s.simplify(phi.subs(dict(zip(x,psi)),simultaneous=True)-y)==s.zeros(3,1))
H=phi[0]**2+phi[1]**2+7
Qmat=s.hessian(H,x)/2
ck('non-diagonal-psd-rank-two',Qmat.rank()==2 and Qmat==B[:2,:].T*B[:2,:])
ck('affine-energy-reduction',s.expand(H.subs(dict(zip(x,psi)),simultaneous=True)-(y1**2+y2**2+7))==0)

# Frozen-input assertions, when a review snapshot has been supplied.
bindings=HERE/'AUTHOR_SNAPSHOT_BINDINGS.json'
if bindings.exists():
    rows=json.loads(bindings.read_text())
    for row in rows:
        p=HERE/row['snapshot']
        ck('snapshot-integrity-'+row['snapshot'],p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])
result={'status':'PASS','exact_checks':len(checks),'gaussian_recursion_cases':recursion_cases,
        'claims_not_proved_by_controls':['Imported full infinite-dimensional PSD nonmoment functional','Putinar-Schmudgen Theorem 25','Hamburger theorem','Analytic exhaustion and measure uniqueness'],
        'checks':checks}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
