import ObservedPhaseController

noncomputable section
namespace HiddenParity.Sufficiency
open HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action]
variable [DecidableEq Model]

theorem advanceMemory_index_cases (B : Finset Model) (y : State) (m : PhaseMemory State Action)
    (reject : Bool) :
    (advanceMemory B B y m reject).index = m.index ∨
      (advanceMemory B B y m reject).index = m.index+1 := by
  unfold advanceMemory
  simp only [ne_eq,not_true_eq_false,if_false]
  split_ifs
  · exact Or.inr rfl
  · cases he : m.retained with
    | none => simp [he]
    | some E => simp only [he]; split_ifs <;> simp

theorem advanceMemory_no_reject (B : Finset Model) (y : State) (m : PhaseMemory State Action)
    (hStay : ∀ E, m.retained = some E → y ∈ usedStates Prod.fst E) :
    advanceMemory B B y m false = m := by
  unfold advanceMemory
  simp only [ne_eq,not_true_eq_false,if_false,Bool.false_eq_true]
  cases he : m.retained with
  | none => simp only [he]
  | some E => simp only [he,if_pos (hStay E he)]

theorem advanceMemory_reject_index (B : Finset Model) (y : State) (m : PhaseMemory State Action) :
    (advanceMemory B B y m true).index = m.index+1 := by
  simp [advanceMemory]

theorem advanceMemory_equal_index_retained (B : Finset Model) (y : State)
    (m : PhaseMemory State Action) (reject : Bool)
    (hIndex : (advanceMemory B B y m reject).index = m.index) :
    advanceMemory B B y m reject = m := by
  unfold advanceMemory at hIndex ⊢
  simp only [ne_eq,not_true_eq_false,if_false] at hIndex ⊢
  split_ifs at hIndex ⊢ with hr
  · simp only at hIndex; omega
  · cases he : m.retained with
    | none => simp only [he]
    | some E =>
        simp only [he] at hIndex ⊢
        split_ifs at hIndex ⊢ with hy
        · rfl
        · simp only at hIndex; omega

theorem normalizeMemory_some (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action)
    (E : Finset (State × Action)) (he : m.retained = some E) :
    normalizeMemory P menu priority fallback B s m = m := by simp [normalizeMemory,he]

theorem normalizeMemory_none_avoids (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (fallback : Model) (B : Finset Model) (s : State) (m : PhaseMemory State Action)
    (he : (normalizeMemory P menu priority fallback B s m).retained = none) :
    s ∉ stageTargets P menu priority B (phaseCandidate B fallback m) := by
  intro ht
  cases hm : m.retained <;> simp [normalizeMemory,hm,ht] at he

end HiddenParity.Sufficiency
