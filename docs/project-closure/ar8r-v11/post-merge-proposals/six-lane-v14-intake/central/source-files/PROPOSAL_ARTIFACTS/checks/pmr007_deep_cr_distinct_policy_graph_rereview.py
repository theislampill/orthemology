#!/usr/bin/env python3
import itertools, json, random
from pathlib import Path

SEED=9024107
rng=random.Random(SEED)

def common_actions(elig, hs, s, A):
    return [a for a in range(A) if all(a in elig[h][s] for h in hs)]

def fp_regions(targets, trans, elig, hs, n, A):
    tstar=set(range(n))
    for h in hs:tstar &= targets[h]
    def pre(X):
        return {s for s in range(n) if any(all(trans[h][s][a] in X for h in hs)
                                           for a in common_actions(elig,hs,s,A))}
    V=set(tstar)
    while True:
        nv=tstar & pre(V)
        if nv==V:break
        V=nv
    W=set(V)
    while True:
        nw=W|pre(W)
        if nw==W:break
        W=nw
    return V,W

def reachable(start, policy, trans, elig, hs, n, A, stop=None):
    seen=set(); stack=[start]; invalid=False
    while stack:
        s=stack.pop()
        if stop is not None and s in stop: continue
        if s in seen: continue
        seen.add(s)
        a=policy[s]
        if a not in common_actions(elig,hs,s,A):
            invalid=True; continue
        for h in hs:
            stack.append(trans[h][s][a])
    return seen,invalid

def direct_regions(targets, trans, elig, hs, n, A):
    tstar=set(range(n))
    for h in hs:tstar &= targets[h]
    policies=list(itertools.product(range(A),repeat=n))
    V=set()
    for s in range(n):
        for p in policies:
            reach,invalid=reachable(s,p,trans,elig,hs,n,A)
            if not invalid and reach <= tstar:
                V.add(s); break
    W=set()
    for s in range(n):
        for p in policies:
            # policy must preserve V when V is reached
            preserve=True
            for v in V:
                a=p[v]
                if a not in common_actions(elig,hs,v,A) or any(trans[h][v][a] not in V for h in hs):
                    preserve=False; break
            if not preserve: continue
            outside,invalid=reachable(s,p,trans,elig,hs,n,A,stop=V)
            if invalid: continue
            # adversary can avoid V forever iff outside graph has a directed cycle.
            graph={u:[trans[h][u][p[u]] for h in hs if trans[h][u][p[u]] not in V]
                   for u in outside}
            color={u:0 for u in outside}
            def cyc(u):
                color[u]=1
                for v in graph[u]:
                    if v not in color: continue
                    if color[v]==1:return True
                    if color[v]==0 and cyc(v):return True
                color[u]=2; return False
            if not any(color[u]==0 and cyc(u) for u in list(outside)):
                W.add(s); break
    return V,W

def rand_nonempty_subset(A):
    mask=rng.randrange(1,1<<A)
    return {a for a in range(A) if mask>>a&1}

def random_system(n,A,H):
    targets=[]; trans=[]; elig=[]
    for _ in range(H):
        mask=rng.randrange(1<<n)
        targets.append({s for s in range(n) if mask>>s&1})
        trans.append([[rng.randrange(n) for _ in range(A)] for _ in range(n)])
        elig.append([rand_nonempty_subset(A) for _ in range(n)])
    return targets,trans,elig

def main():
    trials=15000; mismatches=[]; mono=[]
    for i in range(trials):
        n=3 if i%2==0 else 4; A=2; H=2
        t,tr,e=random_system(n,A,H)
        fp=fp_regions(t,tr,e,(0,1),n,A)
        direct=direct_regions(t,tr,e,(0,1),n,A)
        if fp!=direct:
            mismatches.append({'i':i,'n':n,'fp':[sorted(fp[0]),sorted(fp[1])],
                               'direct':[sorted(direct[0]),sorted(direct[1])]})
            if len(mismatches)>=3:break
        for hs in ((0,),(1,)):
            r=fp_regions(t,tr,e,hs,n,A)
            if not fp[0]<=r[0] or not fp[1]<=r[1]:
                mono.append({'i':i,'hs':hs});break
    # Independent Boolean formula check for the two-level source/world guard contract.
    guard_rows=source_rows=world_rows=0
    for bits in itertools.product([False,True],repeat=11):
        guard_rows+=1
        source=all(bits[:9]); world=source and bits[9] and bits[10]
        source_rows+=int(source); world_rows+=int(world)
    result={
      'seed':SEED,'random_policy_graph_trials':trials,
      'fixed_point_policy_graph_mismatches':len(mismatches),
      'first_mismatches':mismatches,
      'restriction_monotonicity_failures':len(mono),
      'guard_rows':guard_rows,'source_rows':source_rows,'world_rows':world_rows,
      'overall':'PASS' if not mismatches and not mono and guard_rows==2048
                   and source_rows==4 and world_rows==1 else 'FAIL'
    }
    out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
