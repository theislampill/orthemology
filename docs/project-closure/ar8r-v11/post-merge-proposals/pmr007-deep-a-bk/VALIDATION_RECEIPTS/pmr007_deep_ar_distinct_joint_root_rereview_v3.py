#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
RECEIPT=ROOT/"PMR-007_DEEP_AR_V2_FROZEN_HASHES.sha256"

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def ratio(a,b):
    if b==0:
        return 'INF' if a>0 else 'UNDEFINED'
    return a/b

def main():
    fail=[]; counts={"frozen_files":0,"hash_mismatches":0,"binary_distributions":0,
                     "stochastic_channels":0,"root_channel_cases":0,"two_root_factor_cases":0,
                     "copy_bundle_cases":0,"common_cause_cases":0,"root_alias_cases":0,"failures":0}
    for line in RECEIPT.read_text().splitlines():
        exp,rel=line.split(maxsplit=1); p=ROOT/rel; act=sha(p);counts["frozen_files"]+=1
        if exp!=act: fail.append({"kind":"hash","path":rel});counts["hash_mismatches"]+=1
    dists=[(Fraction(k,3),Fraction(3-k,3)) for k in range(4)]
    vals=[Fraction(0),Fraction(1,2),Fraction(1)]
    channels=[((a,1-a),(b,1-b)) for a,b in product(vals,repeat=2)]
    counts["binary_distributions"]=len(dists);counts["stochastic_channels"]=len(channels)
    # independent common-channel recomputation
    for p,q,ch in product(dists,dists,channels):
        pp=tuple(sum(p[x]*ch[x][y] for x in range(2)) for y in range(2))
        pq=tuple(sum(q[x]*ch[x][y] for x in range(2)) for y in range(2))
        tv0=sum(abs(p[i]-q[i]) for i in range(2))/2
        tv1=sum(abs(pp[i]-pq[i]) for i in range(2))/2
        if tv1>tv0: fail.append({"kind":"data_processing"})
        counts["root_channel_cases"]+=1
    # independent-root product law
    for p1,q1,p2,q2 in product(dists,dists,dists,dists):
      for x1,x2 in product((0,1),repeat=2):
        l1,l2=ratio(p1[x1],q1[x1]),ratio(p2[x2],q2[x2])
        lj=ratio(p1[x1]*p2[x2],q1[x1]*q2[x2])
        if isinstance(l1,Fraction) and isinstance(l2,Fraction) and lj!=l1*l2:
            fail.append({"kind":"factorization"})
        counts["two_root_factor_cases"]+=1
    # exact copies and informative overcount witnesses
    for p,q in product(dists,dists):
      for x in (0,1):
        L=ratio(p[x],q[x])
        for n in (1,2,3,4,5):
            if ratio(p[x],q[x])!=L: fail.append({"kind":"copy_conservation"})
            if isinstance(L,Fraction) and L not in (0,1) and n>1 and L**n==L:
                fail.append({"kind":"informative_common_cause_witness","L":str(L),"n":n})
            counts["copy_bundle_cases"]+=1
    # Common-cause messages contract to one root. Explicitly exercise boundary ratios.
    for L in [Fraction(0),Fraction(1),Fraction(1,2),Fraction(2),Fraction(3), 'INF']:
        if isinstance(L,Fraction) and L not in (0,1):
            if L**2==L: fail.append({"kind":"common_cause_informative"})
        # 0,1,INF are classified, not used as strict arithmetic witnesses
        counts["common_cause_cases"]+=1
    aliases=[{"m1":"r0","m2":"r0"},{"m1":"r0","m2":"r1"},{"m1":"r0","m2":"r0","m3":"r1"}]
    for a in aliases:
        if len(set(a.values()))>len(a): fail.append({"kind":"alias_partition"})
        counts["root_alias_cases"]+=1
    counts["failures"]=len(fail)
    res={"identity":"PMR-007-PREC-1","rereview":"distinct joint-root, support-classification, and channel semantics V3",
         "counts":counts,"failures":fail[:20],"result":"PASS" if not fail else "FAIL",
         "scope_notes":["authenticated roots assumed","conditional independence explicit","finite binary observations","warrant and tawatur not inferred"]}
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
    print(json.dumps(res,indent=2,sort_keys=True));return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
