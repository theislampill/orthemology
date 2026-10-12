"""Finite settings-only control, not a theorem about original bearers."""
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
labels=tuple(range(3))
keys=list(combinations_with_replacement(labels,3))
fixed={(x,x,x):x for x in labels}
free=[k for k in keys if k not in fixed]
survivors=[]
for vals in product(labels, repeat=len(free)):
    table=dict(fixed); table.update(zip(free,vals))
    if all({table[tuple(sorted((a,b,c)))] for c in labels}==set(labels)
           for a,b in product(labels, repeat=2)):
        survivors.append(table)
result={'candidate_tables':3**len(free),'survivors':len(survivors),
 'hypotheses':['three positive output labels','settings-only unordered triple','unanimity','surjectivity in every slot with other two fixed'],
 'not_required':'full output-label permutation covariance',
 'limits':'Act-slot symmetry is not bearer-level agency. Ownership/provenance can change the domain. No exclusion of two original sources, no claim of new pure mathematics.'}
assert result['candidate_tables']==2187 and not survivors
Path(__file__).with_name('TERNARY_CENSUS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
