import SCCRegionAlgorithm

/- A finite native control, not a kernel proof or general complexity bound.
The 64-pair allowed set would have 2^64 subsets under the old MEC enumeration. -/
namespace HiddenParity.SCCRegion.ScaleExecution
abbrev S := Fin 1
abbrev A := Fin 64
abbrev M := Fin 1

def kernel : RationalKernel M (S × A) S where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp

def menu (_ : Finset M) (_ : S) : Finset A := Finset.univ
def priority (_ : M) (e : S × A) : Nat := if e.2.val < 32 then 1 else 2

def output : Finset S := winningRegion kernel menu priority Finset.univ
end HiddenParity.SCCRegion.ScaleExecution

def main : IO Unit := do
  let result := HiddenParity.SCCRegion.ScaleExecution.output
  IO.println s!"{result.card},{decide ((0 : Fin 1) ∈ result)}"
