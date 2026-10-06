import SourceAttemptTransport

/-! Independent same-state controls: these inspect accepted full-key predicates,
not a modified handler or a boolean model. Nonidentity is an explicit premise.
No physical state conversion is inferred from the positive symmetry theorem. -/
namespace SharedAlias.OrderTransport.Controls
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface)
noncomputable section
open Classical

 theorem commitment_not_reusable {m} (T : Symmetry m)
    (p : ComposedExecution.Plant) (d : ComposedExecution.Policy) (time : Nat)
    (k : BoundedEnvelope m) (different : T.command k ≠ k)
    (accepted : ComposedExecution.localStep p d time k.val.action = some k.val.successor) :
    let z : RootState (interface m) := ⟨d, ∅, {k}, ∅⟩
    Permits p time z k k.val.action.actor ∧ ¬Permits p time z (T.command k) k.val.action.actor := by
  simp [Permits, Envelope, interface, different, accepted]

 theorem cancellation_not_reusable {m} (T : Symmetry m)
    (p : ComposedExecution.Plant) (d : ComposedExecution.Policy) (time : Nat)
    (k : BoundedEnvelope m) (different : T.command k ≠ k)
    (accepted : ComposedExecution.localStep p d time k.val.action = some k.val.successor) :
    let z : RootState (interface m) := ⟨d, ∅, {k, T.command k}, {k}⟩
    ¬Permits p time z k k.val.action.actor ∧ Permits p time z (T.command k) k.val.action.actor := by
  simp [Permits, Envelope, interface, different, T.action, T.successor, accepted]

 theorem unchanged_receipt_key_fails {m} (T : Symmetry m)
    (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (k : BoundedEnvelope m) (different : T.command k ≠ k)
    (valid : ValidPath E.labelConfig k) :
    let D := { C with cancelAcks := Function.update (fun _ => ∅) k (OperationalJoin.Typed.path k) }
    E.labelBudget < (D.cancelAcks k).card ∧ ¬E.labelBudget < (D.cancelAcks (T.command k)).card := by
  have big := SharedAlias.Progress.quorum_more_than_twice_budget E
  change (OperationalJoin.Typed.path k).card = E.q at valid
  have hbudget : E.labelBudget < E.q := by omega
  simpa [Function.update_apply, different, valid] using hbudget

 theorem root_payload_changes {m} (T : Symmetry m) (d : ComposedExecution.Policy)
    (k : BoundedEnvelope m) (different : T.command k ≠ k) :
    root T (⟨d, ∅, {k}, ∅⟩ : RootState (interface m)) ≠ ⟨d, ∅, {k}, ∅⟩ := by
  intro same
  have eq := congrArg RootState.commitments same
  have bad : T.command k = k := by simpa [root, memory] using eq
  exact different bad

 theorem unchanged_corrupt_payload_fails {m} (T : Symmetry m)
    (C : SharedAlias.State (interface m)) (r : Option (Fin m))
    (d : ComposedExecution.Policy) (k : BoundedEnvelope m) (different : T.command k ≠ k) :
    state T (SharedAlias.setRoot C r (⟨d, ∅, {k}, ∅⟩ : RootState (interface m))) ≠
      SharedAlias.setRoot (state T C) r (⟨d, ∅, {k}, ∅⟩ : RootState (interface m)) := by
  intro same
  have eq := congrArg (fun D : SharedAlias.State (interface m) => D.roots r) same
  have payload : root T (⟨d, ∅, {k}, ∅⟩ : RootState (interface m)) = ⟨d, ∅, {k}, ∅⟩ := by
    simpa [state, SharedAlias.setRoot] using eq
  exact root_payload_changes T d k different payload

 theorem corrupt_target {m} {E : Environment (interface m)}
    {C D : SharedAlias.State (interface m)} {i : Fin m} {z : RootState (interface m)}
    (h : SharedAlias.Step E C (.corrupt i z) D) : D = SharedAlias.setRoot C (E.rootOf i) z := by
  cases h
  rfl

 theorem unchanged_corrupt_event_is_illegal {m} (T : Symmetry m)
    (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (i : Fin m) (bad : i ∈ E.labelConfig.faulty) (d : ComposedExecution.Policy)
    (k : BoundedEnvelope m) (different : T.command k ≠ k) :
    let z : RootState (interface m) := ⟨d, ∅, {k}, ∅⟩
    SharedAlias.Step E C (.corrupt i z) (SharedAlias.setRoot C (E.rootOf i) z) ∧
      ¬SharedAlias.Step E (state T C) (.corrupt i z)
        (state T (SharedAlias.setRoot C (E.rootOf i) z)) := by
  constructor
  · exact SharedAlias.Step.corrupt C i _ bad
  · intro h
    exact unchanged_corrupt_payload_fails T C (E.rootOf i) d k different (corrupt_target h)

end
end SharedAlias.OrderTransport.Controls
