import StageTargetOrExit
import ConditionalKilledContinuation

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Necessity
open HiddenParity.Stochastic HiddenParity.Stage HiddenParity.ResidualSeed
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Exact finite-history live support, retaining precisely models positive on
every recorded full state/action row. Histories are stored newest-first. -/
def liveHistory (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (h : History (State × Action) State) : Finset Model := by
  classical
  exact B.filter (fun σ => ∀ ey ∈ h, 0 < P.row σ ey.1 ey.2)

@[simp] theorem mem_liveHistory (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (h : History (State × Action) State) (σ : Model) :
    σ ∈ liveHistory P B h ↔ σ ∈ B ∧ ∀ ey ∈ h, 0 < P.row σ ey.1 ey.2 := by
  classical
  simp [liveHistory]

@[simp] theorem liveHistory_nil (P : RationalKernel Model (State × Action) State) (B : Finset Model) :
    liveHistory P B [] = B := by
  ext σ
  simp

theorem liveHistory_subset (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (h : History (State × Action) State) : liveHistory P B h ⊆ B :=
  fun σ hσ => ((mem_liveHistory P B h σ).mp hσ).1

theorem liveHistory_cons (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (h : History (State × Action) State) (e : State × Action) (y : State) :
    liveHistory P B ((e,y)::h) = liveUpdate P (liveHistory P B h) e y := by
  ext σ
  simp only [mem_liveHistory, List.forall_mem_cons, mem_liveUpdate]
  tauto

theorem liveHistory_append (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (tail h : History (State × Action) State) :
    liveHistory P B (tail ++ h) = liveHistory P (liveHistory P B h) tail := by
  ext σ
  simp only [mem_liveHistory, List.forall_mem_append]
  tauto

theorem liveHistory_survives (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (h : History (State × Action) State) (σ : Model)
    (hσ : σ ∈ liveHistory P B h) : SurvivesHistory P σ h := by
  intro i
  exact ((mem_liveHistory P B h σ).mp hσ).2 _ (List.getElem_mem i.isLt)

theorem currentState_append (s₀ : State) (tail h : History (State × Action) State) :
    currentState s₀ (tail ++ h) = currentState (currentState s₀ h) tail := by
  cases tail <;> rfl

/-- Genuine finite-history lawfulness: null private-seed branches are ignored,
while every compatible positive-likelihood observed history uses its hard menu. -/
def Lawful (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (s₀ : State)
    (π : R → History Action State → Action) (ρ : Measure R) : Prop :=
  ∀ h : History (State × Action) State, (liveHistory P B h).Nonempty →
    ∀ᵐ r ∂ρ, ActionCompatible (pairPolicy s₀ π) r h →
      (pairPolicy s₀ π r h).2 ∈ menu (liveHistory P B h) (currentState s₀ h)

theorem commonPosterior_ae_of_original
    (s₀ : State) (π : R → History Action State → Action) (ρ : Measure R)
    (h : History (State × Action) State) (Q : R → Prop) (hq : ∀ᵐ r ∂ρ, Q r) :
    ∀ᵐ r ∂commonSeedPosterior (pairPolicy s₀ π) ρ h, Q r :=
  Measure.ae_smul_measure (ae_restrict_of_ae hq) _

theorem commonPosterior_compatible
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) (h : History (State × Action) State) :
    ∀ᵐ r ∂commonSeedPosterior (pairPolicy s₀ π) ρ h, ActionCompatible (pairPolicy s₀ π) r h :=
  Measure.ae_smul_measure (ae_restrict_mem
    (compatibleSeeds_measurable (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ) h)) _

/-- Lawfulness is preserved by the actual common posterior/restart construction.
This is proved by compatibility and support concatenation plus measure restriction. -/
theorem lawful_restart
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (B : Finset Model) (s₀ : State)
    (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) (h : History (State × Action) State) (hL : Lawful P menu B s₀ π ρ) :
    Lawful P menu (liveHistory P B h) (currentState s₀ h)
      (restartPolicy π (erasePairSources h)) (commonSeedPosterior (pairPolicy s₀ π) ρ h) := by
  intro tail hNonempty
  have hGlobal : (liveHistory P B (tail ++ h)).Nonempty := by
    rwa [liveHistory_append]
  have hMenu := commonPosterior_ae_of_original s₀ π ρ h _ (hL (tail ++ h) hGlobal)
  filter_upwards [hMenu, commonPosterior_compatible s₀ π hπ ρ h] with r hMenu hOld
  intro hNew
  have hRestart : ActionCompatible (restartPolicy (pairPolicy s₀ π) h) r tail := by
    have he : restartPolicy (pairPolicy s₀ π) h =
        pairPolicy (currentState s₀ h) (restartPolicy π (erasePairSources h)) := by
      funext r t
      exact (restart_pairPolicy_agrees s₀ π h t r).symm
    rwa [he]
  have hCompat := (compatible_append (pairPolicy s₀ π) r h tail).mpr ⟨hOld, hRestart⟩
  have hChoice := hMenu hCompat
  have hAct : pairPolicy (currentState s₀ h) (restartPolicy π (erasePairSources h)) r tail =
      pairPolicy s₀ π r (tail ++ h) := restart_pairPolicy_agrees s₀ π h tail r
  rw [hAct]
  simpa only [liveHistory_append, currentState_append] using hChoice

end HiddenParity.Necessity
