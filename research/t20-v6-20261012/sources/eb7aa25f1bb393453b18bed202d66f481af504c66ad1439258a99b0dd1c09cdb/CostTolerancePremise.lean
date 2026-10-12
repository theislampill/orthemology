import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

/-! This checks only the exact scalar premise changed by the hash-bound Sixth
cost mutation. It is not a replay of ActualExponentialMoments or a counterexample
to its unchanged positive theorem. -/

theorem original_premise_is_satisfiable :
    (0 : ℝ) < 1 ∧ (1 : ℝ) ≤ 1 := by norm_num

theorem half_tolerance_premise_does_not_follow :
    ¬ (∀ ε η : ℝ, 0 < η → η ≤ ε → η ≤ ε / 2) := by
  intro h
  have hx := h 1 1 (by norm_num) (by norm_num)
  norm_num at hx

#print axioms half_tolerance_premise_does_not_follow
