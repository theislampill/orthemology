import ExplicitWinningRecord
import AcceptedFixtureController
import EncodedPolicyHistory

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace Orthemology.RuntimeBridge.Controller.Fixture
open HiddenParity HiddenParity.Stochastic HiddenParity.Sufficiency HiddenParity.ExplicitController

/-- The literal retained explicit record, including its internal classical
choices, has exactly the concrete fixture selector's observed-history law. -/
theorem explicit_record_history_law (σ : Bool) :
    markovHistoryLaw kernel σ false
      (winningRecord kernel (singletonMenu id) zeroPriority Finset.univ
        (by exact ⟨false,Finset.mem_univ _⟩) false initial_winning (false,false)).policy
      (winningRecord kernel (singletonMenu id) zeroPriority Finset.univ
        (by exact ⟨false,Finset.mem_univ _⟩) false initial_winning (false,false)).seedLaw =
    markovHistoryLaw kernel σ false (selectedPolicy id false) (Measure.dirac ()) := by
  change markovHistoryLaw kernel σ false
    (generatedPhasePolicy kernel (singletonMenu id) zeroPriority Finset.univ false
      (Classical.choose (show (Finset.univ : Finset Bool).Nonempty from ⟨false,Finset.mem_univ _⟩)) false
      (empiricalReject kernel (HiddenParity.ExplicitController.tolerance kernel Finset.univ))) (Measure.dirac ()) = _
  exact generated_singleton_law kernel id zeroPriority Finset.univ false initial_winning
    _ false _ σ (Finset.mem_univ _)

/-- Source-program policy identity on all acquired histories supplies the exact
selector used on the right of the retained explicit-record law theorem. -/
theorem source_selector_history_identity (h : History Bool Bool) :
    HistoryRuntime.observedState (HistoryRuntime.encodeHistory h) = selectedPolicy id false () h :=
  HistoryRuntime.selector_retained_policy h

end Orthemology.RuntimeBridge.Controller.Fixture
