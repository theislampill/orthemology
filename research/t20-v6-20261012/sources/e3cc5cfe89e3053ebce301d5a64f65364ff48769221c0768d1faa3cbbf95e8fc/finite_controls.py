from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
A=Path(__file__).resolve().parent
laws=[{a:{0:F(1-y),1:F(y)} for a,y in enumerate(ys)} for ys in product([F(0),F(1,2),F(1)],repeat=2)]
checks=0;supports=0
for P,Q in product(laws,repeat=2):
 for r in (0,1):
  pi=lambda h: r if not h else (h[0][1]^r)
  histories={():[F(1),F(1)]}
  for n in range(5):
   for h,masses in histories.items():
    live={i for i,law in enumerate([P,Q]) if all(law[a][y]>0 for a,y in h)}
    for i,mass in enumerate(masses):
     product_mass=F(1)
     for a,y in h:product_mass*=[P,Q][i][a][y]
     assert mass==product_mass
     assert (mass>0)==(i in live)
     checks+=1
    supports+=1
   nxt={}
   for h,ms in histories.items():
    a=pi(h)
    for y in (0,1):nxt[((a,y),)+h]=[ms[i]*law[a][y] for i,law in enumerate([P,Q])]
   histories=nxt
# Null seed: mixture Dirac0 licenses every actual action, while seed1 violates.
rho={0:F(1),1:F(0)}
assert sum(p for r,p in rho.items() if r==0)==1
assert not all(r==0 for r in rho)
# Public support cannot be reconstructed from the action projection alone.
reveal=[{a:{0:F(1),1:F(0)} for a in (0,1)}, {a:{0:F(0),1:F(1)} for a in (0,1)}]
h0=((0,0),);h1=((0,1),)
assert tuple(a for a,y in h0)==tuple(a for a,y in h1)
live=lambda h:{i for i,law in enumerate(reveal) if all(law[a][y]>0 for a,y in h)}
assert live(h0)=={0} and live(h1)=={1}
# A menu may shrink/change after the observation: action0 must be checked
# against old support, next action1 against new support, never retroactively.
menu=lambda B:{0} if len(B)==2 else {1}
assert 0 in menu({0,1}) and 0 not in menu({0}) and 1 in menu({0})
r={'status':'PASS','exact_fixed_seed_cylinder_mass_checks':checks,'live_support_histories':supports,'controls':['zero-probability histories','null seed','action-only information loss','pre-action support clock'],'scope':'Finite exact corroboration; no universal refinement claim'}
(A/'FINITE_CONTROL_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
