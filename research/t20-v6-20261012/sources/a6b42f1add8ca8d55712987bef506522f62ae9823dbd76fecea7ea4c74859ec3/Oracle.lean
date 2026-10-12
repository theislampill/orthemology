import ObservedPhaseController
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
