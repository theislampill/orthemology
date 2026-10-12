#!/usr/bin/env python3
"""Exact finite controls for the ordinary proof; no universal proof claim."""
from pathlib import Path
from fractions import Fraction
import hashlib, json, math
import sympy as S

ROOT=Path(__file__).resolve().parent
counts={}
def check(ok,group):
    assert bool(ok), group
    counts[group]=counts.get(group,0)+1

def zero(v,group):
    check(S.cancel(S.expand(v))==0,group)

for row in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    b=(ROOT/row['copy']).read_bytes()
    check(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'input_bindings')

x,y,z,u,v=S.symbols('x y z u v',real=True)
points=[(-2,1),(0,-1),(1,2),(2,-2)]
weights=[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]
polys=[x**i*y**j for i in range(5) for j in range(5-i)]+[x-y,1+x*y,(x-y)**2]
for label,h in [('quadratic',x*x+y*y),('triangular',x*x+(y-x**3)**2)]:
    energies=[int(h.subs({x:a,y:b})) for a,b in points]
    check(all(e>=0 for e in energies),'finite_law_energy')
    def A(p):
        return S.Poly(sum(w*p.subs({x:a,y:b})*z**e for (a,b),w,e in zip(points,weights,energies)),z).as_expr()
    den=A(S.Integer(1))
    for p in polys:
        ap=A(p)
        zero(-z*S.diff(ap,z)+A(h*p),label+'_linear_hierarchy')
        # Work with a denominator-cleared quotient identity, to avoid large simplification.
        lhs=-z*(S.diff(ap,z)*den-ap*S.diff(den,z))
        rhs=-A(h*p)*den+A(h)*ap
        zero(lhs-rhs,label+'_normalized_hierarchy')
    for qa in [S.Rational(1,2),S.Rational(2,3),S.Rational(3,4)]:
        first=[w*qa**e for w,e in zip(weights,energies)]
        Z=sum(first); first=[a/Z for a in first]
        recovered=[a*qa**(-e) for a,e in zip(first,energies)]
        recovered=[a/sum(recovered) for a in recovered]
        for a,b in zip(recovered,weights): zero(a-b,label+'_untwisting')
        for qb in [S.Rational(1,3),S.Rational(4,5)]:
            seq=[w*qb**e for w,e in zip(first,energies)]; seq=[a/sum(seq) for a in seq]
            direct=[w*(qa*qb)**e for w,e in zip(weights,energies)]; direct=[a/sum(direct) for a in direct]
            for a,b in zip(seq,direct):zero(a-b,label+'_semigroup')

# Explicit nonnegative-coefficient SOS identities for radial and certified energies.
for h in [x*x+y*y,x*x+y*y+x*x*y*y]:
    for n in range(1,8):
        for coordinate in [x,y]:
            difference=S.Poly(S.expand(h**n-coordinate**(2*n)),x,y)
            check(all(c>=0 and i%2==j%2==0 for (i,j),c in difference.terms()),'sos_domination')
            rhs=(h-coordinate**2)*sum(h**(n-1-k)*coordinate**(2*k) for k in range(n))
            zero(h**n-coordinate**(2*n)-rhs,'sos_factorization')
        q=1+x-y+x*y
        rhs=sum(S.binomial(n,k)*(q*x**k*y**(n-k))**2 for k in range(n+1))
        # q²|x|^(2n), not the more general h, for the explicit multinomial control.
        zero(q*q*(x*x+y*y)**n-rhs,'weighted_square_identity')
        check(math.factorial(n)<=n**n,'factorial_carleman_bound')

# The slow-radial-growth example is polynomially conjugate, not scalarized.
for k in range(3,8):
    phi=(x,y-x**k); psi=(u,v+u**k)
    for back,coordinate in zip([e.subs({u:phi[0],v:phi[1]},simultaneous=True) for e in psi],[x,y]):
        zero(back-coordinate,'polynomial_inverse')
    h=x*x+(y-x**k)**2
    zero(h.subs({x:psi[0],y:psi[1]},simultaneous=True)-(u*u+v*v),'energy_conjugacy')
    zero(h.subs(y,x**k)-x*x,'slow_radial_valley')

# Universal symbolic cancellation at integer lognormal moment orders.
n=S.symbols('n',integer=True,nonnegative=True)
zero(S.sin(2*S.pi*n),'lognormal_integer_cancellation')
for j in range(12):
    zero(S.exp(S.Rational(j*j,2)-2*S.pi**2)*S.sin(2*S.pi*j),'lognormal_finite_controls')
    if j%2==0:
        check(S.exp(S.Rational(j*j,2))>0,'signed_lognormal_even_moments')
    else:
        zero(S.exp(S.Rational(j*j,2)-2*S.pi**2)*S.sin(2*S.pi*j),'signed_lognormal_odd_moments')

# Degenerate quadratic: nontrivial X dynamics times equal Y moments.
for a in range(6):
    for b in range(6):
        yn=S.exp(S.Rational(b*b,2))
        m=yn if a==0 else yn*z/(1+z)
        mhp=yn*z/(1+z)
        mh=z/(1+z)
        zero(-z*S.diff(m,z)-(-mhp+mh*m),'noncoercive_mixed_hierarchy')
zero((z/(1+z)).subs(z,S.Rational(1,2))-S.Rational(1,3),'noncoercive_exact_time')

# Bare quadratic hierarchy at determinate zero data; negative fourth moment.
t,eps=S.symbols('t eps',positive=True)
f=S.exp(-1/t); mass=1-eps*f
A2=-S.diff(mass,t); A4=S.diff(mass,t,2)
zero(A4-eps*S.exp(-1/t)*(2*t-1)/t**4,'flat_exact_formula')
check(S.simplify(A4.subs({t:S.Rational(1,4),eps:S.Rational(1,2)}))<0,'flat_negative_square')
zero(S.diff(A2/mass,t)-(-A4/mass+(A2/mass)**2),'flat_quadratic_hierarchy')

# Unbounded-below linear energy: normalized negative-geometric moments.
z=S.symbols('z',positive=True)
raw=[1/(1-z)]
for r in range(1,8):raw.append(S.cancel(z*S.diff(raw[-1],z)))
mom=[S.cancel((-1)**r*(1-z)*raw[r]) for r in range(8)]
for r in range(7):zero(z*S.diff(mom[r],z)-(-mom[r+1]+mom[1]*mom[r]),'geometric_hierarchy')
zero(mom[1]+z/(1-z),'geometric_mean')
zero(mom[1].subs(z,S.Rational(3,4))+3,'geometric_exact_time')
check(S.limit(mom[1],z,1,dir='-')==-S.oo,'geometric_blowup')

result={'status':'PASS','total_exact_checks':sum(counts.values()),'checks_by_group':counts,
        'scope':'Finite exact symbolic and rational controls only; universal proofs are in RESULT.md.',
        'python_sympy_version':S.__version__}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
