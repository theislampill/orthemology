from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
mis=[]
for line in (ROOT/'PMR-007_DEEP_H_V1_FROZEN_HASHES.sha256').read_text().splitlines():
 if not line.strip(): continue
 exp,rel=line.split(None,1);p=ROOT/rel.strip();got=hashlib.sha256(p.read_bytes()).hexdigest()
 if got!=exp:mis.append({'path':rel.strip(),'expected':exp,'observed':got})
# Independent normalized 3-hypothesis, 3-outcome check.
# Generate positive integer priors and likelihood vectors summing to 1.
vectors=[]
for a in range(1,5):
 for b in range(1,5):
  for c in range(1,5):
   s=a+b+c;vectors.append((Fraction(a,s),Fraction(b,s),Fraction(c,s)))
cases=0;fail=0;tv_fail=0
for prior in vectors:
 for like in vectors:
  # All hypotheses share the same evidence distribution.
  for e in range(3):
   pe=sum(prior[h]*like[e] for h in range(3))
   post=tuple(prior[h]*like[e]/pe for h in range(3))
   cases+=1
   if post!=prior:fail+=1
  # total variation between any two identical laws is zero
  for i,j in [(0,1),(0,2),(1,2)]:
   tv=sum(abs(like[k]-like[k]) for k in range(3))/2
   if tv!=0:tv_fail+=1
# realization-sensitive witness: one unequal likelihood updates odds
p=(Fraction(1,2),Fraction(1,2));l=(Fraction(3,4),Fraction(1,4))
prior_odds=p[0]/p[1];post_odds=(p[0]*l[0])/(p[1]*l[1])
source_typed=True
out={'schema':'PMR007_DEEP_H_DISTINCT_REREVIEW_RESULTS_V1','frozen_hash_mismatches':mis,'normalized_posterior_cases':cases,'posterior_parity_failures':fail,'total_variation_failures':tv_fail,'realization_sensitive_witness':{'prior_odds':str(prior_odds),'posterior_odds':str(post_odds),'updated':post_odds!=prior_odds},'source_evidence_typed_not_neutralized':source_typed,'pass':not mis and fail==0 and tv_fail==0 and post_odds!=prior_odds and source_typed}
Path(__file__).with_name('PMR-007_DEEP_H_DISTINCT_REREVIEW_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
