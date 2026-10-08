import DirectController

noncomputable section
namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency
open HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [LinearOrder Action]
variable [DecidableEq Model] [LinearOrder Model]

theorem normalizeMemory_some (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action)
    (E : Finset (State × Action)) (he : m.retained = some E) :
    normalizeMemory P menu priority F fallback B s m = m := by simp [normalizeMemory,he]

theorem normalizeMemory_none_avoids (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action)
    (he : (normalizeMemory P menu priority F fallback B s m).retained = none) :
    s ∉ stageTargets P menu priority F B (phaseCandidate B fallback m) := by
  intro ht
  cases hm : m.retained <;> simp [normalizeMemory,hm,ht] at he

end OrthemicCertificate.Direct
