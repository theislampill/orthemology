import Fixtures

/- Independent direct-source controls. These small plant payloads keep reduction
cost bounded; they are not a substitute for the separately pinned native bytes.
No new batch/controller definition is used to compute the outcomes. -/
namespace BatchSourceReview
open ComposedExecution
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

def p : Plant := _root_.plant [65]
def pol : Policy := _root_.policy "install-criterion"
def a : Action := .install _root_.installCommand
def actor : Actor := ⟨pol, p, "A", 2, 0⟩
def w (bad : List Nat) : World := initialWorld p pol bad
def successor : Plant :=
  { p with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] }
def fourth : Envelope := ⟨a, successor, 4, [1,2,3]⟩
def first : Envelope := ⟨a, successor, 1, [0,1,2]⟩

theorem source_admits : localStep p pol 2 a = some successor := by decide

/-- Exhaust the sixteen possible taint patterns on the four named roots.
This is a pure portfolio fact, independent of any service-admission premise. -/
theorem intact_portfolio_path_iff_at_most_one_fault :
    ∀ b0 b1 b2 b3 : Bool,
      let bad := [b0,b1,b2,b3]
      (∃ path ∈ fourPaths, ∀ i ∈ path, (bad[i]?).getD false = false) ↔
        (bad.filter id).length ≤ 1 := by decide

/-- Each path is needed for this fixed three-of-four, one-fault guarantee. -/
theorem deleting_any_path_loses_one_fault_guarantee :
    (∀ path ∈ fourPaths.erase [0,1,2], 3 ∈ path) ∧
    (∀ path ∈ fourPaths.erase [0,1,3], 2 ∈ path) ∧
    (∀ path ∈ fourPaths.erase [0,2,3], 1 ∈ path) ∧
    (∀ path ∈ fourPaths.erase [1,2,3], 0 ∈ path) := by decide

theorem no_proposal_has_synthetic_closed_logs :
    let out := runBatch (w [0]) { actor with observedTime := 90 } a
    out.2.map AttemptTrace.closed = [true,true,true,true] ∧
    out.2.map AttemptTrace.prepared = [false,false,false,false] ∧
    out.2.map AttemptTrace.landed = [false,false,false,false] ∧
    (out.1.roots 0).commitments = [] ∧
    (out.1.roots 1).cancelled = [] ∧ out.1.plant = p := by decide

theorem wrong_requester_retains_partial_prepare_effect :
    let out := runBatch (w [0]) { actor with identity := "B" } a
    out.2.map AttemptTrace.prepared = [false,false,false,false] ∧
    out.2.map AttemptTrace.landed = [false,false,false,false] ∧
    out.2.map AttemptTrace.closed = [false,false,false,false] ∧
    first ∈ (out.1.roots 0).commitments ∧
    first ∉ (out.1.roots 1).commitments ∧ out.1.plant = p := by decide

theorem stale_time_observation_does_not_create_progress :
    let out := runBatch { w [0] with now := 90 } actor a
    out.2.map AttemptTrace.prepared = [false,false,false,false] ∧
    out.2.map AttemptTrace.landed = [false,false,false,false] ∧
    out.2.map AttemptTrace.closed = [true,true,true,true] ∧
    first ∈ (out.1.roots 0).commitments ∧
    first ∉ (out.1.roots 1).commitments ∧
    first ∈ (out.1.roots 1).cancelled ∧ out.1.plant = p := by decide

theorem success_does_not_stop_or_refresh_actor :
    let out := runBatch (w []) actor a
    out.2.map AttemptTrace.prepared = [true,false,false,false] ∧
    out.2.map AttemptTrace.landed = [true,false,false,false] ∧
    out.2.map AttemptTrace.closed = [true,true,true,true] ∧
    out.2.map AttemptTrace.nonce = [1,2,3,4] ∧
    out.2.map AttemptTrace.path = fourPaths ∧ out.1.plant = successor := by decide

