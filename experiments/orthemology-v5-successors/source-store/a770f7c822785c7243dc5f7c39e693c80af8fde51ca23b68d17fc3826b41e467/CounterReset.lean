import NativeControllerControls
import StageFamily
import MemoryTransitions

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding

namespace OrthemicCertificate.DirectCounterReset
open OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [LinearOrder Action] [Inhabited State]
variable [DecidableEq Model] [LinearOrder Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

def phaseCandidate (B : Finset Model) (fallback : Model) (m : PhaseMemory State Action) : Model :=
  OrthemicCertificate.Direct.cycleAction B fallback m.index

def normalizeMemory (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action) : PhaseMemory State Action :=
  match m.retained with
  | some _ => m
  | none => if s ∈ OrthemicCertificate.Direct.stageTargets P menu priority F B (phaseCandidate B fallback m) then
      ⟨m.index,some (OrthemicCertificate.Direct.chooseTarget P menu priority F B (phaseCandidate B fallback m) s)⟩ else m

def activePairs (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action)
    (B : Finset Model) (m : PhaseMemory State Action) : Finset (State × Action) :=
  m.retained.getD (OrthemicCertificate.Direct.stageActions P menu priority F B)

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
  OrthemicCertificate.Direct.cycleAction (retainedActions (activePairs P menu priority F B m) s) fallbackAction 0


def checkedAction {q n k : ℕ} (I : Input q n k) (B : Support q) (s : Fin n)
    (c : Body q n k) (h : List (Fin k × Fin n)) : Option (Fin k) :=
  if hc : check I c B s = true then
    let hI := ((check_iff I c B s).mp hc).1.1
    letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
    some (generatedPhasePolicy (I.kernel hI) I.menu I.priority (submittedFamily c) B s
      ⟨0,hI.1.1⟩ ⟨0,hI.1.2.2.1⟩ (rationalReject I (tolerance I B)) () h)
  else none
end OrthemicCertificate.DirectCounterReset
open OrthemicCertificate.Fixtures
#guard OrthemicCertificate.DirectCounterReset.checkedAction choices {0} 1 [fairNode] [(0,1)] = some 1
