import JoinInvariant
namespace OperationalJoin
noncomputable section
open Classical

theorem good_member {n} {I : Interface n} (c : Config I) (L : Finset (Fin n))
    (large : c.budget < L.card) : ∃ i ∈ L, Good c i := by
  by_contra no
  have sub : L ⊆ c.faulty := by
    intro i hi
    by_contra hg
    exact no ⟨i, hi, hg⟩
  have := Finset.card_le_card sub
  have := c.budget_bound
  omega

theorem good_cross_member {n} {I : Interface n} (c : Config I) (L S : Finset (Fin n))
    (large : n + c.budget < L.card + S.card) :
    ∃ i ∈ L, i ∈ S ∧ Good c i := by
  by_contra no
  have sub : L ∩ S ⊆ c.faulty := by
    intro i hi
    obtain ⟨hl, hs⟩ := Finset.mem_inter.mp hi
    by_contra hg
    exact no ⟨i, hl, hs, hg⟩
  have interBound := Finset.card_le_card sub
  have unionBound : (L ∪ S).card ≤ n := by
    have := Finset.card_le_univ (L ∪ S)
    simpa using this
  have eq := Finset.card_union_add_card_inter L S
  have := c.budget_bound
  omega

theorem path_has_good {n} {I : Interface n} (c : Config I) (k : I.Command)
    (path : ValidPath c k) : ∃ i ∈ I.commandPath k, Good c i := by
  apply good_member
  have := c.overlap
  have := c.revoke_available
  unfold ValidPath at path
  omega

/-- Authenticity yields full policy identity, not only equal epoch numbers.
The two roots may belong to different consistent points of one authority stream. -/
theorem authentic_same_epoch {n} {I : Interface n} {c : Config I} {s t : State I}
    (hs : Consistent c s) (ht : Consistent c t) (i j : Fin n)
    (gi : Good c i) (gj : Good c j)
    (epochs : I.policyEpoch (s.roots i).descriptor = I.policyEpoch (t.roots j).descriptor) :
    (s.roots i).descriptor = (t.roots j).descriptor := by
  rw [hs.local_authentic i gi, epochs, ← ht.local_authentic j gj]

theorem stale_cannot_land {n} {I : Interface n} {c : Config I} {s : State I}
    (h : Consistent c s) (time : Nat) (k : I.Command) (requester : I.Requester)
    (old : I.commandEpoch k < s.epoch) : ¬Lands c s time k requester := by
  intro lands
  obtain ⟨size, closed⟩ := h.past_certificates (I.commandEpoch k) old
  have overlap : n + c.budget < (I.commandPath k).card +
      (s.certificates (I.commandEpoch k)).card := by
    rw [size, lands.1]
    exact c.overlap
  obtain ⟨i, path, cert, good⟩ := good_cross_member c _ _ overlap
  have gate := lands.2 i path good
  exact gate.2.2.1 (closed i cert good)

/-- Same actual plant/time are used in the root-local predicate and in the
current-policy conclusion. No effective policy is supplied to a live gate. -/
theorem admitted_current_authorized {n} {I : Interface n} {c : Config I} {s : State I}
    (h : Consistent c s) (time : Nat) (k : I.Command) (requester : I.Requester)
    (lands : Lands c s time k requester) :
    requester = I.recipient k ∧ I.commandEpoch k = s.epoch ∧
      I.admits s.plant time (c.source s.epoch) k requester := by
  obtain ⟨i, path, good⟩ := path_has_good c k lands.1
  have gate := lands.2 i path good
  have localEpoch : I.commandEpoch k = I.policyEpoch (s.roots i).descriptor :=
    I.admitted_epoch _ _ _ _ _ gate.2.1
  have notFuture : I.commandEpoch k ≤ s.epoch := by
    rw [localEpoch]
    exact h.local_not_future i good
  have current : I.commandEpoch k = s.epoch := by
    by_contra ne
    have old : I.commandEpoch k < s.epoch := by omega
    exact stale_cannot_land h time k requester old lands
  refine ⟨I.admitted_requester _ _ _ _ _ gate.2.1, current, ?_⟩
  have auth := gate.2.1
  rw [h.local_authentic i good, ← localEpoch, current] at auth
  exact auth

abbrev Cancelled {n} {I : Interface n} (c : Config I) (s : State I)
    (k : I.Command) : Prop := c.budget < (s.cancelAcks k).card

theorem cancelled_cannot_land {n} {I : Interface n} {c : Config I} {s : State I}
    (h : Consistent c s) (time : Nat) (k : I.Command) (requester : I.Requester)
    (closed : Cancelled c s k) : ¬Lands c s time k requester := by
  obtain ⟨i, ack, good⟩ := good_member c (s.cancelAcks k) closed
  intro lands
  have gate := lands.2 i (h.cancel_selected k i ack) good
  exact gate.2.2.2 (h.cancel_durable k i ack good)

theorem step_memory {n} {I : Interface n} {c : Config I} {s t : State I} {a : Event I}
    (step : Step c s a t) (i : Fin n) (good : Good c i) :
    (s.roots i).revoked ⊆ (t.roots i).revoked ∧
    (s.roots i).cancelled ⊆ (t.roots i).cancelled := by
  cases step <;>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, land,
      setRoot, Function.update_apply, Good] <;>
    split_ifs <;> simp_all [Function.update_apply] <;>
    split_ifs <;> simp_all

theorem step_cancelAcks {n} {I : Interface n} {c : Config I} {s t : State I} {a : Event I}
    (step : Step c s a t) (k : I.Command) : s.cancelAcks k ⊆ t.cancelAcks k := by
  cases step <;>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, land,
      setRoot, Function.update_apply] <;>
    split_ifs <;> simp_all

theorem step_epoch {n} {I : Interface n} {c : Config I} {s t : State I} {a : Event I}
    (step : Step c s a t) : s.epoch ≤ t.epoch := by
  cases step <;>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, land,
      setRoot] <;>
    split_ifs <;> simp_all

theorem trace_memory {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (trace : Trace c s as t) (i : Fin n) (good : Good c i) :
    (s.roots i).revoked ⊆ (t.roots i).revoked ∧
    (s.roots i).cancelled ⊆ (t.roots i).cancelled := by
  induction trace with
  | nil => exact ⟨subset_rfl, subset_rfl⟩
  | cons step _ ih =>
    have hm := step_memory step i good
    exact ⟨hm.1.trans ih.1, hm.2.trans ih.2⟩

theorem trace_cancelled {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (trace : Trace c s as t) (k : I.Command)
    (closed : Cancelled c s k) : Cancelled c t k := by
  induction trace with
  | nil => exact closed
  | cons step _ ih =>
    apply ih
    have := Finset.card_le_card (step_cancelAcks step k)
    unfold Cancelled at *
    omega

theorem no_landing_after_cancellation {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (reachable : Reachable c s) (trace : Trace c s as t)
    (time : Nat) (k : I.Command) (requester : I.Requester) (closed : Cancelled c s k) :
    ¬Lands c t time k requester := by
  exact cancelled_cannot_land (consistent_trace (reachable_consistent reachable) trace)
    time k requester (trace_cancelled trace k closed)

#print axioms authentic_same_epoch
#print axioms admitted_current_authorized
#print axioms no_landing_after_cancellation
end
end OperationalJoin
