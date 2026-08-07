#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
def d(a,b): return sum(x!=y for x,y in zip(a,b))
def md(code): return min(d(a,b) for i,a in enumerate(code) for b in code[i+1:])
def balls(w,f):
 out=set(); n=len(w)
 for k in range(f+1):
  for pos in itertools.combinations(range(n),k):
   v=list(w)
   for i in pos: v[i]^=1
   out.add(tuple(v))
 return out
def err_ok(code,f):
 B=[balls(w,f) for w in code]
 return all(B[i].isdisjoint(B[j]) for i in range(len(B)) for j in range(i+1,len(B)))
def era_ok(code,f):
 n=len(code[0])
 for k in range(f+1):
  for er in itertools.combinations(range(n),k):
   keep=[i for i in range(n) if i not in er]; seen=set()
   for w in code:
    p=tuple(w[i] for i in keep)
    if p in seen:return False
    seen.add(p)
 return True
r={"schema":"pmr007-deep-aw-primary-check-v2-results","codebooks":0,"error_cases":0,"erasure_cases":0,
"error_failures":0,"erasure_failures":0,"subset_cases":0,"multicover_failures":0,
"minimal_error_root_histogram":{},"minimal_erasure_root_histogram":{},"controls":{},"overall":""}
for bits in itertools.product((0,1),repeat=12):
 code=[tuple(bits[i*4:(i+1)*4]) for i in range(3)]; r['codebooks']+=1
 for f in (0,1):
  r['error_cases']+=1
  if err_ok(code,f)!=(md(code)>=2*f+1):r['error_failures']+=1
  r['erasure_cases']+=1
  if era_ok(code,f)!=(md(code)>=f+1):r['erasure_failures']+=1
 # root subset selection, f=0 and f=1
 for mode,f,need in [('err',0,1),('err',1,3),('era',1,2)]:
  feasible=[]
  for mask in range(16):
   idx=[i for i in range(4) if (mask>>i)&1]
   if not idx: continue
   sub=[tuple(w[i] for i in idx) for w in code]
   direct=(err_ok(sub,f) if mode=='err' else era_ok(sub,f))
   paircrit=all(sum(code[a][i]!=code[b][i] for i in idx)>=need for a in range(3) for b in range(a+1,3))
   r['subset_cases']+=1
   if direct!=paircrit:r['multicover_failures']+=1
   if direct:feasible.append(len(idx))
  if feasible:
   key='minimal_error_root_histogram' if mode=='err' else 'minimal_erasure_root_histogram'
   k=str(min(feasible));r[key][k]=r[key].get(k,0)+1
r['controls']['distance_two']={'error_f1':err_ok([(0,0),(1,1)],1),'erasure_f1':era_ok([(0,0),(1,1)],1)}
r['controls']['distance_three']={'error_f1':err_ok([(0,0,0),(1,1,1)],1)}
r['controls']['copies_one_root']={'apparent_messages':40,'root_coordinates':1,'distance_contribution_max':1}
r['controls']['alias_contraction']={'before_distance':2,'after_joint_root_distance':1}
r['overall']='PASS' if all(r[k]==0 for k in ['error_failures','erasure_failures','multicover_failures']) else 'FAIL'
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
