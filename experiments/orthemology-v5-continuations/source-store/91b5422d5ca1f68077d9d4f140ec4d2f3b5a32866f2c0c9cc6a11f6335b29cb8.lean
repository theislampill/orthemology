import RelativeContamination

/-! A generic p=1 version of the accepted point-prior/report transport. This is
new glue for the nonconvexity witness, not a new claim about the predecessor. -/
namespace GeneralPointTransport
noncomputable section
open MeasureTheory Set SparsePriorBayes SparsePolicyTransport EndpointProcess
open scoped ENNReal

def pointPrior (a : ℕ → ℝ) : Measure ℝ :=
  Measure.sum (fun i => ENNReal.ofReal (priorWeight a 1 i) • Measure.dirac (a i))

instance pointPrior_probability (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) : IsProbabilityMeasure (pointPrior a) := by
  constructor
  unfold pointPrior
  rw [Measure.sum_apply _ MeasurableSet.univ]
  simp only [Measure.smul_apply,smul_eq_mul,measure_univ,mul_one]
  have hw : Summable (fun i => priorWeight a 1 i) :=
    (power_weights_summable hp hs (by norm_num : (0:ℝ)<1)).div_const (normalizer a 1)
  rw [← ENNReal.ofReal_tsum_of_nonneg (fun i => (priorWeight_pos (by norm_num) hp hs i).le) hw,
    priorWeight_sum_one (by norm_num) hp hs]
  norm_num

lemma pointPrior_lintegral (a : ℕ → ℝ) (f : ℝ → ℝ≥0∞) :
    (∫⁻ x, f x ∂pointPrior a)=∑' i, ENNReal.ofReal (priorWeight a 1 i)*f (a i) := by
  unfold pointPrior
  rw [lintegral_sum_measure]
  apply tsum_congr
  intro i
  rw [lintegral_smul_measure,lintegral_dirac,smul_eq_mul]

lemma total_count_pointwise {Z : Type*} (a : ℕ → ℝ) (e : ℝ) (π : Z → Policy)
    (i : ℕ) (z : Z) (u : Innovations) :
    EndpointProcess.totalFailures e (transportPolicy π) ((a i,z),u)=
      SparsePriorProcess.totalFailures a e π (z,(i,receiptStream (a i) u)) := by
  unfold EndpointProcess.totalFailures SparsePriorProcess.totalFailures
  apply tsum_congr
  intro n
  simp only [EndpointProcess.stageFailure,transportPolicy,wordSet_observed,
    SparsePriorProcess.stageFailure,literal_failure_identical]

