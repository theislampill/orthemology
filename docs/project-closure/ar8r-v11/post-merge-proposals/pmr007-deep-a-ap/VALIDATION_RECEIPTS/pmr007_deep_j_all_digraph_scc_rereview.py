from __future__ import annotations
from pathlib import Path
import itertools, random, json, hashlib

def reach(n,edges):
    R=[[False]*n for _ in range(n)]
    for i in range(n):R[i][i]=True
    for a,b in edges:R[a][b]=True
    for k in range(n):
        for i in range(n):
            if R[i][k]:
                for j in range(n):
                    if R[k][j]:R[i][j]=True
    return R

def acyclic(n,edges):
    out=[[] for _ in range(n)]; indeg=[0]*n
    for a,b in edges:out[a].append(b);indeg[b]+=1
    q=[i for i,d in enumerate(indeg) if d==0]; seen=0
    while q:
        v=q.pop();seen+=1
        for w in out[v]:
            indeg[w]-=1
            if indeg[w]==0:q.append(w)
    return seen==n

def roots(n,edges):
    indeg=[0]*n
    for a,b in edges:indeg[b]+=1
    return [i for i,d in enumerate(indeg) if d==0]

def upstream_directed(n,R):
    return all(any(R[u][v] and R[u][w] for u in range(n)) for v in range(n) for w in range(n))

def theorem_values(n,edges):
    R=reach(n,edges);rt=roots(n,edges);ud=upstream_directed(n,R);univ=len(rt)==1 and all(R[rt[0]][v] for v in range(n))
    return ud,univ,rt,R

fail=[]; all_graphs=0; dags=0; cyclic=0; cyclic_ud_rootless=0
for n in range(1,5):
    poss=[(i,j) for i in range(n) for j in range(n) if i!=j]
    for mask in range(1<<len(poss)):
        edges=[e for i,e in enumerate(poss) if mask>>i&1]
        all_graphs+=1; dag=acyclic(n,edges); ud,univ,rt,R=theorem_values(n,edges)
        if dag:
            dags+=1
            if ud!=univ:fail.append({'type':'dag_equivalence','n':n,'edges':edges,'ud':ud,'univ':univ,'roots':rt})
        else:
            cyclic+=1
            if ud and not rt:cyclic_ud_rootless+=1
# Random DAGs with randomized topological order.
rng=random.Random(351352); random_dags=0
for n in range(5,10):
    for _ in range(10000):
        order=list(range(n));rng.shuffle(order);edges=[]
        for i in range(n):
            for j in range(i+1,n):
                if rng.random()<0.28:edges.append((order[i],order[j]))
        random_dags+=1;ud,univ,rt,R=theorem_values(n,edges)
        if ud!=univ:fail.append({'type':'random_dag','n':n,'edges':edges,'ud':ud,'univ':univ,'roots':rt})
# Exact semantic controls.
controls={
 'cycle_is_upstream_directed_without_root': None,
 'downstream_merger_has_two_roots': None,
 'unique_root_positive': None,
}
def chk(n,edges):
    ud,univ,rt,_=theorem_values(n,edges);return {'upstream_directed':ud,'unique_universal_root':univ,'roots':rt,'acyclic':acyclic(n,edges)}
controls['cycle_is_upstream_directed_without_root']=chk(3,[(0,1),(1,2),(2,0)])
controls['downstream_merger_has_two_roots']=chk(5,[(0,2),(1,2),(2,3),(2,4)])
controls['unique_root_positive']=chk(4,[(0,1),(0,2),(1,3),(2,3)])
if not (controls['cycle_is_upstream_directed_without_root']['upstream_directed'] and not controls['cycle_is_upstream_directed_without_root']['roots']):fail.append({'type':'cycle_control'})
if controls['downstream_merger_has_two_roots']['roots']!=[0,1]:fail.append({'type':'merger_control'})
if not controls['unique_root_positive']['unique_universal_root']:fail.append({'type':'positive_control'})
# Frozen hash verification.
root=Path(__file__).parents[1]; hm=[]
for line in (root/'PMR-007_DEEP_J_V2_FROZEN_HASHES.sha256').read_text().splitlines():
    exp,path=line.split(None,1);p=Path(path.strip());got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=exp:hm.append({'path':str(p),'expected':exp,'got':got})
if hm:fail.append({'type':'hash_mismatch','data':hm})
out={'schema':'PMR007_DEEP_J_ALL_DIGRAPH_REREVIEW_RESULTS_V1','all_loopless_digraphs_n_le_4':all_graphs,'acyclic_digraphs_n_le_4':dags,'cyclic_digraphs_n_le_4':cyclic,'cyclic_upstream_directed_rootless_controls':cyclic_ud_rootless,'random_dags_n_5_to_9':random_dags,'controls':controls,'frozen_hash_mismatches':hm,'failure_count':len(fail),'failures':fail[:20],'result':'PASS' if not fail else 'FAIL'}
Path(__file__).with_name('PMR-007_DEEP_J_ALL_DIGRAPH_SCC_REREVIEW_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
