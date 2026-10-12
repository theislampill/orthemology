#!/usr/bin/env python3
"""Independent exhaustive-component, bottom-up fixed point oracle.
No pruning/MEC routine from the candidate is imported. Standard library only.
"""
import argparse,json,random,itertools,hashlib
from fractions import Fraction as F
from pathlib import Path

def subsets(xs):
 xs=list(xs)
 return [set(xs[i] for i in range(len(xs)) if mask>>i&1) for mask in range(1<<len(xs))]
def reach(edges,s):
 out={s}
 while True:
  new=out|{t for u,t in edges if u in out}
  if new==out:return out
  out=new

def solve(table,menus,prio):
 P={(m,s,a):(table[m*4+s*2+a],1-table[m*4+s*2+a]) for m in range(2) for s in range(2) for a in range(2)}
 lower={frozenset():set()};details=[]
 for B in [frozenset([0]),frozenset([1]),frozenset([0,1])]:
  W={0,1};rounds=0
  while True:
   def child(e,y):return frozenset(m for m in B if P[m,*e][y]>0)
   allowed={e for e in itertools.product(range(2),repeat=2) if e[0] in W and e[1] in menus[sum(1<<m for m in B),e[0]] and all(not(C:=child(e,y)) or y in (W if C==B else lower[C]) for y in range(2))}
   internal={e:{y for y in range(2) if child(e,y)==B} for e in allowed}
   edges={(s,y) for s,a in allowed for y in internal[s,a]}
   targets={m:set() for m in B};exits={m:set() for m in B}
   for m in B:
    exits[m]={s for s,a in allowed if any(P[m,s,a][y]>0 and child((s,a),y)!=B for y in range(2))}
    for C in subsets(allowed):
     if not C:continue
     states={e[0] for e in C};ce={(e[0],y) for e in C for y in internal[e]}
     if any(not internal[e] or not internal[e]<=states for e in C):continue
     if any(not states<=reach(ce,s) for s in states):continue
     if any(any(P[m,*e][y]>0 and y not in internal[e] for y in range(2)) for e in C):continue
     matches=[r for r in B if all(P[r,*e]==P[m,*e] for e in C)]
     if all(min(prio[r*4+e[0]*2+e[1]] for e in C)%2==0 for r in matches):targets[m]|=states
   V={s for s in W if all(reach(edges,s)&(exits[m]|targets[m]) for m in B)}
   rounds+=1
   if V==W:break
   W=V
  lower[B]=W;details.append({'support':sorted(B),'states':sorted(W),'rounds':rounds})
 return lower,details

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 rng=random.Random(50301);probs=[F(0),F(1,3),F(1,2),F(2,3),F(1)];cases=[]
 # Exact probabilities, varied full rows and dynamic menus; include all deterministic rows.
 tables=list(itertools.product([0,4],repeat=8))+[tuple(rng.randrange(5) for _ in range(8)) for _ in range(256)]
 for i,tab in enumerate(tables):
  menuCode=rng.randrange(1<<12);pr=[rng.randrange(6) for _ in range(8)]
  menus={(B,s):{a for a in range(2) if menuCode>>(4*(B-1)+2*s+a)&1} for B in [1,2,3] for s in range(2)}
  result,details=solve([probs[x] for x in tab],menus,pr)
  cases.append({'table':sum(v*5**j for j,v in enumerate(tab)),'menu':menuCode,'priority':sum(v*6**j for j,v in enumerate(pr)),'expected':[sum(1<<s for s in result[B]) for B in [frozenset(),frozenset([0]),frozenset([1]),frozenset([0,1])]],'details':details})
 (a.out/'CASES.json').write_text(json.dumps(cases,indent=2)+'\n')
 source='''import RegionControls
namespace IndependentRegionOracle
open HiddenParity HiddenParity.Necessity
abbrev T := Fin 2
set_option maxRecDepth 100000
set_option maxHeartbeats 0
def probability (n : Nat) : ℚ := if n=0 then 0 else if n=1 then 1/3 else if n=2 then 1/2 else if n=3 then 2/3 else 1
theorem probability_bounds (n : Nat) : 0 ≤ probability n ∧ probability n ≤ 1 := by
 unfold probability; split_ifs <;> norm_num
def kernel (code : Nat) : RationalKernel T (T × T) T where
 row := fun m e y => if y=0 then probability ((code / 5^(m.val*4+e.1.val*2+e.2.val)) % 5) else 1-probability ((code / 5^(m.val*4+e.1.val*2+e.2.val)) % 5)
 nonnegative := by intro m e y; split <;> linarith [(probability_bounds ((code / 5^(m.val*4+e.1.val*2+e.2.val)) % 5)).1,(probability_bounds ((code / 5^(m.val*4+e.1.val*2+e.2.val)) % 5)).2]
 normalized := by intro m e; simp [Fin.sum_univ_two]
def mask (B : Finset T) : Nat := (if (0:T) ∈ B then 1 else 0)+(if (1:T) ∈ B then 2 else 0)
def menu (code : Nat) (B : Finset T) (s : T) : Finset T := Finset.univ.filter (fun a => (code / 2^(4*(mask B-1)+2*s.val+a.val))%2=1)
def priority (code : Nat) (m : T) (e : T × T) : Nat := (code / 6^(m.val*4+e.1.val*2+e.2.val))%6
def support (n : Nat) : Finset T := Finset.univ.filter (fun m => n/2^m.val%2=1)
def cases : List (Nat × Nat × Nat) := [
'''+',\n'.join(f"({c['table']},{c['menu']},{c['priority']})" for c in cases)+''']
def run : IO Unit := do
 for (i,(t,m,p)) in cases.zipIdx.map (fun (x,i) => (i,x)) do
  let out := (List.range 4).map (fun b => mask (winningRegion (kernel t) (menu m) (priority p) (support b)))
  IO.println s!"{i},{out[0]!},{out[1]!},{out[2]!},{out[3]!}"
end IndependentRegionOracle
def main : IO Unit := IndependentRegionOracle.run
'''
 (a.out/'Oracle.lean').write_text(source)
 print(json.dumps({'cases':len(cases),'support_comparisons':len(cases)*4,'kind':'independent exhaustive qualifying-component enumeration and bottom-up fixed point'}))
if __name__=='__main__':main()
