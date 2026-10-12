#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as Q
from math import comb, factorial, ceil
from itertools import product
import runpy, json, time, hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
source=runpy.run_path(str(ROOT/'full-polynomial-moment-countermodel-20261010/countermodel.py'),run_name='inherited_schur')
model=source['SchurMoment']()
def indices(n): return [(a,n-a) for a in range(n+1)]
def moment(mu,alpha): return sum((w*p[0]**alpha[0]*p[1]**alpha[1] for p,w in mu.items()),Q(0))
def add(mu,other):
 for p,w in other.items():
  mu[p]=mu.get(p,Q(0))+w
  if not mu[p]: del mu[p]
def F(p):
 u,v=p
 return 1+u**4*v**2+u**2*v**4-u**2*v**2
rho={(0,0):Q(1)}; N={}; prev=0; rows=[]; start=time.perf_counter()
for n in range(1,7):
 residual={a:model.moment(*a)-moment(rho,a) for a in indices(n)}
 B=sum((abs(r)*Q(2**n,factorial(a[0])*factorial(a[1])) for a,r in residual.items()),Q(0))
 R=max(1,prev+1,ceil(2**n*n**(n-1)*B)); block={}
 for a,r in residual.items():
  if not r: continue
  denom=factorial(a[0])*factorial(a[1])*R**n
  for j in product(range(a[0]+1),range(a[1]+1)):
   p=(R*j[0],R*j[1])
   block[p]=block.get(p,Q(0))+r*Q((-1)**(n-sum(j))*comb(a[0],j[0])*comb(a[1],j[1]),denom)
 block={p:w for p,w in block.items() if w}
 for m in range(n): assert sum((abs(w)*sum(p)**m for p,w in block.items()),Q(0))<=Q(1,2**n)
 add(rho,block); add(N,{p:-w for p,w in block.items() if w<0})
 for degree in range(n+1):
  for a in indices(degree): assert moment(rho,a)==model.moment(*a)
 nf=sum((w*F(p) for p,w in N.items()),Q(0))
 rows.append({'degree':n,'radius':str(R),'radius_bits':R.bit_length(),'block_atoms':len(block),'N_F_num_bits':nf.numerator.bit_length(),'N_F_den_bits':nf.denominator.bit_length(),'N_F_log2_floor':nf.numerator.bit_length()-nf.denominator.bit_length()})
 prev=R
assert sum((w*F(p) for p,w in rho.items()),Q(0))==-1
upper=nf+Q(1,16)
bits=upper.numerator.bit_length()-upper.denominator.bit_length()+1
while upper>=2**bits: bits+=1
while bits and upper<2**(bits-1): bits-=1
assert upper<2**bits
result={'status':'PASS','N_F_prefix':str(nf),'N_F_upper':str(upper),'N_F_upper_power2_exponent':bits,'rows':rows,'elapsed_seconds':time.perf_counter()-start,'schur_maximum_index':len(model.j),'source_sha256':hashlib.sha256((ROOT/'full-polynomial-moment-countermodel-20261010/countermodel.py').read_bytes()).hexdigest()}
(HERE/'HIDDEN_BOUND.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['N_F_prefix','N_F_upper']},indent=2))
