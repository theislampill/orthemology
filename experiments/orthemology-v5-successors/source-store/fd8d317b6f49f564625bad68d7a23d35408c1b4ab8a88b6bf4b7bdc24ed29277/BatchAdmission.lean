import BatchSafety
import BatchFrames

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

theorem proposal_step (actor : Actor) (action : Action) (path : List Nat)
    (e : ComposedExecution.Envelope) (proposal : propose actor action path = some e) :
    localStep actor.observedPlant actor.policy actor.observedTime action = some e.successor := by
  unfold propose at proposal
  cases step : localStep actor.observedPlant actor.policy actor.observedTime action with
  | none => simp [step] at proposal
  | some successor =>
      simp only [step, Option.map_some, Option.some.injEq] at proposal
      cases proposal
      rfl

/-- An actual successful proposed trial is authorized under the full policy at
its source-world boundary. This is derived from aligned reachable history,
not assumed as a progress premise. -/
theorem serviceTrial_current_admission {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (s : State (interface base 4))
    (aligned : Aligned authority w s) (reachable : Reachable authority.config s)
    (e : BoundedEnvelope 4) (requester : String)
    (landed : (serviceTrial w e.val requester).2.landed = true) :
    e.val.action.epoch = w.effectivePolicy.epoch ∧
      localStep w.plant w.effectivePolicy w.now e.val.action = some e.val.successor := by
  cases prepared : (ComposedExecution.prepare w e.val requester true).2 with
  | false => simp only [serviceTrial, prepared, Bool.false_eq_true, if_false] at landed
  | true =>
      have applied : (attempt (ComposedExecution.prepare w e.val requester true).1 e.val requester false).2 = true := by
        simpa only [serviceTrial, prepared, if_true] using landed
      have prehistory : RuntimeWithCancellationTrace authority w
          [.ordinary (.prepare e requester true)] (ComposedExecution.prepare w e.val requester true).1 :=
        .cons (.ordinary (.prepare w e requester true)) (.nil _)
      have current := reached_runtime_cancel_current_admission authority aligned reachable prehistory e requester false applied
      have frame := prepare_static w e.val requester true
      simpa only [prepare_plant, frame.2.2.2.1, frame.2.2.2.2.1] using current

/-- Safety reading of a successful actual batch: the single aggregate change
has an actual source-level admission from the original plant, policy and time.
This does not assert that success will occur. -/
theorem fold_landing_admitted {base} (authority : Authority base 4)
    (actor : Actor) (action : Action) (paths : List (List Nat))
    (bounded : ∀ path ∈ paths, path.Nodup ∧ ∀ i ∈ path, i < 4)
    (acc : ComposedExecution.World × List AttemptTrace) (s : State (interface base 4))
    (aligned : Aligned authority acc.1 s) (reachable : Reachable authority.config s)
    (noEarlier : landedCount acc.2 = 0)
    (positive : 0 < landedCount (paths.foldl (batchBody actor action) acc).2) :
    ∃ successor, localStep acc.1.plant acc.1.effectivePolicy acc.1.now action = some successor ∧
      (paths.foldl (batchBody actor action) acc).1.plant = successor := by
  induction paths generalizing acc s with
  | nil => simp only [List.foldl_nil, noEarlier] at positive; omega
  | cons path rest ih =>
      have tailBounded : ∀ selected ∈ rest, selected.Nodup ∧ ∀ i ∈ selected, i < 4 := by
        intro selected member
        exact bounded selected (by simp [member])
      obtain ⟨headEvents, headTrace⟩ := batchBody_runtime_trace authority actor action acc path
        (bounded path (by simp))
      obtain ⟨middle, primitive, middleAligned, primitiveHistory⟩ :=
        runtime_cancel_trace_refines_history authority aligned reachable headTrace
      have middleReachable := reachable_after reachable primitiveHistory
      cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
      | none =>
          have unchanged : (batchBody actor action acc path).1 = acc.1 := by simp [batchBody, proposal]
          have noHead : landedCount (batchBody actor action acc path).2 = 0 := by
            simp only [batchBody, proposal, landedCount_append, Bool.false_eq_true, if_false, Nat.add_zero, noEarlier]
          obtain ⟨successor, admitted, finalPlant⟩ := ih tailBounded _ middle middleAligned middleReachable noHead positive
          exact ⟨successor, by simpa only [unchanged] using admitted, finalPlant⟩
      | some raw =>
          have fields := proposal_fields _ _ _ raw proposal
          let e : BoundedEnvelope 4 := ⟨raw, by simpa only [fields.2.1] using bounded path (by simp)⟩
          have bodyEq := batchBody_of_proposal actor action acc path raw proposal
          cases landed : (serviceTrial acc.1 raw actor.identity).2.landed with
          | false =>
              have unchanged : (batchBody actor action acc path).1.plant = acc.1.plant := by
                rw [bodyEq, serviceTrial_plant, landed]
                rfl
              have noHead : landedCount (batchBody actor action acc path).2 = 0 := by
                rw [bodyEq, landedCount_append, landed]
                simpa using noEarlier
              obtain ⟨successor, admitted, finalPlant⟩ := ih tailBounded _ middle middleAligned middleReachable noHead positive
              have frame := batchBody_static actor action acc path
              exact ⟨successor, by simpa only [unchanged, frame.2.2.2.1, frame.2.2.2.2.1] using admitted, finalPlant⟩
          | true =>
              have current := serviceTrial_current_admission authority acc.1 s aligned reachable e actor.identity landed
              have stored : localStep actor.observedPlant actor.policy actor.observedTime action = some raw.successor :=
                proposal_step { actor with nonce := actor.nonce + acc.2.length } action path raw proposal
              have finalPlant := fold_positive_plant actor action raw.successor stored rest
                (batchBody actor action acc path)
                (by intro _; rw [bodyEq, serviceTrial_plant, landed]; rfl) positive
              exact ⟨raw.successor, by simpa only [e, fields.1] using current.2, finalPlant⟩

theorem runBatch_landing_admitted {base} (authority : Authority base 4)
    (w : ComposedExecution.World) (s : State (interface base 4))
    (aligned : Aligned authority w s) (reachable : Reachable authority.config s)
    (actor : Actor) (action : Action) (positive : 0 < landedCount (runBatch w actor action).2) :
    action.epoch = w.effectivePolicy.epoch ∧
      ∃ successor, localStep w.plant w.effectivePolicy w.now action = some successor ∧
        (runBatch w actor action).1.plant = successor := by
  rw [runBatch_eq_fold] at positive ⊢
  obtain ⟨successor, admitted, finalPlant⟩ := fold_landing_admitted authority actor action fourPaths
    fourPaths_bounded (w, []) s aligned reachable rfl positive
  exact ⟨local_action_epoch w.plant w.effectivePolicy w.now action successor admitted,
    successor, admitted, finalPlant⟩

#print axioms serviceTrial_current_admission
#print axioms runBatch_landing_admitted
end
end OperationalJoin.Offset.Batch
