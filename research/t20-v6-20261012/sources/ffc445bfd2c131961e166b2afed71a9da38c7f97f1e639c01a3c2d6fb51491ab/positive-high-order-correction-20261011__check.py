#!/usr/bin/env python3
"""Author controls: exact finite algebra plus labelled numerical diagnostics."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json,sys,hashlib
import sympy as sp
import mpmath as mp
checks=[]
def ck(name,condition):
    if not bool(condition): raise RuntimeError(name)
    checks.append(name)
def P(z,m): return sum((z**j/F(factorial(j)) for j in range(m+1)),F(0))
def norm(w):
    z=sum(w)
    if z<=0: raise ValueError('zero normalizer')
    return tuple(v/z for v in w)
def step(w,v,h,m):
    if h<0 or m<1 or any(x<0 for x in v):raise ValueError('outside nonnegative domain')
    return norm(tuple(a/P(h*b,m) for a,b in zip(w,v)))
def audit(w,L):return norm(tuple(a*b for a,b in zip(w,L)))
w=(F(1,6),F(1,3),F(1,2)); v=(F(0),F(1),F(3)); L=(F(0),F(2),F(5))
for m in range(1,9):
 for h in (F(0),F(1,10),F(1),F(30)):
    u=step(w,v,h,m)
    ck(f'positive m{m} h{h}',all(x>0 for x in u) and sum(u)==1)
    ck(f'descent m{m} h{h}',sum(a*b for a,b in zip(u,v))<=sum(a*b for a,b in zip(w,v)))
    ck(f'audit m{m} h{h}',audit(u,L)==step(audit(w,L),v,h,m))
    n=7; it=w
    for _ in range(n):it=step(it,v,h,m)
    ck(f'iteration m{m} h{h}',it==norm(tuple(a/P(h*b,m)**n for a,b in zip(w,v))))
    for k in range(1,m+1):
     if h: ck(f'moment envelope m{m} k{k} h{h}',all(b**k/P(h*b,m)<=F(factorial(k))/h**k for b in v))
z=sp.Symbol('z')
for m in range(1,8):
 pp=sum(z**j/sp.factorial(j) for j in range(m+1))
 ck(f'scalar series order {m}',sp.series(1/pp-sp.exp(-z),z,0,m+2).removeO()==z**(m+1)/sp.factorial(m+1))
 # Exact normalized leading coefficient for nonconstant finite law.
 aa=[1/pp.subs(z,z*x) for x in v]; bb=[sp.exp(-z*x) for x in v]
 za=sum(sp.Rational(a.numerator,a.denominator)*b for a,b in zip(w,aa)); zb=sum(sp.Rational(a.numerator,a.denominator)*b for a,b in zip(w,bb))
 # The zero-loss atom isolates the normalizer and avoids expensive full vector expansions.
 lead=sp.limit((1/za-1/zb)/z**(m+1),z,0)
 ck(f'normalized leading {m}',sp.simplify(lead+sum(sp.Rational(a.numerator,a.denominator)*x**(m+1) for a,x in zip(w,v))/sp.factorial(m+1))==0)
 for n in (m+2,m+5,2*m+8):
  q=m+1; maximizer=F(q,n-q)
  sup=maximizer**q/(1+maximizer)**n
  ck(f'endpoint supremum m{m} n{n}',sup==F(q,n)**q*F(n-q,n)**(n-q) and F(n)*sup/F(factorial(q))<=F(q**q,factorial(q)*n**m))
  for zz in (F(0),F(1,100),F(1),F(4),F(100)):
   ck(f'endpoint majorant m{m} n{n} z{zz}',zz**q/(1+zz)**n<=sup)
# Weighted endpoint loss-power majorants, at integer powers s.
for m in range(1,6):
 for s in range(4):
  r=m+1+s; n=r+7
  maximum=F(r,n-r)**r/(1+F(r,n-r))**n
  ck(f'weighted endpoint m{m} s{s}',F(n**(s+1),factorial(m+1))*maximum<=F(r**r,factorial(m+1)*n**m))
# Noncommutation under support-dependent baseline, including an audit with zeros.
w3=(F(1,3),)*3; v3=(F(0),F(1),F(2)); ll=(F(0),F(1),F(1))
left=audit(step(w3,v3,F(1),2),ll)
right=(F(0),)+step((F(1,2),F(1,2)),(F(0),F(1)),F(1),2)
ck('adaptive support baseline fails',left!=right and left==(F(0),F(2,3),F(1,3)) and right==(F(0),F(5,7),F(2,7)))
# Positive audit and weight-dependent, nonnegative addition baseline.
lp=(F(1),F(2),F(4))
def adaptive(ww):
 c=sum(a*b for a,b in zip(ww,v3))
 return step(ww,tuple(x+c for x in v3),F(1),2)
ck('positive audit mean-dependent baseline fails',audit(adaptive(w3),lp)!=adaptive(audit(w3,lp)))
ck('not semigroup',step(step(w,v,F(1),2),v,F(1),2)!=step(w,v,F(2),2))
mu=(F(1,2),F(0),F(1,2)); nu=(F(0),F(1),F(0))
ck('same first moment',sum(a*b for a,b in zip(mu,v3))==sum(a*b for a,b in zip(nu,v3)))
ck('updated first moments differ',sum(a*b for a,b in zip(step(mu,v3,F(1),2),v3))==F(1,3) and sum(a*b for a,b in zip(step(nu,v3,F(1),2),v3))==1)
for K in range(1,8):
 # m=1 has nonzero rational finite difference at every order, giving exact arbitrary-K controls.
 weights=[F((-1)**i*int(sp.binomial(K+1,i))) for i in range(K+2)]
 ck(f'finite summary annihilator {K}',all(sum(weights[i]*i**j for i in range(K+2))==0 for j in range(K+1)))
 ck(f'finite summary normalizer differs {K}',sum(weights[i]/F(1+i) for i in range(K+2))!=0)
mp.mp.dps=70
diagnostics=[]
for m in range(1,5):
 def pm(x):return sum(x**j/mp.factorial(j) for j in range(m+1))
 def endpoint(n):
  a=[(mp.mpf(x.numerator)/x.denominator)/pm(mp.mpf(b.numerator)/b.denominator/n)**n for x,b in zip(w,v)]
  b=[(mp.mpf(x.numerator)/x.denominator)*mp.exp(-mp.mpf(y.numerator)/y.denominator) for x,y in zip(w,v)]
  return sum(abs(x/sum(a)-y/sum(b)) for x,y in zip(a,b))/2
 e1,e2=endpoint(50),endpoint(100)
 diagnostics.append({'m':m,'endpoint_error_n50':str(e1),'endpoint_error_n100':str(e2),'ratio':str(e1/e2)})
 ck(f'numerical endpoint trend {m}',mp.mpf(2)**(m-mp.mpf('.2'))<e1/e2<mp.mpf(2)**(m+mp.mpf('.2')))
# Exact loss damping is only polynomial; analytical Pareto proofs reside in RESULT.md.
out={'status':'PASS','control_count':len(checks),'numerical_control_count':len(diagnostics),'controls':checks,'numerical_diagnostics':diagnostics,'scope':'Finite exact/symbolic controls and labelled numerical diagnostics; universal measure proofs are in RESULT.md; not independent review or formal verification.'}
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('CHECKS.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','controls':len(checks),'output':str(path)}))
