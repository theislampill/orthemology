import EndpointAtoms
import ConcreteContractProbe

/-! Source-specific parameter-prior transport and a paired perturbation result.
The before and after experiments retain their explicit different representations.
No unproved policy transport between representations is asserted. -/
namespace SparseAtomBridge
noncomputable section
open MeasureTheory Set
open ConcreteSparsePrior EndpointAtoms EndpointMoment
open scoped ENNReal

abbrev SourcePoint := ℕ × SparsePriorProcess.Receipts

def sourceLaw : Measure SourcePoint := SparsePriorProcess.latentLaw quadraticSupport 1
  (by norm_num) quadraticSupport_pos quadraticSupport_half quadraticSupport_sep

instance sourceLaw_probability : IsProbabilityMeasure sourceLaw := by
  unfold sourceLaw
  infer_instance

def parameter (x : SourcePoint) : ℝ := quadraticSupport x.1

lemma parameter_measurable : Measurable parameter :=
  (measurable_of_countable quadraticSupport).comp measurable_fst

/-- This is the actual parameter marginal of the accepted sparse experiment. -/
def realPrior : Measure ℝ := sourceLaw.map parameter

instance realPrior_probability : IsProbabilityMeasure realPrior :=
  isProbabilityMeasure_map parameter_measurable.aemeasurable

lemma realPrior_inside : ∀ᵐ a ∂realPrior, a ∈ Ioo (0:ℝ) 1 := by
  apply (ae_map_iff parameter_measurable.aemeasurable measurableSet_Ioo).mpr
  apply Filter.Eventually.of_forall
  intro x
  exact ⟨quadraticSupport_pos x.1,lt_of_le_of_lt (quadraticSupport_half x.1) (by norm_num)⟩

lemma realPrior_supported : ∀ᵐ a ∂realPrior, 0≤a ∧ a≤1 :=
  realPrior_inside.mono (fun _ h => ⟨h.1.le,h.2.le⟩)

theorem parameter_event_mass (A : Set ℝ) (hA : MeasurableSet A) :
    realPrior A=sourceLaw {x | parameter x ∈ A} :=
  Measure.map_apply parameter_measurable hA

theorem literal_contract_identical (a e q : ℝ) :
    SparsePriorGeometry.Accepted a e q ↔ AnnularLiteral.Accepted a e q := Iff.rfl

/-- Mapping to a convenient fixed parameter would destroy the claimed moment;
the actual parameter coordinate in realPrior is load-bearing. -/
theorem constant_parameter_countercontrol :
    leftMoment (sourceLaw.map (fun _ => (1/2:ℝ)))=2 := by
  have hm : sourceLaw.map (fun _ => (1/2:ℝ))=Measure.dirac (1/2:ℝ) := by simp
  rw [hm]
  norm_num [leftMoment,EndpointMoment.interior,restrict_dirac]

/-- The infinite inverse moment is transported through the actual parameter
map; it is not assumed merely because the support formulas look alike. -/
theorem realPrior_left_moment_infinite : leftMoment realPrior=⊤ := by
  unfold leftMoment EndpointMoment.interior
  rw [Measure.restrict_eq_self_of_ae_mem realPrior_inside]
  unfold realPrior
  rw [lintegral_map (by fun_prop) parameter_measurable]
  simpa only [sourceLaw,parameter,one_div] using quadraticSupport_inverse_moment_infinite

theorem contaminated_sparse_prior_all_policies_infinite {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (θ : ℝ≥0∞) (hθ0 : 0<θ) (hθ1 : θ<1) (r : EndpointProcess.ReportFamily Z)
    (hr : ∀ n w, Measurable (r n w)) :
    (∫⁻ ω, EndpointProcess.totalFailures e r ω
      ∂EndpointProcess.experimentLaw (leftSpike realPrior θ) ν)=⊤ :=
  left_spike_destroys_finite_budget ν realPrior realPrior_supported e he he4 θ hθ0 hθ1
    realPrior_left_moment_infinite r hr

/-- The old certified sparse experiment has a finite-count witness, while the
normalized contaminated parameter marginal gives infinite count expectation for
every policy in the new actual experiment. Both representations are explicit. -/
theorem finite_before_infinite_after {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (he : 0<e) (he4 : e≤1/4)
    (θ : ℝ≥0∞) (hθ0 : 0<θ) (hθ1 : θ<1) :
    (∃ π : Z → SparsePriorBayes.Policy,
      (∀ n S, Measurable (fun z => π z n S)) ∧
      (∀ z n S, 0≤π z n S ∧ π z n S≤1) ∧
      (∫⁻ ω, SparsePriorProcess.totalFailures quadraticSupport e π ω
        ∂SparsePriorProcess.experimentLaw ν quadraticSupport 1 (by norm_num)
          quadraticSupport_pos quadraticSupport_half quadraticSupport_sep)<⊤) ∧
    (∀ r : EndpointProcess.ReportFamily Z, (∀ n w, Measurable (r n w)) →
      (∫⁻ ω, EndpointProcess.totalFailures e r ω
        ∂EndpointProcess.experimentLaw (leftSpike realPrior θ) ν)=⊤) := by
  obtain ⟨π,hmeas,hcoh,hfinite,hmom,hvar,hend⟩ :=
    IndependentConcreteContract.coherent_counterexample_same_law ν e he he4
  exact ⟨⟨π,hmeas,hcoh,hfinite⟩,
    fun r hr => contaminated_sparse_prior_all_policies_infinite ν e he he4 θ hθ0 hθ1 r hr⟩

#print axioms realPrior_probability
#print axioms realPrior_inside
#print axioms realPrior_left_moment_infinite
#print axioms parameter_event_mass
#print axioms literal_contract_identical
#print axioms constant_parameter_countercontrol
#print axioms contaminated_sparse_prior_all_policies_infinite
#print axioms finite_before_infinite_after
end
end SparseAtomBridge
