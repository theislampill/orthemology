#!/usr/bin/env python3
from __future__ import annotations
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json

OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")

def rows_from_code(code,n=4,m=4):
    return tuple(tuple((code>>(h*m+i))&1 for i in range(m)) for h in range(n))

def identifies(rows,J):
    sigs=[tuple(rows[h][i] for i in J) for h in range(len(rows))]
    return len(set(sigs))==len(sigs)

def na_min(rows):
    m=len(rows[0])
    for k in range(m+1):
        for J in combinations(range(m),k):
            if identifies(rows,J): return k,J
    return None,None

def hit_min(rows):
    n=len(rows);m=len(rows[0])
    edges=[]
    for a in range(n):
        for b in range(a+1,n):
            D={i for i in range(m) if rows[a][i]!=rows[b][i]}
            if not D:return None,None
            edges.append(D)
    for k in range(m+1):
        for J in combinations(range(m),k):
            if all(set(J)&D for D in edges):return k,J
    return None,None

def adaptive(rows):
    n=len(rows);m=len(rows[0])
    @lru_cache(None)
    def V(S,available):
        S=tuple(S);available=tuple(available)
        if len(S)<=1:return 0
        best=10**9
        for i in available:
            groups={}
            for h in S:groups.setdefault(rows[h][i],[]).append(h)
            if len(groups)<=1:continue
            rem=tuple(j for j in available if j!=i)
            vals=[]
            bad=False
            for g in groups.values():
                d=V(tuple(g),rem)
                if d>=10**9:bad=True;break
                vals.append(d)
            if not bad:best=min(best,1+max(vals))
        return best
    d=V(tuple(range(n)),tuple(range(m)))
    return None if d>=10**9 else d

def main():
    failures=[]
    counts={"binary_response_matrices":0,"fully_identifiable":0,"nonidentifiable":0,
            "hitting_characterization_cases":0,"adaptive_recurrence_cases":0,
            "adaptive_le_nonadaptive_cases":0,"strict_adaptive_gap_cases":0,
            "intervention_deletion_monotonicity_cases":0,"failures":0}
    for code in range(1<<16):
        rows=rows_from_code(code)
        counts["binary_response_matrices"]+=1
        n1,J1=na_min(rows);n2,J2=hit_min(rows)
        counts["hitting_characterization_cases"]+=1
        if n1!=n2:
            failures.append({"kind":"hitting_characterization","code":code,"na":n1,"hit":n2})
        full=identifies(rows,range(4))
        if full:counts["fully_identifiable"]+=1
        else:counts["nonidentifiable"]+=1
        if full!=(n1 is not None):failures.append({"kind":"full_identifiability","code":code})
        ad=adaptive(rows);counts["adaptive_recurrence_cases"]+=1
        if (ad is None)!=(n1 is None):failures.append({"kind":"adaptive_feasibility","code":code,"ad":ad,"na":n1})
        if ad is not None:
            counts["adaptive_le_nonadaptive_cases"]+=1
            if ad>n1:failures.append({"kind":"adaptive_bound","code":code,"ad":ad,"na":n1})
            if ad<n1:counts["strict_adaptive_gap_cases"]+=1
        # deleting one available intervention cannot improve either minimum
        for deleted in range(4):
            sub=tuple(tuple(row[i] for i in range(4) if i!=deleted) for row in rows)
            subna,_=na_min(sub)
            subad=adaptive(sub)
            counts["intervention_deletion_monotonicity_cases"]+=1
            if n1 is not None and subna is not None and subna<n1:
                failures.append({"kind":"na_deletion","code":code,"deleted":deleted})
            if ad is not None and subad is not None and subad<ad:
                failures.append({"kind":"ad_deletion","code":code,"deleted":deleted})
    witness=((0,0,0),(0,0,1),(0,1,0),(1,0,1))
    wna,wJ=na_min(witness);wad=adaptive(witness)
    if (wna,wad)!=(3,2):failures.append({"kind":"strict_gap_witness","na":wna,"ad":wad})
    counts["failures"]=len(failures)
    result={"identity":"PMR-007-PFIT-1","checker":"primary exhaustive binary response-matrix semantics",
            "declared_class":{"accounts":4,"interventions":4,"response_alphabet":2,"matrices":1<<16},
            "counts":counts,"strict_gap_witness":{"rows":witness,"delta_NA":wna,"delta_AD":wad,"basis":wJ},
            "failures":failures[:20],"result":"PASS" if not failures else "FAIL"}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not failures else 1
if __name__=='__main__':raise SystemExit(main())
