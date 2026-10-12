#!/usr/bin/env python3
"""Finite illustrations of possible-dependence well-foundedness.

No finite enumeration establishes a metaphysical accessibility relation.
"""
from itertools import product
from pathlib import Path
import json


def acyclic(n, edges):
    reach=set(edges)
    while True:
        new=reach|{(a,d) for a,b in reach for c,d in reach if b==c}
        if any(a==b for a,b in new): return False
        if new==reach: return True
        reach=new


def main():
    inspected=0; premises_hold=0; checks=0
    for n in range(1,4):
        pairs=[(i,j) for i in range(n) for j in range(n) if i!=j]
        for profiles in product([1,2,3], repeat=n):
            ex=[{i for i,v in enumerate(profiles) if v>>w&1} for w in range(2)]
            necessary=ex[0]&ex[1]
            valid_edges=[[e for e in pairs if set(e)<=ex[w]] for w in range(2)]
            all_edges=[[{e for j,e in enumerate(es) if mask>>j&1}
                        for mask in range(1<<len(es))] for es in valid_edges]
            for g0,g1 in product(*all_edges):
                inspected+=1
                gs=[g0,g1]
                possible=g0|g1
                cdep=all(any(b==x for a,b in gs[w])
                         for w in range(2) for x in ex[w]-necessary)
                if cdep and acyclic(n,possible):
                    premises_hold+=1
                    roots=set(range(n))-{b for a,b in possible}
                    assert roots and roots<=necessary
                    for r in roots:
                        assert all(r in ex[w] and not any(b==r for a,b in gs[w])
                                   for w in range(2))
                        checks+=1
    # Every world has a unique root and all entities exist necessarily;
    # nevertheless no individual is underived at both worlds.
    rotation={'worlds':['w0','w1'],'entities':['a','b'],
              'existence':[['a','b'],['a','b']],
              'grounding':[[['a','b']],[['b','a']]],
              'unique_roots':['a','b'],
              'necessary_entities':['a','b'],
              'uniform_underived_entities':[],
              'point':'worldwise foundation is strictly weaker than possible-dependence foundation'}
    assert acyclic(2,{(0,1)}) and acyclic(2,{(1,0)})
    assert not acyclic(2,{(0,1),(1,0)})
    data={'status':'PASS','modal_structures_inspected':inspected,
          'structures_satisfying_global_foundation_and_contingent_dependence':premises_hold,
          'uniform_root_checks':checks,
          'scope':'two worlds; up to three potentially concrete entities; all endpoint-valid loopless grounding relations',
          'rotation_countermodel':rotation}
    p=Path(__file__).resolve().parent/'uniform_foundation_results.json'
    p.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__': main()
