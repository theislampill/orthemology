import ReferenceClockControls

namespace ReferenceClockV6Review
noncomputable section
open Classical
open OperationalJoin OperationalJoin.Offset
open ComposedExecution NativeFixture ReferenceClockControls
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

theorem setting_same_reference_time_is_identity (w : World) :
    setReferenceTime w w.now = w := by
  cases w
  rfl

/-- Weak monotonicity permits arbitrarily many equal-time events. It supplies
neither strict clock progress nor any useful work. -/
theorem arbitrary_finite_clock_stalling {base n} (a : Authority base n)
    (w : World) (count : Nat) :
    MonotoneReferenceTrace a w (List.replicate count (.advance w.now)) w := by
  induction count with
  | zero => exact .nil _
  | succ count ih =>
      rw [List.replicate_succ]
      have step : MonotoneReferenceStep a w (.advance w.now) w := by
        simpa only [setting_same_reference_time_is_identity] using
          MonotoneReferenceStep.advance (a := a) w w.now (Nat.le_refl _)
      exact .cons step ih

/-- There is no numerical bound on the permitted forward jump. -/
theorem arbitrarily_large_forward_jump {base n} (a : Authority base n)
    (w : World) (delta : Nat) :
    MonotoneReferenceTrace a w [.advance (w.now + delta)]
      (setReferenceTime w (w.now + delta)) :=
  .cons (.advance w (w.now + delta) (Nat.le_add_right _ _)) (.nil _)

/-- The rollback control can use one and the same genuinely reachable common
state at both endpoints. Structural alignment alone does not enforce monotonicity. -/
theorem rollback_counterexample_is_aligned_and_reachable :
    ∃ s, Reachable authority.config s ∧
      Aligned authority (setReferenceTime installPrepared 100) s ∧
      Aligned authority (setReferenceTime installPrepared 2) s ∧
      (attempt (setReferenceTime installPrepared 100) installEnvelope.val "A" true).2 = false ∧
      (attempt (setReferenceTime installPrepared 2) installEnvelope.val "A" true).2 = true := by
  obtain ⟨alignment, history⟩ := prepare_preserves_alignment authority start
    (Initial authority.config before) start_aligned start_reachable installEnvelope "A" false (by decide)
  refine ⟨_, reachable_after start_reachable history,
    setReferenceTime_aligned alignment 100, setReferenceTime_aligned alignment 2, ?_, ?_⟩
  · decide
  · decide

/-- Expiry failure preserves the complete World, including the old commitments
and certificate stream. The conclusion quantifies over the shared badOpen flag. -/
theorem expired_attempt_full_identity {base n} (a : Authority base n)
    (w : World) (s : State (interface base n)) (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (e : Typed.BoundedEnvelope n)
    (requester : String) (badOpen : Bool) (expired : actionLeaseEnd e.val.action ≤ w.now) :
    (attempt w e.val requester badOpen).1 = w := by
  have rejected := expired_aligned_attempt_rejected a w s aligned reachable e requester badOpen expired
  cases outcome : (attempt w e.val requester badOpen).2 with
  | false => exact rejected_attempt_full_identity w e.val requester badOpen outcome
  | true => exact False.elim (rejected outcome)

def renewedEnvelope : Typed.BoundedEnvelope 4 :=
  ⟨⟨.install { _root_.installCommand with leaseEnd := 95 }, installed, 2, [1,2,3]⟩, by decide⟩

/-- Permanent rejection is scoped to the fixed envelope. A different fresh
command with a longer lease inside the same grant can still be admitted. -/
theorem renewed_envelope_can_land_after_original_expiry :
    (attempt (setReferenceTime installPrepared 90) installEnvelope.val "A" true).2 = false ∧
    (attempt (ComposedExecution.prepare (setReferenceTime start 90)
      renewedEnvelope.val "A" true).1 renewedEnvelope.val "A" true).2 = true ∧
    renewedEnvelope.val ≠ installEnvelope.val := by
  exact ⟨by decide, by decide, by decide⟩

/-- The lower observed-at bound is still checked after unrestricted updates;
backward time is not uniformly accepting. -/
theorem before_observed_at_is_rejected :
    (attempt (setReferenceTime installPrepared 0) installEnvelope.val "A" true).2 = false ∧
    (attempt (setReferenceTime installPrepared 1) installEnvelope.val "A" true).2 = true := by decide

def pathWithBadRoot : Typed.BoundedEnvelope 4 :=
  ⟨⟨installEnvelope.val.action, installEnvelope.val.successor, 3, [0,1,2]⟩, by decide⟩
def expiredPartial : World :=
  (ComposedExecution.prepare (setReferenceTime start 90) pathWithBadRoot.val "A" true).1

/-- An expired preparation can still collect a dishonest root's commitment.
The live honest gate, rather than absence of all preparation, prevents landing. -/
theorem expired_partial_preparation_does_not_land :
    (ComposedExecution.prepare (setReferenceTime start 90) pathWithBadRoot.val "A" true).2 = false ∧
    pathWithBadRoot.val ∈ (expiredPartial.roots 0).commitments ∧
    pathWithBadRoot.val ∉ (expiredPartial.roots 1).commitments ∧
    (attempt expiredPartial pathWithBadRoot.val "A" true).2 = false := by decide

/-- Clock changes do not alter fault membership or any admission threshold. -/
theorem reference_update_retains_fault_configuration (w : World) (now : Nat) :
    (setReferenceTime w now).n = w.n ∧
    (setReferenceTime w now).budget = w.budget ∧
    (setReferenceTime w now).q = w.q ∧
    (setReferenceTime w now).r = w.r ∧
    (setReferenceTime w now).tainted = w.tainted := by
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

/-- The whole existing cancellation trace embeds without imposing new clock
premises on each existing operation. -/
theorem old_cancellation_trace_embeds {base n} {a : Authority base n}
    {w v : World} {events : List (RuntimeWithCancellationEvent n)}
    (history : RuntimeWithCancellationTrace a w events v) :
    MonotoneReferenceTrace a w (events.map MonotoneReferenceEvent.ordinary) v :=
  runtime_cancel_trace_lifts history

#print axioms setting_same_reference_time_is_identity
#print axioms arbitrary_finite_clock_stalling
#print axioms arbitrarily_large_forward_jump
#print axioms rollback_counterexample_is_aligned_and_reachable
#print axioms expired_attempt_full_identity
#print axioms renewed_envelope_can_land_after_original_expiry
#print axioms before_observed_at_is_rejected
#print axioms expired_partial_preparation_does_not_land
#print axioms reference_update_retains_fault_configuration
#print axioms old_cancellation_trace_embeds
end
end ReferenceClockV6Review
