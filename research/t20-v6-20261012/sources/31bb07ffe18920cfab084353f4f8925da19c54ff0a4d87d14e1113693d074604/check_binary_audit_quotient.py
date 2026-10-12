from fractions import Fraction as F
from itertools import product
import json
states=set(tuple(F(x,sum(xs)) for x in xs) for xs in product(range(1,4),repeat=4))
def sig(p):
 # Coordinates (theta0,D0),(theta0,D1),(theta1,D0),(theta1,D1)
 return (p[2]+p[3],p[2]/(p[0]+p[2]),p[3]/(p[1]+p[3]))
def independent(p):
 q,a,b=sig(p)
 return a==b
count=0
for p in states:
 q,a,b=sig(p)
 if a!=b:
  t=(q-a)/(b-a)
  assert t==p[1]+p[3]
  assert ((1-t)*(1-a),t*(1-b),(1-t)*a,t*b)==p
 for r in states:
  assert (sig(p)==sig(r)) == (p==r or (independent(p) and independent(r) and sig(p)[0]==sig(r)[0]))
  count+=1
print(json.dumps({'status':'PASS','distinct_positive_joint_laws':len(states),'pair_checks':count,'scope':'exact controls supplement the ordinary fixed-audit quotient proof'},indent=2))
