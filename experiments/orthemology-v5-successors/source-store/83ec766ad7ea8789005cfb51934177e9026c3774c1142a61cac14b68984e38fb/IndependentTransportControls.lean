import SourceAttemptTransport

namespace TransportIndependentReview
open SharedAlias SharedAlias.OrderTransport OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface path)
noncomputable section
open Classical

-- No second support-dependent choice is available after the first swap.
theorem no_complete_key_collision {m} (A : Profile m) (a b : BoundedEnvelope m) :
    selected A a = selected A b ↔ a = b := (selectedEquiv A).injective.eq_iff

theorem same_support_does_not_collapse {m} (A : Profile m) (a b : BoundedEnvelope m)
    (_same : path a = path b) (different : a ≠ b) : selected A a ≠ selected A b :=
  fun eq => different ((no_complete_key_collision A a b).mp eq)

def sortCommand {m} (k : BoundedEnvelope m) : BoundedEnvelope m :=
  ⟨{k.val with path := SharedAlias.Progress.labelList (path k)},
    SharedAlias.Progress.labelList_nodup _, SharedAlias.Progress.labelList_bounded _⟩

theorem sorting_collapses_a_nonfixed_pair {m} (T : Symmetry m) (k : BoundedEnvelope m) :
    sortCommand (T.command k) = sortCommand k := by
  apply Subtype.ext
  change (⟨(T.command k).val.action, (T.command k).val.successor, (T.command k).val.nonce,
    SharedAlias.Progress.labelList (path (T.command k))⟩ : ComposedExecution.Envelope) = _
  rw [T.action, T.successor, T.nonce, T.support]
  rfl

theorem sorting_not_injective_if_nonfixed {m} (T : Symmetry m) (k : BoundedEnvelope m)
    (different : T.command k ≠ k) : ¬Function.Injective (sortCommand (m := m)) := by
  intro inj
  exact different (inj (sorting_collapses_a_nonfixed_pair T k))

-- All fields omitted by record-update syntax remain exactly equal.
theorem full_unchanged_fields {m} (T : Symmetry m) (C : SharedAlias.State (interface m)) :
    (state T C).epoch = C.epoch ∧ (state T C).pending = C.pending ∧
    (state T C).acks = C.acks ∧ (state T C).certificates = C.certificates ∧
    (state T C).plant = C.plant := ⟨rfl,rfl,rfl,rfl,rfl⟩

theorem full_root_fields {m} (T : Symmetry m) (z : RootState (interface m)) :
    (root T z).descriptor = z.descriptor ∧ (root T z).revoked = z.revoked ∧
    (∀ k, T.command k ∈ (root T z).commitments ↔ k ∈ z.commitments) ∧
    (∀ k, T.command k ∈ (root T z).cancelled ↔ k ∈ z.cancelled) := by
  exact ⟨rfl, rfl, fun _ => mem_memory_command T _ _, fun _ => mem_memory_command T _ _⟩

theorem effect_exact {m} (T : Symmetry m) (p : ComposedExecution.Plant) (k : BoundedEnvelope m) :
    (interface m).effect p (T.command k) = (interface m).effect p k := T.successor k

theorem traces_keep_positions {m} (T : Symmetry m) (a b : Event (interface m))
    (rest : List (Event (interface m))) :
    (a :: b :: rest).map (event T) = event T a :: event T b :: rest.map (event T) := rfl

theorem corrupt_payload_and_order {m} (T : Symmetry m) (i : Fin m)
    (z : RootState (interface m)) (k : BoundedEnvelope m) (who : String) (t : Nat) :
    ([Event.corrupt i z, Event.prepare i k who t, Event.close k]).map (event T) =
    [Event.corrupt i (root T z), Event.prepare i (T.command k) who t, Event.close (T.command k)] := rfl

-- Same-state close-event legality changes when only the command key is swapped.
theorem close_iff_key_quorum {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) :
    SharedAlias.Step E C (.close k) C ↔ E.labelBudget < (C.cancelAcks k).card := by
  constructor
  · intro h; cases h; assumption
  · exact SharedAlias.Step.close C k

theorem unchanged_state_close_failure {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (different : T.command k ≠ k)
    (qs : Finset (Fin m)) (enough : E.labelBudget < qs.card) :
    let D : SharedAlias.State (interface m) :=
      { C with cancelAcks := Function.update (fun _ => ∅) k qs }
    SharedAlias.Step E D (.close k) D ∧ ¬SharedAlias.Step E D (.close (T.command k)) D := by
  dsimp
  rw [close_iff_key_quorum, close_iff_key_quorum]
  simpa [Function.update_apply, different] using enough

-- Exact false and true source results, with arbitrary rather than reachable states.
theorem withholding_preserved {m} (A : Profile m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String) (t : Nat) :
    Progress.applied E (state (profileSymmetry A) C) (selected A k) who t false =
    Progress.applied E C k who t false := applied_eq (profileSymmetry A) E C k who t false

theorem opening_preserved {m} (A : Profile m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String) (t : Nat) :
    Progress.applied E (state (profileSymmetry A) C) (selected A k) who t true =
    Progress.applied E C k who t true := applied_eq (profileSymmetry A) E C k who t true

end
end TransportIndependentReview
