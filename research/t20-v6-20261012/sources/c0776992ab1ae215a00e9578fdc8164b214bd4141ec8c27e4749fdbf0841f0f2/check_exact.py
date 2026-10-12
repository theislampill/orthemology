#!/usr/bin/env python3
"""Focused exact controls for compact-energy PDE localization.

Inherited regression checks are explicitly separated from the new bridge algebra.
No symbolic run proves the universal analytic or measure theorem.
"""
from pathlib import Path
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
checks=[]

def zero(group,name,expr):
    v=s.simplify(s.cancel(expr))
    assert v==0,(name,v)
    checks.append({'group':group,'name':name})

def true(group,name,condition):
    assert bool(condition),name
    checks.append({'group':group,'name':name})

for path,digest in json.loads((HERE/'INPUT_BINDINGS.json').read_text()).items():
    true('input_integrity',path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest)
# Verify every file in the prior frozen packet without modifying or replaying it.
base=ROOT/'energy-controlled-gradient-reverse-lift-20261010'
manifest=json.loads((base/'AUTHOR_MANIFEST.json').read_text())
for name,digest in manifest['files'].items():
    true('narrow_frozen_integrity',name,hashlib.sha256((base/name).read_bytes()).hexdigest()==digest)
receipt=json.loads((base/'AUTHOR_RECEIPT.json').read_text())
true('narrow_frozen_integrity','manifest matches receipt',hashlib.sha256((base/'AUTHOR_MANIFEST.json').read_bytes()).hexdigest()==receipt['manifest_sha256'])

# Product-generator identity for genuinely composed smooth energy tests.
x,y,z=s.symbols('x y z',real=True)
for d in (1,2,3):
    xs=(x,y,z)[:d]
    H=s.Function('H')(*xs);p=s.Function('p')(*xs)
    bs=[s.Function('b'+str(i))(*xs) for i in range(d)]
    chi=s.Function('chi')
    bg=lambda f:sum(bi*s.diff(f,xi) for bi,xi in zip(bs,xs))
    G=lambda f:bg(f)-H*f
    zero('new_localization_algebra',f'composed energy cutoff product d={d}',G(p*chi(H))-(bg(p)-H*p)*chi(H)-p*bg(H)*s.diff(chi(H),H))
    # D(phi)=c0 phi+sum ci partial_i phi at the measure-coefficient level.
    c0=s.symbols('c0');cs=s.symbols('c1:'+str(d+1))
    D=lambda f:c0*f+sum(ci*s.diff(f,xi) for ci,xi in zip(cs,xs))
    alpha_p=c0*p+sum(ci*s.diff(p,xi) for ci,xi in zip(cs,xs))
    beta_p=p*sum(ci*s.diff(H,xi) for ci,xi in zip(cs,xs))
    zero('new_localization_algebra',f'compact distribution scalar split d={d}',D(p*chi(H))-alpha_p*chi(H)-beta_p*s.diff(chi(H),H))
    # Explicit residual time coefficient gives the sign in alpha,beta.
    zero('new_localization_algebra',f'residual alpha beta sign d={d}',-G(p*chi(H))-(-(bg(p)-H*p)*chi(H)-p*bg(H)*s.diff(chi(H),H)))
    xi=s.symbols('xi',real=True)
    zero('new_localization_algebra',f'scalar Fourier derivative term d={d}',G(p*s.exp(s.I*xi*H))-s.exp(s.I*xi*H)*(bg(p)-H*p+s.I*xi*p*bg(H)))

# Finite Taylor product recurrences on the beyond-H2 actual energy and drift.
u=x-y**3;H=1+u*u+y*y
bs=[-s.diff(H,x),-s.diff(H,y)]
bg=lambda p:sum(bi*s.diff(p,v) for bi,v in zip(bs,(x,y)))
G=lambda p:bg(p)-H*p
zz=s.symbols('zz')
for n in range(0,7):
    P=sum((s.I*zz*H)**j/s.factorial(j) for j in range(n+1))
    Pprev=sum((s.I*zz*H)**j/s.factorial(j) for j in range(n)) if n else 0
    for j,p in enumerate((1+x*y,x*x-y,x+u*u)):
        zero('new_localization_algebra',f'polynomial energy Taylor generator N={n},p={j}',G(p*P)-((bg(p)-H*p)*P+s.I*zz*p*bg(H)*Pprev))

# Distribution multiplication with an outer coordinate test needs first derivatives only.
for d in (1,2,3):
    xs=(x,y,z)[:d]
    H=s.Function('H')(*xs);q=s.Function('q')(*xs);chi=s.Function('chi')
    for i,xi in enumerate(xs):
        zero('new_localization_algebra',f'localization C1 product d={d},i={i}',s.diff(chi(H)*q,xi)-chi(H)*s.diff(q,xi)-s.diff(chi(H),H)*s.diff(H,xi)*q)

# Beyond-H2 control is m=3 only; no new example campaign.
u=x-y**3;F=u*u+y*y;H=F+1;R=x*x+y*y
S=s.diff(F,x)**2+s.diff(F,y)**2
zero('beyond_H2_control','gradient dissipation SOS',S-(4*u*u+(-6*y*y*u+2*y)**2))
zero('beyond_H2_control','H explicit SOS',H-(1+u*u+y*y))
cc,C=s.symbols('c C',real=True)
old=((F+C)**2-cc*R).subs(x,y**3)
zero('beyond_H2_control','squared energy leading coefficient',s.Poly(s.expand(old),y).LC()+cc)
true('beyond_H2_control','squared energy failure degree six',s.Poly(s.expand(old),y).degree()==6)
zero('beyond_H2_control','elementary radius bound square',2*u*u+2*y**6+y*y-R-(u-y**3)**2)
U,Y=s.symbols('U Y',real=True)
HP=1+U*U+Y*Y
rem=s.Poly(s.expand(3*HP+2*HP**3-(2*U*U+2*Y**6+Y*Y)),U,Y)
true('beyond_H2_control','polynomial sublevel envelope remainder SOS',all(co>=0 and all(e%2==0 for e in mon) for mon,co in rem.terms()))
zero('beyond_H2_control','static inverse map first coordinate',(x-y**3)+y**3-x)
# This checks invertibility only; the proof does not use it as a flow.

# Explicit inherited regressions: these are not counted as new discoveries.
for n in range(0,9):
    true('inherited_regression',f'weighted energy factorial n={n}',s.binomial(4*n,2*n)<=2**(4*n))
for n in range(0,5):
    expected=-H**(n+1) if n==0 else -n*H**(n-1)*S-H**(n+1)
    zero('inherited_regression',f'energy recurrence m3 n={n}',G(H**n)-expected)
ss,uu=s.symbols('s u',nonnegative=True)
M=1+ss*ss;P=uu*uu-(1+ss*ss)**2
zero('inherited_regression','representative graph polynomial',P.subs(uu,M))
root_excess=1+(1+ss*ss)**2-M
true('inherited_regression','representative root-bound polynomial envelope',all(co>=0 for co in s.Poly(root_excess,ss).all_coeffs()))

summary={}
for item in checks:summary[item['group']]=summary.get(item['group'],0)+1
out={'status':'passed','checks':len(checks),'groups':summary,'limit':'Finite exact checks supplement the written proof; inherited regressions and input checks are not new mathematical discoveries.','details':checks}
(HERE/'EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
