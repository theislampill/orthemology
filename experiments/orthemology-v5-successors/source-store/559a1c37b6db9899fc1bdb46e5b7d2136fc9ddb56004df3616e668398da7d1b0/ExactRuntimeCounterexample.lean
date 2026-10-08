import OppositeTailTransfer
import MixedReceiptLaw
set_option autoImplicit false

noncomputable section
namespace Orthemology.Eighth.SemanticControls
open MeasureTheory
open scoped ENNReal
open HiddenParity HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RationalLaw.CanonicalBinding
open P02A2.Q8Measure (fairCantor)

/-- This equality holds only on the eventual opposite-action set. Full histories
and finite-prefix laws need not agree. -/
theorem fixture_blind_agree (θ : Bool) (e : Bool × Bool) (he : e ∈ goodPairs (!θ)) :
    fixtureKernel.row (!θ) e = blindKernel.row θ e := by
  funext y
  have ha := (mem_goodPairs (!θ) e).mp he
  simp [fixtureKernel,Controller.Fixture.kernel,blindKernel,ha]

/-- Positive probability of failure under the exact mixed program/decoder pair
of the inherited runtime mutation. The actual model is fixed before tape choice. -/
theorem exact_runtime_mutant_positive_failure (d : Bool × Bool) :
    0 < fairCantor {x |
      ¬ ParitySuccess (actionPriority initialCandidate) (historyAction d
        (decodedHistory (policyProgram oldConfig)
          (sourcePolicy (withComputedTolerance oldConfig)) initialCandidate x))} := by
  have hp := positive_opposite_failure initialCandidate blindKernel blindKernel_positive
    (fixture_blind_agree initialCandidate) d
  have hl := mixed_runtime_blind_history_law (policyProgram oldConfig)
    (sourcePolicy oldConfig) (sourcePolicy (withComputedTolerance oldConfig))
    (policy_program_implements oldConfig) initialCandidate old_source_constant
  change 0 < ((markovHistoryLaw blindKernel initialCandidate false computedDecoder
    (Measure.dirac ())).map (historyAction d)) {x | ¬ ParitySuccess (actionPriority initialCandidate) x} at hp
  change fairCantor.map (decodedHistory (policyProgram oldConfig)
    (sourcePolicy (withComputedTolerance oldConfig)) initialCandidate) =
      markovHistoryLaw blindKernel initialCandidate false computedDecoder (Measure.dirac ()) at hl
  have hm : MeasurableSet {x : ℕ → Bool × Bool | ¬ ParitySuccess (actionPriority initialCandidate) x} :=
    (paritySuccess_measurable (actionPriority initialCandidate)).compl
  rw [← hl,Measure.map_map (historyAction_measurable d)
    (decodedHistory_measurable _ _ _),Measure.map_apply
      ((historyAction_measurable d).comp (decodedHistory_measurable _ _ _))
      hm] at hp
  exact hp

theorem exact_runtime_mutant_not_ae (d : Bool × Bool) :
    ¬ (∀ᵐ x ∂fairCantor,
      ParitySuccess (actionPriority initialCandidate) (historyAction d
        (decodedHistory (policyProgram oldConfig)
          (sourcePolicy (withComputedTolerance oldConfig)) initialCandidate x))) := by
  intro h
  exact (exact_runtime_mutant_positive_failure d).ne' (ae_iff.mp h)

/-- The unchanged computed/computed conclusion remains true on the same fully
certified, nonzero-priority fixture. -/
theorem exact_runtime_positive_control (d : Bool × Bool) :
    ∀ᵐ x ∂fairCantor,
      ParitySuccess (actionPriority initialCandidate) (historyAction d
        (decodedHistory (policyProgram (withComputedTolerance oldConfig))
          (sourcePolicy (withComputedTolerance oldConfig)) initialCandidate x)) := by
  exact full_phase_computed_tolerance_decoded_parity oldConfig bothMenu actionPriority
    oldConfig_certificate rfl rfl oldConfig_winning initialCandidate (Finset.mem_univ _) d

/-- Exact statement form of the one changed inherited theorem. This repeats
all hypotheses, including initial winningness and the supplied finite certificate. -/
def MutatedRuntimeClaim : Prop :=
  ∀ (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ),
    Certificate c menu priority → c.kernel = Controller.Fixture.kernel →
    c.initialState = false →
    c.initialState ∈ winningRegion c.kernel menu priority c.initialSupport →
    ∀ (σ : Bool), σ ∈ c.initialSupport → ∀ (d : Bool × Bool),
      ∀ᵐ x ∂fairCantor,
        ParitySuccess (priority σ) (historyAction d
          (decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x))

/-- A kernel-certified existential configuration suffices to refute the exact
universal mutant. This does not claim execution of evaluated selector numerals. -/
theorem exact_mutated_runtime_claim_false : ¬ MutatedRuntimeClaim := by
  intro h
  exact exact_runtime_mutant_not_ae (false,false)
    (h oldConfig bothMenu actionPriority oldConfig_certificate rfl rfl oldConfig_winning
      initialCandidate (Finset.mem_univ _) (false,false))

end Orthemology.Eighth.SemanticControls
