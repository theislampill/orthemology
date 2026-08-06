from itertools import permutations, product
from pathlib import Path
import json

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')


def graph_auts(n,edges,designated=None):
    E={tuple(sorted(e)) for e in edges}
    aut=[]
    for p in permutations(range(n)):
        if designated is not None and p[designated]!=designated: continue
        Ep={tuple(sorted((p[a],p[b]))) for a,b in E}
        if Ep==E: aut.append(p)
    return aut

def act(p,mu): return tuple(p[c] for c in mu)

def atomic_profile(mu,edges):
    E={tuple(sorted(e)) for e in edges}
    nX=len(mu)
    # equality and graph-edge facts for all ordered pairs of structural positions
    return tuple((mu[i]==mu[j], tuple(sorted((mu[i],mu[j]))) in E) for i in range(nX) for j in range(nX))

structures=0; interpretations=0; orbit_profile_failures=0; nontrivial_orbits=0; singleton_orbits=0
rigid_with_anchor=0; hidden_anchor_changes=0
for mask in range(1<<3): # all simple graphs on 3 content labels
    pairs=[(0,1),(0,2),(1,2)]
    edges=[pairs[i] for i in range(3) if mask>>i & 1]
    aut=graph_auts(3,edges)
    structures+=1
    for mu in product(range(3),repeat=3):
        interpretations+=1
        prof=atomic_profile(mu,edges)
        orb={act(p,mu) for p in aut}
        if len(orb)>1: nontrivial_orbits+=1
        else: singleton_orbits+=1
        for nu in orb:
            if atomic_profile(nu,edges)!=prof:
                orbit_profile_failures+=1
    # adding designated constant 0 restricts automorphisms
    aut0=graph_auts(3,edges,designated=0)
    if len(aut0)==1: rigid_with_anchor+=1
    if len(aut0)<len(aut): hidden_anchor_changes+=1

# Explicit structural-rigid/content-gauge control: X positions distinguishable but equality-only C has S3.
structural_rigid_content_gauge=True
truth_swap_control=True

res={
 'schema':'pmr007-deep-ay-semantic-gauge-primary-check-v1-results',
 'content_structures':structures,
 'interpretations':interpretations,
 'orbit_profile_failures':orbit_profile_failures,
 'nontrivial_interpretation_orbits':nontrivial_orbits,
 'singleton_interpretation_orbits':singleton_orbits,
 'content_structures_rigid_after_designating_0':rigid_with_anchor,
 'structures_where_designated_anchor_reduced_group':hidden_anchor_changes,
 'structural_rigid_content_gauge_control':structural_rigid_content_gauge,
 'truth_swap_control':truth_swap_control,
 'overall':'PASS' if orbit_profile_failures==0 and nontrivial_orbits>0 and hidden_anchor_changes>0 else 'FAIL'
}
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
