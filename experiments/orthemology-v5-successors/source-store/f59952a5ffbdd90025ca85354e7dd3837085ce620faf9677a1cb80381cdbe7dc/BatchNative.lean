import BatchSafety
import BatchProgress
import BatchMemory
import BatchFrames
import BatchCleanup
import RuntimeFixture

namespace OperationalJoin.Offset.Batch.Native
noncomputable section
open Classical
open ComposedExecution
open NativeFixture
set_option maxRecDepth 60000
set_option maxHeartbeats 8000000

/-- Exact imported actor and full pinned 3013-byte plant, raw epoch 2. -/
def installedBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch NativeFixture.start installActor (.install _root_.installCommand)

/-- The same predicted-observation update used by the accepted source fixture.
It does not read the effect reply or acquire an observation oracle. -/
def predictedActor : Actor := { installActor with observedPlant := installed, nonce := 4 }

def batchCertificate : ComposedExecution.Certificate := ⟨2, source 1, [0,1,2]⟩
def certifiedBatch : ComposedExecution.World :=
  (certifyTransition installedBatch.1 [0,1,2] (source 1)).1
def deliveredBatch : ComposedExecution.World := ComposedExecution.deliver certifiedBatch batchCertificate
def receivedActor : Actor := receiveActor predictedActor batchCertificate 4 3

def repairedBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch deliveredBatch receivedActor (.repair (_root_.repairCommand sourceBytes))

theorem native_install_ready :
    ReadyFor NativeFixture.start (.install _root_.installCommand) installed installActor.identity installActor.nonce := by
  refine ⟨rfl, install_local, ?_, ?_⟩
  · intro i bound good
    exact ⟨rfl, by simp [NativeFixture.start, initialWorld]⟩
  · intro i bound good e cancelled
    cases cancelled

theorem native_install_batch_once : landedCount installedBatch.2 = 1 ∧ installedBatch.1.plant = installed := by
  exact runBatch_stable_completion NativeFixture.start installActor (.install _root_.installCommand)
    installed install_local rfl rfl (by decide) native_install_ready

theorem native_install_batch_common_history :
    ∃ next events, Aligned authority installedBatch.1 next ∧
      Trace authority.config (Initial authority.config before) events next :=
  runBatch_refines_history authority NativeFixture.start (Initial authority.config before)
    start_aligned start_reachable installActor (.install _root_.installCommand)

theorem native_certificate_exact :
    (certifyTransition installedBatch.1 [0,1,2] (source 1)).2 = some batchCertificate := by decide

theorem native_actor_receives_full_policy :
    receivedActor = { installActor with policy := source 1, observedPlant := installed, nonce := 4 } := by rfl

theorem native_repair_proposal :
    localStep receivedActor.observedPlant receivedActor.policy receivedActor.observedTime
      (.repair (_root_.repairCommand sourceBytes)) = some repaired := by
  rw [native_actor_receives_full_policy]
  exact repair_local

theorem native_repair_ready :
    ReadyFor deliveredBatch (.repair (_root_.repairCommand sourceBytes)) repaired
      receivedActor.identity receivedActor.nonce := by
  rw [native_actor_receives_full_policy]
  refine ⟨rfl, ?_, ?_, ?_⟩
  · change localStep deliveredBatch.plant deliveredBatch.effectivePolicy deliveredBatch.now
      (.repair (_root_.repairCommand sourceBytes)) = some repaired
    have plantEq : deliveredBatch.plant = installed := by
      change installedBatch.1.plant = installed
      exact native_install_batch_once.2
    rw [plantEq]
    exact repair_local
  · intro i bound good
    have finite : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by
      have bound4 : i < 4 := bound
      omega
    rcases finite with rfl | rfl | rfl | rfl
    · have impossible : true = false := good
      cases impossible
    · decide
    · decide
    · decide
  · have firstFresh : FreshAbove installedBatch.1 4 := by
      have result := runBatch_fresh NativeFixture.start installActor (.install _root_.installCommand)
        native_install_ready.2.2.2
      simpa only [installActor, Nat.zero_add] using result
    exact deliver_fresh certifiedBatch batchCertificate 4
      (certifyTransition_fresh installedBatch.1 [0,1,2] (source 1) 4 firstFresh)

theorem native_repair_batch_once : landedCount repairedBatch.2 = 1 ∧ repairedBatch.1.plant = repaired := by
  apply runBatch_stable_completion deliveredBatch receivedActor (.repair (_root_.repairCommand sourceBytes))
    repaired native_repair_proposal
  · rfl
  · rfl
  · decide
  · exact native_repair_ready

