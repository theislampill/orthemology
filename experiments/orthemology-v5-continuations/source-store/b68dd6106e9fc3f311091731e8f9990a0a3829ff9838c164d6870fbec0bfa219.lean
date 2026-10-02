import PriorSufficiency

/-! A separate actual-process successor. A single real parameter is drawn once.
Independent uniform innovations generate the conditional Bernoulli stream.
This extends the finite-observedWord theorem and is a new author candidate. -/
namespace EndpointProcess
noncomputable section
open MeasureTheory ProbabilityTheory Set
open AnnularLiteral BernoulliWord EndpointMoment BayesBridge GrowthMoment
open EmpiricalGeometry EmpiricalChernoff PriorSufficiency
open scoped ENNReal

abbrev Innovations := ℕ → ℝ

def uniformLaw : Measure ℝ := volume.restrict (Icc 0 1)

instance uniformLaw_probability : IsProbabilityMeasure uniformLaw := by
  constructor
  simp [uniformLaw,Real.volume_Icc]

def innovationLaw : Measure Innovations :=
  Measure.infinitePi (fun _ : ℕ => uniformLaw)

instance innovationLaw_probability : IsProbabilityMeasure innovationLaw := by
  unfold innovationLaw
  infer_instance

def bit (a u : ℝ) : Bool := if u≤a then true else false

def observedWord (n : ℕ) (a : ℝ) (u : Innovations) : Fin n → Bool :=
  fun i => bit a (u i)

lemma bit_measurable : Measurable (fun p : ℝ × ℝ => bit p.1 p.2) := by
  unfold bit
  exact Measurable.ite (measurableSet_le measurable_snd measurable_fst) measurable_const measurable_const

lemma prefix_measurable (n : ℕ) :
    Measurable (fun p : ℝ × Innovations => observedWord n p.1 p.2) := by
  apply measurable_pi_iff.mpr
  intro i
  exact bit_measurable.comp (measurable_fst.prodMk ((measurable_pi_apply (i:ℕ)).comp measurable_snd))

def bitEvent (a : ℝ) (b : Bool) : Set ℝ := if b then Iic a else Ioi a

lemma bitEvent_measurable (a : ℝ) (b : Bool) : MeasurableSet (bitEvent a b) := by
  cases b <;> simp [bitEvent]

lemma bit_eq_iff (a u : ℝ) (b : Bool) : bit a u=b ↔ u ∈ bitEvent a b := by
  cases b <;> simp [bit,bitEvent]

lemma uniform_bitEvent_mass {a : ℝ} (ha : 0≤a) (ha1 : a≤1) (b : Bool) :
    uniformLaw (bitEvent a b) = if b then ENNReal.ofReal a else ENNReal.ofReal (1-a) := by
  rw [uniformLaw,Measure.restrict_apply (bitEvent_measurable a b)]
  cases b
  · have hset : bitEvent a false ∩ Icc 0 1 = Ioc a 1 := by
      ext x
      simp only [bitEvent,Bool.false_eq_true,↓reduceIte,mem_inter_iff,mem_Ioi,mem_Icc,mem_Ioc]
      constructor
      · rintro ⟨h0,h1,h2⟩
        exact ⟨h0,h2⟩
      · rintro ⟨h0,h1⟩
        exact ⟨h0,by linarith,h1⟩
    rw [hset,Real.volume_Ioc]
    rfl
  · have hset : bitEvent a true ∩ Icc 0 1 = Icc 0 a := by
      ext x
      simp only [bitEvent,↓reduceIte,mem_inter_iff,mem_Iic,mem_Icc]
      constructor
      · rintro ⟨h0,h1,h2⟩
        exact ⟨h1,h0⟩
      · rintro ⟨h0,h1⟩
        exact ⟨h1,h0,by linarith⟩
    rw [hset,Real.volume_Icc]
    simp

def wordEvent (n : ℕ) (a : ℝ) (w : Fin n → Bool) : Set Innovations :=
  {u | observedWord n a u=w}

lemma wordEvent_measurable (n : ℕ) (a : ℝ) (w : Fin n → Bool) :
    MeasurableSet (wordEvent n a w) :=
  (measurableSet_singleton w).preimage
    ((prefix_measurable n).comp (measurable_const.prodMk measurable_id))

def extendedEvent (n : ℕ) (a : ℝ) (w : Fin n → Bool) (k : ℕ) : Set ℝ :=
  if h : k<n then bitEvent a (w ⟨k,h⟩) else univ

