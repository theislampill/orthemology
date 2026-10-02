import CriticalPairProcess
import SparsePolicyTransport

namespace RelativeContamination
noncomputable section
open MeasureTheory Set EndpointProcess SparseAtomBridge ConcreteSparsePrior
open CriticalPairProcess SparsePolicyTransport
open scoped ENNReal

lemma pairPrior_inside (a : ℕ → ℝ) (e : ℝ)
    (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (he : 0<e) (he4 : e≤1/4) : ∀ᵐ x ∂pairPrior a e, x∈Ioo (0:ℝ) 1 := by
  rw [ae_iff]
  change pairPrior a e ((Ioo 0 1)ᶜ)=0
  rw [pairPrior,Measure.sum_apply _ measurableSet_Ioo.compl]
  apply ENNReal.tsum_eq_zero.mpr
  intro i
  have hprod := mul_le_mul he4 (hh i) (hp i).le (by norm_num : (0:ℝ)≤1/4)
  have hlp : 0<(1-e)*a i := mul_pos (by linarith) (hp i)
  have hup : 0<(1+e)*a i := mul_pos (by linarith) (hp i)
  have hlt : (1-e)*a i<1 := by nlinarith [hp i,hh i,mul_nonneg he.le (hp i).le]
  have hut : (1+e)*a i<1 := by nlinarith [hh i]
  simp [Measure.smul_apply,pairLaw,Measure.add_apply,hlp,hup,hlt,hut]

def contaminated (e : ℝ) (theta : ℝ≥0∞) : Measure ℝ :=
  theta • pairPrior quadraticSupport e+(1-theta) • realPrior

lemma contaminated_probability (e : ℝ) (theta : ℝ≥0∞) (ht : theta≤1) :
    IsProbabilityMeasure (contaminated e theta) := by
  letI := pairPrior_probability quadraticSupport e quadraticSupport_pos quadraticSupport_sep
  constructor
  simp [contaminated,add_tsub_cancel_of_le ht]

lemma contaminated_inside {e : ℝ} (he : 0<e) (he4 : e≤1/4) (theta : ℝ≥0∞) :
    ∀ᵐ x ∂contaminated e theta, x∈Ioo (0:ℝ) 1 := by
  unfold contaminated
  rw [ae_add_measure_iff]
  exact ⟨Measure.ae_smul_measure (pairPrior_inside quadraticSupport e quadraticSupport_pos
    quadraticSupport_half he he4) theta,Measure.ae_smul_measure realPrior_inside (1-theta)⟩

/-- Prior linearity is derived from the actual product experiment by Fubini. -/
lemma count_prior_lintegral {Z : Type*} [MeasurableSpace Z]
    (μ : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (e : ℝ) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ w, totalFailures e r w ∂experimentLaw μ ν) =
      ∫⁻ x, ∫⁻ z, ∫⁻ u, totalFailures e r ((x,z),u) ∂innovationLaw ∂ν ∂μ := by
  have hm := totalFailures_measurable e r hr
  unfold experimentLaw
  rw [lintegral_prod _ hm.aemeasurable]
  exact lintegral_prod _ hm.lintegral_prod_right'.aemeasurable

lemma count_mixture {Z : Type*} [MeasurableSpace Z]
    (μ μ' : Measure ℝ) (ν : Measure Z) [IsProbabilityMeasure ν]
    (e : ℝ) (r : ReportFamily Z) (hr : ∀ n w, Measurable (r n w))
    (c d : ℝ≥0∞) :
    (∫⁻ w, totalFailures e r w ∂experimentLaw (c • μ+d • μ') ν) =
      c*(∫⁻ w, totalFailures e r w ∂experimentLaw μ ν)+
      d*(∫⁻ w, totalFailures e r w ∂experimentLaw μ' ν) := by
  simp_rw [count_prior_lintegral _ ν e r hr]
  rw [lintegral_add_measure,lintegral_smul_measure,lintegral_smul_measure]
  rfl

/-- Every positive mixture fraction of the interior paired perturbation is
fatal to finite expected count. No endpoint atom is introduced. -/
theorem every_policy_infinite {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (theta : ℝ≥0∞) (ht : 0<theta) (r : ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ w, totalFailures e r w ∂experimentLaw (contaminated e theta) ν)=⊤ := by
  unfold contaminated
  rw [count_mixture _ _ ν e r hr]
  rw [CriticalPairProcess.every_policy_infinite quadraticSupport e quadraticSupport_pos
    quadraticSupport_half quadraticSupport_sep he he4 ν r hr,
    ENNReal.mul_top (ne_of_gt ht),top_add]

/-- Same-interface finite-before/universal-infinite-after, with an interior
relative perturbation rather than the predecessor's endpoint contamination. -/
theorem same_interface_nonendpoint_perturbation {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (theta : ℝ≥0∞) (ht0 : 0<theta) (ht1 : theta≤1) :
    IsProbabilityMeasure (contaminated e theta) ∧
    (∀ᵐ x ∂contaminated e theta, x∈Ioo (0:ℝ) 1) ∧
    (∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ w, totalFailures e r w ∂experimentLaw realPrior ν)<⊤) ∧
    (∀ r : ReportFamily Z, (∀ n w, Measurable (r n w)) →
      (∫⁻ w, totalFailures e r w ∂experimentLaw (contaminated e theta) ν)=⊤) :=
  ⟨contaminated_probability e theta ht1,contaminated_inside he he4 theta,
    realPrior_finite_coherent_actual_count ν e he he4,
    fun r hr => every_policy_infinite ν e he he4 theta ht0 r hr⟩

#print axioms pairPrior_inside
#print axioms contaminated_probability
#print axioms contaminated_inside
#print axioms count_prior_lintegral
#print axioms count_mixture
#print axioms every_policy_infinite
#print axioms same_interface_nonendpoint_perturbation
end
end RelativeContamination
