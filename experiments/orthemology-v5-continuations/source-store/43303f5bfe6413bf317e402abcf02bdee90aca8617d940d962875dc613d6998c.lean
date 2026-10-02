import EndpointProcess

/-! Endpoint-atom necessity without lower-growth assumptions. This is a separate
author supplement. All accepted dependency bytes remain unchanged. -/
namespace EndpointAtoms
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge
open EmpiricalGeometry PriorSufficiency EndpointProcess
open scoped ENNReal

lemma accepted_zero_iff {e q : ℝ} (he : 0<e) (he4 : e≤1/4) :
    Accepted 0 e q ↔ q=1/2 := by
  constructor
  · intro h
    have hq := accepted_range (by norm_num) (by norm_num) he he4 h
    have hh := h.1
    dsimp [D0] at hh
    nlinarith [hq.1]
  · intro h
    subst q
    norm_num [Accepted,D0,D1]

lemma accepted_one_iff {e q : ℝ} (he : 0<e) (he4 : e≤1/4) :
    Accepted 1 e q ↔ q=1/2+e := by
  constructor
  · intro h
    have hq := accepted_range (by norm_num) (by norm_num) he he4 h
    have hh := h.2
    dsimp [D1] at hh
    have hp := mul_nonneg (show 0≤1/2+e-q by linarith [hq.2])
      (show 0≤1-2*e by linarith)
    nlinarith [hq.2]
  · intro h
    subst q
    constructor <;> dsimp [D0,D1] <;> nlinarith

lemma zero_interior_separation {a e q : ℝ} (ha : 0<a)
    (he : 0<e) (he4 : e≤1/4) : ¬ (Accepted 0 e q ∧ Accepted a e q) := by
  rintro ⟨h0,haq⟩
  rw [(accepted_zero_iff he he4).mp h0] at haq
  have he1 : 0<1-e := by linarith
  have hp : 0<a*e*(1-e) := by positivity
  have hh := haq.2
  dsimp [D1] at hh
  nlinarith

lemma one_interior_separation {a e q : ℝ} (ha : a<1)
    (he : 0<e) (he4 : e≤1/4) : ¬ (Accepted 1 e q ∧ Accepted a e q) := by
  rintro ⟨h1,haq⟩
  rw [(accepted_one_iff he he4).mp h1] at haq
  have ha1 : 0<1-a := by linarith
  have hp : 0<(1-a)*e*(1+e) := by positivity
  have hh := haq.1
  dsimp [D0] at hh
  nlinarith

def lowerConstant : ℝ≥0∞ := ENNReal.ofReal (Real.exp (-16))

lemma lowerConstant_pos : 0<lowerConstant := by
  exact ENNReal.ofReal_pos.mpr (Real.exp_pos _)

lemma lowerConstant_le_one : lowerConstant≤1 := by
  have h : Real.exp (-16)≤1 := by
    simpa using (Real.exp_le_exp.mpr (by norm_num : (-16:ℝ)≤0))
  simpa [lowerConstant] using ENNReal.ofReal_le_ofReal h

/-- An endpoint atom and the entire punctured left interval are incompatible
for one report; the extreme-prefix likelihood lower bound is uniform. -/
theorem zero_prefix_atom_lower (μ : Measure ℝ) (e q x : ℝ) (n : ℕ)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx2 : x≤1/2)
    (hnx : (n:ℝ)*x≤1) :
    lowerConstant * min (μ {0}) (μ (Ioc 0 x)) ≤
      weightedFailure μ (fun a => ENNReal.ofReal ((1-a)^n)) e q := by
  apply weightedFailure_lower_two_sets μ _ e q lowerConstant {0} (Ioc 0 x)
    (measurableSet_singleton 0) measurableSet_Ioc
  · intro a ha b hb
    have ha0 : a=0 := ha
    subst a
    exact zero_interior_separation hb.1 he he4
  · intro a ha
    rcases ha with ha|ha
    · have ha0 : a=0 := ha
      subst a
      simpa using lowerConstant_le_one
    · apply ENNReal.ofReal_le_ofReal
      apply zero_prefix_lower ha.1.le (ha.2.trans hx2) n
      have h := mul_le_mul_of_nonneg_left ha.2 (Nat.cast_nonneg n : (0:ℝ)≤n)
      linarith

