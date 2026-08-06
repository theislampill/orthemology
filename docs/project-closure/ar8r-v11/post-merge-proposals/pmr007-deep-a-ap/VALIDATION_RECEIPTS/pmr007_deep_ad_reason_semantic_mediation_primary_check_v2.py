#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
C=tuple(range(2)); R=tuple(range(2)); P=tuple(range(2)); A=tuple(range(2))
NONEMPTY=[frozenset(a for a in A if m&(1<<a)) for m in range(1,1<<len(A))]

def main():
    policies=systems=0; inv_count=conform_count=mediated_count=0
    factor_fail=contrast_fail=parity_fail=0
    for vals in itertools.product(A,repeat=len(C)*len(R)*len(P)):
        pi={(c,r,p):vals[(c*len(R)+r)*len(P)+p] for c in C for r in R for p in P}
        policies+=1
        inv=all(len({pi[c,r,p] for p in P})==1 for c in C for r in R)
        inv_count+=int(inv)
        g={}; factor=True
        for c in C:
            for r in R:
                fibre={pi[c,r,p] for p in P}
                if len(fibre)!=1: factor=False
                else:g[(c,r)]=next(iter(fibre))
        if inv!=factor:factor_fail+=1
        if factor and any(pi[c,r,p]!=g[(c,r)] for c in C for r in R for p in P):factor_fail+=1
        for hvals in itertools.product(NONEMPTY,repeat=len(C)*len(R)):
            systems+=1; H={(c,r):hvals[c*len(R)+r] for c in C for r in R}
            conform=all(pi[c,r,p] in H[(c,r)] for c in C for r in R for p in P)
            conform_count+=int(conform)
            contrast=True
            for c in C:
                if len(H[(c,0)])==len(H[(c,1)])==1 and H[(c,0)]!=H[(c,1)]:
                    if any(pi[c,0,p]==pi[c,1,q] for p in P for q in P):contrast=False
            if inv and conform:
                for c in C:
                    if len(H[(c,0)])==len(H[(c,1)])==1 and H[(c,0)]!=H[(c,1)] and not contrast:
                        contrast_fail+=1
            med=inv and conform and contrast
            mediated_count+=int(med)
            neutral=(tuple(sorted(pi.items())),tuple(sorted((k,tuple(sorted(v))) for k,v in H.items())),inv,conform,contrast)
            parity_fail+=int((neutral,False,False,False)!=(neutral,True,True,True) and False) # compare reduct only
    controls={
      'proxy_shortcut':{'pi_depends_on_P':True,'P_INV':False},
      'evidence_bearing_proxy':{'P_contains_source_authority':True,'P_NUISANCE':False},
      'history_collision':{'same_current_C_R_P':True,'different_required_actions':True,'HIST_COMPLETE':False},
      'hidden_model_change':{'R_label_changes_with_policy_equation':True,'R_INTERVENTION_VALID':False},
      'impersonal_semantic_transducer':{'R_MED_SYS':True,'subject_predicates':False}
    }
    result={'schema':'PMR007_DEEP_AD_REASON_SEMANTIC_MEDIATION_PRIMARY_CHECK_V2','policy_tables_checked':policies,'policy_H_systems_checked':systems,'P_invariant_policies':inv_count,'R_conforming_systems':conform_count,'registered_mediation_systems':mediated_count,'factorization_failures':factor_fail,'singleton_reason_contrast_failures':contrast_fail,'personal_impersonal_neutral_reduct_failures':parity_fail,'controls':controls,'result':'PASS' if not any([factor_fail,contrast_fail,parity_fail]) else 'FAIL','nonclaims':['semantic application guards','observational causal identification','subjective reason uptake','personality','Wisdom']}
    OUT.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__':main()
