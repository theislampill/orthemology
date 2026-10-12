import PriorSufficiency

namespace EndpointIndependentReview
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge
open GrowthMoment EmpiricalGeometry EmpiricalChernoff EmpiricalEndpoints PriorSufficiency
open scoped ENNReal

def rawRisk {Z : Type*} [MeasurableSpace Z] (n : ℕ) (μ : Measure ℝ)
    (ν : Measure Z) (e : ℝ) (r : (Fin n → Bool) → Z → ℝ) : ℝ≥0∞ := by
  classical
  exact ∫⁻ p : ℝ × Z, ∑ w : Fin n → Bool,
    ENNReal.ofReal (∏ i, if w i then p.1 else 1-p.1) *
      (if (r w p.2)^2-1/4-p.1*e*(1+e)≤0 ∧
          (1-r w p.2)^2-1/4+p.1*e*(1-e)≤0 then (0:ℝ≥0∞) else 1) ∂μ.prod ν

lemma rawRisk_eq {Z : Type*} [MeasurableSpace Z] (n : ℕ) (μ : Measure ℝ)
    (ν : Measure Z) (e : ℝ) (r : (Fin n → Bool) → Z → ℝ) :
    rawRisk n μ ν e r = productRisk n μ ν e r := by
  classical
  unfold rawRisk productRisk weight failureIndicator Accepted D0 D1
  apply lintegral_congr
  intro p
  apply Finset.sum_congr rfl
  intro w hw
  split_ifs <;> rfl

