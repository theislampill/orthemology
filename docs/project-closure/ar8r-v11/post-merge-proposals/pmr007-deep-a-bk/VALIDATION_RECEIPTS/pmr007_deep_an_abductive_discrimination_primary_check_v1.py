#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
import itertools,json
from pathlib import Path

def grid_distributions(n=4,total=4):
    out=[]
    for xs in itertools.product(range(total+1),repeat=n):
        if sum(xs)==total: out.append(tuple(Fraction(x,total) for x in xs))
    return out

def likelihood(P,data):
    z=Fraction(1,1)
    for x in data: z*=P[x]
    return z

def posterior_odds(prior_odds,PA,PR,data):
    la,lr=likelihood(PA,data),likelihood(PR,data)
    if lr==0:
        return None if la==0 else 'INF'
    return prior_odds*la/lr

def prefix_free(words):
    vals=list(words.values())
    return all(not (i!=j and vals[j].startswith(vals[i])) for i in range(len(vals)) for j in range(len(vals)))

D=grid_distributions(); priors=[Fraction(1,3),Fraction(1,1),Fraction(3,1)]
counts={'distributions':len(D),'model_pairs':0,'evidence_sequences':0,'likelihood_parity_cases':0,'parity_failures':0,'different_models_without_event':0,'support_restriction_cases':0,'support_bayes_failures':0}
for PA in D:
  for PR in D:
    counts['model_pairs']+=1
    if PA!=PR and not any(PA[i]!=PR[i] for i in range(4)): counts['different_models_without_event']+=1
    for L in (0,1,2,3):
      for data in itertools.product(range(4),repeat=L):
        counts['evidence_sequences']+=1
        la,lr=likelihood(PA,data),likelihood(PR,data)
        if la==lr and la>0:
          counts['likelihood_parity_cases']+=1
          for o in priors:
            if posterior_odds(o,PA,PR,data)!=o: counts['parity_failures']+=1
# positive support-restriction family: A uniform on nonempty proper S, R uniform on Omega.
R=tuple(Fraction(1,4) for _ in range(4))
for mask in range(1,15):
    S=[i for i in range(4) if (mask>>i)&1]
    A=tuple(Fraction(1,len(S)) if i in S else Fraction(0) for i in range(4))
    for x in S:
        counts['support_restriction_cases']+=1
        bf=A[x]/R[x]
        if bf!=Fraction(4,len(S)): counts['support_bayes_failures']+=1
code_A={'A':'0','R':'10'}; code_R={'A':'10','R':'0'}
claims={
 'likelihood_parity_preserves_prior_odds':counts['parity_failures']==0,
 'distinct_finite_models_have_a_discriminating_event':counts['different_models_without_event']==0,
 'support_restriction_yields_declared_bayes_factor':counts['support_bayes_failures']==0,
 'prefix_codes_can_reverse_description_length_ranking':prefix_free(code_A) and prefix_free(code_R) and len(code_A['A'])<len(code_A['R']) and len(code_R['R'])<len(code_R['A']),
}
res={'schema':'PMR007_DEEP_AN_PRIMARY_RESULTS_V1','counts':counts,'code_controls':{'favor_A':code_A,'favor_R':code_R},'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json'); out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
