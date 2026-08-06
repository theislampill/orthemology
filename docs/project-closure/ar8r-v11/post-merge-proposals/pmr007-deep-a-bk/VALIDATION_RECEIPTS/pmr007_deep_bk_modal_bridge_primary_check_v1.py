from itertools import product
import json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
W=range(2); D=range(2); w0=0
res={'identity':'PMR-007-NCBD-1','checker':'PRIMARY_V1','assignments':0,
     'actual_underived_models':0,'actual_to_necessary_countermodels':0,
     'unique_each_models':0,'unique_each_to_constant_bearer_countermodels':0,
     'full_guard_models':0,'full_guard_failures':0,'deletion_witnesses':{}}
# E,U,C bits for each w,x = 12 bits.
for bits in product([False,True],repeat=12):
    E={(w,x):bits[(w*2+x)*3] for w in W for x in D}
    U={(w,x):bits[(w*2+x)*3+1] for w in W for x in D}
    C={(w,x):bits[(w*2+x)*3+2] for w in W for x in D}
    root=lambda w,x:E[w,x] and U[w,x]
    actual=any(root(w0,x) for x in D)
    necessary=any(all(root(w,x) for w in W) for x in D)
    roots={w:[x for x in D if root(w,x)] for w in W}
    unique_each=all(len(roots[w])==1 for w in W)
    constant=unique_each and roots[0][0]==roots[1][0]
    full=constant and all(C[w,roots[w][0]] for w in W)
    conclusion=any(all(root(w,x) and C[w,x] for w in W) for x in D)
    res['assignments']+=1
    if actual:
        res['actual_underived_models']+=1
        if not necessary:res['actual_to_necessary_countermodels']+=1
    if unique_each:
        res['unique_each_models']+=1
        if not constant:res['unique_each_to_constant_bearer_countermodels']+=1
    if full:
        res['full_guard_models']+=1
        if not conclusion:res['full_guard_failures']+=1
# Explicit guard deletion witnesses.
res['deletion_witnesses']={
 'coverage': {'actual_root':True,'world1_root':False,'conclusion':False},
 'B_ID': {'world_roots':['r0','r1'],'coherent_counterpart':True,'same_bearer':False,'conclusion':False},
 'concreteness': {'same_root_all_worlds':True,'concrete_worlds':['w0'],'conclusion':False},
 'abstract_to_concrete': {'abstract_order_all_worlds':True,'concrete_bearer':False,'conclusion':False},
}
res['result']='PASS' if res['actual_to_necessary_countermodels']>0 and res['unique_each_to_constant_bearer_countermodels']>0 and res['full_guard_models']>0 and res['full_guard_failures']==0 else 'FAIL'
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
