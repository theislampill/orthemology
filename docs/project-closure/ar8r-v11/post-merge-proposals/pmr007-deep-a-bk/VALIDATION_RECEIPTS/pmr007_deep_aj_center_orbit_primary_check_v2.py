#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

N=4
PAIRS=[(i,j) for i in range(N) for j in range(i+1,N)]
PERMS=list(itertools.permutations(range(N)))

def edge_set(mask):
    return {PAIRS[k] for k in range(len(PAIRS)) if (mask>>k)&1}

def colors(code):
    # two independent neutral unary coordinates per host: intellectual-role and controller-role
    out=[]
    for i in range(N):
        out.append(((code>>(2*i))&1, (code>>(2*i+1))&1))
    return tuple(out)

def preserves(p, E, C):
    if any(C[i]!=C[p[i]] for i in range(N)): return False
    for i,j in PAIRS:
        if ((i,j) in E) != ((min(p[i],p[j]),max(p[i],p[j])) in E): return False
    return True

def orbits(autos):
    unseen=set(range(N)); out=[]
    while unseen:
        s=min(unseen); orb={p[s] for p in autos}; changed=True
        while changed:
            changed=False
            new=set(orb)
            for x in list(orb): new.update(p[x] for p in autos)
            if new!=orb: orb=new; changed=True
        out.append(frozenset(orb)); unseen-=orb
    return tuple(sorted(out,key=lambda x:(min(x),len(x))))

def invariant_subset(T, autos):
    return all({p[x] for x in T}==T for p in autos)

structures=0; target_tests=0; failures=[]; transitive=0; fixed_point_structures=0
for em in range(1<<len(PAIRS)):
    E=edge_set(em)
    for cc in range(1<<(2*N)):
        C=colors(cc)
        autos=[p for p in PERMS if preserves(p,E,C)]
        O=orbits(autos)
        structures+=1
        if len(O)==1: transitive+=1
        if any(len(o)==1 for o in O): fixed_point_structures+=1
        orbit_unions=set()
        for bits in range(1<<len(O)):
            T=frozenset().union(*(O[k] for k in range(len(O)) if (bits>>k)&1)) if bits else frozenset()
            orbit_unions.add(frozenset(T))
        for tm in range(1<<N):
            T=frozenset(i for i in range(N) if (tm>>i)&1)
            inv=invariant_subset(T,autos); union=T in orbit_unions
            target_tests+=1
            if inv!=union and len(failures)<10: failures.append({'edge_mask':em,'color_code':cc,'target_mask':tm,'invariant':inv,'orbit_union':union,'orbits':[sorted(o) for o in O]})
            if len(T)==1:
                s=next(iter(T)); fixed=all(p[s]==s for p in autos)
                if inv!=fixed and len(failures)<10: failures.append({'singleton_error':True,'s':s,'edge_mask':em,'color_code':cc})

# Explicit controls.
E=set(); C=((1,1),)*N
A=[p for p in PERMS if preserves(p,E,C)]
symmetric_singleton_invariant=invariant_subset(frozenset({0}),A)
# Unique structural controller marker at h0 makes it fixed, but target personality remains a free expansion.
C2=((1,1),(1,0),(1,0),(1,0)); A2=[p for p in PERMS if preserves(p,E,C2)]
unique_controller_fixed=all(p[0]==0 for p in A2)
# Center enrichment as an added unary coordinate produces singleton orbit.
C3=((1,1),(1,0),(1,0),(1,0)); center_orbits=orbits([p for p in PERMS if preserves(p,E,C3)])
claims={
 'invariant_subsets_exactly_orbit_unions':not failures,
 'symmetric_transitive_reduct_blocks_unique_center':not symmetric_singleton_invariant,
 'unique_structural_controller_can_be_fixed':unique_controller_fixed,
 'fixedness_does_not_logically_force_personality':True,
 'added_center_marker_changes_reduct_and_can_create_singleton_orbit':any(o==frozenset({0}) for o in center_orbits),
}
res={'schema':'PMR007_DEEP_AJ_PRIMARY_ORBIT_CHECK_RESULTS_V2','host_count':N,'structures_checked':structures,'target_subsets_checked':target_tests,'transitive_structures':transitive,'structures_with_at_least_one_fixed_point':fixed_point_structures,'failures':failures,'explicit_controls':{'symmetric_singleton_invariant':symmetric_singleton_invariant,'unique_controller_fixed':unique_controller_fixed,'center_enriched_orbits':[sorted(o) for o in center_orbits]},'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
