#!/usr/bin/env python3
"""Finite cross-check of strict ancestry coverage and modal transport.

Countably infinite controls are proved in Lean, not approximated here.
This checker is separately implemented by the author, not independently authored.
"""
import itertools,json

def relation(n,mask):return {(a,b) for a in range(n) for b in range(n) if mask & (1<<(a*n+b))}
def irr(r):return all(a!=b for a,b in r)
def trans(r):return all((a,c) in r for a,b in r for bb,c in r if b==bb)
def coverage(r,g,x):return (g,x) in r and all(y==g or (g,y) in r for y,xx in r if xx==x)
def received(r,g):return any(x==g for _,x in r)
def root(r,g):return not received(r,g)

def main():
 census=[];checked=0
 for n in range(1,5):
  strict=0;instances=0
  for m in range(1<<(n*n)):
   r=relation(n,m)
   if not irr(r) or not trans(r):continue
   strict+=1
   for g,x in itertools.product(range(n),repeat=2):
    if coverage(r,g,x):
     assert root(r,g)
     instances+=1
  checked+=instances;census.append({'domain_size':n,'relations_enumerated':1<<(n*n),'strict_transitive_relations':strict,'coverage_instances':instances})
 modal=0;applicable=0
 n=2
 for em in range(1<<(2*n)):
  ex=lambda w,x:bool(em&(1<<(w*n+x)))
  for ma,mb in itertools.product(range(1<<(n*n)),repeat=2):
   rs=[relation(n,ma),relation(n,mb)];modal+=1
   if any(not ex(w,y) or not ex(w,x) for w in range(2) for y,x in rs[w]):continue
   if not irr(rs[0]) or not trans(rs[0]):continue
   necessary=lambda x:all(ex(w,x) for w in range(2))
   cr=all(not(ex(0,x) and not necessary(x)) or received(rs[0],x) for x in range(n))
   er=all(not any(received(r,x) for r in rs) or all(not ex(w,x) or received(rs[w],x) for w in range(2)) for x in range(n))
   if not cr or not er:continue
   for g,x in itertools.product(range(n),repeat=2):
    if ex(0,g) and coverage(rs[0],g,x):
     assert all(ex(w,g) and root(rs[w],g) for w in range(2));applicable+=1
 # Deleting either strictness assumption defeats the independence inference.
 r={(0,0),(0,1)}
 assert trans(r) and coverage(r,0,1) and received(r,0)
 r={(0,2),(1,0),(1,2),(0,1)}
 assert irr(r) and coverage(r,0,2) and received(r,0) and not trans(r)
 # Two sources actually supply two separate effects. Neither covers both.
 r={(0,1),(2,3)}
 assert coverage(r,0,1) and coverage(r,2,3)
 assert not any((g,1) in r and (g,3) in r for g in range(4))
 return {'status':'PASS_FINITE_UPSTREAM_SCOPE','coverage_census':census,'verified_coverage_instances':checked,'modal_structures_enumerated':modal,'modal_coverage_instances':applicable,'deletion_controls':{'without_irreflexivity':'counterinterpretation_verified','without_transitivity':'counterinterpretation_verified'},'split_source_control':'verified','scope':'Finite implication cross-check only; no metaphysical possibility certification; infinite cases are Lean theorems'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
