"""Exhaustive bounded search, not a theorem about all finite sizes."""
import json
from itertools import combinations
from grounded_support import powerset,minimize,minimum_cuts,quotient_supports,cuts

def partitions(n):
 def rec(a):
  if len(a)==n:yield tuple(a);return
  for v in range(max(a,default=-1)+2):yield from rec(a+[v])
 return list(rec([]))

def antichains(n):
 sets=[s for s in powerset(range(n)) if s]
 out=[]
 def rec(i,chosen):
  if i==len(sets):
   if chosen:out.append(frozenset(chosen))
   return
  rec(i+1,chosen)
  s=sets[i]
  if not any(t<=s or s<=t for t in chosen):rec(i+1,chosen+[s])
 rec(0,[]);return out

records=[];first=None;preservation_checks=0
for n in range(1,5):
 fs=antichains(n);ps=partitions(n);bad=0
 for f in fs:
  for p in ps:
   pi=dict(enumerate(p));old=minimum_cuts(f,set(range(n)));q=quotient_supports(f,pi);new=minimum_cuts(q,set(p))
   wrong=min(len({pi[x] for x in c}) for c in old);true=min(map(len,new))
   # Full inclusion-minimal cuts, unlike min-cardinality cuts, are sufficient.
   all_label_min=minimize(cuts(f,set(range(n))))
   transported=minimize(frozenset(pi[x] for x in c) for c in all_label_min)
   all_root_min=minimize(cuts(q,set(p)))
   assert transported==all_root_min
   preservation_checks+=1
   if wrong>true:
    bad+=1
    if first is None:first={'labels':n,'supports':[sorted(s) for s in sorted(f,key=lambda s:(len(s),sorted(s)))],'root_map':list(p),'wrong_cost':wrong,'true_cost':true,'label_minimum_cuts':[sorted(s) for s in old],'root_minimum_cuts':[sorted(s) for s in new]}
 records.append({'labels':n,'nonempty_antichains_without_empty_support':len(fs),'root_partitions':len(ps),'cases':len(fs)*len(ps),'strict_failures':bad})
assert first['labels']==4
out={'scope':'All nonempty support antichains without empty supports on 1 through 4 labelled roots, all set partitions as root maps','records':records,'first_counterexample':first,'full_inclusion_minimal_cut_transport_checks':preservation_checks,'no_global_minimality_claim_from_search_alone':True}
open('CUT_ORDER_SEARCH.json','w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
