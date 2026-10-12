#!/usr/bin/env python3
"""Independent counterexample search against deliberate semantic shortcuts.
Each baseline is checked against direct valid-component enumeration first.
"""
import argparse,itertools,json,random
from pathlib import Path

def powerset(U):
 U=sorted(U)
 return [frozenset(U[i] for i in range(len(U)) if n>>i&1) for n in range(1<<len(U))]
def component(E,source,succ,mode='normal'):
 if not E:return False
 states={source[e] for e in E}
 if mode!='allow_empty_successors' and any(not succ[e] for e in E):return False
 if mode!='drop_closure' and any(not succ[e]<=states for e in E):return False
 if mode=='drop_connectivity':return True
 R={(s,s) for s in states}|{(source[e],t) for e in E for t in succ[e]}
 for k in sorted(states):
  for s in sorted(states):
   for t in sorted(states):
    if (s,k) in R and (k,t) in R:R.add((s,t))
 return all((s,t) in R for s in states for t in states)
def matches(E,row,theta,m):return all(row[m][e]==row[theta][e] for e in E)
def exact(source,succ,row,pri,B,theta,U):
 valid=[E for E in powerset(U) if component(E,source,succ) and
        all(min(pri[m][e] for e in E)%2==0 for m in B if matches(E,row,theta,m))]
 return {E for E in valid if not any(E<D for D in valid)}
def prune(source,succ,row,pri,B,theta,U,mode='normal'):
 current=frozenset(U);initial=current;fuel=len(U)
 if mode=='one_round':fuel=1
 if mode=='one_fewer_round':fuel=max(0,fuel-1)
 def mecs(V):
  cs=[E for E in powerset(V) if component(E,source,succ,mode)]
  return [E for E in cs if not any(E<D for D in cs)]
 for _ in range(fuel):
  comps=mecs(current);keep=set(current) if mode=='keep_noncomponent_pairs' else set().union(*comps) if comps else set()
  for D in comps:
   for m in ([theta] if mode=='candidate_only' else B):
    test=initial if mode=='freeze_matching' else D
    if mode!='ignore_matching' and not matches(test,row,theta,m):continue
    d=min(pri[m][e] for e in D)
    if mode=='delete_all_odd':keep.difference_update(e for e in D if pri[m][e]%2)
    elif d%2:keep.difference_update(e for e in D if pri[m][e]==d)
  current=frozenset(keep)
 return set(mecs(current))
def serial(x):
 if isinstance(x,(set,frozenset)):return sorted(serial(i) for i in x)
 if isinstance(x,(tuple,list)):return [serial(i) for i in x]
 return x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path);args=ap.parse_args()
 cases=[]
 # Core cascading, rematching, higher odd, and source-closure fixtures.
 def add(src,succ,row,pri,B=(0,1),theta=0,U=None):
  cases.append((src,list(map(set,succ)),row,pri,list(B),theta,set(range(len(src))) if U is None else set(U)))
 add([0,0,0],[{0}]*3,[[0]*3]*2,[[2]*3,[1,3,4]])
 add([0,0,0],[{0}]*3,[[0,0,0],[0,0,0],[1,0,0]],[[2,2,2],[1,4,4],[4,1,4]],(0,1,2))
 add([0,1],[{1},{0}],[[0,0]],[[2,3]],(0,))
 add([0,0,0],[{0}]*3,[[0]*3]*2,[[1,3,5]]*2)
 add([0],[set()],[[0]],[[2]],(0,))
 add([0],[{1}],[[0]],[[2]],(0,))
 add([0,1],[{0},{1}],[[0,0]],[[2,4]],(0,))
 add([0],[{0}],[[0],[1]],[[2],[1]])
 add([0],[{0}],[[0],[0]],[[2],[1]])
 rng=random.Random(202610011541)
 for _ in range(1500):
  n=4;src=[0,0,1,1];succ=[{s for s in range(2) if rng.randrange(2)} for _ in range(n)]
  row=[[rng.randrange(2) for _ in range(n)] for _ in range(3)]
  pri=[[rng.randrange(6) for _ in range(n)] for _ in range(3)]
  add(src,succ,row,pri,(0,1,2),rng.randrange(3))
 modes=['delete_all_odd','candidate_only','ignore_matching','freeze_matching','one_round','one_fewer_round','allow_empty_successors','drop_closure','drop_connectivity']
 witnesses={}
 for i,c in enumerate(cases):
  ex=exact(*c);assert prune(*c)==ex,(i,c)
  for mode in modes:
   if mode not in witnesses:
    wrong=prune(*c,mode)
    if wrong!=ex:witnesses[mode]={'case':i,'input':serial(c),'expected':serial(ex),'mutant':serial(wrong)}
 assert set(witnesses)==set(modes),set(modes)-set(witnesses)
 result={'status':'PASS_ALL_ALTERNATIVES_REFUTED','baseline_cases':len(cases),'mutants_rejected':len(witnesses),'witnesses':witnesses,
 'scope':'finite semantic countercontrols; no unbounded theorem inferred'}
 dest=args.out if args.out else Path(__file__).resolve().parents[1]/'evidence'/'SEMANTIC_MUTANTS.json'
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='witnesses'}))
if __name__=='__main__':main()
