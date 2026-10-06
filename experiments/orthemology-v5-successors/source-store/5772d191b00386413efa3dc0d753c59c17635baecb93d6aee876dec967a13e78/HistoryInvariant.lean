import HistoryModel
namespace InterlockHistory

theorem consistent_initial {n} (c : Config n) (table : Table) :
    Consistent c (Initial c table) := by
  constructor
  · intro i hi
    simp [Initial, c.source_epoch]
  · intro i hi
    simp [Initial, c.source_epoch]
  · intro e he
    simp [Initial] at he
  · simp [Initial]
  · simp [Initial]
  · simp [Initial]

/-- A derived preservation lemma, applied only to the explicit root operations.
    It is not a transition rule and assumes no global landing property. -/
theorem consistent_setRoot {n} {c : Config n} {s : State n}
    (h : Consistent c s) (i : Fin n) (z : RootState n)
    (change : Good c i →
      z.descriptor = c.source z.descriptor.epoch ∧ z.descriptor.epoch ≤ s.epoch ∧
      (s.roots i).revoked ⊆ z.revoked ∧ (s.roots i).cancelled ⊆ z.cancelled) :
    Consistent c (setRoot s i z) := by
  constructor
  · intro j hj
    by_cases eq : j = i
    · subst j
      simpa [setRoot] using (change hj).1
    · simpa [setRoot, Function.update_of_ne eq] using h.local_authentic j hj
  · intro j hj
    by_cases eq : j = i
    · subst j
      simpa [setRoot] using (change hj).2.1
    · simpa [setRoot, Function.update_of_ne eq] using h.local_not_future j hj
  · intro e he
    obtain ⟨hc, hv⟩ := h.past_certificates e he
    refine ⟨hc, ?_⟩
    intro j hj hg
    by_cases eq : j = i
    · subst j
      simpa [setRoot] using (change hg).2.2.1 (hv i hj hg)
    · simpa [setRoot, Function.update_of_ne eq] using hv j hj hg
  · intro j hj hg
    by_cases eq : j = i
    · subst j
      simpa [setRoot] using (change hg).2.2.1 (h.pending_revoked i hj hg)
    · simpa [setRoot, Function.update_of_ne eq] using h.pending_revoked j hj hg
  · exact h.cancel_selected
  · intro k j hj hg
    by_cases eq : j = i
    · subst j
      simpa [setRoot] using (change hg).2.2.2 (h.cancel_durable k i hj hg)
    · simpa [setRoot, Function.update_of_ne eq] using h.cancel_durable k j hj hg

theorem consistent_request {n} {c : Config n} {s : State n}
    (h : Consistent c s) : Consistent c (request s) := by
  exact ⟨h.local_authentic, h.local_not_future, h.past_certificates,
    by simp [request], h.cancel_selected, h.cancel_durable⟩

theorem consistent_prepare {n} {c : Config n} {s : State n}
    (h : Consistent c s) (i : Fin n) (k : Command n) :
    Consistent c (prepare s i k) := by
  apply consistent_setRoot h
  intro hi
  exact ⟨h.local_authentic i hi, h.local_not_future i hi, subset_rfl, subset_rfl⟩

theorem consistent_corrupt {n} {c : Config n} {s : State n}
    (h : Consistent c s) (i : Fin n) (z : RootState n) (bad : i ∈ c.faulty) :
    Consistent c (setRoot s i z) := by
  apply consistent_setRoot h
  intro hi
  exact False.elim (hi bad)

theorem consistent_deliver {n} {c : Config n} {s : State n}
    (h : Consistent c s) (i : Fin n) (e : Nat) (he : e ≤ s.epoch) :
    Consistent c (deliver c s i e) := by
  unfold deliver
  split
  · apply consistent_setRoot h
    intro hi
    exact ⟨by rw [c.source_epoch], by simpa [c.source_epoch] using he,
      subset_rfl, subset_rfl⟩
  · exact h

theorem consistent_acknowledge {n} {c : Config n} {s : State n}
    (h : Consistent c s) (i : Fin n) : Consistent c (acknowledge c s i) := by
  by_cases hg : Good c i
  · have hz : Consistent c (setRoot s i
        { s.roots i with revoked := insert s.epoch (s.roots i).revoked }) := by
      apply consistent_setRoot h
      intro hi
      exact ⟨h.local_authentic i hi, h.local_not_future i hi,
        Finset.subset_insert _ _, subset_rfl⟩
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · simpa [acknowledge, hg, setRoot] using hz.local_authentic
    · simpa [acknowledge, hg, setRoot] using hz.local_not_future
    · simpa [acknowledge, hg, setRoot] using hz.past_certificates
    · intro j hj good
      change j ∈ insert i s.acks at hj
      rw [Finset.mem_insert] at hj
      rcases hj with eq | old
      · subst j
        simp [acknowledge, hg]
      · have hv := hz.pending_revoked j old good
        simpa [acknowledge, hg, setRoot] using hv
    · exact h.cancel_selected
    · simpa [acknowledge, hg, setRoot] using hz.cancel_durable
  · refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · simpa [acknowledge, hg] using h.local_authentic
    · simpa [acknowledge, hg] using h.local_not_future
    · simpa [acknowledge, hg] using h.past_certificates
    · intro j hj good
      change j ∈ insert i s.acks at hj
      rw [Finset.mem_insert] at hj
      rcases hj with eq | old
      · subst j
        exact False.elim (hg good)
      · simpa [acknowledge, hg] using h.pending_revoked j old good
    · exact h.cancel_selected
    · simpa [acknowledge, hg] using h.cancel_durable

