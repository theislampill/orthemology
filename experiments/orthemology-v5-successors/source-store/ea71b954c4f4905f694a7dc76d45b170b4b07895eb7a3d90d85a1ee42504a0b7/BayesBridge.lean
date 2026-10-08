import GrowthMoment

namespace BayesBridge
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment GrowthMoment
open scoped ENNReal

lemma measurable_weight (n : ℕ) (word : Fin n → Bool) : Measurable (fun a => weight n a word) := by
  unfold weight
  apply Measurable.ennreal_ofReal
  apply Finset.measurable_prod
  intro i hi
  split <;> fun_prop

lemma measurable_failure {Z : Type*} [MeasurableSpace Z] (e : ℝ)
    (q : Z → ℝ) (hq : Measurable q) :
    Measurable (fun p : ℝ × Z => failureIndicator e (q p.2) p.1) := by
  classical
  have hq' : Measurable (fun p : ℝ × Z => q p.2) := hq.comp measurable_snd
  have hD0 : Measurable (fun p : ℝ × Z => D0 p.1 e (q p.2)) := by unfold D0;fun_prop
  have hD1 : Measurable (fun p : ℝ × Z => D1 p.1 e (q p.2)) := by unfold D1;fun_prop
  have hacc : MeasurableSet {p : ℝ × Z | Accepted p.1 e (q p.2)} :=
    (measurableSet_le hD0 measurable_const).inter (measurableSet_le hD1 measurable_const)
  unfold failureIndicator
  exact Measurable.ite hacc measurable_const measurable_const

lemma measurable_weighted_failure {Z : Type*} [MeasurableSpace Z]
    (n : ℕ) (e : ℝ) (word : Fin n → Bool) (q : Z → ℝ) (hq : Measurable q) :
    Measurable (fun p : ℝ × Z => weight n p.1 word * failureIndicator e (q p.2) p.1) :=
  ((measurable_weight n word).comp measurable_fst).mul (measurable_failure e q hq)

/-- Prior-first Bayes failure mass. For parameters in [0,1], the finite sum is
exactly the failure probability in the normalized Bernoulli-word PMF. -/
def bayesRisk {Z : Type*} [MeasurableSpace Z] (n : ℕ) (μ : Measure ℝ)
    (ν : Measure Z) (e : ℝ) (report : (Fin n → Bool) → Z → ℝ) : ℝ≥0∞ :=
  ∫⁻ a, ∫⁻ z, ∑ word, weight n a word * failureIndicator e (report word z) a ∂ν ∂μ

/-- The independent prior-seed product law is an actual Mathlib product measure. -/
def productRisk {Z : Type*} [MeasurableSpace Z] (n : ℕ) (μ : Measure ℝ)
    (ν : Measure Z) (e : ℝ) (report : (Fin n → Bool) → Z → ℝ) : ℝ≥0∞ :=
  ∫⁻ p : ℝ × Z, ∑ word, weight n p.1 word * failureIndicator e (report word p.2) p.1 ∂μ.prod ν

lemma productRisk_eq_bayesRisk {Z : Type*} [MeasurableSpace Z]
    (n : ℕ) (μ : Measure ℝ) (ν : Measure Z) [SFinite ν] (e : ℝ)
    (report : (Fin n → Bool) → Z → ℝ) (hr : ∀ word, Measurable (report word)) :
    productRisk n μ ν e report = bayesRisk n μ ν e report := by
  apply lintegral_prod
  exact (Finset.measurable_sum _ (fun word _ =>
    measurable_weighted_failure n e word (report word) (hr word))).aemeasurable

set_option maxHeartbeats 1000000 in
lemma bayesRisk_eq_risk {Z : Type*} [MeasurableSpace Z]
    (n : ℕ) (μ : Measure ℝ) [SFinite μ] (ν : Measure Z) [SFinite ν] (e : ℝ)
    (report : (Fin n → Bool) → Z → ℝ) (hr : ∀ word, Measurable (report word)) :
    bayesRisk n μ ν e report = risk n μ ν e report := by
  have hf := fun word => measurable_weighted_failure n e word (report word) (hr word)
  unfold bayesRisk risk weightedFailure
  calc
    _ = ∫⁻ a, ∑ word, ∫⁻ z, weight n a word * failureIndicator e (report word z) a ∂ν ∂μ := by
      apply lintegral_congr
      intro a
      exact lintegral_finset_sum (Finset.univ : Finset (Fin n → Bool)) (fun word _ =>
        (hf word).comp (measurable_const.prodMk measurable_id))
    _ = ∑ word, ∫⁻ a, ∫⁻ z, weight n a word * failureIndicator e (report word z) a ∂ν ∂μ :=
      lintegral_finset_sum (Finset.univ : Finset (Fin n → Bool)) (fun word _ => (hf word).lintegral_prod_right)
    _ = _ := by
      apply Finset.sum_congr rfl
      intro word hword
      exact lintegral_lintegral_swap (hf word).aemeasurable

/-- Measurable randomized report families are connected to the actual prior-seed
product law before using the inverse-moment necessity theorem. -/
theorem finite_product_risk_implies_inverse_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (report : (n : ℕ) → (Fin n → Bool) → Z → ℝ)
    (hr : ∀ n word, Measurable (report n word))
    (hfinite : (∑' t, productRisk (t+1) μ ν e (report (t+1))) < ⊤) :
    inverseVarianceMoment μ < ⊤ := by
  apply finite_risk_implies_inverse_moment ν μ e x0 η hη hx0 he he4 hg report
  have hsum : (∑' t, risk (t+1) μ ν e (report (t+1))) =
      ∑' t, productRisk (t+1) μ ν e (report (t+1)) := by
    apply tsum_congr
    intro t
    rw [productRisk_eq_bayesRisk _ _ _ _ _ (hr (t+1)),bayesRisk_eq_risk _ _ _ _ _ (hr (t+1))]
  rwa [hsum]

end
end BayesBridge
