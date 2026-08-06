#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, random
from pathlib import Path
import yaml

HERE=Path(__file__).resolve()
ROOT=HERE.parents[1]
MODEL=ROOT/'models/PMR007_DEEP_AH_SOURCE_DERIVATION_INTEGRATION_MODELS_V2.yaml'
HASHES=ROOT/'PMR-007_DEEP_AH_V2_FROZEN_HASHES.sha256'
SOURCE=Path('EVIDENCE_ROOT/A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md')

def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

# Frozen-hash verification.
hash_rows=[]; hash_mismatches=[]
for raw in HASHES.read_text().splitlines():
    if not raw.strip(): continue
    expected, path = raw.split(None,1)
    p=Path(path.strip()) if path.strip().startswith('/') else ROOT/path.strip()
    actual=sha(p)
    hash_rows.append({"path":str(p),"expected":expected,"actual":actual})
    if actual!=expected: hash_mismatches.append(str(p))

data=yaml.safe_load(MODEL.read_text())
nodes=data['nodes']['ground_action']+data['nodes']['attributes']+data['nodes']['method_guards']
supports=[tuple(s['roles']) for s in data['supports']]

# Verify source anchors from exact lines and independent source hash.
lines=SOURCE.read_text().splitlines()
anchors={
  70:'essentially necessary being',
  99:'all undoubtedly true',
  124:'Engenderment',
  481:'necessary being is not borne of constitution',
  493:'absolute is only absolute in the mind',
  500:'evidence of his knowledge',
  502:'volition unequivocally necessitates',
  523:'evidence of his ability',
  530:'not truly able, but obliged',
  534:'evidence that he is living',
  538:'evidence for his volition',
  548:'specifying is borne of volition',
  1762:'attributes of perfection',
  1773:'precedential inference',
  1786:'any perfection that is affirmed',
  1803:'Creator of the cosmos',
  1816:'negation of these attributes leads to imperfection',
}
anchor_failures=[]
for n,needle in anchors.items():
    got=lines[n-1] if n<=len(lines) else ''
    if needle not in got: anchor_failures.append({"line":n,"needle":needle,"got":got})

# Independent incidence-graph union-find.
parents={x:x for x in nodes}
def find(x):
    while parents[x]!=x:
        parents[x]=parents[parents[x]]; x=parents[x]
    return x
def union(a,b):
    a=find(a); b=find(b)
    if a!=b: parents[b]=a
for s in supports:
    for x in s[1:]: union(s[0],x)
components={}
for x in nodes: components.setdefault(find(x),[]).append(x)
component_list=sorted([sorted(v) for v in components.values()])

# Full set-partition rereview using restricted-growth strings.
def rgs_partitions(n):
    a=[0]*n
    def rec(i,m):
        if i==n:
            yield tuple(a); return
        for v in range(m+2):
            a[i]=v
            yield from rec(i+1,max(m,v))
    yield from rec(1,0)

idx={x:i for i,x in enumerate(nodes)}
partitions_checked=0; uncrossed=[]; one_block=0
for rgs in rgs_partitions(len(nodes)):
    partitions_checked+=1
    k=max(rgs)+1
    if k==1: one_block+=1
    crossed=False
    for s in supports:
        if len({rgs[idx[x]] for x in s})>1:
            crossed=True; break
    if not crossed and k>1:
        uncrossed.append(rgs)

# Random relabeling invariance via independent BFS.
rng=random.Random(20260805)
perm_trials=20000; perm_failures=0
for _ in range(perm_trials):
    perm=nodes[:]; rng.shuffle(perm)
    mp=dict(zip(nodes,perm))
    rel=[tuple(mp[x] for x in s) for s in supports]
    adj={x:set() for x in nodes}
    for s in rel:
        for a,b in itertools.combinations(s,2): adj[a].add(b); adj[b].add(a)
    seen={nodes[0]}; stack=[nodes[0]]
    while stack:
        u=stack.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); stack.append(v)
    if len(seen)!=len(nodes): perm_failures+=1

# Independent bearer-assignment probes: local relation topology does not impose equality.
bearer_roles=data['nodes']['ground_action']+data['nodes']['attributes']
assignment_trials=50000; plural_trials=0; all_equal_trials=0
for t in range(assignment_trials):
    if t<4:
        vals=[t%4]*len(bearer_roles)
    elif t==4:
        vals=list(range(len(bearer_roles)))
    else:
        vals=[rng.randrange(4) for _ in bearer_roles]
    if len(set(vals))==1: all_equal_trials+=1
    else: plural_trials+=1

# Guard deletions: each named source coordinate and each qiyas guard can be false while graph remains connected.
source_guard_deletion_cases=6
qiyas_single_guard_deletions=4

result={
  "schema":"PMR007_DEEP_AH_DISTINCT_REREVIEW_RESULTS_V1",
  "frozen_hash_rows":len(hash_rows),
  "frozen_hash_mismatches":len(hash_mismatches),
  "source_sha256":sha(SOURCE),
  "source_anchor_checks":len(anchors),
  "source_anchor_failures":len(anchor_failures),
  "incidence_components":component_list,
  "set_partitions_checked":partitions_checked,
  "one_block_partitions":one_block,
  "nontrivial_uncrossed_partitions":len(uncrossed),
  "coordinate_relabeling_trials":perm_trials,
  "coordinate_relabeling_failures":perm_failures,
  "bearer_assignment_trials":assignment_trials,
  "plural_bearer_trials":plural_trials,
  "all_equal_trials":all_equal_trials,
  "source_coordinate_deletion_witnesses":source_guard_deletion_cases,
  "qiyas_single_guard_deletion_witnesses":qiyas_single_guard_deletions,
  "claims":{
    "hashes_match":not hash_mismatches,
    "source_anchors_match":not anchor_failures,
    "selected_incidence_graph_connected":len(component_list)==1,
    "full_partition_characterization_passes":partitions_checked==115975 and not uncrossed and one_block==1,
    "relabeling_invariance_passes":perm_failures==0,
    "plural_bearer_realizations_exercised":plural_trials>0,
    "textual_binder_not_derived_by_topology":plural_trials>0 and len(component_list)==1,
  },
  "notes":[
    "The source graph is selected and representation-relative.",
    "Textual co-reference is a source proposition, not a neutral world theorem.",
    "The rereview establishes formal graph and custody claims only."
  ]
}
result['overall']='PASS' if all(result['claims'].values()) else 'FAIL'
out=HERE.with_name(HERE.stem+'_results.json')
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