/-- The right endpoint uses its exact asymmetric accepted report, with the
all-one likelihood. No epsilon reflection is assumed. -/
theorem one_prefix_atom_lower (μ : Measure ℝ) (e q x : ℝ) (n : ℕ)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx2 : x≤1/2)
    (hnx : (n:ℝ)*x≤1) :
    lowerConstant * min (μ {1}) (μ (Ico (1-x) 1)) ≤
      weightedFailure μ (fun a => ENNReal.ofReal (a^n)) e q := by
  apply weightedFailure_lower_two_sets μ _ e q lowerConstant {1} (Ico (1-x) 1)
    (measurableSet_singleton 1) measurableSet_Ico
  · intro a ha b hb
    have ha1 : a=1 := ha
    subst a
    exact one_interior_separation hb.2 he he4
  · intro a ha
    rcases ha with ha|ha
    · have ha1 : a=1 := ha
      subst a
      simpa using lowerConstant_le_one
    · have hb : 0≤1-a := by linarith [ha.2]
      have hbx : 1-a≤x := by linarith [ha.1]
      have hn := mul_le_mul_of_nonneg_left hbx (Nat.cast_nonneg n : (0:ℝ)≤n)
      have h := zero_prefix_lower hb (hbx.trans hx2) n (by linarith)
      apply ENNReal.ofReal_le_ofReal
      simpa using h

lemma reciprocal_scale (t : ℕ) :
    0<((t+2:ℕ):ℝ)⁻¹ ∧ ((t+2:ℕ):ℝ)⁻¹≤1/2 ∧
      ((t+2:ℕ):ℝ)*((t+2:ℕ):ℝ)⁻¹≤1 := by
  have hp : (0:ℝ)<((t+2:ℕ):ℝ) := by positivity
  refine ⟨inv_pos.mpr hp,?_,?_⟩
  · have h : (2:ℝ)≤((t+2:ℕ):ℝ) := by exact_mod_cast (show 2≤t+2 by omega)
    simpa using (inv_le_inv₀ hp (by norm_num : (0:ℝ)<2)).mpr h
  · rw [mul_inv_cancel₀ (ne_of_gt hp)]

lemma fixed_word_le_risk {Z : Type*} [MeasurableSpace Z]
    (n : ℕ) (μ : Measure ℝ) (ν : Measure Z) (e : ℝ)
    (r : (Fin n → Bool) → Z → ℝ) (w : Fin n → Bool) :
    (∫⁻ z, weightedFailure μ (fun a => weight n a w) e (r w z) ∂ν) ≤
      risk n μ ν e r := by
  unfold risk
  exact Finset.single_le_sum (f := fun w : Fin n → Bool =>
    ∫⁻ z, weightedFailure μ (fun a => weight n a w) e (r w z) ∂ν)
    (fun _ _ => bot_le) (Finset.mem_univ w)

theorem left_atom_profile_lower {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (e : ℝ)
    (he : 0<e) (he4 : e≤1/4) (t : ℕ)
    (r : (Fin (t+2) → Bool) → Z → ℝ) :
    lowerConstant * min (μ {0}) (leftMass μ (t+1)) ≤ risk (t+2) μ ν e r := by
  obtain ⟨hx,hx2,hnx⟩ := reciprocal_scale t
  rw [leftMass_eq_Ioc μ (t+1) (by omega)]
  have h : lowerConstant * min (μ {0}) (μ (Ioc 0 (((t+2:ℕ):ℝ)⁻¹))) ≤
      ∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal ((1-a)^(t+2))) e (r (fun _ => false) z) ∂ν := by
    calc
      _ = ∫⁻ _z : Z, lowerConstant * min (μ {0}) (μ (Ioc 0 (((t+2:ℕ):ℝ)⁻¹))) ∂ν := by simp
      _ ≤ _ := lintegral_mono (fun z => zero_prefix_atom_lower μ e (r (fun _ => false) z) _ (t+2) he he4 hx hx2 hnx)
  have hs := fixed_word_le_risk (t+2) μ ν e r (fun _ => false)
  simp only [weight_zero] at hs
  simpa only [Nat.add_assoc] using h.trans hs

theorem right_atom_profile_lower {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (e : ℝ)
    (he : 0<e) (he4 : e≤1/4) (t : ℕ)
    (r : (Fin (t+2) → Bool) → Z → ℝ) :
    lowerConstant * min (μ {1}) (rightMass μ (t+1)) ≤ risk (t+2) μ ν e r := by
  obtain ⟨hx,hx2,hnx⟩ := reciprocal_scale t
  rw [rightMass_eq_Ico μ (t+1) (by omega)]
  have h : lowerConstant * min (μ {1}) (μ (Ico (1-(((t+2:ℕ):ℝ)⁻¹)) 1)) ≤
      ∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal (a^(t+2))) e (r (fun _ => true) z) ∂ν := by
    calc
      _ = ∫⁻ _z : Z, lowerConstant * min (μ {1}) (μ (Ico (1-(((t+2:ℕ):ℝ)⁻¹)) 1)) ∂ν := by simp
      _ ≤ _ := lintegral_mono (fun z => one_prefix_atom_lower μ e (r (fun _ => true) z) _ (t+2) he he4 hx hx2 hnx)
  have hs := fixed_word_le_risk (t+2) μ ν e r (fun _ => true)
  simp only [weight_one] at hs
  simpa only [Nat.add_assoc] using h.trans hs

