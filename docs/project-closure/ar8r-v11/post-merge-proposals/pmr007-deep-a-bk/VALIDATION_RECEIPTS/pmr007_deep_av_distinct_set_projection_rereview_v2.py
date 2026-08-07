#!/usr/bin/env python3
from __future__ import annotations
import hashlib,itertools,json,random
from pathlib import Path
ROOT=Path(__file__).parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
res={"schema":"pmr007-deep-av-distinct-set-projection-rereview-v2-results",
"hash_check":{"checked":0,"mismatches":0},"exhaustive_pairs":0,"entailed_pairs":0,
"criterion_failures":0,"interval_count_failures":0,"unique_failures":0,
"random_large_cases":0,"random_large_failures":0,"controls":{},"overall":""}
for line in (ROOT/'PMR-007_DEEP_AV_V2_FROZEN_HASHES.sha256').read_text().splitlines():
 if not line.strip(): continue
 h,rel=line.split(None,1); p=ROOT/rel.strip(); got=hashlib.sha256(p.read_bytes()).hexdigest()
 res['hash_check']['checked']+=1
 if got!=h: res['hash_check']['mismatches']+=1

# X={0,1}, N={0,1,2,3}, Y={0,1}. A and C are sets of pairs.
Xs=range(2); Ns=range(4); Ys=range(2)
AXN=[(x,n) for x in Xs for n in Ns]
CNY=[(n,y) for n in Ns for y in Ys]
for abit in range(1<<8):
 A={AXN[i] for i in range(8) if (abit>>i)&1}
 SA={n for n in Ns if any((x,n) in A for x in Xs)}
 for cbit in range(1<<8):
  C={CNY[i] for i in range(8) if (cbit>>i)&1}
  TC={n for n in Ns if all((n,y) in C for y in Ys)}
  ent=all(((x,n) not in A) or ((n,y) in C) for x,n,y in itertools.product(Xs,Ns,Ys))
  crit=SA.issubset(TC)
  res['exhaustive_pairs']+=1
  if ent: res['entailed_pairs']+=1
  if ent!=crit: res['criterion_failures']+=1
  if ent:
   slack=len(TC-SA)
   count=0
   for ibit in range(1<<4):
    I={n for n in Ns if (ibit>>n)&1}
    if SA.issubset(I) and I.issubset(TC): count+=1
   if count!=(1<<slack): res['interval_count_failures']+=1
   if (count==1)!=(SA==TC): res['unique_failures']+=1

# Different dimensions and random set semantics: X,N,Y each four valuations.
random.seed(2026080602)
Xs=range(4); Ns=range(4); Ys=range(4)
for _ in range(20000):
 A={(x,n) for x in Xs for n in Ns if random.getrandbits(1)}
 C={(n,y) for n in Ns for y in Ys if random.getrandbits(1)}
 SA={n for n in Ns if any((x,n) in A for x in Xs)}
 TC={n for n in Ns if all((n,y) in C for y in Ys)}
 ent=all(((x,n) not in A) or ((n,y) in C) for x,n,y in itertools.product(Xs,Ns,Ys))
 if ent!=SA.issubset(TC): res['random_large_failures']+=1
 if ent:
  count=sum(1 for ibit in range(16) if SA.issubset({n for n in Ns if (ibit>>n)&1}) and {n for n in Ns if (ibit>>n)&1}.issubset(TC))
  if count!=(1<<(len(TC-SA))): res['random_large_failures']+=1
 res['random_large_cases']+=1

res['controls']['no_shared']={'rule':'if N has one valuation, satisfiable A and nonuniversal C make SA not subset TC'}
res['controls']['target_import']={'rule':'moving target symbol into shared vocabulary changes the partition, not the theorem'}
res['controls']['source_inconsistency']={'rule':'empty A makes SA empty and entailment vacuous'}
res['overall']='PASS' if res['hash_check']['mismatches']==0 and all(res[k]==0 for k in ['criterion_failures','interval_count_failures','unique_failures','random_large_failures']) else 'FAIL'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
