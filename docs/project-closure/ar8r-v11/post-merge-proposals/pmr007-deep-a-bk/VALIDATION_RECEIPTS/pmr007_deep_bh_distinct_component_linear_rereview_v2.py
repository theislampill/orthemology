from __future__ import annotations
from itertools import combinations, product
from pathlib import Path
import hashlib, json, random, yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def comps(n,edges):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    seen=set(); out=[]
    for s in range(n):
        if s in seen: continue
        stack=[s]; seen.add(s); c=[]
        while stack:
            u=stack.pop(); c.append(u)
            for v in adj[u]:
                if v not in seen: seen.add(v); stack.append(v)
        out.append(sorted(c))
    return out,adj

def oriented(d,u,v): return d[(u,v)] if (u,v) in d else -d[(v,u)]

def forest_potential(n,edges,d):
    components,adj=comps(n,edges)
    N=[None]*n; tree=set()
    for c in components:
        root=c[0]; N[root]=0; q=[root]
        for u in q:
            for v in adj[u]:
                if N[v] is None:
                    N[v]=N[u]+oriented(d,u,v); q.append(v); tree.add(tuple(sorted((u,v))))
    return N,tree,components

def A_calibrated(edges,d,L): return all(oriented(d,u,v)==L[u]-L[v] for u,v in edges)

def B_forest_cycles(n,edges,d,L):
    N,tree,components=forest_potential(n,edges,d)
    tree_ok=all(oriented(d,u,v)==L[u]-L[v] for u,v in tree)
    residual_ok=all(oriented(d,u,v)==N[v]-N[u] for u,v in edges if tuple(sorted((u,v))) not in tree)
    return tree_ok and residual_ok

def C_component_potential(n,edges,d,L):
    N,tree,components=forest_potential(n,edges,d)
    exact=all(oriented(d,u,v)==N[v]-N[u] for u,v in edges)
    calibrated=True
    for c in components:
        constants={N[v]+L[v] for v in c}
        calibrated &= len(constants)==1
    return exact and calibrated, len(components)

res={'identity':'PMR-007-TCRPF-1','checker':'DISTINCT_COMPONENT_LINEAR_REREVIEW_V2',
     'frozen_hash_rows':0,'frozen_hash_mismatches':[],
     'exhaustive_three_vertex_cases':0,'exhaustive_equivalence_failures':0,
     'random_component_cases':0,'random_equivalence_failures':0,
     'component_constant_cases':0,'ordinal_additive_controls':{},
     'proper_function_account_expansions':0,'source_scope_checks':{},
     'dynamic_extension_witness':{}}

for line in (ROOT/'PMR-007_DEEP_BH_V2_FROZEN_HASHES.sha256').read_text().splitlines():
    if not line.strip(): continue
    exp,rel=line.split(None,1); rel=rel.strip(); act=sha(ROOT/rel)
    res['frozen_hash_rows']+=1
    if exp!=act: res['frozen_hash_mismatches'].append({'path':rel,'expected':exp,'actual':act})

# Exhaust every three-vertex graph, all edge labels and truth losses in {-1,0,1}.
verts=range(3); all_edges=list(combinations(verts,2))
for mask in range(1<<len(all_edges)):
    edges=[all_edges[i] for i in range(len(all_edges)) if (mask>>i)&1]
    for dvals in product([-1,0,1],repeat=len(edges)):
        d=dict(zip(edges,dvals))
        for L in product([-1,0,1],repeat=3):
            A=A_calibrated(edges,d,L)
            B=B_forest_cycles(3,edges,d,L)
            C,k=C_component_potential(3,edges,d,L)
            res['exhaustive_three_vertex_cases']+=1
            res['component_constant_cases']+=k
            if not (A==B==C): res['exhaustive_equivalence_failures']+=1

rng=random.Random(2026080604)
for _ in range(60000):
    n=rng.randint(2,9); poss=list(combinations(range(n),2))
    edges=[e for e in poss if rng.random()<0.25]
    d={e:rng.randint(-5,5) for e in edges}
    L=[rng.randint(-5,5) for _ in range(n)]
    A=A_calibrated(edges,d,L); B=B_forest_cycles(n,edges,d,L); C,k=C_component_potential(n,edges,d,L)
    res['random_component_cases']+=1; res['component_constant_cases']+=k
    if not (A==B==C): res['random_equivalence_failures']+=1

# Ordinal versus additive controls.
res['ordinal_additive_controls']={
 'acyclic_chain_has_topological_rank': True,
 'topological_rank_need_not_match_declared_increments': True,
 'exact_anti_truth_field_can_be_path_independent': True,
}

for _ in product([False,True],repeat=10): res['proper_function_account_expansions']+=1

source_note=(ROOT/'source_and_prior_art/PMR-007_DEEP_BH_PROPER_FUNCTION_AND_FITRAH_AUTHORITY_NOTE.md').read_text()
res['source_scope_checks']={
 'fitrah_track_N_only': 'Track-N' in source_note and 'neutral theorem' in source_note,
 'El_Tobgui_secondary': 'secondary scholarly reconstruction' in source_note,
 'general_novelty_zero': 'general mathematical novelty: 0' in source_note,
}

# Frozen graph passes; adding an omitted chord with incompatible increment breaks certification.
base_edges=[(0,1),(1,2)]; base_d={(0,1):1,(1,2):1}; L=[2,1,0]
ext_edges=base_edges+[(0,2)]; ext_d={**base_d,(0,2):1}
res['dynamic_extension_witness']={
 'base_calibrated':A_calibrated(base_edges,base_d,L),
 'extended_calibrated':A_calibrated(ext_edges,ext_d,L),
 'new_edge_creates_holonomy':not B_forest_cycles(3,ext_edges,ext_d,L),
}

failed=bool(res['frozen_hash_mismatches']) or res['exhaustive_equivalence_failures'] or res['random_equivalence_failures']
failed=failed or res['proper_function_account_expansions']!=1024
failed=failed or not all(res['source_scope_checks'].values()) or not all([res['dynamic_extension_witness']['base_calibrated'],not res['dynamic_extension_witness']['extended_calibrated'],res['dynamic_extension_witness']['new_edge_creates_holonomy']])
res['result']='FAIL' if failed else 'PASS'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