lemma wordEvent_eq_pi (n : ℕ) (a : ℝ) (w : Fin n → Bool) :
    wordEvent n a w = Set.pi (Finset.range n) (extendedEvent n a w) := by
  ext u
  simp only [wordEvent,mem_setOf_eq,Set.mem_pi,Finset.mem_coe,Finset.mem_range]
  constructor
  · intro h k hk
    have he := congrFun h ⟨k,hk⟩
    simpa [extendedEvent,hk,observedWord,bit_eq_iff] using he
  · intro h
    funext i
    have hi := h i i.isLt
    simpa [extendedEvent,i.isLt,observedWord,bit_eq_iff] using hi

/-- Exact conditional Bernoulli observedWord mass, derived from the actual uniform
infinite product. No conditional distribution premise is assumed. -/
theorem wordEvent_mass (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1) (w : Fin n → Bool) :
    innovationLaw (wordEvent n a w) = weight n a w := by
  rw [wordEvent_eq_pi,innovationLaw,Measure.infinitePi_pi]
  · rw [Finset.prod_range,weight_prod n ha ha1]
    apply Finset.prod_congr rfl
    intro i hi
    simp only [extendedEvent,i.isLt,↓reduceDIte]
    exact uniform_bitEvent_mass ha ha1 (w i)
  · intro k hk
    unfold extendedEvent
    split
    · exact bitEvent_measurable _ _
    · exact MeasurableSet.univ

lemma prefix_partition (n : ℕ) (a : ℝ) (u : Innovations) (f : (Fin n → Bool) → ℝ≥0∞) :
    f (observedWord n a u) = ∑ w : Fin n → Bool, if observedWord n a u=w then f w else 0 := by
  classical
  simp

theorem lintegral_prefix_function (n : ℕ) {a : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (f : (Fin n → Bool) → ℝ≥0∞) :
    (∫⁻ u, f (observedWord n a u) ∂innovationLaw) = ∑ w, weight n a w * f w := by
  classical
  have hm (w : Fin n → Bool) : Measurable (fun u => if observedWord n a u=w then f w else 0) :=
    Measurable.ite (wordEvent_measurable n a w) measurable_const measurable_const
  calc
    _ = ∫⁻ u, ∑ w : Fin n → Bool, if observedWord n a u=w then f w else 0 ∂innovationLaw := by
      apply lintegral_congr
      intro u
      exact prefix_partition n a u f
    _ = ∑ w : Fin n → Bool, ∫⁻ u, (if observedWord n a u=w then f w else 0) ∂innovationLaw :=
      lintegral_finset_sum _ (fun w _ => hm w)
    _ = _ := by
      apply Finset.sum_congr rfl
      intro w hw
      have hind : (fun u => if observedWord n a u=w then f w else 0) =
          (wordEvent n a w).indicator (fun _ => f w) := by
        funext u
        simp [wordEvent,Set.indicator_apply]
      rw [hind,lintegral_indicator (wordEvent_measurable n a w),lintegral_const,
        Measure.restrict_apply_univ,wordEvent_mass n ha ha1 w,mul_comm]

abbrev ReportFamily (Z : Type*) := (n : ℕ) → (Fin n → Bool) → Z → ℝ

/-- The parameter and seed are each drawn once, independently of the entire
uniform innovation stream. A probability prior gives a probability experiment. -/
def experimentLaw {Z : Type*} [MeasurableSpace Z] (μ : Measure ℝ) (ν : Measure Z) :
    Measure ((ℝ × Z) × Innovations) := (μ.prod ν).prod innovationLaw

instance experimentLaw_probability {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) [IsProbabilityMeasure μ] (ν : Measure Z) [IsProbabilityMeasure ν] :
    IsProbabilityMeasure (experimentLaw μ ν) := by
  unfold experimentLaw
  infer_instance

def stageFailure {Z : Type*} (e : ℝ) (r : ReportFamily Z) (n : ℕ)
    (ω : (ℝ × Z) × Innovations) : ℝ≥0∞ :=
  failureIndicator e (r n (observedWord n ω.1.1 ω.2) ω.1.2) ω.1.1

lemma stageFailure_measurable {Z : Type*} [MeasurableSpace Z]
    (e : ℝ) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) (n : ℕ) :
    Measurable (stageFailure e r n) := by
  classical
  have hword : Measurable (fun ω : (ℝ × Z) × Innovations => observedWord n ω.1.1 ω.2) :=
    (prefix_measurable n).comp (measurable_fst.fst.prodMk measurable_snd)
  have hpart (w : Fin n → Bool) : Measurable (fun ω : (ℝ × Z) × Innovations =>
      if observedWord n ω.1.1 ω.2=w then failureIndicator e (r n w ω.1.2) ω.1.1 else 0) :=
    Measurable.ite ((measurableSet_singleton w).preimage hword)
      ((measurable_failure e (r n w) (hr n w)).comp measurable_fst) measurable_const
  have hsum := Finset.measurable_sum (Finset.univ : Finset (Fin n → Bool)) (fun w _ => hpart w)
  convert hsum using 1
  funext ω
  exact prefix_partition n ω.1.1 ω.2 (fun w => failureIndicator e (r n w ω.1.2) ω.1.1)