theorem native_full_batch_runtime_trace :
    ∃ events, RuntimeWithCancellationTrace authority NativeFixture.start events repairedBatch.1 := by
  obtain ⟨firstEvents, firstTrace⟩ := runBatch_runtime_trace authority NativeFixture.start installActor
    (.install _root_.installCommand)
  obtain ⟨lastEvents, lastTrace⟩ := runBatch_runtime_trace authority deliveredBatch receivedActor
    (.repair (_root_.repairCommand sourceBytes))
  change RuntimeWithCancellationTrace authority NativeFixture.start firstEvents installedBatch.1 at firstTrace
  change RuntimeWithCancellationTrace authority deliveredBatch lastEvents repairedBatch.1 at lastTrace
  have current : installedBatch.1.effectivePolicy.epoch = 2 + 0 := by
    have policyEq := (runBatch_static NativeFixture.start installActor (.install _root_.installCommand)).2.2.2.2.1
    change installedBatch.1.effectivePolicy = _ at policyEq
    rw [policyEq]
    rfl
  have middle : RuntimeWithCancellationTrace authority installedBatch.1
      [.ordinary (.certify 0 [0,1,2]), .ordinary (.deliver batchCertificate)] deliveredBatch :=
    .cons (.ordinary (.certify installedBatch.1 0 [0,1,2] current (by decide) rfl (by decide)))
      (.cons (.ordinary (.deliver certifiedBatch batchCertificate)) (.nil _))
  have firstMiddle := runtime_trace_append firstTrace middle
  exact ⟨_, runtime_trace_append firstMiddle lastTrace⟩

theorem native_full_batch_common_history :
    ∃ next events, Aligned authority repairedBatch.1 next ∧
      Trace authority.config (Initial authority.config before) events next := by
  obtain ⟨events, history⟩ := native_full_batch_runtime_trace
  exact runtime_cancel_trace_refines_history authority start_aligned start_reachable history

theorem native_full_plant_and_audits :
    repairedBatch.1.plant.source = before.source ∧
    repairedBatch.1.plant.destination = before.destination ∧
    repairedBatch.1.plant.standard = before.standard ∧
    repairedBatch.1.plant.unrelated = before.unrelated ∧
    repairedBatch.1.plant.rule = .exact ∧ repairedBatch.1.plant.draft = sourceBytes ∧
    repairedBatch.1.plant.ruleVersion = 4 ∧ repairedBatch.1.plant.draftRevision = 9 ∧
    repairedBatch.1.plant.ruleHistory = [.normalizedLF] ∧
    repairedBatch.1.plant.draftHistory = [[88], sourceBytes ++ [10]] := by
  rw [native_repair_batch_once.2]
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem native_install_four_closed :
    installedBatch.2.length = 4 ∧ ∀ record ∈ installedBatch.2, record.closed = true := by
  exact ⟨runBatch_length _ _ _, runBatch_records_closed _ _ _ rfl rfl rfl rfl⟩

theorem native_repair_four_closed :
    repairedBatch.2.length = 4 ∧ ∀ record ∈ repairedBatch.2, record.closed = true := by
  exact ⟨runBatch_length _ _ _, runBatch_records_closed _ _ _ rfl rfl rfl rfl⟩

/-- Authentic old actor time still creates proposals, but the actual world has
reached the lease boundary. Logical trial completion is not live admission. -/
def expiredBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch (setReferenceTime NativeFixture.start 90) installActor (.install _root_.installCommand)

theorem native_expired_batch_zero : landedCount expiredBatch.2 = 0 := by decide

theorem native_expired_batch_unchanged : expiredBatch.1.plant = before :=
  runBatch_zero_landings_unchanged _ _ _ native_expired_batch_zero

theorem native_expired_still_prepared_or_cancelled :
    (expiredBatch.1.roots 1).cancelled ≠ [] := by decide

/-- The actor-observed time fails source admission even though actual time 2
would admit. The source generates four synthetic closed log records. -/
def nonadmittingActor : Actor := { installActor with observedTime := 0 }
def syntheticBatch : ComposedExecution.World × List AttemptTrace :=
  runBatch NativeFixture.start nonadmittingActor (.install _root_.installCommand)

theorem native_synthetic_closure_without_cancellation :
    (∀ record ∈ syntheticBatch.2, record.closed = true) ∧
    (syntheticBatch.1.roots 1).cancelled = [] ∧ landedCount syntheticBatch.2 = 0 := by decide

#print axioms native_install_batch_once
#print axioms native_install_batch_common_history
#print axioms native_certificate_exact
#print axioms native_actor_receives_full_policy
#print axioms native_repair_batch_once
#print axioms native_full_batch_common_history
#print axioms native_full_plant_and_audits
#print axioms native_expired_batch_zero
#print axioms native_synthetic_closure_without_cancellation
end
end OperationalJoin.Offset.Batch.Native
