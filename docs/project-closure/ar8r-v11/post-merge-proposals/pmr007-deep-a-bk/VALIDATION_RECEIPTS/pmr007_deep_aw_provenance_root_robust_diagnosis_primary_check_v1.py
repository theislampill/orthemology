#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")

def dist(a,b): return sum(x!=y for x,y in zip(a,b))
def min_dist(code): return min(dist(a,b) for i,a in enumerate(code) for b in code[i+1:])
def words_with_errors(w,f,alphabet=(0,1)):
 out=set()
 n=len(w)
 for k in range(f+1):
  for pos in itertools.combinations(range(n),k):
   choices=[]
   for i in pos: choices.append([a for a in alphabet if a!=w[i]])
   for vals in itertools.product(*choices):
    v=list(w)
    for i,x in zip(pos,vals): v[i]=x
    out.add(tuple(v))
 return out
def errors_decodable(code,f):
 balls=[]
 for w in code: balls.append(words_with_errors(w,f))
 return all(balls[i].isdisjoint(balls[j]) for i in range(len(code)) for j in range(i+1,len(code)))
def erasures_decodable(code,f):
 n=len(code[0])
 for k in range(f+1):
  for erased in itertools.combinations(range(n),k):
   keep=[i for i in range(n) if i not in erased]
   seen=set()
   for w in code:
    proj=tuple(w[i] for i in keep)
    if proj in seen: return False
    seen.add(proj)
 return True

r={"schema":"pmr007-deep-aw-primary-check-v1-results","codebooks":0,
"error_cases":0,"error_distance_failures":0,"v1_error_threshold_failures":0,
"erasure_cases":0,"erasure_distance_failures":0,"controls":{},"overall":""}
# Three labelled hypotheses, four binary provenance roots: 2^(12)=4096 codebooks.
for bits in itertools.product((0,1),repeat=12):
 code=[tuple(bits[i*4:(i+1)*4]) for i in range(3)]
 d=min_dist(code)
 r["codebooks"]+=1
 for f in (0,1):
  actual=errors_decodable(code,f)
  correct=d>2*f
  v1=d>f
  r["error_cases"]+=1
  if actual!=correct: r["error_distance_failures"]+=1
  if actual!=v1: r["v1_error_threshold_failures"]+=1
  eactual=erasures_decodable(code,f)
  ecorrect=d>f
  r["erasure_cases"]+=1
  if eactual!=ecorrect: r["erasure_distance_failures"]+=1
# controls
r["controls"]["distance_two_one_error"]={"code":[[0,0],[1,1]],"distance":2,"one_error_decodable":errors_decodable([(0,0),(1,1)],1),"v1_predicts":True}
r["controls"]["distance_three_one_error"]={"code":[[0,0,0],[1,1,1]],"distance":3,"one_error_decodable":errors_decodable([(0,0,0),(1,1,1)],1)}
r["controls"]["one_erasure"]={"distance_two_survives":erasures_decodable([(0,0),(1,1)],1)}
r["controls"]["copied_root"]={"apparent_copies":40,"root_coordinates":1,"max_distance_contribution":1}
r["overall"]="PASS_WITH_V1_ERROR_THRESHOLD_COUNTEREXAMPLES" if r["error_distance_failures"]==0 and r["erasure_distance_failures"]==0 and r["v1_error_threshold_failures"]>0 else "FAIL"
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
print(json.dumps(r,indent=2,sort_keys=True))
