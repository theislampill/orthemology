import ExplicitWinningRecord

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.IndependentExplicit
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
universe u w
variable {S A : Type u} {M : Type w}
variable [Fintype S] [Fintype A] [DecidableEq S] [DecidableEq A] [Inhabited S] [DecidableEq M]
variable [MeasurableSpace S] [MeasurableSingletonClass S] [MeasurableSpace A] [MeasurableSingletonClass A]
variable (P : RationalKernel M (S × A) S) (menu : Finset M → S → Finset A)
variable (priority : M → (S × A) → Nat) (B : Finset M) (hB : B.Nonempty)
variable (s : S) (hs : s ∈ winningRegion P menu priority B) (d : S × A)
set_option linter.unusedSectionVars false

/-- This independent rfl probe expands all the way to the literal generator. -/
theorem literal_generator_field :
    (ExplicitController.winningRecord P menu priority B hB s hs d).policy =
      generatedPhasePolicy P menu priority B s (Classical.choose hB) d.2
        (empiricalReject P (ExplicitController.tolerance P B)) := rfl

theorem literal_dirac_field :
    (ExplicitController.winningRecord P menu priority B hB s hs d).seedLaw = Measure.dirac () := rfl

include hs in
theorem literal_generator_measurable :
    Measurable (fun z : Unit × History A S =>
      ExplicitController.policy P menu priority B hB s d z.1 z.2) :=
  (ExplicitController.winningRecord P menu priority B hB s hs d).measurable

include hs in
/-- The actual history law uses the literal generator and exact Dirac law. -/
theorem literal_generator_common_success :
    ∀ θ ∈ B, ∀ᵐ H ∂markovHistoryLaw P θ s
      (ExplicitController.policy P menu priority B hB s d) (Measure.dirac ()),
      ParitySuccess (priority θ) (historyAction d H) :=
  (ExplicitController.winningRecord P menu priority B hB s hs d).parity

include hs in
theorem literal_generator_lawful :
    Lawful P menu B s (ExplicitController.policy P menu priority B hB s d) (Measure.dirac ()) :=
  (ExplicitController.winningRecord P menu priority B hB s hs d).lawful

theorem tolerance_positive : 0 < ExplicitController.tolerance P B :=
  (Classical.choose_spec (finite_row_separation P B)).1

theorem policy_ignores_dummy_source (d' : S × A) (h : d.2 = d'.2) :
    ExplicitController.policy P menu priority B hB s d =
      ExplicitController.policy P menu priority B hB s d' := by
  unfold ExplicitController.policy
  rw [h]

end HiddenParity.IndependentExplicit
