import Composition

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

/-- A name for the literal source fold body. It is not an alternative service:
`runBatch_eq_fold` is definitional equality to the unchanged imported function. -/
def batchBody (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat) :
    ComposedExecution.World × List AttemptTrace :=
  let current := acc.1
  let traces := acc.2
  let trialActor := { actor with nonce := actor.nonce + traces.length }
  match propose trialActor action path with
  | none => (current, traces ++ [⟨trialActor.nonce + 1, path, false, false, true,
      current.plant.ruleVersion, current.plant.draftRevision⟩])
  | some e =>
      let prepared := ComposedExecution.prepare current e actor.identity
      let landed := if prepared.2 then attempt prepared.1 e actor.identity false else (prepared.1, false)
      let closed := cancelWith landed.1 e actor.identity e.path
      (closed.1, traces ++ [⟨e.nonce, path, prepared.2, landed.2, closed.2,
        closed.1.plant.ruleVersion, closed.1.plant.draftRevision⟩])

theorem runBatch_eq_fold (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    runBatch w actor action = fourPaths.foldl (batchBody actor action) (w, []) := rfl

theorem proposal_fields (actor : Actor) (action : Action) (path : List Nat)
    (e : ComposedExecution.Envelope) (proposal : propose actor action path = some e) :
    e.action = action ∧ e.path = path ∧ e.nonce = actor.nonce + 1 := by
  unfold propose at proposal
  cases result : localStep actor.observedPlant actor.policy actor.observedTime action with
  | none => simp [result] at proposal
  | some successor =>
      simp only [result, Option.map_some, Option.some.injEq] at proposal
      cases proposal
      exact ⟨rfl, rfl, rfl⟩

theorem fourPaths_bounded (path : List Nat) (member : path ∈ fourPaths) :
    path.Nodup ∧ (∀ i ∈ path, i < 4) := by
  simp only [fourPaths, List.mem_cons, List.not_mem_nil, or_false] at member
  rcases member with rfl | rfl | rfl | rfl <;> decide

theorem fourPaths_length (path : List Nat) (member : path ∈ fourPaths) :
    path.length = 3 := by
  simp only [fourPaths, List.mem_cons, List.not_mem_nil, or_false] at member
  rcases member with rfl | rfl | rfl | rfl <;> rfl

theorem batchBody_record (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat) :
    ∃ record, (batchBody actor action acc path).2 = acc.2 ++ [record] ∧
      record.path = path ∧ record.nonce = actor.nonce + acc.2.length + 1 := by
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none => simp only [batchBody, proposal]; exact ⟨_, rfl, rfl, rfl⟩
  | some raw =>
      have fields := proposal_fields _ _ _ raw proposal
      simp only [batchBody, proposal]
      exact ⟨_, rfl, rfl, fields.2.2⟩

theorem batchBody_length (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat) :
    (batchBody actor action acc path).2.length = acc.2.length + 1 := by
  obtain ⟨record, records, _, _⟩ := batchBody_record actor action acc path
  simp only [records, List.length_append, List.length_singleton]

theorem fold_length (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace) :
    (paths.foldl (batchBody actor action) acc).2.length = acc.2.length + paths.length := by
  induction paths generalizing acc with
  | nil => simp
  | cons path rest ih => simp only [List.foldl_cons, ih, batchBody_length, List.length_cons]; omega

theorem fold_paths (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace) :
    ((paths.foldl (batchBody actor action) acc).2.map AttemptTrace.path) =
      acc.2.map AttemptTrace.path ++ paths := by
  induction paths generalizing acc with
  | nil => simp
  | cons path rest ih =>
      obtain ⟨record, records, recordPath, _⟩ := batchBody_record actor action acc path
      simp only [List.foldl_cons, ih, records, List.map_append, List.map_singleton, recordPath]
      simp only [List.append_assoc, List.singleton_append]

theorem runBatch_paths (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    (runBatch w actor action).2.map AttemptTrace.path = fourPaths := by
  rw [runBatch_eq_fold, fold_paths]
  rfl

theorem runBatch_length (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    (runBatch w actor action).2.length = 4 := by
  rw [runBatch_eq_fold, fold_length]
  rfl

theorem runBatch_nonces (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    (runBatch w actor action).2.map AttemptTrace.nonce =
      [actor.nonce + 1, actor.nonce + 2, actor.nonce + 3, actor.nonce + 4] := by
  rw [runBatch_eq_fold]
  simp only [fourPaths, List.foldl_cons, List.foldl_nil]
  obtain ⟨r1, h1, _, n1⟩ := batchBody_record actor action (w, []) [0,1,2]
  obtain ⟨r2, h2, _, n2⟩ := batchBody_record actor action (batchBody actor action (w, []) [0,1,2]) [0,1,3]
  obtain ⟨r3, h3, _, n3⟩ := batchBody_record actor action (batchBody actor action
    (batchBody actor action (w, []) [0,1,2]) [0,1,3]) [0,2,3]
  obtain ⟨r4, h4, _, n4⟩ := batchBody_record actor action (batchBody actor action (batchBody actor action
    (batchBody actor action (w, []) [0,1,2]) [0,1,3]) [0,2,3]) [1,2,3]
  simp only [h1, h2, h3, h4, List.map_append, List.map_singleton, List.map_nil, List.nil_append]
  simp only [h1, h2, h3, List.length_append, List.length_singleton, List.length_nil] at n1 n2 n3 n4
  simp only [n1, n2, n3, n4, List.append_assoc, List.singleton_append]
  congr 1 <;> omega


#print axioms runBatch_paths
#print axioms runBatch_nonces
#print axioms runBatch_length
end
end OperationalJoin.Offset.Batch
