import RoundRobinRecurrence
import CheckedTargetOperation
import GlobalParityNecessity

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
open HiddenParity.Recurrence
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The checked component graph is the actual successor graph of each matching
live model, using the same normalized transition table. -/
theorem qualifying_matching_actual_component
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E) (hm : Match P.row θ σ E) :
    IsEndComponent Prod.fst (supportSuccessors (realRows P σ)) E := by
  have hNo := matching_noExit P B hm hQ.2.1
  apply endComponent_successor_congr Prod.fst (internalSuccessors P B) _ E hQ.2.2.1
  intro e he
  exact (positiveSuccessors_eq_internal P B σ hσ e (hNo e he)).symm

/-- Actual history-policy operational soundness: one explicit deterministic
policy satisfies the hidden parity objective in every matching live model. -/
theorem qualifying_roundRobin_wins_matching
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E) (hm : Match P.row θ σ E)
    (fallback : Action) (s₀ : State) (hs₀ : s₀ ∈ usedStates Prod.fst E)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action) :
    ∀ᵐ H ∂markovHistoryLaw P σ s₀ (roundRobinPolicy E fallback s₀) ρ,
      ParitySuccess (priority σ) (historyAction d H) := by
  have hEC := qualifying_matching_actual_component P B priority θ σ hσ allowed E hQ hm
  filter_upwards [roundRobin_markov_recurrent P σ E fallback s₀ hs₀ ρ hEC d] with H hH
  simpa only [ParitySuccess,hH] using hQ.2.2.2 σ hσ hm

/-- Every feasible compatible history of a support-preserving component policy
retains the original live support and a retained current observed state. -/
theorem compatible_roundRobin_live
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (hs₀ : s₀ ∈ usedStates Prod.fst E)
    (hNo : ∀ σ ∈ B, ∀ e ∈ E, NoExit P B σ e)
    (hClosed : ∀ σ ∈ B, ∀ e ∈ E, ∀ y, 0 < P.row σ e y → y ∈ usedStates Prod.fst E)
    (r : R) (h : History (State × Action) State)
    (hLive : (liveHistory P B h).Nonempty)
    (hComp : ActionCompatible (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) r h) :
    liveHistory P B h = B ∧ currentState s₀ h ∈ usedStates Prod.fst E := by
  induction h with
  | nil => exact ⟨liveHistory_nil P B,hs₀⟩
  | cons ey h ih =>
      obtain ⟨σ,hσ⟩ := hLive
      have hσh : σ ∈ liveHistory P B h := by
        have hm := (mem_liveHistory P B (ey::h) σ).mp hσ
        exact (mem_liveHistory P B h σ).mpr ⟨hm.1,fun e he => hm.2 e (List.mem_cons_of_mem _ he)⟩
      have hPos : 0 < P.row σ ey.1 ey.2 := ((mem_liveHistory P B (ey::h) σ).mp hσ).2 ey (by simp)
      have hB := liveHistory_subset P B h hσh
      have hTail := ih ⟨σ,hσh⟩ hComp.1
      have heE : ey.1 ∈ E := by
        rw [← hComp.2]
        exact roundRobin_pair_mem E fallback s₀ r h hTail.2
      refine ⟨?_,hClosed σ hB ey.1 heE ey.2 hPos⟩
      rw [liveHistory_cons,hTail.1]
      exact (liveUpdate_eq_iff_internal P B ey.1 ey.2).mpr (hNo σ hB ey.1 heE ey.2 hPos)

