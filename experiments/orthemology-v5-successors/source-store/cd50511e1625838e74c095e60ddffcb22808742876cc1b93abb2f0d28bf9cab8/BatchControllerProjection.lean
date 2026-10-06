import BatchNative

namespace OperationalJoin.Offset.Batch.ControllerProjection
noncomputable section
open Classical
open ComposedExecution
open NativeFixture
set_option maxRecDepth 60000
set_option maxHeartbeats 8000000

/-- Pure projection of the let-bound source sequence in the accepted
composition/tests/BatchTests.lean, excluding IO assertions and the outer test
loop. The actual service and actor functions are imported unchanged. -/
def batchTestsPureProjection (bytes : List Nat) (bad : List Nat) :
    ComposedExecution.World × List AttemptTrace :=
  let p := _root_.plant bytes
  let ip := _root_.policy "install-criterion"
  let rp := _root_.policy "replace-derived" 3
  let expectedInstalled := { p with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] }
  let actor : Actor := ⟨ip, p, "A", 2, 0⟩
  let w := initialWorld p ip bad
  let installed := runBatch w actor (.install _root_.installCommand)
  let actorAfter := { actor with observedPlant := expectedInstalled, nonce := 4 }
  let revoked := certifyTransition installed.1 [0,1,2] rp
  let certificate := revoked.2.getD ⟨2, rp, [0,1,2]⟩
  let actorRepair := receiveActor actorAfter certificate 4 3
  runBatch (ComposedExecution.deliver revoked.1 certificate) actorRepair (.repair (_root_.repairCommand bytes))

/-- The new native aggregate witness is exactly this source projection at the
pinned complete source and the declared bad-root-0 fixture. -/
theorem native_is_exact_controller_projection :
    batchTestsPureProjection sourceBytes [0] = Native.repairedBatch := by
  rfl

theorem exact_source_projection_completes :
    landedCount (batchTestsPureProjection sourceBytes [0]).2 = 1 ∧
      (batchTestsPureProjection sourceBytes [0]).1.plant = repaired := by
  rw [native_is_exact_controller_projection]
  exact Native.native_repair_batch_once

#print axioms native_is_exact_controller_projection
#print axioms exact_source_projection_completes
end
end OperationalJoin.Offset.Batch.ControllerProjection
