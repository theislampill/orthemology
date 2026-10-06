import RuntimeCancellationControls

namespace BatchHistoryPremiseReview
noncomputable section
open Classical
open OperationalJoin OperationalJoin.Offset ComposedExecution NativeFixture
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/- This file uses the accepted full pinned native source fixture. Unlike a
malformed-world counterexample, the blockage is reached by an actual permitted
cancellation operation from the genuine aligned initial state. -/
def actualFourth : Typed.BoundedEnvelope 4 :=
  ⟨{ installEnvelope.val with nonce := 4 }, by decide⟩
def blockedStart : World :=
  (cancelWith start actualFourth.val "A" [1,2,3]).1

theorem cancellation_reaches_aligned_blocked_start :
    ∃ s, Aligned authority blockedStart s ∧ Reachable authority.config s := by
  obtain ⟨aligned, history⟩ := cancelWith_preserves_alignment authority start
    (Initial authority.config before) start_aligned actualFourth "A" [1,2,3]
    (by decide) (by decide) (by decide)
  exact ⟨_, aligned, reachable_after start_reachable history⟩

theorem aligned_reachable_current_proposal_can_still_stall :
    (∃ s, Aligned authority blockedStart s ∧ Reachable authority.config s) ∧
    localStep before (source 0) 2 (.install _root_.installCommand) = some installed ∧
    blockedStart.plant = before ∧ blockedStart.effectivePolicy = source 0 ∧
    (runBatch blockedStart installActor (.install _root_.installCommand)).2.map
      AttemptTrace.landed = [false,false,false,false] ∧
    (runBatch blockedStart installActor (.install _root_.installCommand)).1.plant = before := by
  exact ⟨cancellation_reaches_aligned_blocked_start, install_local,
    by decide, by decide, by decide, by decide⟩

/-- The cancellation call really returns true and preserves all old plant
versions; inability to land is not masked by an already-consumed command. -/
theorem full_envelope_cancellation_is_the_missing_premise :
    (cancelWith start actualFourth.val "A" [1,2,3]).2 = true ∧
    blockedStart.plant.ruleVersion = 3 ∧
    actualFourth.val ∈ (blockedStart.roots 1).cancelled ∧
    (runBatch blockedStart installActor (.install _root_.installCommand)).2.map
      AttemptTrace.prepared = [true,true,true,false] := by decide

#print axioms cancellation_reaches_aligned_blocked_start
#print axioms aligned_reachable_current_proposal_can_still_stall
#print axioms full_envelope_cancellation_is_the_missing_premise
end
end BatchHistoryPremiseReview
