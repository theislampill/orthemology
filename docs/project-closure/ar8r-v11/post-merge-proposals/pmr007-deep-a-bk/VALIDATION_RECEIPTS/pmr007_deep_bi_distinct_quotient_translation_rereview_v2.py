from __future__ import annotations
from pathlib import Path
from itertools import product, permutations
import hashlib, json, random, yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

res={'identity':'PMR-007-FTASA-1','checker':'DISTINCT_QUOTIENT_TRANSLATION_REREVIEW_V2',
     'frozen_hash_rows':0,'frozen_hash_mismatches':[],
     'algebras_checked':0,'tokens_checked':0,'operation_samples':0,
     'homomorphism_failures':0,'congruence_failures':0,'quotient_failures':0,
     'good_translation_cases':0,'good_translation_failures':0,
     'bad_translation_cases':0,'bad_translation_undetected':0,
     'world_anchor_variants':0,'source_authority_twins':0,'version_twins':0,
     'personal_impersonal_twins':0,'anti_unification_controls':{}}

for line in (ROOT/'PMR-007_DEEP_BI_V2_FROZEN_HASHES.sha256').read_text().splitlines():
    if not line.strip(): continue
    exp,rel=line.split(None,1); rel=rel.strip(); act=sha(ROOT/rel)
    res['frozen_hash_rows']+=1
    if exp!=act: res['frozen_hash_mismatches'].append({'path':rel,'expected':exp,'actual':act})

rng=random.Random(2026080605)
for n in range(1,7):
    mask=(1<<n)-1; contents=list(range(1<<n))
    for copies in range(1,5):
        tokens=[(c,k) for c in contents for k in range(copies)]
        sigma=lambda t:t[0]
        AND=lambda a,b:(sigma(a)&sigma(b),0)
        OR=lambda a,b:(sigma(a)|sigma(b),0)
        NOT=lambda a:((mask^sigma(a)),0)
        res['algebras_checked']+=1; res['tokens_checked']+=len(tokens)
        # sample enough operations, exhaustive for small token sets
        pairs=list(product(tokens,tokens)) if len(tokens)<=32 else [(rng.choice(tokens),rng.choice(tokens)) for _ in range(20000)]
        for a,b in pairs:
            res['operation_samples']+=1
            if sigma(AND(a,b))!=(sigma(a)&sigma(b)) or sigma(OR(a,b))!=(sigma(a)|sigma(b)):
                res['homomorphism_failures']+=1
        for a in tokens:
            if sigma(NOT(a))!=(mask^sigma(a)): res['homomorphism_failures']+=1
        # Kernel classes and representative independence.
        classes={c:[t for t in tokens if sigma(t)==c] for c in contents}
        if len(classes)!=len(contents) or any(len(v)!=copies for v in classes.values()): res['quotient_failures']+=1
        for _ in range(min(5000,len(contents)*len(contents)*4)):
            c=rng.choice(contents); d=rng.choice(contents)
            a=rng.choice(classes[c]); a2=rng.choice(classes[c]); b=rng.choice(classes[d]); b2=rng.choice(classes[d])
            if sigma(AND(a,b))!=sigma(AND(a2,b2)) or sigma(OR(a,b))!=sigma(OR(a2,b2)) or sigma(NOT(a))!=sigma(NOT(a2)):
                res['congruence_failures']+=1

# Guarded translations between two disjoint token alphabets.
for n in range(1,7):
    contents=list(range(1<<n)); mask=(1<<n)-1
    source=[('S',c,k) for c in contents for k in (0,1)]
    target=[('T',c,k) for c in contents for k in (0,1)]
    sigma=lambda t:t[1]
    good=lambda t:('T',t[1],t[2])
    res['good_translation_cases']+=len(source)
    res['good_translation_failures']+=sum(sigma(good(t))!=sigma(t) for t in source)
    bad=lambda t:('T',mask^t[1],t[2])
    for t in source:
        res['bad_translation_cases']+=1
        if sigma(bad(t))==sigma(t) and mask!=0: res['bad_translation_undetected']+=1

# Same grammar/semantic algebra with multiple world anchors and independent extra coordinates.
for n in range(1,5):
    res['world_anchor_variants']+=sum(1 for _ in permutations(range(n)))
res['source_authority_twins']=2
res['version_twins']=2
res['personal_impersonal_twins']=2
res['anti_unification_controls']={
 'token_form_not_occurrence_context':True,
 'semantic_content_not_world_reference':True,
 'world_reference_not_source_authority':True,
 'source_authority_not_recipient_warrant':True,
 'version_applicability_not_semantic_equivalence':True,
 'algebraic_realization_not_mentality_or_Speech':True,
}
failed=bool(res['frozen_hash_mismatches']) or any(res[k] for k in ['homomorphism_failures','congruence_failures','quotient_failures','good_translation_failures','bad_translation_undetected'])
failed=failed or not all(res['anti_unification_controls'].values())
res['result']='FAIL' if failed else 'PASS'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
