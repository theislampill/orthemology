import NativeEntryData

namespace SharedAlias.Native.Entry
open ComposedExecution
open OperationalJoin.Typed (interface)
noncomputable section
open Classical

theorem revoke_quorum_positive {m} (E : SharedAlias.Environment (interface m)) : 0 < E.r := by
  have overlap := E.overlap
  have available := E.repair_available
  omega

/-- Exact-r is inherited from accepted completion, not an arbitrary stronger
wrapper threshold. The certificate function itself survives shared simulation. -/
theorem reachable_certificate_card {m} (E : SharedAlias.Environment (interface m))
    (C : SharedAlias.State (interface m)) (reach : SharedAlias.Reachable E C)
    (e : Nat) (past : e < C.epoch) : (C.certificates e).card = E.r := by
  obtain ⟨s, reached, related⟩ := SharedAlias.reachable_witness reach
  have before : e < s.epoch := by simpa only [related.epoch] using past
  have card := ((OperationalJoin.reachable_consistent reached).past_certificates e before).1
  simpa only [related.certificates] using card

theorem tableRead_find {α β : Type} [DecidableEq α] (rows : List (α × β))
    (key : α) (fallback : β) :
    tableRead rows key fallback = (tableFind rows key).getD fallback := by
  induction rows with
  | nil => rfl
  | cons row rows ih =>
      obtain ⟨k,v⟩ := row
      by_cases same : key = k
      · simp [tableRead, tableFind, same]
      · simp [tableRead, tableFind, same, ih]

/-- A reachable nonzero representation cannot hide a missing row behind the
empty fallback. Duplicate raw labels and noncanonical/shadowed tables are fine. -/
theorem completionRow_present {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matches : RoutingMatches D E) (C : FiniteState m)
    (reach : SharedAlias.Reachable E (view C)) (positive : 0 < C.epoch) :
    ∃ labels, completionRow D C C.epoch = some labels ∧
      tableFind C.certificateRows (C.epoch - 1) = some labels ∧ labels.toFinset.card = D.r := by
  cases epoch : C.epoch with
  | zero => omega
  | succ e =>
      have card := reachable_certificate_card E (view C) reach e (by change e < C.epoch; omega)
      change (tableRead C.certificateRows e []).toFinset.card = E.r at card
      rw [tableRead_find] at card
      cases found : tableFind C.certificateRows e with
      | none =>
          rw [found] at card
          have pos := revoke_quorum_positive E
          simp only [Option.getD_none, List.toFinset_nil, Finset.card_empty] at card
          omega
      | some labels =>
          have size : labels.toFinset.card = D.r := by
            simpa only [found, Option.getD_some, matches.revokeQuorum] using card
          refine ⟨labels, ?_, ?_, size⟩
          · simp only [epoch, completionRow, found, Option.bind_some, size, ↓reduceIte]
          · simpa only [epoch, Nat.add_sub_cancel] using found

/-- The wrapper's shape checks are total on every represented reachable idle
state satisfying authentic actor observation and explicitly present sample. -/
theorem checkedPolicy_complete {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matches : RoutingMatches D E) (C : FiniteState m) (actor : Actor)
    (samples : List (Nat × Policy)) (bits : List Bool)
    (reach : SharedAlias.Reachable E (view C)) (idle : C.pending = false)
    (observed : actor.observedPlant = C.plant) (authentic : actor.policy = E.source C.epoch)
    (sample : policySample samples C.epoch = some actor.policy) (count : bits.length = m) :
    checkedPolicy D C actor samples bits = some actor.policy := by
  have epoch : actor.policy.epoch = C.epoch := by rw [authentic]; exact E.source_epoch C.epoch
  unfold checkedPolicy
  simp only [idle, Bool.false_eq_true, ↓reduceIte, epoch, observed, count, and_self, sample,
    Option.bind_some]
  by_cases zero : C.epoch = 0
  · simp [zero]
  · obtain ⟨labels, present, _, _⟩ := completionRow_present D E matches C reach (Nat.pos_of_ne_zero zero)
    simp [zero, present]

end
end SharedAlias.Native.Entry
