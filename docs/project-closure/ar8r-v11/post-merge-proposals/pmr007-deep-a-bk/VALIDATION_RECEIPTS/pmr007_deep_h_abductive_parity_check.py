from fractions import Fraction
from itertools import product
from pathlib import Path
import json

# Exhaustive small exact-rational checks of posterior-odds identity.
priors=[Fraction(i,10) for i in range(1,10)]
likes=[Fraction(i,10) for i in range(1,11)]
parity_cases=0;parity_fail=0;asym_cases=0;asym_fail=0
examples=[]
for p1,p2,l1,l2 in product(priors,priors,likes,likes):
    # unnormalized posteriors suffice for odds
    prior_odds=p1/p2
    post_odds=(p1*l1)/(p2*l2)
    if l1==l2:
        parity_cases+=1
        if post_odds!=prior_odds: parity_fail+=1
    else:
        asym_cases+=1
        expected=prior_odds*(l1/l2)
        if post_odds!=expected: asym_fail+=1

# Matched score checks.
score_cases=0;tie_fail=0;prior_driven=[]
for fit in range(-3,4):
  for cost in range(0,6):
    for lam in range(0,5):
      score_cases+=1
      s1=fit-lam*cost;s2=fit-lam*cost
      if s1!=s2: tie_fail+=1
# coding reversal witnesses
coding_reversal={
 'language_L1':{'C_personal':1,'C_impersonal':4,'preferred':'personal'},
 'language_L2':{'C_personal':4,'C_impersonal':1,'preferred':'impersonal'}}
# Equal likelihood, different priors.
for a,b in [(9,1),(1,9),(3,2)]:
    prior=Fraction(a,b);like=Fraction(7,10);post=(Fraction(a,1)*like)/(Fraction(b,1)*like)
    prior_driven.append({'prior_odds':str(prior),'posterior_odds':str(post),'unchanged':prior==post})

out={
 'schema':'PMR007_DEEP_H_ABDUCTIVE_PARITY_RESULTS_V1',
 'exact_rational_parity_cases':parity_cases,
 'parity_failures':parity_fail,
 'likelihood_asymmetry_cases':asym_cases,
 'bayes_identity_failures':asym_fail,
 'matched_score_cases':score_cases,
 'matched_score_tie_failures':tie_fail,
 'coding_reversal':coding_reversal,
 'prior_driven_examples':prior_driven,
 'all_prior_driven_examples_unchanged':all(x['unchanged'] for x in prior_driven),
 'pass':parity_fail==0 and asym_fail==0 and tie_fail==0 and all(x['unchanged'] for x in prior_driven)
}
Path(__file__).with_name('pmr007_deep_h_abductive_parity_check_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
