#!/usr/bin/env python3
"""Independent bounded test of map images, not an assessment of real norms."""
from itertools import product
import json
n=4
maps=[t for t in product(range(n), repeat=n) if all(t[t[x]]==t[x] for x in range(n))]
commutes={(i,j): all(a[b[x]]==b[a[x]] for x in range(n)) for i,a in enumerate(maps) for j,b in enumerate(maps)}
count=0
for i,a in enumerate(maps):
 for j,b in enumerate(maps):
  if not commutes[i,j]:continue
  for k,c in enumerate(maps):
   if not commutes[i,k] or not commutes[j,k]:continue
   count+=1
   target=set(a)&set(b)&set(c)
   endpoints={c[b[a[x]]] for x in range(n)}
   assert endpoints<=target
   assert endpoints==target
# A one-point image can be wholly wrong under the independently given target.
claimed_good=(0,0,0,0)
real_target={3}
assert all(claimed_good[claimed_good[x]]==claimed_good[x] for x in range(n))
assert not set(claimed_good)<=real_target
print(json.dumps({'domain':n,'idempotent_maps':len(maps),'ordered_commuting_triples':count,'joint_image_equals_intersection':True,'idempotence_without_semantic_adequacy_control':'REJECTED','scope':'Finite algebra only; neither real semantic certificates nor a general formal proof'},indent=2))
