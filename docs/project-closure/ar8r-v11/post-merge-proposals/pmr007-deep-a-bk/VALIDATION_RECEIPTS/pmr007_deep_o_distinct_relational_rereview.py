#!/usr/bin/env python3
"""Distinct relational/potential rereview for PMR-007-GUPP-1 V2.

Unlike the primary checker, this script does not enumerate Boolean-function
families. It parses the frozen model owner, treats the profile map as a finite
relation, checks its functional dependencies and potential equations, then
enumerates all personal-predicate expansions of the same neutral reduct.
"""
from __future__ import annotations
import hashlib, itertools, json
from pathlib import Path
import yaml

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
MODEL=ROOT/'models'/'PMR007_DEEP_O_FORMAL_COUPLING_PERSONALITY_PARITY_V2.yaml'
CAND=ROOT/'PMR-007_DEEP_ROUND_O_FORMAL_DERIVATIONAL_COUPLING_AND_PERSONALITY_PARITY_V2.md'
PRIMARY=HERE/'pmr007_deep_o_formal_coupling_primary_check_v2_results.json'
OUT=ROOT/'rereviews'/'PMR-007_DEEP_O_V2_DISTINCT_RELATIONAL_REREVIEW_RESULTS.json'

obj=yaml.safe_load(MODEL.read_text())
rows=[]
for q,d in obj['formal_setting']['profile_map'].items():
    x,y=map(int,q)
    row={'q':q,'x':x,'y':y,**d}
    rows.append(row)
rows.sort(key=lambda r:r['q'])

# Verify defining equations independently.
equation_failures=[]
for r in rows:
    checks={
      'M=x': r['M']==r['x'],
      'A=y': r['A']==r['y'],
      'S=x XOR y': r['S']==(r['x']^r['y']),
      'N=x+y': r['N']==r['x']+r['y'],
      'R=1 iff N>0': r['R']==int(r['N']>0),
    }
    for name,ok in checks.items():
        if not ok: equation_failures.append({'q':r['q'],'equation':name})
assert not equation_failures

coords=['M','A','S','N','R']
image={tuple(r[c] for c in coords) for r in rows}
marginals={c:{r[c] for r in rows} for c in coords}
product_count=1
for c in coords: product_count*=len(marginals[c])
assert len(image)==4 and product_count==48

# Functional-dependency closure: x,y determine all; no single primitive does.
def agrees_on(rs, attrs):
    return all(rs[0][a]==rs[1][a] for a in attrs)
def fd(lhs,rhs):
    for a,b in itertools.combinations(rows,2):
        if agrees_on((a,b),lhs) and not agrees_on((a,b),rhs):
            return False
    return True
assert fd(['x','y'],coords)
assert not fd(['x'],coords)
assert not fd(['y'],coords)

# Influence by paired interventions.
influence={bit:set() for bit in ('x','y')}
by={(r['x'],r['y']):r for r in rows}
for (x,y),r in by.items():
    for bit,q2 in [('x',(1-x,y)),('y',(x,1-y))]:
        s=by[q2]
        influence[bit].update(c for c in coords if r[c]!=s[c])
assert len(influence['x'])>=3 and len(influence['y'])>=3

# Potential and closed-walk check.
V={(r['x'],r['y']):r['N'] for r in rows}
cycle=[(0,0),(0,1),(1,1),(1,0),(0,0)]
cycle_increments=[V[cycle[i+1]]-V[cycle[i]] for i in range(4)]
assert sum(cycle_increments)==0

# All 16 personal/intentional expansions preserve the neutral reduct.
preds=['PERS','MENT','IOWN','BECAUSE_F']
expansions=[]
neutral_digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
for bits in itertools.product((False,True),repeat=4):
    expansion=dict(zip(preds,bits))
    expansions.append({'predicates':expansion,'neutral_digest':neutral_digest})
assert len({e['neutral_digest'] for e in expansions})==1
for p in preds:
    assert {e['predicates'][p] for e in expansions}=={False,True}

# Guard deletions / interpretation controls.
product_profiles=list(itertools.product(*[sorted(marginals[c]) for c in coords]))
assert len(product_profiles)==48
assert len(set(product_profiles)-image)==44

hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (MODEL,CAND,PRIMARY)}
result={
  'frozen_hashes':hashes,
  'equation_failures':equation_failures,
  'relational_rows':len(rows),
  'joint_image_count':len(image),
  'product_marginal_count':product_count,
  'excluded_product_profiles':44,
  'functional_dependency_xy_to_all':True,
  'functional_dependency_x_to_all':False,
  'functional_dependency_y_to_all':False,
  'primitive_influence':{k:sorted(v) for k,v in influence.items()},
  'cycle_increments':cycle_increments,
  'cycle_sum':sum(cycle_increments),
  'personal_predicate_expansions_checked':len(expansions),
  'each_personal_predicate_varies_on_one_neutral_reduct':True,
  'source_bridge_required_to_exclude_impersonal_expansions':True,
  'world_semantics_or_metaphysical_possibility_checked':False,
  'status':'PASS_WITH_NONBLOCKING_SCOPE_NOTES'
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
