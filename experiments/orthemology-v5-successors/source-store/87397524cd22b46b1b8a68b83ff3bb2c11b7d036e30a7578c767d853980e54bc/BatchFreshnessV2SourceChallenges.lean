import BatchSourceChallenges
import BatchAvailabilityChallenges
import BatchSafety

namespace BatchFreshnessV2SourceReview
noncomputable section
open Classical
open ComposedExecution OperationalJoin OperationalJoin.Offset
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- Even exact-four freshness is not necessary for progress: the cancelled
first path already contains a withholding faulty gate, while the last is fresh. -/
theorem cancelled_faulty_trial_does_not_block_the_intact_trial :
    let prior := (cancelWith (BatchSourceReview.w [0]) BatchSourceReview.first "A" [1,2]).1
    BatchSourceReview.first ∈ (prior.roots 1).cancelled ∧
    (runBatch prior BatchSourceReview.actor BatchSourceReview.a).2.map AttemptTrace.prepared =
      [false,true,true,true] ∧
    (runBatch prior BatchSourceReview.actor BatchSourceReview.a).2.map AttemptTrace.landed =
      [false,false,false,true] ∧
    (runBatch prior BatchSourceReview.actor BatchSourceReview.a).1.plant =
      BatchSourceReview.successor := by decide

def repairAction : Action := .repair (_root_.repairCommand NativeFixture.sourceBytes)
def premature : World :=
  (runBatch NativeFixture.certified NativeFixture.repairActor repairAction).1
def deliveredAfterFailure : World := ComposedExecution.deliver premature NativeFixture.certificate
def lastOld : Typed.BoundedEnvelope 4 :=
  ⟨⟨repairAction, NativeFixture.repaired, 5, [1,2,3]⟩, by decide⟩

theorem false_preparation_still_consumes_exact_envelopes :
    (runBatch NativeFixture.certified NativeFixture.repairActor repairAction).2.map
      AttemptTrace.prepared = [false,false,false,false] ∧
    (runBatch NativeFixture.certified NativeFixture.repairActor repairAction).2.map
      AttemptTrace.closed = [true,true,true,true] ∧
    premature.plant = NativeFixture.installed ∧
    lastOld.val ∈ (premature.roots 1).cancelled ∧
    lastOld.val ∈ (premature.roots 2).cancelled ∧
    lastOld.val ∈ (premature.roots 3).cancelled := by decide

/-- Policy delivery restores live local admission but does not erase cleanup.
The fixed action is still version-current; only its old exact envelopes fail. -/
theorem delivery_does_not_revive_cancelled_trials_but_fresh_batch_lands :
    localStep deliveredAfterFailure.plant deliveredAfterFailure.effectivePolicy
      deliveredAfterFailure.now repairAction = some NativeFixture.repaired ∧
    (attempt (ComposedExecution.prepare deliveredAfterFailure lastOld.val "A" true).1
      lastOld.val "A" true).2 = false ∧
    (runBatch deliveredAfterFailure { NativeFixture.repairActor with nonce := 5 } repairAction).2.map
      AttemptTrace.landed = [false,false,false,true] ∧
    (runBatch deliveredAfterFailure { NativeFixture.repairActor with nonce := 5 } repairAction).1.plant =
      NativeFixture.repaired := by decide

/-- Both the premature aggregate and the later delivery are genuine operations
from the independently established reachable pre-delivery native snapshot. -/
theorem restored_policy_countercontrol_is_genuinely_reachable :
    ∃ s, Aligned NativeFixture.authority deliveredAfterFailure s ∧
      Reachable NativeFixture.authority.config s := by
  obtain ⟨before, aligned, reachable⟩ :=
    BatchAvailabilityReview.certified_without_delivery_is_aligned_reachable
  obtain ⟨middle, first, middleAligned, history⟩ := Batch.runBatch_refines_history
    NativeFixture.authority NativeFixture.certified before aligned reachable
    NativeFixture.repairActor repairAction
  have delivery : RuntimeWithCancellationTrace NativeFixture.authority premature
      [.ordinary (.deliver NativeFixture.certificate)] deliveredAfterFailure :=
    .cons (.ordinary (.deliver premature NativeFixture.certificate)) (.nil _)
  obtain ⟨next, events, last, tail⟩ := runtime_cancel_trace_refines_history
    NativeFixture.authority middleAligned (reachable_after reachable history) delivery
  exact ⟨next, last, reachable_after (reachable_after reachable history) tail⟩

#print axioms cancelled_faulty_trial_does_not_block_the_intact_trial
#print axioms false_preparation_still_consumes_exact_envelopes
#print axioms delivery_does_not_revive_cancelled_trials_but_fresh_batch_lands
#print axioms restored_policy_countercontrol_is_genuinely_reachable
end
end BatchFreshnessV2SourceReview
