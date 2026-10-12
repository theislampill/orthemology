from fractions import Fraction as F
from itertools import product
from math import comb,ceil
from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parents[1]
def losses(alpha,e,q):return q*q-F(1,4)-alpha*e*(1+e),(1-q)**2-F(1,4)+alpha*e*(1-e)
def fail(alpha,e,q):return int(not(0<=q<=1) or max(losses(alpha,e,q))>0)
radius=moment=constants=paired=0
for alpha,e in product([F(p,32) for p in range(1,32)],[F(1,4),F(1,8),F(1,16)]):
 v=alpha*(1-alpha);m=v*e*e;r=v*e/4
 assert losses(alpha,e,F(1,2)+e*alpha)==(-m,-m)
 for estimate in [alpha-r,alpha,alpha+r]:
  q=F(1,2)+e*estimate;assert 0<=q<=1 and max(losses(alpha,e,q))<=-m/4;radius+=1
 K=1/(v*e*e);N=ceil(28*K);aa=256/(v**3*e**4);bb=768/(v*v*e**4)
 assert K>=64 and N+aa/(2*N*N)+bb/N<56*K;constants+=1
 for q in [F(-1),F(0),F(1,2),F(1,2)+e*alpha,F(1,2)+e,F(1),F(2)]:
  for n in range(9):
   z=(1-alpha)**n;o=alpha**n
   assert fail(0,e,q)+z*fail(alpha,e,q)>=z
   assert fail(1,e,q)+o*fail(alpha,e,q)>=o
   paired+=2
for alpha,n in product([F(p,16) for p in range(1,16)],range(1,21)):
 v=alpha*(1-alpha);actual=sum(F(comb(n,k))*alpha**k*(1-alpha)**(n-k)*(F(k,n)-alpha)**4 for k in range(n+1))
 exact=(n*v*(1-3*v)+3*n*(n-1)*v*v)/n**4
 assert actual==exact and exact<=v/n**3+3*v*v/n**2;moment+=1

def report(kind,seed,w,e):
 n=len(w)
 if kind=='empirical':return F(1,2)+e*(F(sum(w),n) if n else 0)
 if kind=='balanced_0_half':return F(1,2)+e/2 if not n or any(w) else F(1,2)
 if kind=='random_initial_endpoints':return F(1,2)+e*seed if not n else F(1,2)+e*F(sum(w),n)
 raise ValueError(kind)
def partial(kind,alpha,e,N):
 out=F(0)
 for n in range(N+1):
  for w in product([0,1],repeat=n):
   p=alpha**sum(w)*(1-alpha)**(n-sum(w))
   for seed in [0,1]:out+=p*fail(alpha,e,report(kind,seed,w,e))/2
 return out
clock=0
for e,N in product([F(1,4),F(1,8)],range(8)):
 assert partial('empirical',0,e,N)==0 and partial('empirical',1,e,N)==1
 assert partial('balanced_0_half',0,e,N)==1
 assert partial('balanced_0_half',F(1,2),e,N)==1-F(1,2)**N
 assert partial('random_initial_endpoints',0,e,N)==F(1,2)
 assert partial('random_initial_endpoints',1,e,N)==F(1,2)
 for kind in ['empirical','balanced_0_half','random_initial_endpoints']:
  for alpha in [F(1,4),F(1,2),F(3,4)]:
   c0=partial(kind,0,e,N);c1=partial(kind,1,e,N);ca=partial(kind,alpha,e,N)
   assert c0+ca>=sum((1-alpha)**n for n in range(N+1))
   assert c1+ca>=sum(alpha**n for n in range(N+1));clock+=2
# Boundaries: zero disturbance, acceptance-boundary direction, forbidden shortcuts.
assert all(fail(a,0,F(1,2))==0 for a in [F(0),F(1,10),F(1)])
assert fail(0,F(1,4),F(1,2))==0 and all(fail(F(1,k),F(1,4),F(1,2))==1 for k in range(2,25))
assert all(fail(F(1,k),F(1,4),F(5,8))==1 for k in range(3,25))
assert F(1)<sum(F(3,4)**n for n in range(5)) # one evaluated report then stopping violates the infinite-report contract
out={'status':'FRESH_PASS_CONTINUUM_CONTROLS','radius_checks':radius,'central_moment_identities':moment,'upper_constant_checks':constants,'pointwise_pair_checks':paired,'finite_clock_pair_checks':clock,'endpoint_pair_0_half_minimax':1,'endpoint_pair_0_1_randomized_minimax':'1/2','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite geometry, moments and clock checks; Fatou, Tonelli and infinite lower bounds are ordinary proof obligations.'};(A/'CONTROL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
