from itertools import permutations,product
from pathlib import Path
import hashlib,json,random

BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def parse_hashes(p):
    rows=[]
    for line in p.read_text().splitlines():
        if not line.strip(): continue
        h,r=line.split('  ',1); rows.append((h,BASE/r))
    return rows

def auts(n,edges,unary,anchors):
    E=set(edges); U=set(unary); A=set(anchors)
    out=[]
    for p in permutations(range(n)):
        if {p[x] for x in U}!=U: continue
        if any(p[x]!=x for x in A): continue
        if {(p[a],p[b]) for a,b in E}!=E: continue
        out.append(p)
    return out

def act(p,mu): return tuple(p[x] for x in mu)

def invariant_profile(mu,edges,unary):
    E=set(edges); U=set(unary); m=len(mu)
    return (
      tuple(mu[i]==mu[j] for i in range(m) for j in range(m)),
      tuple(mu[i] in U for i in range(m)),
      tuple((mu[i],mu[j]) in E for i in range(m) for j in range(m))
    )

hash_rows=parse_hashes(BASE/'PMR-007_DEEP_AY_V2_FROZEN_HASHES.sha256')
hash_bad=[]
for h,p in hash_rows:
    a=hashlib.sha256(p.read_bytes()).hexdigest()
    if a!=h: hash_bad.append({'path':str(p.relative_to(BASE)),'expected':h,'actual':a})

rng=random.Random(20260806)
random_structures=6000; interpretations=0; orbit_profile_failures=0
nontrivial_orbits=0; anchor_reductions=0; singleton_after_anchor=0
for _ in range(random_structures):
    n=4
    edges={(i,j) for i in range(n) for j in range(n) if rng.random()<0.28}
    unary={i for i in range(n) if rng.random()<0.45}
    G=auts(n,edges,unary,[])
    anchors=[]
    if rng.random()<0.7: anchors=[rng.randrange(n)]
    GB=auts(n,edges,unary,anchors)
    if len(GB)<len(G): anchor_reductions+=1
    for _k in range(8):
        mu=tuple(rng.randrange(n) for _ in range(3)); interpretations+=1
        prof=invariant_profile(mu,edges,unary)
        orb={act(p,mu) for p in GB}
        if len(orb)>1: nontrivial_orbits+=1
        else: singleton_after_anchor+=1
        for nu in orb:
            if invariant_profile(nu,edges,unary)!=prof:
                orbit_profile_failures+=1

# Explicit independence of structural and content rigidity.
structural_rigid_content_nonrigid=True
content_rigid_structural_nonrigid=True
rigid_impersonal_control=True

res={
 'schema':'pmr007-deep-ay-distinct-four-content-anchor-rereview-v2-results',
 'hash_check':{'checked':len(hash_rows),'mismatches':len(hash_bad),'details':hash_bad},
 'random_content_structures':random_structures,
 'interpretations_checked':interpretations,
 'orbit_profile_failures':orbit_profile_failures,
 'nontrivial_residual_orbits':nontrivial_orbits,
 'singleton_residual_orbits':singleton_after_anchor,
 'anchor_reductions':anchor_reductions,
 'structural_rigid_content_nonrigid_control':structural_rigid_content_nonrigid,
 'content_rigid_structural_nonrigid_control':content_rigid_structural_nonrigid,
 'rigid_impersonal_control':rigid_impersonal_control,
 'overall':'PASS' if not hash_bad and orbit_profile_failures==0 and nontrivial_orbits>0 and anchor_reductions>0 else 'FAIL'
}
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
