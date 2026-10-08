import RuntimeCancellationTrace
import BatchSource

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

theorem runtime_trace_append {base n} {authority : Authority base n}
    {w v u : ComposedExecution.World} {xs ys : List (RuntimeWithCancellationEvent n)}
    (first : RuntimeWithCancellationTrace authority w xs v)
    (second : RuntimeWithCancellationTrace authority v ys u) :
    RuntimeWithCancellationTrace authority w (xs ++ ys) u := by
  induction first with
  | nil => exact second
  | cons step _ ih => exact .cons step (ih second)

/-- Every source branch emits exactly its actual service calls. In particular,
proposal rejection is an empty runtime trace, irrespective of the closed log bit. -/
theorem batchBody_runtime_trace {base n} (authority : Authority base n)
    (actor : Actor) (action : Action) (acc : ComposedExecution.World × List AttemptTrace)
    (path : List Nat) (bounded : path.Nodup ∧ ∀ i ∈ path, i < n) :
    ∃ events, RuntimeWithCancellationTrace authority acc.1 events
      (batchBody actor action acc path).1 := by
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none =>
      refine ⟨[], ?_⟩
      simpa only [batchBody, proposal] using RuntimeWithCancellationTrace.nil (a := authority) acc.1
  | some raw =>
      have fields := proposal_fields _ _ _ raw proposal
      let e : BoundedEnvelope n := ⟨raw, by simpa only [fields.2.1] using bounded⟩
      let prepared := ComposedExecution.prepare acc.1 raw actor.identity true
      cases ready : prepared.2 with
      | false =>
          change (ComposedExecution.prepare acc.1 raw actor.identity true).2 = false at ready
          refine ⟨[.ordinary (.prepare e actor.identity true), .cancel e actor.identity raw.path], ?_⟩
          have history : RuntimeWithCancellationTrace authority acc.1
              [.ordinary (.prepare e actor.identity true), .cancel e actor.identity raw.path]
              (cancelWith prepared.1 raw actor.identity raw.path).1 :=
            .cons (.ordinary (.prepare acc.1 e actor.identity true))
              (.cons (.cancel prepared.1 e actor.identity raw.path) (.nil _))
          simpa only [batchBody, proposal,
            ready, Bool.false_eq_true, if_false] using history
      | true =>
          change (ComposedExecution.prepare acc.1 raw actor.identity true).2 = true at ready
          refine ⟨[.ordinary (.prepare e actor.identity true), .ordinary (.attempt e actor.identity false),
            .cancel e actor.identity raw.path], ?_⟩
          have history : RuntimeWithCancellationTrace authority acc.1
              [.ordinary (.prepare e actor.identity true), .ordinary (.attempt e actor.identity false),
                .cancel e actor.identity raw.path]
              (cancelWith (attempt prepared.1 raw actor.identity false).1 raw actor.identity raw.path).1 :=
            .cons (.ordinary (.prepare acc.1 e actor.identity true))
              (.cons (.ordinary (.attempt prepared.1 e actor.identity false))
                (.cons (.cancel (attempt prepared.1 raw actor.identity false).1 e actor.identity raw.path) (.nil _)))
          simpa only [batchBody, proposal,
            ready, if_true] using history

theorem fold_runtime_trace {base n} (authority : Authority base n)
    (actor : Actor) (action : Action) (paths : List (List Nat))
    (bounded : ∀ path ∈ paths, path.Nodup ∧ ∀ i ∈ path, i < n)
    (acc : ComposedExecution.World × List AttemptTrace) :
    ∃ events, RuntimeWithCancellationTrace authority acc.1 events
      (paths.foldl (batchBody actor action) acc).1 := by
  induction paths generalizing acc with
  | nil => exact ⟨[], .nil _⟩
  | cons path rest ih =>
      obtain ⟨first, headTrace⟩ := batchBody_runtime_trace authority actor action acc path
        (bounded path (by simp))
      obtain ⟨tail, tailTrace⟩ := ih (by intro p hp; exact bounded p (by simp [hp]))
        (batchBody actor action acc path)
      exact ⟨first ++ tail, runtime_trace_append headTrace tailTrace⟩

/-- The actual fixed four-path controller, with arbitrary actor state. No
alignment, observer honesty, successful proposal, or fault-discovery premise is
needed to extract its finite list of genuine service calls. -/
theorem runBatch_runtime_trace {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    ∃ events, RuntimeWithCancellationTrace authority w events (runBatch w actor action).1 := by
  rw [runBatch_eq_fold]
  exact fold_runtime_trace authority actor action fourPaths fourPaths_bounded (w, [])

theorem runBatch_clock {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    (runBatch w actor action).1.now = w.now := by
  obtain ⟨events, trace⟩ := runBatch_runtime_trace authority w actor action
  exact runtime_cancel_trace_clock trace

#print axioms runBatch_runtime_trace
#print axioms runBatch_paths
#print axioms runBatch_nonces
#print axioms runBatch_length
#print axioms runBatch_clock
end
end OperationalJoin.Offset.Batch
