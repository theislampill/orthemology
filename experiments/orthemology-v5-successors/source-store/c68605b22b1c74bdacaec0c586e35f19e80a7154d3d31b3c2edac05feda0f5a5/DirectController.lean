import StageFamily
import MemoryTransitions

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding

namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [LinearOrder Action] [Inhabited State]
variable [DecidableEq Model] [LinearOrder Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

def phaseCandidate (B : Finset Model) (fallback : Model) (m : PhaseMemory State Action) : Model :=
  cycleAction B fallback m.index

def normalizeMemory (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action) : PhaseMemory State Action :=
  match m.retained with
  | some _ => m
  | none => if s ∈ stageTargets P menu priority F B (phaseCandidate B fallback m) then
      ⟨m.index,some (chooseTarget P menu priority F B (phaseCandidate B fallback m) s)⟩ else m

def activePairs (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (B : Finset Model) (m : PhaseMemory State Action) : Finset (State × Action) :=
  m.retained.getD (stageActions P menu priority F B)

/-- Rejection uses an explicit observed-history test. Its later empirical
instantiation is separate; safety below is valid for every such test. -/
def phaseMemory (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model)
    (reject : Model → ℕ → History (State × Action) State → Bool) :
    History Action State → PhaseMemory State Action
  | [] => ⟨0,none⟩
  | (a,y)::h =>
      let B := liveHistory P B₀ (augmentHistory s₀ h)
      let C := liveHistory P B₀ (augmentHistory s₀ ((a,y)::h))
      let m := normalizeMemory P menu priority F fallback B (observedState s₀ h)
        (phaseMemory P menu priority F B₀ s₀ fallback reject h)
      advanceMemory B C y m
        (reject (phaseCandidate B fallback m) m.index (augmentHistory s₀ ((a,y)::h)))

def currentMemory (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model)
    (reject : Model → ℕ → History (State × Action) State → Bool) (h : History Action State) :
    PhaseMemory State Action :=
  normalizeMemory P menu priority F fallback (liveHistory P B₀ (augmentHistory s₀ h))
    (observedState s₀ h) (phaseMemory P menu priority F B₀ s₀ fallback reject h)

/-- The actual generated policy uses only observed action/state history. It
cycles the safe stage menu during navigation, then the selected target menu. -/
def generatedPhasePolicy (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool)
    (_ : Unit) (h : History Action State) : Action :=
  let B := liveHistory P B₀ (augmentHistory s₀ h)
  let m := currentMemory P menu priority F B₀ s₀ fallback reject h
  let s := observedState s₀ h
  cycleAction (retainedActions (activePairs P menu priority F B m) s) fallbackAction (historyVisits s₀ s h)

theorem generatedPhasePolicy_measurable
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [CertifiedStageFamily P menu priority F]
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool) :
    Measurable (fun z : Unit × History Action State =>
      generatedPhasePolicy P menu priority F B₀ s₀ fallback fallbackAction reject z.1 z.2) := by
  exact measurable_of_countable _

/-- Invariant of a stored component at the current support/state. -/
def MemoryValid (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action) : Prop :=
  ∀ E, m.retained = some E →
    MarkovQualifying P Prod.fst B priority (phaseCandidate B fallback m) (stageActions P menu priority F B) E ∧
      s ∈ usedStates Prod.fst E

@[simp] theorem normalizeMemory_index (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [CertifiedStageFamily P menu priority F]
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action) :
    (normalizeMemory P menu priority F fallback B s m).index = m.index := by
  unfold normalizeMemory
  split
  · rfl
  · split_ifs <;> rfl

theorem normalizeMemory_valid (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [CertifiedStageFamily P menu priority F]
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action)
    (hm : MemoryValid P menu priority F fallback B s m) :
    MemoryValid P menu priority F fallback B s (normalizeMemory P menu priority F fallback B s m) := by
  unfold normalizeMemory
  split
  · exact hm
  · split_ifs with ht
    · intro E he
      have hE : chooseTarget P menu priority F B (phaseCandidate B fallback m) s = E := Option.some.inj he
      subst E
      exact chooseTarget_spec P menu priority F B (phaseCandidate B fallback m) s ht
    · exact hm

theorem valid_activePairs (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [CertifiedStageFamily P menu priority F]
    (fallback : Model) (B : Finset Model) (hB : B.Nonempty) (s : State)
    (hs : s ∈ F.states B) (m : PhaseMemory State Action)
    (hm : MemoryValid P menu priority F fallback B s m) :
    activePairs P menu priority F B m ⊆ stageActions P menu priority F B ∧
      s ∈ usedStates Prod.fst (activePairs P menu priority F B m) := by
  cases he : m.retained with
  | none =>
      simp only [activePairs,he,Option.getD_none]
      exact ⟨Finset.Subset.refl _,family_action_available P menu priority F B hB s hs⟩
  | some E =>
      simp only [activePairs,he,Option.getD_some]
      exact ⟨(hm E he).1.1,(hm E he).2⟩

/-- Every transition preserves the stored-component invariant. Rejected or
support-changing transitions clear the component rather than reuse a stale one. -/
theorem advanceMemory_valid (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [CertifiedStageFamily P menu priority F]
    (fallback : Model) (B C : Finset Model) (s y : State) (m : PhaseMemory State Action)
    (reject : Bool) (hm : MemoryValid P menu priority F fallback B s m) :
    MemoryValid P menu priority F fallback C y (advanceMemory B C y m reject) := by
  unfold advanceMemory
  split_ifs with hChange hReject
  · intro E he; cases he
  · intro E he; cases he
  · have hEq : C = B := by simpa only [not_not] using hChange
    subst C
    cases he : m.retained with
    | none => simp only [he]; intro E h; simp only [he] at h; cases h
    | some E =>
        simp only [he]
        split_ifs with hy
        · intro F hF
          have hFE : E = F := Option.some.inj (he.symm.trans hF)
          subst F
          exact ⟨(hm E he).1,hy⟩
        · intro F hF; cases hF

end OrthemicCertificate.Direct
