#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

OUT=Path(__file__).with_name('pmr007_deep_q_articulability_groupoid_primary_check_v2_results.json')

def inv(p):
    q=[None]*len(p)
    for i,v in enumerate(p): q[v]=i
    return tuple(q)

def compose(f,g):
    # f after g
    return tuple(f[g[x]] for x in range(len(g)))

def tau(ei,ej):
    return compose(ej,inv(ei))

def main():
    systems=0; law_checks=0; law_failures=0; predicate_checks=0; predicate_failures=0
    by_n={}
    for n in range(2,6):
        perms=list(itertools.permutations(range(n)))
        e0=tuple(range(n)); count=0
        for e1 in perms:
            for e2 in perms:
                E=(e0,e1,e2); systems+=1; count+=1
                T={(i,j):tau(E[i],E[j]) for i in range(3) for j in range(3)}
                # identities, inverses, composition
                for i in range(3):
                    law_checks += 1
                    if T[(i,i)] != tuple(range(n)): law_failures += 1
                for i in range(3):
                    for j in range(3):
                        law_checks += 1
                        if compose(T[(j,i)],T[(i,j)]) != tuple(range(n)): law_failures += 1
                        for k in range(3):
                            law_checks += 1
                            if compose(T[(j,k)],T[(i,j)]) != T[(i,k)]: law_failures += 1
                # Every predicate on content transports exactly.
                for mask in range(1<<n):
                    pred={c for c in range(n) if (mask>>c)&1}
                    images=[{E[i][c] for c in pred} for i in range(3)]
                    for i in range(3):
                        for j in range(3):
                            predicate_checks += 1
                            transported={T[(i,j)][x] for x in images[i]}
                            if transported != images[j]: predicate_failures += 1
        by_n[str(n)]={"encoding_systems":count,"permutations":math.factorial(n)}
    res={
      "identity":"PMR-007-FEAG-1",
      "language_count":3,
      "content_sizes":[2,3,4,5],
      "systems_checked":systems,
      "law_checks":law_checks,
      "law_failures":law_failures,
      "predicate_transport_checks":predicate_checks,
      "predicate_transport_failures":predicate_failures,
      "by_content_size":by_n,
      "personal_impersonal_expansions_per_system":2,
      "overall":"PASS" if law_failures==0 and predicate_failures==0 else "FAIL",
      "scope_note":"Finite lossless encoding groupoids only; no absolute articulability, mentality, or world-truth claim."
    }
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__': main()
