import AliasModel

namespace SharedAlias
open OperationalJoin
noncomputable section
open Classical

/-- An additional reachability invariant of the unchanged common machine. -/
def SelectedMemory {m} {I : Interface m} (c : Config I) (s : OperationalJoin.State I) : Prop :=
  ∀ i, Good c i → ∀ k,
    (k ∈ (s.roots i).commitments ∨ k ∈ (s.roots i).cancelled) → i ∈ I.commandPath k

theorem selected_memory_initial {m} {I : Interface m} (c : Config I) (p : I.Plant) :
    SelectedMemory c (Initial c p) := by
  intro i good k member
  simp [Initial] at member

theorem selected_memory_step {m} {I : Interface m} {c : Config I}
    {s t : OperationalJoin.State I} {a : Event I} (h : SelectedMemory c s)
    (step : OperationalJoin.Step c s a t) : SelectedMemory c t := by
  intro j good k member
  cases step with
  | request => exact h j good k member
  | acknowledge i pending =>
      have old : k ∈ (s.roots j).commitments ∨ k ∈ (s.roots j).cancelled := by
        by_cases gi : Good c i
        · by_cases same : j = i
          · subst j
            simpa only [OperationalJoin.acknowledge, if_pos gi, Function.update_self] using member
          · simpa only [OperationalJoin.acknowledge, if_pos gi, Function.update_of_ne same] using member
        · simpa only [OperationalJoin.acknowledge, if_neg gi] using member
      exact h j good k old
  | complete => exact h j good k member
  | deliver i e cert =>
      unfold OperationalJoin.deliver at member
      split at member
      · by_cases same : j = i
        · subst j
          simp [OperationalJoin.setRoot] at member
          exact h i good k member
        · simp [OperationalJoin.setRoot, Function.update_of_ne same] at member
          exact h j good k member
      · exact h j good k member
  | prepare i command who time selected path grant =>
      by_cases same : j = i
      · subst j
        simp only [OperationalJoin.prepare, OperationalJoin.setRoot, Function.update_self,
          Finset.mem_insert] at member
        rcases member with (eq | old) | old
        · simpa [eq] using selected
        · exact h i good k (Or.inl old)
        · exact h i good k (Or.inr old)
      · simp [OperationalJoin.prepare, OperationalJoin.setRoot, Function.update_of_ne same] at member
        exact h j good k member
  | cancelAck i command who selected auth =>
      by_cases same : j = i
      · subst j
        simp only [OperationalJoin.cancelAck, if_pos good, Function.update_self,
          Finset.mem_insert] at member
        rcases member with old | (eq | old)
        · exact h i good k (Or.inl old)
        · simpa [eq] using selected
        · exact h i good k (Or.inr old)
      · by_cases gi : Good c i
        · simp [OperationalJoin.cancelAck, gi, Function.update_of_ne same] at member
          exact h j good k member
        · simp [OperationalJoin.cancelAck, gi] at member
          exact h j good k member
  | close => exact h j good k member
  | land command who time admitted =>
      unfold OperationalJoin.land at member
      split at member <;> exact h j good k member
  | hold => exact h j good k member
  | corrupt i z bad =>
      have ne : j ≠ i := by intro eq; subst j; exact good bad
      simp [OperationalJoin.setRoot, Function.update_of_ne ne] at member
      exact h j good k member

theorem selected_memory_trace {m} {I : Interface m} {c : Config I}
    {s t : OperationalJoin.State I} {events : List (Event I)}
    (h : SelectedMemory c s) (trace : OperationalJoin.Trace c s events t) :
    SelectedMemory c t := by
  induction trace with
  | nil => exact h
  | cons step _ ih => exact ih (selected_memory_step h step)

theorem selected_memory_reachable {m} {I : Interface m} {c : Config I}
    {s : OperationalJoin.State I} (reach : OperationalJoin.Reachable c s) :
    SelectedMemory c s := by
  obtain ⟨p, events, trace⟩ := reach
  exact selected_memory_trace (selected_memory_initial c p) trace

/-- No reachable common state can have even this single literal shared-store
commitment equality at a good, unselected alias. No whole-state match is needed. -/
theorem no_reachable_literal_prepare {m} {I : Interface m} (E : Environment I)
    (C : State I) (i j : Fin m) (k : I.Command)
    (same : E.rootOf j = E.rootOf i) (good : Good E.labelConfig j)
    (unselected : j ∉ I.commandPath k) :
    ¬∃ s : OperationalJoin.State I, OperationalJoin.Reachable E.labelConfig s ∧
      (k ∈ (s.roots j).commitments ↔
        k ∈ ((prepare E C i k).roots (E.rootOf j)).commitments) := by
  rintro ⟨s, reachable, literal⟩
  exact unselected (selected_memory_reachable reachable j good k
    (Or.inl (literal.mpr (shared_prepare E C i j k same))))

theorem no_reachable_literal_cancel {m} {I : Interface m} (E : Environment I)
    (C : State I) (i j : Fin m) (k : I.Command)
    (same : E.rootOf j = E.rootOf i) (good : Good E.labelConfig i)
    (unselected : j ∉ I.commandPath k) :
    ¬∃ s : OperationalJoin.State I, OperationalJoin.Reachable E.labelConfig s ∧
      (k ∈ (s.roots j).cancelled ↔
        k ∈ ((cancelAck E C i k).roots (E.rootOf j)).cancelled) := by
  rintro ⟨s, reachable, literal⟩
  have goodJ : Good E.labelConfig j := (good_same_root E j i same).mpr good
  exact unselected (selected_memory_reachable reachable j goodJ k
    (Or.inr (literal.mpr (shared_cancel E C i j k same good))))

end
end SharedAlias
