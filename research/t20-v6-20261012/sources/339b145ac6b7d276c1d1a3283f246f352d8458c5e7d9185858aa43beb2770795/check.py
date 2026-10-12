from fractions import Fraction as F
from pathlib import Path
import json
K=((F(1,8),F(1,8),F(1,8),F(5,8)),(F(1,8),F(1,8),F(5,8),F(1,8)))
L=((F(1,40),F(9,40),F(9,40),F(21,40)),(F(9,40),F(1,40),F(21,40),F(9,40)))
# Polynomials represented coefficient-low first. Exact identities support proofs
# on the entire real interval; finite samples below are only extra regressions.
def mul(a,b):
 o=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):o[i+j]+=x*y
 return o
def sub(a,b):return [(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
def deriv(a):return [i*a[i] for i in range(1,len(a))]
n=[F(3),F(-19),F(16)];d=[F(0),F(-13),F(16)]
num=sub(mul(deriv(n),d),mul(n,deriv(d)))
assert num==[F(39),F(-96),F(96),F(0)]
# derivative numerator = 96(p-1/2)^2 + 15 > 0.
assert num[:3]==[F(96)*F(1,4)+15,-96,96]
checks=0
for family in (K,L):
 for i in range(1001):
  t=F(i,1000);a,b,c,d=[(1-t)*x+t*y for x,y in zip(*family)]
  p=a+c; q=a/(a+b);r=a*(1-p)/(b*p)
  assert a+b==F(1,4) and min(a,b,c,d)>0
  assert p==F(1,4)+t/2
  assert q==(F(1,2) if family==K else F(1,10)+4*t/5)
  assert F(1,3)<=r<=3
  checks+=1
# Null vertices cannot supply arbitrary conditional laws. One possible and one
# impossible vertex condition to the possible vertex at every positive mixture.
v=(F(1,6),F(1,3),F(1,2));zero=(F(0),F(0),F(1))
for i in range(1,101):
 t=F(i,100); w=[t*x+(1-t)*z for x,z in zip(v,zero)]
 assert w[0]/(w[0]+w[1])==F(1,3)
# Curve convex-combination control: posterior sum a_i t_i² / sum a_i t_i;
# strict positivity holds analytically whenever denominator positive.
for i in range(101):
 for j in range(101):
  t,u=F(i,100),F(j,100)
  den=(t+u)/2
  if den:assert 0<(t*t+u*u)/(2*den)<=1
# Adopted stronger convex full-support boundary: every positive-event law has
# positive cells, but its exact posterior infimum is unattained.
full_support_boundary=0
for i in range(1,101):
 v=F(i,200)
 for j in range(101):
  u=v*v+F(j,100)*(v/2-v*v)
  row=(u,v-u,(1-v)/2,(1-v)/2)
  assert sum(row)==1 and min(row)>0 and 0<u/v<=F(1,2)
  full_support_boundary+=1
for j in range(1,101):
 q=F(j,200);v=q;u=q*q
 assert v*v<=u<=v/2 and u/v==q
result={'full_support_boundary_cases':full_support_boundary,'status':'PASS','segment_regression_cases':checks,'derivative_polynomial_coefficients':[str(x) for x in num], 'universal_sign_certificate':'96*(p-1/2)^2+15 > 0; denominator p^2*(16p-13)^2 > 0 on [1/4,3/4]', 'scope':'Independent ordinary algebra and exact finite controls, not kernel proof'}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
