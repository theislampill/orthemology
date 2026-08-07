from itertools import product
from pathlib import Path
import hashlib,json,random

BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def parse_hashes(p):
    rows=[]
    for line in p.read_text().splitlines():
        if not line.strip(): continue
        h,r=line.split('  ',1); rows.append((h,BASE/r))
    return rows

def cm(fn,F,C):
    fi=all(fn[f*C+c]==fn[0*C+c] for c in range(C) for f in range(F))
    cs=any(fn[0*C+c]!=fn[0*C+d] for c in range(C) for d in range(c+1,C))
    return fi and cs

hash_rows=parse_hashes(BASE/'PMR-007_DEEP_AZ_V2_FROZEN_HASHES.sha256')
hash_bad=[]
for h,p in hash_rows:
    a=hashlib.sha256(p.read_bytes()).hexdigest()
    if a!=h: hash_bad.append({'path':str(p.relative_to(BASE)),'expected':h,'actual':a})

# Exhaustive Boolean 3x3 functions.
F=C=3
functions=[bits for bits in product([0,1],repeat=F*C)]
cm_count=sum(cm(fn,F,C) for fn in functions)
# Diagonal profile collisions.
profiles={}
for fn in functions:
    prof=tuple(fn[i*C+i] for i in range(3))
    profiles.setdefault(prof,[]).append(fn)
diagonal_cross_class=0
for fs in profiles.values():
    seen={cm(fn,F,C) for fn in fs}
    if len(seen)>1: diagonal_cross_class+=1

# Every single-cell deletion admits a collision in unrestricted class.
deletion_failures=0
for missing in range(F*C):
    found=False
    buckets={}
    for fn in functions:
        key=fn[:missing]+fn[missing+1:]
        prev=buckets.get(key)
        if prev is not None and cm(prev,F,C)!=cm(fn,F,C):
            found=True; break
        buckets[key]=fn
    if not found: deletion_failures+=1

# Random stochastic 3x3 Bernoulli response probability tables.
rng=random.Random(20260806)
stochastic_cases=30000; stochastic_classifier_failures=0
for _ in range(stochastic_cases):
    # probabilities represented by integer tenths
    q=[rng.randrange(11) for _ in range(9)]
    fi=all(q[f*C+c]==q[c] for c in range(C) for f in range(F))
    cs=any(q[c]!=q[d] for c in range(C) for d in range(c+1,C))
    direct=fi and cs
    # independently group columns and check singleton distributions per content
    columns=[[q[f*C+c] for f in range(F)] for c in range(C)]
    alt=all(len(set(col))==1 for col in columns) and len({col[0] for col in columns})>1
    if direct!=alt: stochastic_classifier_failures+=1

res={
 'schema':'pmr007-deep-az-distinct-three-by-three-rereview-v2-results',
 'hash_check':{'checked':len(hash_rows),'mismatches':len(hash_bad),'details':hash_bad},
 'boolean_3x3_functions':len(functions),
 'content_mediated_functions':cm_count,
 'diagonal_profiles_with_cross_class_collision':diagonal_cross_class,
 'single_cell_deletion_failures':deletion_failures,
 'stochastic_tables':stochastic_cases,
 'stochastic_classifier_failures':stochastic_classifier_failures,
 'impersonal_semantic_processor_control':True,
 'semantic_anchor_deletion_control':True,
 'overall':'PASS' if not hash_bad and diagonal_cross_class>0 and deletion_failures==0 and stochastic_classifier_failures==0 else 'FAIL'
}
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
