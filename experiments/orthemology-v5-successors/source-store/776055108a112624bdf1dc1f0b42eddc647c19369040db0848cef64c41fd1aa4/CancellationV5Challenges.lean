import RuntimeCancellationControls

namespace CancellationV5Review
noncomputable section
open Classical
open OperationalJoin OperationalJoin.Offset
open NativeFixture CancellationControls
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- B+1 is sufficient to certify an intact reply without knowing its identity.
A known intact single reply can veto even though this call's Boolean is false. -/
theorem one_intact_reply_can_veto_without_true_boolean :
    (ComposedExecution.cancelWith start installEnvelope.val "A" [1]).2 = false ∧
    (ComposedExecution.attempt
      (ComposedExecution.prepare falseFirst installEnvelope.val "A" true).1
      installEnvelope.val "A" true).2 = false := by decide

theorem one_intact_reply_has_no_B_plus_one_certificate :
    ¬Cancelled authority.config commonFalseFirst installEnvelope := by
  unfold Cancelled
  rw [cumulative_acknowledgement_sets.1]
  decide

/-- Distinct-root count is idempotent, but the actual runtime list may retain
duplicate tombstone entries across separate calls. -/
theorem repeated_call_appends_runtime_tombstone :
    (falseFirst.roots 1).cancelled.length = 1 ∧
    ((ComposedExecution.cancelWith falseFirst installEnvelope.val "A" [1]).1.roots 1).cancelled.length = 2 ∧
    commonRepeated.cancelAcks installEnvelope = {1} := by
  exact ⟨by decide, by decide, cumulative_acknowledgement_sets.2.2⟩

/-- The deduplicated repeated-call state is itself produced by real calls and
allowed common histories, rather than by manually setting an evidence field. -/
theorem repeated_call_state_is_genuine :
    Aligned authority (ComposedExecution.cancelWith falseFirst installEnvelope.val "A" [1]).1 commonRepeated ∧
    Reachable authority.config commonRepeated := by
  have first := cancelWith_preserves_alignment authority start commonStart start_aligned
    installEnvelope "A" [1] (by decide) (by decide) (by decide)
  have second := cancelWith_preserves_alignment authority falseFirst commonFalseFirst first.1
    installEnvelope "A" [1] (by decide) (by decide) (by decide)
  exact ⟨second.1, reachable_after (reachable_after start_reachable first.2) second.2⟩

/-- Every actual call preserves the entire plant, including failures and
cleanup after execution or revocation. No local-step validity premise is used. -/
theorem cancellation_never_changes_plant (w : ComposedExecution.World)
    (e : ComposedExecution.Envelope) (requester : String) (acks : List Nat) :
    (ComposedExecution.cancelWith w e requester acks).1.plant = w.plant := by
  unfold ComposedExecution.cancelWith
  split <;> rfl

/-- Wrong requesters cannot mutate any root, independent of their reply count.
This is model-string equality, with no claimed real authentication warrant. -/
theorem wrong_requester_full_world_identity (w : ComposedExecution.World)
    (e : ComposedExecution.Envelope) (requester : String) (acks : List Nat)
    (wrong : requester ≠ e.action.actor) :
    (ComposedExecution.cancelWith w e requester acks).1 = w := by
  simp [ComposedExecution.cancelWith, wrong]
  split <;> rfl

/-- Cancellation never erases commitments: a late attempt is stopped by the
durable full-envelope veto, not by deleting the old preparation evidence. -/
theorem cancellation_preserves_commitments (w : ComposedExecution.World)
    (e : ComposedExecution.Envelope) (requester : String) (acks : List Nat) (i : Nat) :
    ((ComposedExecution.cancelWith w e requester acks).1.roots i).commitments = (w.roots i).commitments := by
  unfold ComposedExecution.cancelWith
  split
  · dsimp only
    split <;> rfl
  · rfl

/-- The unchanged old runtime class embeds without extra side conditions. -/
theorem old_trace_embeds_exactly {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {events : List (RuntimeEvent n)}
    (history : RuntimeTrace a w events v) :
    RuntimeWithCancellationTrace a w (events.map RuntimeWithCancellationEvent.ordinary) v :=
  ordinary_runtime_trace_lifts history

#print axioms one_intact_reply_can_veto_without_true_boolean
#print axioms one_intact_reply_has_no_B_plus_one_certificate
#print axioms repeated_call_appends_runtime_tombstone
#print axioms repeated_call_state_is_genuine
#print axioms cancellation_never_changes_plant
#print axioms wrong_requester_full_world_identity
#print axioms cancellation_preserves_commitments
#print axioms old_trace_embeds_exactly
end
end CancellationV5Review
