#!/usr/bin/env python3
from itertools import product
import json
from pathlib import Path

def parts(n):
    out=[]
    def rec(a,m):
        if len(a)==n:out.append(tuple(a));return
        for x in range(m+2):rec(a+[x],max(m,x))
    rec([0],0);return out

def canon(v):
    d={};o=[]
    for x in v:
        if x not in d:d[x]=len(d)
        o.append(d[x])
    return tuple(o)
def joint(*ps):return canon(zip(*ps))
def refines(p,q):return all(p[i]!=p[j] or q[i]==q[j] for i in range(len(p)) for j in range(len(p)))
def sufficient(E,r,Q):return refines(joint(E,r),Q)
def weak(E,r,s):return refines(joint(E,s),joint(E,r))

def main():
    P=parts(4); cases=0; fail=[]; post=[]; floor=[]; nonunique=0; empty=0
    for E,Q in product(P,repeat=2):
        D=[r for r in P if sufficient(E,r,Q)]
        mins=[r for r in D if not any(s!=r and weak(E,s,r) and not weak(E,r,s) for s in D)]
        if not D:empty+=1
        if len(mins)>1:nonunique+=1
        pi=joint(E,Q)
        for r in P:
            cases+=1
            direct=all(joint(E,r)[i]!=joint(E,r)[j] or Q[i]==Q[j] for i in range(4) for j in range(4))
            if direct!=sufficient(E,r,Q):fail.append((E,Q,r))
            if sufficient(E,r,Q) and not refines(joint(E,r),pi):floor.append((E,Q,r))
            if refines(E,r) and not refines(E,Q) and sufficient(E,r,Q):post.append((E,Q,r))
    E=(0,0,0);Q=(0,1,2);bearer=(0,0,1);uptake=(0,1,1);const=(0,0,0)
    ui={
      'constant':sufficient(E,const,Q),
      'bearer':sufficient(E,bearer,Q),
      'uptake':sufficient(E,uptake,Q),
      'bearer_plus_uptake':sufficient(E,joint(bearer,uptake),Q),
      'target_oracle':sufficient(E,Q,Q)}
    result={'partitions_n4':len(P),'cases':cases,'criterion_failures':len(fail),
      'coarsest_floor_failures':len(floor),'postprocessing_barrier_failures':len(post),
      'nonunique_minimum_cases':nonunique,'empty_discriminator_cases':empty,'ui':ui,
      'overall':'PASS' if not fail and not floor and not post and nonunique>0 and ui=={
       'constant':False,'bearer':False,'uptake':False,'bearer_plus_uptake':True,'target_oracle':True} else 'FAIL'}
    out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