def totalFailures {Z : Type*} (e : ℝ) (r : ReportFamily Z)
    (ω : (ℝ × Z) × Innovations) : ℝ≥0∞ := ∑' t : ℕ, stageFailure e r (t+1) ω

lemma totalFailures_measurable {Z : Type*} [MeasurableSpace Z]
    (e : ℝ) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    Measurable (totalFailures e r) :=
  Measurable.ennreal_tsum (fun t => stageFailure_measurable e r hr (t+1))

lemma ae_supported_product {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [SFinite ν] (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) :
    ∀ᵐ p : ℝ × Z ∂μ.prod ν, 0≤p.1 ∧ p.1≤1 := by
  apply (Measure.ae_prod_iff_ae_ae ?_).mpr
  · filter_upwards [hs] with a ha
    exact Filter.Eventually.of_forall (fun z => ha)
  · exact (measurableSet_le measurable_const measurable_fst).inter
      (measurableSet_le measurable_fst measurable_const)

/-- Actual stage expectation agrees with the frozen finite-word product risk. -/
theorem expected_stage_eq {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) (n : ℕ) :
    (∫⁻ ω, stageFailure e r n ω ∂experimentLaw μ ν) = productRisk n μ ν e (r n) := by
  unfold experimentLaw
  rw [lintegral_prod _ (stageFailure_measurable e r hr n).aemeasurable]
  unfold productRisk
  apply lintegral_congr_ae
  filter_upwards [ae_supported_product μ ν hs] with p hp
  exact lintegral_prefix_function n hp.1 hp.2 (fun w => failureIndicator e (r n w p.2) p.1)

/-- The actual positive-time realized bad-count random variable has exactly the
sum of finite-prefix risks as its expectation, including the infinite case. -/
theorem actual_expectation_eq_risk_series {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν) =
      ∑' t : ℕ, productRisk (t+1) μ ν e (r (t+1)) := by
  unfold totalFailures
  rw [lintegral_tsum (fun t => (stageFailure_measurable e r hr (t+1)).aemeasurable)]
  apply tsum_congr
  intro t
  exact expected_stage_eq μ ν hs e r hr (t+1)

/-- Arbitrary-prior actual-process sufficiency needs no endpoint lower growth. -/
theorem empirical_actual_expectation_bound {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (e : ℝ) (he : 0<e) (he4 : e≤1/4) :
    (∫⁻ ω, totalFailures e (fun n w _ => empiricalReport n e w) ω ∂experimentLaw μ ν) ≤
      ENNReal.ofReal (32/e^2) * inverseVarianceMoment μ := by
  rw [actual_expectation_eq_risk_series μ ν hs e _ (fun n w => measurable_const)]
  simp_rw [empirical_productRisk_eq]
  exact summed_empirical_risk_bound μ e hs he he4

/-- Actual-process endpoint inverse-moment iff, for the same one-time latent
parameter and independent seed/innovation experiment. -/
theorem exists_finite_actual_expectation_iff {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η≠0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) :
    (∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν) < ⊤) ↔
      inverseVarianceMoment μ < ⊤ := by
  constructor
  · rintro ⟨r,hr,hf⟩
    rw [actual_expectation_eq_risk_series μ ν hs e r hr] at hf
    exact finite_product_risk_implies_inverse_moment ν μ e x0 η hη hx0 he he4 hg r hr hf
  · intro hm
    obtain ⟨r,hr,hf⟩ := (exists_seeded_report_family_iff ν μ e x0 η hη hx0 he he4 hg hs).mpr hm
    exact ⟨r,hr,by rwa [actual_expectation_eq_risk_series μ ν hs e r hr]⟩

theorem every_policy_infinite_of_infinite_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η≠0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) (hm : inverseVarianceMoment μ=⊤)
    (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν) = ⊤ := by
  by_contra h
  have hf := (exists_finite_actual_expectation_iff ν μ e x0 η hη hx0 he he4 hg hs).mp
    ⟨r,hr,lt_top_iff_ne_top.mpr h⟩
  simpa [hm] using hf