theorem one_fault_portfolio_positions :
    (runBatch (w [0]) actor a).2.map AttemptTrace.landed = [false,false,false,true] ∧
    (runBatch (w [1]) actor a).2.map AttemptTrace.landed = [false,false,true,false] ∧
    (runBatch (w [2]) actor a).2.map AttemptTrace.landed = [false,true,false,false] ∧
    (runBatch (w [3]) actor a).2.map AttemptTrace.landed = [true,false,false,false] := by decide

theorem two_faults_block_every_path :
    let out := runBatch (w [0,1]) actor a
    out.2.map AttemptTrace.prepared = [true,true,true,true] ∧
    out.2.map AttemptTrace.landed = [false,false,false,false] ∧ out.1.plant = p := by decide

def fourthCancelled : World := (cancelWith (w [0]) fourth "A" [1,2,3]).1

theorem prior_tombstone_blocks_only_intact_path :
    (cancelWith (w [0]) fourth "A" [1,2,3]).2 = true ∧
    (runBatch fourthCancelled actor a).2.map AttemptTrace.prepared = [true,true,true,false] ∧
    (runBatch fourthCancelled actor a).2.map AttemptTrace.landed = [false,false,false,false] ∧
    (runBatch fourthCancelled actor a).1.plant = p := by decide

/-- A high-water condition over all old tombstones is sufficient but not
necessary. This larger-nonce old envelope differs from every prospective trial. -/
theorem unrelated_high_nonce_tombstone_does_not_block_progress :
    let old := { first with nonce := 100 }
    let oldWorld := (cancelWith (w [0]) old "A" [1,2]).1
    old ∈ (oldWorld.roots 1).cancelled ∧ actor.nonce < old.nonce ∧
    oldWorld.tainted 1 = false ∧
    (runBatch oldWorld actor a).2.map AttemptTrace.landed = [false,false,false,true] ∧
    (runBatch oldWorld actor a).1.plant = successor := by decide

theorem repeated_actor_reuses_nonce_sequence :
    let out := runBatch (w [0]) actor a
    out.2.map AttemptTrace.nonce = [1,2,3,4] ∧
    (runBatch out.1 actor a).2.map AttemptTrace.nonce = [1,2,3,4] := by decide

theorem wrong_path_quorum_rejects_before_mutation :
    let out := runBatch { w [0] with q := 2 } actor a
    out.2.map AttemptTrace.prepared = [false,false,false,false] ∧
    out.2.map AttemptTrace.landed = [false,false,false,false] ∧
    out.2.map AttemptTrace.closed = [false,false,false,false] ∧
    (out.1.roots 0).commitments = [] ∧ (out.1.roots 1).cancelled = [] := by decide

theorem cancellation_threshold_is_separate_from_progress :
    let out := runBatch { w [] with budget := 3 } actor a
    out.2.map AttemptTrace.landed = [true,false,false,false] ∧
    out.2.map AttemptTrace.closed = [false,false,false,false] ∧
    first ∈ (out.1.roots 1).cancelled ∧ out.1.plant = successor := by decide

#print axioms source_admits
#print axioms intact_portfolio_path_iff_at_most_one_fault
#print axioms deleting_any_path_loses_one_fault_guarantee
#print axioms no_proposal_has_synthetic_closed_logs
#print axioms wrong_requester_retains_partial_prepare_effect
#print axioms stale_time_observation_does_not_create_progress
#print axioms success_does_not_stop_or_refresh_actor
#print axioms one_fault_portfolio_positions
#print axioms two_faults_block_every_path
#print axioms prior_tombstone_blocks_only_intact_path
#print axioms unrelated_high_nonce_tombstone_does_not_block_progress
#print axioms repeated_actor_reuses_nonce_sequence
#print axioms wrong_path_quorum_rejects_before_mutation
#print axioms cancellation_threshold_is_separate_from_progress
end BatchSourceReview
