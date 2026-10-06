import BatchSafety
import BatchMemory
import BatchFrames
import BatchSourceChallenges
import RuntimeFixture

namespace BatchContractReview
noncomputable section
open Classical
open ComposedExecution OperationalJoin OperationalJoin.Offset
open Batch BatchSourceReview
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- Type-check the absence of any authority, good-observation or fault-bound
argument in the literal controller's source-specific uniqueness result. -/
theorem uniqueness_has_no_hidden_readiness_argument
    (world : World) (who : Actor) (action : Action) :
    landedCount (runBatch world who action).2 ≤ 1 :=
  runBatch_at_most_one_landing world who action

theorem failed_proposal_is_full_world_identity
    (world : World) (who : Actor) (action : Action)
    (reject : localStep who.observedPlant who.policy who.observedTime action = none) :
    (runBatch world who action).1 = world := by
  simp [runBatch, fourPaths, propose, reject]

theorem semantics_progress_does_not_require_successful_cleanup :
    landedCount (runBatch { w [] with budget := 3 } actor a).2 = 1 ∧
    (runBatch { w [] with budget := 3 } actor a).1.plant = successor ∧
    (runBatch { w [] with budget := 3 } actor a).2.map AttemptTrace.closed =
      [false,false,false,false] := by
  have ready : ReadyFor { w [] with budget := 3 } a successor actor.identity actor.nonce := by
    refine ⟨rfl, source_admits, ?_, ?_⟩
    · intro i bound good
      exact ⟨rfl, by simp [w, initialWorld]⟩
    · intro i bound good e member
      change e ∈ ([] : List ComposedExecution.Envelope) at member
      cases member
  have completed := runBatch_stable_completion { w [] with budget := 3 }
    actor a successor source_admits rfl rfl (by decide) ready
  exact ⟨completed.1, completed.2, cancellation_threshold_is_separate_from_progress.2.1⟩

def old : ComposedExecution.Envelope := { first with nonce := 100 }
def oldWorld : World := (cancelWith (w [0]) old "A" [1,2]).1

theorem FreshAbove_is_not_a_necessary_progress_condition :
    ¬FreshAbove oldWorld actor.nonce ∧
    landedCount (runBatch oldWorld actor a).2 = 1 := by
  constructor
  · intro fresh
    have upper := fresh 1 (by decide) (by decide) old (by decide)
    change 100 ≤ 0 at upper
    omega
  · decide

/-- The actual history theorem accepts every actor without assuming success,
while preserving the original full authority/alignment/reachability boundary. -/
theorem arbitrary_actor_refinement_has_exact_assumptions {base}
    (authority : Authority base 4) (world : World) (s : State (interface base 4))
    (aligned : Aligned authority world s) (reachable : Reachable authority.config s)
    (who : Actor) (action : Action) :
    ∃ next events, Aligned authority (runBatch world who action).1 next ∧
      Trace authority.config s events next :=
  runBatch_refines_history authority world s aligned reachable who action

/-- Instantiate the new theorem on the unchanged full 3,013-byte native
installation fixture. This is an actual aggregate batch, not a chosen-path call. -/
theorem full_native_installation_batch_reaches_exact_successor :
    landedCount (runBatch NativeFixture.start NativeFixture.installActor
      (.install _root_.installCommand)).2 = 1 ∧
    (runBatch NativeFixture.start NativeFixture.installActor
      (.install _root_.installCommand)).1.plant = NativeFixture.installed := by
  apply runBatch_stable_completion NativeFixture.start NativeFixture.installActor
    (.install _root_.installCommand) NativeFixture.installed
    NativeFixture.install_local rfl rfl (by decide)
  refine ⟨rfl, NativeFixture.install_local, ?_, ?_⟩
  · intro i bound good
    exact ⟨rfl, by simp [NativeFixture.start, initialWorld]⟩
  · intro i bound good e member
    change e ∈ ([] : List ComposedExecution.Envelope) at member
    cases member

#print axioms uniqueness_has_no_hidden_readiness_argument
#print axioms failed_proposal_is_full_world_identity
#print axioms semantics_progress_does_not_require_successful_cleanup
#print axioms FreshAbove_is_not_a_necessary_progress_condition
#print axioms arbitrary_actor_refinement_has_exact_assumptions
#print axioms full_native_installation_batch_reaches_exact_successor
end
end BatchContractReview
