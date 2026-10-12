import SparsePolicyTransport

noncomputable section
open MeasureTheory Set
open scoped ENNReal
open EndpointProcess SparseAtomBridge SparsePolicyTransport ConcreteSparsePrior
namespace IndependentSparseTransportReview

theorem word_round_trip (n : ℕ) (w : Fin n → Bool) :
    (fun i : Fin n => decide ((i:ℕ) ∈ wordSet w)) = w := by
  funext i
  cases hi : w i <;> simp [mem_wordSet,hi]

theorem word_set_uses_only_received_indices {n : ℕ} (w : Fin n → Bool) :
    wordSet w ⊆ Finset.range n := by
  unfold wordSet
  exact Finset.filter_subset _ _

/-- Two words with the same count lead to different transported reports when
the original policy actually observes their positions. -/
theorem positional_report_survives_transport :
    transportPolicy (fun (_z : Unit) (_n : ℕ) S => if 0 ∈ S then (1/4:ℝ) else 3/4)
      2 ![true,false] () = 1/4 ∧
    transportPolicy (fun (_z : Unit) (_n : ℕ) S => if 0 ∈ S then (1/4:ℝ) else 3/4)
      2 ![false,true] () = 3/4 := by
  norm_num [transportPolicy,wordSet]

/-- The parameter marginal remains the actual strictly interior sparse prior. -/
theorem real_prior_has_no_endpoint_atoms : realPrior {0}=0 ∧ realPrior {1}=0 := by
  have h0 : ∀ᵐ a ∂realPrior, a ≠ 0 := realPrior_inside.mono (fun _ h => ne_of_gt h.1)
  have h1 : ∀ᵐ a ∂realPrior, a ≠ 1 := realPrior_inside.mono (fun _ h => ne_of_lt h.2)
  constructor
  · simpa only [not_not] using (ae_iff.mp h0)
  · simpa only [not_not] using (ae_iff.mp h1)

/-- There is no finite-integrability premise hiding in the transport. -/
theorem finiteness_equivalent_for_every_old_policy {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (e : ℝ) (π : Z → SparsePriorBayes.Policy)
    (hπ : ∀ n S, Measurable (fun z => π z n S)) :
    ((∫⁻ ω, EndpointProcess.totalFailures e (transportPolicy π) ω
      ∂EndpointProcess.experimentLaw realPrior ν) < ⊤) ↔
    ((∫⁻ ω, SparsePriorProcess.totalFailures quadraticSupport e π ω
      ∂SparsePriorProcess.experimentLaw ν quadraticSupport 1 (by norm_num)
        quadraticSupport_pos quadraticSupport_half quadraticSupport_sep) < ⊤) := by
  rw [actual_count_expectations_equal ν e π hπ]

/-- One concrete epsilon and contamination, with the identical policy/count
interface before and after; only the prior measure is changed. -/
theorem same_interface_one_fifth_one_seventh {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] :
    (∃ r : ReportFamily Z, (∀ n w, Measurable (r n w)) ∧
      (∀ n w z, 0≤r n w z ∧ r n w z≤1) ∧
      (∫⁻ ω, EndpointProcess.totalFailures (1/5) r ω
        ∂EndpointProcess.experimentLaw realPrior ν)<⊤) ∧
    (∀ r : ReportFamily Z, (∀ n w, Measurable (r n w)) →
      (∫⁻ ω, EndpointProcess.totalFailures (1/5) r ω
        ∂EndpointProcess.experimentLaw (EndpointAtoms.leftSpike realPrior (1/7)) ν)=⊤) :=
  same_interface_finite_before_infinite_after ν (1/5) (by norm_num) (by norm_num)
    (1/7) (by norm_num) (by norm_num)

/-- The actual stream map is many-to-one. Its proved measure pushforward is
sufficient; an inverse or path-space bijection would be an unjustified claim. -/
theorem innovation_magnitudes_are_not_recoverable :
    (fun _ : ℕ => (3/4:ℝ)) ≠ (fun _ : ℕ => (7/8:ℝ)) ∧
    receiptStream (1/2) (fun _ => 3/4) = receiptStream (1/2) (fun _ => 7/8) := by
  constructor
  · intro h
    have he := congrFun h 0
    norm_num at he
  · funext n
    norm_num [receiptStream,bit]

set_option pp.explicit true in
#check @SparseAtomBridge.finite_before_infinite_after
set_option pp.explicit true in
#check @SparsePolicyTransport.actual_count_expectations_equal
set_option pp.explicit true in
#check @SparsePolicyTransport.same_interface_finite_before_infinite_after
#print axioms word_round_trip
#print axioms word_set_uses_only_received_indices
#print axioms positional_report_survives_transport
#print axioms real_prior_has_no_endpoint_atoms
#print axioms finiteness_equivalent_for_every_old_policy
#print axioms same_interface_one_fifth_one_seventh
#print axioms innovation_magnitudes_are_not_recoverable
end IndependentSparseTransportReview
