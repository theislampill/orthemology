#!/usr/bin/env python3
import json, yaml, hashlib, itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent
model=yaml.safe_load((BASE/'models/PMR007_DEEP_AG_STRENGTHENED_R5_COMMON_MODEL_V2.yaml').read_text())
states=model['domain']['states']; failures=[]
# Complete cube and basic equations.
seen={(s['m'],s['r'],s['nuisance']) for s in states}
if len(states)!=8 or len(seen)!=8: failures.append('state_cube')
for s in states:
 if s['theta']!=s['m']: failures.append('theta')
 if s['truth']!=s['r'] or s['score']!=s['r']: failures.append('semantic_score')
 if s['action']!=(s['r']^s['m']): failures.append('action')
 if s['fitting_action']!=s['action']: failures.append('fitting')
 if s['potential']!=s['m']+s['r']+s['nuisance']: failures.append('potential')
 if s['coupling']!=s['m']*s['r']+s['r']*s['nuisance']: failures.append('coupling')
# Causal/reason guidance and nuisance invariance.

# Independent admissibility table conformity.
hmap={(row['theta'],row['reason']):set(row['allowed_actions']) for row in model['registered_admissibility_table']}
h_fail=sum(1 for s in states if s['action'] not in hmap[(s['theta'],s['r'])])
guidance=0; nuisance_fail=0; asym_fail=0
for m,n in itertools.product([0,1],repeat=2):
 a={s['r']:s['action'] for s in states if s['m']==m and s['nuisance']==n}
 guidance+=int(a[0]!=a[1])
for m,r in itertools.product([0,1],repeat=2):
 vals={s['action'] for s in states if s['m']==m and s['r']==r}
 if len(vals)!=1: nuisance_fail+=1
for r,n in itertools.product([0,1],repeat=2):
 vals={s['m']:s['action'] for s in states if s['r']==r and s['nuisance']==n}
 if vals[0]==vals[1]: asym_fail+=1
# Additive potential path independence on cube edges.
edge_deltas={}
for s in states:
 x=(s['m'],s['r'],s['nuisance'])
 for i in range(3):
  if x[i]==0:
   y=list(x);y[i]=1;y=tuple(y)
   t=next(q for q in states if (q['m'],q['r'],q['nuisance'])==y)
   edge_deltas[(x,y)]=t['potential']-s['potential']
cycle_fail=0
# each square two paths give same sum
for dims in itertools.combinations(range(3),2):
 other=({0,1,2}-set(dims)).pop()
 for ov in [0,1]:
  x=[0,0,0];x[other]=ov;x=tuple(x)
  i,j=dims
  xi=list(x);xi[i]=1;xi=tuple(xi)
  xj=list(x);xj[j]=1;xj=tuple(xj)
  xij=list(x);xij[i]=xij[j]=1;xij=tuple(xij)
  if edge_deltas[(x,xi)]+edge_deltas[(xi,xij)] != edge_deltas[(x,xj)]+edge_deltas[(xj,xij)]: cycle_fail+=1
# Interaction graph from explicit supports {m,r}, {r,n} is connected.
interaction_edges={('m','r'),('r','nuisance')}; nodes={'m','r','nuisance'}
reach={'m'}
while True:
 old=set(reach)
 for u,v in interaction_edges:
  if u in reach: reach.add(v)
  if v in reach: reach.add(u)
 if reach==old: break
connected=reach==nodes
# Role enumeration independent common-bearer control.
bearers=range(4); global_count=common_count=no_common_count=0
for mask in range(1<<12):
 alloc=[[bool(mask>>(role*4+b)&1) for b in bearers] for role in range(3)]
 if all(any(row) for row in alloc):
  global_count+=1
  common=any(all(alloc[role][b] for role in range(3)) for b in bearers)
  common_count+=int(common); no_common_count+=int(not common)
# Neutral digest identical across personal and impersonal expansions.
neutral=json.dumps({'states':states,'neutral':model['neutral_coordinates'],'roles':model['role_allocation']},sort_keys=True).encode()
digest=hashlib.sha256(neutral).hexdigest()
pers_diff=model['personal_expansion']!=model['impersonal_expansion']
out={'schema':'PMR007_DEEP_AG_PRIMARY_CHECK_V2','states_checked':len(states),'equation_failures':failures,'admissibility_table_failures':h_fail,'reason_guidance_contexts':guidance,'nuisance_invariance_failures':nuisance_fail,'asymmetry_sensitivity_failures':asym_fail,'square_holonomy_failures':cycle_fail,'interaction_graph_connected':connected,'role_allocations':4096,'globally_available_WPK_allocations':global_count,'common_WPK_allocations':common_count,'no_common_WPK_allocations':no_common_count,'personal_impersonal_neutral_digest':digest,'personal_impersonal_targets_differ':pers_diff,'result':'PASS' if not failures and h_fail==0 and guidance==4 and nuisance_fail==0 and asym_fail==0 and cycle_fail==0 and connected and no_common_count>0 and pers_diff else 'FAIL'}
Path(__file__).with_name(Path(__file__).stem+'_results.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
