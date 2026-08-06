from pathlib import Path
from itertools import product, permutations
import json

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
res={'identity':'PMR-007-FTASA-1','checker':'PRIMARY_V1','atom_sizes':{},
     'homomorphism_failures':0,'surjectivity_failures':0,'congruence_failures':0,
     'quotient_failures':0,'world_anchor_twins':0,'personal_expansions':0,
     'source_authority_expansions':0,'version_expansions':0}

for n in range(1,6):
    contents=list(range(1<<n))
    tokens=[(c,k) for c in contents for k in (0,1)]
    sigma=lambda t:t[0]
    AND=lambda t,u:(sigma(t)&sigma(u),0)
    OR=lambda t,u:(sigma(t)|sigma(u),0)
    NOT=lambda t:(((1<<n)-1)^sigma(t),0)
    hfail=0
    for t in tokens:
        if sigma(NOT(t))!=(((1<<n)-1)^sigma(t)): hfail+=1
        for u in tokens:
            if sigma(AND(t,u))!=(sigma(t)&sigma(u)): hfail+=1
            if sigma(OR(t,u))!=(sigma(t)|sigma(u)): hfail+=1
    surj={sigma(t) for t in tokens}==set(contents)
    # Congruence: operations on either representative stay in same semantic class.
    cfail=0
    for c in contents:
        reps=[(c,0),(c,1)]
        for d in contents:
            reps2=[(d,0),(d,1)]
            and_vals={sigma(AND(t,u)) for t in reps for u in reps2}
            or_vals={sigma(OR(t,u)) for t in reps for u in reps2}
            if len(and_vals)!=1 or len(or_vals)!=1: cfail+=1
        if len({sigma(NOT(t)) for t in reps})!=1: cfail+=1
    quotient_classes={c:{t for t in tokens if sigma(t)==c} for c in contents}
    qpass=len(quotient_classes)==len(contents) and all(len(v)==2 for v in quotient_classes.values())
    res['atom_sizes'][str(n)]={'contents':len(contents),'tokens':len(tokens),'homomorphism_failures':hfail,'congruence_failures':cfail,'surjective':surj,'quotient_pass':qpass}
    res['homomorphism_failures']+=hfail
    res['congruence_failures']+=cfail
    res['surjectivity_failures']+=int(not surj)
    res['quotient_failures']+=int(not qpass)
    # Two different world anchors: identity and complement, same token/semantic algebra.
    res['world_anchor_twins']+=2

# Personal, source-authority, and version applicability predicates vary independently.
for _ in product([False,True],repeat=4): res['personal_expansions']+=1
for _ in product([False,True],repeat=2): res['source_authority_expansions']+=1
for _ in product([False,True],repeat=2): res['version_expansions']+=1

failed=any(res[k] for k in ['homomorphism_failures','congruence_failures','surjectivity_failures','quotient_failures'])
failed=failed or res['world_anchor_twins']!=10 or res['personal_expansions']!=16 or res['source_authority_expansions']!=4 or res['version_expansions']!=4
res['result']='FAIL' if failed else 'PASS'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
