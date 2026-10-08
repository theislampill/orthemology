import HistoryInvariant
namespace InterlockHistory

theorem good_member {n} (c : Config n) (L : Finset (Fin n))
    (large : c.budget < L.card) : ∃ i ∈ L, Good c i := by
  classical
  by_contra no
  have sub : L ⊆ c.faulty := by
    intro i hi
    by_contra hg
    exact no ⟨i, hi, hg⟩
  have := Finset.card_le_card sub
  have := c.budget_bound
  omega

theorem good_cross_member {n} (c : Config n) (L S : Finset (Fin n))
    (large : n + c.budget < L.card + S.card) :
    ∃ i ∈ L, i ∈ S ∧ Good c i := by
  classical
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

theorem path_has_good {n} (c : Config n) (k : Command n) (path : ValidPath c k) :
    ∃ i ∈ k.path, Good c i := by
  apply good_member
  have := c.overlap
  have := c.revoke_available
  unfold ValidPath at path
  omega

/-- Old epochs are blocked by a previously acknowledged, still-durable physical
    veto. Local descriptors need not have received any newer certificate. -/
theorem stale_cannot_land {n} {c : Config n} {s : State n}
    (h : Consistent c s) (k : Command n) (requester : Nat)
    (old : k.epoch < s.epoch) : ¬Lands c s k requester := by
  intro lands
  obtain ⟨size, closed⟩ := h.past_certificates k.epoch old
  have overlap : n + c.budget < k.path.card + (s.certificates k.epoch).card := by
    rw [size, lands.1]
    exact c.overlap
  obtain ⟨i, path, cert, good⟩ := good_cross_member c _ _ overlap
  have gate := lands.2 i path good
  exact gate.2.2.2.1 (closed i cert good)

/-- The local descriptor equals an authentic completed descriptor by induction;
    no honest gate is given global permission or currentness as an oracle. -/
theorem admitted_current_authorized {n} {c : Config n} {s : State n}
    (h : Consistent c s) (k : Command n) (requester : Nat)
    (lands : Lands c s k requester) :
    requester = k.recipient ∧ k.epoch = s.epoch ∧ Authorized k (c.source s.epoch) := by
  obtain ⟨i, path, good⟩ := path_has_good c k lands.1
  have gate := lands.2 i path good
  have localEpoch : k.epoch = (s.roots i).descriptor.epoch := gate.2.2.1.2.1
  have notFuture : k.epoch ≤ s.epoch := by
    rw [localEpoch]
    exact h.local_not_future i good
  have current : k.epoch = s.epoch := by
    by_contra ne
    have old : k.epoch < s.epoch := by omega
    exact stale_cannot_land h k requester old lands
  refine ⟨gate.2.1, current, ?_⟩
  have auth := gate.2.2.1
  rw [h.local_authentic i good, ← localEpoch, current] at auth
  exact auth

abbrev Cancelled {n} (c : Config n) (s : State n) (k : Command n) : Prop :=
  c.budget < (s.cancelAcks k).card

/-- The cancellation certificate is only evidence. The actual blocking cause is
    one selected honest acknowledger's full-command tombstone at its live gate. -/
theorem cancelled_cannot_land {n} {c : Config n} {s : State n}
    (h : Consistent c s) (k : Command n) (requester : Nat)
    (closed : Cancelled c s k) : ¬Lands c s k requester := by
  obtain ⟨i, ack, good⟩ := good_member c (s.cancelAcks k) closed
  intro lands
  have gate := lands.2 i (h.cancel_selected k i ack) good
  exact gate.2.2.2.2 (h.cancel_durable k i ack good)

/-- Actual step-wise memory monotonicity, independent of the invariant proof. -/
theorem step_memory {n} {c : Config n} {s t : State n} {a : Event n}
    (step : Step c s a t) (i : Fin n) (good : Good c i) :
    (s.roots i).revoked ⊆ (t.roots i).revoked ∧
    (s.roots i).cancelled ⊆ (t.roots i).cancelled := by
  cases step <;>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, land,
      setRoot, Function.update_apply, Good] <;>
    split_ifs <;> simp_all [Function.update_apply] <;>
    split_ifs <;> simp_all

theorem step_cancelAcks {n} {c : Config n} {s t : State n} {a : Event n}
    (step : Step c s a t) (k : Command n) : s.cancelAcks k ⊆ t.cancelAcks k := by
  cases step <;>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, land,
      setRoot, Function.update_apply] <;>
    split_ifs <;> simp_all

theorem step_epoch {n} {c : Config n} {s t : State n} {a : Event n}
    (step : Step c s a t) : s.epoch ≤ t.epoch := by
  cases step <;>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, land,
      setRoot] <;>
    split_ifs <;> simp_all

theorem trace_memory {n} {c : Config n} {s t : State n} {as : List (Event n)}
    (trace : Trace c s as t) (i : Fin n) (good : Good c i) :
    (s.roots i).revoked ⊆ (t.roots i).revoked ∧
    (s.roots i).cancelled ⊆ (t.roots i).cancelled := by
  induction trace with
  | nil => exact ⟨subset_rfl, subset_rfl⟩
  | cons step _ ih =>
    have hm := step_memory step i good
    exact ⟨hm.1.trans ih.1, hm.2.trans ih.2⟩

theorem trace_cancelled {n} {c : Config n} {s t : State n} {as : List (Event n)}
    (trace : Trace c s as t) (k : Command n) (closed : Cancelled c s k) :
    Cancelled c t k := by
  induction trace with
  | nil => exact closed
  | cons step _ ih =>
    apply ih
    have := Finset.card_le_card (step_cancelAcks step k)
    unfold Cancelled at *
    omega

theorem no_landing_after_cancellation {n} {c : Config n} {s t : State n}
    {as : List (Event n)} (reachable : Reachable c s) (trace : Trace c s as t)
    (k : Command n) (requester : Nat) (closed : Cancelled c s k) :
    ¬Lands c t k requester := by
  exact cancelled_cannot_land (consistent_trace (reachable_consistent reachable) trace)
    k requester (trace_cancelled trace k closed)

/-- Exact payload binding is an explicit consequence, not a separate assumption. -/
theorem admitted_exact_target {n} {c : Config n} {s : State n}
    (reachable : Reachable c s) (k : Command n) (requester : Nat)
    (lands : Lands c s k requester) : k.table = (c.source s.epoch).table := by
  exact (admitted_current_authorized (reachable_consistent reachable) k requester lands).2.2.2.2.2.2.2.2

#print axioms stale_cannot_land
#print axioms admitted_current_authorized
#print axioms no_landing_after_cancellation
#print axioms trace_memory
#print axioms admitted_exact_target
end InterlockHistory
