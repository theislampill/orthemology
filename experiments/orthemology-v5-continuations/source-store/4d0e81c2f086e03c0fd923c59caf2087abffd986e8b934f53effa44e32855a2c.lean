import EmpiricalEndpoints

namespace PriorSufficiency
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge GrowthMoment CentredBernoulli EmpiricalGeometry EmpiricalChernoff ExponentialSeries EmpiricalEndpoints
open scoped ENNReal

lemma measurable_error (n : ℕ) (e : ℝ) : Measurable (fun a => error n a e) := by
  classical
  apply Finset.measurable_sum
  intro word hword
  apply (measurable_weight n word).mul
  unfold failureIndicator
  exact Measurable.ite (measurableSet_accepted e (empiricalReport n e word)) measurable_const measurable_const

/-- Arbitrary endpoint atoms have zero empirical error at every positive time. The
interior envelope is integrated using actual Mathlib restriction and Tonelli. -/
theorem summed_empirical_risk_bound (μ : Measure ℝ) (e : ℝ)
    (hsupport : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (he : 0<e) (he4 : e≤1/4) :
    (∑' n : ℕ, ∫⁻ a, error (n+1) a e ∂μ) ≤
      ENNReal.ofReal (32/e^2) * inverseVarianceMoment μ := by
  have hC : 0≤32/e^2 := by positivity
  have hpoint : ∀ᵐ a ∂μ, (∑' n : ℕ, error (n+1) a e) ≤
      (Ioo (0:ℝ) 1).indicator (fun a => ENNReal.ofReal (32/e^2) * ENNReal.ofReal (a*(1-a))⁻¹) a := by
    filter_upwards [hsupport] with a ha
    by_cases hint : a ∈ Ioo (0:ℝ) 1
    · rw [Set.indicator_of_mem hint,← ENNReal.ofReal_mul hC]
      exact summed_error_bound hint.1 hint.2 he he4
    · rw [Set.indicator_of_not_mem hint]
      by_cases h0 : a=0
      · subst a;simp [error_at_zero]
      · have h1 : a=1 := by
          have hn : ¬(0<a ∧ a<1) := hint
          rcases not_and_or.mp hn with h|h
          · exact False.elim (h (lt_of_le_of_ne ha.1 (Ne.symm h0)))
          · linarith
        subst a
        have hz : ∀ n : ℕ, error (n+1) 1 e=0 := fun n => error_at_one (n+1) (by omega) e
        simp_rw [hz]
        simp
  calc
    _ = ∫⁻ a, ∑' n : ℕ, error (n+1) a e ∂μ :=
      (lintegral_tsum (fun n => (measurable_error (n+1) e).aemeasurable)).symm
    _ ≤ ∫⁻ a, (Ioo (0:ℝ) 1).indicator
        (fun a => ENNReal.ofReal (32/e^2) * ENNReal.ofReal (a*(1-a))⁻¹) a ∂μ :=
      lintegral_mono_ae hpoint
    _ = ∫⁻ a, ENNReal.ofReal (32/e^2) * ENNReal.ofReal (a*(1-a))⁻¹ ∂interior μ :=
      lintegral_indicator measurableSet_Ioo _
    _ = _ := lintegral_const_mul' _ _ ENNReal.ofReal_ne_top

lemma empirical_productRisk_eq {Z : Type*} [MeasurableSpace Z]
    (n : ℕ) (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) :
    productRisk n μ ν e (fun word _z => empiricalReport n e word) =
      ∫⁻ a, error n a e ∂μ := by
  rw [productRisk_eq_bayesRisk _ _ _ _ _ (fun word => measurable_const)]
  simp [bayesRisk,error]

/-- Concrete deterministic empirical reports have finite summed product-law risk
whenever the interior inverse moment is finite. No lower growth is needed here. -/
theorem empirical_product_risk_finite {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ)
    (hsupport : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (he : 0<e) (he4 : e≤1/4)
    (hmoment : inverseVarianceMoment μ < ⊤) :
    (∑' n : ℕ, productRisk (n+1) μ ν e (fun word _z => empiricalReport (n+1) e word)) < ⊤ := by
  simp_rw [empirical_productRisk_eq]
  exact lt_of_le_of_lt (summed_empirical_risk_bound μ e hsupport he he4)
    (ENNReal.mul_lt_top ENNReal.ofReal_lt_top hmoment)

/-- The same existence boundary holds for any fixed independent probability seed law. -/
theorem exists_seeded_report_family_iff {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (hsupport : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) :
    (∃ report : (n : ℕ) → (Fin n → Bool) → Z → ℝ,
      (∀ n word, Measurable (report n word)) ∧
      (∑' t : ℕ, productRisk (t+1) μ ν e (report (t+1))) < ⊤) ↔
      inverseVarianceMoment μ < ⊤ := by
  constructor
  · rintro ⟨report,hr,hfinite⟩
    exact finite_product_risk_implies_inverse_moment ν μ e x0 η hη hx0 he he4 hg report hr hfinite
  · intro hm
    refine ⟨(fun n word _ => empiricalReport n e word), (fun n word => measurable_const), ?_⟩
    exact empirical_product_risk_finite μ ν e hsupport he he4 hm

/-- Full existence iff for deterministic-time finite-word product risks. It does
not assert a construction of an infinite sample process or pathwise bad counter. -/
theorem exists_report_family_iff (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (hsupport : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) :
    (∃ report : (n : ℕ) → (Fin n → Bool) → Unit → ℝ,
      (∀ n word, Measurable (report n word)) ∧
      (∑' t : ℕ, productRisk (t+1) μ (Measure.dirac ()) e (report (t+1))) < ⊤) ↔
      inverseVarianceMoment μ < ⊤ := by
  constructor
  · rintro ⟨report,hr,hfinite⟩
    exact finite_product_risk_implies_inverse_moment (Measure.dirac ()) μ e x0 η hη hx0
      he he4 hg report hr hfinite
  · intro hm
    refine ⟨(fun n word _ => empiricalReport n e word), (fun n word => measurable_const), ?_⟩
    exact empirical_product_risk_finite μ (Measure.dirac ()) e hsupport he he4 hm

end
end PriorSufficiency
