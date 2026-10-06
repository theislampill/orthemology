import BatchExactProgress
import RuntimeFixture

namespace OperationalJoin.Offset.Batch.ExactControls
noncomputable section
open Classical
open ComposedExecution
open NativeFixture
set_option maxRecDepth 60000
set_option maxHeartbeats 8000000

/-- Same native source and action, unrelated solely by complete-envelope nonce.
It predates this test state as an externally supplied durable tombstone. -/
def unrelatedHighEnvelope : ComposedExecution.Envelope :=
  ⟨.install _root_.installCommand, installed, 99, [1,2,3]⟩

def highTombstoneWorld : ComposedExecution.World :=
  { NativeFixture.start with roots := fun i =>
      { NativeFixture.start.roots i with cancelled := [unrelatedHighEnvelope] } }

theorem high_tombstone_exact_ready :
    ExactReady highTombstoneWorld (.install _root_.installCommand) installed
      installActor.identity installActor.nonce fourPaths := by
  refine ⟨rfl, install_local, ?_, ?_⟩
  · intro i bound good
    exact ⟨rfl, by simp [highTombstoneWorld, NativeFixture.start, initialWorld]⟩
  · intro i bound good e future
    rw [exact_four_predicted_envelopes] at future
    simp only [List.mem_cons, List.not_mem_nil, or_false] at future
    rcases future with rfl | rfl | rfl | rfl
    all_goals dsimp [highTombstoneWorld, installActor]; decide

theorem high_tombstone_violates_conservative_freshness :
    ¬ FreshAbove highTombstoneWorld installActor.nonce := by
  intro fresh
  have bound := fresh 1 (by decide) (by decide) unrelatedHighEnvelope (by simp [highTombstoneWorld])
  change 99 ≤ 0 at bound
  omega

theorem high_tombstone_sharpened_completion :
    landedCount (runBatch highTombstoneWorld installActor (.install _root_.installCommand)).2 = 1 ∧
    (runBatch highTombstoneWorld installActor (.install _root_.installCommand)).1.plant = installed :=
  runBatch_exact_fresh_completion highTombstoneWorld installActor (.install _root_.installCommand)
    installed install_local rfl rfl (by decide) high_tombstone_exact_ready

/-- The sharp theorem admits a case explicitly excluded by the conservative
hypothesis. Neither theorem grants an actor knowledge of these root memories. -/
theorem exact_freshness_strictly_less_restrictive :
    ¬ FreshAbove highTombstoneWorld installActor.nonce ∧
    ExactReady highTombstoneWorld (.install _root_.installCommand) installed
      installActor.identity installActor.nonce fourPaths ∧
    landedCount (runBatch highTombstoneWorld installActor (.install _root_.installCommand)).2 = 1 :=
  ⟨high_tombstone_violates_conservative_freshness, high_tombstone_exact_ready,
    high_tombstone_sharpened_completion.1⟩

#print axioms high_tombstone_exact_ready
#print axioms high_tombstone_sharpened_completion
#print axioms exact_freshness_strictly_less_restrictive
end
end OperationalJoin.Offset.Batch.ExactControls