theorem consistent_complete {n} {c : Config n} {s : State n}
    (h : Consistent c s) (quorum : s.acks.card = c.r) :
    Consistent c (complete s) := by
  refine ⟨h.local_authentic, ?_, ?_, ?_, h.cancel_selected, h.cancel_durable⟩
  · intro i hi
    have := h.local_not_future i hi
    change (s.roots i).descriptor.epoch ≤ s.epoch + 1
    omega
  · intro e he
    change e < s.epoch + 1 at he
    by_cases eq : e = s.epoch
    · subst e
      simpa [complete] using And.intro quorum h.pending_revoked
    · have lt : e < s.epoch := by omega
      simpa [complete, Function.update_of_ne eq] using h.past_certificates e lt
  · simp [complete]

theorem consistent_cancelAck {n} {c : Config n} {s : State n}
    (h : Consistent c s) (i : Fin n) (k : Command n) (selected : i ∈ k.path) :
    Consistent c (cancelAck c s i k) := by
  by_cases hg : Good c i
  · have hz : Consistent c (setRoot s i
        { s.roots i with cancelled := insert k (s.roots i).cancelled }) := by
      apply consistent_setRoot h
      intro hi
      exact ⟨h.local_authentic i hi, h.local_not_future i hi,
        subset_rfl, Finset.subset_insert _ _⟩
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · simpa [cancelAck, hg, setRoot] using hz.local_authentic
    · simpa [cancelAck, hg, setRoot] using hz.local_not_future
    · simpa [cancelAck, hg, setRoot] using hz.past_certificates
    · simpa [cancelAck, hg, setRoot] using hz.pending_revoked
    · intro k' j hj
      by_cases eq : k' = k
      · subst k'
        simp only [cancelAck, Function.update_self, Finset.mem_insert] at hj
        rcases hj with eq | old
        · simpa [eq] using selected
        · exact h.cancel_selected k j old
      · simp only [cancelAck, Function.update_of_ne eq] at hj
        exact h.cancel_selected k' j hj
    · intro k' j hj good
      by_cases eq : k' = k
      · subst k'
        simp only [cancelAck, Function.update_self, Finset.mem_insert] at hj
        rcases hj with eq | old
        · subst j
          simp [cancelAck, hg]
        · simpa [cancelAck, hg, setRoot] using hz.cancel_durable k j old good
      · simp only [cancelAck, Function.update_of_ne eq] at hj
        simpa [cancelAck, hg, setRoot] using hz.cancel_durable k' j hj good
  · refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · simpa [cancelAck, hg] using h.local_authentic
    · simpa [cancelAck, hg] using h.local_not_future
    · simpa [cancelAck, hg] using h.past_certificates
    · simpa [cancelAck, hg] using h.pending_revoked
    · intro k' j hj
      by_cases eq : k' = k
      · subst k'
        simp only [cancelAck, Function.update_self, Finset.mem_insert] at hj
        rcases hj with eq | old
        · simpa [eq] using selected
        · exact h.cancel_selected k j old
      · simp only [cancelAck, Function.update_of_ne eq] at hj
        exact h.cancel_selected k' j hj
    · intro k' j hj good
      by_cases eq : k' = k
      · subst k'
        simp only [cancelAck, Function.update_self, Finset.mem_insert] at hj
        rcases hj with eq | old
        · subst j
          exact False.elim (hg good)
        · simpa [cancelAck, hg] using h.cancel_durable k j old good
      · simp only [cancelAck, Function.update_of_ne eq] at hj
        simpa [cancelAck, hg] using h.cancel_durable k' j hj good

theorem consistent_land {n} {c : Config n} {s : State n}
    (h : Consistent c s) (k : Command n) (requester : Nat) :
    Consistent c (land c s k requester) := by
  unfold land
  split <;> exact ⟨h.local_authentic, h.local_not_future, h.past_certificates,
    h.pending_revoked, h.cancel_selected, h.cancel_durable⟩

theorem consistent_step {n} {c : Config n} {s t : State n} {a : Event n}
    (h : Consistent c s) (step : Step c s a t) : Consistent c t := by
  cases step with
  | request => exact consistent_request h
  | acknowledge => exact consistent_acknowledge h _
  | complete _ quorum => exact consistent_complete h quorum
  | deliver i e he => exact consistent_deliver h i e he.2
  | prepare => exact consistent_prepare h _ _
  | cancelAck i k _ selected _ => exact consistent_cancelAck h i k selected
  | close => exact h
  | land => exact consistent_land h _ _
  | hold => exact h
  | corrupt i z bad => exact consistent_corrupt h i z bad

theorem consistent_trace {n} {c : Config n} {s t : State n} {as : List (Event n)}
    (h : Consistent c s) (trace : Trace c s as t) : Consistent c t := by
  induction trace with
  | nil => exact h
  | cons step _ ih => exact ih (consistent_step h step)

theorem reachable_consistent {n} {c : Config n} {s : State n} (h : Reachable c s) :
    Consistent c s := by
  obtain ⟨table, events, trace⟩ := h
  exact consistent_trace (consistent_initial c table) trace

#print axioms consistent_trace
#print axioms reachable_consistent
end InterlockHistory
