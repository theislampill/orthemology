import BatchSourceChallenges
import RuntimeCancellationControls

namespace BatchAvailabilityIffSourceReview
noncomputable section
open Classical
open ComposedExecution OperationalJoin OperationalJoin.Offset BatchSourceReview
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

def e1 : Typed.BoundedEnvelope 4 := ⟨first, by decide⟩
def e2 : Typed.BoundedEnvelope 4 := ⟨⟨a, successor, 2, [0,1,3]⟩, by decide⟩
def e3 : Typed.BoundedEnvelope 4 := ⟨⟨a, successor, 3, [0,2,3]⟩, by decide⟩
def e4 : Typed.BoundedEnvelope 4 := ⟨fourth, by decide⟩
def c1 : World := (cancelWith (w []) e1.val "A" [0]).1
def c2 : World := (cancelWith c1 e2.val "A" [0]).1
def c3 : World := (cancelWith c2 e3.val "A" [0]).1
def c4 : World := (cancelWith c3 e4.val "A" [1]).1

/-- Four different envelopes each receive only one selected owner reply. No
current-call cancellation reaches the numerical B+1 threshold. -/
theorem four_preliminary_cancellation_replies_are_false :
    (cancelWith (w []) e1.val "A" [0]).2 = false ∧
    (cancelWith c1 e2.val "A" [0]).2 = false ∧
    (cancelWith c2 e3.val "A" [0]).2 = false ∧
    (cancelWith c3 e4.val "A" [1]).2 = false := by decide

/-- Actual good-root memory still blocks every individual trial. A false
cancellation reply does not mean no partial mutation or trial availability. -/
theorem selected_singleton_tombstones_block_all_four_trials :
    e1.val ∈ (c4.roots 0).cancelled ∧
    e2.val ∈ (c4.roots 0).cancelled ∧
    e3.val ∈ (c4.roots 0).cancelled ∧
    e4.val ∈ (c4.roots 1).cancelled ∧
    (runBatch c4 actor a).2.map AttemptTrace.prepared = [false,false,false,false] ∧
    (runBatch c4 actor a).2.map AttemptTrace.landed = [false,false,false,false] ∧
    (runBatch c4 actor a).1.plant = p := by decide

def zeroFaultAuthority : Authority 2 4 :=
  { NativeFixture.authority with faulty := ∅, budget_bound := by decide }

theorem zero_fault_initial_alignment :
    Aligned zeroFaultAuthority (w []) (Initial zeroFaultAuthority.config p) := by
  apply initial_aligned zeroFaultAuthority p [] rfl rfl rfl
  intro i
  simp [zeroFaultAuthority]

theorem partial_cleanup_history_is_genuine :
    RuntimeWithCancellationTrace zeroFaultAuthority (w [])
      [.cancel e1 "A" [0], .cancel e2 "A" [0], .cancel e3 "A" [0], .cancel e4 "A" [1]] c4 :=
  .cons (.cancel (w []) e1 "A" [0])
    (.cons (.cancel c1 e2 "A" [0])
      (.cons (.cancel c2 e3 "A" [0]) (.cons (.cancel c3 e4 "A" [1]) (.nil _))))

theorem partial_cleanup_blockage_is_aligned_and_reachable :
    ∃ s, Aligned zeroFaultAuthority c4 s ∧ Reachable zeroFaultAuthority.config s := by
  have reachable : Reachable zeroFaultAuthority.config (Initial zeroFaultAuthority.config p) :=
    ⟨p, [], Trace.nil _⟩
  obtain ⟨next, events, aligned, history⟩ := runtime_cancel_trace_refines_history
    zeroFaultAuthority zero_fault_initial_alignment reachable partial_cleanup_history_is_genuine
  exact ⟨next, aligned, reachable_after reachable history⟩

#print axioms four_preliminary_cancellation_replies_are_false
#print axioms selected_singleton_tombstones_block_all_four_trials
#print axioms zero_fault_initial_alignment
#print axioms partial_cleanup_history_is_genuine
#print axioms partial_cleanup_blockage_is_aligned_and_reachable
end
end BatchAvailabilityIffSourceReview
