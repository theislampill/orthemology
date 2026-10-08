import BatchExactProgress
import BatchAdmission
import BatchCleanup
import BatchNative
import BatchFreshnessV2SourceChallenges

namespace BatchV2ContractReview
noncomputable section
open Classical
open ComposedExecution OperationalJoin OperationalJoin.Offset
open Batch
set_option maxRecDepth 60000
set_option maxHeartbeats 8000000

def highEnvelope : Typed.BoundedEnvelope 4 :=
  ⟨{ NativeFixture.installEnvelope.val with nonce := 99 }, by decide⟩
def reachedHigh : World :=
  (cancelWith NativeFixture.start highEnvelope.val "A" [1,2,3]).1

/-- The strictness witness can be reached by an actual allowed cancellation;
it need not be an externally supplied arbitrary tombstone state. -/
theorem high_nonce_counterstate_is_genuinely_reachable :
    ∃ s, Aligned NativeFixture.authority reachedHigh s ∧
      Reachable NativeFixture.authority.config s := by
  obtain ⟨aligned, history⟩ := cancelWith_preserves_alignment NativeFixture.authority
    NativeFixture.start (Initial NativeFixture.authority.config NativeFixture.before)
    NativeFixture.start_aligned highEnvelope "A" [1,2,3]
    (by decide) (by decide) (by decide)
  exact ⟨_, aligned, reachable_after NativeFixture.start_reachable history⟩

theorem reached_high_nonce_still_has_exact_trial_readiness :
    ExactReady reachedHigh (.install _root_.installCommand) NativeFixture.installed
      NativeFixture.installActor.identity NativeFixture.installActor.nonce fourPaths := by
  refine ⟨rfl, NativeFixture.install_local, ?_, ?_⟩
  · intro i bound good
    have finite : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by
      change i < 4 at bound
      omega
    rcases finite with rfl | rfl | rfl | rfl
    · have impossible : true = false := good
      cases impossible
    · decide
    · decide
    · decide
  · intro i bound good e future
    have finite : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by
      change i < 4 at bound
      omega
    rw [exact_four_predicted_envelopes] at future
    simp only [List.mem_cons, List.not_mem_nil, or_false] at future
    rcases finite with rfl | rfl | rfl | rfl
    all_goals rcases future with rfl | rfl | rfl | rfl
    all_goals decide

theorem reached_high_nonce_refutes_global_high_water_necessity :
    ¬FreshAbove reachedHigh NativeFixture.installActor.nonce ∧
    landedCount (runBatch reachedHigh NativeFixture.installActor
      (.install _root_.installCommand)).2 = 1 ∧
    (runBatch reachedHigh NativeFixture.installActor
      (.install _root_.installCommand)).1.plant = NativeFixture.installed := by
  refine ⟨?_, ?_⟩
  · intro fresh
    have upper := fresh 1 (by decide) (by decide) highEnvelope.val (by decide)
    change 99 ≤ 0 at upper
    omega
  · exact runBatch_exact_fresh_completion reachedHigh NativeFixture.installActor
      (.install _root_.installCommand) NativeFixture.installed NativeFixture.install_local
      rfl rfl (by decide) reached_high_nonce_still_has_exact_trial_readiness

def cancelledFaultyFirst : World :=
  (cancelWith (BatchSourceReview.w [0]) BatchSourceReview.first "A" [1,2]).1

/-- Even the sharpened predicate is only sufficient, as demonstrated by a
cancelled prospective trial that could not execute through its faulty gate. -/
theorem exact_four_freshness_is_not_necessary_for_progress :
    ¬FreshTrials cancelledFaultyFirst
      (trialEnvelopes BatchSourceReview.a BatchSourceReview.successor
        BatchSourceReview.actor.nonce fourPaths) ∧
    landedCount (runBatch cancelledFaultyFirst BatchSourceReview.actor BatchSourceReview.a).2 = 1 := by
  constructor
  · intro fresh
    have absence := fresh 1 (by decide) (by decide) BatchSourceReview.first (by decide)
    exact absence (by decide)
  · decide

/-- The new aggregate admission endpoint concerns the original world, and
accepts arbitrary actors without adding a live-admission progress premise. -/
theorem aggregate_safety_has_exact_source_world_endpoint {base}
    (authority : Authority base 4) (world : World) (s : State (interface base 4))
    (aligned : Aligned authority world s) (reachable : Reachable authority.config s)
    (who : Actor) (action : Action)
    (positive : 0 < landedCount (runBatch world who action).2) :
    action.epoch = world.effectivePolicy.epoch ∧
      ∃ next, localStep world.plant world.effectivePolicy world.now action = some next ∧
        (runBatch world who action).1.plant = next :=
  runBatch_landing_admitted authority world s aligned reachable who action positive

/-- The current-call cancellation result is distinct from fault-budget soundness;
the source produces this Boolean even when all four execution roots are bad. -/
theorem owner_cleanup_boolean_has_no_fault_count_requirement :
    (serviceTrial (BatchSourceReview.w [0,1,2,3]) BatchSourceReview.first "A").2.closed = true :=
  serviceTrial_closes _ _ _ rfl (by decide) rfl rfl

#print axioms high_nonce_counterstate_is_genuinely_reachable
#print axioms reached_high_nonce_still_has_exact_trial_readiness
#print axioms reached_high_nonce_refutes_global_high_water_necessity
#print axioms exact_four_freshness_is_not_necessary_for_progress
#print axioms aggregate_safety_has_exact_source_world_endpoint
#print axioms owner_cleanup_boolean_has_no_fault_count_requirement
end
end BatchV2ContractReview
