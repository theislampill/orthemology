import EndpointAtoms
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge
open EmpiricalGeometry EmpiricalChernoff EmpiricalEndpoints PriorSufficiency EndpointProcess EndpointAtoms
open scoped ENNReal
noncomputable section

/-- The unnormalized shortcut min(A,F)≥A*F is false. The total-mass
factor in the actual finite-measure proof is necessary. -/
example : ¬ ((2 : ℝ≥0∞) * 2 ≤ min 2 2) := by norm_num
example : (2 : ℝ≥0∞) * 2 ≤ 2 * min 2 2 := by norm_num

/-- Epsilon zero destroys the endpoint separation geometry. -/
example (a : ℝ) : Accepted a 0 (1/2) := by norm_num [Accepted,D0,D1]

/-- The right endpoint's accepted report is asymmetric. -/
example : Accepted 1 (1/4) (3/4) := by norm_num [Accepted,D0,D1]
example : ¬ Accepted 1 (1/4) (1/2) := by norm_num [Accepted,D0,D1]
example : ¬ Accepted (1/2) (1/4) (3/4) := by norm_num [Accepted,D0,D1]
example : ¬ Accepted (1/2) (1/4) (1/2) := by norm_num [Accepted,D0,D1]

theorem spike_zero_unchanged (μ : Measure ℝ) : leftSpike μ 0=μ := by simp [leftSpike]
theorem spike_one_pure_endpoint (μ : Measure ℝ) : leftSpike μ 1=Measure.dirac 0 := by simp [leftSpike]

/-- Complete replacement is an actual zero-budget prior, so the strict θ<1
hypothesis of the divergence theorem cannot be silently removed. -/
theorem spike_one_empirical_zero {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (e : ℝ) :
    (∫⁻ ω, totalFailures e (fun n w _ => empiricalReport n e w) ω
      ∂experimentLaw (leftSpike μ 1) ν)=0 := by
  rw [spike_one_pure_endpoint,actual_expectation_eq_risk_series _ ν (by simp) e _
    (fun n w => measurable_const)]
  simp_rw [empirical_productRisk_eq]
  simp [error_at_zero]

/-- Both endpoint atoms may be present with zero interior moment. -/
theorem endpoint_pair_interior_moment_zero (A B : ℝ≥0∞) :
    inverseVarianceMoment (A • Measure.dirac 0 + B • Measure.dirac 1)=0 := by
  have h := interior_add_endpoint_atoms (0 : Measure ℝ) A B
  simp only [zero_add] at h
  unfold inverseVarianceMoment
  rw [h]
  simp [EndpointMoment.interior]

/-- An ordinary two-atom probability prior has the expected scaled moment
after normalized endpoint contamination. -/
example : leftMoment (leftSpike (Measure.dirac (1/2:ℝ)) (1/4))=(3/2:ℝ≥0∞) := by
  rw [leftSpike_leftMoment]
  have hm : leftMoment (Measure.dirac (1/2:ℝ))=2 := by
    norm_num [leftMoment,EndpointMoment.interior,restrict_dirac]
  rw [hm]
  apply (ENNReal.toReal_eq_toReal_iff' (ENNReal.mul_ne_top (by simp) (by norm_num))
    (ENNReal.mul_ne_top (by norm_num) (by simp))).mp
  rw [ENNReal.toReal_mul,ENNReal.toReal_sub_of_le (by norm_num : (1/4:ℝ≥0∞)≤1) (by simp)]
  norm_num

#print axioms spike_zero_unchanged
#print axioms spike_one_pure_endpoint
#print axioms spike_one_empirical_zero
#print axioms endpoint_pair_interior_moment_zero
