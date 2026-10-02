import SCCRegionAlgorithm
import GlobalControllerControls

noncomputable section
namespace HiddenParity.SCCController
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The actual SCC-substituted region computation has the full common-policy
characterization. Selector and recursive-region equality are proved imports,
not assumptions. The outer support recursion has no polynomial-time claim. -/
theorem scc_region_iff_common_parity_policy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action) :
    s ∈ SCCRegion.winningRegion P menu priority B ↔
      Necessity.SemanticWinning (R := Unit) P menu priority d B s := by
  rw [SCCRegion.winningRegion_eq]
  exact Sufficiency.computed_region_iff_common_parity_policy P menu priority B s d

/-- An accepted SCC-computed state yields the actual deterministic common
history-policy witness. This does not claim an extracted SCC runtime controller. -/
def sccAcceptedWinningPolicy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action)
    (hs : s ∈ SCCRegion.winningRegion P menu priority B) :
    Necessity.WinningPolicy (R := Unit) P menu priority d B s := by
  have hRef : s ∈ Necessity.winningRegion P menu priority B := by rwa [SCCRegion.winningRegion_eq] at hs
  exact Sufficiency.computedRegionWinningPolicy P menu priority B
    (Sufficiency.winningRegion_mem_support_nonempty P menu priority B s hRef) s hRef d

open Sufficiency.ControllerControls

/-- The SCC result accepts the hidden quarter-coin learning instance. -/
theorem scc_coin_accepts :
    SCCRegion.winningRegion coinKernel menu oppositePriority Finset.univ = Finset.univ := by
  rw [SCCRegion.winningRegion_eq]
  exact coin_full_region

/-- The same substitution preserves the observationally indistinguishable
opposite-objective impossibility control. -/
theorem scc_indistinguishable_rejects :
    SCCRegion.winningRegion indistinguishableKernel menu oppositePriority Finset.univ = ∅ := by
  rw [SCCRegion.winningRegion_eq]
  exact indistinguishable_region_empty

end HiddenParity.SCCController
