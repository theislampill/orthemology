import LawfulProbability
import ConditionalAlmostSure

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Necessity
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- A genuine common lawful almost-sure hidden-parity policy. The seed law and
policy are shared before the true model is quantified; source coordinates are
computed from actual observations. Lawfulness has a proved finite-probability
interpretation and contains no winning-region or target premise. -/
structure WinningPolicy (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (d : State × Action)
    (B : Finset Model) (s₀ : State) where
  nonempty : B.Nonempty
  seedLaw : Measure R
  probability : IsProbabilityMeasure seedLaw
  policy : R → History Action State → Action
  measurable : Measurable (fun z : R × History Action State => policy z.1 z.2)
  lawful : Lawful P menu B s₀ policy seedLaw
  parity : ∀ σ ∈ B, ∀ᵐ H ∂markovHistoryLaw P σ s₀ policy seedLaw,
    ParitySuccess (priority σ) (historyAction d H)

def SemanticWinning (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (d : State × Action)
    (B : Finset Model) (s₀ : State) : Prop :=
  Nonempty (WinningPolicy (R := R) P menu priority d B s₀)

noncomputable def semanticRegion (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (d : State × Action)
    (B : Finset Model) : Finset State := by
  classical
  exact Finset.univ.filter (SemanticWinning (R := R) P menu priority d B)

@[simp] theorem mem_semanticRegion (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (d : State × Action)
    (B : Finset Model) (s : State) :
    s ∈ semanticRegion (R := R) P menu priority d B ↔ SemanticWinning (R := R) P menu priority d B s := by
  classical
  simp [semanticRegion]

/-- Positive finite histories have an actual common lawful winning restart for
all surviving models, with the derived common posterior seed law. -/
def restartWinningPolicy
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action}
    {priority : Model → (State × Action) → ℕ} {d : State × Action}
    {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀)
    (θ : Model) (hθ : θ ∈ B) (h : History (State × Action) State)
    (hp : 0 < markovHistoryLaw P θ s₀ w.policy w.seedLaw {H | H h.length = h}) :
    WinningPolicy (R := R) P menu priority d (liveHistory P B h) (currentState s₀ h) := by
  letI := w.probability
  have hInput := hp
  rw [markov_observed_prefix_mass P θ s₀ w.policy w.measurable w.seedLaw h] at hInput
  have hLive := positive_prefix_mem_live P B s₀ w.policy w.seedLaw θ hθ h hInput
  have hPosterior := markov_common_residual_seed P θ s₀ w.policy w.measurable w.seedLaw h hp
  refine ⟨⟨θ, hLive⟩, commonSeedPosterior (pairPolicy s₀ w.policy) w.seedLaw h, hPosterior.1,
    restartPolicy w.policy (erasePairSources h), restartPolicy_measurable w.policy w.measurable _,
    lawful_restart P menu B s₀ w.policy w.measurable w.seedLaw h w.lawful, ?_⟩
  intro σ hσ
  have hpσ := (hPosterior.2 σ (liveHistory_survives P B h σ hσ)).1
  exact markov_restart_ae_parity P σ s₀ w.policy w.measurable w.seedLaw h d (priority σ) hpσ
    (w.parity σ (liveHistory_subset P B h hσ))

/-- The semantic region contains every common positive-history residual state. -/
theorem semanticWinning_at_positive_history
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action}
    {priority : Model → (State × Action) → ℕ} {d : State × Action}
    {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀)
    (θ : Model) (hθ : θ ∈ B) (h : History (State × Action) State)
    (hp : 0 < markovHistoryLaw P θ s₀ w.policy w.seedLaw {H | H h.length = h}) :
    currentState s₀ h ∈ semanticRegion (R := R) P menu priority d (liveHistory P B h) :=
  (mem_semanticRegion P menu priority d _ _).mpr ⟨restartWinningPolicy w θ hθ h hp⟩

/-- The same genuine policy satisfies its parity predicate under the constructed
pair-sequence law required by the stage necessity theorem. -/
theorem winningPolicy_pair_parity
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action}
    {priority : Model → (State × Action) → ℕ} {d : State × Action}
    {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀) :
    ∀ σ ∈ B, ∀ᵐ x ∂markovPairLaw P σ s₀ w.policy w.seedLaw d, ParitySuccess (priority σ) x := by
  intro σ hσ
  exact (ae_map_iff (historyAction_measurable d).aemeasurable (paritySuccess_measurable (priority σ))).mpr
    (w.parity σ hσ)

end HiddenParity.Necessity
