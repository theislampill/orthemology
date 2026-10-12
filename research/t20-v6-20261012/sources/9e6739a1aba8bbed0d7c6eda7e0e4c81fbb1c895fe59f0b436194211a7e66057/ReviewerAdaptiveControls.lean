import StableSupportParityNecessity
import ParityTailInvariance

noncomputable section
namespace HiddenParity.IndependentAdaptive
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Adaptive HiddenParity.Stochastic
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
set_option linter.unusedSectionVars false
abbrev Two := Fin 2

section Count
universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [DecidableEq A] [Inhabited Y]

/-- Selected occurrences cannot reuse one raw tape cell. -/
theorem selected_count_strict (π : R → History A Y → A) (z : R × FlatStack A Y)
    (a : A) {n m : Nat} (hnm : n < m) (hn : stackActionTrajectory π z n = a) :
    countBefore π z a n < countBefore π z a m := by
  have hm := countBefore_mono π z a (show n+1 ≤ m by omega)
  rw [countBefore_succ, if_pos hn] at hm
  omega

theorem consumed_index_unique (π : R → History A Y → A) (z : R × FlatStack A Y)
    (a : A) {n m : Nat} (hn : stackActionTrajectory π z n = a)
    (hm : stackActionTrajectory π z m = a)
    (hc : countBefore π z a n = countBefore π z a m) : n = m := by
  rcases lt_trichotomy n m with h | h | h
  · have := selected_count_strict π z a h hn
    omega
  · exact h
  · have := selected_count_strict π z a h hm
    omega
end Count

-- Raw recurrence of an unused pair does not force it to be observed.
def onlyZero (_ : Unit) (_ : History Two Two) : Two := 0
def tapeByPair (an : Two × Nat) : Two := an.1
def unusedInput : Unit × FlatStack Two Two := ((), tapeByPair)

theorem always_zero_action (n : Nat) : stackActionTrajectory onlyZero unusedInput n = 0 := rfl

theorem always_zero_receipt (n : Nat) : stackReceipt onlyZero unusedInput n = 0 := by
  simp [stackReceipt, stackActionTrajectory, onlyZero, unusedInput, tapeByPair]

theorem unused_tape_one_recurs : ∃ᶠ k in atTop, unusedInput.2 (1,k) = 1 := by
  exact Frequently.of_forall (fun _ => rfl)

theorem unused_pair_not_recurrent : ¬ (∃ᶠ n in atTop, stackActionTrajectory onlyZero unusedInput n = 1) := by
  simp [always_zero_action]

-- The count index distinguishes state/action pairs even when the action is identical.
def unitPolicy (_ : Unit) (_ : History Unit Two) : Unit := ()
def stateTape (an : (Two × Unit) × Nat) : Two :=
  if an.1.1 = 0 then 1 else if an.2 % 2 = 0 then 0 else 1
def stateInput : Unit × FlatStack (Two × Unit) Two := ((), stateTape)

theorem same_action_new_state_uses_index_zero :
    countBefore (pairPolicy 0 unitPolicy) stateInput (1,()) 1 = 0 := by decide

theorem correct_second_receipt : stackReceipt (pairPolicy 0 unitPolicy) stateInput 1 = 0 := by decide

theorem action_only_counter_cell_differs : stateInput.2 ((1,()),1) = 1 := by decide

theorem source_consistency_at_second_step :
    (stackActionTrajectory (pairPolicy 0 unitPolicy) stateInput 2).1 =
      stackReceipt (pairPolicy 0 unitPolicy) stateInput 1 :=
  stack_pair_source_next 0 unitPolicy stateInput 1

theorem unrelated_readout_default_not_initial_state :
    historyAction (1,()) (stackHistoryTrajectory (pairPolicy 0 unitPolicy) stateInput) 0 = (0,()) := by
  rw [← stackActionTrajectory_eq_historyAction]
  rfl

-- Actual revealing source: winning under both models, but no initial-support target.
def revealRows (m : Two) (_ : Two × Two) (y : Two) : ℚ := if y = m then 1 else 0

def revealKernel : RationalKernel Two (Two × Two) Two where
  row := revealRows
  nonnegative := by intro m e y; unfold revealRows; split_ifs <;> norm_num
  normalized := by intro m e; fin_cases m <;> norm_num [revealRows, Fin.sum_univ_two]

def revealPriority (m : Two) (e : Two × Two) : Nat := if e.2 = m then 2 else 1

def revealPolicy (_ : Unit) : History Two Two → Two
  | [] => 0
  | (_,y) :: _ => y

def revealTape (m : Two) (_ : (Two × Two) × Nat) : Two := m

