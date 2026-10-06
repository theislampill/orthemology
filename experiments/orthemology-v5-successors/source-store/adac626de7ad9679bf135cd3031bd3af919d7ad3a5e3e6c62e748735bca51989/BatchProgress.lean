import BatchReadiness
import BatchUniqueness

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

theorem batchBody_static (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat) :
    (batchBody actor action acc path).1.n = acc.1.n ∧
    (batchBody actor action acc path).1.q = acc.1.q ∧
    (batchBody actor action acc path).1.budget = acc.1.budget ∧
    (batchBody actor action acc path).1.now = acc.1.now ∧
    (batchBody actor action acc path).1.effectivePolicy = acc.1.effectivePolicy ∧
    (batchBody actor action acc path).1.tainted = acc.1.tainted := by
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none => simp [batchBody, proposal]
  | some e =>
      rw [batchBody_of_proposal actor action acc path e proposal]
      exact serviceTrial_static acc.1 e actor.identity

theorem batchBody_count_mono (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat) :
    landedCount acc.2 ≤ landedCount (batchBody actor action acc path).2 := by
  obtain ⟨record, records, _, _⟩ := batchBody_record actor action acc path
  rw [records, landedCount_append]
  omega

theorem fold_count_mono (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace) :
    landedCount acc.2 ≤ landedCount (paths.foldl (batchBody actor action) acc).2 := by
  induction paths generalizing acc with
  | nil => exact Nat.le_refl _
  | cons path rest ih =>
      exact Nat.le_trans (batchBody_count_mono actor action acc path) (ih _)

