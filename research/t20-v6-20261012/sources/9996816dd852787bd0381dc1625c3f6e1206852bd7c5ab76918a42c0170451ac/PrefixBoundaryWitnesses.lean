import PrefixControls

namespace IndependentPrefixAudit
open P02A2.ObserverCore P02A2.Q8Measure P02A2.SurvivorCandidates OrthemologyTagged

def oneWitness (_ : Unit) (_i s _t : ℕ) : Prop := s = 1
instance oneWitness_decidable : ∀ a i, DecidableRel (oneWitness a i) := by
  intro a i s t
  unfold oneWitness
  infer_instance

def wrongTailStage (n word : ℕ) : ℕ :=
  let i := selector n word
  if n ≤ i then word % 2
  else if innovation (oneWitness () i) (n-i) then word % 2 else 0

/-- Advancing the row stage by one loses its first innovation. -/
theorem wrong_tail_stage_changes_first_bit :
    pi3PrefixValue oneWitness () 1 5 = 1 ∧ wrongTailStage 1 5 = 0 := by
  decide +kernel

/-- The actual finite-prefix observer is causal for all input pairs, not only almost everywhere. -/
theorem no_future_input_use {A : Type*} (R : A → ℕ → ℕ → ℕ → Prop)
    [∀ a i, DecidableRel (R a i)] (a : A) (x y : Cantor) (n : ℕ)
    (h : ∀ i ≤ n, x i = y i) :
    pi3Observer R a x n = pi3Observer R a y n := by
  rw [← pi3PrefixValue_output R a]
  exact prefix_causal (pi3PrefixValue R a) x y n h

/-- The finite selector before and at the first zero has distinct boundary results. -/
theorem boundary_before_and_at : selector 0 3 = 1 ∧ selector 1 6 = 1 := by
  decide +kernel

#print axioms wrong_tail_stage_changes_first_bit
#print axioms no_future_input_use
#print axioms boundary_before_and_at
end IndependentPrefixAudit
