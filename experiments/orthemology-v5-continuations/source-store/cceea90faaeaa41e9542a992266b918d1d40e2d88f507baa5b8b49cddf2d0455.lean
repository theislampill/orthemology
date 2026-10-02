import GlobalParitySufficiency

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.ExplicitController
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The common tolerance is chosen once from the known finite input family. -/
def tolerance (P : RationalKernel Model (State × Action) State) (B : Finset Model) : ℝ :=
  Classical.choose (finite_row_separation P B)

/-- A definitionally exposed generated policy. Its two finite classical choices
are made from the initial support/table, before any true model is quantified. -/
def policy (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (hB : B.Nonempty) (s : State) (d : State × Action) :
    Unit → History Action State → Action :=
  generatedPhasePolicy P menu priority B s (Classical.choose hB) d.2 (empiricalReject P (tolerance P B))

/-- This record exposes its policy and seed-law fields directly. There is no
outer choice of an arbitrary element of Nonempty WinningPolicy. Classical
finite choices inside the generator remain; executable extraction is not claimed. -/
def winningRecord (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (hB : B.Nonempty) (s : State)
    (hs : s ∈ winningRegion P menu priority B) (d : State × Action) :
    WinningPolicy (R := Unit) P menu priority d B s where
  nonempty := hB
  seedLaw := Measure.dirac ()
  probability := inferInstance
  policy := policy P menu priority B hB s d
  measurable := generatedPhasePolicy_measurable P menu priority B s (Classical.choose hB) d.2 _
  lawful := generatedPhasePolicy_lawful P menu priority B s hs (Classical.choose hB) d.2 _
  parity := by
    intro σ hσ
    have hGap := Classical.choose_spec (finite_row_separation P B)
    exact generatedPhasePolicy_parity P menu priority B s (Classical.choose hB) d.2
      (tolerance P B) hGap.1 hs σ hσ (fun θ hθ e hNe => hGap.2 θ hθ σ hσ e hNe) d

/-- Literal policy-field identity, proved by reflexivity. -/
theorem winningRecord_policy (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (hB : B.Nonempty) (s : State)
    (hs : s ∈ winningRegion P menu priority B) (d : State × Action) :
    (winningRecord P menu priority B hB s hs d).policy = policy P menu priority B hB s d := rfl

/-- Literal seed-law identity, also proved by reflexivity. -/
theorem winningRecord_seedLaw (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (hB : B.Nonempty) (s : State)
    (hs : s ∈ winningRegion P menu priority B) (d : State × Action) :
    (winningRecord P menu priority B hB s hs d).seedLaw = Measure.dirac () := rfl

end HiddenParity.ExplicitController
