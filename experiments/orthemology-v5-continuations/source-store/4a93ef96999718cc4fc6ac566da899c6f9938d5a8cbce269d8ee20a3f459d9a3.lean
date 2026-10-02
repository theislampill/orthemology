import GeneratedParitySuccess

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u v w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Actual almost-sure parity for the generated state/history controller. All
raw-tape regularity and test correctness properties are derived from the actual
normalized rows; no fairness, success, termination or law-equivalence premise
is used to replace the policy construction. -/
theorem generatedPhasePolicy_parity
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (ε : ℝ) (hε : 0 < ε) (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (σ : Model) (hσ : σ ∈ B₀)
    (hSep : ∀ θ ∈ B₀, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P θ e y|) (d : State × Action) :
    ∀ᵐ H ∂markovHistoryLaw P σ s₀
      (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε)) (Measure.dirac ()),
      ParitySuccess (priority σ) (historyAction d H) := by
  let π := generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε)
  have hπ := generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε)
  have hAction : ∀ᵐ x ∂markovPairLaw P σ s₀ π (Measure.dirac ()) d, ParitySuccess (priority σ) x := by
    apply actionLaw_ae_of_stack (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
      (Measure.dirac ()) (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) d _
      (paritySuccess_measurable (priority σ))
    filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ),
      seeded_all_tapes_recurrent (Measure.dirac ()) (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ),
      empiricalReject_true_eventually_never P σ (Measure.dirac ()) ε hε,
      empiricalReject_recurrent_mismatch P B₀ σ hσ (Measure.dirac ()) ε hSep]
      with z hSupported hTape hTrue hFalse
    apply generated_stack_parity P menu priority B₀ s₀ fallback fallbackAction ε hs₀ σ hσ z hSupported hTape
    · obtain ⟨K,hK⟩ := hTrue
      exact ⟨K,fun k hk n => hK k hk (pairPolicy s₀ π) n⟩
    · intro θ hθ e he hNe k
      exact hFalse (pairPolicy s₀ π) θ hθ e he hNe k
  exact ae_of_ae_map (historyAction_measurable d).aemeasurable hAction

/-- A genuine common lawful winning policy is constructed from every nonempty
computed winning support/state. All finite choices are shared before the true
model is quantified. Unit seed makes the policy deterministic. -/
def computedRegionWinningPolicy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (hB : B₀.Nonempty) (s₀ : State)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (d : State × Action) :
    WinningPolicy (R := Unit) P menu priority d B₀ s₀ := by
  apply Classical.choice
  obtain ⟨fallback,hFallback⟩ := hB
  have hAvail := winningRegion_safe_action_available P menu priority B₀ ⟨fallback,hFallback⟩ s₀ hs₀
  obtain ⟨e,he,hes⟩ := Finset.mem_image.mp hAvail
  obtain ⟨ε,hε,hSep⟩ := finite_row_separation P B₀
  let π := generatedPhasePolicy P menu priority B₀ s₀ fallback e.2 (empiricalReject P ε)
  refine ⟨⟨⟨fallback,hFallback⟩,Measure.dirac (),inferInstance,π,
    generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback e.2 (empiricalReject P ε),
    generatedPhasePolicy_lawful P menu priority B₀ s₀ hs₀ fallback e.2 (empiricalReject P ε),?_⟩⟩
  intro σ hσ
  exact generatedPhasePolicy_parity P menu priority B₀ s₀ fallback e.2 ε hε hs₀ σ hσ
    (fun θ hθ a hNe => hSep θ hθ σ hσ a hNe) d

/-- Empty support cannot create a spurious computed winner. -/
theorem winningRegion_mem_support_nonempty
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (hs : s ∈ winningRegion P menu priority B) : B.Nonempty := by
  by_contra hNot
  have hEmpty : B = ∅ := Finset.not_nonempty_iff_eq_empty.mp hNot
  simp only [hEmpty,winningRegion,Finset.card_empty,computedRegion,Finset.not_mem_empty] at hs

/-- Full observed-state hidden-priority characterization for this finite rational
input model and the proved almost-sure finite-history lawfulness contract. The
solver is the finite exhaustive target reference, not a polynomial runtime claim. -/
theorem computed_region_iff_common_parity_policy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action) :
    s ∈ winningRegion P menu priority B ↔ SemanticWinning (R := Unit) P menu priority d B s := by
  constructor
  · intro hs
    exact ⟨computedRegionWinningPolicy P menu priority B
      (winningRegion_mem_support_nonempty P menu priority B s hs) s hs d⟩
  · rintro ⟨w⟩
    exact winning_policy_mem_winningRegion P menu priority d B s w

/-- Every successful common policy with any measurable private seed space has a
generated deterministic history-policy witness for the same input and objective.
This is existence of a witness, not equality of the original policy laws. -/
theorem arbitrary_seed_winning_has_deterministic_witness {R : Type v} [MeasurableSpace R]
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (s : State) (d : State × Action)
    (w : WinningPolicy (R := R) P menu priority d B s) :
    SemanticWinning (R := Unit) P menu priority d B s := by
  exact (computed_region_iff_common_parity_policy P menu priority B s d).mp
    (winning_policy_mem_winningRegion P menu priority d B s w)

end HiddenParity.Sufficiency
