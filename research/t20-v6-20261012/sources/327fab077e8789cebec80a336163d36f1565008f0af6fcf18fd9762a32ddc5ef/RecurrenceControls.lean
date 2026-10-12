import CheckedTargetOperation

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2 Orthemology.Tranche2.RecurrentSupport
open scoped BigOperators ENNReal

namespace HiddenParity.Recurrence.Controls

abbrev Two := Fin 2

def flipChain : FiniteChain Two where
  prob s t := if s = t then 0 else 1
  nonnegative s t := by split_ifs <;> norm_num
  normalized s := by fin_cases s <;> norm_num [Fin.sum_univ_two]

def absorbingChain : FiniteChain Two where
  prob s t := if s = t then 1 else 0
  nonnegative s t := by split_ifs <;> norm_num
  normalized s := by simp

/-- This strongly connected chain is periodic, so no aperiodicity is smuggled in. -/
theorem flip_strong : ∀ s t, Relation.ReflTransGen (fun s t => 0 < flipChain.prob s t) s t := by
  intro s t
  by_cases h : s = t
  · subst t
    exact Relation.ReflTransGen.refl
  · exact Relation.ReflTransGen.single (by simp [flipChain, h])

theorem flip_two_step_hit : ∀ s : Two, avoid flipChain 1 2 s = 0 := by
  intro s
  fin_cases s <;> norm_num [avoid, flipChain, Fin.sum_univ_two]

/-- Two steps give a uniform avoidance factor zero in the deterministic cycle. -/
theorem flip_avoidance_bound (k : ℕ) (s : Two) : avoid flipChain 1 (k*2) s ≤ (0 : ℝ)^k :=
  avoid_blocks_bound flipChain 1 2 0 (le_refl _) (fun t => le_of_eq (flip_two_step_hit t)) k s

theorem flip_visits_both :
    ∀ᵐ x ∂markovTrajectory (transitionKernel flipChain) 0, ∀ t, ∃ᶠ n in atTop, x n = t :=
  all_states_recur_almost_surely flipChain 0 flip_strong

def priority23 (s : Two) : ℕ := if s = 0 then 2 else 3

theorem cycle_minimum_even : ∃ k, IsMinimum priority23 (Finset.univ : Finset Two) k ∧ k % 2 = 0 :=
  ⟨2, by decide, rfl⟩

/-- Actual parity success coexists with infinitely many odd-priority visits. -/
theorem actual_cycle_wins_with_infinite_odd_visits :
    ∀ᵐ x ∂markovTrajectory (transitionKernel flipChain) 0,
      PairParitySuccess priority23 x ∧ ∃ᶠ n in atTop, priority23 (x n) = 3 := by
  filter_upwards [flip_visits_both] with x hx
  have hRec : recurrentSet x = Finset.univ := by
    apply Finset.ext
    intro t
    simp only [mem_recurrentSet, Finset.mem_univ, iff_true]
    exact hx t
  refine ⟨by simpa only [PairParitySuccess, hRec] using cycle_minimum_even, ?_⟩
  exact (hx 1).mono (fun n hn => by simp [hn, priority23])

/-- Mere finite nonemptiness/closure is insufficient without connectivity. -/
theorem absorbing_avoids_other (n : ℕ) : avoid absorbingChain 1 n 0 = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [avoid, absorbingChain, Fin.sum_univ_two] using ih

theorem disconnected_has_no_strict_hitting_bound :
    ¬ ∃ N : ℕ, ∃ r : ℝ, r < 1 ∧ ∀ s, avoid absorbingChain 1 N s ≤ r := by
  rintro ⟨N, r, hr, h⟩
  have h0 := h 0
  rw [absorbing_avoids_other] at h0
  linarith

/-- A stationary scheduler that gives a retained action zero probability can miss
that action forever. Positive retained-action probabilities are essential. -/
def unfairPairChain : FiniteChain Two where
  prob _ t := if t = 1 then 1 else 0
  nonnegative _ t := by split_ifs <;> norm_num
  normalized _ := by simp

theorem unfair_avoids_good_pair (n : ℕ) : avoid unfairPairChain 0 n 1 = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [avoid, unfairPairChain, Fin.sum_univ_two] using ih

end HiddenParity.Recurrence.Controls
