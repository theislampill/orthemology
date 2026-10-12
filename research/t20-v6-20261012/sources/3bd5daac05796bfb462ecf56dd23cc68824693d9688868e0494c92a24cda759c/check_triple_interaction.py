from fractions import Fraction as F
from itertools import product,combinations
import json
rows=[]
for a in [F(1,5),F(1,2),F(4,5)]:
 rho=2*a-1
 law={b:(1+rho*(-1)**sum(b))/8 for b in product((0,1),repeat=3)}
 assert sum(law.values())==1 and all(p>0 for p in law.values())
 for inds in combinations(range(3),2):
  for vals in product((0,1),repeat=2):
   assert sum(p for bits,p in law.items() if tuple(bits[i] for i in inds)==vals)==F(1,4)
 assert sum(p*(-1)**sum(bits) for bits,p in law.items())==rho
 regret=F(0)
 for y,d in product((0,1),repeat=2):
  mass=sum(law[t,y,d] for t in (0,1))
  post=law[1,y,d]/mass
  assert post==(1-rho*(-1)**(y+d))/2
  regret+=mass*(post-F(1,2))**2
 assert regret==rho*rho/4
 rows.append({'accuracy':str(a),'interaction':str(rho),'half_Brier_regret':str(regret)})
print(json.dumps({'status':'PASS','arithmetic':'exact rational','cases':rows},indent=2))
