import FullControllerReceiptLaw
import ComputedToleranceSource
import CanonicalHistoryBinding
set_option autoImplicit false

/-! Full Boolean source → actual P02 output → common measurable history readout
→ the retained canonical Markov law and decoded parity success. All classical
finite selector bindings and the fixed simulated-environment match are explicit. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate.FullController
open MeasureTheory
open Orthemology.Frontier.MealyMeasure
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw Orthemology.RationalLaw.RuntimeBinding Orthemology.RationalLaw.CanonicalBinding
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.CertifiedObserver
open P02A2.Q8Measure (fairCantor)
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity

/-- The source's sole common history policy is literally the retained generated
phase policy at the supplied rational tolerance on every acquired history. -/
theorem source_history_policy_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    historyPolicy (sourcePolicy c) = (fun (_ : Unit) h => policy c menu priority h) := by
  funext u h
  exact source_policy_retained_exact c menu priority hc h

/-- Exact complete canonical history-law equality, derived through finite
cylinders rather than supplied as a compiler or controller hypothesis. -/
theorem full_phase_runtime_canonical_history_law (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (hinit : c.initialState = false) (σ : Bool) :
    fairCantor.map (decodedHistory (policyProgram c) (sourcePolicy c) σ) =
      markovHistoryLaw c.kernel σ c.initialState (fun (_ : Unit) h => policy c menu priority h)
        (Measure.dirac ()) := by
  simpa only [source_history_policy_exact c menu priority hc,hkernel,hinit] using
    actual_runtime_canonical_history_law (policyProgram c) (sourcePolicy c) (policy_program_implements c) σ

/-- The readout takes only the physical output stream and common policy. It does
not inspect the hidden-model index or original input tape. -/
theorem full_phase_physical_projected_canonical_law (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (hinit : c.initialState = false) (σ : Bool) :
    (fairCantor.map (Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ))).map
      (canonicalHistoryDecoder (sourcePolicy c)) =
      markovHistoryLaw c.kernel σ c.initialState (fun (_ : Unit) h => policy c menu priority h)
        (Measure.dirac ()) := by
  simpa only [source_history_policy_exact c menu priority hc,hkernel,hinit] using
    physical_runtime_projected_canonical_law (policyProgram c) (sourcePolicy c) (policy_program_implements c) σ

/-- Actual full-phase source with a computed rational tolerance is almost surely
winning after the explicit history readout, whenever the retained region says
so. Two models/states/actions and supplied exact finite selector bindings remain.
This is not a parity or nonatomic-defect claim about the raw Boolean stream. -/
theorem full_phase_computed_tolerance_decoded_parity (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (hinit : c.initialState = false)
    (hs : c.initialState ∈ winningRegion c.kernel menu priority c.initialSupport)
    (σ : Bool) (hσ : σ ∈ c.initialSupport) (d : Bool × Bool) :
    ∀ᵐ x ∂fairCantor,
      ParitySuccess (priority σ) (historyAction d
        (decodedHistory (policyProgram (withComputedTolerance c)) (sourcePolicy (withComputedTolerance c)) σ x)) := by
  have hw := computed_policy_parity c menu priority hs σ hσ d
  have hl := full_phase_runtime_canonical_history_law (withComputedTolerance c) menu priority
    (computed_tolerance_certificate c menu priority hc) hkernel hinit σ
  rw [show (withComputedTolerance c).kernel = c.kernel from rfl,
    show (withComputedTolerance c).initialState = c.initialState from rfl] at hl
  rw [← hl] at hw
  exact ae_of_ae_map
    (decodedHistory_measurable (policyProgram (withComputedTolerance c))
      (sourcePolicy (withComputedTolerance c)) σ).aemeasurable hw

/-- The same success statement is a property of a common measurable decoder of
the actual physical output law, with no hidden model in the observation map. -/
theorem full_phase_computed_tolerance_output_parity (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (hkernel : c.kernel = Controller.Fixture.kernel)
    (hinit : c.initialState = false)
    (hs : c.initialState ∈ winningRegion c.kernel menu priority c.initialSupport)
    (σ : Bool) (hσ : σ ∈ c.initialSupport) (d : Bool × Bool) :
    ∀ᵐ z ∂fairCantor.map (Indexed.runtimeOutput (runtimeIndex (policyProgram (withComputedTolerance c)) σ)),
      ParitySuccess (priority σ) (historyAction d (canonicalHistoryDecoder (sourcePolicy (withComputedTolerance c)) z)) := by
  have hw := computed_policy_parity c menu priority hs σ hσ d
  have hl := full_phase_physical_projected_canonical_law (withComputedTolerance c) menu priority
    (computed_tolerance_certificate c menu priority hc) hkernel hinit σ
  rw [show (withComputedTolerance c).kernel = c.kernel from rfl,
    show (withComputedTolerance c).initialState = c.initialState from rfl] at hl
  rw [← hl] at hw
  exact ae_of_ae_map (canonicalHistoryDecoder_measurable (sourcePolicy (withComputedTolerance c))).aemeasurable hw

end Orthemology.RuntimeBridge.PhaseUpdate.FullController
