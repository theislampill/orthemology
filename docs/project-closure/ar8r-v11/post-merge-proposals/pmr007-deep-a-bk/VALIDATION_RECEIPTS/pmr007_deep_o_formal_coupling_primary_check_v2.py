#!/usr/bin/env python3
"""V2 primary check with repaired vocabulary for PMR-007-GUPP-1."""
from __future__ import annotations
import itertools, json
from pathlib import Path

OUT = Path(__file__).with_name("pmr007_deep_o_formal_coupling_primary_check_v2_results.json")
DOMAIN = ((0,0),(0,1),(1,0),(1,1))
INDEX = {q:i for i,q in enumerate(DOMAIN)}

def value(fn: int, q: tuple[int,int]) -> int:
    return (fn >> INDEX[q]) & 1

def changes(fn: int, bit: int) -> bool:
    for q in DOMAIN:
        r = (1-q[0],q[1]) if bit == 0 else (q[0],1-q[1])
        if value(fn,q) != value(fn,r):
            return True
    return False

structurally_coupled = 0
all_nonconstant = 0
injective_maps = 0
for funcs in itertools.product(range(16), repeat=5):
    if any(f in (0,15) for f in funcs):
        continue
    all_nonconstant += 1
    image = {tuple(value(f,q) for f in funcs) for q in DOMAIN}
    if len(image) != 4:
        continue
    injective_maps += 1
    influence = [[changes(f,b) for b in (0,1)] for f in funcs]
    if any(sum(influence[i][b] for i in range(5)) < 2 for b in (0,1)):
        continue
    # connected output coupling graph through shared primitive influence
    adj=[set() for _ in range(5)]
    for i in range(5):
        for j in range(i+1,5):
            if any(influence[i][b] and influence[j][b] for b in (0,1)):
                adj[i].add(j); adj[j].add(i)
    seen={0}; todo=[0]
    while todo:
        u=todo.pop()
        for v in adj[u]-seen:
            seen.add(v); todo.append(v)
    if len(seen)==5:
        structurally_coupled += 1

profiles=[]
for x,y in DOMAIN:
    n=x+y
    profiles.append({"q":f"{x}{y}","M":x,"A":y,"S":x^y,"N":n,"R":int(n>0)})
assert len({tuple(p[k] for k in ("M","A","S","N","R")) for p in profiles})==4
marginal_sizes={k:len({p[k] for p in profiles}) for k in ("M","A","S","N","R")}
product=1
for n in marginal_sizes.values(): product*=n
assert product==48

# equations and intervention effects
for p in profiles:
    assert p["S"]==(p["M"]^p["A"])
    assert p["N"]==p["M"]+p["A"]
    assert p["R"]==int(p["N"]>0)

def profile(q):
    x,y=q; n=x+y
    return (x,y,x^y,n,int(n>0))
intervention_effects=[]
for q in DOMAIN:
    for bit in (0,1):
        r=(1-q[0],q[1]) if bit==0 else (q[0],1-q[1])
        diffs=[i for i,(a,b) in enumerate(zip(profile(q),profile(r))) if a!=b]
        assert len(diffs)>=3
        intervention_effects.append({"from":q,"to":r,"changed_coordinates":diffs})

# exact potential on square, including zero closed-walk holonomy
V={q:q[0]+q[1] for q in DOMAIN}
edges=[((0,0),(0,1)),((0,0),(1,0)),((0,1),(1,1)),((1,0),(1,1))]
for u,v in edges:
    assert V[v]-V[u]==1
cycle=[(0,0),(0,1),(1,1),(1,0),(0,0)]
cycle_sum=sum(V[cycle[i+1]]-V[cycle[i]] for i in range(len(cycle)-1))
assert cycle_sum==0

neutral={"profiles":profiles,"potential":V,"edges":edges,"interventions":intervention_effects}
HI={**neutral,"PERS":False,"MENT":False,"IOWN":False,"BECAUSE_F":False}
HP={**neutral,"PERS":True,"MENT":True,"IOWN":True,"BECAUSE_F":True}
assert all(HI[k]==HP[k] for k in neutral)
assert HI["PERS"]!=HP["PERS"]

result={
  "boolean_coordinate_function_tuples_enumerated":16**5,
  "all_five_nonconstant":all_nonconstant,
  "injective_joint_maps":injective_maps,
  "structurally_coupled_maps_under_frozen_filter":structurally_coupled,
  "semantic_or_explanatory_unification_certified_by_count":False,
  "explicit_profiles":profiles,
  "marginal_sizes":marginal_sizes,
  "product_marginal_profile_count":product,
  "joint_image_count":4,
  "excluded_marginal_combinations":product-4,
  "intervention_cases":len(intervention_effects),
  "minimum_coordinates_changed_by_one_bit_flip":min(len(x["changed_coordinates"]) for x in intervention_effects),
  "closed_walk_potential_sum":cycle_sum,
  "neutral_reduct_equal":True,
  "personality_varies_over_neutral_reduct":True,
  "status":"PASS"
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
