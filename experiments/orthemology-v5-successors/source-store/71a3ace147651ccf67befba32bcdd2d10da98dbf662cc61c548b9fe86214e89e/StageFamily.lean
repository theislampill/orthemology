import CertificateSoundness
import OrderedCycle

/-! A witness-parametric stage interface. Its proof fields are local graph and
safety facts, never policy success, almost-sure fairness, or solver membership. -/
namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Stage HiddenParity.Necessity
universe u w

structure StageData (Model : Type w) (State Action : Type u) where
  states : Finset Model → Finset State
  pairs : Finset Model → Finset (State × Action)
  targets : Finset Model → Model → Finset State
  choose : Finset Model → Model → State → Finset (State × Action)

variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action]
variable [DecidableEq Model]

class CertifiedStageFamily (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (F : StageData Model State Action) : Prop where
  available : ∀ B, B.Nonempty → ∀ s ∈ F.states B, s ∈ usedStates Prod.fst (F.pairs B)
  menu : ∀ B e, e ∈ F.pairs B → e.2 ∈ menu B e.1
  successor : ∀ B e, e ∈ F.pairs B → ∀ y, (liveUpdate P B e y).Nonempty →
    y ∈ F.states (liveUpdate P B e y)
  target : ∀ B θ s, s ∈ F.targets B θ →
    MarkovQualifying P Prod.fst B priority θ (F.pairs B) (F.choose B θ s) ∧
      s ∈ usedStates Prod.fst (F.choose B θ s)
  reach : ∀ B θ, θ ∈ B → ∀ s ∈ F.states B,
    ReachableExit P B θ (F.pairs B) s ∨
      ∃ t ∈ F.targets B θ, Reach Prod.fst (internalSuccessors P B) (F.pairs B) s t

/-- Thin executable projections retain uniform policy signatures. -/
def stageActions (_P : RationalKernel Model (State × Action) State)
    (_menu : Finset Model → State → Finset Action) (_priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) (B : Finset Model) : Finset (State × Action) := F.pairs B

def stageTargets (_P : RationalKernel Model (State × Action) State)
    (_menu : Finset Model → State → Finset Action) (_priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) (B : Finset Model) (θ : Model) : Finset State := F.targets B θ

def chooseTarget (_P : RationalKernel Model (State × Action) State)
    (_menu : Finset Model → State → Finset Action) (_priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) (B : Finset Model) (θ : Model) (s : State) : Finset (State × Action) := F.choose B θ s

theorem chooseTarget_spec (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (B : Finset Model) (θ : Model) (s : State) (hs : s ∈ stageTargets P menu priority F B θ) :
    MarkovQualifying P Prod.fst B priority θ (stageActions P menu priority F B)
      (chooseTarget P menu priority F B θ s) ∧
      s ∈ usedStates Prod.fst (chooseTarget P menu priority F B θ s) := hF.target B θ s hs

theorem family_action_available (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (B : Finset Model) (hB : B.Nonempty) (s : State) (hs : s ∈ F.states B) :
    s ∈ usedStates Prod.fst (stageActions P menu priority F B) := hF.available B hB s hs

theorem stageActions_successor (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (F : StageData Model State Action) [hF : CertifiedStageFamily P menu priority F]
    (B : Finset Model) (e : State × Action) (he : e ∈ stageActions P menu priority F B) (y : State)
    (hLive : (liveUpdate P B e y).Nonempty) : y ∈ F.states (liveUpdate P B e y) :=
  hF.successor B e he y hLive

end OrthemicCertificate.Direct
