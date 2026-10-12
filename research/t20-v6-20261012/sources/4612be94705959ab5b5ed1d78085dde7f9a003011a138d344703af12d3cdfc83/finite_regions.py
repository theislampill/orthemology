"""Fresh independent exhaustive-component oracle; not the production solver."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json, hashlib
HERE=Path(__file__).resolve().parents[1]
def subsets(items):
    items=tuple(sorted(items))
    return [frozenset(c) for k in range(1,len(items)+1) for c in combinations(items,k)]
def reachable(start,edges):
    out={start}
    while True:
        nxt=out|{y for s in out for y in edges.get(s,set())}
        if nxt==out:return out
        out=nxt
def solve(raw,good,menu,conditional=False,ignore_child=False):
    P=tuple(tuple(tuple(tuple(F(x) for x in row) for row in state) for state in model) for model in raw)
    M,N,K=len(P),len(P[0]),len(P[0][0]);states=set(range(N));regions={};traces={}
    assert all(len(model)==N for model in P)
    assert all(len(state)==K for model in P for state in model)
    assert all(len(row)==N and min(row)>=0 and sum(row)==1 for model in P for state in model for row in state)
    for B in subsets(range(M)):
        update=lambda s,a,y:frozenset(t for t in B if P[t][s][a][y]>0)
        inner=lambda s,a:{y for y in states if update(s,a,y)==B}
        exiting=lambda t,s,a:sum(P[t][s][a][y] for y in states if update(s,a,y) and update(s,a,y)!=B)
        def step(W):
            allowed={(s,a) for s in W for a in menu(B,s) if all(
                (update(s,a,y)!=B or y in W) and
                (ignore_child or not update(s,a,y) or update(s,a,y)==B or y in regions[update(s,a,y)])
                for y in states)}
            edges={s:{y for z,a in allowed if z==s for y in inner(s,a)} for s in W}
            result=set(W)
            for t in B:
                target=set()
                eligible={e for e in allowed if e in good[t] and exiting(t,*e)==0}
                for E in subsets(eligible):
                    C={s for s,a in E};adj={s:{y for z,a in E if z==s for y in inner(s,a)} for s in C}
                    if any(not inner(s,a)<=C for s,a in E):continue
                    if any(reachable(s,adj)!=C for s in C):continue
                    def match(v):
                        for s,a in E:
                            if not conditional:
                                if P[t][s][a]!=P[v][s][a]:return False
                            else:
                                I=inner(s,a);x=sum(P[t][s][a][y] for y in I);z=sum(P[v][s][a][y] for y in I)
                                if not x or not z or any(P[t][s][a][y]/x!=P[v][s][a][y]/z for y in I):return False
                        return True
                    if all(not match(v) or E<=good[v] for v in B):target|=C
                target|={s for s,a in allowed if exiting(t,s,a)>0}
                result&={s for s in W if reachable(s,edges)&target}
            return frozenset(result)
        W=frozenset(states);trace=[W]
        while True:
            nxt=step(W);trace.append(nxt)
            if nxt==W:break
            assert nxt<W;W=nxt
        regions[B]=W;traces[B]=trace
    return regions,traces

def loops(m,n,k):return [[[[F(y==s) for y in range(n)] for a in range(k)] for s in range(n)] for t in range(m)]
rows=[]
def case(name,P,G,menu,want,**opts):
    R,T=solve(P,G,menu,**opts);B=frozenset(range(len(P)));assert R[B]==frozenset(want),(name,R,T)
    rows.append({'name':name,'region':sorted(R[B]),'iterations':[sorted(x) for x in T[B]],'all_support_regions':{','.join(map(str,b)):sorted(w) for b,w in R.items()}});return R,T
for eta in [F(0),F(1,2),F(1,1000)]:
    P=loops(2,2,2)
    for a in range(2):P[1][0][a]=[1-eta,eta]
    case('absent_exit_'+str(eta),P,[{(0,1)},{(1,0),(1,1)}],lambda b,s:{0,1},{0} if eta else set())
P=loops(2,2,1);P[1][0][0]=[F(1,2),F(1,2)];G=[{(0,0)},{(1,0)}]
case('full_row_equality',P,G,lambda b,s:{0},{0})
case('incorrect_conditional_equality',P,G,lambda b,s:{0},set(),conditional=True)
P=loops(3,3,3);P[0][0][0]=[0,1,0];P[1][0][0]=[0,F(1,2),F(1,2)];P[2][0][0]=[0,0,1]
G=[{(1,1)},{(1,1),(2,2)},{(2,2)}]
def menu(B,s):return {0} if s==0 else ({1} if s==1 else {2})
def broken(B,s):return {2} if B==frozenset({0,1}) and s==1 else menu(B,s)
case('correct_support_state_children',P,G,menu,{0});case('losing_child',P,G,broken,set());case('incorrect_child_omission',P,G,broken,{0},ignore_child=True)
P=loops(2,4,2)
for t,p in [(0,F(1,4)),(1,F(3,4))]:
    for s in range(4):
        low=0 if s<2 else 2;P[t][s][0]=[F(0)]*4;P[t][s][0][low]=p;P[t][s][0][low+1]=1-p
        if s<2:P[t][s][1]=[0,0,1,0]
G=[{(0,0),(1,0)},{(2,0),(3,0),(2,1),(3,1)}]
R,T=case('one_way_trap',P,G,lambda b,s:{0,1},set());assert T[frozenset({0,1})][1]==frozenset({0,1})
P=loops(2,1,2)
case('identical_opposite',P,[{(0,0)},{(0,1)}],lambda b,s:{0,1},set());case('common_good',P,[{(0,0)},{(0,0)}],lambda b,s:{0,1},{0});case('empty_menu',P,[{(0,0)},{(0,0)}],lambda b,s:set(),set())
# Container representation must not affect exact probability-row equality.
mixed=loops(2,1,2);mixed[1][0][0]=tuple(mixed[1][0][0])
assert solve(mixed,[{(0,0)},{(0,1)}],lambda b,s:{0,1})[0][frozenset({0,1})]==frozenset()
out={'status':'FRESH_PASS_FINITE_REGION_CONTROLS','cases':rows,'count':len(rows),'mixed_container_control':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite oracle corroboration only; no production-API or universal proof qualification.'}
(HERE/'REGION_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(rows),'plus mixed-container boundary')
