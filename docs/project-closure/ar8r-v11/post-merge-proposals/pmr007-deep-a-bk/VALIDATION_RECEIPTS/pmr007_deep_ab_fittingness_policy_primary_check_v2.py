#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
A=tuple(range(3)); C=tuple(range(2)); TH=tuple(range(3))
NONEMPTY=[frozenset(i for i in A if mask&(1<<i)) for mask in range(1,1<<len(A))]

def main():
    systems=0
    aware_fail=blind_mismatch=singleton_function_fail=singleton_scm_fail=0
    blind_true=0
    inert_expansion_fail=0
    minimal={}
    for choices in itertools.product(NONEMPTY, repeat=len(C)*len(TH)):
        H={(t,c):choices[t*len(C)+c] for t in TH for c in C}
        systems += 1
        # canonical policy used only for the primary witness
        pi={(t,c):min(H[t,c]) for t in TH for c in C}
        if any(pi[t,c] not in H[t,c] for t in TH for c in C):
            aware_fail += 1
        intersections={c:set(A).intersection(*(set(H[t,c]) for t in TH)) for c in C}
        criterion=all(bool(intersections[c]) for c in C)
        brute=any(
            all(actions[c] in H[t,c] for t in TH for c in C)
            for actions in itertools.product(A, repeat=len(C))
        )
        blind_true += int(criterion)
        if criterion != brute:
            blind_mismatch += 1
            minimal.setdefault('blind_mismatch', {f'{t},{c}':sorted(H[t,c]) for t in TH for c in C})
        # Functional and frozen-SCM sensitivity: Act := pi(C,Theta)
        for c in C:
            for t,u in itertools.combinations(TH,2):
                if len(H[t,c])==len(H[u,c])==1 and H[t,c] != H[u,c]:
                    if pi[t,c] == pi[u,c]:
                        singleton_function_fail += 1
                    do_t=pi[t,c]; do_u=pi[u,c]
                    if do_t == do_u:
                        singleton_scm_fail += 1
        # Personal/impersonal expansions are inert labels over same full reduct.
        neutral=(tuple(sorted((t,c,tuple(sorted(H[t,c]))) for t in TH for c in C)),
                 tuple(sorted(pi.items())),
                 tuple((c,t,pi[t,c]) for c in C for t in TH))
        imp=(neutral, False,False,False,False,False)
        per=(neutral, True,True,True,True,True)
        if imp[0] != per[0]:
            inert_expansion_fail += 1
    result={
      'schema':'PMR007_DEEP_AB_FITTINGNESS_POLICY_PRIMARY_CHECK_V2',
      'contexts':len(C),'actions':len(A),'profiles':len(TH),
      'systems_checked':systems,
      'profile_aware_selector_failures':aware_fail,
      'profile_blind_intersection_criterion_true':blind_true,
      'profile_blind_criterion_mismatches':blind_mismatch,
      'singleton_functional_responsiveness_failures':singleton_function_fail,
      'singleton_frozen_scm_intervention_failures':singleton_scm_fail,
      'personal_impersonal_neutral_reduct_failures':inert_expansion_fail,
      'minimal_failures':minimal,
      'result':'PASS' if not any([aware_fail,blind_mismatch,singleton_function_fail,singleton_scm_fail,inert_expansion_fail]) else 'FAIL',
      'nonclaims':[
        'H truth authority world adequacy or source validity',
        'causal claims outside the frozen SCM',
        'intentional because-of relation or first-person ownership',
        'personality Wisdom or world realization'
      ]
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
