import RoundRobinSchedule
import HistoryStageSafety

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity
universe u v
variable {State Action : Type u} {R : Type v}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Current state read exclusively from actual observed receipts. -/
def observedState (s₀ : State) : History Action State → State
  | [] => s₀
  | (_,y) :: _ => y

/-- Prior departure count reconstructed from the complete observed history. -/
def historyVisits (s₀ s : State) : History Action State → ℕ
  | [] => 0
  | (_,_) :: h => historyVisits s₀ s h + if observedState s₀ h = s then 1 else 0

def retainedActions (E : Finset (State × Action)) (s : State) : Finset Action :=
  Finset.univ.filter (fun a => (s,a) ∈ E)

@[simp] theorem mem_retainedActions (E : Finset (State × Action)) (s : State) (a : Action) :
    a ∈ retainedActions E s ↔ (s,a) ∈ E := by simp [retainedActions]

theorem retainedActions_nonempty (E : Finset (State × Action)) (s : State)
    (hs : s ∈ usedStates Prod.fst E) : (retainedActions E s).Nonempty := by
  obtain ⟨e,he,hs⟩ := Finset.mem_image.mp hs
  exact ⟨e.2, (mem_retainedActions E s e.2).mpr (by simpa [← hs] using he)⟩

/-- One total, seed-independent causal policy, sharing no hidden-model input. -/
def roundRobinPolicy (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (_ : R) (h : History Action State) : Action :=
  cycleAction (retainedActions E (observedState s₀ h)) fallback
    (historyVisits s₀ (observedState s₀ h) h)

theorem roundRobinPolicy_measurable (E : Finset (State × Action)) (fallback : Action) (s₀ : State) :
    Measurable (fun z : R × History Action State => roundRobinPolicy E fallback s₀ z.1 z.2) := by
  exact (measurable_of_countable (fun h : History Action State => roundRobinPolicy E fallback s₀ () h)).comp measurable_snd

@[simp] theorem observedState_erase (s₀ : State) (h : History (State × Action) State) :
    observedState s₀ (erasePairSources h) = currentState s₀ h := by cases h <;> rfl

theorem roundRobin_pair_mem (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (r : R) (h : History (State × Action) State) (hs : currentState s₀ h ∈ usedStates Prod.fst E) :
    pairPolicy s₀ (roundRobinPolicy E fallback s₀) r h ∈ E := by
  have hm := cycleAction_mem (retainedActions E (currentState s₀ h)) fallback
    (retainedActions_nonempty E _ hs) (historyVisits s₀ (currentState s₀ h) (erasePairSources h))
  simpa only [mem_retainedActions, pairPolicy, roundRobinPolicy, observedState_erase] using hm

/-- The reconstructed departure counter equals the pathwise visit counter on
actual runs, including the initial state's first departure. -/
theorem stack_historyVisits (s₀ s : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State) (n : ℕ) :
    historyVisits s₀ s (erasePairSources (stackHistoryTrajectory (pairPolicy s₀ π) z n)) =
      visitsBefore (fun k => (stackActionTrajectory (pairPolicy s₀ π) z k).1) s n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [stack_history_succ]
      simp only [erasePairSources, List.map_cons, historyVisits]
      rw [show List.map (fun z : (State × Action) × State => (z.1.2,z.2))
          (stackHistoryTrajectory (pairPolicy s₀ π) z n) =
          erasePairSources (stackHistoryTrajectory (pairPolicy s₀ π) z n) from rfl]
      rw [observedState_erase, ih]
      rfl

theorem stack_roundRobin_action (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (z : R × FlatStack (State × Action) State) (n : ℕ) :
    let x := stackActionTrajectory (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) z
    (x n).2 = cycleAction (retainedActions E (x n).1) fallback
      (visitsBefore (fun k => (x k).1) (x n).1 n) := by
  dsimp only
  rw [← stack_historyVisits]
  simp only [stackActionTrajectory, pairPolicy, roundRobinPolicy, observedState_erase]

/-- Every retained action at a recurrent source state is actually recurrent. -/
theorem stack_roundRobin_fair (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (z : R × FlatStack (State × Action) State) (e : State × Action) (he : e ∈ E)
    (hs : e.1 ∈ usedStates Prod.fst
      (recurrentSet (stackActionTrajectory (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) z))) :
    e ∈ recurrentSet (stackActionTrajectory (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) z) := by
  let x := stackActionTrajectory (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) z
  obtain ⟨f,hf,hfs⟩ := Finset.mem_image.mp hs
  have hRec : ∃ᶠ n in atTop, (x n).1 = e.1 :=
    ((mem_recurrentSet x f).mp hf).mono (fun n hn => by simpa [hn] using hfs)
  have ha : e.2 ∈ retainedActions E e.1 := (mem_retainedActions E e.1 e.2).mpr he
  have hBoth := cycle_every_action_recurrent (fun k => (x k).1) e.1
    (retainedActions E e.1) fallback hRec ⟨e.2,ha⟩
  apply (mem_recurrentSet x e).mpr
  apply hBoth.mono
  intro n hn
  apply Prod.ext hn.1
  rw [stack_roundRobin_action E fallback s₀ z n, hn.1]
  exact hn.2

end HiddenParity.Sufficiency
