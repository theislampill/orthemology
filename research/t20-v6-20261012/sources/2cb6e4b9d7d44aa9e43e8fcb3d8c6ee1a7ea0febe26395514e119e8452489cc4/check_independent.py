#!/usr/bin/env python3
"""Independent exact controls; imports no author functions."""
from fractions import Fraction as R
from math import factorial
import json, pathlib
import sympy as S
import mpmath as M
checks=[]
def ck(name, v):
 if not bool(v): raise RuntimeError(name)
 checks.append(name)
def p(x,m): return sum((x**j/R(factorial(j)) for j in range(m+1)),R(0))
def tilt(w,a):
 raw=[x*y for x,y in zip(w,a)]; total=sum(raw)
 return [x/total for x in raw]
w=list(map(R,[1,3,5])); w=[x/sum(w) for x in w]; v=[R(0),R(2),R(7)]; L=[R(3),R(0),R(9)]
for m in range(1,10):
 for h in [R(0),R(1,13),R(3),R(101)]:
  a=[1/p(h*x,m) for x in v]; u=tilt(w,a)
  ck(f'probability {m} {h}',sum(u)==1 and all(x>0 for x in u))
  ck(f'audit {m} {h}',tilt(u,L)==tilt(tilt(w,L),a))
  ck(f'descent {m} {h}',sum(x*y for x,y in zip(u,v))<=sum(x*y for x,y in zip(w,v)))
  uu=w
  for j in range(5): uu=tilt(uu,a)
  ck(f'iteration {m} {h}',uu==tilt(w,[x**5 for x in a]))
  if h:
   for k in range(1,m+1): ck(f'moment {m} {h} {k}',all(x**k*y<=factorial(k)/h**k for x,y in zip(v,a)))
 z=S.Symbol('z'); pp=sum(z**j/S.factorial(j) for j in range(m+1))
 ck(f'local coefficient {m}',S.series(1/pp-S.exp(-z),z,0,m+2).removeO()==z**(m+1)/S.factorial(m+1))
 # Weighted maxima. Integer s controls supplement the real-s calculus proof.
 for s in range(5):
  r=m+1+s
  for n in [r+1,2*r,4*r]:
   peak=R(r,n-r); maximum=peak**r/(1+peak)**n
   ck(f'weighted maximum {m} {s} {n}', maximum==R(r,n)**r*R(n-r,n)**(n-r) and maximum<=R(r,n)**r)
   for x in [R(0),R(1,100),R(1),R(15),R(1000)]: ck(f'majorant sample {m} {s} {n} {x}',x**r/(1+x)**n<=maximum)
# Independent finite-summary example and baseline noncommutation.
ck('finite summary',tilt([R(1,2),R(1,2)],[1,1/p(R(2),2)])[1]*2==R(1,3))
u=tilt([R(1,3)]*3,[1,1/p(R(1),2),1/p(R(2),2)])
ck('support baseline',tilt(u,[0,1,1])!=[0]+tilt([R(1,2)]*2,[1,1/p(R(1),2)]))
# Numeric checks explicitly separate from exact controls.
M.mp.dps=80; numerics=[]
for m in range(1,6):
 q=m+1
 for n in [q,2*q,10*q]:
  for x in [M.mpf('1e-4'),M.mpf('.3'),M.mpf(1),M.mpf(20)]:
   a=1/sum(x**j/M.factorial(j) for j in range(m+1)); b=M.exp(-x)
   err=a**n-b**n; bound=n*x**q*a**n/M.factorial(q)
   if not (-M.mpf('1e-75')<=err<=bound+M.mpf('1e-75')):raise RuntimeError('numeric telescoping')
   numerics.append([m,n,str(x)])
out={'status':'PASS','exact_symbolic_controls':len(checks),'numeric_telescoping_controls':len(numerics),'checks':checks,'scope':'Finite controls supplement independent universal proof review, not formal verification.'}
pathlib.Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
