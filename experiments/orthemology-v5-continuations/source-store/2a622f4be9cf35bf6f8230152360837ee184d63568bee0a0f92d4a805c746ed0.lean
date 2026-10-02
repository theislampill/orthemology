import CanonicalHistoryBinding
import ExplicitRecordRuntimeBinding
set_option autoImplicit false

namespace Orthemology.RationalLaw.ExplicitRecordBinding
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.CertifiedObserver
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RuntimeBridge.Controller Orthemology.RuntimeBridge.Controller.Fixture
open Orthemology.RationalLaw.CanonicalBinding
open HiddenParity HiddenParity.Stochastic HiddenParity.Sufficiency HiddenParity.ExplicitController
open P02A2.Q8Measure (fairCantor)

/-- Exact complete law of the literal actual source after the common measurable
history decoder, equal to the retained explicit record with all choices unchanged. -/
theorem physical_runtime_explicit_record_law (σ : Bool) :
    (fairCantor.map (Indexed.runtimeOutput (runtimeIndex selectorProgram σ))).map
      (canonicalHistoryDecoder Orthemology.RuntimeBridge.HistoryRuntime.observedState) =
    markovHistoryLaw kernel σ false
      (winningRecord kernel (singletonMenu id) zeroPriority Finset.univ
        (by exact ⟨false,Finset.mem_univ _⟩) false initial_winning (false,false)).policy
      (winningRecord kernel (singletonMenu id) zeroPriority Finset.univ
        (by exact ⟨false,Finset.mem_univ _⟩) false initial_winning (false,false)).seedLaw := by
  rw [physical_runtime_projected_canonical_law selectorProgram
    Orthemology.RuntimeBridge.HistoryRuntime.observedState selector_program_exact]
  have hp : historyPolicy Orthemology.RuntimeBridge.HistoryRuntime.observedState = selectedPolicy id false := by
    funext u h
    cases u
    exact selector_retained_policy h
  rw [hp]
  exact (explicit_record_history_law σ).symm

end Orthemology.RationalLaw.ExplicitRecordBinding
