import CertifiedSelectorFamily
set_option autoImplicit false

namespace Orthemology.Ninth.CertifiedSelectorFamily.Reviewer
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.CertifiedObserver
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.Eighth.SemanticControls
open Orthemology.Eighth.SemanticControls.LiteralAssessment
open Orthemology.Ninth.SelectorExtraction
open Orthemology.Ninth.SelectorTransport
open P02A2.Q8Measure (fairCantor)

/-- Direct numeric/record consumer check: no false-orientation selector survives replacement. -/
theorem supplied_record_fields (d : FiniteSelectorSource.Data) :
    (suppliedConfig d).selectors = d ∧
    (suppliedConfig d).toleranceNumerator = 2 ∧
    (suppliedConfig d).toleranceDenominator = 1 ∧
    (suppliedConfig d).rowDenominator = 3 ∧
    (suppliedConfig d).initialSupport = Finset.univ ∧
    (suppliedConfig d).initialState = false ∧
    (suppliedConfig d).fallbackModel = false ∧
    (suppliedConfig d).fallbackAction = false :=
  ⟨rfl,rfl,rfl,rfl,rfl,rfl,rfl,rfl⟩

/-- The actual model is exactly a bit read from d, with no input tape argument. -/
theorem recovered_model_is_bit_twelve (d : FiniteSelectorSource.Data) :
    recoveredOrientation d = decide (d.cycleTable / 4096 % 2 = 1) := by
  change decide (d.cycleTable / 2^(cellIndex Finset.univ false false).val % 2 = 1) = _
  rw [show (cellIndex Finset.univ false false).val = 12 by decide]
  rfl

/-- The family wrapper neither strengthens nor weakens the original data certificate. -/
theorem supplied_failure_iff_original_certificate (d : FiniteSelectorSource.Data) :
    CertifiedSuppliedFailure d ↔
      FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority := by
  constructor
  · intro h
    exact h.2.1.selectors
  · exact certified_supplied_failure d

/-- All inherited endpoint premises appear before the tape/event quantifiers. -/
theorem original_consumer_premises (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority) :
    ∃ σ : Bool, σ = recoveredOrientation d ∧
      Certificate (suppliedConfig d) sparseMenu actionPriority ∧
      (suppliedConfig d).kernel = Controller.Fixture.kernel ∧
      (suppliedConfig d).initialState = false ∧
      (suppliedConfig d).initialState ∈ winningRegion (suppliedConfig d).kernel
        sparseMenu actionPriority (suppliedConfig d).initialSupport ∧
      σ ∈ (suppliedConfig d).initialSupport ∧
      ∀ fallback : Bool × Bool, 0 < fairCantor {x | ¬ ParitySuccess (actionPriority σ)
        (historyAction fallback (decodedHistory (policyProgram (suppliedConfig d))
          (sourcePolicy (withComputedTolerance (suppliedConfig d))) σ x))} :=
  ⟨recoveredOrientation d,rfl,suppliedConfig_certificate d hc,suppliedConfig_kernel d,
    suppliedConfig_initialState d,suppliedConfig_winning d,suppliedConfig_model_member d,
    suppliedConfig_positive_failure d hc⟩

/-- The family contains every ignored-high-digit extension, not only literal data. -/
theorem supplied_failure_high_digits (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (c t s : ℕ) : CertifiedSuppliedFailure (addHighDigits d c t s) :=
  certified_supplied_failure _
    ((certificate_addHighDigits_iff d c t s fixtureKernel sparseMenu actionPriority).mpr hc)

theorem high_digits_preserve_recovered_model (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (c t s : ℕ) : recoveredOrientation (addHighDigits d c t s) = recoveredOrientation d := by
  have hh := (certificate_addHighDigits_iff d c t s fixtureKernel sparseMenu actionPriority).mpr hc
  exact (recoveredOrientation_exact _ hh).trans (recoveredOrientation_exact d hc).symm

/-- The old executed action is the recovered actual model on every acquired history. -/
theorem supplied_old_action_constant (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (h : HistoryFold.History) :
    sourcePolicy (suppliedConfig d) (HistoryRuntime.encodeHistory h) = recoveredOrientation d := by
  rw [suppliedConfig_source_history d hc]
  exact literal_old_source_constant (recoveredOrientation d) (recoveredOrientation_exact d hc).symm h

/-- The positive failure conclusion concerns a measurable event, not just an outer-measure assertion. -/
theorem supplied_mixed_failure_measurable (d : FiniteSelectorSource.Data) (fallback : Bool × Bool) :
    MeasurableSet {x | ¬ ParitySuccess (actionPriority (recoveredOrientation d))
      (historyAction fallback (decodedHistory (policyProgram (suppliedConfig d))
        (sourcePolicy (withComputedTolerance (suppliedConfig d))) (recoveredOrientation d) x))} := by
  exact (paritySuccess_measurable (actionPriority (recoveredOrientation d))).compl.preimage
    ((historyAction_measurable fallback).comp (decodedHistory_measurable _ _ _))

/-- The independently matching computed/computed pairing retains the inherited success theorem. -/
theorem supplied_matching_computed_positive_control (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (fallback : Bool × Bool) :
    ∀ᵐ x ∂fairCantor, ParitySuccess (actionPriority (recoveredOrientation d))
      (historyAction fallback (decodedHistory (policyProgram (withComputedTolerance (suppliedConfig d)))
        (sourcePolicy (withComputedTolerance (suppliedConfig d))) (recoveredOrientation d) x)) :=
  full_phase_computed_tolerance_decoded_parity (suppliedConfig d) sparseMenu actionPriority
    (suppliedConfig_certificate d hc) (suppliedConfig_kernel d) (suppliedConfig_initialState d)
    (suppliedConfig_winning d) (recoveredOrientation d) (suppliedConfig_model_member d) fallback

/-- The supplied mixed failure cannot be silently relabelled as a matching-readout failure. -/
theorem supplied_mixed_not_matching (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority) :
    decodedHistory (policyProgram (suppliedConfig d))
      (sourcePolicy (withComputedTolerance (suppliedConfig d))) (recoveredOrientation d) ≠
    decodedHistory (policyProgram (withComputedTolerance (suppliedConfig d)))
      (sourcePolicy (withComputedTolerance (suppliedConfig d))) (recoveredOrientation d) := by
  intro h
  have hp := suppliedConfig_positive_failure d hc (false,false)
  rw [h] at hp
  exact hp.ne' (ae_iff.mp (supplied_matching_computed_positive_control d hc (false,false)))

#print axioms supplied_record_fields
#print axioms recovered_model_is_bit_twelve
#print axioms supplied_failure_iff_original_certificate
#print axioms original_consumer_premises
#print axioms supplied_failure_high_digits
#print axioms high_digits_preserve_recovered_model
#print axioms supplied_old_action_constant
#print axioms supplied_mixed_failure_measurable
#print axioms supplied_matching_computed_positive_control
#print axioms supplied_mixed_not_matching
end Orthemology.Ninth.CertifiedSelectorFamily.Reviewer
