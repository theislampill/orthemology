from fractions import Fraction as F
from math import prod
from pathlib import Path
import json
counts={}
def ck(k,v):
 assert v,k
 counts[k]=counts.get(k,0)+1
# Infinite support: x0=0, xj=2^-j. Effective cap cj=2^-j has total 2.
# Each finite perturbation leaves all other positive seed coordinates cj/2 unchanged.
for R in range(9):
 N=R+2; xs=[F(0)]+[F(1,2**j) for j in range(1,N)]
 c=[F(1,2**j) for j in range(N)]; w=[a/2 for a in c]
 h=[1/prod(xs[j]-xs[k] for k in range(N) if k!=j) for j in range(N)]
 e=min(c[j]/(4*abs(h[j])) for j in range(N))
 wp=[w[j]+e*h[j] for j in range(N)]; wm=[w[j]-e*h[j] for j in range(N)]
 ck('nonzero_normalized_perturbation',any(h) and sum(h)==0)
 ck('strict_cap_feasibility',all(0<wp[j]<c[j] and 0<wm[j]<c[j] for j in range(N)))
 for r in range(R+1):
  for a in range(r+1):
   ck('full_binary_tensor_equality',sum((wp[j]-wm[j])*xs[j]**a*(1-xs[j])**(r-a) for j in range(N))==0)
 ck('later_moment_distinction',sum((wp[j]-wm[j])*xs[j]**(R+1) for j in range(N))!=0)
# No-cap point masses: input moments converge coordinatewise to the supported x0=0 atom.
for j in range(1,17):
 x=F(1,2**j)
 for r in range(1,17):
  for a in range(r+1):
   d=abs(x**a*(1-x)**(r-a)-(F(1) if a==0 else F(0)))
   ck('accumulation_moment_bound',d<=r*x)
 ck('escaping_mass_excluded_by_cap',F(1)>F(1,2**j))
# Two known support atoms 0 and 1: grade 1 max norm is exactly half l1 weight error.
for a in range(17):
 for b in range(17):
  p=F(a,16);q=F(b,16)
  ck('finite_precision_inverse_control',2*abs(p-q)==abs(p-q)+abs((1-p)-(1-q)))
out={'status':'PASS','checks':counts,'total':sum(counts.values()),'scope':'Exact finite corroboration; no universal, effective-compactness or noncomputability claim from execution.'}
p=Path(__file__).resolve().parents[1]/'INDEPENDENT_CHECKS.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
