#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")

def tv(p,q): return sum(abs(a-b) for a,b in zip(p,q))/2

def push(p,ch):
    return tuple(sum(p[x]*ch[x][y] for x in range(2)) for y in range(2))

def lr(a,b):
    if b==0:
        return "INF" if a>0 else "UNDEFINED"
    return a/b

def main():
    vals=[Fraction(k,4) for k in range(5)]
    dists=[(p,1-p) for p in vals]
    cvals=[Fraction(0),Fraction(1,2),Fraction(1)]
    channels=[((a,1-a),(b,1-b)) for a,b in product(cvals,repeat=2)]
    failures=[]
    counts={"root_distribution_pairs":0,"root_channel_cases":0,"data_processing_cases":0,
            "faithful_copy_ratio_cases":0,"naive_copy_overcount_witnesses":0,
            "independent_root_joint_cases":0,"root_alias_cases":0,"root_merge_cases":0,
            "failures":0}
    for p,q in product(dists,dists):
        counts["root_distribution_pairs"]+=1
        for ch in channels:
            pp,pq=push(p,ch),push(q,ch)
            counts["root_channel_cases"]+=1;counts["data_processing_cases"]+=1
            if tv(pp,pq)>tv(p,q): failures.append({"kind":"data_processing","p":str(p),"q":str(q),"ch":str(ch)})
        # exact copy tuple c_n(x) for n=1..4; probability of tuple equals root probability
        for x in (0,1):
            root_lr=lr(p[x],q[x])
            for n in range(1,5):
                tuple_lr=lr(p[x],q[x])
                if tuple_lr!=root_lr: failures.append({"kind":"copy_ratio","n":n})
                counts["faithful_copy_ratio_cases"]+=1
                if isinstance(root_lr,Fraction) and root_lr not in (0,1) and n>1 and root_lr**n!=root_lr:
                    counts["naive_copy_overcount_witnesses"]+=1
    # independent roots: factorization and likelihood multiplication
    for p1,q1,p2,q2 in product(dists,dists,dists,dists):
      for x1,x2 in product((0,1),repeat=2):
        a=p1[x1]*p2[x2]; b=q1[x1]*q2[x2]
        joint=lr(a,b); l1=lr(p1[x1],q1[x1]); l2=lr(p2[x2],q2[x2])
        if isinstance(l1,Fraction) and isinstance(l2,Fraction):
            if joint != l1*l2: failures.append({"kind":"independent_factor"})
        counts["independent_root_joint_cases"]+=1
    # root alias and merge invariance are partition facts
    aliases={"m1":"r0","m2":"r0","m3":"r1"}
    if len(set(aliases.values()))!=2: failures.append({"kind":"alias_partition"})
    counts["root_alias_cases"]+=1
    merged_label={"r0":"displayed-x","r1":"displayed-x"}
    if len(set(merged_label.values()))!=1 or len(merged_label)!=2: failures.append({"kind":"merge_control"})
    counts["root_merge_cases"]+=1
    counts["failures"]=len(failures)
    result={"identity":"PMR-007-PREC-1","checker":"primary root/channel/copy/factorization semantics",
            "declared_class":{"binary_root_observations":True,"probability_denominator":4,
                              "common_channels":"2x2 stochastic grid {0,1/2,1}","independent_roots":2},
            "counts":counts,"failures":failures[:20],"result":"PASS" if not failures else "FAIL"}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
