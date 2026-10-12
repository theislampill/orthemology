from fractions import Fraction as F
import json
p=[F(1,2),F(1,3),F(1,6)]
qs=[[F(1,3)]*3,[F(1,5),F(3,10),F(1,2)]]
rows=[]
for q in qs:
 for eps in [F(1,100),F(1,1000),F(1,10000)]:
  joint=[(pi-eps*qi,eps*qi) for pi,qi in zip(p,q)]
  assert all(a>0 and b>0 for a,b in joint)
  assert [sum(row) for row in joint]==p
  mass=sum(b for a,b in joint)
  post=[b/mass for a,b in joint]
  tv=sum(abs(a-pi)+abs(b) for pi,(a,b) in zip(p,joint))/2
  assert mass==eps and post==q and tv==eps
  rows.append({'epsilon':str(eps),'posterior':list(map(str,post)),'total_variation':str(tv)})
assert qs[0]!=qs[1]
print(json.dumps({'status':'PASS','arithmetic':'exact rational','cases':rows,'scope':'finite controls supplement the written general proof'},indent=2))
