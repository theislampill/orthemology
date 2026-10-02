import ConditionalRotorHistory

noncomputable section
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.FrozenRotor
attribute [local instance] Classical.propDecidable
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
universe u
variable {State Action : Type u}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Literal global source-departure residues reconstructed from the entire
observed history, including every pre-entry departure. -/
def residuesOfHistory (F : Finset (State × Action)) (s₀ : State)
    (h : History (State × Action) State) : Residues F := fun s =>
  ⟨historyVisits s₀ s (erasePairSources h) % max 1 (retainedActions F s).card,
    Nat.mod_lt _ (lt_of_lt_of_le (by decide : 0<1) (Nat.le_max_left _ _))⟩

def snapshot (F : Finset (State × Action)) (s₀ : State)
    (h : History (State × Action) State) : Aug F :=
  some (currentState s₀ h,residuesOfHistory F s₀ h)

@[simp] theorem snapshot_ne_none (F : Finset (State × Action)) (s₀ : State)
    (h : History (State × Action) State) : snapshot F s₀ h ≠ none := by simp [snapshot]

/-- The finite snapshot update is exactly the source's global counter update;
it does not restart counters at phase or support changes. -/
theorem residuesOfHistory_cons (F : Finset (State × Action)) (s₀ : State)
    (h : History (State × Action) State) (e : State × Action) (y : State) :
    residuesOfHistory F s₀ ((e,y)::h) = bump F (residuesOfHistory F s₀ h) (currentState s₀ h) := by
  funext s
  apply Fin.ext
  simp only [residuesOfHistory,erasePairSources,List.map_cons,historyVisits,bump]
  rw [show List.map (fun z : (State × Action) × State => (z.1.2,z.2)) h = erasePairSources h from rfl,
    observedState_erase,Nat.mod_add_mod]

theorem snapshot_cons (F : Finset (State × Action)) (s₀ : State)
    (h : History (State × Action) State) (e : State × Action) (y : State) :
    snapshot F s₀ ((e,y)::h) = some (y,bump F (residuesOfHistory F s₀ h) (currentState s₀ h)) := by
  simp only [snapshot,currentState,residuesOfHistory_cons]

/-- Max(1,card) residues agree even for unused empty menus, whose source cycle
is constantly the fallback. -/
theorem cycleAction_max_mod (F : Finset Action) (fallback : Action) (n : ℕ) :
    cycleAction F fallback (n % max 1 F.card)=cycleAction F fallback n := by
  classical
  by_cases hzero : F.card=0
  · have he : F=∅ := Finset.card_eq_zero.mp hzero
    simp [he,cycleAction]
  · rw [max_eq_right (show 1 ≤ F.card by omega)]
    exact HiddenParity.Cost.cycleAction_mod F fallback n

/-- The snapshot's finite rotor action equals the exact source action formula
with its unbounded global departure count. -/
theorem pairChoice_snapshot (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (h : History (State × Action) State) :
    pairChoice F fallback s₀ (snapshot F s₀ h) =
      (currentState s₀ h,cycleAction (retainedActions F (currentState s₀ h)) fallback
        (historyVisits s₀ (currentState s₀ h) (erasePairSources h))) := by
  simp only [pairChoice,snapshot,source,action,chosen,residuesOfHistory]
  rw [cycleAction_max_mod]

/-- One un-killed step of the explicit finite kernel preserves the literal
full-history snapshot whenever its pair agrees with the source rotor. -/
theorem next_snapshot_of_clear (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (h : History (State × Action) State) (e : State × Action) (y : State)
    (he : e=pairChoice F fallback s₀ (snapshot F s₀ h))
    (hs : currentState s₀ h ∈ usedStates Prod.fst F) (hb : ¬ before e) (ha : ¬ after e y) :
    next F fallback before after (snapshot F s₀ h) y = snapshot F s₀ ((e,y)::h) := by
  have he' : e=(currentState s₀ h,chosen F fallback (currentState s₀ h) (residuesOfHistory F s₀ h)) := he
  rw [snapshot_cons]
  simp only [snapshot,next]
  rw [← he']
  simp only [hs,hb,ha,not_true_eq_false,false_or,if_false]

end HiddenParity.Cost.FrozenRotor
