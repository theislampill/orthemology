"""Independent finite comparison: direct hidden paths versus descriptor rows."""
from fractions import Fraction as F
from itertools import product
from random import Random
from pathlib import Path
import json,hashlib
A=Path(__file__).resolve().parents[1];rng=Random(217409)
def validate(T,n,k=2):
 for q,a in product(range(n),range(k)):
  assert sum(T[q,a].values())==1 and min(T[q,a].values())>=0
  for o in [0,1]:
   if len({v for (z,v),p in T[q,a].items() if z==o and p>0})>1:raise ValueError('not posterior deterministic')
def obsprob(T,q,a,o):return sum(p for (z,v),p in T[q,a].items() if z==o)
def update(T,f,a,o):
 out=[]
 for q in f:
  possibilities=[] if q is None else [v for (z,v),p in T[q,a].items() if z==o and p>0]
  if len(set(possibilities))>1:raise ValueError('not posterior deterministic')
  out.append(possibilities[0] if possibilities else None)
 return tuple(out)
def lift(T,tags,h):
 states=[(tuple(tags),None)];actions=[]
 for a,o in h:states.append((update(T,states[-1][0],a,o),o));actions.append(a)
 return tuple(states),tuple(actions)
def project(states,actions):return tuple((a,s[1]) for a,s in zip(actions,states[1:]))
def probability(T,theta,h):
 dist={theta:F(1)}
 for a,o in h:
  nxt={}
  for q,p in dist.items():
   for (z,v),w in T[q,a].items():
    if z==o:nxt[v]=nxt.get(v,F(0))+p*w
  dist=nxt
 return sum(dist.values())
def row(T,tags,theta,s,a,off='reset'):
 f,last=s;q=f[tags.index(theta)]
 if q is None:return {(tuple(tags),None) if off=='reset' else s:F(1)}
 out={}
 for o in [0,1]:
  p=obsprob(T,q,a,o)
  if p:out[update(T,f,a,o),o]=p
 return out

def source_pi(seed,h):return (seed+len(h)+sum((i+1)*(a+2*o+1) for i,(a,o) in enumerate(h)))%2
def target_pi(seed,states,actions):
 return (seed+sum((i+1)*(sum(q+1 for q in f if q is not None)+(o+2 if o is not None else 0)) for i,(f,o) in enumerate(states))+sum(actions))%2

def original(T,tags,theta,seed,H,direction):
 paths={(theta,(),()):F(1)}
 for _ in range(H):
  nxt={}
  for (q,h,bad),p in paths.items():
   a=source_pi(seed,h) if direction=='source_to_target' else target_pi(seed,*lift(T,tags,h))
   nb=bad+(int(q%2!=a),)
   for (o,v),w in T[q,a].items():
    if w:key=(v,h+((a,o),),nb);nxt[key]=nxt.get(key,F(0))+p*w
  paths=nxt
 return {(h,bad,q):p for (q,h,bad),p in paths.items()}
def lifted(T,tags,theta,seed,H,direction,off):
 start=(tuple(tags),None);paths={((start,),(),()):F(1)}
 for _ in range(H):
  nxt={}
  for (states,actions,bad),p in paths.items():
   h=project(states,actions);assert lift(T,tags,h)==(states,actions)
   f,last=states[-1];domain={t for t,q in zip(tags,f) if q is not None};assert domain=={t for t in tags if probability(T,t,h)>0};assert theta in domain
   a=source_pi(seed,h) if direction=='source_to_target' else target_pi(seed,states,actions)
   nb=bad+(int(f[tags.index(theta)]%2!=a),)
   for ns,w in row(T,tags,theta,states[-1],a,off).items():
    key=(states+(ns,),actions+(a,),nb);nxt[key]=nxt.get(key,F(0))+p*w
  paths=nxt
 out={}
 for (states,actions,bad),p in paths.items():
  h=project(states,actions);q=states[-1][0][tags.index(theta)];assert q is not None;key=h,bad,q;out[key]=out.get(key,F(0))+p
 return out
