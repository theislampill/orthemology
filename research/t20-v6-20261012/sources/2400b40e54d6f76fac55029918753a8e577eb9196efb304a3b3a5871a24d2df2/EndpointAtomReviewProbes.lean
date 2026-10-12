import EndpointAtomControls

noncomputable section
open MeasureTheory Set
open scoped ENNReal
open EndpointAtoms EndpointProcess EndpointMoment AnnularLiteral BernoulliWord BayesBridge
open EmpiricalGeometry PriorSufficiency
namespace IndependentEndpointAtomReview

/-- Quantitative actual-process lower bound before imposing finiteness. This
exposes the total-mass factor for arbitrary finite, unnormalized priors. -/
theorem actual_left_profile_budget_bound {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (lowerConstant*μ {0}) * (∑' t : ℕ, leftMass μ (t+1)) ≤
      μ univ * (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν) := by
  have hsplit : (∑ t ∈ Finset.range 1, risk (t+1) μ ν e (r (t+1))) +
      (∑' t, risk (t+1+1) μ ν e (r (t+1+1))) =
      ∑' t, risk (t+1) μ ν e (r (t+1)) :=
    ENNReal.summable.sum_add_tsum_nat_add'
  have htail : (∑' t, risk (t+2) μ ν e (r (t+2))) ≤
      ∑' t, risk (t+1) μ ν e (r (t+1)) := by
    simpa only [Nat.add_assoc] using
      (show (∑' t, risk (t+1+1) μ ν e (r (t+1+1))) ≤
        ∑' t, risk (t+1) μ ν e (r (t+1)) from by rw [← hsplit];exact le_add_self)
  have hsum : (lowerConstant*μ {0}) * (∑' t : ℕ, leftMass μ (t+1)) ≤
      μ univ*(∑' t, risk (t+2) μ ν e (r (t+2))) := by
    rw [← ENNReal.tsum_mul_left,← ENNReal.tsum_mul_left]
    exact ENNReal.tsum_le_tsum (fun t => left_atom_mass_lower ν μ e he he4 t (r (t+2)))
  have hseries : (∑' t, risk (t+1) μ ν e (r (t+1))) =
      ∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν := by
    rw [risk_series_eq_product ν μ e r hr,actual_expectation_eq_risk_series μ ν hs e r hr]
  exact hsum.trans ((mul_le_mul_left' htail (μ univ)).trans_eq (congrArg (fun x => μ univ*x) hseries))

/-- The same result remains uniform in arbitrary independent probability seed
spaces and does not demand the reports themselves be coherent for necessity. -/
theorem either_divergent_required_moment_rules_out_all_reports {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (h : (0<μ {0} ∧ leftMoment μ=⊤) ∨ (0<μ {1} ∧ rightMoment μ=⊤))
    (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν)=⊤ := by
  rcases h with ⟨h0,hl⟩ | ⟨h1,hright⟩
  · exact left_atom_infinite_of_infinite_moment ν μ hs e he he4 h0 hl r hr
  · exact right_atom_infinite_of_infinite_moment ν μ hs e he he4 h1 hright r hr

theorem right_endpoint_asymmetric_at_seventh :
    Accepted 1 (1/7) (9/14) ∧ ¬ Accepted 1 (1/7) (1/2) ∧
      ¬ Accepted (3/7) (1/7) (9/14) := by
  norm_num [Accepted,D0,D1]

/-- An unnormalized endpoint-only prior has zero actual empirical budget. -/
theorem unnormalized_endpoints_actual_zero {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4) :
    (∫⁻ ω, totalFailures e (fun n w _ => empiricalReport n e w) ω
      ∂experimentLaw ((2:ℝ≥0∞) • Measure.dirac (0:ℝ) + (3:ℝ≥0∞) • Measure.dirac (1:ℝ)) ν)=0 := by
  have hs : ∀ᵐ a ∂((2:ℝ≥0∞) • Measure.dirac (0:ℝ) + (3:ℝ≥0∞) • Measure.dirac (1:ℝ)), 0≤a ∧ a≤1 := by
    rw [ae_add_measure_iff]
    constructor <;> apply Measure.ae_smul_measure <;> simp
  apply le_antisymm _ bot_le
  have h := empirical_actual_expectation_bound ((2:ℝ≥0∞) • Measure.dirac (0:ℝ) + (3:ℝ≥0∞) • Measure.dirac (1:ℝ)) ν hs e he he4
  simpa only [endpoint_pair_interior_moment_zero,mul_zero] using h

/-- The normalized spike's probability law is a theorem, not an input premise. -/
theorem normalized_spike_is_actual_probability {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsProbabilityMeasure μ]
    (θ : ℝ≥0∞) (hθ : θ≤1) : IsProbabilityMeasure (experimentLaw (leftSpike μ θ) ν) := by
  letI := leftSpike_probability μ θ hθ
  infer_instance

/-- Strict partial contamination matters: the endpoint replacement has zero
count, so an all-θ divergence claim would be false even under infinite moments. -/
theorem complete_replacement_not_infinite {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (e : ℝ) :
    (∫⁻ ω, totalFailures e (fun n w _ => empiricalReport n e w) ω
      ∂experimentLaw (leftSpike μ 1) ν) ≠ ⊤ := by
  rw [spike_one_empirical_zero]
  exact ENNReal.zero_ne_top

/-- A finite total mass is part of the quantitative statement; dropping it
fails as a finite numerical inequality, even for positive finite masses. -/
theorem unnormalized_minimum_shortcut_fails :
    ¬ ((3 : ℝ≥0∞) * 2 ≤ min 3 2) ∧ ((3 : ℝ≥0∞) * 2 ≤ 5 * min 3 2) := by norm_num

/-- A zero seed measure would make every actual count integral zero. The
probability-seed hypothesis cannot be dropped from the necessity contract. -/
theorem zero_seed_measure_is_vacuous (μ : Measure ℝ) (e : ℝ) (r : ReportFamily Unit) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ (0 : Measure Unit)) = 0 := by
  simp [experimentLaw]

set_option pp.explicit true in
#check @finite_actual_implies_left_moment
set_option pp.explicit true in
#check @finite_actual_implies_right_moment
set_option pp.explicit true in
#check @both_atoms_coherent_actual_iff
set_option pp.explicit true in
#check @left_spike_destroys_finite_budget
#print axioms actual_left_profile_budget_bound
#print axioms either_divergent_required_moment_rules_out_all_reports
#print axioms right_endpoint_asymmetric_at_seventh
#print axioms unnormalized_endpoints_actual_zero
#print axioms normalized_spike_is_actual_probability
#print axioms complete_replacement_not_infinite
#print axioms unnormalized_minimum_shortcut_fails
#print axioms zero_seed_measure_is_vacuous
end IndependentEndpointAtomReview
