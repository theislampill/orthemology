import SCCGlobalParityIff

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Necessity HiddenParity.SCCController
open HiddenParity.Adaptive
open HiddenParity.Stochastic
set_option linter.unusedSectionVars false

namespace IndependentSCCIffReview
universe u v w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

theorem public_root_is_scc_recursion
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) :
    SCCRegion.winningRegion P menu priority B =
      SCCRegion.computedRegion P menu priority B.card B := rfl

theorem public_stage_calls_scc_target
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) (W : Finset State) :
    SCCRegion.regionStep P menu priority B lower W = W.filter (fun s => ∀ θ ∈ B,
      Stage.ReachableExit P B θ (regionAllowed P menu B lower W) s ∨
      ∃ t ∈ SCCPruning.markovTarget P Prod.fst B priority θ (regionAllowed P menu B lower W),
        Reach Prod.fst (internalSuccessors P B) (regionAllowed P menu B lower W) s t) := rfl

theorem accepted_witness_is_lawful
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action)
    (hs : s ∈ SCCRegion.winningRegion P menu priority B) :
    let w := sccAcceptedWinningPolicy P menu priority B s d hs
    Lawful P menu B s w.policy w.seedLaw := by
  exact (sccAcceptedWinningPolicy P menu priority B s d hs).lawful

theorem accepted_witness_has_actual_parity
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action)
    (hs : s ∈ SCCRegion.winningRegion P menu priority B) :
    let w := sccAcceptedWinningPolicy P menu priority B s d hs
    ∀ σ ∈ B, ∀ᵐ H ∂Stochastic.markovHistoryLaw P σ s w.policy w.seedLaw,
      ParitySuccess (priority σ) (historyAction d H) := by
  exact (sccAcceptedWinningPolicy P menu priority B s d hs).parity

/-- Determinism follows from the Unit domain; this does not unfold any
Classical.choice-selected policy field or identify it by rfl. -/
theorem accepted_witness_unit_seed_irrelevant
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action)
    (hs : s ∈ SCCRegion.winningRegion P menu priority B) (r r' : Unit)
    (h : History Action State) :
    (sccAcceptedWinningPolicy P menu priority B s d hs).policy r h =
      (sccAcceptedWinningPolicy P menu priority B s d hs).policy r' h := by
  cases r
  cases r'
  rfl

theorem arbitrary_seed_policy_enters_public_scc_region
    {R : Type v} [MeasurableSpace R]
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action)
    (w : WinningPolicy (R := R) P menu priority d B s) :
    s ∈ SCCRegion.winningRegion P menu priority B :=
  SCCRegion.winning_policy_mem_winningRegion P menu priority d B s w

theorem empty_support_public_rejects
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ) :
    SCCRegion.winningRegion P menu priority ∅ = ∅ := rfl

open HiddenParity.Sufficiency.ControllerControls

theorem coin_public_acceptance_yields_common_witness :
    SemanticWinning (R := Unit) coinKernel menu oppositePriority (0,0) Finset.univ 0 := by
  exact (scc_region_iff_common_parity_policy coinKernel menu oppositePriority Finset.univ 0 (0,0)).mp
    (by rw [scc_coin_accepts]; exact Finset.mem_univ _)

theorem identical_rows_public_rejection_rules_out_common_witness :
    ¬ SemanticWinning (R := Unit) indistinguishableKernel menu oppositePriority (0,0) Finset.univ 0 := by
  intro h
  have hm := (scc_region_iff_common_parity_policy indistinguishableKernel menu oppositePriority Finset.univ 0 (0,0)).mpr h
  rw [scc_indistinguishable_rejects] at hm
  exact Finset.not_mem_empty _ hm

end IndependentSCCIffReview
