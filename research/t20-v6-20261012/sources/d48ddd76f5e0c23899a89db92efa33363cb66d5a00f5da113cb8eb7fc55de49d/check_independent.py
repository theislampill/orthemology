#!/usr/bin/env python3
"""Finite exact checks of the central-Taylor and fibre algebra, not theorem proof."""
from pathlib import Path
import hashlib,json,itertools
import sympy as S
ROOT=Path(__file__).resolve().parent
counts={}
def check(ok,group):
    assert bool(ok),group
    counts[group]=counts.get(group,0)+1
def eq(a,b,group):
    check(S.cancel(S.expand(a-b))==0,group)

for row in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    original=(ROOT.parent/row['source']).read_bytes()
    frozen=(ROOT/row['copy']).read_bytes()
    check(original==frozen,'prior_source_bytes')
    check(hashlib.sha256(original).hexdigest()==row['sha256'],'prior_source_hash')

# Central Taylor cancellation depends on EVEN derivatives, not signs of odd terms.
b=S.symbols('b',positive=True)
for N in range(8):
    coefficients=S.symbols('c:'+str(2*N+2),real=True)
    forward=sum(coefficients[j]*b**j/S.factorial(j) for j in range(2*N+2))
    backward=sum(coefficients[j]*(-b)**j/S.factorial(j) for j in range(2*N+2))
    central=2*sum(coefficients[2*j]*b**(2*j)/S.factorial(2*j) for j in range(N+1))
    eq(forward+backward,central,'odd_taylor_terms_cancel')
    check((-1)**(2*N+2)==1,'backward_even_remainder_sign')

# For a one-atom law at negative h the local central step still works.
# An assumed Stieltjes h measure would incorrectly rule this toy case out.
t=S.symbols('t',real=True)
energy=-3
f=S.exp(-t*energy)
for n in range(8):
    eq(S.diff(f,t,2*n),energy**(2*n)*f,'even_h_square_derivatives')
    check(energy**(2*n)>=0,'even_h_nonnegative')
check(energy<0,'negative_odd_h_allowed_before_representation')
eq((S.exp(b)+S.exp(-b))/2,S.cosh(b).rewrite(S.exp),'cosh_even_series_identity')

# A coercive polynomial with a negative mixed coefficient; no SOS certificate is
# used or claimed in these finite conditional-law calculations.
x,y=S.symbols('x y',real=True)
h=10*(x**4*y**2+x**2*y**4-3*x**2*y**2+1)+x*x+y*y
points=[(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
weights=[S.Rational(j,45) for j in range(1,10)]
energies=[h.subs({x:a,y:b}) for a,b in points]
levels=sorted(set(energies))
def value(p,point):
    return S.sympify(p).subs({x:point[0],y:point[1]},simultaneous=True)
def nu(p,level):
    return sum(w*value(p,point) for w,point,e in zip(weights,points,energies) if e==level)
base={level:nu(1,level) for level in levels}
def fibre(p,level): return nu(p,level)/base[level]
polys=[S.Integer(1),x,y,x*y,x*x-y,1+x-y+x*y,x**3-y**3]
for level in levels:
    check(base[level]>0,'positive_base_mass')
    eq(fibre(1,level),1,'fibre_unit')
    for p in polys:
        eq(nu(p,level),(nu((p+1)**2,level)-nu((p-1)**2,level))/4,
           'signed_measure_polarization')
        eq(nu(h*p,level),level*nu(p,level),'measure_h_intertwining')
        eq(fibre((h-level)*p,level),0,'fibre_ideal_annihilation')
        check(fibre(p*p,level)>=0,'fibre_square_positivity')
        eq(nu(p,level),fibre(p,level)*base[level],'rn_recombination')
    # Real-coefficient square positivity is an algebraic matrix property.
    a,c,d=S.symbols('a c d',real=True)
    q=a+c*x+d*y
    conditional_sum=sum(w/base[level]*value(q,point)**2
                        for w,point,e in zip(weights,points,energies) if e==level)
    eq(fibre(q*q,level),conditional_sum,'arbitrary_real_coefficient_square_identity')

# The measure-valued Cauchy-Schwarz inequality supports absolute continuity.
for flags in itertools.product((False,True),repeat=len(levels)):
    selected=[level for level,flag in zip(levels,flags) if flag]
    def on_set(p): return sum((nu(p,level) for level in selected),S.Integer(0))
    for p in polys:
        check(on_set(p)**2 <= on_set(1)*on_set(p*p),'borel_set_cauchy_schwarz')
        if on_set(1)==0:
            eq(on_set(p),0,'base_null_set_annihilated')
        for c in (S.Rational(-3,2),S.Rational(2,3)):
            eq(on_set((p+c)**2),on_set(p*p)+2*c*on_set(p)+c*c*on_set(1),
               'measure_quadratic_identity')

for p in polys:
    for n in range(7):
        original=sum(w*value(p,point)*e**n for w,point,e in zip(weights,points,energies))
        eq(original,sum(fibre(p,level)*level**n*base[level] for level in levels),
           'all_mixed_moments_recombined')
check(any(fibre(x*x,level)>fibre(x,level)**2 for level in levels),
      'fibre_functionals_need_not_be_characters')

# Exact coefficient elimination behind the homogeneous Motzkin non-SOS proof.
# If a sum of cubic squares has a zero displayed coefficient after earlier
# eliminations, the corresponding coefficient in every cubic must vanish.
z=S.symbols('z',real=True)
triples=[(a,b,3-a-b) for a in range(4) for b in range(4-a)]
coefficients={power:S.Symbol('c_'+''.join(map(str,power)),real=True) for power in triples}
cubic=sum(coefficient*x**power[0]*y**power[1]*z**power[2]
          for power,coefficient in coefficients.items())
square=S.Poly(cubic*cubic,x,y,z)
removed={}
for power in [(3,0,0),(0,3,0),(2,0,1),(0,2,1),(1,0,2),(0,1,2)]:
    target=tuple(2*v for v in power)
    eq(square.coeff_monomial(target).subs(removed),coefficients[power]**2,
       'motzkin_zero_coefficient_elimination')
    removed[coefficients[power]]=0
eq(square.coeff_monomial((2,2,2)).subs(removed),coefficients[(1,1,1)]**2,
   'motzkin_remaining_coefficient_nonnegative')
M=x**4*y**2+x**2*y**4+z**6-3*x*x*y*y*z*z
eq(S.Poly(M,x,y,z).coeff_monomial((2,2,2)),-3,'motzkin_negative_target')
C,c=S.symbols('C c',real=True)
perturbed=S.Poly(M+(1-c)*(x*x+y*y+z*z)+C,x,y,z)
top=sum(coefficient*x**a*y**b*z**d for (a,b,d),coefficient in perturbed.terms()
        if a+b+d==6)
eq(top,M,'all_constant_quadratic_shifts_preserve_obstruction')

out={'status':'PASS','total_exact_checks':sum(counts.values()),'checks_by_group':counts,
     'sympy_version':S.__version__,'scope':'Finite algebraic controls only; universal claims are reviewed in REVIEW.md.'}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
