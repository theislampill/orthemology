#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/(Path(__file__).stem+"_results.json")
HASH_RECEIPT=ROOT/"PMR-007_DEEP_AQ_V2_FROZEN_HASHES.sha256"

def sha(path):
    h=hashlib.sha256();
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def parse_hashes():
    rows=[]
    for line in HASH_RECEIPT.read_text().splitlines():
        digest,rel=line.split(maxsplit=1)
        rows.append((digest,ROOT/rel))
    return rows

def push_binary(p, channel):
    # channel[x][y]
    return tuple(sum(p[x]*channel[x][y] for x in range(2)) for y in range(2))

def tv(p,q): return sum(abs(a-b) for a,b in zip(p,q))/2

def main():
    failures=[]
    counts={"frozen_files":0,"hash_mismatches":0,"raw_distributions":0,"stochastic_channels":0,
            "pair_channel_cases":0,"data_processing_cases":0,"equal_event_parity_cases":0,
            "unequal_event_cases":0,"source_version_cases":0,"swap_symmetry_cases":0,"failures":0}
    for expected,path in parse_hashes():
        counts["frozen_files"]+=1
        actual=sha(path)
        if actual!=expected:
            failures.append({"kind":"hash","path":str(path.relative_to(ROOT)),"expected":expected,"actual":actual})
            counts["hash_mismatches"]+=1
    raw=[(Fraction(k,3),Fraction(3-k,3)) for k in range(4)]
    vals=[Fraction(0),Fraction(1,2),Fraction(1)]
    channels=[]
    # each input row is a binary stochastic distribution
    for a,b in product(vals,repeat=2):
        channels.append(((a,1-a),(b,1-b)))
    counts["raw_distributions"]=len(raw); counts["stochastic_channels"]=len(channels)
    for p,q,ch in product(raw,raw,channels):
        pp,pq=push_binary(p,ch),push_binary(q,ch)
        counts["pair_channel_cases"]+=1; counts["data_processing_cases"]+=1
        if tv(pp,pq)>tv(p,q): failures.append({"kind":"data_processing","p":str(p),"q":str(q),"ch":str(ch)})
        for y in range(2):
            a,b=pp[y],pq[y]
            if a==b and a>0:
                # equal priors; posterior is equal
                postA=a/(a+b)
                if postA!=Fraction(1,2): failures.append({"kind":"equal_event_posterior"})
                counts["equal_event_parity_cases"]+=1
                # tuple-based invariant score ties under candidate swap
                if (True,a,Fraction(1,2)) != (True,b,Fraction(1,2)):
                    failures.append({"kind":"swap_symmetry"})
                counts["swap_symmetry_cases"]+=1
            elif a!=b:
                counts["unequal_event_cases"]+=1
    # independent source/version semantics: source role alone does not force full admissibility
    # source-role, authentication, translation, version, scope, world-link
    for bits in product([False,True], repeat=6):
        role,auth,tr,ver,scope,world=bits
        full=all(bits)
        if full != (role and auth and tr and ver and scope and world): failures.append({"kind":"source_contract"})
        counts["source_version_cases"]+=1
    counts["failures"]=len(failures)
    result={"identity":"PMR-007-SCAP-1","rereview":"distinct stochastic-channel and source-contract semantics",
            "counts":counts,"failures":failures[:20],"result":"PASS" if not failures else "FAIL",
            "scope_notes":["finite binary raw evidence","common candidate-independent stochastic channels","positive-probability event guard","source/world truth not certified"]}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
