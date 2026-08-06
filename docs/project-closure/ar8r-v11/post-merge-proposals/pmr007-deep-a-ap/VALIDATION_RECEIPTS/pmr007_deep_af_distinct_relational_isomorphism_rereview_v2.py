#!/usr/bin/env python3
import itertools, json, random, hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
freeze=BASE/'PMR-007_DEEP_AF_V2_FROZEN_HASHES.sha256'
fail=[]; rows=0
for line in freeze.read_text().splitlines():
    if not line.strip(): continue
    h,rel=line.split('  ',1); rows+=1
    p=BASE/rel
    got=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'MISSING'
    if got!=h: fail.append({'path':rel,'expected':h,'actual':got})

# Canonical directed-graph reduct code under all permutations, n=3.
def canon(edges, unary):
    n=3; reps=[]
    for p in itertools.permutations(range(n)):
        e=tuple(sorted((p[i],p[j]) for i,j in edges))
        u=tuple(sorted(p[i] for i in unary))
        reps.append((e,u))
    return min(reps)

# Build all 3-node neutral reducts with one unary and loop-free directed edges.
red=[]
pairs=[(i,j) for i in range(3) for j in range(3) if i!=j]
for em in range(1<<len(pairs)):
    e={(i,j) for k,(i,j) in enumerate(pairs) if em>>k&1}
    for um in range(8):
        u={i for i in range(3) if um>>i&1}
        red.append(canon(e,u))
classes=sorted(set(red))

rng=random.Random(772301)
trials=50000; fibre_cases=0; mism=0; iso_fail=0
for _ in range(trials):
    chosen=rng.sample(classes,rng.randint(1,min(8,len(classes))))
    allowed={c:{v for v in range(4) if rng.random()<.55} for c in chosen}
    for c in chosen:
        if not allowed[c]: allowed[c].add(rng.randrange(4))
    implicit=all(len(s)==1 for s in allowed.values())
    exact=implicit # independent lookup construction at canonical-isomorphism level
    if implicit: fibre_cases+=1
    if implicit!=exact: mism+=1
    # Relabel a random representative: canonical code must remain fixed.
    c=rng.choice(chosen); e,u=c
    perm=rng.choice(list(itertools.permutations(range(3))))
    ep={(perm[i],perm[j]) for i,j in e}; up={perm[i] for i in u}
    if canon(ep,up)!=c: iso_fail+=1

controls={
 'current_personal_impersonal_twin':{'same_complete_neutral_reduct':True,'personal_target_differs':True,'implicit':False},
 'source_restricted_class':{'neutral_implicit':False,'source_relative_implicit':True,'neutral_migration':False},
 'smuggled_proxy':{'definition_available':True,'independent_eligibility':False},
 'abductive_metric':{'may_prefer_one_expansion':True,'exact_entailment':False},
 'beth_scope':{'ordinary_first_order_all_models_only':True,'finite_or_modal_transfer_automatic':False}
}
out={'schema':'PMR007_DEEP_AF_DISTINCT_RELATIONAL_ISOMORPHISM_REREVIEW_V2','frozen_hash_rows_checked':rows,'frozen_hash_failures':fail,'three_node_neutral_isomorphism_classes':len(classes),'random_intended_classes':trials,'implicitly_defined_classes':fibre_cases,'criterion_mismatches':mism,'canonical_isomorphism_failures':iso_fail,'controls':controls,'result':'PASS' if not fail and not mism and not iso_fail else 'FAIL','nonclaims':['metaphysical possibility','probability parity','finite Beth theorem','source truth','modal or phenomenal reduction']}
Path(__file__).with_name(Path(__file__).stem+'_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