lemma atom_profile_product_le {A F M : ℝ≥0∞} (hA : A≤M) (hF : F≤M) :
    A*F≤M*min A F := by
  rcases le_total A F with h|h
  · rw [min_eq_left h]
    exact (mul_le_mul_left' hF A).trans_eq (mul_comm A M)
  · rw [min_eq_right h]
    exact mul_le_mul_right' hA F

/-- The finite total mass absorbs the minimum without division or any
continuity-of-mass or eventual-truncation premise. -/
theorem left_atom_mass_lower {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (e : ℝ)
    (he : 0<e) (he4 : e≤1/4) (t : ℕ)
    (r : (Fin (t+2) → Bool) → Z → ℝ) :
    (lowerConstant*μ {0}) * leftMass μ (t+1) ≤ μ univ * risk (t+2) μ ν e r := by
  have hA : μ {0}≤μ univ := measure_mono (subset_univ _)
  have hF : leftMass μ (t+1)≤μ univ := by
    rw [leftMass_eq_Ioc μ (t+1) (by omega)]
    exact measure_mono (subset_univ _)
  calc
    _ = lowerConstant*(μ {0}*leftMass μ (t+1)) := mul_assoc _ _ _
    _ ≤ lowerConstant*(μ univ*min (μ {0}) (leftMass μ (t+1))) :=
      mul_le_mul_left' (atom_profile_product_le hA hF) _
    _ = μ univ*(lowerConstant*min (μ {0}) (leftMass μ (t+1))) := by ac_rfl
    _ ≤ _ := mul_le_mul_left' (left_atom_profile_lower ν μ e he he4 t r) _

theorem right_atom_mass_lower {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) (e : ℝ)
    (he : 0<e) (he4 : e≤1/4) (t : ℕ)
    (r : (Fin (t+2) → Bool) → Z → ℝ) :
    (lowerConstant*μ {1}) * rightMass μ (t+1) ≤ μ univ * risk (t+2) μ ν e r := by
  have hA : μ {1}≤μ univ := measure_mono (subset_univ _)
  have hF : rightMass μ (t+1)≤μ univ := by
    rw [rightMass_eq_Ico μ (t+1) (by omega)]
    exact measure_mono (subset_univ _)
  calc
    _ = lowerConstant*(μ {1}*rightMass μ (t+1)) := mul_assoc _ _ _
    _ ≤ lowerConstant*(μ univ*min (μ {1}) (rightMass μ (t+1))) :=
      mul_le_mul_left' (atom_profile_product_le hA hF) _
    _ = μ univ*(lowerConstant*min (μ {1}) (rightMass μ (t+1))) := by ac_rfl
    _ ≤ _ := mul_le_mul_left' (right_atom_profile_lower ν μ e he he4 t r) _

lemma shifted_risk_finite {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) (μ : Measure ℝ) (e : ℝ) (r : ReportFamily Z)
    (hf : (∑' t : ℕ, risk (t+1) μ ν e (r (t+1)))<⊤) :
    (∑' t : ℕ, risk (t+2) μ ν e (r (t+2)))<⊤ := by
  have hsplit : (∑ t ∈ Finset.range 1, risk (t+1) μ ν e (r (t+1))) +
      (∑' t, risk (t+1+1) μ ν e (r (t+1+1))) =
      ∑' t, risk (t+1) μ ν e (r (t+1)) :=
    ENNReal.summable.sum_add_tsum_nat_add'
  have ht : (∑' t, risk (t+1+1) μ ν e (r (t+1+1)))<⊤ :=
    lt_of_le_of_lt (by rw [← hsplit];exact le_add_self) hf
  simpa only [Nat.add_assoc] using ht

/-- A positive left endpoint atom forces the actual interior left inverse
moment to be finite whenever any full-word randomized policy has finite risk. -/
theorem finite_risk_implies_left_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e : ℝ) (he : 0<e) (he4 : e≤1/4) (h0 : 0<μ {0}) (r : ReportFamily Z)
    (hf : (∑' t : ℕ, risk (t+1) μ ν e (r (t+1)))<⊤) : leftMoment μ<⊤ := by
  have ht := shifted_risk_finite ν μ e r hf
  have hsum : (lowerConstant*μ {0})*(∑' t : ℕ, leftMass μ (t+1)) ≤
      μ univ*(∑' t : ℕ, risk (t+2) μ ν e (r (t+2))) := by
    rw [← ENNReal.tsum_mul_left,← ENNReal.tsum_mul_left]
    exact ENNReal.tsum_le_tsum (fun t => left_atom_mass_lower ν μ e he he4 t (r (t+2)))
  have hprof : (∑' t : ℕ, leftMass μ (t+1))<⊤ :=
    ENNReal.lt_top_of_mul_ne_top_right
      (ne_of_lt (hsum.trans_lt (ENNReal.mul_lt_top (measure_lt_top μ univ) ht)))
      (mul_ne_zero (ne_of_gt lowerConstant_pos) (ne_of_gt h0))
  exact (tsum_profile_tail_lt_top_iff (interior μ) id measurable_id (ae_left_distance μ) 1).mp hprof

theorem finite_risk_implies_right_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e : ℝ) (he : 0<e) (he4 : e≤1/4) (h1 : 0<μ {1}) (r : ReportFamily Z)
    (hf : (∑' t : ℕ, risk (t+1) μ ν e (r (t+1)))<⊤) : rightMoment μ<⊤ := by
  have ht := shifted_risk_finite ν μ e r hf
  have hsum : (lowerConstant*μ {1})*(∑' t : ℕ, rightMass μ (t+1)) ≤
      μ univ*(∑' t : ℕ, risk (t+2) μ ν e (r (t+2))) := by
    rw [← ENNReal.tsum_mul_left,← ENNReal.tsum_mul_left]
    exact ENNReal.tsum_le_tsum (fun t => right_atom_mass_lower ν μ e he he4 t (r (t+2)))
  have hprof : (∑' t : ℕ, rightMass μ (t+1))<⊤ :=
    ENNReal.lt_top_of_mul_ne_top_right
      (ne_of_lt (hsum.trans_lt (ENNReal.mul_lt_top (measure_lt_top μ univ) ht)))
      (mul_ne_zero (ne_of_gt lowerConstant_pos) (ne_of_gt h1))
  exact (tsum_profile_tail_lt_top_iff (interior μ) (fun x => 1-x)
    (by fun_prop) (ae_right_distance μ) 1).mp hprof

lemma risk_series_eq_product {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e : ℝ) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (∑' t : ℕ, risk (t+1) μ ν e (r (t+1)))=
      ∑' t : ℕ, productRisk (t+1) μ ν e (r (t+1)) := by
  apply tsum_congr
  intro t
  rw [productRisk_eq_bayesRisk _ _ _ _ _ (hr (t+1)),bayesRisk_eq_risk _ _ _ _ _ (hr (t+1))]

theorem finite_actual_implies_left_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (h0 : 0<μ {0}) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w))
    (hf : (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν)<⊤) : leftMoment μ<⊤ := by
  apply finite_risk_implies_left_moment ν μ e he he4 h0 r
  rwa [risk_series_eq_product ν μ e r hr,← actual_expectation_eq_risk_series μ ν hs e r hr]

theorem finite_actual_implies_right_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (h1 : 0<μ {1}) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w))
    (hf : (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν)<⊤) : rightMoment μ<⊤ := by
  apply finite_risk_implies_right_moment ν μ e he he4 h1 r
  rwa [risk_series_eq_product ν μ e r hr,← actual_expectation_eq_risk_series μ ν hs e r hr]

/-- With both endpoint atoms positive, the complete actual-process moment iff
holds without any lower growth, density or atomlessness assumption. -/
theorem both_atoms_coherent_actual_iff {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (h0 : 0<μ {0}) (h1 : 0<μ {1}) :
    (∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n, 0<n → ∀ w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν)<⊤) ↔ inverseVarianceMoment μ<⊤ := by
  constructor
  · rintro ⟨r,hr,hcoh,hf⟩
    rw [inverseVarianceMoment_eq,ENNReal.add_lt_top]
    exact ⟨finite_actual_implies_left_moment ν μ hs e he he4 h0 r hr hf,
      finite_actual_implies_right_moment ν μ hs e he he4 h1 r hr hf⟩
  · intro hm
    refine ⟨(fun n w _ => empiricalReport n e w),(fun n w => measurable_const),?_,?_⟩
    · intro n hn w z
      exact EndpointProcess.empirical_report_coherent n hn e he he4 w
    · exact (empirical_actual_expectation_bound μ ν hs e he he4).trans_lt
        (ENNReal.mul_lt_top ENNReal.ofReal_lt_top hm)

theorem left_atom_infinite_of_infinite_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (h0 : 0<μ {0}) (hm : leftMoment μ=⊤) (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν)=⊤ := by
  by_contra h
  have hf := finite_actual_implies_left_moment ν μ hs e he he4 h0 r hr (lt_top_iff_ne_top.mpr h)
  simpa [hm] using hf

theorem right_atom_infinite_of_infinite_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (h1 : 0<μ {1}) (hm : rightMoment μ=⊤) (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν)=⊤ := by
  by_contra h
  have hf := finite_actual_implies_right_moment ν μ hs e he he4 h1 r hr (lt_top_iff_ne_top.mpr h)
  simpa [hm] using hf

/-- A normalized left-endpoint contamination. The original prior keeps mass
1-θ; this is a probability prior when μ is one and θ≤1. -/
def leftSpike (μ : Measure ℝ) (θ : ℝ≥0∞) : Measure ℝ :=
  θ • Measure.dirac 0 + (1-θ) • μ

lemma leftSpike_probability (μ : Measure ℝ) [IsProbabilityMeasure μ]
    (θ : ℝ≥0∞) (hθ : θ≤1) : IsProbabilityMeasure (leftSpike μ θ) := by
  constructor
  simp [leftSpike,add_tsub_cancel_of_le hθ]

lemma leftSpike_supported (μ : Measure ℝ) (θ : ℝ≥0∞)
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) : ∀ᵐ a ∂leftSpike μ θ, 0≤a ∧ a≤1 := by
  unfold leftSpike
  rw [ae_add_measure_iff]
  exact ⟨Measure.ae_smul_measure (by simp) θ,Measure.ae_smul_measure hs (1-θ)⟩

lemma leftSpike_atom_positive (μ : Measure ℝ) {θ : ℝ≥0∞} (hθ : 0<θ) :
    0<leftSpike μ θ {0} := by
  have h : θ≤leftSpike μ θ {0} := by
    simp only [leftSpike,Measure.add_apply,Measure.smul_apply,smul_eq_mul]
    simp
  exact hθ.trans_le h

lemma leftSpike_leftMoment (μ : Measure ℝ) (θ : ℝ≥0∞) :
    leftMoment (leftSpike μ θ)=(1-θ)*leftMoment μ := by
  unfold leftMoment EndpointMoment.interior leftSpike
  rw [Measure.restrict_add,Measure.restrict_smul,Measure.restrict_smul]
  simp [restrict_dirac,lintegral_smul_measure]

/-- Any positive contamination short of total replacement by the left endpoint
forces every policy to have infinite actual expectation if the original prior's
left inverse moment is infinite. No growth or original-budget premise is needed. -/
theorem left_spike_destroys_finite_budget {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsProbabilityMeasure μ]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (θ : ℝ≥0∞) (hθ0 : 0<θ) (hθ1 : θ<1) (hm : leftMoment μ=⊤)
    (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw (leftSpike μ θ) ν)=⊤ := by
  letI := leftSpike_probability μ θ hθ1.le
  apply left_atom_infinite_of_infinite_moment ν (leftSpike μ θ)
    (leftSpike_supported μ θ hs) e he he4 (leftSpike_atom_positive μ hθ0) _ r hr
  rw [leftSpike_leftMoment,hm]
  exact ENNReal.mul_top (ne_of_gt (tsub_pos_iff_lt.mpr hθ1))

#print axioms accepted_zero_iff
#print axioms accepted_one_iff
#print axioms zero_prefix_atom_lower
#print axioms one_prefix_atom_lower
#print axioms atom_profile_product_le
#print axioms left_atom_mass_lower
#print axioms right_atom_mass_lower
#print axioms finite_risk_implies_left_moment
#print axioms finite_risk_implies_right_moment
#print axioms finite_actual_implies_left_moment
#print axioms finite_actual_implies_right_moment
#print axioms both_atoms_coherent_actual_iff
#print axioms left_atom_infinite_of_infinite_moment
#print axioms right_atom_infinite_of_infinite_moment
#print axioms leftSpike_probability
#print axioms leftSpike_leftMoment
#print axioms left_spike_destroys_finite_budget

end
end EndpointAtoms
