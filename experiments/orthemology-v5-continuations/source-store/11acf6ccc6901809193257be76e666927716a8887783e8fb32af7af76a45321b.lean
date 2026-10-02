import GlobalParityNecessity

namespace HiddenParity.Necessity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

abbrev S := Fin 2
abbrev A := Fin 1
abbrev M := Fin 2

/-- Candidate 0 reveals itself by moving to 1; candidate 1 stays at 0.
At state 1 both models remain at 1. -/
def branchKernel : RationalKernel M (S × A) S where
  row := fun m e y => if y = (if e.1 = 0 ∧ m = 1 then 0 else 1) then 1 else 0
  nonnegative := by intros; split <;> split <;> norm_num
  normalized := by intro m e; fin_cases m <;> rcases e with ⟨s,a⟩ <;>
    fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two]

def allMenu (_ : Finset M) (_ : S) : Finset A := Finset.univ

def branchPriority (m : M) (e : S × A) : ℕ := if m = 1 ∧ e.1 = 0 then 1 else 2

/-- Favorable revealing branches do not excuse a losing alternative child. -/
theorem losing_child_rejects_parent :
    winningRegion branchKernel allMenu branchPriority Finset.univ = ({1} : Finset S) := by decide

theorem revealed_even_child_wins :
    winningRegion branchKernel allMenu branchPriority ({0} : Finset M) = Finset.univ := by decide

theorem revealed_odd_child_loses :
    winningRegion branchKernel allMenu branchPriority ({1} : Finset M) = ({1} : Finset S) := by decide

def deadMenu (_ : Finset M) (s : S) : Finset A := if s = 0 then Finset.univ else ∅

theorem dead_successor_rejected :
    winningRegion branchKernel deadMenu (fun _ _ => 2) Finset.univ = ∅ := by decide

theorem empty_support_rejected :
    winningRegion branchKernel allMenu branchPriority ∅ = ∅ := by decide

/-- A deterministic two-cycle checks the minimum-recurrent-priority convention. -/
def cycleKernel : RationalKernel (Fin 1) (S × A) S where
  row := fun _ e y => if y = (if e.1 = 0 then 1 else 0) then 1 else 0
  nonnegative := by intros; split <;> split <;> norm_num
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;>
    norm_num [Fin.sum_univ_two]

def cycleMenu (_ : Finset (Fin 1)) (_ : S) : Finset A := Finset.univ

def cyclePriority (odd : ℕ) (_ : Fin 1) (e : S × A) : ℕ := if e.1 = 0 then 2 else odd

theorem higher_odd_recurs_and_wins :
    winningRegion cycleKernel cycleMenu (cyclePriority 3) Finset.univ = Finset.univ := by decide

theorem lower_odd_recurs_and_loses :
    winningRegion cycleKernel cycleMenu (cyclePriority 1) Finset.univ = ∅ := by decide

theorem excess_fuel_same_output :
    computedRegion branchKernel allMenu branchPriority 4 Finset.univ =
      winningRegion branchKernel allMenu branchPriority Finset.univ := by decide

/-- Concrete negative output rules out arbitrary common seed/history policies. -/
theorem no_common_policy_at_bad_branch {R : Type*} [MeasurableSpace R] :
    ¬ SemanticWinning (R := R) branchKernel allMenu branchPriority (0,0) Finset.univ 0 := by
  apply computed_losing_excludes_common_policy
  rw [losing_child_rejects_parent]
  decide

end HiddenParity.Necessity.Controls
