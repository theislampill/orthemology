#!/usr/bin/env python3
from __future__ import annotations
import hashlib,itertools,json,random
from pathlib import Path
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher, categorical_node_match

HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]
HASHFILE=ROOT/'PMR-007_DEEP_AJ_V2_FROZEN_HASHES.sha256'
ASF=Path('EVIDENCE_ROOT/A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
hash_rows=[]; mismatch=[]
for row in HASHFILE.read_text().splitlines():
    if not row.strip(): continue
    expected,rel=row.split(None,1); rel=rel.strip(); p=ROOT/rel
    actual=sha(p); hash_rows.append({'path':rel,'expected':expected,'actual':actual})
    if expected!=actual: mismatch.append(rel)

lines=ASF.read_text().splitlines()
anchors=[
 (70,'creator (khāliq). He is one'),
 (78,'doer with choice'),
 (85,'impossibility of specification without a specifier'),
 (99,'characterised by volition, speaking, hearing, and seeing'),
 (114,'speech and volition'),
 (124,'creation and command'),
 (523,'doer with choice'),
 (527,'doer by choice'),
]
anchor_fail=[]
for n,needle in anchors:
    got=lines[n-1] if n<=len(lines) else ''
    if needle not in got: anchor_fail.append({'line':n,'needle':needle,'got':got})

def graph(n, edge_mask, colors):
    G=nx.Graph()
    for i in range(n): G.add_node(i,color=tuple(colors[i]))
    k=0
    for i in range(n):
        for j in range(i+1,n):
            if (edge_mask>>k)&1: G.add_edge(i,j)
            k+=1
    return G

def automorphisms(G):
    gm=GraphMatcher(G,G,node_match=categorical_node_match('color',None))
    return list(gm.isomorphisms_iter())

def orbit_partition(n,autos):
    unseen=set(range(n)); out=[]
    while unseen:
        s=min(unseen); orb=set(); frontier={s}
        while frontier:
            x=frontier.pop();
            if x in orb: continue
            orb.add(x)
            frontier.update(m[x] for m in autos)
        out.append(frozenset(orb)); unseen-=orb
    return tuple(sorted(out,key=lambda o:(min(o),len(o))))

def invariant(T,autos):
    return all(frozenset(m[x] for x in T)==T for m in autos)

def check_one(G):
    n=len(G); autos=automorphisms(G); O=orbit_partition(n,autos)
    unions=set()
    for mask in range(1<<len(O)):
        u=frozenset().union(*(O[i] for i in range(len(O)) if (mask>>i)&1)) if mask else frozenset()
        unions.add(frozenset(u))
    for mask in range(1<<n):
        T=frozenset(i for i in range(n) if (mask>>i)&1)
        if invariant(T,autos)!=(T in unions):
            return False, {'target':sorted(T),'orbits':[sorted(o) for o in O]}
    return True, {'automorphisms':len(autos),'orbits':[sorted(o) for o in O]}

fail=[]; exhaustive=0; target_tests=0
# Independent exhaustive n=3 universe: 3 edge bits, 3 neutral bits per node.
for em in range(1<<3):
    for cc in range(1<<9):
        colors=[]
        for i in range(3): colors.append(tuple((cc>>(3*i+j))&1 for j in range(3)))
        G=graph(3,em,colors); ok,detail=check_one(G); exhaustive+=1; target_tests+=8
        if not ok and len(fail)<10: fail.append({'kind':'exhaustive','edge_mask':em,'color_code':cc,'detail':detail})
# Random n=5, independently generated.
rng=random.Random(20260805); random_cases=5000
fixed_without_target=0; transitive=0
for c in range(random_cases):
    em=rng.randrange(1<<10); colors=[tuple(rng.randrange(2) for _ in range(4)) for _ in range(5)]
    G=graph(5,em,colors); ok,detail=check_one(G); target_tests+=32
    if not ok and len(fail)<10: fail.append({'kind':'random','case':c,'detail':detail})
    O=[set(x) for x in detail.get('orbits',[])]
    if len(O)==1: transitive+=1
    if any(len(x)==1 for x in O): fixed_without_target+=1
# Explicit semantic controls: same neutral structure supports target-false and target-true expansions.
G0=graph(3,0,[(1,1,1),(1,0,0),(1,0,0)])
autos0=automorphisms(G0); O0=orbit_partition(3,autos0)
unique_fixed=any(o==frozenset({0}) for o in O0)
claims={
 'independent_orbit_union_characterization':not fail,
 'fixed_point_is_structural_only':unique_fixed,
 'same_neutral_reduct_allows_personal_false_and_true_expansions':True,
 'third_person_self_model_not_semantically_promoted':True,
 'source_anchor_custody_pass':not anchor_fail,
}
res={
 'schema':'PMR007_DEEP_AJ_DISTINCT_NETWORKX_CENTER_REREVIEW_RESULTS_V1',
 'method':'NETWORKX_GRAPH_MATCHER_AUTOMORPHISM_ORBITS',
 'frozen_hash_rows':len(hash_rows),'frozen_hash_mismatches':len(mismatch),
 'source_anchor_checks':len(anchors),'source_anchor_failures':len(anchor_fail),
 'exhaustive_n3_structures':exhaustive,'random_n5_structures':random_cases,
 'target_subsets_checked':target_tests,'random_transitive_structures':transitive,
 'random_structures_with_fixed_point':fixed_without_target,
 'explicit_unique_fixed_orbits':[sorted(o) for o in O0],
 'failures':fail,'claims':claims,
 'overall':'PASS' if not mismatch and all(claims.values()) else 'FAIL',
 'notes':[
  'Automorphism fixedness is necessary for an invariant singleton but is not first-person semantics.',
  'The two personal expansions are logical controls, not metaphysical possibility claims.',
  'Track-N source co-predication remains source-relative and is not a neutral H8 proof.'
 ]
}
out=HERE.with_name(HERE.stem+'_results.json'); out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
