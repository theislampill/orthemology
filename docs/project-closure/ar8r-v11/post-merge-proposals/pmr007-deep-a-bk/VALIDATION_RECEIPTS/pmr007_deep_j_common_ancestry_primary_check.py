from itertools import combinations
from pathlib import Path
import json

def reach(n,edges):
    R=[[False]*n for _ in range(n)]
    for i in range(n):R[i][i]=True
    for a,b in edges:R[a][b]=True
    for k in range(n):
        for i in range(n):
            if R[i][k]:
                for j in range(n):R[i][j]=R[i][j] or R[k][j]
    return R

def roots(n,edges):
    indeg=[0]*n
    for a,b in edges:indeg[b]+=1
    return [i for i,d in enumerate(indeg) if d==0]

def upstream_directed(n,R):
    return all(any(R[u][v] and R[u][w] for u in range(n)) for v in range(n) for w in range(n))

def check_dag(n,edges):
    # edges are constrained i<j, so acyclic by construction
    R=reach(n,edges); rt=roots(n,edges); ud=upstream_directed(n,R)
    universal=len(rt)==1 and all(R[rt[0]][v] for v in range(n))
    return ud,universal,len(rt)

fail=[]; dags=0; directed=0; unique=0
for n in range(1,7):
    poss=[(i,j) for i in range(n) for j in range(i+1,n)]
    for mask in range(1<<len(poss)):
        edges=[e for i,e in enumerate(poss) if mask>>i&1]
        dags+=1
        ud,univ,nr=check_dag(n,edges)
        directed+=ud; unique+=univ
        if ud!=univ:
            fail.append({'n':n,'edges':edges,'upstream_directed':ud,'unique_universal_root':univ,'root_count':nr})
            if len(fail)>=20:break
    if fail:break
# explicit controls
def eval_graph(names,elist):
    ix={x:i for i,x in enumerate(names)}; edges=[(ix[a],ix[b]) for a,b in elist]
    R=reach(len(names),edges)
    return {'roots':[names[i] for i in roots(len(names),edges)],'upstream_directed':upstream_directed(len(names),R)}
controls={
 'plural_roots':eval_graph(['r0','r1','e0','e1'],[('r0','e0'),('r1','e1')]),
 'downstream_merger':eval_graph(['r0','r1','m','e0','e1'],[('r0','m'),('r1','m'),('m','e0'),('m','e1')]),
 'positive':eval_graph(['r','a','b','e'],[('r','a'),('r','b'),('a','e'),('b','e')]),
}
# cycle handled separately: reachability is universal, roots absent.
cyc=eval_graph(['a','b','c'],[('a','b'),('b','c'),('c','a')]); controls['cycle']=cyc
assert controls['plural_roots']['roots']==['r0','r1'] and not controls['plural_roots']['upstream_directed']
assert controls['downstream_merger']['roots']==['r0','r1'] and not controls['downstream_merger']['upstream_directed']
assert controls['positive']['roots']==['r'] and controls['positive']['upstream_directed']
assert controls['cycle']['roots']==[] and controls['cycle']['upstream_directed']
out={'schema':'PMR007_DEEP_J_PRIMARY_RESULTS_V1','topologically_ordered_dags_checked':dags,'upstream_directed_dags':directed,'unique_universal_root_dags':unique,'theorem_failures':len(fail),'failures':fail,'controls':controls,'result':'PASS' if not fail else 'FAIL'}
p=Path(__file__).with_name('pmr007_deep_j_common_ancestry_primary_check_results.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