/-- Direct lawful-policy proof, valid on all feasible finite histories; it does
not replace lawfulness with a probability-one path certificate. -/
theorem roundRobin_lawful
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model)
    (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (hs₀ : s₀ ∈ usedStates Prod.fst E)
    (hMenu : ∀ e ∈ E, e.2 ∈ menu B e.1)
    (hNo : ∀ σ ∈ B, ∀ e ∈ E, NoExit P B σ e)
    (hClosed : ∀ σ ∈ B, ∀ e ∈ E, ∀ y, 0 < P.row σ e y → y ∈ usedStates Prod.fst E)
    (ρ : Measure R) : Lawful P menu B s₀ (roundRobinPolicy E fallback s₀) ρ := by
  intro h hLive
  apply ae_of_all
  intro r hComp
  have hh := compatible_roundRobin_live P B E fallback s₀ hs₀ hNo hClosed r h hLive hComp
  have he := roundRobin_pair_mem E fallback s₀ r h hh.2
  simpa only [hh.1,pairPolicy_source] using hMenu _ he

/-- Genuine common lawful winning policy on a target whose full rows match every
live model. In particular this closes actual-policy sufficiency on singleton targets. -/
def matchingTargetWinningPolicy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (hB : B.Nonempty)
    (priority : Model → (State × Action) → ℕ) (θ : Model)
    (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E)
    (hMatch : ∀ σ ∈ B, Match P.row θ σ E)
    (hMenu : ∀ e ∈ E, e.2 ∈ menu B e.1)
    (fallback : Action) (s₀ : State) (hs₀ : s₀ ∈ usedStates Prod.fst E) (d : State × Action) :
    WinningPolicy (R := Unit) P menu priority d B s₀ := by
  refine ⟨hB, Measure.dirac (), inferInstance, roundRobinPolicy E fallback s₀,
    roundRobinPolicy_measurable E fallback s₀, ?_, ?_⟩
  · apply roundRobin_lawful P menu B E fallback s₀ hs₀ hMenu
    · intro σ hσ
      exact matching_noExit P B (hMatch σ hσ) hQ.2.1
    · intro σ hσ e he y hy
      apply matching_component_closed P Prod.fst B priority θ σ allowed E hQ (hMatch σ hσ) e he y
      change (0 : ℝ) < (P.row σ e y : ℝ)
      exact_mod_cast hy
  · intro σ hσ
    exact qualifying_roundRobin_wins_matching P B priority θ σ hσ allowed E hQ (hMatch σ hσ)
      fallback s₀ hs₀ (Measure.dirac ()) d

/-- Every computed target state has one concrete observed-history policy whose
actual law wins in all full-row-matching live models. -/
theorem computed_target_actual_policy
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model)
    (allowed : Finset (State × Action)) (s₀ : State)
    (hs : s₀ ∈ markovTargetStates P Prod.fst B priority θ allowed)
    (fallback : Action) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action) :
    ∃ E : Finset (State × Action), MarkovQualifying P Prod.fst B priority θ allowed E ∧
      ∀ σ ∈ B, Match P.row θ σ E →
        ∀ᵐ H ∂markovHistoryLaw P σ s₀ (roundRobinPolicy E fallback s₀) ρ,
          ParitySuccess (priority σ) (historyAction d H) := by
  obtain ⟨E,hQ,hsE⟩ := (markovTargetStates_exact P Prod.fst B priority θ allowed s₀).mp hs
  refine ⟨E,hQ,?_⟩
  intro σ hσ hm
  exact qualifying_roundRobin_wins_matching P B priority θ σ hσ allowed E hQ hm fallback s₀ hsE ρ d

/-- Singleton-support target states have actual common lawful winning policies.
This is local target sufficiency; navigation from other computed states is separate. -/
theorem computed_singleton_target_semanticWinning
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (θ : Model)
    (allowed : Finset (State × Action)) (s₀ : State)
    (hs : s₀ ∈ markovTargetStates P Prod.fst {θ} priority θ allowed)
    (hMenu : ∀ e ∈ allowed, e.2 ∈ menu {θ} e.1) (fallback : Action) (d : State × Action) :
    SemanticWinning (R := Unit) P menu priority d {θ} s₀ := by
  obtain ⟨E,hQ,hsE⟩ := (markovTargetStates_exact P Prod.fst {θ} priority θ allowed s₀).mp hs
  apply Nonempty.intro
  exact matchingTargetWinningPolicy P menu {θ} (by simp) priority θ allowed E hQ
    (by intro σ hσ; have he : σ = θ := Finset.mem_singleton.mp hσ; subst σ; intro e _; rfl)
    (fun e he => hMenu e (hQ.1 he)) fallback s₀ hsE d

end HiddenParity.Sufficiency
