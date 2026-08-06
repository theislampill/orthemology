#!/usr/bin/env python3
from __future__ import annotations
import hashlib,itertools,json,random
from pathlib import Path
ROOT=Path(__file__).parents[1]; OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
AL=(0,1,2)
def d(a,b):return sum(x!=y for x,y in zip(a,b))
def md(C):return min(d(a,b) for i,a in enumerate(C) for b in C[i+1:])
def ball(w,f):
 out=set();n=len(w)
 for k in range(f+1):
  for pos in itertools.combinations(range(n),k):
   choices=[[a for a in AL if a!=w[i]] for i in pos]
   for vals in itertools.product(*choices):
    v=list(w)
    for i,x in zip(pos,vals):v[i]=x
    out.add(tuple(v))
 return out
def err(C,f):
 B=[ball(w,f) for w in C]
 return all(B[i].isdisjoint(B[j]) for i in range(len(B)) for j in range(i+1,len(B)))
def era(C,f):
 n=len(C[0])
 for k in range(f+1):
  for er in itertools.combinations(range(n),k):
   keep=[i for i in range(n) if i not in er];seen=set()
   for w in C:
    p=tuple(w[i] for i in keep)
    if p in seen:return False
    seen.add(p)
 return True
r={"schema":"pmr007-deep-aw-distinct-ternary-rereview-v2-results","hash_check":{"checked":0,"mismatches":0},
"exhaustive_codebooks":0,"exhaustive_error_failures":0,"exhaustive_erasure_failures":0,
"random_codebooks":0,"random_error_failures":0,"random_erasure_failures":0,"subset_multicover_cases":0,"subset_failures":0,"controls":{},"overall":""}
for line in (ROOT/'PMR-007_DEEP_AW_V2_FROZEN_HASHES.sha256').read_text().splitlines():
 if not line.strip():continue
 h,rel=line.split(None,1);p=ROOT/rel.strip();got=hashlib.sha256(p.read_bytes()).hexdigest();r['hash_check']['checked']+=1
 if got!=h:r['hash_check']['mismatches']+=1
# Exhaustive 3 hypotheses, 3 ternary roots.
words=list(itertools.product(AL,repeat=3))
for C in itertools.product(words,repeat=3):
 r['exhaustive_codebooks']+=1;dist=md(C)
 if err(C,1)!=(dist>=3):r['exhaustive_error_failures']+=1
 if era(C,1)!=(dist>=2):r['exhaustive_erasure_failures']+=1
# Random larger and root subsets.
random.seed(2026080603)
for _ in range(15000):
 C=[tuple(random.choice(AL) for _ in range(5)) for __ in range(4)]
 dist=md(C);r['random_codebooks']+=1
 if err(C,1)!=(dist>=3):r['random_error_failures']+=1
 if era(C,1)!=(dist>=2):r['random_erasure_failures']+=1
 for _j in range(3):
  idx=[i for i in range(5) if random.getrandbits(1)]
  if not idx:idx=[random.randrange(5)]
  sub=[tuple(w[i] for i in idx) for w in C]
  direct=err(sub,1)
  paircrit=all(sum(C[a][i]!=C[b][i] for i in idx)>=3 for a in range(4) for b in range(a+1,4))
  r['subset_multicover_cases']+=1
  if direct!=paircrit:r['subset_failures']+=1
r['controls']['distance2']={'error_f1':err([(0,0),(1,1)],1),'erasure_f1':era([(0,0),(1,1)],1)}
r['controls']['distance3']={'error_f1':err([(0,0,0),(1,1,1)],1)}
r['controls']['same_root_tuple']={'rule':'many within-root test outputs form one alphabet symbol and one Hamming coordinate'}
r['overall']='PASS' if r['hash_check']['mismatches']==0 and all(r[k]==0 for k in ['exhaustive_error_failures','exhaustive_erasure_failures','random_error_failures','random_erasure_failures','subset_failures']) else 'FAIL'
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
