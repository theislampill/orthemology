import IntegerBudget
import Mathlib.Analysis.SpecialFunctions.Log.Basic
noncomputable section
namespace Orthemology.IntegerBudget

/-- A rational upper bound on the raw-tape geometric prefactor, requiring
only a positive real rate and a nonnegative finite multiplicity. -/
theorem geometric_prefactor_le_rational (b c : ℝ) (hb : 0 ≤ b) (hc : 0 < c) :
    b/(1-Real.exp (-c)) ≤ b*(1+c)/c := by
  have hd : 0 < 1-Real.exp (-c) := by
    have he : Real.exp (-c) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
    linarith
  have he := Real.add_one_le_exp c
  have hh := mul_le_mul_of_nonneg_right he (Real.exp_pos (-c)).le
  have hexp : Real.exp c * Real.exp (-c) = 1 := by rw [← Real.exp_add]; simp
  rw [hexp] at hh
  have hcore : c ≤ (1+c)*(1-Real.exp (-c)) := by nlinarith
  have hscaled := mul_le_mul_of_nonneg_left hcore hb
  apply (div_le_div_iff₀ hd hc).mpr
  nlinarith

/-- The exact logarithmic progress rate dominates a rational half-success
probability. The positive argument requirement is derived from r<=1. -/
theorem progress_log_rate_lower (r : ℝ) (hr : r ≤ 1) :
    r/2 ≤ -Real.log (1-r/2) := by
  have harg : 0 < 1-r/2 := by linarith
  have hh := Real.log_le_sub_one_of_pos harg
  linarith

/-- The numeric evaluator's rational envelope can safely replace the exact
raw coefficient and exact logarithmic rate in the explicit tail consequence. -/
theorem confidence_from_exact_tail
    (bad b δ c D r T : ℝ) (N J k ell : ℕ)
    (hb : 0 ≤ b) (hδ : 0 ≤ δ) (hc : 0 < c) (hD : 0 < D)
    (hr : r ≤ 1) (hT : 0 ≤ T)
    (hw₁ : 2*(b*(1+c)/c) ≤ δ*(2:ℝ)^k)
    (hw₂ : 2 ≤ δ*(2:ℝ)^ell)
    (hN : (k:ℝ) ≤ c*N)
    (hbudget : 2*D*((J:ℝ)+ell) ≤ r*T)
    (htail : bad ≤ (b/(1-Real.exp (-c)))*Real.exp (-(c*N)) +
      (2:ℝ)^J*Real.exp (-((-Real.log (1-r/2))*T/D))) : bad ≤ δ := by
  apply confidence_from_witnesses bad (b*(1+c)/c) δ c D r
    (-Real.log (1-r/2)) T N J k ell (by positivity) hδ hD hT
    (progress_log_rate_lower r hr) hw₁ hw₂ hN hbudget
  apply htail.trans
  apply add_le_add_right
  exact mul_le_mul_of_nonneg_right (geometric_prefactor_le_rational b c hb hc)
    (Real.exp_pos _).le

#print axioms geometric_prefactor_le_rational
#print axioms progress_log_rate_lower
#print axioms confidence_from_exact_tail
end Orthemology.IntegerBudget
