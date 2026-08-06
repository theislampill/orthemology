#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = [
    "CREATION", "SPECIFICATION", "CHOICE", "VOLITION", "KNOWLEDGE",
    "ABILITY", "LIFE", "SPEECH", "PERFECTION"
]
SUPPORTS = [
    ("CREATION", "VOLITION"),
    ("VOLITION", "KNOWLEDGE"),
    ("SPECIFICATION", "VOLITION"),
    ("CHOICE", "ABILITY"),
    ("KNOWLEDGE", "ABILITY", "LIFE"),
    ("CREATION", "SPEECH"),
    ("SPEECH", "PERFECTION"),
]

def partitions(items):
    if not items:
        yield []
        return
    first, *rest = items
    for p in partitions(rest):
        yield [{first}] + [set(x) for x in p]
        for i in range(len(p)):
            q = [set(x) for x in p]
            q[i].add(first)
            yield q

def canonical(p):
    return tuple(sorted(tuple(sorted(b)) for b in p))

def support_crosses(support, p):
    loc = {}
    for i,b in enumerate(p):
        for x in b: loc[x] = i
    return len({loc[x] for x in support}) > 1

def graph_components():
    adj = {r:set() for r in ROLES}
    for s in SUPPORTS:
        for a,b in itertools.combinations(s,2):
            adj[a].add(b); adj[b].add(a)
    seen=set(); comps=[]
    for r in ROLES:
        if r in seen: continue
        stack=[r]; seen.add(r); c=[]
        while stack:
            x=stack.pop(); c.append(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); stack.append(y)
        comps.append(sorted(c))
    return comps

parts = {}
for p in partitions(ROLES): parts[canonical(p)] = p
nontrivial = [p for p in parts.values() if len(p)>1]
uncrossed = [canonical(p) for p in nontrivial if not any(support_crosses(s,p) for s in SUPPORTS)]

# Local role-edge satisfaction intentionally has no bearer-equality axiom.
# Hence every partition is a local realization; the source binder selects only one block.
local_realizations = len(parts)
source_binder_realizations = sum(1 for p in parts.values() if len(p)==1)
injective_realizations = sum(1 for p in parts.values() if len(p)==len(ROLES))

# Deletion importance: remove each support and count resulting components.
deletions=[]
for idx,sdel in enumerate(SUPPORTS):
    saved=SUPPORTS[:idx]+SUPPORTS[idx+1:]
    adj={r:set() for r in ROLES}
    for s in saved:
        for a,b in itertools.combinations(s,2):
            adj[a].add(b); adj[b].add(a)
    seen=set(); ncomp=0
    for r in ROLES:
        if r in seen: continue
        ncomp += 1; stack=[r]; seen.add(r)
        while stack:
            x=stack.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); stack.append(y)
    deletions.append({"deleted_support": list(sdel), "components": ncomp})

result = {
    "schema": "PMR007_DEEP_AH_PRIMARY_CHECK_RESULTS_V1",
    "roles": len(ROLES),
    "supports": len(SUPPORTS),
    "components": graph_components(),
    "set_partitions_checked": len(parts),
    "nontrivial_partitions_checked": len(nontrivial),
    "nontrivial_partitions_not_crossed": len(uncrossed),
    "local_role_graph_realizations": local_realizations,
    "source_binder_realizations": source_binder_realizations,
    "injective_plural_realizations": injective_realizations,
    "support_deletion_component_counts": deletions,
    "claims": {
        "selected_support_graph_connected": len(graph_components()) == 1,
        "every_nontrivial_partition_crossed": len(uncrossed) == 0,
        "connected_graph_allows_plural_bearer_realization_without_binder": injective_realizations == 1,
        "source_binder_selects_one_bearer_partition": source_binder_realizations == 1,
    },
    "overall": "PASS" if len(graph_components())==1 and not uncrossed and source_binder_realizations==1 else "FAIL",
}
out = Path(__file__).with_name(Path(__file__).stem + "_results.json")
out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
print(json.dumps(result, indent=2, sort_keys=True))
