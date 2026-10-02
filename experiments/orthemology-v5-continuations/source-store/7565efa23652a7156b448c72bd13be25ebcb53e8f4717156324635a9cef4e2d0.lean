import AnnularLiteral

namespace BernoulliWord
noncomputable section
open MeasureTheory Set AnnularLiteral
open scoped ENNReal

def weight (n : ℕ) (a : ℝ) (word : Fin n → Bool) : ℝ≥0∞ :=
  ENNReal.ofReal (∏ i, if word i then a else 1-a)

@[simp] lemma weight_zero (n : ℕ) (a : ℝ) :
    weight n a (fun _ => false) = ENNReal.ofReal ((1-a)^n) := by simp [weight]

@[simp] lemma weight_one (n : ℕ) (a : ℝ) :
    weight n a (fun _ => true) = ENNReal.ofReal (a^n) := by simp [weight]

lemma weight_prod (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1) (word : Fin n → Bool) :
    weight n a word = ∏ i, if word i then ENNReal.ofReal a else ENNReal.ofReal (1-a) := by
  unfold weight
  rw [ENNReal.ofReal_prod_of_nonneg (by intro i hi; split <;> linarith)]
  apply Finset.prod_congr rfl
  intro i hi
  split <;> rfl

lemma sum_weight (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1) :
    ∑ word : Fin n → Bool, weight n a word = 1 := by
  simp_rw [weight_prod n ha ha1]
  rw [← Fintype.prod_sum (fun (_i : Fin n) (b : Bool) =>
    if b then ENNReal.ofReal a else ENNReal.ofReal (1-a))]
  have hab : ENNReal.ofReal (1-a) + ENNReal.ofReal a = 1 := by
    rw [← ENNReal.ofReal_add (by linarith) ha]
    norm_num
  have hab' : ENNReal.ofReal a + ENNReal.ofReal (1-a) = 1 := by simpa [add_comm] using hab
  simp [hab']

/-- This is an actual Mathlib PMF on length-n Boolean words. -/
def distribution (n : ℕ) (a : ℝ) (ha : 0≤a) (ha1 : a≤1) : PMF (Fin n → Bool) :=
  PMF.ofFintype (weight n a) (sum_weight n ha ha1)

@[simp] lemma distribution_apply (n : ℕ) (a : ℝ) (ha : 0≤a) (ha1 : a≤1)
    (word : Fin n → Bool) : distribution n a ha ha1 word = weight n a word := rfl

/-- The mass formula agrees with the event probability of the actual finite-word PMF. -/
lemma failure_probability (n : ℕ) (a : ℝ) (ha : 0≤a) (ha1 : a≤1)
    (e : ℝ) (report : (Fin n → Bool) → ℝ) :
    (distribution n a ha ha1).toOuterMeasure {word | ¬ Accepted a e (report word)} =
      ∑ word, weight n a word * failureIndicator e (report word) a := by
  classical
  rw [PMF.toOuterMeasure_apply_fintype]
  apply Finset.sum_congr rfl
  intro word hword
  by_cases h : Accepted a e (report word)
  · simp [h, failureIndicator]
  · simp [h, failureIndicator, distribution_apply]

/-- Finite-word error mass, integrating the independent seed and parameter prior.
The displayed word weights form a probability distribution for every a in [0,1]. -/
def risk {Z : Type*} [MeasurableSpace Z] (n : ℕ) (μ : Measure ℝ)
    (ν : Measure Z) (e : ℝ) (report : (Fin n → Bool) → Z → ℝ) : ℝ≥0∞ :=
  ∑ word, ∫⁻ z, weightedFailure μ (fun a => weight n a word) e (report word z) ∂ν

lemma two_prefix_le_risk {Z : Type*} [MeasurableSpace Z]
    (n : ℕ) (hn : 0<n) (μ : Measure ℝ) (ν : Measure Z) (e : ℝ)
    (report : (Fin n → Bool) → Z → ℝ) :
    (∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal ((1-a)^n)) e
      (report (fun _ => false) z) ∂ν) +
    (∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal (a^n)) e
      (report (fun _ => true) z) ∂ν) ≤ risk n μ ν e report := by
  have hne : (fun _ : Fin n => false) ≠ (fun _ : Fin n => true) := by
    intro h
    have := congrFun h ⟨0,hn⟩
    contradiction
  have h := Finset.sum_le_sum_of_subset (f := fun word : Fin n → Bool =>
      ∫⁻ z, weightedFailure μ (fun a => weight n a word) e (report word z) ∂ν)
      (s := {(fun _ => false),(fun _ => true)}) (Finset.subset_univ _)
  simpa [Finset.sum_pair hne, risk] using h

/-- Every report based on the complete finite Boolean word and arbitrary independent
random seed satisfies the lower-growth endpoint risk lower bound. -/
theorem all_reports_growth_lower {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν]
    (μ : Measure ℝ) [IsFiniteMeasure μ] (e x : ℝ) (η0 η1 : ℝ≥0∞)
    (n : ℕ) (hn : 0<n) (report : (Fin n → Bool) → Z → ℝ)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx16 : x≤1/16)
    (hnx : (n:ℝ)*x≤1)
    (hg0 : (1+η0)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x)))
    (hg04 : (1+η0)*μ (Ioc 0 (4*x)) ≤ μ (Ioc 0 (8*x)))
    (hg1 : (1+η1)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1))
    (hg14 : (1+η1)*μ (Ico (1-4*x) 1) ≤ μ (Ico (1-8*x) 1)) :
    ENNReal.ofReal (Real.exp (-16)) *
      (η0*μ (Ioc 0 x) + η1*μ (Ico (1-x) 1)) ≤ risk n μ ν e report :=
  (seed_averaged_two_prefix_growth_lower ν (report (fun _ => false))
    (report (fun _ => true)) μ e x η0 η1 n he he4 hx hx16 hnx hg0 hg04 hg1 hg14).trans
    (two_prefix_le_risk n hn μ ν e report)

end
end BernoulliWord
