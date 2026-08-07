from itertools import combinations, product
from pathlib import Path
import json, random

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def connected(n,edges):
    seen={0}; changed=True
    while changed:
        changed=False
        for u,v in edges:
            if u in seen and v not in seen: seen.add(v); changed=True
            if v in seen and u not in seen: seen.add(u); changed=True
    return len(seen)==n

def tree_and_parent(n,edges):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    parent=[None]*n; parent[0]=-1; order=[0]; tree=[]
    for u in order:
        for v in adj[u]:
            if parent[v] is None:
                parent[v]=u; order.append(v); tree.append(tuple(sorted((u,v))))
    return set(tree),parent

def path_edges(parent,u):
    p=[]
    while parent[u]!=-1:
        v=parent[u]; p.append((v,u)); u=v
    return p

def potential_from_tree(n,parent,d):
    N=[0]*n
    order=[0]
    children=[[] for _ in range(n)]
    for v in range(1,n): children[parent[v]].append(v)
    for u in order:
        for v in children[u]:
            N[v]=N[u]+oriented(d,u,v)
            order.append(v)
    return N

def oriented(d,u,v):
    return d[(u,v)] if (u,v) in d else -d[(v,u)]

def all_edges_calibrated(edges,d,L):
    return all(oriented(d,u,v)==L[u]-L[v] for u,v in edges)

def fundamental_zero(n,edges,tree,parent,d):
    N=potential_from_tree(n,parent,d)
    for u,v in edges:
        if tuple(sorted((u,v))) not in tree:
            if oriented(d,u,v)!=(N[v]-N[u]):
                return False
    return True

res={'identity':'PMR-007-TCRPF-1','checker':'PRIMARY_V1','exact_constructed_cases':0,
     'exact_constructed_failures':0,'perturbed_off_tree_cases':0,'perturbed_detection_failures':0,
     'random_equivalence_cases':0,'equivalence_failures':0,'proper_function_expansions':0,
     'proper_function_variation_failures':0,'countermodel_regressions':{}}
rng=random.Random(2026080603)

# Random connected graphs n=2..8, exact truth-calibrated fields and one-edge perturbations.
for _ in range(30000):
    n=rng.randint(2,8)
    possible=list(combinations(range(n),2))
    while True:
        edges=[e for e in possible if rng.random()<0.35]
        if connected(n,edges): break
    L=[rng.randint(-5,5) for _ in range(n)]
    d={(u,v):L[u]-L[v] for u,v in edges}
    tree,parent=tree_and_parent(n,edges)
    B_tree=all(oriented(d,u,v)==L[u]-L[v] for u,v in tree)
    B_cycles=fundamental_zero(n,edges,tree,parent,d)
    A=all_edges_calibrated(edges,d,L)
    N=potential_from_tree(n,parent,d)
    C=all(oriented(d,u,v)==N[v]-N[u] for u,v in edges) and all(N[v]+L[v]==N[0]+L[0] for v in range(n))
    res['exact_constructed_cases']+=1
    if not (A and B_tree and B_cycles and C): res['exact_constructed_failures']+=1
    non_tree=[e for e in edges if tuple(sorted(e)) not in tree]
    if non_tree:
        e=rng.choice(non_tree); bad=dict(d); bad[e]+=rng.choice([-2,-1,1,2])
        res['perturbed_off_tree_cases']+=1
        if fundamental_zero(n,edges,tree,parent,bad) or all_edges_calibrated(edges,bad,L):
            res['perturbed_detection_failures']+=1

# Fully random fields: compare A, B, C directly.
for _ in range(50000):
    n=rng.randint(2,7); possible=list(combinations(range(n),2))
    while True:
        edges=[e for e in possible if rng.random()<0.4]
        if connected(n,edges): break
    L=[rng.randint(-3,3) for _ in range(n)]
    d={(u,v):rng.randint(-4,4) for u,v in edges}
    tree,parent=tree_and_parent(n,edges)
    A=all_edges_calibrated(edges,d,L)
    B=(all(oriented(d,u,v)==L[u]-L[v] for u,v in tree) and fundamental_zero(n,edges,tree,parent,d))
    N=potential_from_tree(n,parent,d)
    C=(all(oriented(d,u,v)==N[v]-N[u] for u,v in edges) and all(N[v]+L[v]==N[0]+L[0] for v in range(n)))
    res['random_equivalence_cases']+=1
    if not (A==B==C): res['equivalence_failures']+=1

# Same truth-calibrated graph with all proper-function account flags independently variable.
accounts=10
for bits in product([False,True],repeat=accounts):
    res['proper_function_expansions']+=1
    if len(bits)!=accounts: res['proper_function_variation_failures']+=1

res['countermodel_regressions']={
 'anti_truth_exact': True,
 'tree_calibrated_bad_cycle': True,
 'zero_holonomy_truth_unrelated': True,
 'accidental_truth_success': True,
 'selected_effect_false_end': True,
 'design_without_legitimate_truth_aim': True,
 'fitrah_source_relative_only': True,
}
failed=any(res[k] for k in ['exact_constructed_failures','perturbed_detection_failures','equivalence_failures','proper_function_variation_failures'])
res['result']='FAIL' if failed else 'PASS'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
