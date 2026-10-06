import LifecycleCancellation

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

/-- A separate successor event language keeps the accepted v4 class unchanged. -/
inductive RuntimeWithCancellationEvent (n : Nat) where
  | ordinary (event : RuntimeEvent n)
  | cancel (e : BoundedEnvelope n) (requester : String) (acknowledgers : List Nat)

inductive RuntimeWithCancellationStep {base n} (a : Authority base n) :
    ComposedExecution.World → RuntimeWithCancellationEvent n → ComposedExecution.World → Prop where
  | ordinary {w v event} : RuntimeStep a w event v →
      RuntimeWithCancellationStep a w (.ordinary event) v
  | cancel (w e requester acknowledgers) : RuntimeWithCancellationStep a w (.cancel e requester acknowledgers)
      (cancelWith w e.val requester acknowledgers).1

inductive RuntimeWithCancellationTrace {base n} (a : Authority base n) :
    ComposedExecution.World → List (RuntimeWithCancellationEvent n) → ComposedExecution.World → Prop where
  | nil (w) : RuntimeWithCancellationTrace a w [] w
  | cons {w v u event events} : RuntimeWithCancellationStep a w event v →
      RuntimeWithCancellationTrace a v events u →
      RuntimeWithCancellationTrace a w (event :: events) u

theorem ordinary_runtime_trace_lifts {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {events : List (RuntimeEvent n)} (history : RuntimeTrace a w events v) :
    RuntimeWithCancellationTrace a w (events.map RuntimeWithCancellationEvent.ordinary) v := by
  induction history with
  | nil => exact .nil _
  | cons step _ ih => exact .cons (.ordinary step) ih

theorem runtime_cancel_step_refines_history {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)} {event : RuntimeWithCancellationEvent n}
    (aligned : Aligned a w s) (reachable : Reachable a.config s)
    (step : RuntimeWithCancellationStep a w event v) :
    ∃ next events, Aligned a v next ∧ Trace a.config s events next := by
  cases step with
  | ordinary step => exact runtime_step_refines_history a aligned reachable step
  | cancel e requester acknowledgers =>
      by_cases valid : validPath w e.val = true ∧ acknowledgers.Nodup ∧
          ∀ i ∈ acknowledgers, i ∈ e.val.path
      · obtain ⟨alignment, history⟩ := cancelWith_preserves_alignment a w s aligned e requester acknowledgers
          valid.1 valid.2.1 valid.2.2
        cases outcome : (cancelWith w e.val requester acknowledgers).2 with
        | false => exact ⟨_, _, alignment, history⟩
        | true =>
            have closed := true_cancel_implies_certificate a w s aligned e requester acknowledgers
              valid.1 valid.2.1 valid.2.2 outcome
            exact ⟨_, _, alignment, trace_append history
              (Trace.cons (Step.close _ e closed) (Trace.nil _))⟩
      · refine ⟨s, [], ?_, Trace.nil s⟩
        rw [cancelWith_invalid_identity w e.val requester acknowledgers valid]
        exact aligned

/-- False returns are not treated as absence of partial work or of a previously
accumulated certificate. True returns additionally justify a close event. -/
theorem runtime_cancel_trace_refines_history {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)}
    {events : List (RuntimeWithCancellationEvent n)} (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (trace : RuntimeWithCancellationTrace a w events v) :
    ∃ next primitiveEvents, Aligned a v next ∧ Trace a.config s primitiveEvents next := by
  induction trace generalizing s with
  | nil => exact ⟨s, [], aligned, Trace.nil s⟩
  | cons step _ ih =>
      obtain ⟨middle, first, alignment, history⟩ := runtime_cancel_step_refines_history a aligned reachable step
      obtain ⟨next, rest, last, tail⟩ := ih alignment (reachable_after reachable history)
      exact ⟨next, first ++ rest, last, trace_append history tail⟩

/-- A true actual cancelWith reply blocks the exact full envelope after every
finite continuation of the enlarged actual-operation class. -/
theorem true_runtime_cancel_blocks_all_continuations {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n) (owner : String) (acks : List Nat)
    (closed : (cancelWith w e.val owner acks).2 = true)
    {later : ComposedExecution.World} {events : List (RuntimeWithCancellationEvent n)}
    (continuation : RuntimeWithCancellationTrace a (cancelWith w e.val owner acks).1 events later)
    (requester : String) (badOpen : Bool) : (attempt later e.val requester badOpen).2 ≠ true := by
  obtain ⟨valid, nodup, selected⟩ := true_cancel_outer_guards w e.val owner acks closed
  obtain ⟨middleAligned, cancellationHistory⟩ :=
    cancelWith_preserves_alignment a w s aligned e owner acks valid nodup selected
  have certificate := true_cancel_implies_certificate a w s aligned e owner acks valid nodup selected closed
  have middleReachable := reachable_after reachable cancellationHistory
  obtain ⟨next, _, lastAligned, history⟩ :=
    runtime_cancel_trace_refines_history a middleAligned middleReachable continuation
  have veto := no_landing_after_cancellation middleReachable history later.now e requester certificate
  intro applied
  exact veto (successful_attempt_lands a later next lastAligned (reachable_after middleReachable history)
    e requester badOpen applied)

theorem reached_runtime_cancel_current_admission {base n} (a : Authority base n)
    {w v : ComposedExecution.World} {s : State (interface base n)}
    {events : List (RuntimeWithCancellationEvent n)} (aligned : Aligned a w s)
    (reachable : Reachable a.config s) (trace : RuntimeWithCancellationTrace a w events v)
    (e : BoundedEnvelope n) (requester : String) (badOpen : Bool)
    (applied : (attempt v e.val requester badOpen).2 = true) :
    e.val.action.epoch = v.effectivePolicy.epoch ∧
      localStep v.plant v.effectivePolicy v.now e.val.action = some e.val.successor := by
  obtain ⟨next, _, last, history⟩ := runtime_cancel_trace_refines_history a aligned reachable trace
  exact successful_attempt_current_policy a v next last (reachable_after reachable history)
    e requester badOpen applied

/-- Clock advance is still outside this operation language; adding cancellation
does not silently introduce real-time progress or refresh actor observations. -/
theorem runtime_cancel_step_clock {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {event : RuntimeWithCancellationEvent n}
    (step : RuntimeWithCancellationStep a w event v) : v.now = w.now := by
  cases step with
  | ordinary original =>
      cases original <;>
        simp [ComposedExecution.prepare, ComposedExecution.attempt,
          ComposedExecution.certifyTransition, ComposedExecution.deliver] <;>
        split_ifs <;> rfl
  | cancel =>
      simp [ComposedExecution.cancelWith]
      split_ifs <;> rfl

theorem runtime_cancel_trace_clock {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {events : List (RuntimeWithCancellationEvent n)}
    (history : RuntimeWithCancellationTrace a w events v) : v.now = w.now := by
  induction history with
  | nil => rfl
  | cons step _ ih => exact ih.trans (runtime_cancel_step_clock step)

#print axioms runtime_cancel_step_refines_history
#print axioms runtime_cancel_trace_refines_history
#print axioms true_runtime_cancel_blocks_all_continuations
#print axioms reached_runtime_cancel_current_admission
#print axioms runtime_cancel_trace_clock
end
end OperationalJoin.Offset
