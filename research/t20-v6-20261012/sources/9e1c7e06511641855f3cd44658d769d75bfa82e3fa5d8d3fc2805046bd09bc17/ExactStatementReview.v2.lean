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
  norm_num [RationalGate.tolerance, RationalGate.positiveGaps, RationalGate.gaps,
    fixtureKernel, Controller.Fixture.kernel, Finset.univ_product, Finset.univ_bool]

theorem exact_computed_binding :
    ((withComputedTolerance oldConfig).toleranceNumerator : ℚ) /
      (withComputedTolerance oldConfig).toleranceDenominator = 1/6 := by
  rw [computed_tolerance_exact]
  exact fixture_computed_tolerance

theorem actual_model_membership : initialCandidate ∈ oldConfig.initialSupport := Finset.mem_univ _

theorem finite_prior_probability : IsProbabilityMeasure (Measure.dirac ()) := inferInstance

theorem fixed_fair_input_probability : IsProbabilityMeasure fairCantor := inferInstance

#print axioms extracted_statement_exact
#print axioms extracted_statement_refuted
#print axioms exact_failure_event_measurable
#print axioms fixture_computed_tolerance
#print axioms exact_computed_binding
#print axioms actual_model_membership
#print axioms finite_prior_probability
#print axioms fixed_fair_input_probability
end SemanticControlIndependentReview
