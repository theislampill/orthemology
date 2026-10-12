#!/usr/bin/env python3
"""Finite exact controls only; classical existence/Λ positivity are imported."""
from __future__ import annotations
import hashlib, itertools, json, math, pathlib, sys
from collections import Counter
import sympy as S

ROOT = pathlib.Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
counts = Counter()

def check(condition, category, detail=''):
    if not bool(condition):
        raise AssertionError(f'{category}: {detail}')
    counts[category] += 1

def eq(a,b,category,detail=''):
    check(S.simplify(a-b)==0,category,detail)

def compositions(n,r):
    if r==0:
        if n==0: yield ()
    elif r==1:
        yield (n,)
    else:
        for j in range(n+1):
            for tail in compositions(n-j,r-1): yield (j,)+tail

# Read-only bindings are checked against both the snapshot and live predecessor.
for entry in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    for path in [ROOT/entry['copy'], WORKSPACE/entry['source']]:
        check(hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],
              'input_sha256',str(path))
for entry in json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())['local_files']:
    check(hashlib.sha256((ROOT/entry['file']).read_bytes()).hexdigest()==entry['sha256'],
          'primary_source_sha256',entry['file'])

# Full SOS identities are mathematical; these check finite symbolic instances.
x=S.symbols('x0:5', real=True)
for r in range(5):
    h=sum((v*v for v in x[:r]),S.Integer(0))
    q=1+x[0]+2*x[1]**2-3*x[0]*x[1]
    for n in range(7):
        terms=[]
        for beta in compositions(n,r):
            c=S.Integer(math.factorial(n))
            for b in beta: c/=math.factorial(b)
            mon=S.prod(x[i]**beta[i] for i in range(r))
            check(c>0,'multinomial_positive_coefficient')
            terms.append(c*(q*mon)**2)
        eq(q*q*h**n,sum(terms,S.Integer(0)),'weighted_sos_identity',(r,n))
        if n:
            for i in range(r):
                diff=S.Poly(S.expand(h**n-x[i]**(2*n)),*x)
                check(all(c>=0 and all(e%2==0 for e in powers)
                          for powers,c in diff.terms()),
                      'controlled_difference_monomial_sos',(r,n,i))
for n in range(1,129):
    check(math.factorial(n)<=n**n,'factorial_growth_bound',n)

# Stationary embedding's algebra-homomorphism and annihilation identities.
u,v=S.symbols('u v', real=True)
for d in range(2,6):
    for r in range(d-1):
        subs={x[i]:(u if i==r else v if i==r+1 else S.Integer(0))
              for i in range(d)}
        h=sum((x[i]**2 for i in range(r)),S.Integer(0))
        p=1+sum((i+1)*x[i]**(i%3+1) for i in range(d))
        q=2+sum((i+2)*x[i] for i in range(d))+x[0]*x[d-1]
        E=lambda f:S.expand(f).subs(subs,simultaneous=True)
        eq(E(q*q),E(q)**2,'stationary_square_substitution',(d,r))
        eq(E(p*q),E(p)*E(q),'stationary_product_substitution',(d,r))
        eq(E(h*p),0,'stationary_killing_annihilation',(d,r))
        eq(E(S.Integer(1)),1,'stationary_normalization',(d,r))

# Gaussian moments and exact killing recursion, including r=0.
t=S.symbols('t', nonnegative=True)
s=1+2*t

def normal_moment(n):
    return S.Integer(0) if n%2 else S.Integer(math.prod(range(1,n,2)))

def gaussian_killed(alpha,r):
    if any(n%2 for n in alpha): return S.Integer(0)
    coeff=S.prod(normal_moment(n) for n in alpha)
    return coeff*s**(-S.Rational(r+sum(alpha[:r]),2))

for d in range(1,5):
    for r in range(d+1):
        for deg in range(5):
            for alpha in compositions(deg,d):
                g=gaussian_killed(alpha,r)
                hp=S.Integer(0)
                for i in range(r):
                    beta=list(alpha); beta[i]+=2
                    hp+=gaussian_killed(tuple(beta),r)
                eq(S.diff(g,t),-hp,'gaussian_killing_monomial',(d,r,alpha))

# Nonnegative witness's finite Gaussian expectation; the Λ values are source inputs.
F=1+u**4*v**2+u**2*v**4-u**2*v**2
M=sum(c*normal_moment(a)*normal_moment(b)
      for (a,b),c in S.Poly(F,u,v).terms())
eq(M,6,'gaussian_witness_expectation')
# AM-GM applies to A=u^4v^2, B=u^2v^4, C=1 with cube root product u^2v^2.
eq((u**4*v**2)*(u**2*v**4), (u**2*v**2)**3,'amgm_witness_product')
eq(F-(u**4*v**2+u**2*v**4+1-3*u**2*v**2),2*u**2*v**2,
   'amgm_witness_remainder')
