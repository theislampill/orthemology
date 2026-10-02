import PriorSufficiency
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge CentredBernoulli EmpiricalGeometry EmpiricalChernoff ExponentialSeries EmpiricalEndpoints PriorSufficiency
open scoped ENNReal

/-- The tolerance-range restriction cannot simply be deleted from the margin lemma. -/
example : |(5/8:ℝ)-1/2| ≤ 1*(1/2)*(1-1/2)/2 := by
  rw [abs_of_nonneg (by norm_num : (0:ℝ)≤5/8-1/2)]
  norm_num
example : ¬ Accepted (1/2) 1 (1/2+1*(5/8)) := by norm_num [Accepted,D0,D1]

/-- Positive-time endpoint errors vanish, while time zero is genuinely different. -/
example (e : ℝ) : error 4 0 e=0 := error_at_zero 4 e
example (e : ℝ) : error 4 1 e=0 := error_at_one 4 (by norm_num) e
example : error 0 1 (1/4)=1 := by
  norm_num [error,weight,empiricalReport,empiricalMean,failureIndicator,Accepted,D0,D1]

/-- With a fair coin and one receipt the literal empirical report fails on both words. -/
example : error 1 (1/2) (1/4)=1 := by
  have hf : ∀ word : Fin 1 → Bool,
      failureIndicator (1/4) (empiricalReport 1 (1/4) word) (1/2)=1 := by
    intro word
    have hmean : empiricalMean 1 word = if word 0 then (1:ℝ) else 0 := by
      unfold empiricalMean
      rw [Fin.sum_univ_one]
      norm_num
    unfold empiricalReport
    rw [hmean]
    cases hw : word 0 <;> norm_num [hw,failureIndicator,Accepted,D0,D1]
  unfold error
  simp_rw [hf,mul_one]
  exact sum_weight 1 (by norm_num) (by norm_num)

#print axioms CentredBernoulli.one_mgf_upper
#print axioms CentredBernoulli.word_mgf_exact
#print axioms CentredBernoulli.word_mgf_upper
#print axioms EmpiricalGeometry.accepted_of_relative_error
#print axioms EmpiricalChernoff.realError_upper
#print axioms EmpiricalChernoff.error_upper
#print axioms ExponentialSeries.summed_error_bound
#print axioms EmpiricalEndpoints.error_at_zero
#print axioms EmpiricalEndpoints.error_at_one
#print axioms PriorSufficiency.summed_empirical_risk_bound
#print axioms PriorSufficiency.empirical_productRisk_eq
#print axioms PriorSufficiency.empirical_product_risk_finite
#print axioms PriorSufficiency.exists_seeded_report_family_iff
#print axioms PriorSufficiency.exists_report_family_iff
#check PriorSufficiency.exists_seeded_report_family_iff
#check PriorSufficiency.summed_empirical_risk_bound
