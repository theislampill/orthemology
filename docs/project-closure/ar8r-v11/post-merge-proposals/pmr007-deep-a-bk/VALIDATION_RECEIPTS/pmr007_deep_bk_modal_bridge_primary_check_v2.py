from itertools import product
import json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
W=range(2); D=range(2); w0=0
res={'identity':'PMR-007-NCBD-1','checker':'PRIMARY_V2_CONSTANT_DOMAIN_REGRESSION',
     'semantic_scope':'constant global bearer domain is a regression special case, not authority for local occurrence B_ID',
     'assignments':0,'actual_models':0,'actual_nonpersistence_countermodels':0,
     'unique_each_models':0,'unique_each_distinct_bearer_countermodels':0,
     'guarded_models':0,'guarded_failures':0}
# E,Role,U,C = 16 bits.
for bits in product([False,True],repeat=16):
  E={};R={};U={};C={}
  for w in W:
    for x in D:
      i=(w*2+x)*4;E[w,x]=bits[i];R[w,x]=bits[i+1];U[w,x]=bits[i+2];C[w,x]=bits[i+3]
  root=lambda w,x:E[w,x] and R[w,x] and U[w,x]
  roots={w:[x for x in D if root(w,x)] for w in W}
  actual=bool(roots[w0]); necessary=any(all(root(w,x) for w in W) for x in D)
  unique=all(len(roots[w])==1 for w in W)
  same=unique and roots[0][0]==roots[1][0]
  guarded=same and all(C[w,roots[w][0]] for w in W)
  conclusion=any(all(root(w,x) and C[w,x] for w in W) for x in D)
  res['assignments']+=1
  if actual:
    res['actual_models']+=1
    if not necessary:res['actual_nonpersistence_countermodels']+=1
  if unique:
    res['unique_each_models']+=1
    if not same:res['unique_each_distinct_bearer_countermodels']+=1
  if guarded:
    res['guarded_models']+=1
    if not conclusion:res['guarded_failures']+=1
res['result']='PASS' if res['actual_nonpersistence_countermodels'] and res['unique_each_distinct_bearer_countermodels'] and res['guarded_models'] and not res['guarded_failures'] else 'FAIL'
OUT.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
