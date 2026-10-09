from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import random
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen'))
import countable_support as reference
import gcd_decoder as author
import oracle_boundaries as boundary

spec=importlib.util.spec_from_file_location('independent_gcd_review',ROOT/'independent_gcd_decoder.py')
independent=importlib.util.module_from_spec(spec)
spec.loader.exec_module(independent)
rng=random.Random(572091)
models=[{}, {1:1000}, {127:1}, {256:1}, {3:20,32:7}, {16:1,1:1}]
for _ in range(60):
    counts={e:n for e in range(1,33) if (n:=rng.randrange(4))}
    models.append(counts)
for model in models:
    q=independent.probability(model)
    expected,independent_trace=independent.decode(q)
    actual,trace=author.decode_gcd(q)
    assert expected==actual==model
    assert trace['largest_generator']==max(model,default=0)
    assert independent_trace['stopping_exponent']==trace['largest_generator']
    for row in trace['selectors']:
        assert all(row['checks'].values())
small_reference_cases=0
for _ in range(25):
    model={e:n for e in range(1,17) if (n:=rng.randrange(3))}
    q=independent.probability(model)
    assert reference.decode(q)[0]==independent.decode(q)[0]==author.decode_gcd(q)[0]==model
    small_reference_cases+=1

# Independent two-trial mixture arithmetic over a larger rational grid.
mixture_cases=0
for x in (F(1,10),F(1,3),F(1,2),F(2,3),F(9,10)):
    for y in (F(1,10),F(1,3),F(1,2),F(2,3),F(9,10)):
        left=(1-x,1-y)
        right=((1-x)*(1-y),1-x*y)
        assert sum(left)==sum(right)
        difference=(sum(v*v for v in right)-sum(v*v for v in left))/2
        assert difference==x*y*(1-x)*(1-y)>0
        mixture_cases+=1

# The candidate gap is computed from an already exact first response.
gap=boundary.inside_value_gap(F(9,16),max_inside_count=2)
assert gap['values']==(F(9,16),F(3,4),F(1))
assert gap['gap']==F(3,16)

receipt={'independent_lcm_vs_frozen_product_gcd_models':len(models),'three_way_prime_and_two_gcd_comparisons':small_reference_cases,'mixture_second_moment_grid':mixture_cases,'largest_support_code':256,'candidate_gap_checked':'q=9/16, R0={0}, values {9/16,3/4,1}, gap 3/16'}
(ROOT/'results/CROSSCHECK_METRICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
