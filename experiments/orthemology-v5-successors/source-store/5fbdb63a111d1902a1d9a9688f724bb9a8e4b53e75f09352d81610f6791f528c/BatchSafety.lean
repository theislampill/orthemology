import BatchExtraction
import MonotoneReferenceTrace

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

/-- Full refinement of the actual aggregate batch. Actor observations and
identity are arbitrary. Failed proposals and partial service effects are kept
by the literal fold extraction, not assumed away by a success premise. -/
theorem runBatch_refines_history {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (s : State (interface base 4))
    (aligned : Aligned authority w s) (reachable : Reachable authority.config s)
    (actor : Actor) (action : Action) :
    ∃ next events, Aligned authority (runBatch w actor action).1 next ∧
      Trace authority.config s events next := by
  obtain ⟨runtimeEvents, runtimeHistory⟩ := runBatch_runtime_trace authority w actor action
  exact runtime_cancel_trace_refines_history authority aligned reachable runtimeHistory

/-- This consequence is about the actual aggregate output, and still checks
the full effective policy at the actual query time. -/
theorem after_runBatch_current_admission {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (s : State (interface base 4))
    (aligned : Aligned authority w s) (reachable : Reachable authority.config s)
    (actor : Actor) (action : Action) (e : BoundedEnvelope 4)
    (requester : String) (badOpen : Bool)
    (applied : (attempt (runBatch w actor action).1 e.val requester badOpen).2 = true) :
    e.val.action.epoch = (runBatch w actor action).1.effectivePolicy.epoch ∧
      localStep (runBatch w actor action).1.plant
        (runBatch w actor action).1.effectivePolicy (runBatch w actor action).1.now
        e.val.action = some e.val.successor := by
  obtain ⟨runtimeEvents, runtimeHistory⟩ := runBatch_runtime_trace authority w actor action
  exact reached_runtime_cancel_current_admission authority aligned reachable runtimeHistory
    e requester badOpen applied

/-- Every old genuine cancellation certificate survives arbitrary actor batches.
No interpretation of a batch log's synthetic closed bit is needed. -/
theorem true_cancel_blocks_after_runBatch {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (s : State (interface base 4))
    (aligned : Aligned authority w s) (reachable : Reachable authority.config s)
    (e : BoundedEnvelope 4) (owner : String) (acks : List Nat)
    (closed : (cancelWith w e.val owner acks).2 = true)
    (actor : Actor) (action : Action) (requester : String) (badOpen : Bool) :
    (attempt (runBatch (cancelWith w e.val owner acks).1 actor action).1
      e.val requester badOpen).2 ≠ true := by
  obtain ⟨events, history⟩ := runBatch_runtime_trace authority
    (cancelWith w e.val owner acks).1 actor action
  exact true_runtime_cancel_blocks_all_continuations authority w s aligned reachable
    e owner acks closed history requester badOpen

/-- Batches can occur after a monotone reference-clock history without changing
that reference annotation themselves. This does not add a clock to the service. -/
theorem monotone_prefix_then_batch_refines {base} (authority : Authority base 4)
    {w v : ComposedExecution.World} {s : State (interface base 4)}
    {events : List (MonotoneReferenceEvent 4)}
    (aligned : Aligned authority w s) (reachable : Reachable authority.config s)
    (prehistory : MonotoneReferenceTrace authority w events v) (actor : Actor) (action : Action) :
    ∃ next primitiveEvents, Aligned authority (runBatch v actor action).1 next ∧
      Trace authority.config s primitiveEvents next := by
  obtain ⟨middle, first, middleAligned, firstHistory⟩ :=
    monotone_reference_trace_refines_history authority aligned reachable prehistory
  obtain ⟨next, rest, lastAligned, tailHistory⟩ :=
    runBatch_refines_history authority v middle middleAligned
      (reachable_after reachable firstHistory) actor action
  exact ⟨next, first ++ rest, lastAligned, trace_append firstHistory tailHistory⟩

#print axioms runBatch_refines_history
#print axioms after_runBatch_current_admission
#print axioms true_cancel_blocks_after_runBatch
#print axioms monotone_prefix_then_batch_refines
end
end OperationalJoin.Offset.Batch
