#!/usr/bin/env python3
from itertools import product
import json
from pathlib import Path

N_GUARDS=9
W_GUARDS=2

def pre(X, targets, transitions, hs, n=2, actions=2):
    return {s for s in range(n) if any(all(transitions[h][s][a] in X for h in hs)
                                      for a in range(actions))}

def fixed(targets, transitions, hs, n=2, actions=2):
    tstar=set(range(n))
    for h in hs: tstar &= targets[h]
    V=set(tstar)
    while True:
        nv=tstar & pre(V,targets,transitions,hs,n,actions)
        if nv==V: break
        V=nv
    W=set(V)
    while True:
        nw=W | pre(W,targets,transitions,hs,n,actions)
        if nw==W: break
        W=nw
    return V,W

def trans(bits):
    it=iter(bits); return [[next(it),next(it)] for _ in range(2)]

def main():
    source_rows=world_rows=0
    total_rows=0
    for row in product([0,1],repeat=N_GUARDS+W_GUARDS):
        total_rows+=1
        if all(row[:N_GUARDS]): source_rows+=1
        if all(row): world_rows+=1
    source_deletions=sum(not all(([1]*i+[0]+[1]*(N_GUARDS-i-1))) for i in range(N_GUARDS))
    world_deletions=0
    for i in range(W_GUARDS):
        row=[1]*(N_GUARDS+W_GUARDS); row[N_GUARDS+i]=0
        if all(row[:N_GUARDS]) and not all(row): world_deletions+=1

    systems=0; failures=[]
    masks=range(4); transbits=list(product([0,1],repeat=4))
    for m0,m1 in product(masks,repeat=2):
        targets=[{s for s in range(2) if (m0>>s)&1},
                 {s for s in range(2) if (m1>>s)&1}]
        for b0,b1 in product(transbits,repeat=2):
            trs=[trans(b0),trans(b1)]
            vf,wf=fixed(targets,trs,(0,1))
            for hs in ((0,),(1,)):
                vr,wr=fixed(targets,trs,hs)
                if not (vf<=vr and wf<=wr):
                    failures.append((targets,trs,hs,vf,wf,vr,wr)); break
            systems+=1

    family_shapes={
      'empty': len(set())==0,
      'singleton': len({0})==1,
      'plural': len({0,1})>1,
    }
    result={
      'guard_rows':total_rows,
      'source_relative_licensed_rows':source_rows,
      'world_directed_licensed_rows':world_rows,
      'source_guard_single_deletion_witnesses':source_deletions,
      'world_guard_single_deletion_witnesses':world_deletions,
      'family_shapes_exercised':family_shapes,
      'exhaustive_two_state_systems':systems,
      'inheritance_monotonicity_failures':len(failures),
      'first_failure':str(failures[0]) if failures else None,
      'overall':'PASS' if (total_rows==2048 and source_rows==4 and world_rows==1
          and source_deletions==9 and world_deletions==2 and all(family_shapes.values())
          and systems==4096 and not failures) else 'FAIL'
    }
    out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
