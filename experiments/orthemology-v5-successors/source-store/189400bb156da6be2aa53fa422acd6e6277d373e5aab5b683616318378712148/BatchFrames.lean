import BatchProgress

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

theorem prepare_root_policy (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (i : Nat) :
    ((ComposedExecution.prepare w e requester true).1.roots i).policy = (w.roots i).policy := by
  unfold ComposedExecution.prepare
  split
  · dsimp
    split <;> split <;> rfl
  · rfl

theorem prepare_root_revoked (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (i : Nat) :
    ((ComposedExecution.prepare w e requester true).1.roots i).revoked = (w.roots i).revoked := by
  unfold ComposedExecution.prepare
  split
  · dsimp
    split <;> split <;> rfl
  · rfl

theorem attempt_roots (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) : (attempt w e requester badOpen).1.roots = w.roots := by
  unfold attempt
  split <;> rfl

theorem cancel_root_policy (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (i : Nat) :
    ((cancelWith w e requester e.path).1.roots i).policy = (w.roots i).policy := by
  unfold cancelWith
  split
  · dsimp
    split <;> rfl
  · rfl

theorem cancel_root_revoked (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (i : Nat) :
    ((cancelWith w e requester e.path).1.roots i).revoked = (w.roots i).revoked := by
  unfold cancelWith
  split
  · dsimp
    split <;> rfl
  · rfl

theorem serviceTrial_root_frame (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (i : Nat) :
    ((serviceTrial w e requester).1.roots i).policy = (w.roots i).policy ∧
    ((serviceTrial w e requester).1.roots i).revoked = (w.roots i).revoked := by
  cases prepared : (ComposedExecution.prepare w e requester true).2 <;>
    simp only [serviceTrial, prepared, Bool.false_eq_true, if_false, if_true,
      cancel_root_policy, cancel_root_revoked, attempt_roots, prepare_root_policy, prepare_root_revoked, and_self]

theorem batchBody_root_frame (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat) (i : Nat) :
    ((batchBody actor action acc path).1.roots i).policy = (acc.1.roots i).policy ∧
    ((batchBody actor action acc path).1.roots i).revoked = (acc.1.roots i).revoked := by
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none => simp [batchBody, proposal]
  | some e =>
      rw [batchBody_of_proposal actor action acc path e proposal]
      exact serviceTrial_root_frame acc.1 e actor.identity i

theorem fold_root_frame (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace) (i : Nat) :
    (((paths.foldl (batchBody actor action) acc).1).roots i).policy = (acc.1.roots i).policy ∧
    (((paths.foldl (batchBody actor action) acc).1).roots i).revoked = (acc.1.roots i).revoked := by
  induction paths generalizing acc with
  | nil => exact ⟨rfl, rfl⟩
  | cons path rest ih =>
      have tail := ih (batchBody actor action acc path)
      have head := batchBody_root_frame actor action acc path i
      exact ⟨tail.1.trans head.1, tail.2.trans head.2⟩

theorem runBatch_root_frame (w : ComposedExecution.World) (actor : Actor) (action : Action) (i : Nat) :
    ((runBatch w actor action).1.roots i).policy = (w.roots i).policy ∧
    ((runBatch w actor action).1.roots i).revoked = (w.roots i).revoked := by
  rw [runBatch_eq_fold]
  exact fold_root_frame actor action fourPaths (w, []) i

theorem fold_static (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace) :
    (paths.foldl (batchBody actor action) acc).1.n = acc.1.n ∧
    (paths.foldl (batchBody actor action) acc).1.q = acc.1.q ∧
    (paths.foldl (batchBody actor action) acc).1.budget = acc.1.budget ∧
    (paths.foldl (batchBody actor action) acc).1.now = acc.1.now ∧
    (paths.foldl (batchBody actor action) acc).1.effectivePolicy = acc.1.effectivePolicy ∧
    (paths.foldl (batchBody actor action) acc).1.tainted = acc.1.tainted := by
  induction paths generalizing acc with
  | nil => exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩
  | cons path rest ih =>
      have tail := ih (batchBody actor action acc path)
      have head := batchBody_static actor action acc path
      exact ⟨tail.1.trans head.1, tail.2.1.trans head.2.1, tail.2.2.1.trans head.2.2.1,
        tail.2.2.2.1.trans head.2.2.2.1, tail.2.2.2.2.1.trans head.2.2.2.2.1,
        tail.2.2.2.2.2.trans head.2.2.2.2.2⟩

theorem runBatch_static (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    (runBatch w actor action).1.n = w.n ∧
    (runBatch w actor action).1.q = w.q ∧
    (runBatch w actor action).1.budget = w.budget ∧
    (runBatch w actor action).1.now = w.now ∧
    (runBatch w actor action).1.effectivePolicy = w.effectivePolicy ∧
    (runBatch w actor action).1.tainted = w.tainted := by
  rw [runBatch_eq_fold]
  exact fold_static actor action fourPaths (w, [])

#print axioms runBatch_root_frame
#print axioms runBatch_static
end
end OperationalJoin.Offset.Batch
