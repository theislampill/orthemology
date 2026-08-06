#!/usr/bin/env python3
from __future__ import annotations
from itertools import product, combinations
from functools import lru_cache
from pathlib import Path
import hashlib, json, random
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
RECEIPT=ROOT/"PMR-007_DEEP_AS_V2_FROZEN_HASHES.sha256"

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def nonadaptive_partition(rows):
    n=len(rows);m=len(rows[0])
    for k in range(m+1):
        for J in combinations(range(m),k):
            blocks={tuple(rows[h][i] for i in J) for h in range(n)}
            if len(blocks)==n:return k
    return None

def pair_hitting(rows):
    n=len(rows);m=len(rows[0]);edges=[]
    for a in range(n):
      for b in range(a+1,n):
        mask=0
        for i in range(m):
            if rows[a][i]!=rows[b][i]:mask|=1<<i
        if mask==0:return None
        edges.append(mask)
    for k in range(m+1):
      for J in combinations(range(m),k):
        jm=sum(1<<i for i in J)
        if all(jm&e for e in edges):return k
    return None

def adaptive_partition(rows):
    n=len(rows);m=len(rows[0]);INF=999
    @lru_cache(None)
    def rec(S,avail):
        if S & (S-1)==0:return 0
        best=INF
        for i in range(m):
            if not (avail>>i)&1:continue
            groups={}
            for h in range(n):
                if (S>>h)&1:groups.setdefault(rows[h][i],0);groups[rows[h][i]]|=1<<h
            if len(groups)<=1:continue
            d=1+max(rec(g,avail&~(1<<i)) for g in groups.values())
            best=min(best,d)
        return best
    d=rec((1<<n)-1,(1<<m)-1)
    return None if d>=INF else d

def check(rows,tag,fail,counts):
    na=nonadaptive_partition(rows);hit=pair_hitting(rows);ad=adaptive_partition(rows)
    counts["matrices_checked"]+=1
    if na!=hit:fail.append({"kind":"hitting_mismatch","tag":tag,"na":na,"hit":hit,"rows":rows})
    if (na is None)!=(ad is None):fail.append({"kind":"adaptive_feasibility","tag":tag,"na":na,"ad":ad})
    if na is not None and ad>na:fail.append({"kind":"adaptive_bound","tag":tag,"na":na,"ad":ad})
    if na is not None:counts["identifiable"]+=1
    else:counts["nonidentifiable"]+=1
    if na is not None and ad<na:counts["strict_adaptive_gaps"]+=1

def main():
    fail=[];counts={"frozen_files":0,"hash_mismatches":0,"exhaustive_ternary_matrices":0,
                    "random_binary_matrices":0,"matrices_checked":0,"identifiable":0,"nonidentifiable":0,
                    "strict_adaptive_gaps":0,"surface_projection_controls":0,"failures":0}
    for line in RECEIPT.read_text().splitlines():
        exp,rel=line.split(maxsplit=1);p=ROOT/rel;counts["frozen_files"]+=1
        if sha(p)!=exp:fail.append({"kind":"hash","path":rel});counts["hash_mismatches"]+=1
    # exhaustive independent class: 3 accounts x 3 interventions x ternary responses
    for flat in product(range(3),repeat=9):
        rows=tuple(tuple(flat[h*3+i] for i in range(3)) for h in range(3))
        check(rows,"ternary3x3",fail,counts);counts["exhaustive_ternary_matrices"]+=1
    rng=random.Random(20260806)
    for k in range(50000):
        rows=tuple(tuple(rng.randrange(2) for _ in range(5)) for _ in range(5))
        check(rows,f"binary5x5-{k}",fail,counts);counts["random_binary_matrices"]+=1
    witness=((0,0,0),(0,0,1),(0,1,0),(1,0,1))
    if (nonadaptive_partition(witness),adaptive_partition(witness))!=(3,2):
        fail.append({"kind":"strict_gap_witness"})
    # Complete certificates differ while their surface action projection is identical.
    cert_rows=((('act','source-a'),),(('act','source-b'),))
    action_rows=(("act",),("act",))
    if nonadaptive_partition(cert_rows)!=1 or nonadaptive_partition(action_rows) is not None:
        fail.append({"kind":"surface_projection"})
    counts["surface_projection_controls"]+=1
    counts["failures"]=len(fail)
    res={"identity":"PMR-007-PFIT-1","rereview":"distinct partition-refinement and bitmask decision-tree DP",
         "counts":counts,"failures":fail[:20],"result":"PASS" if not fail else "FAIL",
         "scope_notes":["deterministic static response maps","complete certificate objects","intervention feasibility assumed","identification is not truth"]}
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
    print(json.dumps(res,indent=2,sort_keys=True));return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
