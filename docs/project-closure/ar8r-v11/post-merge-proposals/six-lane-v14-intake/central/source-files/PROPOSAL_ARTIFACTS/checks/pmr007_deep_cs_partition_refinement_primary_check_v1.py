#!/usr/bin/env python3
from itertools import product
import json
from pathlib import Path

# Restricted growth strings enumerate set partitions.
def partitions(n):
    out=[]
    def rec(a,m):
        if len(a)==n:
            out.append(tuple(a)); return
        for x in range(m+2):
            rec(a+[x],max(m,x))
    rec([0],0)
    return out

def canon(values):
    d={}; nxt=0; out=[]
    for v in values:
        if v not in d: d[v]=nxt; nxt+=1
        out.append(d[v])
    return tuple(out)

def joint(*ps):
    return canon(list(zip(*ps)))

def refines(p,q):
    # p finer than q: equal p labels imply equal q labels
    return all(p[i]!=p[j] or q[i]==q[j] for i in range(len(p)) for j in range(len(p)))

def sufficient(E,r,Q): return refines(joint(E,r),Q)
def weaker(E,r,s): return refines(joint(E,s),joint(E,r))

def main():
    ps=partitions(4)
    theorem_cases=0; criterion_failures=[]; post_failures=[]
    nonunique=0
    for E,Q in product(ps,repeat=2):
        conflicts=not refines(E,Q)
        D=[r for r in ps if sufficient(E,r,Q)]
        mins=[r for r in D if not any(s!=r and weaker(E,s,r) and not weaker(E,r,s) for s in D)]
        nonunique += int(len(mins)>1)
        for r in ps:
            theorem_cases+=1
            # exact fibre criterion checked directly
            direct=all(joint(E,r)[i]!=joint(E,r)[j] or Q[i]==Q[j]
                       for i in range(4) for j in range(4))
            if direct!=sufficient(E,r,Q):criterion_failures.append((E,Q,r))
            if conflicts and refines(E,r): # r is postprocessing/coarsening of E
                if sufficient(E,r,Q): post_failures.append((E,Q,r))
    # Explicit U/I/P registry
    E=(0,0,0); Q=(0,1,2)
    bearer=(0,0,1); uptake=(0,1,1); oracle=Q; constant=(0,0,0)
    ui={
      'neutral_sufficient':sufficient(E,constant,Q),
      'bearer_sufficient':sufficient(E,bearer,Q),
      'uptake_sufficient':sufficient(E,uptake,Q),
      'joint_sufficient':sufficient(E,joint(bearer,uptake),Q),
      'oracle_sufficient':sufficient(E,oracle,Q),
    }
    result={
      'partitions_n4':len(ps),'theorem_cases':theorem_cases,
      'criterion_failures':len(criterion_failures),
      'postprocessing_split_failures':len(post_failures),
      'nonunique_minimal_cases':nonunique,'ui_registry':ui,
      'overall':'PASS' if not criterion_failures and not post_failures
        and nonunique>0 and ui=={
          'neutral_sufficient':False,'bearer_sufficient':False,
          'uptake_sufficient':False,'joint_sufficient':True,
          'oracle_sufficient':True} else 'FAIL'}
    out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
