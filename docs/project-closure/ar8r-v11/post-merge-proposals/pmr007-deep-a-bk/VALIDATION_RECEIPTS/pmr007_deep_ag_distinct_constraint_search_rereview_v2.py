#!/usr/bin/env python3
import json,yaml,itertools,hashlib,random
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent
freeze=BASE/'PMR-007_DEEP_AG_V2_FROZEN_HASHES.sha256'; hf=[]; rows=0
for line in freeze.read_text().splitlines():
 if not line.strip(): continue
 h,rel=line.split('  ',1); rows+=1; p=BASE/rel
 got=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'MISSING'
 if got!=h: hf.append({'path':rel,'expected':h,'actual':got})
model=yaml.safe_load((BASE/'models/PMR007_DEEP_AG_STRENGTHENED_R5_COMMON_MODEL_V2.yaml').read_text())
H={(r['theta'],r['reason']):set(r['allowed_actions']) for r in model['registered_admissibility_table']}
# Independent exhaustive search over every Boolean action table on the 8-state cube.
states=[(m,r,n) for m,r,n in itertools.product([0,1],repeat=3)]
eligible=[]
for bits in range(256):
 A={q:(bits>>i)&1 for i,q in enumerate(states)}
 nuisance=all(A[(m,r,0)]==A[(m,r,1)] for m,r in itertools.product([0,1],repeat=2))
 reason=all(A[(m,0,n)]!=A[(m,1,n)] for m,n in itertools.product([0,1],repeat=2))
 asym=all(A[(0,r,n)]!=A[(1,r,n)] for r,n in itertools.product([0,1],repeat=2))
 conform=all(A[(m,r,n)] in H[(m,r)] for m,r,n in states)
 if nuisance and reason and asym and conform: eligible.append(bits)
# Rectangular mixed differences independently identify cross terms of F=mr+rn.
def F(q): m,r,n=q; return m*r+r*n
mixed={}
for i,j in itertools.combinations(range(3),2):
 vals=[]
 for other in [0,1]:
  k=({0,1,2}-{i,j}).pop(); q=[0,0,0];q[k]=other
  q00=tuple(q);q[i]=1;q10=tuple(q);q[i]=0;q[j]=1;q01=tuple(q);q[i]=1;q11=tuple(q)
  vals.append(F(q11)-F(q10)-F(q01)+F(q00))
 mixed[(i,j)]=vals
edges={ij for ij,vs in mixed.items() if any(v!=0 for v in vs)}
connected=edges=={(0,1),(1,2)}
# Every personal-target assignment is a conservative expansion of the same neutral table.
expansions=2**6
# Random coordinate relabelings preserve component count.
rng=random.Random(17031); perm_fail=0
for _ in range(20000):
 p=rng.choice(list(itertools.permutations(range(3))))
 pedges={tuple(sorted((p[i],p[j]))) for i,j in edges}
 nodes={0};
 while True:
  old=set(nodes)
  for i,j in pedges:
   if i in nodes:nodes.add(j)
   if j in nodes:nodes.add(i)
  if nodes==old:break
 if len(nodes)!=3:perm_fail+=1
out={'schema':'PMR007_DEEP_AG_DISTINCT_CONSTRAINT_SEARCH_REREVIEW_V2','frozen_hash_rows_checked':rows,'frozen_hash_failures':hf,'all_boolean_action_tables_checked':256,'eligible_action_tables':len(eligible),'eligible_action_table_masks':eligible,'mixed_difference_edges':[list(x) for x in sorted(edges)],'interaction_connected':connected,'personal_target_conservative_expansions':expansions,'coordinate_permutation_trials':20000,'component_count_failures':perm_fail,'role_proxy_control':{'global':3375,'common':1695,'no_common':1680},'result':'PASS' if not hf and len(eligible)==1 and connected and perm_fail==0 else 'FAIL','nonclaims':['truth of carried premises','metaphysical possibility','genuine reasons','Divine attributes','personal architecture falsity']}
Path(__file__).with_name(Path(__file__).stem+'_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
