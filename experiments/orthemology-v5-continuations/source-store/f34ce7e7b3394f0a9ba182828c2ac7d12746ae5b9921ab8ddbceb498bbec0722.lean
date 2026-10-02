import ExponentialSeries

namespace EmpiricalEndpoints
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge CentredBernoulli EmpiricalGeometry EmpiricalChernoff ExponentialSeries
open scoped ENNReal

lemma weight_at_zero (n : ℕ) (word : Fin n → Bool) :
    weight n 0 word = if word=(fun _ => false) then 1 else 0 := by
  classical
  by_cases h : word=(fun _ => false)
  · simp [h]
  · have hi : ∃ i, word i=true := by
      by_contra hh
      apply h
      funext i
      cases hw : word i
      · rfl
      · exact False.elim (hh ⟨i,hw⟩)
    obtain ⟨i,hi⟩ := hi
    have hp : (∏ j : Fin n, if word j then (0:ℝ) else 1-0)=0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) (by simp [hi])
    simp only [weight,hp,ENNReal.ofReal_zero,if_neg h]

lemma weight_at_one (n : ℕ) (word : Fin n → Bool) :
    weight n 1 word = if word=(fun _ => true) then 1 else 0 := by
  classical
  by_cases h : word=(fun _ => true)
  · simp [h]
  · have hi : ∃ i, word i=false := by
      by_contra hh
      apply h
      funext i
      cases hw : word i
      · exact False.elim (hh ⟨i,hw⟩)
      · rfl
    obtain ⟨i,hi⟩ := hi
    have hp : (∏ j : Fin n, if word j then (1:ℝ) else 1-1)=0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) (by simp [hi])
    simp only [weight,hp,ENNReal.ofReal_zero,if_neg h]

lemma error_at_zero (n : ℕ) (e : ℝ) : error n 0 e=0 := by
  classical
  unfold error
  simp_rw [weight_at_zero]
  apply Finset.sum_eq_zero
  intro word hword
  by_cases h : word=(fun _ => false)
  · subst word
    norm_num [empiricalReport,empiricalMean,failureIndicator,Accepted,D0,D1]
  · simp [h]

lemma error_at_one (n : ℕ) (hn : 0<n) (e : ℝ) : error n 1 e=0 := by
  classical
  have hn0 : (n:ℝ)≠0 := by exact_mod_cast (ne_of_gt hn)
  have hacc : Accepted 1 e (1/2+e) := by
    constructor <;> dsimp [D0,D1] <;> nlinarith
  unfold error
  simp_rw [weight_at_one]
  apply Finset.sum_eq_zero
  intro word hword
  by_cases h : word=(fun _ => true)
  · subst word
    simp [empiricalReport,empiricalMean,hn0,failureIndicator]
    convert hacc using 1 <;> norm_num
  · simp [h]

end
end EmpiricalEndpoints
