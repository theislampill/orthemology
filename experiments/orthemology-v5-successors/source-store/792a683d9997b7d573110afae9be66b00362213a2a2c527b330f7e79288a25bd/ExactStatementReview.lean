import ExactRuntimeCounterexample
set_option autoImplicit false
noncomputable section
namespace SemanticControlIndependentReview
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.Eighth.SemanticControls
open P02A2.Q8Measure (fairCantor)

def ExtractedMutantStatement : Prop :=
∀ (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (hinit : c.initialState = false)
    (hs : c.initialState ∈ winningRegion c.kernel menu priority c.initialSupport)
    (σ : Bool) (hσ : σ ∈ c.initialSupport) (d : Bool × Bool),
    ∀ᵐ x ∂fairCantor,
      ParitySuccess (priority σ) (historyAction d
        (decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x))

theorem extracted_statement_exact : ExtractedMutantStatement = MutatedRuntimeClaim := rfl

theorem extracted_statement_refuted : ¬ ExtractedMutantStatement :=
  exact_mutated_runtime_claim_false

-- A positive set here is a measurable fair-Cantor event, not merely outer measure.
theorem exact_failure_event_measurable (d : Bool × Bool) :
    MeasurableSet {x | ¬ ParitySuccess (actionPriority initialCandidate) (historyAction d
      (decodedHistory (policyProgram oldConfig)
        (sourcePolicy (withComputedTolerance oldConfig)) initialCandidate x))} := by
  exact (paritySuccess_measurable (actionPriority initialCandidate)).compl.preimage
    ((historyAction_measurable d).comp (decodedHistory_measurable _ _ _))

theorem fixture_computed_tolerance : RationalGate.tolerance fixtureKernel Finset.univ = 1/6 := by
  have hg : RationalGate.positiveGaps fixtureKernel Finset.univ = {(1/3 : ℚ)} := by
    ext q
    simp only [RationalGate.positiveGaps, RationalGate.gaps, Finset.mem_filter,
      Finset.mem_image, Finset.mem_product, Finset.mem_univ, true_and, Prod.exists,
      Bool.exists_bool]
    norm_num [fixtureKernel, Controller.Fixture.kernel,
      abs_of_pos (by norm_num : (0 : ℚ) < 1/3)]
    constructor
    · rintro ⟨h, hp⟩
      rcases h with ((h | h) | h | h) <;> linarith
    · intro h
      subst q
      norm_num
  unfold RationalGate.tolerance
  rw [hg]
  norm_num


theorem exact_computed_binding :
    ((withComputedTolerance oldConfig).toleranceNumerator : ℚ) /
      (withComputedTolerance oldConfig).toleranceDenominator = 1/6 := by
  rw [computed_tolerance_exact]
  exact fixture_computed_tolerance

theorem actual_model_membership : initialCandidate ∈ oldConfig.initialSupport := Finset.mem_univ _

theorem finite_prior_probability : IsProbabilityMeasure (Measure.dirac ()) := inferInstance

theorem fixed_fair_input_probability : IsProbabilityMeasure fairCantor := inferInstance

-- Same witness, old program and old decoder: physical old actions are correct.
theorem old_old_every_tape (d : Bool × Bool) (x : ℕ → Bool) :
    ParitySuccess (actionPriority initialCandidate) (historyAction d
      (decodedHistory (policyProgram oldConfig) (sourcePolicy oldConfig) initialCandidate x)) := by
  apply (actionPriority_parity_iff initialCandidate _).mpr
  apply Filter.Eventually.of_forall
  intro n
  simp only [historyAction, decodedHistory, generatedHistory_snoc, List.headD_cons,
    pairSelector, pairPolicy, old_source_constant]

#print axioms old_old_every_tape

#print axioms extracted_statement_exact
#print axioms extracted_statement_refuted
#print axioms exact_failure_event_measurable
#print axioms fixture_computed_tolerance
#print axioms exact_computed_binding
#print axioms actual_model_membership
#print axioms finite_prior_probability
#print axioms fixed_fair_input_probability
end SemanticControlIndependentReview
