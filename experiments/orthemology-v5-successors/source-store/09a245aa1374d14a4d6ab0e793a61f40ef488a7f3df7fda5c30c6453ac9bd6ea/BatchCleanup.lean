import BatchFrames

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

theorem full_path_cancel_closes (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (owner : requester = e.action.actor)
    (valid : validPath w e = true) (length : e.path.length = 3) (budget : w.budget = 1) :
    (cancelWith w e requester e.path).2 = true := by
  have nodup : e.path.Nodup := (of_decide_eq_true valid).1
  unfold cancelWith
  have guard : (validPath w e && decide (e.path.Nodup ∧ ∀ i ∈ e.path, i ∈ e.path)) = true := by
    simp only [valid, Bool.true_and]
    exact decide_eq_true ⟨nodup, by intro _ member; exact member⟩
  rw [if_pos guard]
  have filterTrue : e.path.filter (fun _ => true) = e.path := by
    induction e.path with
    | nil => rfl
    | cons i rest ih =>
        change i :: rest.filter (fun _ => true) = i :: rest
        exact congrArg (List.cons i) ih
  simp [owner, filterTrue, length, budget]

theorem serviceTrial_closes (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (owner : requester = e.action.actor)
    (valid : validPath w e = true) (length : e.path.length = 3) (budget : w.budget = 1) :
    (serviceTrial w e requester).2.closed = true := by
  have ps := prepare_static w e requester true
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simp only [serviceTrial, prepared, Bool.false_eq_true, if_false]
      exact full_path_cancel_closes _ e requester owner
        (by simpa only [validPath, ps.1, ps.2.1] using valid) length (ps.2.2.1.trans budget)
  | true =>
      simp only [serviceTrial, prepared, if_true]
      have ats := attempt_static (ComposedExecution.prepare w e requester true).1 e requester false
      exact full_path_cancel_closes _ e requester owner
        (by simpa only [validPath, ats.1, ats.2.1, ps.1, ps.2.1] using valid) length
        (ats.2.2.1.trans (ps.2.2.1.trans budget))

theorem batchBody_records_closed (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat)
    (owner : actor.identity = action.actor) (valid : path.Nodup ∧ path.length = acc.1.q ∧ ∀ i ∈ path, i < acc.1.n)
    (length : path.length = 3) (budget : acc.1.budget = 1)
    (already : ∀ record ∈ acc.2, record.closed = true) :
    ∀ record ∈ (batchBody actor action acc path).2, record.closed = true := by
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none =>
      simp only [batchBody, proposal]
      intro record member
      rcases List.mem_append.mp member with old | new
      · exact already record old
      · have same := List.mem_singleton.mp new
        subst record
        rfl
  | some e =>
      have fields := proposal_fields _ _ _ e proposal
      rw [batchBody_of_proposal actor action acc path e proposal]
      intro record member
      rcases List.mem_append.mp member with old | new
      · exact already record old
      · have same := List.mem_singleton.mp new
        subst record
        exact serviceTrial_closes acc.1 e actor.identity (by simpa only [fields.1] using owner)
          (decide_eq_true (by simpa only [fields.2.1] using valid))
          (by simpa only [fields.2.1] using length) budget

theorem fold_records_closed (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace)
    (owner : actor.identity = action.actor)
    (wellformed : ∀ path ∈ paths, path.Nodup ∧ path.length = acc.1.q ∧ ∀ i ∈ path, i < acc.1.n)
    (lengths : ∀ path ∈ paths, path.length = 3) (budget : acc.1.budget = 1)
    (already : ∀ record ∈ acc.2, record.closed = true) :
    ∀ record ∈ (paths.foldl (batchBody actor action) acc).2, record.closed = true := by
  induction paths generalizing acc with
  | nil => exact already
  | cons path rest ih =>
      have static := batchBody_static actor action acc path
      apply ih
      · intro p member
        simpa only [static.1, static.2.1] using wellformed p (by simp [member])
      · intro p member; exact lengths p (by simp [member])
      · exact static.2.2.1.trans budget
      · exact batchBody_records_closed actor action acc path owner (wellformed path (by simp))
          (lengths path (by simp)) budget already

/-- All four log records are closed for the correctly named owner at n=4,
q=3,B=1. Proposal-none closure is still synthetic; proposed trials invoke the
actual cancellation call and obtain its true current-call reply. -/
theorem runBatch_records_closed (w : ComposedExecution.World) (actor : Actor) (action : Action)
    (owner : actor.identity = action.actor) (roots : w.n = 4) (quorum : w.q = 3) (budget : w.budget = 1) :
    ∀ record ∈ (runBatch w actor action).2, record.closed = true := by
  rw [runBatch_eq_fold]
  apply fold_records_closed actor action fourPaths (w, []) owner
  · intro path member
    exact ⟨(fourPaths_bounded path member).1,
      by simpa only [quorum] using fourPaths_length path member,
      by simpa only [roots] using (fourPaths_bounded path member).2⟩
  · exact fourPaths_length
  · exact budget
  · intro record impossible; cases impossible

#print axioms serviceTrial_closes
#print axioms runBatch_records_closed
end
end OperationalJoin.Offset.Batch
