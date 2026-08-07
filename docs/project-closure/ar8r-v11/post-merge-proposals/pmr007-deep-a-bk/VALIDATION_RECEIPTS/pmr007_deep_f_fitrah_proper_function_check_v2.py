from itertools import product
from collections import defaultdict
from pathlib import Path
import json

# q=(accuracy,reliability,corrigibility,coherence)
# hidden=(source,designer,aim,fitrah,operation,environment,undefeated)
worlds=[]
for q in product([0,1], repeat=4):
    for h in product([0,1], repeat=7):
        src,des,aim,fit,op,env,und=h
        acc=q[0]
        nfunc=int(all([src,des,aim,fit,op,env]))
        nacc=int(nfunc and acc)
        nwarr=int(nacc and und)
        worlds.append({'q':q,'h':h,'nfunc':nfunc,'nacc':nacc,'nwarr':nwarr})

collisions={}
for target in ['nfunc','nacc','nwarr']:
    fibres=defaultdict(set)
    for w in worlds: fibres[w['q']].add(w[target])
    collisions[target]=sum(1 for vals in fibres.values() if len(vals)>1)

# Enriched coordinates determine every target.
enriched_fail=0
seen={}
for w in worlds:
    key=w['q']+w['h']
    vals=(w['nfunc'],w['nacc'],w['nwarr'])
    if key in seen and seen[key]!=vals: enriched_fail+=1
    seen[key]=vals

# Guard deletion at the appropriate level.
func_guards=['source','designer','truth_aim','fitrah_health','proper_operation','suitable_environment']
func_deletions=[]
for i,g in enumerate(func_guards):
    v=[1]*6;v[i]=0
    func_deletions.append({'guard':g,'nfunc':int(all(v))})
proper_function_episode_error={'nfunc':1,'accuracy':0,'nacc':0}
accurate_but_defeated={'nfunc':1,'accuracy':1,'undefeated':0,'nacc':1,'nwarr':0}
lucky_accuracy={'nfunc':0,'accuracy':1,'nacc':0}

# Same neutral profile, different realizations.
q=(1,1,1,1)
track_h=(1,1,1,1,1,1,1)
impersonal_h=(0,0,1,1,1,1,1)
def vals(q,h):
    src,des,aim,fit,op,env,und=h
    nf=int(all([src,des,aim,fit,op,env]));na=int(nf and q[0]);nw=int(na and und)
    return nf,na,nw
profile_twins={'q':q,'track_n':vals(q,track_h),'impersonal':vals(q,impersonal_h)}

out={
 'schema':'PMR007_DEEP_F_PRIMARY_CHECK_RESULTS_V2',
 'worlds_checked':len(worlds),
 'neutral_fibres':16,
 'collision_fibres':collisions,
 'all_three_fail_neutral_factorization':all(v>0 for v in collisions.values()),
 'enriched_factorization_failures':enriched_fail,
 'nfunc_guard_deletions':func_deletions,
 'all_nfunc_deletions_block':all(x['nfunc']==0 for x in func_deletions),
 'proper_function_episode_error':proper_function_episode_error,
 'accurate_but_defeated':accurate_but_defeated,
 'lucky_accuracy':lucky_accuracy,
 'profile_twins':profile_twins,
 'pass':all(v>0 for v in collisions.values()) and enriched_fail==0 and all(x['nfunc']==0 for x in func_deletions) and proper_function_episode_error=={'nfunc':1,'accuracy':0,'nacc':0} and accurate_but_defeated['nacc']==1 and accurate_but_defeated['nwarr']==0 and lucky_accuracy['nfunc']==0 and lucky_accuracy['nacc']==0 and profile_twins['track_n']==(1,1,1) and profile_twins['impersonal']==(0,0,0)
}
Path(__file__).with_name('pmr007_deep_f_fitrah_proper_function_check_v2_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
