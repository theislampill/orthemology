import EndpointProcessControls

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal
open EndpointProcess BernoulliWord EndpointMoment AnnularLiteral BayesBridge GrowthMoment
namespace IndependentEndpointProcessReview

/-- Independent bridge for any observable finite-word payoff. It follows from
actual product integration and prefix masses, without a loss-risk identity premise. -/
theorem actual_word_payoff {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (n : ℕ) (f : (Fin n → Bool) → ℝ≥0∞) :
    (∫⁻ ω : (ℝ × Z) × Innovations, f (observedWord n ω.1.1 ω.2)
      ∂experimentLaw μ ν) = ∫⁻ a, ∑ w, weight n a w * f w ∂μ := by
  have hm : Measurable (fun ω : (ℝ × Z) × Innovations => f (observedWord n ω.1.1 ω.2)) :=
    (measurable_of_countable f).comp ((prefix_measurable n).comp
      (measurable_fst.fst.prodMk measurable_snd))
  have hg : Measurable (fun p : ℝ × Z => ∑ w, weight n p.1 w * f w) := by
    apply Finset.measurable_sum
    intro w _
    exact ((measurable_weight n w).comp measurable_fst).mul_const _
  unfold experimentLaw
  rw [lintegral_prod _ hm.aemeasurable]
  calc
    _ = ∫⁻ p : ℝ × Z, ∑ w, weight n p.1 w * f w ∂μ.prod ν := by
      apply lintegral_congr_ae
      filter_upwards [ae_supported_product μ ν hs] with p hp
      exact lintegral_prefix_function n hp.1 hp.2 f
    _ = _ := by rw [lintegral_prod _ hg.aemeasurable]; simp

/-- Same latent parameter at both receipts, with actual innovation readout in
an actual two-point prior product experiment. -/
theorem actual_two_ones_mass :
    (∫⁻ ω : (ℝ × Unit) × Innovations,
      (if observedWord 2 ω.1.1 ω.2 = (fun _ => true) then (1:ℝ≥0∞) else 0)
      ∂experimentLaw ((1/2:ℝ≥0∞) • Measure.dirac (1/4:ℝ) +
        (1/2:ℝ≥0∞) • Measure.dirac (3/4:ℝ)) (Measure.dirac ())) = 5/16 := by
  have hs : ∀ᵐ a ∂((1/2:ℝ≥0∞) • Measure.dirac (1/4:ℝ) +
      (1/2:ℝ≥0∞) • Measure.dirac (3/4:ℝ)), 0≤a ∧ a≤1 := by
    rw [ae_add_measure_iff]
    constructor <;> apply Measure.ae_smul_measure <;> norm_num
  change (∫⁻ ω : (ℝ × Unit) × Innovations,
    (fun w : Fin 2 → Bool => if w = (fun _ => true) then (1:ℝ≥0∞) else 0)
      (observedWord 2 ω.1.1 ω.2) ∂experimentLaw _ _) = _
  rw [actual_word_payoff _ _ hs 2 (fun w => if w = (fun _ => true) then (1:ℝ≥0∞) else 0)]
  simp only [mul_ite,mul_one,mul_zero,Finset.sum_ite_eq',Finset.mem_univ,if_true]
  rw [lintegral_add_measure]
  norm_num [ENNReal.ofReal_div_of_pos]
  have h0 : (2:ℝ≥0∞)⁻¹ * 16⁻¹ ≠ ⊤ := ENNReal.mul_ne_top (by simp) (by simp)
  have h1 : (2:ℝ≥0∞)⁻¹ * (9/16) ≠ ⊤ :=
    ENNReal.mul_ne_top (by simp) (ENNReal.mul_ne_top (by norm_num) (by simp))
  apply (ENNReal.toReal_eq_toReal_iff' (ENNReal.add_ne_top.mpr ⟨h0,h1⟩)
    (ENNReal.mul_ne_top (by norm_num) (by simp))).mp
  rw [ENNReal.toReal_add h0 h1]
  norm_num

/-- Reports expose no innovation magnitude or source parameter beyond the
observed Boolean prefix. Equal observed words and seed give equal reports. -/
theorem reports_only_observed_word {Z : Type*} (r : ReportFamily Z) (n : ℕ)
    (a b : ℝ) (z : Z) (u v : Innovations)
    (hword : observedWord n a u = observedWord n b v) :
    r n (observedWord n a u) z = r n (observedWord n b v) z := by rw [hword]

/-- The actual literal count expands to the precise accepted-loss complement
at every positive sample index. There is no error-magnitude weighting. -/
theorem total_count_literal_contract {Z : Type*} (e : ℝ) (r : ReportFamily Z)
    (ω : (ℝ × Z) × Innovations) :
    totalFailures e r ω = ∑' t : ℕ,
      if D0 ω.1.1 e (r (t+1) (observedWord (t+1) ω.1.1 ω.2) ω.1.2) ≤ 0 ∧
        D1 ω.1.1 e (r (t+1) (observedWord (t+1) ω.1.1 ω.2) ω.1.2) ≤ 0
      then (0:ℝ≥0∞) else 1 := by
  unfold totalFailures
  apply tsum_congr
  intro t
  by_cases h : Accepted ω.1.1 e (r (t+1) (observedWord (t+1) ω.1.1 ω.2) ω.1.2)
  · have hh := h
    unfold Accepted at hh
    simp [stageFailure,failureIndicator,h,hh]
  · have hh := h
    unfold Accepted at hh
    simp [stageFailure,failureIndicator,h,hh]

/-- The process is a genuine probability experiment for a continuous Borel
prior too, not only for an atomic or countable latent law. -/
example : IsProbabilityMeasure (experimentLaw uniformLaw (Measure.dirac ())) := inferInstance

/-- At alpha zero there are exceptional innovation paths with all true bits;
they have no probability mass. A universal all-path zero-bit assertion is false. -/
theorem exceptional_zero_innovation_path :
    observedWord 3 0 (fun _ => 0) = (fun _ => true) ∧
      innovationLaw (wordEvent 3 0 (fun _ => true)) = 0 := by
  constructor
  · funext i; norm_num [observedWord,bit]
  · rw [wordEvent_mass 3 (by norm_num) (by norm_num)]
    norm_num [weight]

/-- The independent private seed may have an arbitrary measurable space;
rectangle independence needs no equality of source-conditional laws as premise. -/
theorem source_seed_innovation_rectangles {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (A : Set ℝ) (B : Set Z) (C : Set Innovations) :
    experimentLaw μ ν ((A ×ˢ B) ×ˢ C) = μ A * ν B * innovationLaw C :=
  experiment_rectangle μ ν A B C

set_option pp.explicit true in
#check @actual_expectation_eq_risk_series
set_option pp.explicit true in
#check @exists_coherent_finite_actual_expectation_iff
set_option pp.explicit true in
#check @every_policy_infinite_of_infinite_moment
#print axioms actual_word_payoff
#print axioms actual_two_ones_mass
#print axioms reports_only_observed_word
#print axioms total_count_literal_contract
#print axioms exceptional_zero_innovation_path
#print axioms source_seed_innovation_rectangles
end IndependentEndpointProcessReview
