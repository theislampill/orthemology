import ActualTargetPolicy

noncomputable section
namespace HiddenParity.Sufficiency
open HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action]
variable [DecidableEq Model]

/-- A finite directed path ending at a used state begins at a used state. -/
theorem reach_start_used (D : Finset (State × Action)) (succ : (State × Action) → Finset State)
    {s t : State} (hp : Reach Prod.fst succ D s t) (ht : t ∈ usedStates Prod.fst D) :
    s ∈ usedStates Prod.fst D := by
  induction hp using Relation.ReflTransGen.head_induction_on with
  | refl => exact ht
  | @head s y he _ _ =>
      obtain ⟨e,he,hes,_⟩ := he
      exact Finset.mem_image.mpr ⟨e,he,hes⟩

/-- The concrete greatest stage fixed point supplies an available safe action
at every retained observed state. No nonblocking hypothesis is added. -/
theorem winningRegion_safe_action_available
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) (hB : B.Nonempty)
    (s : State) (hs : s ∈ winningRegion P menu priority B) :
    s ∈ usedStates Prod.fst
      (regionAllowed P menu B (winningRegion P menu priority) (winningRegion P menu priority B)) := by
  let W := winningRegion P menu priority B
  let D := regionAllowed P menu B (winningRegion P menu priority) W
  obtain ⟨θ,hθ⟩ := hB
  have hFix := winningRegion_fixed P menu priority B ⟨θ,hθ⟩
  have hStep : s ∈ regionStep P menu priority B (winningRegion P menu priority) W := hFix.symm ▸ hs
  rcases ((mem_regionStep P menu priority B _ W s).mp hStep).2 θ hθ with
    ⟨e,he,hPath,_⟩ | ⟨t,ht,hPath⟩
  · exact reach_start_used D _ hPath (Finset.mem_image.mpr ⟨e,he,rfl⟩)
  · obtain ⟨E,hQ,htE⟩ := (markovTargetStates_exact P Prod.fst B priority θ D t).mp ht
    exact reach_start_used D _ hPath (Finset.image_mono Prod.fst hQ.1 htE)

def stageActions (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) : Finset (State × Action) :=
  regionAllowed P menu B (winningRegion P menu priority) (winningRegion P menu priority B)

def stageTargets (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) (θ : Model) : Finset State :=
  markovTargetStates P Prod.fst B priority θ (stageActions P menu priority B)

/-- A fixed finite choice of an actual qualifying target containing the current
state. Off-target values are empty and are never installed in lawful operation. -/
def chooseTarget (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) (θ : Model) (s : State) :
    Finset (State × Action) :=
  if h : s ∈ stageTargets P menu priority B θ then
    Classical.choose ((markovTargetStates_exact P Prod.fst B priority θ (stageActions P menu priority B) s).mp h)
  else ∅

theorem chooseTarget_spec (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) (θ : Model) (s : State)
    (hs : s ∈ stageTargets P menu priority B θ) :
    MarkovQualifying P Prod.fst B priority θ (stageActions P menu priority B)
      (chooseTarget P menu priority B θ s) ∧
      s ∈ usedStates Prod.fst (chooseTarget P menu priority B θ s) := by
  simp only [chooseTarget,dif_pos hs]
  exact Classical.choose_spec ((markovTargetStates_exact P Prod.fst B priority θ
    (stageActions P menu priority B) s).mp hs)

theorem stageActions_successor (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model)
    (e : State × Action) (he : e ∈ stageActions P menu priority B) (y : State)
    (hLive : (liveUpdate P B e y).Nonempty) :
    y ∈ winningRegion P menu priority (liveUpdate P B e y) := by
  have hh := (mem_regionAllowed P menu B _ _ e).mp he
  have h := hh.2.2 y hLive
  split_ifs at h with hEq
  · simpa only [hEq] using h
  · exact h

end HiddenParity.Sufficiency
