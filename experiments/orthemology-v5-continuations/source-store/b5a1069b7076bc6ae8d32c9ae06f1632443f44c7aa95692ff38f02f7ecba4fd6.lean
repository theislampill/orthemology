import RegionControls
import SCCRegionAlgorithm

namespace HiddenParity.SCCRegion.Controls
open HiddenParity.Necessity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

theorem losing_child_rejects_parent :
    HiddenParity.SCCRegion.winningRegion branchKernel allMenu branchPriority Finset.univ =
      ({1} : Finset S) := by decide

theorem revealed_even_child_wins :
    HiddenParity.SCCRegion.winningRegion branchKernel allMenu branchPriority ({0} : Finset M) =
      Finset.univ := by decide

theorem revealed_odd_child_loses :
    HiddenParity.SCCRegion.winningRegion branchKernel allMenu branchPriority ({1} : Finset M) =
      ({1} : Finset S) := by decide

theorem dead_successor_rejected :
    HiddenParity.SCCRegion.winningRegion branchKernel deadMenu (fun _ _ => 2) Finset.univ = ∅ := by decide

theorem empty_support_rejected :
    HiddenParity.SCCRegion.winningRegion branchKernel allMenu branchPriority ∅ = ∅ := by decide

theorem higher_odd_recurs_and_wins :
    HiddenParity.SCCRegion.winningRegion cycleKernel cycleMenu (cyclePriority 3) Finset.univ =
      Finset.univ := by decide

theorem lower_odd_recurs_and_loses :
    HiddenParity.SCCRegion.winningRegion cycleKernel cycleMenu (cyclePriority 1) Finset.univ = ∅ := by decide

theorem excess_fuel_same_output :
    HiddenParity.SCCRegion.computedRegion branchKernel allMenu branchPriority 4 Finset.univ =
      HiddenParity.SCCRegion.winningRegion branchKernel allMenu branchPriority Finset.univ := by decide

theorem no_common_policy_at_bad_branch {R : Type*} [MeasurableSpace R] :
    ¬ HiddenParity.Necessity.SemanticWinning (R := R) branchKernel allMenu branchPriority
      (0,0) Finset.univ 0 := by
  apply HiddenParity.SCCRegion.computed_losing_excludes_common_policy
  rw [losing_child_rejects_parent]
  decide
end HiddenParity.SCCRegion.Controls

namespace HiddenParity.SCCRegion.ExtraControls
abbrev S := Fin 1
abbrev A := Fin 2
abbrev M := Fin 2

def kernel : RationalKernel M (S × A) S where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp

def menu (_ : Finset M) (_ : S) : Finset A := Finset.univ

def opposite (m : M) (e : S × A) : Nat := if m=e.2 then 1 else 2

def sharedEven (_m : M) (e : S × A) : Nat := if e.2=0 then 1 else 2

/-- Merely choosing the favorable candidate cannot ignore a matching rival. -/
theorem incompatible_rival_minima_reject :
    winningRegion kernel menu opposite Finset.univ = (∅ : Finset S) := by decide

/-- An odd action may be pruned while the common even action remains viable. -/
theorem shared_even_action_retained :
    winningRegion kernel menu sharedEven Finset.univ = (Finset.univ : Finset S) := by decide

/-- The actual stage call, not just the public recursion, uses the same selector. -/
theorem stage_prunes_odd_but_keeps_even :
    regionStep kernel menu sharedEven Finset.univ (fun _ => ∅) Finset.univ =
      (Finset.univ : Finset S) := by decide
end HiddenParity.SCCRegion.ExtraControls
