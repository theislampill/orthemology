"""Conditional seed uniformity is sufficient, not necessary; participating check."""
from fractions import Fraction as F
from itertools import product
import json

def aggregate(xs, f):
    out={}
    for x,p in xs:
        y=f(x);out[y]=out.get(y,F(0))+p
    return out
base=[(bs,F(1,4)) for bs in product(range(2),repeat=2)]
# Same deterministic four-seed lookup at both steps: reply=floor(seed/2).
# U1=2B1; U2=2B2+B1. U2 deliberately retains B1 within reply fibres.
seeded=[((2*b1,2*b2+b1),p) for (b1,b2),p in base]
checks=[]
def check(n,b):
    if not b: raise RuntimeError(n)
    checks.append(n)
check('first_seed_nonuniform',aggregate(seeded,lambda u:u[0])=={0:F(1,2),2:F(1,2)})
check('same_joint_reply_law',aggregate(seeded,lambda u:(u[0]//2,u[1]//2))==dict(base))
check('hidden_seed_retains_past',all(u[1]%2==u[0]//2 for u,p in seeded))
for h in range(2):
    selected=[(u,p*2) for u,p in seeded if u[0]//2==h]
    check('nonuniform_given_history_'+str(h),len(aggregate(selected,lambda u:u[1]))==2)
    check('correct_conditional_reply_fibre_masses_'+str(h),aggregate(selected,lambda u:u[1]//2)=={0:F(1,2),1:F(1,2)})
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'scope':'Exact conditional output-fibre masses suffice. Seed freshness/uniformity is not necessary. Standard finite-probability application; no source authenticity or metaphysical warrant claim.'},indent=2))
