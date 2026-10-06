import ReferenceClock

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

/-- Explicitly extends the actual-operation language with a NEW reference clock
operation. The actual service functions remain byte-for-byte unchanged. -/
inductive MonotoneReferenceEvent (n : Nat) where
  | ordinary (event : RuntimeWithCancellationEvent n)
  | advance (now : Nat)

inductive MonotoneReferenceStep {base n} (a : Authority base n) :
    ComposedExecution.World → MonotoneReferenceEvent n → ComposedExecution.World → Prop where
  | ordinary {w v event} : RuntimeWithCancellationStep a w event v →
      MonotoneReferenceStep a w (.ordinary event) v
  | advance (w : ComposedExecution.World) (now : Nat) (monotone : w.now ≤ now) :
      MonotoneReferenceStep a w (.advance now) (setReferenceTime w now)

inductive MonotoneReferenceTrace {base n} (a : Authority base n) :
    ComposedExecution.World → List (MonotoneReferenceEvent n) → ComposedExecution.World → Prop where
  | nil (w) : MonotoneReferenceTrace a w [] w
  | cons {w v u event events} : MonotoneReferenceStep a w event v →
      MonotoneReferenceTrace a v events u → MonotoneReferenceTrace a w (event :: events) u

theorem runtime_cancel_trace_lifts {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {events : List (RuntimeWithCancellationEvent n)}
    (history : RuntimeWithCancellationTrace a w events v) :
    MonotoneReferenceTrace a w (events.map MonotoneReferenceEvent.ordinary) v := by
  induction history with
  | nil => exact .nil _
  | cons step _ ih => exact .cons (.ordinary step) ih

/-- A clock update stutters the common state; subsequent preparation and landing
retain their exact actual World.now annotations through the inherited simulation. -/
theorem monotone_reference_step_refines_history {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)} {event : MonotoneReferenceEvent n}
    (aligned : Aligned a w s) (reachable : Reachable a.config s)
    (step : MonotoneReferenceStep a w event v) :
    ∃ next events, Aligned a v next ∧ Trace a.config s events next := by
  cases step with
  | ordinary step => exact runtime_cancel_step_refines_history a aligned reachable step
  | advance now monotone => exact ⟨s, [], setReferenceTime_aligned aligned now, Trace.nil s⟩

theorem monotone_reference_trace_refines_history {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)}
    {events : List (MonotoneReferenceEvent n)} (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (trace : MonotoneReferenceTrace a w events v) :
    ∃ next primitiveEvents, Aligned a v next ∧ Trace a.config s primitiveEvents next := by
  induction trace generalizing s with
  | nil => exact ⟨s, [], aligned, Trace.nil s⟩
  | cons step _ ih =>
      obtain ⟨middle, first, alignment, history⟩ := monotone_reference_step_refines_history a aligned reachable step
      obtain ⟨next, rest, last, tail⟩ := ih alignment (reachable_after reachable history)
      exact ⟨next, first ++ rest, last, trace_append history tail⟩

theorem monotone_reference_step_time {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {event : MonotoneReferenceEvent n}
    (step : MonotoneReferenceStep a w event v) : w.now ≤ v.now := by
  cases step with
  | ordinary step => exact Nat.le_of_eq (runtime_cancel_step_clock step).symm
  | advance now monotone => exact monotone

theorem monotone_reference_trace_time {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {events : List (MonotoneReferenceEvent n)}
    (history : MonotoneReferenceTrace a w events v) : w.now ≤ v.now := by
  induction history with
  | nil => exact Nat.le_refl _
  | cons step _ ih => exact Nat.le_trans (monotone_reference_step_time step) ih

theorem reached_monotone_reference_current_admission {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)}
    {events : List (MonotoneReferenceEvent n)} (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (trace : MonotoneReferenceTrace a w events v)
    (e : BoundedEnvelope n) (requester : String) (badOpen : Bool)
    (applied : (attempt v e.val requester badOpen).2 = true) :
    e.val.action.epoch = v.effectivePolicy.epoch ∧
      localStep v.plant v.effectivePolicy v.now e.val.action = some e.val.successor := by
  obtain ⟨next, _, last, history⟩ := monotone_reference_trace_refines_history a aligned reachable trace
  exact successful_attempt_current_policy a v next last (reachable_after reachable history)
    e requester badOpen applied

/-- Permanent expiry of this fixed action follows within the monotone reference
class. No inference to physical elapsed time or an authentic clock is made. -/
theorem expired_envelope_stays_rejected {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)}
    {events : List (MonotoneReferenceEvent n)} (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (trace : MonotoneReferenceTrace a w events v)
    (e : BoundedEnvelope n) (requester : String) (badOpen : Bool)
    (expired : actionLeaseEnd e.val.action ≤ w.now) : (attempt v e.val requester badOpen).2 ≠ true := by
  obtain ⟨next, _, last, history⟩ := monotone_reference_trace_refines_history a aligned reachable trace
  apply expired_aligned_attempt_rejected a v next last (reachable_after reachable history) e requester badOpen
  exact Nat.le_trans expired (monotone_reference_trace_time trace)

/-- The full-envelope cancellation theorem continues to hold across reference
clock updates, including updates passing the envelope's original lease end. -/
theorem true_cancel_blocks_monotone_reference_continuations {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n) (owner : String) (acks : List Nat)
    (closed : (cancelWith w e.val owner acks).2 = true)
    {later : ComposedExecution.World} {events : List (MonotoneReferenceEvent n)}
    (continuation : MonotoneReferenceTrace a (cancelWith w e.val owner acks).1 events later)
    (requester : String) (badOpen : Bool) : (attempt later e.val requester badOpen).2 ≠ true := by
  obtain ⟨valid, nodup, selected⟩ := true_cancel_outer_guards w e.val owner acks closed
  obtain ⟨middleAligned, cancellationHistory⟩ :=
    cancelWith_preserves_alignment a w s aligned e owner acks valid nodup selected
  have certificate := true_cancel_implies_certificate a w s aligned e owner acks valid nodup selected closed
  have middleReachable := reachable_after reachable cancellationHistory
  obtain ⟨next, _, lastAligned, history⟩ :=
    monotone_reference_trace_refines_history a middleAligned middleReachable continuation
  have veto := no_landing_after_cancellation middleReachable history later.now e requester certificate
  intro applied
  exact veto (successful_attempt_lands a later next lastAligned (reachable_after middleReachable history)
    e requester badOpen applied)

#print axioms monotone_reference_trace_refines_history
#print axioms monotone_reference_trace_time
#print axioms expired_envelope_stays_rejected
#print axioms true_cancel_blocks_monotone_reference_continuations
end
end OperationalJoin.Offset
