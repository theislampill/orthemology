import SelectorSemanticTransport
import LiteralRuntimeCounterexample
set_option autoImplicit false

/-! Conditional counterexample extraction from supplied original certified Data.
The model is computed from the supplied finite numeral, before all tapes. -/
namespace Orthemology.Ninth.CertifiedSelectorFamily
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

/-- Reuse the exact literal fields with the supplied selector record. The false
argument contributes no retained selector after replacement. -/
def suppliedConfig (d : FiniteSelectorSource.Data) : Config :=
  { literalConfig false with selectors := d }

theorem suppliedConfig_selectors (d : FiniteSelectorSource.Data) :
    (suppliedConfig d).selectors = d := rfl

theorem suppliedConfig_literal (o : Bool) :
    suppliedConfig (literalData o) = literalConfig o := rfl

theorem suppliedConfig_kernel (d : FiniteSelectorSource.Data) :
    (suppliedConfig d).kernel = Controller.Fixture.kernel := rfl

theorem suppliedConfig_initialState (d : FiniteSelectorSource.Data) :
    (suppliedConfig d).initialState = false := rfl

theorem suppliedConfig_initialSupport (d : FiniteSelectorSource.Data) :
    (suppliedConfig d).initialSupport = Finset.univ := rfl

/-- No additional selector assumption is introduced by packaging the Data. -/
theorem suppliedConfig_certificate (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority) :
    Certificate (suppliedConfig d) sparseMenu actionPriority := by
  have hl := literalConfig_certificate (recoveredOrientation d)
    (recoveredOrientation_exact d hc).symm
  exact ⟨hc, hl.toleranceDenominator_pos, hl.rowDenominator_pos, hl.row_exact⟩

theorem suppliedConfig_certificate_iff (d : FiniteSelectorSource.Data) :
    Certificate (suppliedConfig d) sparseMenu actionPriority ↔
      FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority :=
  ⟨fun h => h.selectors, suppliedConfig_certificate d⟩

theorem suppliedConfig_winning (d : FiniteSelectorSource.Data) :
    (suppliedConfig d).initialState ∈ winningRegion (suppliedConfig d).kernel
      sparseMenu actionPriority (suppliedConfig d).initialSupport :=
  literalConfig_winning false

theorem suppliedConfig_model_member (d : FiniteSelectorSource.Data) :
    recoveredOrientation d ∈ (suppliedConfig d).initialSupport := Finset.mem_univ _

/-- Canonical Config equality is conditional on the original, full certificate. -/
theorem suppliedConfig_normalized (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority) :
    normalizeConfig (suppliedConfig d) = literalConfig (recoveredOrientation d) := by
  change suppliedConfig (normalizeData d) = _
  rw [normalized_eq_recovered_literal d hc, suppliedConfig_literal]

/-- Exact agreement on every acquired finite history; no raw-input extension. -/
theorem suppliedConfig_source_history (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (h : HistoryFold.History) :
    sourcePolicy (suppliedConfig d) (HistoryRuntime.encodeHistory h) =
      sourcePolicy (literalConfig (recoveredOrientation d)) (HistoryRuntime.encodeHistory h) := by
  have he := normalized_source_history (suppliedConfig d) sparseMenu actionPriority
    (suppliedConfig_certificate d hc) h
  rw [suppliedConfig_normalized d hc] at he
  exact he.symm

/-- Physical frames agree for all tapes and coordinates in the existing wrapper. -/
theorem suppliedConfig_runtime_output (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (σ : Bool) :
    Indexed.runtimeOutput (HistoryRuntime.runtimeIndex (policyProgram (suppliedConfig d)) σ) =
      Indexed.runtimeOutput (HistoryRuntime.runtimeIndex
        (policyProgram (literalConfig (recoveredOrientation d))) σ) := by
  have he := normalized_runtime_output (suppliedConfig d) sparseMenu actionPriority
    (suppliedConfig_certificate d hc) σ
  rw [suppliedConfig_normalized d hc] at he
  exact he.symm

/-- Old execution and computed-tolerance decoding remain distinct roles. -/
theorem suppliedConfig_mixed_history (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (σ : Bool) :
    decodedHistory (policyProgram (suppliedConfig d))
      (sourcePolicy (withComputedTolerance (suppliedConfig d))) σ =
    decodedHistory (policyProgram (literalConfig (recoveredOrientation d)))
      (sourcePolicy (withComputedTolerance (literalConfig (recoveredOrientation d)))) σ := by
  have he := normalized_old_computed_decodedHistory (suppliedConfig d) sparseMenu
    actionPriority (suppliedConfig_certificate d hc) σ
  rw [suppliedConfig_normalized d hc] at he
  exact he.symm

/-- The model recovered from d is fixed outside the complete failure event. -/
theorem suppliedConfig_positive_failure (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority)
    (fallback : Bool × Bool) :
    0 < fairCantor {x | ¬ ParitySuccess (actionPriority (recoveredOrientation d))
      (historyAction fallback (decodedHistory (policyProgram (suppliedConfig d))
        (sourcePolicy (withComputedTolerance (suppliedConfig d))) (recoveredOrientation d) x))} := by
  rw [suppliedConfig_mixed_history d hc]
  exact literal_runtime_positive_failure (recoveredOrientation d)
    (recoveredOrientation_exact d hc).symm fallback

/-- All original Config, environment, winningness and actual-model hypotheses
are explicit; the supplied Data and the actual model precede all tapes. -/
def CertifiedSuppliedFailure (d : FiniteSelectorSource.Data) : Prop :=
  (suppliedConfig d).selectors = d ∧
  Certificate (suppliedConfig d) sparseMenu actionPriority ∧
  (suppliedConfig d).kernel = Controller.Fixture.kernel ∧
  (suppliedConfig d).initialState = false ∧
  (suppliedConfig d).initialState ∈ winningRegion (suppliedConfig d).kernel
    sparseMenu actionPriority (suppliedConfig d).initialSupport ∧
  recoveredOrientation d ∈ (suppliedConfig d).initialSupport ∧
  ∀ fallback : Bool × Bool, 0 < fairCantor {x | ¬ ParitySuccess
    (actionPriority (recoveredOrientation d)) (historyAction fallback
      (decodedHistory (policyProgram (suppliedConfig d))
        (sourcePolicy (withComputedTolerance (suppliedConfig d))) (recoveredOrientation d) x))}

/-- Uniform conditional family extraction, with no closed choice evaluation. -/
theorem certified_supplied_failure (d : FiniteSelectorSource.Data)
    (hc : FiniteSelectorSource.Certificate d fixtureKernel sparseMenu actionPriority) :
    CertifiedSuppliedFailure d :=
  ⟨suppliedConfig_selectors d, suppliedConfig_certificate d hc, suppliedConfig_kernel d,
    suppliedConfig_initialState d, suppliedConfig_winning d, suppliedConfig_model_member d,
    suppliedConfig_positive_failure d hc⟩

end Orthemology.Ninth.CertifiedSelectorFamily