theorem reveal_internal_empty (e : Two × Two) :
    internalSuccessors revealKernel (Finset.univ : Finset Two) e = ∅ := by
  fin_cases e <;> decide

theorem reveal_no_zero_exit (m : Two) (e : Two × Two) :
    ¬ NoExit revealKernel (Finset.univ : Finset Two) m e := by
  fin_cases m <;> fin_cases e <;> decide

theorem reveal_computed_target_empty (m : Two) :
    markovTargetStates revealKernel Prod.fst Finset.univ revealPriority m Finset.univ = ∅ := by
  fin_cases m <;> decide

theorem reveal_pair_after_first (m : Two) (n : Nat) :
    stackActionTrajectory (pairPolicy 0 revealPolicy) ((), revealTape m) (n+1) = (m,m) := by
  simp [stackActionTrajectory, stackHistoryTrajectory, observedHistory, pairPolicy,
    currentState, erasePairSources, revealPolicy, feedback, revealTape]

theorem reveal_stack_parity (m : Two) :
    ParitySuccess (revealPriority m)
      (stackActionTrajectory (pairPolicy 0 revealPolicy) ((), revealTape m)) := by
  apply (paritySuccess_shift_iff _ _ 1).mp
  have ht : (fun n => stackActionTrajectory (pairPolicy 0 revealPolicy) ((), revealTape m) (n+1)) =
      (fun _ : Nat => (m,m)) := funext (reveal_pair_after_first m)
  rw [ht]
  have hr : recurrentSet (fun _ : Nat => (m,m)) = {(m,m)} := by
    ext e
    simp [mem_recurrentSet, Recurs, eq_comm]
  refine ⟨2, ?_, by decide⟩
  rw [hr]
  constructor
  · exact ⟨(m,m), by simp, by simp [revealPriority]⟩
  · intro e he
    have heq := Finset.mem_singleton.mp he
    subst e
    simp [revealPriority]

local instance : MeasurableSpace Two := ⊤
local instance : MeasurableSingletonClass Two := by infer_instance
local instance : MeasurableSpace Unit := ⊤
local instance : MeasurableSingletonClass Unit := by infer_instance

theorem reveal_policy_measurable :
    Measurable (fun z : Unit × History Two Two => revealPolicy z.1 z.2) := measurable_of_countable _

/-- A genuine canonical-law countercontrol to deleting support stability from
stable-support necessity. The same policy wins both deterministic revealing models. -/
theorem reveal_policy_almost_sure_parity (m : Two) :
    ∀ᵐ x ∂markovPairLaw revealKernel m 0 revealPolicy (Measure.dirac ()) (0,0),
      ParitySuccess (revealPriority m) x := by
  unfold markovPairLaw
  apply actionLaw_ae_of_stack (pairPolicy 0 revealPolicy)
    (pairPolicy_measurable 0 revealPolicy reveal_policy_measurable) (Measure.dirac ())
    (realRows revealKernel m) (realRows_nonnegative revealKernel m) (realRows_normalized revealKernel m)
    (0,0) _ (paritySuccess_measurable (revealPriority m))
  filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (realRows revealKernel m)
    (realRows_nonnegative revealKernel m) (realRows_normalized revealKernel m)] with z hz
  obtain ⟨r,X⟩ := z
  have hX : X = revealTape m := by
    funext an
    have hp := hz an.1 an.2
    by_contra hne
    change X an ≠ m at hne
    simp [seededStackCoordinate, realRows, revealKernel, revealRows, hne] at hp
  subst X
  cases r
  exact reveal_stack_parity m


/-- Common canonical success and all-time membership in the full allowed set
coexist with an empty initial-support target. Only the stability premise fails. -/
theorem canonical_revealing_counterexample :
    (∀ m : Two, ∀ᵐ x ∂markovPairLaw revealKernel m 0 revealPolicy (Measure.dirac ()) (0,0),
      ParitySuccess (revealPriority m) x) ∧
    (∀ m : Two, ∀ᵐ x ∂markovPairLaw revealKernel m 0 revealPolicy (Measure.dirac ()) (0,0),
      ∀ n, x n ∈ (Finset.univ : Finset (Two × Two))) ∧
    (∀ m : Two, markovTargetStates revealKernel Prod.fst Finset.univ revealPriority m Finset.univ = ∅) := by
  refine ⟨reveal_policy_almost_sure_parity, ?_, reveal_computed_target_empty⟩
  intro m
  exact ae_of_all _ (fun x n => Finset.mem_univ (x n))

end HiddenParity.IndependentAdaptive