theorem raw_finite_prefix_iff {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) :
    (∃ r : (n : ℕ) → (Fin n → Bool) → Z → ℝ,
      (∀ n w, Measurable (r n w)) ∧
      (∑' t : ℕ, rawRisk (t+1) μ ν e (r (t+1))) < ⊤) ↔
    (∫⁻ a, ENNReal.ofReal ((a*(1-a))⁻¹) ∂μ.restrict (Ioo 0 1)) < ⊤ := by
  simp_rw [rawRisk_eq]
  exact exists_seeded_report_family_iff ν μ e x0 η hη hx0 he he4 hg hs

theorem all_policy_divergence {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (r : (n : ℕ) → (Fin n → Bool) → Z → ℝ)
    (hr : ∀ n w, Measurable (r n w)) (hm : inverseVarianceMoment μ = ⊤) :
    (∑' t : ℕ, productRisk (t+1) μ ν e (r (t+1))) = ⊤ := by
  by_contra h
  have hf := finite_product_risk_implies_inverse_moment ν μ e x0 η hη hx0 he he4 hg r hr (lt_top_iff_ne_top.mpr h)
  simpa [hm] using hf

lemma empiricalMean_unit (n : ℕ) (hn : 0<n) (w : Fin n → Bool) :
    0≤empiricalMean n w ∧ empiricalMean n w≤1 := by
  have hn' : (0:ℝ)<n := by exact_mod_cast hn
  have h0 : 0≤∑ i : Fin n, if w i then (1:ℝ) else 0 := by
    apply Finset.sum_nonneg
    intro i hi
    split <;> norm_num
  have h1 : (∑ i : Fin n, if w i then (1:ℝ) else 0)≤(n:ℝ) := by
    calc
      _ ≤ ∑ _i : Fin n, (1:ℝ) := by
        apply Finset.sum_le_sum
        intro i hi
        split <;> norm_num
      _ = _ := by simp
  constructor
  · exact div_nonneg h0 hn'.le
  · exact (div_le_one hn').mpr h1

theorem empirical_report_coherent (n : ℕ) (hn : 0<n) (e : ℝ)
    (he : 0<e) (he4 : e≤1/4) (w : Fin n → Bool) :
    0≤empiricalReport n e w ∧ empiricalReport n e w≤1 := by
  obtain ⟨h0,h1⟩ := empiricalMean_unit n hn w
  unfold empiricalReport
  constructor <;> nlinarith

theorem endpoint_mixture_zero {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (A B : ℝ≥0∞) (e : ℝ) (n : ℕ) :
    productRisk (n+1) (A • Measure.dirac 0 + B • Measure.dirac 1) ν e
      (fun w _ => empiricalReport (n+1) e w) = 0 := by
  rw [empirical_productRisk_eq,lintegral_add_measure]
  simp [error_at_zero,error_at_one (n+1) (by omega) e]

theorem endpoint_mixture_moment_zero (A B : ℝ≥0∞) :
    inverseVarianceMoment (A • Measure.dirac 0 + B • Measure.dirac 1) = 0 := by
  have h := interior_add_endpoint_atoms (0 : Measure ℝ) A B
  simp only [zero_add] at h
  unfold inverseVarianceMoment
  rw [h]
  simp [EndpointMoment.interior]

theorem single_risk_le_mass {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (n : ℕ) (e : ℝ)
    (r : (Fin n → Bool) → Z → ℝ) (hr : ∀ w, Measurable (r w))
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) : productRisk n μ ν e r≤μ univ := by
  rw [productRisk_eq_bayesRisk _ _ _ _ _ hr]
  unfold bayesRisk
  calc
    _ ≤ ∫⁻ _a : ℝ, (1:ℝ≥0∞) ∂μ := by
      apply lintegral_mono_ae
      filter_upwards [hs] with a ha
      calc
        _ ≤ ∫⁻ _z : Z, (1:ℝ≥0∞) ∂ν := by
          apply lintegral_mono
          intro z
          calc
            _ ≤ ∑ w : Fin n → Bool, weight n a w := by
              apply Finset.sum_le_sum
              intro w hw
              unfold failureIndicator
              split <;> simp
            _ = 1 := sum_weight n ha.1 ha.2
        _ = 1 := by simp
    _ = μ univ := by simp

theorem finite_prefix_tail_equivalence {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e : ℝ) (r : (n : ℕ) → (Fin n → Bool) → Z → ℝ)
    (hr : ∀ n w, Measurable (r n w)) (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (N : ℕ) :
    ((∑' t, productRisk (t+N+1) μ ν e (r (t+N+1))) < ⊤) ↔
    ((∑' t, productRisk (t+1) μ ν e (r (t+1))) < ⊤) := by
  have hsplit : (∑ t ∈ Finset.range N, productRisk (t+1) μ ν e (r (t+1))) +
      (∑' t, productRisk (t+N+1) μ ν e (r (t+N+1))) =
      ∑' t, productRisk (t+1) μ ν e (r (t+1)) :=
    ENNReal.summable.sum_add_tsum_nat_add'
  have hf : (∑ t ∈ Finset.range N, productRisk (t+1) μ ν e (r (t+1))) < ⊤ := by
    apply ENNReal.sum_lt_top.mpr
    intro t ht
    exact (single_risk_le_mass ν μ (t+1) e _ (hr (t+1)) hs).trans_lt (measure_lt_top μ univ)
  rw [← hsplit,ENNReal.add_lt_top]
  exact ⟨fun h => ⟨hf,h⟩,fun h => h.2⟩

theorem one_step_word_consistency (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (w : Fin n → Bool) :
    weight (n+1) a (Fin.cons false w) + weight (n+1) a (Fin.cons true w) = weight n a w := by
  rw [weight_prod _ ha ha1,weight_prod _ ha ha1,weight_prod _ ha ha1]
  simp only [Fin.prod_univ_succ,Fin.cons_zero,Fin.cons_succ,Bool.false_eq_true,↓reduceIte]
  rw [← add_mul,← ENNReal.ofReal_add (by linarith : 0≤1-a) ha]
  simp

#print axioms raw_finite_prefix_iff
#print axioms all_policy_divergence
#print axioms empirical_report_coherent
#print axioms endpoint_mixture_zero
#print axioms endpoint_mixture_moment_zero
#print axioms single_risk_le_mass
#print axioms finite_prefix_tail_equivalence
#print axioms one_step_word_consistency
end
end EndpointIndependentReview
