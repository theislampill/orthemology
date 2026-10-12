#!/usr/bin/env python3
"""Independent normalized-table adapter check; zero and positive support exact."""
from pathlib import Path
import argparse,json,random
from oracle import encode,digits,expected

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 rng=random.Random(202610011551);cases=[];answers=[]
 supports=[1,2,3]
 for i in range(512):
  rc=rng.randrange(3**12);pc=rng.randrange(6**12);theta=i%3;b=7 if i<384 else rng.randrange(8);u=15 if i<384 else rng.randrange(16)
  ids=digits(rc,3,12);graph=[];zero=u
  for e in range(4):
   common=3
   for m in range(3):
    if b>>m&1:common &= supports[ids[m*4+e]]
   graph.append(common)
   if supports[ids[theta*4+e]] & ~common:zero &= ~(1<<e)
  _,target=expected((encode(graph,4),encode(ids,4),pc,b,theta,zero))
  cases.append((rc,pc,b,theta,u));answers.append(target)
 payload={'cases':cases,'expected_targets':answers}
 (args.output/'CASES.json').write_text(json.dumps(payload,separators=(',',':'))+'\n')
 s='''import MarkovSupportAdapter
namespace HiddenParity.NormalizedOracle
set_option maxRecDepth 100000
set_option maxHeartbeats 0
abbrev S := Fin 2
abbrev A := Fin 4
abbrev M := Fin 3
structure Case where
  rows : Nat
  priority : Nat
  live : Nat
  candidate : Nat
  allowed : Nat

def half : ℚ := ⟨1, 2, by decide, by decide⟩
theorem half_eq : half = (1 / 2 : ℚ) := by
  simpa [half] using (Rat.num_div_den half).symm
def digit (n b i : Nat) : Nat := (n / b^i) % b
def src (e : A) : S := ⟨e.val / 2, by omega⟩
def rowFor (c : Nat) (y : S) : ℚ :=
  if c % 3 = 0 then if y = 0 then 1 else 0
  else if c % 3 = 1 then if y = 1 then 1 else 0 else half

def kernel (c : Case) : RationalKernel M A S where
  row := fun m e y => rowFor (digit c.rows 3 (m.val*4+e.val)) y
  nonnegative := by
    intro m e y
    unfold rowFor
    split_ifs <;> norm_num [half_eq] at *
  normalized := by
    intro m e
    simp only [Fin.sum_univ_two, rowFor]
    split_ifs <;> norm_num [half_eq] at *

def pri (c : Case) (m : M) (e : A) : Nat := digit c.priority 6 (m.val*4+e.val)
def live (c : Case) : Finset M := Finset.univ.filter (fun m => digit c.live 2 m.val = 1)
def allowed (c : Case) : Finset A := Finset.univ.filter (fun e => digit c.allowed 2 e.val = 1)
def solve (c : Case) : Nat :=
  (markovTargetStates (kernel c) src (live c) (pri c)
    ⟨c.candidate % 3, Nat.mod_lt _ (by decide)⟩ (allowed c)).sum (fun s => 2^s.val)
def cases : List Case := [
'''
 s+=',\n'.join('  ⟨'+', '.join(map(str,c))+'⟩' for c in cases)+'\n]\nend HiddenParity.NormalizedOracle\ndef main : IO Unit := do\n  for (c,i) in HiddenParity.NormalizedOracle.cases.zipIdx do\n    IO.println s!"{i},{HiddenParity.NormalizedOracle.solve c}"\n'
 (args.output/'NormalizedOracle.lean').write_text(s)
 print(json.dumps({'cases':len(cases),'normalized_row_types':['delta0','delta1','half-half'],'scope':'exact normalized table adapter to independently enumerated maximal valid components'}))
if __name__=='__main__':main()
