import RobustBinaryRepair
import Mathlib.Algebra.Order.BigOperators.Ring.Finset

open scoped BigOperators

namespace Orthemology.Tranche3

noncomputable section

variable {ι : Type*} [Fintype ι]

def reportMean (w q : ι → ℝ) : ℝ := ∑ i, w i*q i
def reportVariance (w q : ι → ℝ) : ℝ := ∑ i, w i*(q i-reportMean w q)^2

theorem reportMean_mem (w q : ι → ℝ) (hw0 : ∀ i, 0 ≤ w i)
    (hw1 : ∑ i, w i = 1) (hq0 : ∀ i, 0 ≤ q i) (hq1 : ∀ i, q i ≤ 1) :
    0 ≤ reportMean w q ∧ reportMean w q ≤ 1 := by
  constructor
  · exact Finset.sum_nonneg fun i _ => mul_nonneg (hw0 i) (hq0 i)
  · calc
      reportMean w q ≤ ∑ i, w i*1 := Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (hq1 i) (hw0 i)
      _ = 1 := by simpa using hw1

theorem reportVariance_nonneg (w q : ι → ℝ) (hw0 : ∀ i, 0 ≤ w i) :
    0 ≤ reportVariance w q :=
  Finset.sum_nonneg fun i _ => mul_nonneg (hw0 i) (sq_nonneg _)

lemma reportVariance_identity (w q : ι → ℝ) (hw1 : ∑ i, w i = 1) :
    reportVariance w q = (∑ i, w i*(q i)^2) - (reportMean w q)^2 := by
  unfold reportVariance
  calc
    (∑ i, w i * (q i-reportMean w q)^2) =
        (∑ i, ((w i*(q i)^2 - 2*reportMean w q*(w i*q i)) + w i*(reportMean w q)^2)) := by
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = (∑ i, w i*(q i)^2) - (reportMean w q)^2 := by
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.sum_mul]
      rw [hw1]
      change (∑ i, w i*(q i)^2)-2*reportMean w q*reportMean w q+1*(reportMean w q)^2 = _
      ring

/-- Each expected truth-state score decomposes into mean-report loss plus
exactly the randomisation variance. -/
theorem expected_excess_decomposition (w q : ι → ℝ) (hw1 : ∑ i, w i = 1)
    (a e : ℝ) :
    (∑ i, w i*excessZero a e (q i)) = excessZero a e (reportMean w q)+reportVariance w q ∧
    (∑ i, w i*excessOne a e (q i)) = excessOne a e (reportMean w q)+reportVariance w q := by
  rw [reportVariance_identity w q hw1]
  constructor
  · simp only [excessZero, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul, hw1]
    ring
  · calc
      (∑ i, w i*excessOne a e (q i)) =
          (∑ i, (w i*(q i)^2 - 2*(w i*q i) + w i*(1-(a*(1/2-e)^2+(1-a)*(1/2)^2)))) := by
        apply Finset.sum_congr rfl
        intro i _
        unfold excessOne
        ring
      _ = excessOne a e (reportMean w q)+((∑ i,w i*(q i)^2)-(reportMean w q)^2) := by
        rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.sum_mul, hw1]
        unfold excessOne reportMean
        ring

/-- Finite randomisation cannot lower minimax expected regret; its entire
variance is an additional cost. This is not a statement about success
probability of individual realised reports. -/
theorem randomised_regret_lower_bound (w q : ι → ℝ) (hw0 : ∀ i, 0 ≤ w i)
    (hw1 : ∑ i,w i = 1) (hq0 : ∀ i, 0 ≤ q i) (hq1 : ∀ i, q i ≤ 1)
    (l u e : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u) (hu1 : u ≤ 1)
    (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    robustValue l u e + reportVariance w q ≤
      max (∑ i,w i*excessZero l e (q i)) (∑ i,w i*excessOne u e (q i)) := by
  rw [(expected_excess_decomposition w q hw1 l e).1,
      (expected_excess_decomposition w q hw1 u e).2, max_add_add_right]
  have hm := reportMean_mem w q hw0 hw1 hq0 hq1
  exact add_le_add_right (robustValue_le_max l u e (reportMean w q) hl0 hlu hu1 he0 he1 hm.1 hm.2) _

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.expected_excess_decomposition
#print axioms Orthemology.Tranche3.randomised_regret_lower_bound
