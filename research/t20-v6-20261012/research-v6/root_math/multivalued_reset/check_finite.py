"""Independent exhaustive finite-automaton check of coordinate factorisation.
No inherited theorem implementation is called. Python reference diagnostics,
not proof of the universal theorem or a cognitive model.
"""
from itertools import product
import json,hashlib,time
from pathlib import Path
root=Path(__file__).resolve().parent

def test(sizes,out,coupled):
 states=list(product(*(range(n) for n in sizes)));idx={x:i for i,x in enumerate(states)};N=len(states)
 reset=[]
 for k,n in enumerate(sizes):
  for a in range(n):
   reset.append(tuple(idx[x[:k]+(a,)+x[k+1:]] for x in states))
 actions=reset+list(coupled)
 rel={(i,j) for i in range(N) for j in range(N) if out[i]==out[j]}
 while True:
  new={(i,j) for i,j in rel if all((f[i],f[j]) in rel for f in actions)}
  if new==rel:break
  rel=new
 crel=[]
 for k,n in enumerate(sizes):
  crel.append({(a,b) for a in range(n) for b in range(n) if all((idx[z[:k]+(a,)+z[k+1:]],idx[z[:k]+(b,)+z[k+1:]]) in rel for z in states)})
 for i,x in enumerate(states):
  for j,y in enumerate(states):
   if ((i,j) in rel)!=all((x[k],y[k]) in crel[k] for k in range(len(sizes))):raise RuntimeError((sizes,out,coupled,x,y))
 return len({tuple(j for j in range(N) if (i,j) in rel) for i in range(N)})

t=time.monotonic();counts={}
for sizes in [(3,),(2,2)]:
 N=1
 for n in sizes:N*=n
 count=0
 for f in product(range(N),repeat=N):
  for out in product(range(2),repeat=N):test(sizes,out,[f]);count+=1
 counts[str(sizes)]=count
# A mixed-alphabet family: all64 outputs, all constant maps, identity,
# and all cyclic affine maps on the six enumerated states (deduplicated).
N=6;maps={tuple((a*i+b)%N for i in range(N)) for a in range(N) for b in range(N)}
count=0
for f in maps:
 for out in product(range(2),repeat=N):test((2,3),out,[f]);count+=1
counts['(2,3)_affine_family']=count
q1=test((3,),(0,0,1),[]);q2=test((3,),(0,0,1),[(0,2,2)])
if (q1,q2)!=(2,3):raise RuntimeError('ternary control failed')
# Finite coordinates without resets: parity can merge00/11 while contextual
# coordinate equivalence is equality. This is an explicit assumption control.
parity={(i,j) for i,x in enumerate(product(range(2),repeat=2)) for j,y in enumerate(product(range(2),repeat=2)) if sum(x)%2==sum(y)%2}
if (0,3) not in parity:raise RuntimeError('parity control failed')
r={'status':'PASS','model_counts':counts,'total_models':sum(counts.values()),'ternary_quotient_states_before_action':q1,'after_action':q2,'seconds':time.monotonic()-t,'scope':'All single coupled maps and Boolean observations on3 and4 states; selected exhaustive affine family on6 states; independent finite reference only.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(root/'FINITE_CHECK.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
