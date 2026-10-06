import BatchSurvival
import BatchRetryControls

namespace OperationalJoin.Offset.Batch.SurvivalControls
noncomputable section
open Classical
open ComposedExecution
open NativeFixture
open Native
set_option maxRecDepth 60000
set_option maxHeartbeats 16000000

def installAction : Action := .install _root_.installCommand
def firstTrial : ComposedExecution.Envelope := ⟨installAction, installed, 1, [0,1,2]⟩
def fourthTrial : ComposedExecution.Envelope := ⟨installAction, installed, 4, [1,2,3]⟩
def firstCancelled : ComposedExecution.World := (cancelWith NativeFixture.start firstTrial "A" firstTrial.path).1
def fourthCancelled : ComposedExecution.World := (cancelWith NativeFixture.start fourthTrial "A" fourthTrial.path).1

theorem initial_admission_ready : AdmissionReady NativeFixture.start installAction installed installActor.identity :=
  ⟨native_install_ready.1, native_install_ready.2.1, native_install_ready.2.2.1⟩

theorem first_cancelled_ready : AdmissionReady firstCancelled installAction installed installActor.identity :=
  cancel_admission_ready NativeFixture.start installAction installed installActor.identity initial_admission_ready firstTrial

theorem fourth_cancelled_ready : AdmissionReady fourthCancelled installAction installed installActor.identity :=
  cancel_admission_ready NativeFixture.start installAction installed installActor.identity initial_admission_ready fourthTrial

theorem fourth_survives_first_cancellation : IntactUncancelled firstCancelled fourthTrial := by
  unfold IntactUncancelled
  decide

theorem first_cancellation_does_not_prevent_progress :
    landedCount (runBatch firstCancelled installActor installAction).2 = 1 ∧
      (runBatch firstCancelled installActor installAction).1.plant = installed := by
  apply (runBatch_survival_effect_iff firstCancelled installActor installAction installed
    install_local rfl rfl first_cancelled_ready).mpr
  refine ⟨fourthTrial, ?_, fourth_survives_first_cancellation⟩
  rw [exact_four_predicted_envelopes]
  simp [fourthTrial, installActor]

theorem first_cancellation_violates_all_four_freshness :
    ¬ ExactReady firstCancelled installAction installed installActor.identity installActor.nonce fourPaths := by
  intro ready
  have future : firstTrial ∈ trialEnvelopes installAction installed installActor.nonce fourPaths := by
    rw [exact_four_predicted_envelopes]
    simp [firstTrial, installActor]
  have veto := ready.2.2.2 1 (by decide) (by decide) firstTrial future
  exact veto (by decide)

/-- Only the fourth source path excludes bad root 0. Its exact old tombstone
therefore eliminates every surviving trial, although earlier faults can mimic
successful preparation/cancellation receipts. -/
theorem fourth_cancellation_leaves_no_survivor :
    ¬ HasSurvivingTrial fourthCancelled installAction installed installActor.nonce fourPaths := by
  rintro ⟨e, member, available⟩
  rw [exact_four_predicted_envelopes] at member
  simp only [List.mem_cons, List.not_mem_nil, or_false] at member
  rcases member with rfl | rfl | rfl | rfl
  · have impossible : true = false := (available 0 (by decide)).1
    cases impossible
  · have impossible : true = false := (available 0 (by decide)).1
    cases impossible
  · have impossible : true = false := (available 0 (by decide)).1
    cases impossible
  · exact (available 1 (by decide)).2 (by decide)

theorem fourth_cancellation_blocks_actual_batch :
    landedCount (runBatch fourthCancelled installActor installAction).2 = 0 ∧
      (runBatch fourthCancelled installActor installAction).1.plant = before := by
  have zero := (runBatch_zero_iff_no_surviving_trial fourthCancelled installActor installAction installed
    install_local rfl rfl fourth_cancelled_ready).mpr fourth_cancellation_leaves_no_survivor
  exact ⟨zero, runBatch_zero_landings_unchanged _ _ _ zero⟩

