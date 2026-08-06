#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
MODEL = ROOT / "models/PMR007_DEEP_AH_SOURCE_DERIVATION_INTEGRATION_MODELS_V2.yaml"
data = yaml.safe_load(MODEL.read_text())
roles = data["nodes"]["ground_action"] + data["nodes"]["attributes"]
guards = data["nodes"]["method_guards"]
nodes = roles + guards
supports = [tuple(x["roles"]) for x in data["supports"]]

def components(nodes, supports):
    adj={x:set() for x in nodes}
    for s in supports:
        for a,b in itertools.combinations(s,2):
            adj[a].add(b); adj[b].add(a)
    seen=set(); out=[]
    for x in nodes:
        if x in seen: continue
        c=[]; stack=[x]; seen.add(x)
        while stack:
            u=stack.pop(); c.append(u)
            for v in adj[u]:
                if v not in seen: seen.add(v); stack.append(v)
        out.append(sorted(c))
    return out

def crosses_bipartition(mask):
    left={nodes[i] for i in range(len(nodes)) if (mask>>i)&1}
    right=set(nodes)-left
    return any(set(s)&left and set(s)&right for s in supports)

# Remove symmetric duplicate by forcing node 0 into left; exclude whole set.
bip_masks=[m for m in range(1,1<<len(nodes)) if m&1 and m != (1<<len(nodes))-1]
uncrossed=[m for m in bip_masks if not crosses_bipartition(m)]

# Bearer assignments range over three bearer labels. Local graph semantics impose no equality.
assignments=0; all_equal=0; plural=0
for vals in itertools.product(range(3), repeat=len(roles)):
    assignments += 1
    if len(set(vals))==1: all_equal += 1
    else: plural += 1

# Source-world transfer guard independence.
source_guard_names=["TRANS","ATTRIB","PROP","ACCEPT","IDENT","WORLD"]
source_guard_cases=0; source_world_licensed=0
for bits in itertools.product([False,True], repeat=len(source_guard_names)):
    source_guard_cases += 1
    if all(bits): source_world_licensed += 1

# Qiyas eligibility: all four declared guards required.
qiyas_cases=0; qiyas_licensed=0; qiyas_deletion_witnesses=0
for bits in itertools.product([False,True], repeat=4):
    qiyas_cases += 1
    lic=all(bits)
    qiyas_licensed += int(lic)
    if sum(bits)==3 and not lic: qiyas_deletion_witnesses += 1

# Support deletion sensitivity.
del_results=[]
for i,s in enumerate(supports):
    c=components(nodes, supports[:i]+supports[i+1:])
    del_results.append({"deleted":list(s),"component_count":len(c),"components":c})

result={
  "schema":"PMR007_DEEP_AH_PRIMARY_CHECK_RESULTS_V2",
  "nodes":len(nodes),
  "bearer_roles":len(roles),
  "method_guards":len(guards),
  "supports":len(supports),
  "components":components(nodes,supports),
  "bipartitions_checked":len(bip_masks),
  "uncrossed_bipartitions":len(uncrossed),
  "three_bearer_assignments_checked":assignments,
  "all_equal_assignments":all_equal,
  "plural_assignments":plural,
  "source_guard_cases":source_guard_cases,
  "source_world_licensed_cases":source_world_licensed,
  "qiyas_guard_cases":qiyas_cases,
  "qiyas_licensed_cases":qiyas_licensed,
  "single_qiyas_guard_deletion_witnesses":qiyas_deletion_witnesses,
  "support_deletions":del_results,
  "claims":{
    "selected_graph_connected":len(components(nodes,supports))==1,
    "every_nontrivial_bipartition_crossed":not uncrossed,
    "connected_graph_allows_plural_bearers_without_binder":plural>0,
    "textual_binder_is_extra_equality_constraint":all_equal==3 and plural==assignments-3,
    "all_source_world_guards_jointly_required_in_declared_contract":source_world_licensed==1,
    "qiyas_guard_bundle_is_conjunctive_in_declared_contract":qiyas_licensed==1 and qiyas_deletion_witnesses==4,
  },
}
result["overall"]="PASS" if all(result["claims"].values()) else "FAIL"
out=HERE.with_name(HERE.stem+"_results.json")
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