comparisons=0;rows_checked=0;positive_cylinders=0
for system in range(24):
 n=2+system%2;tags=tuple(range(n));T={}
 for q,a in product(range(n),range(2)):
  p=rng.choice([F(0),F(1,4),F(1,2),F(3,4),F(1)]);T[q,a]={}
  for o,w in [(0,p),(1,1-p)]:
   if w:T[q,a][o,rng.randrange(n)]=w
 validate(T,n)
 for f,last in product(product([None]+list(range(n)),repeat=n),[None,0,1]):
  for theta,a,off in product(tags,range(2),['reset','stay']):assert sum(row(T,tags,theta,(f,last),a,off).values())==1;rows_checked+=1
 for theta,seed,H,direction in product(tags,[0,1,2],range(5),['source_to_target','target_to_source']):
  direct=original(T,tags,theta,seed,H,direction);assert sum(direct.values())==1
  for off in ['reset','stay']:
   assert direct==lifted(T,tags,theta,seed,H,direction,off);comparisons+=1;positive_cylinders+=len(direct)
# Distinct receipts can induce exactly the same descriptor.
T={(q,a):{(0,q):F(1,4) if q==0 else F(3,4),(1,q):F(3,4) if q==0 else F(1,4)} for q,a in product(range(2),range(2))}
f=(0,1);assert update(T,f,0,0)==update(T,f,0,1)==f
assert (update(T,f,0,0),0)!=(update(T,f,0,1),1)
assert obsprob(T,0,0,0)!=obsprob(T,1,0,0)
# Two initial tags merge in their current state without being eliminated.
T={(q,a):{(0,0):F(1,2),(1,0):F(1,2)} for q,a in product(range(2),range(2))}
merged=update(T,(0,1),0,0);assert merged==(0,0) and {t for t,q in enumerate(merged) if q is not None}=={0,1}
# A zero-probability observation eliminates only its impossible tag.
T={(q,a):{(q,q):F(1)} for q,a in product(range(2),range(2))};assert update(T,(0,1),0,0)==(0,None)
# Product marginals add impossible joint events and shift a current-state cost.
joint={(0,0):F(1,2),(1,1):F(1,2)};product_marginal={(o,q):F(1,4) for o,q in product(range(2),repeat=2)}
assert joint.get((0,1),0)==0 and product_marginal[0,1]>0
assert F(0)!=sum(w*int(q!=0) for (o,q),w in joint.items())==F(1,2)
# Non-PD input is rejected rather than selecting one arbitrary successor.
T={(q,a):{(0,0):F(1,2),(0,1):F(1,2)} for q,a in product(range(2),range(2))}
try:validate(T,2);raise AssertionError('accepted non-PD kernel')
except ValueError:pass
# A zero-prior state is not an additional adversarial initial tag.
T={(q,a):{(q,q):F(1)} for q,a in product(range(2),range(2))}
assert original(T,(0,),0,0,1,'source_to_target')==lifted(T,(0,),0,0,1,'source_to_target','reset')
from math import comb
commitment_cases=0
for n in range(81):
 for theta,p in [(0,F(1,4)),(1,F(3,4))]:
  error=sum(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1) if int(2*k>n)!=theta)
  assert error<=F(7,8)**n
  commitment_cases+=1
out={'status':'FRESH_PASS_PD_PATH_LAW_CONTROLS','systems':24,'finite_commitment_risk_bounds':commitment_cases,'fixed_tag_seed_horizon_direction_extension_comparisons':comparisons,'positive_cylinder_entries':positive_cylinders,'formal_rows_normalized':rows_checked,'boundaries':['last observation collision','merged tag retention','zero-probability elimination','off-domain irrelevance','joint versus product marginals','current-state clock','non-PD rejection','zero-prior scope'],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite joint hidden-state/observed-history/bad-sequence laws; the infinite policy correspondence and complexity theorem require ordinary proof.'};(A/'CONTROL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',comparisons,positive_cylinders,rows_checked)
