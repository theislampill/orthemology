import FiniteModelExponentialUniformity
open MeasureTheory
open scoped ENNReal
-- Extended-value guard is substantively necessary.
example : (⊤ : ℝ≥0∞).toReal = 0 := by simp
example (θ : ℝ) : ENNReal.ofReal (Real.exp (θ * (⊤ : ℝ≥0∞).toReal)) = 1 := by simp
example : ¬ ((⊤ : ℝ≥0∞) < ⊤) := by simp
-- Finite minimum, not maximum, preserves every model's open range.
example : min (2 : ℝ) 5 = 2 := by norm_num
example : (3 : ℝ) < max 2 5 ∧ ¬ (3 : ℝ) < min 2 5 := by norm_num
example : ¬ (2 : ℝ) < min 2 5 := by norm_num
-- A finite maximum dominates each integral; the empty family is harmless.
example : ({(2 : ℝ≥0∞), 5} : Finset ℝ≥0∞).sup id = 5 := by norm_num
example : (∅ : Finset ℝ≥0∞).sup id = 0 := by simp
