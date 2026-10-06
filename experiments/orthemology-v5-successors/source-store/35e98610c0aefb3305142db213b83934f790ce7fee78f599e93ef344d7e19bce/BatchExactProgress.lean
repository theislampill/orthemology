import BatchExactFreshness

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

theorem fold_exact_progress (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (paths : List (List Nat)) (acc : ComposedExecution.World × List AttemptTrace)
    (wellformed : ∀ path ∈ paths, path.Nodup ∧ path.length = acc.1.q ∧ ∀ i ∈ path, i < acc.1.n)
    (ready : ExactReady acc.1 action successor actor.identity (actor.nonce + acc.2.length) paths)
    (intact : ∃ path ∈ paths, ∀ i ∈ path, acc.1.tainted i = false) :
    landedCount acc.2 < landedCount (paths.foldl (batchBody actor action) acc).2 := by
  induction paths generalizing acc with
  | nil => obtain ⟨path, impossible, _⟩ := intact; cases impossible
  | cons path rest ih =>
      let e : ComposedExecution.Envelope := ⟨action, successor, actor.nonce + acc.2.length + 1, path⟩
      have generated : propose { actor with nonce := actor.nonce + acc.2.length } action path = some e := by
        simp only [propose, proposal, Option.map_some]
        rfl
      have bodyEq := batchBody_of_proposal actor action acc path e generated
      have static := batchBody_static actor action acc path
      have headValid : validPath acc.1 e = true :=
        decide_eq_true (wellformed path (by simp))
      cases landed : (serviceTrial acc.1 e actor.identity).2.landed with
      | true =>
          have more : landedCount acc.2 < landedCount (batchBody actor action acc path).2 := by
            rw [bodyEq, landedCount_append, landed]
            simp only [if_true]
            omega
          exact Nat.lt_of_lt_of_le more (fold_count_mono actor action rest _)
      | false =>
          have nextReady : ExactReady (batchBody actor action acc path).1 action successor actor.identity
              (actor.nonce + (batchBody actor action acc path).2.length) rest := by
            rw [batchBody_length, bodyEq]
            have remaining := rejected_trial_exactReady_tail acc.1 action successor actor.identity
              (actor.nonce + acc.2.length) path rest ready landed
            simpa only [Nat.add_assoc] using remaining
          have restIntact : ∃ selected ∈ rest,
              ∀ i ∈ selected, (batchBody actor action acc path).1.tainted i = false := by
            obtain ⟨selected, member, good⟩ := intact
            rcases List.mem_cons.mp member with same | tail
            · subst selected
              have yes := exactReady_head_lands acc.1 action successor actor.identity
                (actor.nonce + acc.2.length) path rest ready headValid good
              rw [landed] at yes
              cases yes
            · exact ⟨selected, tail, by simpa only [static.2.2.2.2.2] using good⟩
          have restWellformed : ∀ selected ∈ rest, selected.Nodup ∧
              selected.length = (batchBody actor action acc path).1.q ∧
              ∀ i ∈ selected, i < (batchBody actor action acc path).1.n := by
            intro selected member
            simpa only [static.1, static.2.1] using wellformed selected (by simp [member])
          have later := ih (batchBody actor action acc path) restWellformed nextReady restIntact
          have sameCount : landedCount (batchBody actor action acc path).2 = landedCount acc.2 := by
            rw [bodyEq, landedCount_append, landed]
            simp
          simpa only [List.foldl_cons, sameCount] using later

/-- Sharpened stable completion: only the four predicted complete envelopes
must be absent from good-root cancellation memories. Unrelated higher-nonce
tombstones are allowed. The world-side absence facts are explicit premises,
not actor observations and not a nonce-allocation implementation. -/
theorem runBatch_exact_fresh_completion (w : ComposedExecution.World) (actor : Actor)
    (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (roots : w.n = 4) (quorum : w.q = 3)
    (budget : ChargedInterlock.card 4 w.tainted ≤ 1)
    (ready : ExactReady w action successor actor.identity actor.nonce fourPaths) :
    landedCount (runBatch w actor action).2 = 1 ∧
      (runBatch w actor action).1.plant = successor := by
  have positive : 0 < landedCount (runBatch w actor action).2 := by
    rw [runBatch_eq_fold]
    apply fold_exact_progress actor action successor proposal fourPaths (w, [])
    · intro path member
      exact ⟨(fourPaths_bounded path member).1,
        by simpa only [quorum] using fourPaths_length path member,
        by simpa only [roots] using (fourPaths_bounded path member).2⟩
    · simpa only [List.length_nil, Nat.add_zero] using ready
    · exact fourPaths_has_intact w.tainted budget
  have atMost := runBatch_at_most_one_landing w actor action
  exact ⟨by omega, runBatch_successor_of_landing w actor action successor proposal positive⟩

theorem exact_four_predicted_envelopes (action : Action) (successor : Plant) (nonce : Nat) :
    trialEnvelopes action successor nonce fourPaths =
      [⟨action, successor, nonce + 1, [0,1,2]⟩,
       ⟨action, successor, nonce + 2, [0,1,3]⟩,
       ⟨action, successor, nonce + 3, [0,2,3]⟩,
       ⟨action, successor, nonce + 4, [1,2,3]⟩] := by
  simp only [trialEnvelopes, fourPaths, Nat.add_assoc]

#print axioms fold_exact_progress
#print axioms runBatch_exact_fresh_completion
#print axioms exact_four_predicted_envelopes
end
end OperationalJoin.Offset.Batch
