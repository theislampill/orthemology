import LifecycleAttempt

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

/-- A deliberately bounded class of actual runtime operations. Paths retain
ordered full-envelope identity. Certification accepts only the authenticated
post-base serial source record; malformed/unrecorded deliveries are still represented. -/
inductive RuntimeEvent (n : Nat) where
  | prepare (e : BoundedEnvelope n) (requester : String) (badSign : Bool)
  | attempt (e : BoundedEnvelope n) (requester : String) (badOpen : Bool)
  | certify (index : Nat) (acknowledgers : List Nat)
  | deliver (certificate : ComposedExecution.Certificate)

inductive RuntimeStep {base n} (a : Authority base n) :
    ComposedExecution.World → RuntimeEvent n → ComposedExecution.World → Prop where
  | prepare (w e requester badSign) : RuntimeStep a w (.prepare e requester badSign)
      (ComposedExecution.prepare w e.val requester badSign).1
  | attempt (w e requester badOpen) : RuntimeStep a w (.attempt e requester badOpen)
      (ComposedExecution.attempt w e.val requester badOpen).1
  | certify (w index acknowledgers)
      (current : w.effectivePolicy.epoch = base + index)
      (nodup : acknowledgers.Nodup) (length : acknowledgers.length = a.r)
      (bounded : ∀ i ∈ acknowledgers, i < n) :
      RuntimeStep a w (.certify index acknowledgers)
        (ComposedExecution.certifyTransition w acknowledgers (a.source (index + 1))).1
  | deliver (w certificate) : RuntimeStep a w (.deliver certificate)
      (ComposedExecution.deliver w certificate)

inductive RuntimeTrace {base n} (a : Authority base n) :
    ComposedExecution.World → List (RuntimeEvent n) → ComposedExecution.World → Prop where
  | nil (w) : RuntimeTrace a w [] w
  | cons {w v u event events} : RuntimeStep a w event v → RuntimeTrace a v events u →
      RuntimeTrace a w (event :: events) u

theorem runtime_step_refines_history {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)} {event : RuntimeEvent n}
    (aligned : Aligned a w s) (reachable : Reachable a.config s) (step : RuntimeStep a w event v) :
    ∃ next events, Aligned a v next ∧ Trace a.config s events next := by
  cases step with
  | prepare e requester badSign =>
      cases valid : validPath w e.val with
      | false =>
          refine ⟨s, [], ?_, Trace.nil s⟩
          rw [prepare_invalid_path_identity w e.val requester badSign valid]
          exact aligned
      | true =>
          obtain ⟨alignment, history⟩ := prepare_preserves_alignment a w s aligned reachable e requester badSign valid
          exact ⟨_, _, alignment, history⟩
  | attempt e requester badOpen =>
      obtain ⟨next, events, alignment, history, _⟩ := attempt_preserves_alignment a w s aligned reachable e requester badOpen
      exact ⟨next, events, alignment, history⟩
  | certify index acknowledgers current nodup length bounded =>
      have raw := aligned_raw_epoch aligned
      have same : index = s.epoch := by omega
      subst index
      obtain ⟨alignment, history⟩ :=
        certifyTransition_preserves_alignment a w s aligned acknowledgers nodup length bounded
      exact ⟨_, _, alignment, history⟩
  | deliver certificate =>
      by_cases member : certificate ∈ w.completed
      · obtain ⟨index, _, _, alignment, history⟩ :=
          deliver_preserves_alignment a w s aligned reachable certificate member
        exact ⟨_, _, alignment, history⟩
      · refine ⟨s, [], ?_, Trace.nil s⟩
        simpa [ComposedExecution.deliver, member] using aligned

/-- Simulation is over arbitrary finite traces of the stated actual-operation
class. It is not a proof about runBatch, aggregate cancellation or liveness. -/
theorem runtime_trace_refines_history {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)} {events : List (RuntimeEvent n)}
    (aligned : Aligned a w s) (reachable : Reachable a.config s) (trace : RuntimeTrace a w events v) :
    ∃ next primitiveEvents, Aligned a v next ∧ Trace a.config s primitiveEvents next := by
  induction trace generalizing s with
  | nil => exact ⟨s, [], aligned, Trace.nil s⟩
  | cons step _ ih =>
      obtain ⟨middle, first, alignment, history⟩ := runtime_step_refines_history a aligned reachable step
      obtain ⟨next, rest, last, tail⟩ := ih alignment (reachable_after reachable history)
      exact ⟨next, first ++ rest, last, trace_append history tail⟩

/-- Every reached actual runtime snapshot has a genuine common history, so a
subsequent successful attempt is admitted under its full effective Policy. -/
theorem reached_runtime_current_admission {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)} {events : List (RuntimeEvent n)}
    (aligned : Aligned a w s) (reachable : Reachable a.config s) (trace : RuntimeTrace a w events v)
    (e : BoundedEnvelope n) (requester : String) (badOpen : Bool)
    (applied : (attempt v e.val requester badOpen).2 = true) :
    e.val.action.epoch = v.effectivePolicy.epoch ∧
      localStep v.plant v.effectivePolicy v.now e.val.action = some e.val.successor := by
  obtain ⟨next, _, alignment, history⟩ := runtime_trace_refines_history a aligned reachable trace
  exact successful_attempt_current_policy a v next alignment (reachable_after reachable history)
    e requester badOpen applied

#print axioms runtime_step_refines_history
#print axioms runtime_trace_refines_history
#print axioms reached_runtime_current_admission
end
end OperationalJoin.Offset