theorem delayed_retry_has_no_survivor :
    ¬ HasSurvivingTrial RetryControls.deliveredAfterFailure RetryControls.repairAction repaired
      receivedActor.nonce fourPaths := by
  have ready : AdmissionReady RetryControls.deliveredAfterFailure RetryControls.repairAction repaired receivedActor.identity :=
    ⟨RetryControls.fresh_retry_ready.1, RetryControls.fresh_retry_ready.2.1, RetryControls.fresh_retry_ready.2.2.1⟩
  exact (runBatch_zero_iff_no_surviving_trial RetryControls.deliveredAfterFailure receivedActor
    RetryControls.repairAction repaired native_repair_proposal rfl rfl ready).mp RetryControls.same_actor_retry_still_zero

theorem fresh_retry_has_survivor :
    HasSurvivingTrial RetryControls.deliveredAfterFailure RetryControls.repairAction repaired
      RetryControls.freshRetryActor.nonce fourPaths := by
  have ready : AdmissionReady RetryControls.deliveredAfterFailure RetryControls.repairAction repaired RetryControls.freshRetryActor.identity :=
    ⟨RetryControls.fresh_retry_ready.1, RetryControls.fresh_retry_ready.2.1, RetryControls.fresh_retry_ready.2.2.1⟩
  exact (runBatch_survival_iff RetryControls.deliveredAfterFailure RetryControls.freshRetryActor
    RetryControls.repairAction repaired native_repair_proposal rfl rfl ready).mp RetryControls.fresh_retry_completes_once.1

/-- Availability alone is insufficient before delivery: actor and effective
policy can be ready while honest roots still hold the prior full policy. -/
theorem before_delivery_has_surviving_trial :
    HasSurvivingTrial certifiedBatch RetryControls.repairAction repaired receivedActor.nonce fourPaths := by
  refine ⟨RetryControls.fourthOldRepair, ?_, ?_⟩
  · rw [exact_four_predicted_envelopes]
    rw [native_actor_receives_full_policy]
    simp [RetryControls.fourthOldRepair, installActor]
  · unfold IntactUncancelled
    decide

theorem before_delivery_not_synchronized_ready :
    ¬ AdmissionReady certifiedBatch RetryControls.repairAction repaired receivedActor.identity := by
  intro ready
  have policyEq := (ready.2.2 1 (by decide) (by decide)).1
  have epochEq := congrArg Policy.epoch policyEq
  change 2 = 3 at epochEq
  omega

theorem availability_without_policy_synchronization_can_stall :
    HasSurvivingTrial certifiedBatch RetryControls.repairAction repaired receivedActor.nonce fourPaths ∧
      landedCount RetryControls.beforeDeliveryBatch.2 = 0 ∧
      ¬ AdmissionReady certifiedBatch RetryControls.repairAction repaired receivedActor.identity :=
  ⟨before_delivery_has_surviving_trial, RetryControls.before_delivery_zero_landing,
    before_delivery_not_synchronized_ready⟩

/-- The unselected-root test concerns predicate coordinates in an arbitrary
raw initial World. It is not asserted to arise from a legal cancelWith call. -/
theorem unselected_memory_does_not_veto_first_trial :
    IntactUncancelled
      { initialWorld before (source 0) [] with roots := fun i => if i = 3 then
          { (initialWorld before (source 0) []).roots i with cancelled := [firstTrial] }
        else (initialWorld before (source 0) []).roots i }
      firstTrial := by
  apply (unselected_tombstone_irrelevant (initialWorld before (source 0) []) firstTrial 3 (by decide)).mpr
  unfold IntactUncancelled
  decide

#print axioms first_cancellation_does_not_prevent_progress
#print axioms first_cancellation_violates_all_four_freshness
#print axioms fourth_cancellation_blocks_actual_batch
#print axioms delayed_retry_has_no_survivor
#print axioms fresh_retry_has_survivor
#print axioms unselected_memory_does_not_veto_first_trial
#print axioms availability_without_policy_synchronization_can_stall
end
end OperationalJoin.Offset.Batch.SurvivalControls
