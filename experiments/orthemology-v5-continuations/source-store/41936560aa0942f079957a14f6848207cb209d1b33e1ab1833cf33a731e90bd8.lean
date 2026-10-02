import TailMoments
noncomputable section
open MeasureTheory
open scoped ENNReal
namespace Orthemology.TailMoments.Controls

/-- A genuine probability mass function on costs n+1. -/
theorem geometric_weights_normalized :
    (∑' n : ℕ, (1/2:ℝ≥0∞)^(n+1)) = 1 := by
  rw [ENNReal.tsum_geometric_add_one]
  norm_num
  exact ENNReal.inv_mul_cancel (by norm_num) (by simp)

/-- At the exact exponential boundary, every summand is one, so the moment
is infinite. Strictness in the sufficient exponential-moment range matters. -/
theorem boundary_exponential_moment_infinite :
    (∑' n : ℕ, (1/2:ℝ≥0∞)^(n+1) * (2:ℝ≥0∞)^(n+1)) = ⊤ := by
  simp_rw [← mul_pow]
  have hh : (1/2:ℝ≥0∞)*2 = 1 := by
    simp only [one_div]
    exact ENNReal.inv_mul_cancel (by norm_num) (by simp)
  simp_rw [hh, one_pow]
  exact ENNReal.tsum_const_eq_top_of_ne_zero (by norm_num)

/-- ENNReal.toReal alone conceals infinity. The actual adapter first proves
cost finite almost surely; this deliberately adverse control prevents confusing
its finite-real integrand with an unconditional extended exponential. -/
theorem toReal_top_exponential_is_one (θ : ℝ) :
    ENNReal.ofReal (Real.exp (θ*(⊤:ℝ≥0∞).toReal)) = 1 := by simp

example : ¬ (⊤:ℝ≥0∞) < ⊤ := by simp

#print axioms geometric_weights_normalized
#print axioms boundary_exponential_moment_infinite
#print axioms toReal_top_exponential_is_one
end Orthemology.TailMoments.Controls
