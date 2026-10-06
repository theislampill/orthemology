import ModelControls

namespace SharedAlias.ReviewerControls
open OperationalJoin
noncomputable section
open Classical

/-- Every legal label address denotes an actual image root. -/
theorem addressed_root_in_image {m} {I : Interface m} (E : Environment I) (i : Fin m) :
    E.rootOf i ∈ AttributionKernel.actualRoots E.aliasClass := by
  apply Finset.mem_image.mpr
  exact ⟨i, Finset.mem_univ i, rfl⟩

/-- Ambient Option coordinates are storage padding; no legal step reaches them. -/
theorem unused_roots_unchanged {m} {I : Interface m} {E : Environment I}
    {C D : State I} {a : Event I} (step : Step E C a D)
    (r : Option (Fin m)) (unused : r ∉ AttributionKernel.actualRoots E.aliasClass) :
    D.roots r = C.roots r := by
  have ne : ∀ i, r ≠ E.rootOf i := by
    intro i eq
    exact unused (eq ▸ addressed_root_in_image E i)
  cases step with
  | request => rfl
  | acknowledge i pending =>
      simp only [acknowledge]
      split <;> simp [Function.update_of_ne (ne i)]
  | complete => rfl
  | deliver i e cert =>
      unfold deliver
      split <;> simp [setRoot, Function.update_of_ne (ne i)]
  | prepare i k who time selected path grant =>
      simp [prepare, setRoot, Function.update_of_ne (ne i)]
  | cancelAck i k who selected auth =>
      simp only [cancelAck]
      split <;> simp [Function.update_of_ne (ne i)]
  | close => rfl
  | land => rfl
  | hold => rfl
  | corrupt i z bad => simp [setRoot, Function.update_of_ne (ne i)]

theorem stale_delivery_is_identity {m} {I : Interface m} (E : Environment I)
    (C : State I) (i : Fin m) (e : Nat)
    (old : e ≤ I.policyEpoch (C.roots (E.rootOf i)).descriptor) : deliver E C i e = C := by
  simp [deliver, Nat.not_lt.mpr old]

theorem delivery_preserves_both_receipt_sets {m} {I : Interface m}
    (E : Environment I) (C : State I) (i : Fin m) (e : Nat) :
    (deliver E C i e).acks = C.acks ∧ (deliver E C i e).cancelAcks = C.cancelAcks := by
  unfold deliver
  split <;> exact ⟨rfl, rfl⟩

theorem preparation_preserves_both_receipt_sets {m} {I : Interface m}
    (E : Environment I) (C : State I) (i : Fin m) (k : I.Command) :
    (prepare E C i k).acks = C.acks ∧ (prepare E C i k).cancelAcks = C.cancelAcks := ⟨rfl, rfl⟩

open ModelControls

def sixReceipts : State testInterface :=
  { request (initial env ()) with acks := {0,1,2,3,4,5} }

theorem excess_real_receipts_cannot_complete (D : State testInterface) :
    ¬ Step env sixReceipts .complete D := by
  intro step
  cases step with
  | complete pending quorum =>
      have impossible : (6 : Nat) = 5 := by simpa [sixReceipts, env] using quorum
      omega

theorem one_reply_does_not_make_certificate (D : State testInterface) :
    ¬ Step env (cancelAck env (initial env ()) 0 command) (.close command) D := by
  intro step
  cases step with
  | close k certificate =>
      have impossible : (2 : Nat) < 1 := by
        simpa [cancelAck, initial, Environment.labelBudget, env] using certificate
      omega

theorem cancellation_literal_pullback_obstruction :
    ¬∃ s : OperationalJoin.State testInterface,
      OperationalJoin.Reachable env.labelConfig s ∧
      (command ∈ (s.roots 1).cancelled ↔
        command ∈ ((cancelAck env (initial env ()) 0 command).roots (env.rootOf 1)).cancelled) := by
  apply no_reachable_literal_cancel <;> decide

#print axioms addressed_root_in_image
#print axioms unused_roots_unchanged
#print axioms stale_delivery_is_identity
#print axioms delivery_preserves_both_receipt_sets
#print axioms preparation_preserves_both_receipt_sets
#print axioms excess_real_receipts_cannot_complete
#print axioms one_reply_does_not_make_certificate
#print axioms cancellation_literal_pullback_obstruction
end
end SharedAlias.ReviewerControls
