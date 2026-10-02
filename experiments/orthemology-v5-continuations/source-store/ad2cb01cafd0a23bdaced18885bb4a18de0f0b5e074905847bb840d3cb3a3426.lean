import BayesBridge
open MeasureTheory Set AnnularLiteral BernoulliWord
open scoped ENNReal

/-- The right width cannot be replaced by the symmetric left 5/3 constant. -/
example : (1-lower (1/4) (37/50)) / (1-upper (1/4) (37/50)) = (149/85:ℝ) := by
  norm_num [lower,upper]
example : (5/3:ℝ) < (149/85:ℝ) ∧ (149/85:ℝ) < 9/5 := by norm_num
example : ¬ (1-lower (1/4) (37/50) ≤ (5/3)*(1-upper (1/4) (37/50))) := by
  norm_num [lower,upper]
example : 1-lower (1/4) (37/50) ≤ (9/5)*(1-upper (1/4) (37/50)) := by
  exact right_width (by norm_num) (by norm_num) (by norm_num)

/-- Zero observations have one word, so the two extreme words may not be double-counted. -/
example : (fun _ : Fin 0 => false) = (fun _ : Fin 0 => true) := by ext i;exact Fin.elim0 i
example : ∑ word : Fin 2 → Bool, weight 2 (1/4) word = 1 := by
  exact sum_weight 2 (by norm_num) (by norm_num)
example : weight 2 (1/4) (fun _ => false) = ENNReal.ofReal (9/16 : ℝ) := by norm_num [weight]
example : weight 2 (1/4) (fun _ => true) = ENNReal.ofReal (1/16 : ℝ) := by norm_num [weight]
example : (distribution 2 (1/4) (by norm_num) (by norm_num)).toOuterMeasure
    {word | ¬ Accepted (1/4) (1/4) (if word 0 then 0 else 1)} = 1 := by
  rw [failure_probability]
  have h : ∀ word : Fin 2 → Bool,
      failureIndicator (1/4) (if word 0 then 0 else 1) (1/4) = 1 := by
    intro word
    split <;> norm_num [failureIndicator,Accepted,D0,D1]
  simp_rw [h,mul_one]
  exact sum_weight 2 (by norm_num) (by norm_num)

#print axioms AnnularLiteral.left_width
#print axioms AnnularLiteral.right_width
#print axioms AnnularLiteral.left_annular_lower
#print axioms AnnularLiteral.right_annular_lower
#print axioms AnnularLiteral.left_growth_weighted_lower
#print axioms AnnularLiteral.right_growth_weighted_lower
#print axioms AnnularLiteral.zero_prefix_lower
#print axioms AnnularLiteral.seed_averaged_two_prefix_growth_lower
#print axioms BernoulliWord.sum_weight
#print axioms BernoulliWord.failure_probability
#print axioms BernoulliWord.all_reports_growth_lower
#print BernoulliWord.all_reports_growth_lower

#print axioms GrowthMoment.exists_cutoff
#print axioms GrowthMoment.finite_tail_risk_implies_inverse_moment
#print axioms GrowthMoment.finite_risk_implies_inverse_moment
#print GrowthMoment.finite_risk_implies_inverse_moment

#print axioms GrowthMoment.lowerGrowth_of_separate
#print axioms BayesBridge.productRisk_eq_bayesRisk
#print axioms BayesBridge.bayesRisk_eq_risk
#print axioms BayesBridge.finite_product_risk_implies_inverse_moment
#print BayesBridge.finite_product_risk_implies_inverse_moment