lemma conditional_count_integral_equal {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (e : ℝ) (π : Z → Policy) (hπ : ∀ n S, Measurable (fun z => π z n S)) (i : ℕ) (z : Z) :
    (∫⁻ u, EndpointProcess.totalFailures e (transportPolicy π) ((a i,z),u) ∂innovationLaw)=
      (∫⁻ y, SparsePriorProcess.totalFailures a e π (z,(i,y))
        ∂SparsePriorProcess.receiptLaw (a i) (hp i).le (by have h := hh i;linarith)) := by
  have hf : Measurable (fun y : SparsePriorProcess.Receipts => SparsePriorProcess.totalFailures a e π (z,(i,y))) :=
    (SparsePriorProcess.totalFailures_measurable a e π hπ).comp
      (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  simp_rw [total_count_pointwise]
  rw [← lintegral_map hf (receiptStream_measurable _),receiptStream_map_law]

lemma prior_conditional_integral_equal {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (e : ℝ) (π : Z → Policy)
    (hπ : ∀ n S, Measurable (fun z => π z n S)) (z : Z) :
    (∫⁻ x, conditionalIntegral e π (x,z) ∂pointPrior a)=
      (∫⁻ iy, SparsePriorProcess.totalFailures a e π (z,iy)
        ∂SparsePriorProcess.latentLaw a 1 (by norm_num) hp hh hs) := by
  have hf : Measurable (fun iy : ℕ × SparsePriorProcess.Receipts => SparsePriorProcess.totalFailures a e π (z,iy)) :=
    (SparsePriorProcess.totalFailures_measurable a e π hπ).comp (measurable_const.prodMk measurable_id)
  rw [pointPrior_lintegral,SparsePriorProcess.latentLaw_lintegral a 1 (by norm_num) hp hh hs _ hf]
  apply tsum_congr
  intro i
  congr 1
  exact conditional_count_integral_equal a hp hh e π hπ i z

/-- Actual count-integral transport for any power-one half-separated support. -/
theorem actual_count_transport {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (ν : Measure Z) [IsProbabilityMeasure ν]
    (e : ℝ) (π : Z → Policy) (hπ : ∀ n S, Measurable (fun z => π z n S)) :
    (∫⁻ w, EndpointProcess.totalFailures e (transportPolicy π) w ∂EndpointProcess.experimentLaw (pointPrior a) ν)=
      (∫⁻ w, SparsePriorProcess.totalFailures a e π w
        ∂SparsePriorProcess.experimentLaw ν a 1 (by norm_num) hp hh hs) := by
  letI : IsProbabilityMeasure (pointPrior a) := pointPrior_probability a hp hs
  have hn := EndpointProcess.totalFailures_measurable e (transportPolicy π) (transportPolicy_measurable π hπ)
  have ho := SparsePriorProcess.totalFailures_measurable a e π hπ
  unfold EndpointProcess.experimentLaw SparsePriorProcess.experimentLaw
  rw [lintegral_prod _ hn.aemeasurable,lintegral_prod _ ho.aemeasurable]
  change (∫⁻ p, conditionalIntegral e π p ∂(pointPrior a).prod ν)=_
  rw [lintegral_prod_symm _ (conditionalIntegral_measurable e π hπ).aemeasurable]
  apply lintegral_congr
  intro z
  exact prior_conditional_integral_equal a hp hh hs e π hπ z

/-- The inherited sparse criterion now supplies a coherent finite-budget witness
on the generic real-parameter point prior in the shared EndpointProcess interface. -/
theorem exists_finite_pointPrior {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) (ν : Measure Z) [IsProbabilityMeasure ν]
    (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (hS : Summable (fun i : ℕ => (a (i+1)/a i)*Real.log (a i/a (i+1)))) :
    ∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ w, EndpointProcess.totalFailures e r w ∂EndpointProcess.experimentLaw (pointPrior a) ν)<⊤ := by
  have hS' : Summable (fun i : ℕ => (a (i+1)^(1:ℝ)/a i)*Real.log (a i/a (i+1))) := by simpa using hS
  obtain ⟨π,hπ,hcoh,hfin⟩ := (IndependentConcreteContract.coherent_policy_finite_iff
    ν a 1 e (by norm_num) hp hh hs he he4).mpr hS'
  refine ⟨transportPolicy π,transportPolicy_measurable π hπ,transportPolicy_coherent π hcoh,?_⟩
  rwa [actual_count_transport a hp hh hs ν e π hπ]

def scaleSupport (c : ℝ) (a : ℕ → ℝ) : ℕ → ℝ := fun i => c*a i

lemma normalizer_scale (a : ℕ → ℝ) (c : ℝ) : normalizer (scaleSupport c a) 1=c*normalizer a 1 := by
  simp [normalizer,scaleSupport,Real.rpow_one,tsum_mul_left]

lemma priorWeight_scale (a : ℕ → ℝ) {c : ℝ} (hc : c≠0) (i : ℕ) :
    priorWeight (scaleSupport c a) 1 i=priorWeight a 1 i := by
  simp only [priorWeight,Real.rpow_one,normalizer_scale,scaleSupport]
  exact mul_div_mul_left _ _ hc

lemma spacing_scale (a : ℕ → ℝ) {c : ℝ} (hc : c≠0) (i : ℕ) :
    (scaleSupport c a (i+1)/scaleSupport c a i)*Real.log (scaleSupport c a i/scaleSupport c a (i+1))=
      (a (i+1)/a i)*Real.log (a i/a (i+1)) := by
  simp only [scaleSupport,mul_div_mul_left _ _ hc]

lemma scale_pos (a : ℕ → ℝ) (hp : ∀ i, 0<a i) {c : ℝ} (hc : 0<c) : ∀ i, 0<scaleSupport c a i :=
  fun i => mul_pos hc (hp i)

lemma scale_sep (a : ℕ → ℝ) (hs : ∀ i, a (i+1)≤a i/2) {c : ℝ} (hc : 0≤c) :
    ∀ i, scaleSupport c a (i+1)≤scaleSupport c a i/2 := by
  intro i
  have h := mul_le_mul_of_nonneg_left (hs i) hc
  dsimp [scaleSupport]
  nlinarith

#print axioms pointPrior_probability
#print axioms actual_count_transport
#print axioms exists_finite_pointPrior
#print axioms normalizer_scale
#print axioms priorWeight_scale
#print axioms spacing_scale
end
end GeneralPointTransport
