import BatchNative
import BatchExactProgress

namespace OperationalJoin.Offset.Batch.RetryControls
noncomputable section
open Classical
open ComposedExecution
open NativeFixture
open Native
set_option maxRecDepth 60000
set_option maxHeartbeats 16000000

def repairAction : Action := .repair (_root_.repairCommand sourceBytes)

/-- Actor receives the authentic certificate before the honest roots do. -/
def beforeDeliveryBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch certifiedBatch receivedActor repairAction

def deliveredAfterFailure : ComposedExecution.World :=
  ComposedExecution.deliver beforeDeliveryBatch.1 batchCertificate

/-- The exact same actor is passed again. runBatch returns no updated Actor. -/
def repeatedBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch deliveredAfterFailure receivedActor repairAction

def freshRetryActor : Actor := { receivedActor with nonce := 8 }
def freshRetryBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch deliveredAfterFailure freshRetryActor repairAction

theorem before_delivery_zero_landing : landedCount beforeDeliveryBatch.2 = 0 := by decide

theorem before_delivery_preserves_installed : beforeDeliveryBatch.1.plant = installed := by
  have unchanged := runBatch_zero_landings_unchanged certifiedBatch receivedActor repairAction before_delivery_zero_landing
  change beforeDeliveryBatch.1.plant = certifiedBatch.plant at unchanged
  calc
    beforeDeliveryBatch.1.plant = certifiedBatch.plant := unchanged
    _ = installedBatch.1.plant := by rfl
    _ = installed := native_install_batch_once.2

theorem after_delivery_preserves_installed : deliveredAfterFailure.plant = installed := by
  unfold deliveredAfterFailure ComposedExecution.deliver
  split <;> exact before_delivery_preserves_installed

def fourthOldRepair : ComposedExecution.Envelope :=
  ⟨repairAction, repaired, 8, [1,2,3]⟩

theorem failed_batch_records_durable_cancellation :
    fourthOldRepair ∈ (beforeDeliveryBatch.1.roots 1).cancelled := by decide

theorem delivery_keeps_old_cancellation :
    fourthOldRepair ∈ (deliveredAfterFailure.roots 1).cancelled := by decide

theorem same_actor_retry_still_zero : landedCount repeatedBatch.2 = 0 := by decide

theorem same_actor_retry_unchanged : repeatedBatch.1.plant = installed := by
  have unchanged := runBatch_zero_landings_unchanged deliveredAfterFailure receivedActor repairAction same_actor_retry_still_zero
  exact unchanged.trans after_delivery_preserves_installed

theorem fresh_retry_ready :
    ReadyFor deliveredAfterFailure repairAction repaired freshRetryActor.identity freshRetryActor.nonce := by
  refine ⟨rfl, ?_, ?_, ?_⟩
  · rw [after_delivery_preserves_installed]
    exact repair_local
  · intro i bound good
    have bound4 : i < 4 := bound
    have finite : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by omega
    rcases finite with rfl | rfl | rfl | rfl
    · have impossible : true = false := good
      cases impossible
    · decide
    · decide
    · decide
  · have installFresh : FreshAbove installedBatch.1 4 := by
      have result := runBatch_fresh NativeFixture.start installActor (.install _root_.installCommand)
        native_install_ready.2.2.2
      simpa only [installActor, Nat.zero_add] using result
    have certifiedFresh : FreshAbove certifiedBatch 4 :=
      certifyTransition_fresh installedBatch.1 [0,1,2] (source 1) 4 installFresh
    have failedFresh : FreshAbove beforeDeliveryBatch.1 8 := by
      exact runBatch_fresh certifiedBatch receivedActor repairAction certifiedFresh
    exact deliver_fresh beforeDeliveryBatch.1 batchCertificate 8 failedFresh

theorem fresh_retry_completes_once :
    landedCount freshRetryBatch.2 = 1 ∧ freshRetryBatch.1.plant = repaired := by
  apply runBatch_stable_completion deliveredAfterFailure freshRetryActor repairAction repaired
    native_repair_proposal rfl rfl (by decide) fresh_retry_ready

/-- A different authorized complete command can also avoid old cancellation
without increasing the actor's nonce. This is a mathematical source control,
not a command-renewal service implemented by runBatch. -/
def renewedRepairAction : Action := .repair { _root_.repairCommand sourceBytes with leaseEnd := 91 }
def sameNonceNewCommandBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch deliveredAfterFailure receivedActor renewedRepairAction

theorem renewed_repair_local :
    localStep installed (source 1) 2 renewedRepairAction = some repaired := by decide

theorem renewed_repair_exact_ready :
    ExactReady deliveredAfterFailure renewedRepairAction repaired receivedActor.identity receivedActor.nonce fourPaths := by
  refine ⟨rfl, ?_, ?_, ?_⟩
  · rw [after_delivery_preserves_installed]
    exact renewed_repair_local
  · exact fresh_retry_ready.2.2.1
  · intro i bound good e future
    have bound4 : i < 4 := bound
    have finite : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by omega
    rw [exact_four_predicted_envelopes] at future
    simp only [List.mem_cons, List.not_mem_nil, or_false] at future
    rcases future with rfl | rfl | rfl | rfl
    all_goals
      rcases finite with rfl | rfl | rfl | rfl
      · have impossible : true = false := good
        cases impossible
      · decide
      · decide
      · decide

theorem same_nonce_changed_command_completes :
    landedCount sameNonceNewCommandBatch.2 = 1 ∧ sameNonceNewCommandBatch.1.plant = repaired := by
  exact runBatch_exact_fresh_completion deliveredAfterFailure receivedActor renewedRepairAction repaired
    renewed_repair_local rfl rfl (by decide) renewed_repair_exact_ready

theorem reused_nonce_violates_high_water : ¬ FreshAbove deliveredAfterFailure receivedActor.nonce := by
  intro fresh
  have old := fresh 1 (by decide) (by decide) fourthOldRepair delivery_keeps_old_cancellation
  change 8 ≤ 4 at old
  omega

/-- Delivery alone does not repair replay of the same complete envelopes;
explicit new envelopes suffice, by a higher nonce or a different admitted command. -/
theorem retry_boundary :
    landedCount beforeDeliveryBatch.2 = 0 ∧
    landedCount repeatedBatch.2 = 0 ∧
    landedCount freshRetryBatch.2 = 1 ∧
    landedCount sameNonceNewCommandBatch.2 = 1 ∧
    ¬ FreshAbove deliveredAfterFailure receivedActor.nonce :=
  ⟨before_delivery_zero_landing, same_actor_retry_still_zero,
    fresh_retry_completes_once.1, same_nonce_changed_command_completes.1, reused_nonce_violates_high_water⟩

#print axioms before_delivery_zero_landing
#print axioms failed_batch_records_durable_cancellation
#print axioms same_actor_retry_still_zero
#print axioms fresh_retry_completes_once
#print axioms same_nonce_changed_command_completes
#print axioms retry_boundary
end
end OperationalJoin.Offset.Batch.RetryControls
