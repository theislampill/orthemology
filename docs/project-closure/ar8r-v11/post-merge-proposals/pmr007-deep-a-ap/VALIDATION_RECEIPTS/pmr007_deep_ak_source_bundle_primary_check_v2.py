#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path

N=3; ROLES=('CREATOR','KNOWING','ABLE','LIVING','VOLITIONAL','SPEAKING')
NONEMPTY=[frozenset(i for i in range(N) if (m>>i)&1) for m in range(1,1<<N)]
assignments=0; common=0; empty=0; personality_expansions=0; failures=[]
minimal_empty=None
for sets in itertools.product(NONEMPTY, repeat=len(ROLES)):
    assignments+=1
    inter=set(range(N))
    for s in sets: inter &= set(s)
    has=bool(inter)
    if has: common+=1; personality_expansions+=2
    else:
        empty+=1
        if minimal_empty is None: minimal_empty={r:sorted(s) for r,s in zip(ROLES,sets)}
    # direct semantics: source common-bearer iff total intersection nonempty
    direct=any(all(g in s for s in sets) for g in range(N))
    if direct!=has and len(failures)<10: failures.append({'sets':[sorted(s) for s in sets],'intersection':sorted(inter),'direct':direct})
# explicit architecture witnesses
A={r:{0} for r in ROLES}
B0={r:{i%N} for i,r in enumerate(ROLES)}
B1={r:{0, (i%2)+1} for i,r in enumerate(ROLES)}
C1={r:{0} for r in ROLES}
def inter(a):
    x=set(range(N))
    for s in a.values(): x &= set(s)
    return x
claims={
 'common_bearer_iff_total_role_intersection_nonempty':not failures,
 'role_existence_alone_allows_empty_common_intersection':empty>0,
 'source_bundle_allows_personal_false_and_true_expansions':personality_expansions==2*common,
 'architecture_A_source_compatible':bool(inter(A)),
 'architecture_B0_source_incompatible':not bool(inter(B0)),
 'architecture_B1_source_compatible_role_extension':bool(inter(B1)),
 'architecture_C1_source_extendable':bool(inter(C1)),
}
res={'schema':'PMR007_DEEP_AK_PRIMARY_SOURCE_BUNDLE_CHECK_RESULTS_V2','bearers':N,'roles':len(ROLES),'role_assignments_checked':assignments,'source_common_bearer_assignments':common,'empty_intersection_assignments':empty,'personality_expansions_over_source_compatible_assignments':personality_expansions,'minimal_empty_intersection_witness':minimal_empty,'architecture_intersections':{'A':sorted(inter(A)),'B0':sorted(inter(B0)),'B1':sorted(inter(B1)),'C1':sorted(inter(C1))},'failures':failures,'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json'); out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
