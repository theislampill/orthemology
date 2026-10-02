import RationalEmpiricalGate
import GlobalParitySufficiency
import AcceptedFixtureController

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace Orthemology.RuntimeBridge.RationalGate
open HiddenParity HiddenParity.Stochastic HiddenParity.Sufficiency HiddenParity.Stage HiddenParity.Necessity
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The actual accepted generator admits an explicit rational guard and tolerance,
with its original almost-sure success theorem. Finite classical selectors remain. -/
theorem rational_gate_parity
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (fallback : Model) (fallbackAction : Action)
    (hs : s ∈ winningRegion P menu priority B) (σ : Model) (hσ : σ ∈ B) (d : State × Action) :
    ∀ᵐ H ∂markovHistoryLaw P σ s
      (generatedPhasePolicy P menu priority B s fallback fallbackAction (reject P (tolerance P B)))
      (Measure.dirac ()), ParitySuccess (priority σ) (historyAction d H) := by
  have he : reject P (tolerance P B) = empiricalReject P (tolerance P B : ℝ) := by
    funext θ k h
    exact reject_exact P _ θ k h
  rw [he]
  have ht := tolerance_real_spec P B
  exact generatedPhasePolicy_parity P menu priority B s fallback fallbackAction _ ht.1 hs σ hσ
    (fun θ hθ e hne => ht.2 θ hθ σ hσ e hne) d

end Orthemology.RuntimeBridge.RationalGate

namespace Orthemology.RuntimeBridge.RationalGate.Controls
open Controller.Fixture
open Orthemology.Tranche2.PolicyEmbedding

/-- Two acquired receipts at one source/action have empirical frequency 1/2. -/
def testHistory : History (Bool × Bool) Bool := [((false,false),true),((false,false),false)]

/-- Both positive tolerances separate the two 1/3-versus-2/3 model rows, yet
substituting one for the other changes a literal observed-history guard. -/
theorem tolerance_substitution_changes_decision :
    (0 : ℚ) < 1/10 ∧ (1/10 : ℚ) < 1/3 ∧
    (0 : ℚ) < 1/5 ∧ (1/5 : ℚ) < 1/3 ∧
    reject kernel (1/10) false 0 testHistory = true ∧
    reject kernel (1/5) false 0 testHistory = false := by
  norm_num [reject,testHistory,frequency,symbolCount,actionCount,Controller.Fixture.kernel,
    List.countP_cons,Prod.exists]
  norm_num [abs_of_pos (show (0 : ℚ) < 1/6 by norm_num)]

end Orthemology.RuntimeBridge.RationalGate.Controls
