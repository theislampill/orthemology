import SparseAtomBridge

namespace SparsePolicyTransport
noncomputable section
open MeasureTheory Set
open EndpointProcess SparseAtomBridge ConcreteSparsePrior
open scoped ENNReal

def receiptStream (a : ℝ) (u : Innovations) : SparsePriorProcess.Receipts :=
  fun k => bit a (u k)

lemma receiptStream_measurable (a : ℝ) : Measurable (receiptStream a) := by
  apply measurable_pi_iff.mpr
  intro k
  exact bit_measurable.comp (measurable_const.prodMk (measurable_pi_apply k))

lemma single_bit_measurable (a : ℝ) : Measurable (bit a) :=
  bit_measurable.comp (measurable_const.prodMk measurable_id)

lemma bit_map_uniform {a : ℝ} (ha : 0≤a) (ha1 : a≤1) :
    uniformLaw.map (bit a)=SparsePriorProcess.sourceCoinMeasure a ha ha1 := by
  apply Measure.ext_of_singleton
  intro b
  rw [Measure.map_apply (single_bit_measurable a) (measurableSet_singleton b),
    SparsePriorProcess.sourceCoin_singleton]
  have he : (bit a) ⁻¹' {b}=bitEvent a b := by
    ext u
    exact bit_eq_iff a u b
  rw [he,uniform_bitEvent_mass ha ha1]
  cases b <;> rfl

