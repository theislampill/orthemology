import AdaptiveLikelihood

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped Topology

namespace Orthemology.Tranche2

variable {A Y Ω : Type*} [Fintype A]

def prefixLikelihood (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (N : A → ℕ) (ω : Ω) : ℝ :=
  ∏ a, ∏ i ∈ Finset.range (N a), p a (X a i ω)

lemma prefixLikelihood_pos (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (N : A → ℕ) (ω : Ω) :
    0 < prefixLikelihood p X N ω := by
  apply Finset.prod_pos
  intro a _
  exact Finset.prod_pos (fun i _ => hp a (X a i ω))

lemma log_prefixLikelihood (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (N : A → ℕ) (ω : Ω) :
    Real.log (prefixLikelihood p X N ω) =
      ∑ a, ∑ i ∈ Finset.range (N a), Real.log (p a (X a i ω)) := by
  unfold prefixLikelihood
  rw [Real.log_prod _ _ (fun a _ => ne_of_gt
    (Finset.prod_pos (fun i _ => hp a (X a i ω))))]
  apply Finset.sum_congr rfl
  intro a _
  exact Real.log_prod _ _ (fun i _ => ne_of_gt (hp a (X a i ω)))

lemma log_prefixLikelihood_ratio (p q : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (hq : ∀ a y, 0 < q a y) (N : A → ℕ) (ω : Ω) :
    Real.log (prefixLikelihood p X N ω / prefixLikelihood q X N ω) =
      ∑ a, ∑ i ∈ Finset.range (N a), logScore (p a) (q a) (X a i ω) := by
  rw [Real.log_div (ne_of_gt (prefixLikelihood_pos p X hp N ω))
    (ne_of_gt (prefixLikelihood_pos q X hq N ω)),
    log_prefixLikelihood p X hp N ω, log_prefixLikelihood q X hq N ω]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro a _
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  exact (Real.log_div (ne_of_gt (hp a (X a i ω)))
    (ne_of_gt (hq a (X a i ω)))).symm

lemma inverse_prefixLikelihood_ratio (p q : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (hq : ∀ a y, 0 < q a y) (N : A → ℕ) (ω : Ω) :
    prefixLikelihood q X N ω / prefixLikelihood p X N ω =
      Real.exp (-(∑ a, ∑ i ∈ Finset.range (N a),
        logScore (p a) (q a) (X a i ω))) := by
  have hpos := div_pos (prefixLikelihood_pos p X hp N ω)
    (prefixLikelihood_pos q X hq N ω)
  rw [← log_prefixLikelihood_ratio p q X hp hq N ω, Real.exp_neg, Real.exp_log hpos]
  simp only [inv_div]

section Probability
variable [Fintype Y]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]

/-- Exact finite products, not an unnamed score, reject every candidate exposed
by an infinitely sampled informative action on the common iid-stack event. -/
theorem sampled_false_likelihood_ratio_tendsto_zero (p q : A → Y → ℝ)
    (X : A → ℕ → Ω → Y)
    (hp : ∀ a y, 0 < p a y) (hq : ∀ a y, 0 < q a y)
    (hpsum : ∀ a, ∑ y, p a y = 1) (hqsum : ∀ a, ∑ y, q a y = 1)
    (hX : ∀ a n, Measurable (X a n))
    (hindep : iIndepFun (fun an : A × ℕ => X an.1 an.2) μ)
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = p a y) :
    ∀ᵐ ω ∂μ, ∀ N : A → ℕ → ℕ,
      (∃ a, p a ≠ q a ∧ Tendsto (N a) atTop atTop) →
      Tendsto (fun t => prefixLikelihood q X (fun a => N a t) ω /
        prefixLikelihood p X (fun a => N a t) ω) atTop (𝓝 0) := by
  filter_upwards [sampled_logScore_tendsto_of_joint_independent
    p q X hp hq hpsum hqsum hX hindep hident hLaw] with ω hω
  intro N hinfo
  have ht := hω N hinfo
  have hneg := tendsto_neg_atTop_atBot.comp ht
  have hexp := Real.tendsto_exp_atBot.comp hneg
  simpa only [inverse_prefixLikelihood_ratio p q X hp hq] using hexp

end Probability
end Orthemology.Tranche2
