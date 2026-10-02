import StableSupportParityNecessity
import ParityTailInvariance

namespace HiddenParity.Adaptive.Controls
open Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

abbrev Two := Fin 2

def alternatingPolicy (_ : Unit) (h : History Two Two) : Two :=
  if h.length % 2 = 0 then 0 else 1

def alternatingTape (an : Two × ℕ) : Two :=
  if an.1 = 0 then if an.2 % 2 = 0 then 0 else 1 else 0

def input : Unit × FlatStack Two Two := ((), alternatingTape)

theorem action_formula (n : ℕ) :
    stackActionTrajectory alternatingPolicy input n = if n % 2 = 0 then 0 else 1 := by
  simp [stackActionTrajectory, alternatingPolicy, stackHistoryTrajectory, observedHistory_length]

theorem action_zero_recurs : ∃ᶠ n in atTop, stackActionTrajectory alternatingPolicy input n = 0 := by
  apply frequently_atTop.mpr
  intro N
  exact ⟨2*N, by omega, by simp [action_formula, Nat.mul_mod]⟩

theorem tape_one_recurs : ∃ᶠ k in atTop, input.2 (0,k) = 1 := by
  apply frequently_atTop.mpr
  intro N
  exact ⟨2*N+1, by omega, by simp [input, alternatingTape, Nat.add_mod, Nat.mul_mod]⟩

/-- Adaptive gaps do not skip the raw tape's intervening sample indices. -/
theorem gaps_still_observe_one :
    ∃ᶠ n in atTop, stackActionTrajectory alternatingPolicy input n = 0 ∧
      stackReceipt alternatingPolicy input n = 1 :=
  recurrent_action_observes_recurrent_symbol alternatingPolicy input 0 1 action_zero_recurs tape_one_recurs

theorem third_step_uses_second_pair_sample : countBefore alternatingPolicy input 0 2 = 1 := by decide

theorem actual_third_step_receipt : stackReceipt alternatingPolicy input 2 = 1 := by decide

/-- Indexing by physical time instead would incorrectly skip the positive symbols. -/
theorem physical_time_index_is_different : input.2 (0,2) = 0 := by decide

theorem selected_sample_counter_cannot_be_replaced_by_clock :
    stackReceipt alternatingPolicy input 2 ≠ input.2 (0,2) := by decide

/-- Source-state transition support cannot be omitted from recurrent graph extraction. -/
def selfSuccessor (e : Two) : Finset Two := {e}
def alternatingPath (n : ℕ) : Two := if n % 2 = 0 then 0 else 1

theorem unsupported_physical_step_rejected : alternatingPath 1 ∉ selfSuccessor (alternatingPath 0) := by decide

theorem self_loop_union_is_not_strong :
    ¬ IsEndComponent id selfSuccessor (Finset.univ : Finset Two) := by decide

end HiddenParity.Adaptive.Controls
