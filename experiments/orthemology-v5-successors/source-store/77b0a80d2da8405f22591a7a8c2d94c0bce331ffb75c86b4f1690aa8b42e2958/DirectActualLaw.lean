import DirectParity

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding

namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u v w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [LinearOrder Action] [Inhabited State]
variable [DecidableEq Model] [LinearOrder Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Actual almost-sure parity for the generated state/history controller. All
raw-tape regularity and test correctness properties are derived from the actual
normalized rows; no fairness, success, termination or law-equivalence premise
is used to replace the policy construction. -/
theorem generatedPhasePolicy_parity
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (ε : ℝ) (hε : 0 < ε) (hs₀ : s₀ ∈ F.states B₀)
    (σ : Model) (hσ : σ ∈ B₀)
    (hSep : ∀ θ ∈ B₀, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P θ e y|) (d : State × Action) :
    ∀ᵐ H ∂markovHistoryLaw P σ s₀
      (generatedPhasePolicy P menu priority F B₀ s₀ fallback fallbackAction (empiricalReject P ε)) (Measure.dirac ()),
      ParitySuccess (priority σ) (historyAction d H) := by
  let π := generatedPhasePolicy P menu priority F B₀ s₀ fallback fallbackAction (empiricalReject P ε)
  have hπ := generatedPhasePolicy_measurable P menu priority F B₀ s₀ fallback fallbackAction (empiricalReject P ε)
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
    apply generated_stack_parity P menu priority F B₀ s₀ fallback fallbackAction ε hs₀ σ hσ z hSupported hTape
    · obtain ⟨K,hK⟩ := hTrue
      exact ⟨K,fun k hk n => hK k hk (pairPolicy s₀ π) n⟩
    · intro θ hθ e he hNe k
      exact hFalse (pairPolicy s₀ π) θ hθ e he hNe k
  exact ae_of_ae_map (historyAction_measurable d).aemeasurable hAction


end OrthemicCertificate.Direct
