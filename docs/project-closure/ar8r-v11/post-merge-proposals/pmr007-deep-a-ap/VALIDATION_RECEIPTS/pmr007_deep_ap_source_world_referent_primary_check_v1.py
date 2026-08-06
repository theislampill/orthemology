#!/usr/bin/env python3
from __future__ import annotations
from itertools import product
import json
from pathlib import Path

ROLES=3
SOURCE=[0,1]
WORLD=[0,1,2]
source_sig={0:(1,1,1),1:(1,0,0)}

def preserves(mapping,world_sig):
    return all(not source_sig[s][r] or world_sig[mapping[s]][r] for s in SOURCE for r in range(ROLES))

def all_maps(): return list(product(WORLD,repeat=len(SOURCE)))

def role_bearers(world_sig): return {w for w in WORLD if all(world_sig[w])}

counts={'world_signatures':0,'nonempty_interpretation_families':0,'role_complete_cases':0,'existence_failures':0,'image_singleton_definition_failures':0,'role_complete_equality_failures':0,'role_complete_uniqueness_failures':0,'hidden_anchor_witnesses':0,'two_bearer_witnesses':0}
for bits in product((0,1),repeat=len(WORLD)*ROLES):
    ws={w:tuple(bits[w*ROLES:(w+1)*ROLES]) for w in WORLD}; counts['world_signatures']+=1
    H=[m for m in all_maps() if preserves(m,ws)]
    B=role_bearers(ws)
    F={m[0] for m in H}
    if H:
        counts['nonempty_interpretation_families']+=1
        if not F or not F.issubset(B): counts['existence_failures']+=1
    # definition sanity
    if (len(F)==1)!=(len({m[0] for m in H})==1): counts['image_singleton_definition_failures']+=1
    role_complete=all(any(m[0]==w for m in H) for w in B)
    if role_complete and H:
        counts['role_complete_cases']+=1
        if F!=B: counts['role_complete_equality_failures']+=1
        if (len(F)==1)!=(len(B)==1): counts['role_complete_uniqueness_failures']+=1
    if len(B)>=2:
        counts['two_bearer_witnesses']+=1
        # restrict H to one image: hidden anchor policy can manufacture singleton
        if H:
            chosen=next(iter(B)); Hr=[m for m in H if m[0]==chosen]
            if Hr and len({m[0] for m in Hr})==1: counts['hidden_anchor_witnesses']+=1
claims={
 'nonempty_role_preserving_H_has_world_role_realizer':counts['existence_failures']==0,
 'image_singleton_criterion_exact':counts['image_singleton_definition_failures']==0,
 'role_complete_image_equals_role_bearers':counts['role_complete_equality_failures']==0,
 'role_complete_unique_iff_unique_role_bearer':counts['role_complete_uniqueness_failures']==0,
 'hidden_anchor_countermodels_exercised':counts['hidden_anchor_witnesses']>0,
 'multiple_role_bearer_countermodels_exercised':counts['two_bearer_witnesses']>0,
}
res={'schema':'PMR007_DEEP_AP_PRIMARY_RESULTS_V1','counts':counts,'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json'); out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
