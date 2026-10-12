#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,datetime
binary=0
for xi,yi in product(range(1,32),repeat=2):
 x,y=F(xi,32),F(yi,32);q=(x+1-y)/2;defect=(x+y-1)**2
 assert 0<q<1
 assert q*q-x*(1-y)==defect/4
 assert (1-q)**2-(1-x)*y==defect/4
 assert (x-1)**2+y*y-((q-1)**2+(1-q)**2)==defect/2
 assert x*x+(y-1)**2-(q*q+((1-q)-1)**2)==defect/2
 binary+=1
# Entropy curvature / quadratic curvature varies, hence generators are not positive-affine.
assert (1/(F(1,2)*(1-F(1,2))))/2==2
assert (1/(F(1,4)*(1-F(1,4))))/2==F(8,3)
# Generic nonseparable positive-definite forms with identical simplex-normal action.
def q(v):return sum(x*x for x in v)
def r(v):return q(v)+(v[0]-v[1])**2
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
normal=0
for nums in product(range(-3,6),repeat=3):
 b=tuple(F(x,4) for x in nums);d=(sum(b)-1)/3;c=tuple(x-d for x in b)
 assert sum(c)==1
 for j in range(3):
  v=tuple(F(int(i==j)) for i in range(3))
  assert q(sub(b,v))-q(sub(c,v))==3*d*d
  assert r(sub(b,v))-r(sub(c,v))==3*d*d
  normal+=1
assert q((1,0,0))==q((0,0,1))==1
assert r((1,0,0))==2 and r((0,0,1))==1
# Distinct diagonal weights fail even pointwise projection compatibility.
def tangent_projection(h,w):
 recip=tuple(1/x for x in w);scale=sum(h)/sum(recip)
 return tuple(x-scale*y for x,y in zip(h,recip))
z1=tangent_projection((F(1),F(0),F(0)),(F(1),F(1),F(1)))
z2=tangent_projection((F(1),F(0),F(0)),(F(1),F(2),F(2)))
assert z1==(F(2,3),F(-1,3),F(-1,3)) and z2==(F(1,2),F(-1,4),F(-1,4)) and z1!=z2
# One-point curvature agreement does not make generators globally affine.
sdd=lambda x:2+12*(x-F(1,3))**2
assert sdd(F(1,3))==2 and sdd(F(1,2))!=2
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binary_rational_cases':binary,'nonseparable_normal_gain_cases':normal,'unequal_diagonal_projection_rejected':True,'one_point_curvature_counterexample':True,'scope':'Exact finite arithmetic controls; full analytic claims come from separately reviewed Lean proofs.'}
Path(__file__).resolve().parents[1].joinpath('FINITE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
