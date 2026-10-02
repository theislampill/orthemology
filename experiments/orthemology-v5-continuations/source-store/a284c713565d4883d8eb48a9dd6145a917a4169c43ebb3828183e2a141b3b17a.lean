import TailMoments
import ActualBadCount
noncomputable section
open MeasureTheory
open scoped ENNReal
namespace Orthemology.TailMoments
open HiddenParity.Cost HiddenParity.Stochastic

/-- The exact inherited actual-pair count, including possible infinite counts.
The affine tail is still a visible premise; this theorem discharges the whole
subsequent expectation, a.s. parity, and exponential-moment implication. -/
theorem actual_bad_count_moments_from_affine_tail
    {Pair : Type*} [Fintype Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair]
    (μ : Measure (ℕ → Pair)) [IsProbabilityMeasure μ]
    (bad : Pair → Prop) [DecidablePred bad] (B V : ℝ) (hV : 0 < V)
    (htail : ∀ u : ℝ, 0 ≤ u →
      μ {x | ENNReal.ofReal (B+V*u) < badCount bad x} ≤ ENNReal.ofReal (Real.exp (-u))) :
    (∫⁻ x, badCount bad x ∂μ) < ⊤ ∧
      (∀ᵐ x ∂μ, ParitySuccess (coBuchiPriority bad) x) ∧
      ∀ θ : ℝ, 0 ≤ θ → θ < 1/V →
        (∫⁻ x, ENNReal.ofReal (Real.exp (θ*(badCount bad x).toReal)) ∂μ) < ⊤ := by
  obtain ⟨hf, _, hmgf⟩ := affine_tail_finite_moments μ (badCount bad)
    (badCount_measurable bad) B V hV htail
  exact ⟨hf, finite_expected_badCount_implies_ae_parity μ bad hf, hmgf⟩

theorem actual_bad_count_all_power_moments_from_affine_tail
    {Pair : Type*} [Fintype Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair]
    (μ : Measure (ℕ → Pair)) [IsProbabilityMeasure μ]
    (bad : Pair → Prop) [DecidablePred bad] (B V : ℝ) (hV : 0 < V)
    (htail : ∀ u : ℝ, 0 ≤ u →
      μ {x | ENNReal.ofReal (B+V*u) < badCount bad x} ≤ ENNReal.ofReal (Real.exp (-u))) :
    ∀ k : ℕ, (∫⁻ x, (badCount bad x)^k ∂μ) < ⊤ := by
  obtain ⟨_, hfinite, hmgf⟩ := affine_tail_finite_moments μ (badCount bad)
    (badCount_measurable bad) B V hV htail
  have hθ : 0 < 1/(2*V) := by positivity
  have hθV : 1/(2*V) < 1/V := by
    apply one_div_lt_one_div_of_lt hV
    linarith
  intro k
  exact finite_power_moment_of_positive_exponential_moment μ (badCount bad)
    (badCount_measurable bad) hfinite (1/(2*V)) hθ (hmgf _ hθ.le hθV) k

#print axioms actual_bad_count_all_power_moments_from_affine_tail
#print axioms actual_bad_count_moments_from_affine_tail
end Orthemology.TailMoments
