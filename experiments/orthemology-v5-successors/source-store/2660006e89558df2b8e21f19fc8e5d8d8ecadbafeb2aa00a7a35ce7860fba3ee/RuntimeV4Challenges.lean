import RuntimeControls

namespace RuntimeV4Review
noncomputable section
open Classical
open OperationalJoin
open OperationalJoin.Offset
open Typed (BoundedEnvelope)
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- The bounded runtime class has no clock-update event. This invariant makes
that exact scope visible rather than treating arbitrary annotations as runtime time. -/
theorem runtime_step_clock {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {e : RuntimeEvent n}
    (step : RuntimeStep a w e v) : v.now = w.now := by
  cases step with
  | prepare => unfold ComposedExecution.prepare; split <;> rfl
  | attempt => unfold ComposedExecution.attempt; split <;> rfl
  | certify => unfold ComposedExecution.certifyTransition; split <;> rfl
  | deliver => unfold ComposedExecution.deliver; split <;> rfl

theorem runtime_trace_clock {base n} {a : Authority base n}
    {w v : ComposedExecution.World} {es : List (RuntimeEvent n)}
    (history : RuntimeTrace a w es v) : v.now = w.now := by
  induction history with
  | nil => rfl
  | cons step _ ih => exact ih.trans (runtime_step_clock step)

/-- Offsetting can collapse low and boundary raw epochs arithmetically, but
source admission still distinguishes them and rejects the retained low command. -/
theorem offset_collision_does_not_admit_low_raw :
    (interface 2 4).commandEpoch RuntimeControls.oldRawEnvelope =
      (interface 2 4).commandEpoch NativeFixture.installEnvelope ∧
    RuntimeControls.oldRawEnvelope.val.action.epoch ≠
      NativeFixture.installEnvelope.val.action.epoch ∧
    (ComposedExecution.attempt
      (ComposedExecution.prepare NativeFixture.start RuntimeControls.oldRawEnvelope.val "A" true).1
      RuntimeControls.oldRawEnvelope.val "A" true).2 = false := by
  exact ⟨rfl, by decide, RuntimeControls.prebase_raw_command_is_rejected.2⟩

/-- A withheld landing leaves the entire partial-preparation World unchanged;
it does not roll back the honest commitments produced by the false prepare reply. -/
theorem withheld_attempt_retains_partial_preparation :
    (ComposedExecution.attempt RuntimeControls.partialPrepared
      RuntimeControls.partialEnvelope.val "A" false).1 = RuntimeControls.partialPrepared ∧
    RuntimeControls.partialEnvelope.val ∈ (RuntimeControls.partialPrepared.roots 1).commitments ∧
    RuntimeControls.partialEnvelope.val ∈ (RuntimeControls.partialPrepared.roots 2).commitments := by
  exact ⟨ComposedExecution.rejected_attempt_full_identity _ _ _ _
    RuntimeControls.shared_badOpen_has_exact_runtime_force.1,
    RuntimeControls.partial_prepare_is_not_identity.2.1,
    RuntimeControls.partial_prepare_is_not_identity.2.2.1⟩

/-- Goal preservation is also dischargeable for the offset interface from its
actual unchanged local source effect, without an additional preservation premise. -/
theorem offset_goals_persist {base n} {a : Authority base n}
    {s t : State (interface base n)} {es : List (Event (interface base n))}
    (reachable : Reachable a.config s) (goals : ComposedExecution.Goals s.plant)
    (history : Trace a.config s es t) : ComposedExecution.Goals t.plant := by
  apply trace_preserves ComposedExecution.Goals ?_ (reachable_consistent reachable)
    (Typed.reachable_safe reachable) goals history
  intro p time policy e requester admission old
  exact ComposedExecution.local_goals_persist p policy time e.val.action e.val.successor admission.2 old

/-- Full actual-policy alignment rules out substituting any unequal policy,
including an equal-numbered policy, while leaving the common state unchanged. -/
theorem effective_policy_cannot_be_replaced {base n} {a : Authority base n}
    {w : ComposedExecution.World} {s : State (interface base n)} (alignment : Aligned a w s)
    (replacement : ComposedExecution.Policy) (different : replacement ≠ w.effectivePolicy) :
    ¬Aligned a {w with effectivePolicy := replacement} s := by
  intro altered
  exact different (altered.effective_policy.trans alignment.effective_policy.symm)

/-- Malformed or unrecorded certificate delivery has an exact full-World
identity result; no partial policy update can be hidden by the simulation. -/
theorem unrecorded_delivery_full_identity (w : ComposedExecution.World)
    (cert : ComposedExecution.Certificate) (unrecorded : cert ∉ w.completed) :
    ComposedExecution.deliver w cert = w := by
  simp [ComposedExecution.deliver, unrecorded]

/-- Repeating a recorded delivery is idempotent at the entire runtime World,
including arbitrary bad-root state and unrelated fields. -/
theorem repeated_delivery_full_identity (w : ComposedExecution.World)
    (cert : ComposedExecution.Certificate) :
    ComposedExecution.deliver (ComposedExecution.deliver w cert) cert =
      ComposedExecution.deliver w cert := by
  by_cases recorded : cert ∈ w.completed
  · simp only [ComposedExecution.deliver, decide_eq_true recorded, if_true]
    congr 1
    funext i
    by_cases tainted : w.tainted i = true
    · simp [tainted]
    · have good : w.tainted i = false := Bool.eq_false_iff.mpr tainted
      by_cases newer : (w.roots i).policy.epoch < cert.policy.epoch
      · simp [good, newer]
      · simp [good, newer]
  · rw [unrecorded_delivery_full_identity w cert recorded]
    exact unrecorded_delivery_full_identity w cert recorded

#print axioms runtime_step_clock
#print axioms runtime_trace_clock
#print axioms offset_collision_does_not_admit_low_raw
#print axioms withheld_attempt_retains_partial_preparation
#print axioms offset_goals_persist
#print axioms effective_policy_cannot_be_replaced
#print axioms unrecorded_delivery_full_identity
#print axioms repeated_delivery_full_identity
end
end RuntimeV4Review
