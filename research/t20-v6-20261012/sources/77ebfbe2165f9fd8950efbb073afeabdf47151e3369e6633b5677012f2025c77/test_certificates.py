#!/usr/bin/env python3
from fractions import Fraction as F
from random import Random
from pathlib import Path
import json,datetime
rng=Random(924612);cases=0
for N in range(1,9):
 for dim in range(1,6):
  for k in range(25):
   v=[[F(rng.randint(-10,10),7) for _ in range(dim)] for _ in range(N)]
   if N>1:v[-1]=v[0][:]
   nums=[rng.randint(0,9) for _ in range(N)]
   if not sum(nums):nums[0]=1
   u=[F(x,sum(nums)) for x in nums]
   t=F(rng.randint(3,14),2);alpha=(t-1)/t;beta=1/t
   q=[sum(row[j] for row in v)/N for j in range(dim)]
   y=[sum(u[i]*v[i][j] for i in range(N)) for j in range(dim)]
   p=[alpha*q[j]+beta*y[j] for j in range(dim)]
   w=[alpha/N+beta*x for x in u]
   assert all(x>0 for x in w) and sum(w)==1
   assert [sum(w[i]*v[i][j] for i in range(N)) for j in range(dim)]==p
   assert [(1-t)*q[j]+t*p[j] for j in range(dim)]==y
   cases+=1
remainder=0
for n in range(1,65):
 e=F(1,n);D=[[F((k+1)*(j-1),n*n) for j in range(4)] for k in range(3)]
 eta=sum(abs(x) for row in D for x in row)
 assert all(x<=eta for row in D for x in row)
 assert eta/e==F(sum(abs((k+1)*(j-1)) for k in range(3) for j in range(4)),n)
 assert eta>0
 remainder+=1
res={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'centroid_extension_blend_cases':cases,'includes_singletons_and_duplicate_rows':True,'finite_common_remainder_cases':remainder,'scope':'Exact arithmetic identities for the certificate and finite remainder construction; topology and analytic limits are separately Lean checked.'}
Path(__file__).resolve().parents[1].joinpath('FINITE_CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
