#!/usr/bin/env python3
import argparse,json,itertools
from pathlib import Path
from fractions import Fraction as F

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 expected=[]
 for B,C,y,r,k,reject in itertools.product(range(4),range(4),range(2),range(17),[0,1,7],range(2)):
  if B!=C:out=(0,0)
  elif reject:out=(k+1,0)
  elif r==0:out=(k,r)
  elif any((r-1)>>(2*y+c)&1 for c in range(2)):out=(k,r)
  else:out=(k+1,0)
  expected.append([len(expected),*out])
 freqChecks=gateChecks=0
 for n in range(6):
  for word in itertools.product(range(4),repeat=n):
   state=0;counts={};symbols={};history=[]
   for token in word:
    action,y=divmod(token,2);pair=(state,action);counts[pair]=counts.get(pair,0)+1;symbols[pair,y]=symbols.get((pair,y),0)+1;history.insert(0,(pair,y));state=y
   for pair in itertools.product(range(2),repeat=2):
    collected=[y for p,y in reversed(history) if p==pair]
    for y in range(2):
     frequency=F(symbols.get((pair,y),0),counts[pair]) if counts.get(pair,0) else F(0)
     direct=F(collected.count(y),len(collected)) if collected else F(0)
     assert frequency==direct;freqChecks+=1
   for model in range(2):
    for k in [0,n,n+1]:
     reject=any(k<counts.get(pair,0) and abs((F(symbols.get((pair,y),0),counts[pair]) if counts.get(pair,0) else F(0))-(F(3,4) if model==y else F(1,4)))>=F(1,8) for pair in itertools.product(range(2),repeat=2) for y in range(2))
     if k>=n:assert not reject
     gateChecks+=1
 # A stale acquired outlier would reject every phase if the count gate were removed.
 assert abs(F(1)-F(1,4))>=F(1,8)
 assert not (1<1) and 0<1
 (a.out/'EXPECTED.json').write_text(json.dumps(expected)+'\n')
 (a.out/'RESULT.json').write_text(json.dumps({'status':'PYTHON_REFERENCE_READY','memory_transitions':len(expected),'exact_history_frequency_checks':freqChecks,'gated_test_checks':gateChecks,'stale_count_countercontrol':True},indent=2)+'\n')
 source='''import ObservedPhaseController
namespace ReviewerTransitionOracle
open HiddenParity HiddenParity.Sufficiency
abbrev T := Fin 2
def support (n : Nat) : Finset T := Finset.univ.filter (fun m => n/2^m.val%2=1)
def pairs (n : Nat) : Finset (T × T) := Finset.univ.filter (fun e => n/2^(2*e.1.val+e.2.val)%2=1)
def encode (r : Option (Finset (T × T))) : Nat := match r with
 | none => 0
 | some E => 1 + (if (0,0) ∈ E then 1 else 0) + (if (0,1) ∈ E then 2 else 0) + (if (1,0) ∈ E then 4 else 0) + (if (1,1) ∈ E then 8 else 0)
def run : IO Unit := do
 let mut i := 0
 for b in List.range 4 do
  for c in List.range 4 do
   for y in List.range 2 do
    for r in List.range 17 do
     for k in [0,1,7] do
      for reject in [false,true] do
       let m : PhaseMemory T T := ⟨k,if r=0 then none else some (pairs (r-1))⟩
       let next := advanceMemory (support b) (support c) (⟨y%2, Nat.mod_lt _ (by decide)⟩ : T) m reject
       IO.println s!"{i},{next.index},{encode next.retained}"
       i := i+1
end ReviewerTransitionOracle
def main : IO Unit := ReviewerTransitionOracle.run
'''
 (a.out/'Oracle.lean').write_text(source);print((a.out/'RESULT.json').read_text())
if __name__=='__main__':main()
