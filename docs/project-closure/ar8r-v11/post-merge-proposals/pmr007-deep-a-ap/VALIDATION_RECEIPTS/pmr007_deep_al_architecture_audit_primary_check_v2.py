#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path

ARCH=('A','B1','C1')
common={'neutral_core','connected_derivation'}
benefits={
 'A':set(common)|{'source_bundle'},
 'B1':set(common)|{'source_bundle'},
 'C1':set(common)|{'source_bundle','order_actualizer_role'},
}
costs={
 'A':{'H7','H8','source_world'},
 'B1':{'powers_law','source_extension','brute_stop'},
 'C1':{'abstract_concrete_bridge','source_extension','brute_actuality'},
}
target_import={'A':{'personal','Wisdom'},'B1':set(),'C1':set()}
# Current evidence never credits target imports as benefits.
def dominates(x,y):
 return benefits[x]>=benefits[y] and costs[x]<=costs[y] and target_import[x]<=target_import[y] and (benefits[x]>benefits[y] or costs[x]<costs[y] or target_import[x]<target_import[y])
pairs={(x,y):dominates(x,y) for x in ARCH for y in ARCH if x!=y}
# Six open discriminators.  For each completion, assign winner only under a transparent rule:
# A needs u1,u2,u3,u6; B1 wins if u4 and not A qualification; C1 wins if u5 and not A qualification;
# ties/incomparability otherwise.  This is a sensitivity test, not canonical scoring.
counts={'A':0,'B1':0,'C1':0,'INCOMPARABLE':0,'MULTIPLE':0};examples={}
for vals in itertools.product([False,True],repeat=6):
 u1,u2,u3,u4,u5,u6=vals
 cand=[]
 if u1 and u2 and u3 and u6:cand.append('A')
 if u4:cand.append('B1')
 if u5:cand.append('C1')
 if len(cand)==0:key='INCOMPARABLE'
 elif len(cand)==1:key=cand[0]
 else:key='MULTIPLE'
 counts[key]+=1;examples.setdefault(key,vals)
claims={
 'no_current_pairwise_dominance_under_frozen_sets':not any(pairs.values()),
 'no_robust_champion_across_all_open_completions':all(counts[k]<64 for k in ['A','B1','C1']),
 'A_can_win_only_under_favorable_open_completion':counts['A']>0,
 'B1_can_remain_live_under_some_completion':counts['B1']>0 or counts['MULTIPLE']>0,
 'C1_can_remain_live_under_some_completion':counts['C1']>0 or counts['MULTIPLE']>0,
 'incomparable_completions_exist':counts['INCOMPARABLE']>0,
}
res={'schema':'PMR007_DEEP_AL_PRIMARY_ARCHITECTURE_AUDIT_RESULTS_V2','architectures':list(ARCH),'benefits':{k:sorted(v) for k,v in benefits.items()},'costs':{k:sorted(v) for k,v in costs.items()},'target_imports':{k:sorted(v) for k,v in target_import.items()},'pairwise_dominance':{f'{x}>{y}':v for (x,y),v in pairs.items()},'open_completions_checked':64,'completion_dispositions':counts,'completion_examples':{k:list(v) for k,v in examples.items()},'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json');out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');print(json.dumps(res,indent=2,sort_keys=True))