eps=S.Rational(1,14)
z=S.symbols('z', nonnegative=True)
a=(1-eps)+eps*z
AF=-(1-eps)+eps*6*z
eq(AF+S.Rational(1,2),S.Rational(3,7)*(z-1),'uniform_negative_witness_bound')
eq(a-(1-eps),eps*z,'uniform_positive_normalizer')
eq(a.subs(z,1),1,'mixture_boundary_normalization')

# Quotient differentiation with independent symbolic B/G polynomial values.
bp,gp,ghp,gone,ghone=S.symbols('bp gp ghp gone ghone')
AP=(1-eps)*bp+eps*gp
A1=(1-eps)+eps*gone
quotient_derivative=(-eps*ghp*A1+eps*AP*ghone)/A1**2
rhs=-eps*ghp/A1+(eps*ghone/A1)*(AP/A1)
eq(quotient_derivative,rhs,'normalized_mixture_hierarchy')

# Exact strict-decrease numerator for every symbolic positive rank.
r=S.symbols('r', positive=True)
z_t=s**(-r/2)
a_t=1-eps+eps*z_t
energy=eps*r*z_t/(s*a_t)
negative_formula=-eps*r*z_t*((r+2)*(1-eps)+2*eps*z_t)/(s*s*a_t*a_t)
eq(S.diff(energy,t),negative_formula,'strict_energy_decrease_formula')
eq(energy,r*z_t/(s*(13+z_t)),'explicit_mixture_energy')
for rank in range(5):
    check(S.simplify(energy.subs({r:rank,t:0}))==S.Rational(rank,14),
          'mixture_initial_energy',rank)

# Inherited lognormal integer cancellation, no floating-point quadrature.
n=S.symbols('n', integer=True, nonnegative=True)
eq(S.exp(n*n/2-2*S.pi**2)*S.sin(2*S.pi*n),0,'symbolic_lognormal_cancellation')
for j in range(25):
    cancellation=S.exp(S.Rational(j*j,2)-2*S.pi**2)*S.sin(2*S.pi*j)
    eq(cancellation,0,'integer_lognormal_cancellation',j)
    eta_plus=(S.exp(S.Rational(j*j,2))+cancellation/2+normal_moment(j))/2
    eta_minus=(S.exp(S.Rational(j*j,2))-cancellation/2+normal_moment(j))/2
    eq(eta_plus,eta_minus,'full_support_hidden_moment_equality',j)
# Controlled normalized variance and survival mass.
for rank in range(1,5):
    alpha=(2,)+(0,)*(rank-1)
    eq(gaussian_killed(alpha,rank)/gaussian_killed((0,)*rank,rank),1/s,
       'controlled_normalized_variance',rank)

# Affine rank-one and rank-two examples, with polynomial inverse maps.
x0,x1,x2=x[:3]
z0,z1,z2=S.symbols('z0 z1 z2', real=True)
examples=[
    (S.Matrix([[2,-1],[1,1]]),S.Matrix([3,0]),1,S.Integer(5)),
    (S.Matrix([[1,1,0],[0,1,2],[1,-1,1]]),S.Matrix([1,-2,0]),2,S.Integer(-7)),
]
for mat,offset,rank,c in examples:
    d=mat.rows; xv=S.Matrix(x[:d]); zv=S.Matrix([z0,z1,z2][:d])
    phi=mat*xv+offset; psi=mat.inv()*(zv-offset)
    check(mat.det()!=0,'affine_map_invertible',d)
    for j in range(d):
        eq(phi[j].subs(dict(zip(x[:d],psi)),simultaneous=True),zv[j],
           'affine_inverse_identity',(d,j))
        eq(psi[j].subs(dict(zip(zv,phi)),simultaneous=True),xv[j],
           'affine_forward_identity',(d,j))
    h=sum(phi[j]**2 for j in range(rank))+c
    eq(h.subs(dict(zip(x[:d],psi)),simultaneous=True),
       sum(zv[j]**2 for j in range(rank))+c,'affine_quadratic_normal_form',d)
    Q=mat[:rank,:].T*mat[:rank,:]
    check(Q.rank()==rank,'quadratic_rank_invariant',d)

result={
  'status':'passed',
  'total_exact_checks':sum(counts.values()),
  'categories':dict(sorted(counts.items())),
  'scope':'Finite symbolic and integrity controls supplement ordinary proofs; no verification of classical representation theorems or the full infinite functional Λ.',
  'python':sys.version.split()[0], 'sympy':S.__version__,
}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
