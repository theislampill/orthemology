#!/usr/bin/env python3
"""Exhaustive finite comparison; arbitrary/infinite fields use the Lean proof."""
import itertools,json

def relation(n,mask):return {(a,b) for a in range(n) for b in range(n) if mask&(1<<(a*n+b))}
def strict(r):return all(a!=b for a,b in r) and all((a,c) in r for a,b in r for bb,c in r if b==bb)
def below(r,a,b):return a==b or (a,b) in r
def root(r,g):return not any(x==g for _,x in r)
def cover(n,r,g,x):return below(r,g,x) and all(not below(r,y,x) or below(r,g,y) for y in range(n))
def components(n,r):
 remaining=set(range(n));out=[]
 while remaining:
  todo=[next(iter(remaining))];seen=set(todo)
  while todo:
   x=todo.pop()
   for y in range(n):
    if y not in seen and ((x,y) in r or (y,x) in r):seen.add(y);todo.append(y)
  remaining-=seen;out.append(seen)
 return out

def main():
 census=[]
 for n in range(1,5):
  row={'n':n,'relations':1<<(n*n),'strict_orders':0,'connected':0,'locally_complete':0,'local_and_connected':0,'least_ancestor':0,'unique_root_cones':0,'pointwise_equivalence_checks':0}
  for mask in range(1<<(n*n)):
   r=relation(n,mask)
   if not strict(r):continue
   row['strict_orders']+=1;cs=components(n,r);conn=len(cs)==1
   sources={x:[g for g in range(n) if cover(n,r,g,x)] for x in range(n)}
   local=all(sources.values());least=[g for g in range(n) if all(below(r,g,x) for x in range(n))]
   uniques=all(sum(root(r,g) and below(r,g,x) for g in range(n))==1 for x in range(n))
   assert local==uniques
   assert (local and conn)==bool(least)
   for x,gs in sources.items():
    unique=sum(root(r,g) and below(r,g,x) for g in range(n))==1
    supported=all(not below(r,y,x) or any(root(r,h) and below(r,h,y) for h in range(n)) for y in range(n))
    assert bool(gs)==(unique and supported)
    row['pointwise_equivalence_checks']+=1
    assert len(gs)<=1
    for g in gs:assert root(r,g)
   if local:
    for a,b in r:assert sources[a]==sources[b]
    for c in cs:assert len({sources[x][0] for x in c})==1
   if least:
    assert len(least)==1
    if r:assert any((least[0],x) in r for x in range(n))
   row['connected']+=conn;row['locally_complete']+=local;row['local_and_connected']+=local and conn;row['least_ancestor']+=bool(least);row['unique_root_cones']+=uniques
  census.append(row)
 merge={(0,2),(1,2)};split={(0,1),(2,3)}
 assert strict(merge) and len(components(3,merge))==1
 assert root(merge,0) and root(merge,1) and not any(cover(3,merge,g,2) for g in range(3))
 assert strict(split) and all(any(cover(4,split,g,x) for g in range(4)) for x in range(4))
 assert len(components(4,split))==2 and not any(all(below(split,g,x) for x in range(4)) for g in range(4))
 assert cover(1,set(),0,0) and not any((0,x) in set() for x in range(1))
 return {'status':'PASS_CONNECTED_FINITE_EQUIVALENCES','census':census,'controls':{'connected_merge_has_two_roots_but_no_local_completion_at_effect':True,'disconnected_components_locally_complete_without_common_root':True,'reflexive_coverage_has_no_productive_witness':True},'scope':'Logical implication and equivalence tests; assigning productive labels is not a metaphysical possibility proof; separately implemented by the author'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
