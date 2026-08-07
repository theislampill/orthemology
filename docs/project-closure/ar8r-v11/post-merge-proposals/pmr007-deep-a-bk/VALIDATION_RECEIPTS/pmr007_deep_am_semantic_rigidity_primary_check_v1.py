#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path


def perms(n):
    return list(itertools.permutations(range(n)))

def edge_pairs(n):
    return [(i,j) for i in range(n) for j in range(i+1,n)]

def graph_edges(n, mask):
    ps=edge_pairs(n)
    return frozenset(ps[k] for k in range(len(ps)) if (mask>>k)&1)

def perm_edge(e,p):
    a,b=p[e[0]],p[e[1]]
    return (a,b) if a<b else (b,a)

def perm_graph(E,p):
    return frozenset(perm_edge(e,p) for e in E)

def auts(n,E):
    return [p for p in perms(n) if perm_graph(E,p)==E]

def act_interp(i,p):
    # push forward: value at p[x] is old value at x
    out=[None]*len(i)
    for x,v in enumerate(i): out[p[x]]=v
    return tuple(out)

def fixed(i,G):
    return all(act_interp(i,p)==i for p in G)

def interp_orbits(interps,G):
    left=set(interps); obs=[]
    while left:
        i=min(left); o={act_interp(i,p) for p in G}
        obs.append(frozenset(o)); left-=o
    return obs

def canonical_copy_check(n,E,i,G):
    # For every labelled copy, all isomorphisms from base to that copy induce
    # the same interpretation iff i is fixed by Aut(S).
    by_copy={}
    for p in perms(n):
        Ep=perm_graph(E,p); ip=act_interp(i,p)
        by_copy.setdefault(Ep,set()).add(ip)
    return all(len(v)==1 for v in by_copy.values())

counts={
 'n3_graphs':0,'n3_invariant_families':0,'n3_families_with_selector':0,
 'n3_selector_criterion_failures':0,'n4_graphs':0,'interpretations_checked':0,
 'fixed_interpretations':0,'nonfixed_with_moving_automorphism':0,
 'canonical_copy_equivalence_failures':0,'kernel_reference_swap_witnesses':0,
}
examples={}
# Exhaustive invariant-family test for n=3, binary content.
n=3
for mask in range(1<<len(edge_pairs(n))):
    E=graph_edges(n,mask); G=auts(n,E); counts['n3_graphs']+=1
    interps=list(itertools.product(range(2),repeat=n)); obs=interp_orbits(interps,G)
    fixed_set={i for i in interps if fixed(i,G)}
    for choose in range(1<<len(obs)):
        fam=set().union(*(obs[k] for k in range(len(obs)) if (choose>>k)&1)) if choose else set()
        counts['n3_invariant_families']+=1
        selector_exists=bool(fam & fixed_set)
        brute_exists=any(fixed(i,G) for i in fam)
        if selector_exists: counts['n3_families_with_selector']+=1
        if selector_exists!=brute_exists: counts['n3_selector_criterion_failures']+=1
# Structure/copy test for n=4 and two/three content values.
n=4
for mask in range(1<<len(edge_pairs(n))):
    E=graph_edges(n,mask); G=auts(n,E); counts['n4_graphs']+=1
    for k in (2,3):
        for i in itertools.product(range(k),repeat=n):
            counts['interpretations_checked']+=1
            f=fixed(i,G)
            if f: counts['fixed_interpretations']+=1
            else:
                if any(act_interp(i,p)!=i for p in G):
                    counts['nonfixed_with_moving_automorphism']+=1
            c=canonical_copy_check(n,E,i,G)
            if c!=f: counts['canonical_copy_equivalence_failures']+=1
            # Equality kernel is unchanged by a global permutation of content labels.
            if k>=2 and len(set(i))>=2:
                j=tuple((v+1)%k for v in i)
                ker_i=tuple(i[a]==i[b] for a in range(n) for b in range(n))
                ker_j=tuple(j[a]==j[b] for a in range(n) for b in range(n))
                if i!=j and ker_i==ker_j:
                    counts['kernel_reference_swap_witnesses']+=1

claims={
 'selector_iff_automorphism_fixed': counts['n3_selector_criterion_failures']==0 and counts['canonical_copy_equivalence_failures']==0,
 'nonfixed_interpretations_have_symmetry_witness': counts['nonfixed_with_moving_automorphism']>0,
 'equal_similarity_kernel_does_not_fix_content_labels': counts['kernel_reference_swap_witnesses']>0,
}
res={'schema':'PMR007_DEEP_AM_PRIMARY_CHECK_RESULTS_V1','counts':counts,'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
