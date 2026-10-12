#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import random,json,hashlib
BASE=Path(__file__).resolve().parents[1]
def d0(a,e,q):return q*q-F(1,4)-a*e*(1+e)
def d1(a,e,q):return (1-q)**2-F(1,4)+a*e*(1-e)
def bad(a,e,q):return not (0<=q<=1 and d0(a,e,q)<=0 and d1(a,e,q)<=0)
def mass(a,w):return a**sum(w)*(1-a)**(len(w)-sum(w))
margin=endpoint=moment=0
for den in [7,11,17]:
 for i in range(1,den):
  a=F(i,den);v=a*(1-a)
  for e in [F(1,16),F(1,8),F(1,4)]:
   for z in [F(-1),F(-1,2),F(0),F(1,2),F(1)]:
    b=a+z*v*e/4;q=F(1,2)+e*b;h=e*(b-a);m=v*e*e
    assert 0<=q<=1 and d0(a,e,q)<0 and d1(a,e,q)<0
    assert d0(a,e,q)==-m+(1+2*a*e)*h+h*h
    assert d1(a,e,q)==-m-(1-2*a*e)*h+h*h;margin+=1
  for n in range(1,10):
   exact=sum(F(comb(n,j))*a**j*(1-a)**(n-j)*(F(j,n)-a)**4 for j in range(n+1))
   assert exact==(n*v*(1-3*v)+3*n*(n-1)*v*v)/n**4;moment+=1
for e in [F(0),F(1,16),F(1,8),F(1,4)]:
 for j in range(-32,97):
  q=F(j,64);assert (not bad(F(0),e,q))==(q==F(1,2));assert (not bad(F(1),e,q))==(q==F(1,2)+e);endpoint+=2
assert F(28)+F(1,64)+F(1,98)+F(192,7)<56
rng=random.Random(126031);rho=[F(0),F(1,5),F(3,10),F(1,2)];grid=[F(0),F(1,2),F(9,16),F(5,8),F(3,4),F(1)]
paired=weighted=0
for trial in range(30):
 e=rng.choice([F(1,8),F(1,4)]);N=6
 table={(r,n,w):rng.choice(grid) for r in range(4) for n in range(N) for w in product([0,1],repeat=n)}
 p0=[sum(rho[r] for r in range(4) if table[r,n,(0,)*n]==F(1,2)) for n in range(N)]
 p1=[sum(rho[r] for r in range(4) if table[r,n,(1,)*n]==F(1,2)+e) for n in range(N)]
 C0=sum(1-p for p in p0);C1=sum(1-p for p in p1)
 for j in range(1,12):
  a=F(j,12);Ca=sum(mass(a,w)*sum(rho[r]*bad(a,e,table[r,n,w]) for r in range(4)) for n in range(N) for w in product([0,1],repeat=n))
  assert Ca>=sum((1-a)**n*p0[n] for n in range(N));assert Ca>=sum(a**n*p1[n] for n in range(N));weighted+=2
  assert Ca+C0>=sum((1-a)**n for n in range(N));assert Ca+C1>=sum(a**n for n in range(N));paired+=2
# Different endpoint pairs, same always-issued n=0 clock.
fixture=[]
for e in [F(1,16),F(1,4)]:
 qp=F(1,2)+e/2
 for N in range(1,9):
  costs=[]
  for a in [F(0),F(1,2)]:
   c=sum(mass(a,w)*bad(a,e,qp if n==0 or any(w) else F(1,2)) for n in range(N) for w in product([0,1],repeat=n));costs.append(c)
  assert costs==[F(1),1-F(1,2)**(N-1)]
  fixture.append({'pair':['0','1/2'],'N':N,'costs':list(map(str,costs))})
 # Pair{0,1}: fair initial randomization, then endpoint revealed by first bit.
 for a in [F(0),F(1)]:
  initial=sum(F(1,2)*bad(a,e,q) for q in [F(1,2),F(1,2)+e]);assert initial==F(1,2)
  assert not bad(a,e,F(1,2)+e*a)
# Exact lower event formula with seed-dependent endpoint settling times.
times=[0,2,5];weights=[F(1,5),F(3,10),F(1,2)];events=0;e=F(1,4)
for N in range(7):
 en=sum(w for w,t in zip(weights,times) if t<=N)
 for n in range(N,8):
  for a in [F(1,10),F(1,3),F(3,4)]:
   risk=F(0)
   for bits in product([0,1],repeat=n):
    for w,t in zip(weights,times):
     q=(F(1,2)+e*F(sum(bits),n)) if any(bits) else (F(1,2)+e/2 if n<t else F(1,2))
     risk+=w*mass(a,bits)*bad(a,e,q)
   assert risk>=en*(1-a)**n;events+=1
# Non-vacuous scope controls.
assert all(not bad(F(j,10),F(0),F(1,2)) for j in range(11))
assert d1(F(1,2),F(1,4),F(1,2))==F(3,32)
assert d0(F(1,2),F(1,4),F(3,4))==F(5,32)
# Seed R is a fair bit, receipt=R, E={R=1}: product factorization fails.
assert F(0)!=F(1,2)*F(1,2)
r={'status':'PASS_FRESH_EXACT_CONTROLS','margin_cases':margin,'endpoint_cases':endpoint,'fourth_moment_cases':moment,'finite_paired_bounds':paired,'weighted_prefix_bounds':weighted,'seed_event_bounds':events,'half_pair_finite_controls':fixture,'endpoint01_randomized_costs':['1/2','1/2'],'endpoint0half_limit_costs':['1','1'],'constant56_check':str(F(28)+F(1,64)+F(1,98)+F(192,7)),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Fresh rational finite corroboration. Infinite probability results require the ordinary proof; no old fourth receipt is recreated.'}
(BASE/'evidence/FRESH_CONTROLS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='half_pair_finite_controls'},indent=2))
