#!/usr/bin/env python3
"""Exact finite controls only; the universal representation proof is in RESULT.md."""
from pathlib import Path
from itertools import product, combinations
import sympy as S
import json,hashlib,math
ROOT=Path(__file__).resolve().parent
counts={}
def check(v,g):
    assert bool(v),g
    counts[g]=counts.get(g,0)+1
def zero(v,g):check(S.expand(v)==0,g)
for r in json.loads((ROOT/'INPUT_BINDINGS.json').read_text()):
    b=(ROOT/r['copy']).read_bytes()
    check(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'input_bindings')

# Taylor identity with its exact two-sided integral remainder, tested on monomials.
t,s,b,v=S.symbols('t s b v',real=True)
for N in range(4):
    for D in range(2*N+5):
        f=t**D
        lhs=f.subs(t,s+b)+f.subs(t,s-b)-2*sum(b**(2*n)*S.diff(f,t,2*n).subs(t,s)/S.factorial(2*n) for n in range(N+1))
        nextder=S.diff(f,t,2*N+2)
        kernel=(b-v)**(2*N+1)/S.factorial(2*N+1)
        rem=S.integrate(kernel*(nextder.subs(t,s+v)+nextder.subs(t,s-v)),(v,0,b))
        zero(lhs-rem,'central_taylor_remainder')
for n in range(20):
    check(math.factorial(2*n)*math.factorial(2*n+2)<=2*math.factorial(2*n+1)**2,'odd_factorial_bound')
    zero(S.Rational(math.factorial(2*n)*math.factorial(2*n+2),math.factorial(2*n+1)**2)-S.Rational(2*n+2,2*n+1),'odd_factorial_ratio')

# Finite signed energy values illustrate central cosh coefficients and moment CS.
energies=[-3,-1,0,2]
weights=[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]
for n in range(12):
    moment=lambda k:sum(w*S.Integer(r)**k for w,r in zip(weights,energies))
    check(moment(2*n)>=0,'even_energy_moment')
    check(moment(2*n)*moment(2*n+2)-moment(2*n+1)**2>=0,'odd_energy_cs')
    for B in [S.Rational(1,4),S.Rational(1,2),S.Rational(3,4)]:
        Cn=sum(B**(2*k)*moment(2*k)/S.factorial(2*k) for k in range(n+1))
        Cnext=Cn+B**(2*n+2)*moment(2*n+2)/S.factorial(2*n+2)
        check(Cnext>=Cn,'central_partial_sum_monotonicity')

x,y,z=S.symbols('x y z',real=True)
M=x**4*y**2+x**2*y**4+z**6-3*x**2*y**2*z**2
rad=x*x+y*y+z*z; h=M+rad
zero((x**4*y**2)*(x**2*y**4)*z**6-(x*x*y*y*z*z)**3,'motzkin_amgm_product')
# For any proposed cubic-square representation, these coefficient comparisons
# force all listed coefficients to vanish before the negative xyz-square term.
c=S.symbols('c0:10',real=True)
mon=[x**3,y**3,z**3,x*x*y,x*x*z,x*y*y,y*y*z,x*z*z,y*z*z,x*y*z]
f=sum(ci*m for ci,m in zip(c,mon)); sq=S.Poly(f*f,x,y,z)
def coeff(expr,powers):return S.Poly(expr,x,y,z).coeff_monomial(powers)
zero(coeff(f*f,x**6)-c[0]**2,'motzkin_elimination_x3')
zero(coeff(f*f,y**6)-c[1]**2,'motzkin_elimination_y3')
g=f.subs({c[0]:0,c[1]:0})
zero(coeff(g*g,x**4*z**2)-c[4]**2,'motzkin_elimination_x2z')
zero(coeff(g*g,y**4*z**2)-c[6]**2,'motzkin_elimination_y2z')
g=g.subs({c[4]:0,c[6]:0})
zero(coeff(g*g,x*x*z**4)-c[7]**2,'motzkin_elimination_xz2')
zero(coeff(g*g,y*y*z**4)-c[8]**2,'motzkin_elimination_yz2')
g=g.subs({c[7]:0,c[8]:0})
zero(coeff(g*g,x*x*y*y*z*z)-c[9]**2,'motzkin_final_square_coefficient')
check(coeff(M,x*x*y*y*z*z)==-3,'motzkin_negative_target')
C,k=S.symbols('C k',real=True)
poly=S.Poly(h+C-k*rad,x,y,z)
top=sum(co*x**a*y**bb*z**cc for (a,bb,cc),co in poly.terms() if a+bb+cc==6)
zero(top-M,'motzkin_shifted_top_form')

# The elementary finite-atomic model of the abstract signed-measure/RN bridge.
points=[(1,0,0),(0,1,0),(-1,0,0),(0,0,1),(1,1,1)]
ws=[S.Rational(i,15) for i in range(1,6)]
levels=[h.subs(dict(zip((x,y,z),pt))) for pt in points]
unique=sorted(set(levels))
polys=[x**i*y**j*z**k for i in range(4) for j in range(4-i) for k in range(4-i-j)]+[1+x-y,z+x*y,M]
def value(p,pt):return S.sympify(p).subs(dict(zip((x,y,z),pt)))
def L(p):return sum(w*value(p,pt) for w,pt in zip(ws,points))
def nu(p):return {r:sum(w*value(p,pt) for w,pt,e in zip(ws,points,levels) if e==r) for r in unique}
nu1=nu(S.Integer(1))
for p in polys:
    np=nu(p); np2=nu(p*p); plus=nu((p+1)**2); minus=nu((p-1)**2)
    nhp=nu(h*p)
    for r in unique:
        zero(np[r]-(plus[r]-minus[r])/4,'measure_polarization')
        zero(nhp[r]-r*np[r],'measure_h_shift')
        check(np2[r]>=0,'measure_square_positivity')
        density=np[r]/nu1[r]
        zero(nu((h-r)*p)[r],'fibre_ideal_annihilation')
        zero(density-sum(w*value(p,pt) for w,pt,e in zip(ws,points,levels) if e==r)/nu1[r],'rn_density')
    zero(sum(np.values())-L(p),'measure_reconstruction')
    zero(sum(nu1[r]*(np[r]/nu1[r]) for r in unique)-L(p),'rn_reconstruction')
    for mask in product([0,1],repeat=len(unique)):
        B=[r for r,flag in zip(unique,mask) if flag]
        vp=sum(np[r] for r in B); v1=sum(nu1[r] for r in B); vp2=sum(np2[r] for r in B)
        check(vp*vp<=v1*vp2,'borel_set_cs')
        if v1==0:check(vp==0,'null_set_control')
# Irrational fixed energy coefficients do not affect finite real-linear relations.
alt=S.sqrt(2)*h+S.pi
for p in polys[:6]:
    altweights=nu(alt*p); np=nu(p)
    for r in unique:zero(altweights[r]-(S.sqrt(2)*r+S.pi)*np[r],'irrational_energy_coefficients')

result={'status':'PASS','total_exact_checks':sum(counts.values()),'checks_by_group':counts,'sympy_version':S.__version__,
'scope':'Finite exact symbolic/rational controls, not universal measure reconstruction or proof-kernel verification.'}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