/-- The intact path is needed only in the proof, never supplied to the actor.
Any preceding trials that did not land retain the ready-state obligations at
the incremented cancellation high-water mark. -/
theorem fold_progress (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (paths : List (List Nat)) (acc : ComposedExecution.World × List AttemptTrace)
    (wellformed : ∀ path ∈ paths, path.Nodup ∧ path.length = acc.1.q ∧ ∀ i ∈ path, i < acc.1.n)
    (ready : ReadyFor acc.1 action successor actor.identity (actor.nonce + acc.2.length))
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
          have nextReady : ReadyFor (batchBody actor action acc path).1 action successor actor.identity
              (actor.nonce + (batchBody actor action acc path).2.length) := by
            rw [batchBody_length, bodyEq]
            apply rejected_serviceTrial_ready acc.1 action successor actor.identity
              (actor.nonce + acc.2.length) ready e landed
            · omega
            · dsimp [e]; omega
          have restIntact : ∃ selected ∈ rest,
              ∀ i ∈ selected, (batchBody actor action acc path).1.tainted i = false := by
            obtain ⟨selected, member, good⟩ := intact
            rcases List.mem_cons.mp member with same | tail
            · subst selected
              have yes := ready_intact_trial_lands acc.1 action successor actor.identity
                (actor.nonce + acc.2.length) ready e rfl rfl (by dsimp [e]; omega) headValid good
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

/-- This is a finite counting fact about the portfolio. The controller itself
always follows the same four paths and receives no taint information. -/
theorem fourPaths_has_intact (tainted : Nat → Bool)
    (budget : ChargedInterlock.card 4 tainted ≤ 1) :
    ∃ path ∈ fourPaths, ∀ i ∈ path, tainted i = false := by
  cases h0 : tainted 0 <;> cases h1 : tainted 1 <;>
    cases h2 : tainted 2 <;> cases h3 : tainted 3 <;>
    simp only [ChargedInterlock.card, h0, h1, h2, h3, Bool.false_eq_true, if_false, if_true] at budget
  all_goals solve
    | omega
    | (refine ⟨[0,1,2], by simp [fourPaths], ?_⟩; simp [h0, h1, h2])
    | (refine ⟨[0,1,3], by simp [fourPaths], ?_⟩; simp [h0, h1, h3])
    | (refine ⟨[0,2,3], by simp [fourPaths], ?_⟩; simp [h0, h2, h3])
    | (refine ⟨[1,2,3], by simp [fourPaths], ?_⟩; simp [h1, h2, h3])

/-- Bounded stable-state completion for the unchanged four-trial source.
Both the actor-observed proposal and actual current source admission must hold.
Good root policies and unrevoked epochs are explicit; initial complete-envelope
cancellation memory must lie below the actor's stated nonce high-water mark. -/
theorem runBatch_exactly_one_landing (w : ComposedExecution.World) (actor : Actor)
    (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (roots : w.n = 4) (quorum : w.q = 3)
    (budget : ChargedInterlock.card 4 w.tainted ≤ 1)
    (ready : ReadyFor w action successor actor.identity actor.nonce) :
    landedCount (runBatch w actor action).2 = 1 := by
  have positive : 0 < landedCount (runBatch w actor action).2 := by
    rw [runBatch_eq_fold]
    apply fold_progress actor action successor proposal fourPaths (w, [])
    · intro path member
      exact ⟨(fourPaths_bounded path member).1,
        by simpa only [quorum] using fourPaths_length path member,
        by simpa only [roots] using (fourPaths_bounded path member).2⟩
    · simpa only [List.length_nil, Nat.add_zero] using ready
    · exact fourPaths_has_intact w.tainted budget
  have atMost := runBatch_at_most_one_landing w actor action
  omega

/-- Every admitted proposal in this batch has the same complete successor.
The actor is not refreshed from an effect receipt between trials. -/
theorem fold_positive_plant (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (paths : List (List Nat)) (acc : ComposedExecution.World × List AttemptTrace)
    (prior : 0 < landedCount acc.2 → acc.1.plant = successor) :
    0 < landedCount (paths.foldl (batchBody actor action) acc).2 →
      (paths.foldl (batchBody actor action) acc).1.plant = successor := by
  induction paths generalizing acc with
  | nil => exact prior
  | cons path rest ih =>
      apply ih
      let e : ComposedExecution.Envelope := ⟨action, successor, actor.nonce + acc.2.length + 1, path⟩
      have generated : propose { actor with nonce := actor.nonce + acc.2.length } action path = some e := by
        simp only [propose, proposal, Option.map_some]
        rfl
      rw [batchBody_of_proposal actor action acc path e generated]
      intro positive
      rw [landedCount_append] at positive
      rw [serviceTrial_plant]
      cases landed : (serviceTrial acc.1 e actor.identity).2.landed with
      | true => rfl
      | false =>
          simp only [landed, Bool.false_eq_true, if_false, Nat.add_zero] at positive
          exact prior positive

theorem runBatch_successor_of_landing (w : ComposedExecution.World) (actor : Actor)
    (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (positive : 0 < landedCount (runBatch w actor action).2) :
    (runBatch w actor action).1.plant = successor := by
  rw [runBatch_eq_fold] at positive ⊢
  apply fold_positive_plant actor action successor proposal fourPaths (w, []) ?_ positive
  intro impossible
  change 0 < 0 at impossible
  omega

/-- The complete exact successor, including versions and audit histories, is
reached once under the explicit stable readiness conditions. This is bounded
logical completion, not a physical service-time or clock-authenticity theorem. -/
theorem runBatch_stable_completion (w : ComposedExecution.World) (actor : Actor)
    (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (roots : w.n = 4) (quorum : w.q = 3)
    (budget : ChargedInterlock.card 4 w.tainted ≤ 1)
    (ready : ReadyFor w action successor actor.identity actor.nonce) :
    landedCount (runBatch w actor action).2 = 1 ∧
      (runBatch w actor action).1.plant = successor := by
  have once := runBatch_exactly_one_landing w actor action successor proposal roots quorum budget ready
  exact ⟨once, runBatch_successor_of_landing w actor action successor proposal (by omega)⟩

#print axioms fold_progress
#print axioms fourPaths_has_intact
#print axioms runBatch_exactly_one_landing
#print axioms runBatch_stable_completion
end
end OperationalJoin.Offset.Batch