/-- The complete experiment has the literal product rectangle masses, including
independence of the seed from the parameter and the whole innovation stream. -/
theorem experiment_rectangle {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (A : Set ℝ) (B : Set Z) (C : Set Innovations) :
    experimentLaw μ ν ((A ×ˢ B) ×ˢ C) = μ A * ν B * innovationLaw C := by
  simp only [experimentLaw,Measure.prod_prod]

/-- Conditional iid law at every finite selection of indices, not merely at
consecutive prefixes. This is proved from the independent uniform product. -/
theorem finite_receipt_mass {a : ℝ} (ha : 0≤a) (ha1 : a≤1)
    (s : Finset ℕ) (w : ℕ → Bool) :
    innovationLaw {u | ∀ i ∈ s, bit a (u i)=w i} =
      ∏ i ∈ s, if w i then ENNReal.ofReal a else ENNReal.ofReal (1-a) := by
  have he : {u : Innovations | ∀ i ∈ s, bit a (u i)=w i} =
      Set.pi s (fun i => bitEvent a (w i)) := by
    ext u
    simp only [Set.mem_setOf_eq,Set.mem_pi,Finset.mem_coe,bit_eq_iff]
  rw [he,innovationLaw,Measure.infinitePi_pi _ (fun i hi => bitEvent_measurable _ _)]
  apply Finset.prod_congr rfl
  intro i hi
  exact uniform_bitEvent_mass ha ha1 (w i)

/-- No future innovation is used by the report or its literal loss. -/
theorem prefix_causality {Z : Type*} (e : ℝ) (r : ReportFamily Z) (n : ℕ)
    (a : ℝ) (z : Z) (u v : Innovations) (h : ∀ i<n, u i=v i) :
    stageFailure e r n ((a,z),u) = stageFailure e r n ((a,z),v) := by
  have hw : observedWord n a u = observedWord n a v := by
    funext i
    exact congrArg (bit a) (h i i.isLt)
  simp only [stageFailure,hw]

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
  exact ⟨div_nonneg h0 hn'.le,(div_le_one hn').mpr h1⟩

lemma empirical_report_coherent (n : ℕ) (hn : 0<n) (e : ℝ)
    (he : 0<e) (he4 : e≤1/4) (w : Fin n → Bool) :
    0≤empiricalReport n e w ∧ empiricalReport n e w≤1 := by
  obtain ⟨h0,h1⟩ := empiricalMean_unit n hn w
  unfold empiricalReport
  constructor <;> nlinarith

/-- The actual-process existence theorem can require coherent reports at every
positive time; the explicit empirical family is the witness. -/
theorem exists_coherent_finite_actual_expectation_iff {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η≠0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (hs : ∀ᵐ a ∂μ, 0≤a ∧ a≤1) :
    (∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n, 0<n → ∀ w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ ω, totalFailures e r ω ∂experimentLaw μ ν) < ⊤) ↔
      inverseVarianceMoment μ < ⊤ := by
  constructor
  · rintro ⟨r,hr,hcoh,hf⟩
    exact (exists_finite_actual_expectation_iff ν μ e x0 η hη hx0 he he4 hg hs).mp ⟨r,hr,hf⟩
  · intro hm
    refine ⟨(fun n w _ => empiricalReport n e w),(fun n w => measurable_const),?_,?_⟩
    · intro n hn w z
      exact empirical_report_coherent n hn e he he4 w
    · exact (empirical_actual_expectation_bound μ ν hs e he he4).trans_lt
        (ENNReal.mul_lt_top ENNReal.ofReal_lt_top hm)

#print axioms wordEvent_mass
#print axioms lintegral_prefix_function
#print axioms stageFailure_measurable
#print axioms totalFailures_measurable
#print axioms expected_stage_eq
#print axioms actual_expectation_eq_risk_series
#print axioms empirical_actual_expectation_bound
#print axioms exists_finite_actual_expectation_iff
#print axioms every_policy_infinite_of_infinite_moment
#print axioms experiment_rectangle
#print axioms finite_receipt_mass
#print axioms prefix_causality
#print axioms empirical_report_coherent
#print axioms exists_coherent_finite_actual_expectation_iff

end
end EndpointProcess