/-- The threshold-generated stream has exactly the accepted Bernoulli stream
law, as a measure pushforward. No path-space inverse is asserted or needed. -/
theorem receiptStream_map_law {a : ℝ} (ha : 0≤a) (ha1 : a≤1) :
    innovationLaw.map (receiptStream a)=SparsePriorProcess.receiptLaw a ha ha1 := by
  unfold SparsePriorProcess.receiptLaw
  apply Measure.eq_infinitePi
  intro s t ht
  rw [Measure.map_apply (receiptStream_measurable a)
    (MeasurableSet.pi (Finset.countable_toSet s) ht)]
  have hpre : (receiptStream a) ⁻¹' Set.pi (s : Set ℕ) t=
      Set.pi (s : Set ℕ) (fun k => (bit a) ⁻¹' t k) := by
    ext u
    simp only [Set.mem_preimage,Set.mem_pi,receiptStream]
  rw [hpre,innovationLaw,Measure.infinitePi_pi _ (fun k hk => (ht k hk).preimage (single_bit_measurable a))]
  apply Finset.prod_congr rfl
  intro k hk
  rw [← bit_map_uniform ha ha1,Measure.map_apply (single_bit_measurable a) (ht k hk)]

def wordSet {n : ℕ} (w : Fin n → Bool) : Finset ℕ := by
  classical
  exact (Finset.range n).filter (fun k => (if h : k<n then w ⟨k,h⟩ else false)=true)

lemma wordSet_observed (n : ℕ) (a : ℝ) (u : Innovations) :
    wordSet (observedWord n a u)=SparsePriorProcess.prefixSet n (receiptStream a u) := by
  classical
  ext k
  by_cases hk : k<n
  · simp [wordSet,SparsePriorProcess.prefixSet,hk,observedWord,receiptStream]
  · simp [wordSet,SparsePriorProcess.prefixSet,hk]

lemma mem_wordSet {n : ℕ} (w : Fin n → Bool) (i : Fin n) :
    (i:ℕ) ∈ wordSet w ↔ w i=true := by
  simp [wordSet,i.isLt]

/-- The encoding retains the full ordered word, not just its number of ones. -/
theorem wordSet_injective (n : ℕ) : Function.Injective (@wordSet n) := by
  intro v w h
  funext i
  have hm : v i=true ↔ w i=true := by
    rw [← mem_wordSet v i,← mem_wordSet w i,h]
  cases hv : v i <;> cases hw : w i <;> simp_all

theorem same_count_different_word_sets : wordSet ![true,false] ≠ wordSet ![false,true] := by
  intro h
  have he := wordSet_injective 2 h
  have hh := congrFun he 0
  norm_num at hh

def transportPolicy {Z : Type*} (π : Z → SparsePriorBayes.Policy) : ReportFamily Z :=
  fun n w z => π z n (wordSet w)

lemma transportPolicy_measurable {Z : Type*} [MeasurableSpace Z]
    (π : Z → SparsePriorBayes.Policy) (hπ : ∀ n S, Measurable (fun z => π z n S)) :
    ∀ n w, Measurable (transportPolicy π n w) := fun n w => hπ n (wordSet w)

lemma transportPolicy_coherent {Z : Type*} (π : Z → SparsePriorBayes.Policy)
    (hπ : ∀ z n S, 0≤π z n S ∧ π z n S≤1) :
    ∀ n w z, 0≤transportPolicy π n w z ∧ transportPolicy π n w z≤1 :=
  fun n w z => hπ z n (wordSet w)

lemma literal_failure_identical (a e q : ℝ) :
    AnnularLiteral.failureIndicator e q a=SparsePriorProcess.literalFailure a e q := by
  classical
  unfold AnnularLiteral.failureIndicator SparsePriorProcess.literalFailure
  by_cases h : AnnularLiteral.Accepted a e q
  · have hh := (literal_contract_identical a e q).mpr h
    simp [h,hh]
  · have hh : ¬ SparsePriorGeometry.Accepted a e q := by
      simpa only [literal_contract_identical] using h
    simp [h,hh]

lemma total_count_pointwise {Z : Type*} (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (i : ℕ) (z : Z) (u : Innovations) :
    EndpointProcess.totalFailures e (transportPolicy π) ((quadraticSupport i,z),u)=
      SparsePriorProcess.totalFailures quadraticSupport e π
        (z,(i,receiptStream (quadraticSupport i) u)) := by
  unfold EndpointProcess.totalFailures SparsePriorProcess.totalFailures
  apply tsum_congr
  intro n
  simp only [EndpointProcess.stageFailure,transportPolicy,wordSet_observed,
    SparsePriorProcess.stageFailure,literal_failure_identical]

theorem conditional_count_integral_equal {Z : Type*} [MeasurableSpace Z]
    (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (hπ : ∀ n S, Measurable (fun z => π z n S)) (i : ℕ) (z : Z) :
    (∫⁻ u, EndpointProcess.totalFailures e (transportPolicy π) ((quadraticSupport i,z),u)
      ∂innovationLaw)=
    (∫⁻ y, SparsePriorProcess.totalFailures quadraticSupport e π (z,(i,y))
      ∂SparsePriorProcess.receiptLaw (quadraticSupport i) (quadraticSupport_pos i).le
        (le_trans (quadraticSupport_half i) (by norm_num))) := by
  have hf : Measurable (fun y : SparsePriorProcess.Receipts =>
      SparsePriorProcess.totalFailures quadraticSupport e π (z,(i,y))) :=
    (SparsePriorProcess.totalFailures_measurable quadraticSupport e π hπ).comp
      (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  simp_rw [total_count_pointwise]
  rw [← lintegral_map hf (receiptStream_measurable _),receiptStream_map_law]

def conditionalIntegral {Z : Type*} (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (p : ℝ × Z) : ℝ≥0∞ :=
  ∫⁻ u, EndpointProcess.totalFailures e (transportPolicy π) (p,u) ∂innovationLaw

lemma conditionalIntegral_measurable {Z : Type*} [MeasurableSpace Z]
    (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (hπ : ∀ n S, Measurable (fun z => π z n S)) : Measurable (conditionalIntegral e π) :=
  (EndpointProcess.totalFailures_measurable e (transportPolicy π)
    (transportPolicy_measurable π hπ)).lintegral_prod_right'

theorem prior_conditional_integral_equal {Z : Type*} [MeasurableSpace Z]
    (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (hπ : ∀ n S, Measurable (fun z => π z n S)) (z : Z) :
    (∫⁻ a, conditionalIntegral e π (a,z) ∂realPrior)=
      (∫⁻ iy, SparsePriorProcess.totalFailures quadraticSupport e π (z,iy) ∂sourceLaw) := by
  have hm := conditionalIntegral_measurable e π hπ
  have hf : Measurable (fun a : ℝ => conditionalIntegral e π (a,z)) :=
    hm.comp (measurable_id.prodMk measurable_const)
  have hleft : Measurable (fun iy : SourcePoint => conditionalIntegral e π (parameter iy,z)) :=
    hm.comp (parameter_measurable.prodMk measurable_const)
  have hright : Measurable (fun iy : SourcePoint =>
      SparsePriorProcess.totalFailures quadraticSupport e π (z,iy)) :=
    (SparsePriorProcess.totalFailures_measurable quadraticSupport e π hπ).comp
      (measurable_const.prodMk measurable_id)
  unfold realPrior
  rw [lintegral_map hf parameter_measurable]
  unfold sourceLaw
  rw [SparsePriorProcess.latentLaw_lintegral quadraticSupport 1 (by norm_num)
    quadraticSupport_pos quadraticSupport_half quadraticSupport_sep _ hleft,
    SparsePriorProcess.latentLaw_lintegral quadraticSupport 1 (by norm_num)
    quadraticSupport_pos quadraticSupport_half quadraticSupport_sep _ hright]
  apply tsum_congr
  intro i
  simp only [parameter,lintegral_const,measure_univ,mul_one]
  unfold conditionalIntegral
  rw [conditional_count_integral_equal e π hπ i z]

/-- The same reporting function, expressed on the observed one-position set,
has identical actual expected total count under the two process constructions. -/
theorem actual_count_expectations_equal {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (hπ : ∀ n S, Measurable (fun z => π z n S)) :
    (∫⁻ ω, EndpointProcess.totalFailures e (transportPolicy π) ω
      ∂EndpointProcess.experimentLaw realPrior ν)=
    (∫⁻ ω, SparsePriorProcess.totalFailures quadraticSupport e π ω
      ∂SparsePriorProcess.experimentLaw ν quadraticSupport 1 (by norm_num)
        quadraticSupport_pos quadraticSupport_half quadraticSupport_sep) := by
  have hn := EndpointProcess.totalFailures_measurable e (transportPolicy π)
    (transportPolicy_measurable π hπ)
  have ho := SparsePriorProcess.totalFailures_measurable quadraticSupport e π hπ
  change (∫⁻ ω, EndpointProcess.totalFailures e (transportPolicy π) ω
      ∂(realPrior.prod ν).prod innovationLaw)=
    (∫⁻ ω, SparsePriorProcess.totalFailures quadraticSupport e π ω ∂ν.prod sourceLaw)
  rw [lintegral_prod _ hn.aemeasurable,lintegral_prod _ ho.aemeasurable]
  change (∫⁻ p, conditionalIntegral e π p ∂realPrior.prod ν)=_
  rw [lintegral_prod_symm _ (conditionalIntegral_measurable e π hπ).aemeasurable]
  apply lintegral_congr
  intro z
  exact prior_conditional_integral_equal e π hπ z

theorem realPrior_finite_coherent_actual_count {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4) :
    ∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ ω, EndpointProcess.totalFailures e r ω
        ∂EndpointProcess.experimentLaw realPrior ν)<⊤ := by
  obtain ⟨π,hπ,hcoh,hfinite,hmom,hvar,hend⟩ :=
    IndependentConcreteContract.coherent_counterexample_same_law ν e he he4
  refine ⟨transportPolicy π,transportPolicy_measurable π hπ,transportPolicy_coherent π hcoh,?_⟩
  rwa [actual_count_expectations_equal ν e π hπ]

/-- Before and after contamination now use the identical reporting interface,
sample-space type, literal count function and uniform-innovation construction.
Only the real-parameter prior changes. -/
theorem same_interface_finite_before_infinite_after {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (θ : ℝ≥0∞) (hθ0 : 0<θ) (hθ1 : θ<1) :
    (∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ ω, EndpointProcess.totalFailures e r ω
        ∂EndpointProcess.experimentLaw realPrior ν)<⊤) ∧
    (∀ r : ReportFamily Z, (∀ n w, Measurable (r n w)) →
      (∫⁻ ω, EndpointProcess.totalFailures e r ω
        ∂EndpointProcess.experimentLaw (EndpointAtoms.leftSpike realPrior θ) ν)=⊤) :=
  ⟨realPrior_finite_coherent_actual_count ν e he he4,
    fun r hr => contaminated_sparse_prior_all_policies_infinite ν e he he4 θ hθ0 hθ1 r hr⟩

#print axioms receiptStream_map_law
#print axioms wordSet_observed
#print axioms wordSet_injective
#print axioms same_count_different_word_sets
#print axioms transportPolicy_measurable
#print axioms transportPolicy_coherent
#print axioms total_count_pointwise
#print axioms conditional_count_integral_equal
#print axioms conditionalIntegral_measurable
#print axioms prior_conditional_integral_equal
#print axioms actual_count_expectations_equal
#print axioms realPrior_finite_coherent_actual_count
#print axioms same_interface_finite_before_infinite_after
end
end SparsePolicyTransport
