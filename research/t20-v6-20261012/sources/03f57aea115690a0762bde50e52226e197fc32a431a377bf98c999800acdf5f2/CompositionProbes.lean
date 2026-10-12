import ActualExponentialMoments
noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace IndependentExponentialComposition

/-- ENNReal.toReal alone can conceal an infinite cost. -/
theorem top_exponential_toReal_is_one (θ : ℝ) :
    ENNReal.ofReal (Real.exp (θ*(⊤ : ℝ≥0∞).toReal)) = 1 := by simp

/-- Thus the separately asserted count-finiteness clause is load-bearing. -/
theorem top_cost_not_finite : ¬ (⊤ : ℝ≥0∞) < ⊤ := by simp

theorem infinite_cost_has_finite_converted_integral (θ : ℝ) :
    (∫⁻ _ : Unit, ENNReal.ofReal (Real.exp (θ*(⊤ : ℝ≥0∞).toReal)) ∂Measure.dirac ()) < ⊤ := by simp

/-- The geometric factor becomes one exactly at the rate boundary. -/
theorem rate_boundary_not_contracting (V : ℝ) :
    Real.exp (1/V)*Real.exp (-(1/V)) = 1 := by rw [← Real.exp_add];simp

/-- At that boundary the generic geometric-series certificate is infinite. -/
theorem rate_boundary_certificate_infinite : ((1-(1:ℝ≥0∞))⁻¹ : ℝ≥0∞) = ⊤ := by simp

/-- Positive affine scale means the selected rate is genuinely positive. -/
theorem inverse_scale_rate_positive (V : ℝ) (hV : 0 < V) : 0 < 1/V := by positivity

/-- Canonical history readout takes the first executed action from H(1). -/
def firstHistory : ℕ → History ℕ Unit
  | 0 => []
  | n+1 => [(if n=0 then 7 else 0,())]

theorem first_action_preserved (d : ℕ) : historyAction d firstHistory 0 = 7 := by
  simp [historyAction, firstHistory]

theorem skipping_first_changes_action (d : ℕ) : historyAction d firstHistory 1 = 0 := by
  simp [historyAction, firstHistory]

#print axioms top_exponential_toReal_is_one
#print axioms top_cost_not_finite
#print axioms infinite_cost_has_finite_converted_integral
#print axioms rate_boundary_not_contracting
#print axioms rate_boundary_certificate_infinite
#print axioms inverse_scale_rate_positive
#print axioms first_action_preserved
#print axioms skipping_first_changes_action
end IndependentExponentialComposition
