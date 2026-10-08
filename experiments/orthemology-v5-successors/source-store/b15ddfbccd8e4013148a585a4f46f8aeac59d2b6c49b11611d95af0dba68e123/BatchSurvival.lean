import BatchSurvivalModel

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

/-- Necessity is stronger than the eventual iff: it needs no synchronized
policy, fault-budget, or live-admission premise. Existing veto memory cannot
be erased by the actual preceding trial calls. -/
theorem fold_landing_has_surviving_trial (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (paths : List (List Nat)) (acc : ComposedExecution.World × List AttemptTrace)
    (noEarlier : landedCount acc.2 = 0)
    (positive : 0 < landedCount (paths.foldl (batchBody actor action) acc).2) :
    HasSurvivingTrial acc.1 action successor (actor.nonce + acc.2.length) paths := by
  induction paths generalizing acc with
  | nil => simp only [List.foldl_nil, noEarlier] at positive; omega
  | cons path rest ih =>
      let e : ComposedExecution.Envelope := ⟨action, successor, actor.nonce + acc.2.length + 1, path⟩
      have generated : propose { actor with nonce := actor.nonce + acc.2.length } action path = some e := by
        simp only [propose, proposal, Option.map_some]
        rfl
      have bodyEq := batchBody_of_proposal actor action acc path e generated
      cases landed : (serviceTrial acc.1 e actor.identity).2.landed with
      | true =>
          exact ⟨e, by simp [trialEnvelopes, e],
            landed_trial_was_intact_uncancelled acc.1 e actor.identity landed⟩
      | false =>
          have noHead : landedCount (batchBody actor action acc path).2 = 0 := by
            rw [bodyEq, landedCount_append, landed]
            simpa using noEarlier
          obtain ⟨other, member, survives⟩ := ih (batchBody actor action acc path) noHead positive
          refine ⟨other, ?_, ?_⟩
          · apply List.mem_cons.mpr
            right
            rw [batchBody_length] at member
            simpa only [Nat.add_assoc] using member
          · rw [bodyEq] at survives
            exact intact_uncancelled_before_trial acc.1 e other actor.identity survives

/-- A chosen witness here is a proof object. The source still runs all four
trials, and the actor receives neither this witness nor the taint/memory facts. -/
theorem fold_surviving_trial_progress (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (paths : List (List Nat)) (acc : ComposedExecution.World × List AttemptTrace)
    (wellformed : ∀ path ∈ paths, path.Nodup ∧ path.length = acc.1.q ∧ ∀ i ∈ path, i < acc.1.n)
    (ready : AdmissionReady acc.1 action successor actor.identity)
    (available : HasSurvivingTrial acc.1 action successor (actor.nonce + acc.2.length) paths) :
    landedCount acc.2 < landedCount (paths.foldl (batchBody actor action) acc).2 := by
  induction paths generalizing acc with
  | nil => obtain ⟨e, impossible, _⟩ := available; cases impossible
  | cons path rest ih =>
      let e : ComposedExecution.Envelope := ⟨action, successor, actor.nonce + acc.2.length + 1, path⟩
      have generated : propose { actor with nonce := actor.nonce + acc.2.length } action path = some e := by
        simp only [propose, proposal, Option.map_some]
        rfl
      have bodyEq := batchBody_of_proposal actor action acc path e generated
      have static := batchBody_static actor action acc path
      have valid : validPath acc.1 e = true := decide_eq_true (wellformed path (by simp))
      cases landed : (serviceTrial acc.1 e actor.identity).2.landed with
      | true =>
          have headMore : landedCount acc.2 < landedCount (batchBody actor action acc path).2 := by
            rw [bodyEq, landedCount_append, landed]
            simp only [if_true]
            omega
          exact Nat.lt_of_lt_of_le headMore (fold_count_mono actor action rest _)
      | false =>
          have remainingReady : AdmissionReady (batchBody actor action acc path).1 action successor actor.identity := by
            rw [bodyEq]
            exact rejected_trial_admission_ready acc.1 action successor actor.identity ready e landed
          have remainingAvailable : HasSurvivingTrial (batchBody actor action acc path).1 action successor
              (actor.nonce + (batchBody actor action acc path).2.length) rest := by
            obtain ⟨other, member, survives⟩ := available
            change other ∈ e :: trialEnvelopes action successor (actor.nonce + acc.2.length + 1) rest at member
            rcases List.mem_cons.mp member with same | tail
            · subst other
              have yes := intact_uncancelled_trial_lands acc.1 action successor actor.identity ready e rfl rfl valid survives
              rw [landed] at yes
              cases yes
            · have different : other ≠ e := by
                intro same
                have later := trialEnvelopes_nonce_gt action successor (actor.nonce + acc.2.length + 1) rest other tail
                rw [same] at later
                exact Nat.lt_irrefl _ later
              refine ⟨other, ?_, ?_⟩
              · rw [batchBody_length]
                simpa only [Nat.add_assoc] using tail
              · rw [bodyEq]
                exact intact_uncancelled_after_other_trial acc.1 e other actor.identity different survives
          have remainingWellformed : ∀ selected ∈ rest, selected.Nodup ∧
              selected.length = (batchBody actor action acc path).1.q ∧
              ∀ i ∈ selected, i < (batchBody actor action acc path).1.n := by
            intro selected member
            simpa only [static.1, static.2.1] using wellformed selected (by simp [member])
          have later := ih (batchBody actor action acc path) remainingWellformed remainingReady remainingAvailable
          have countEq : landedCount (batchBody actor action acc path).2 = landedCount acc.2 := by
            rw [bodyEq, landedCount_append, landed]
            simp
          simpa only [List.foldl_cons, countEq] using later

/-- Exact initial-state characterization for the literal withholding batch.
No fault-cardinality premise or actor-visible oracle is present. Stable full
policy/admission obligations are explicit; cancellation matters only for the
selected roots of at least one predicted complete envelope. -/
theorem runBatch_survival_iff (w : ComposedExecution.World) (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (roots : w.n = 4) (quorum : w.q = 3)
    (ready : AdmissionReady w action successor actor.identity) :
    landedCount (runBatch w actor action).2 = 1 ↔
      HasSurvivingTrial w action successor actor.nonce fourPaths := by
  constructor
  · intro one
    have positive : 0 < landedCount (runBatch w actor action).2 := by omega
    rw [runBatch_eq_fold] at positive
    exact fold_landing_has_surviving_trial actor action successor proposal fourPaths (w, []) rfl positive
  · intro available
    have positive : 0 < landedCount (runBatch w actor action).2 := by
      rw [runBatch_eq_fold]
      apply fold_surviving_trial_progress actor action successor proposal fourPaths (w, [])
      · intro path member
        exact ⟨(fourPaths_bounded path member).1,
          by simpa only [quorum] using fourPaths_length path member,
          by simpa only [roots] using (fourPaths_bounded path member).2⟩
      · exact ready
      · exact available
    have atMost := runBatch_at_most_one_landing w actor action
    omega

theorem runBatch_survival_effect_iff (w : ComposedExecution.World) (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (roots : w.n = 4) (quorum : w.q = 3)
    (ready : AdmissionReady w action successor actor.identity) :
    (landedCount (runBatch w actor action).2 = 1 ∧ (runBatch w actor action).1.plant = successor) ↔
      HasSurvivingTrial w action successor actor.nonce fourPaths := by
  constructor
  · intro success
    exact (runBatch_survival_iff w actor action successor proposal roots quorum ready).mp success.1
  · intro available
    have one := (runBatch_survival_iff w actor action successor proposal roots quorum ready).mpr available
    exact ⟨one, runBatch_successor_of_landing w actor action successor proposal (by omega)⟩

theorem runBatch_zero_iff_no_surviving_trial (w : ComposedExecution.World) (actor : Actor) (action : Action) (successor : Plant)
    (proposal : localStep actor.observedPlant actor.policy actor.observedTime action = some successor)
    (roots : w.n = 4) (quorum : w.q = 3)
    (ready : AdmissionReady w action successor actor.identity) :
    landedCount (runBatch w actor action).2 = 0 ↔
      ¬ HasSurvivingTrial w action successor actor.nonce fourPaths := by
  have exactOne := runBatch_survival_iff w actor action successor proposal roots quorum ready
  have atMost := runBatch_at_most_one_landing w actor action
  constructor
  · intro zero available
    have one := exactOne.mpr available
    omega
  · intro none
    have notOne : landedCount (runBatch w actor action).2 ≠ 1 := by
      intro one
      exact none (exactOne.mp one)
    omega

#print axioms fold_landing_has_surviving_trial
#print axioms fold_surviving_trial_progress
#print axioms runBatch_survival_iff
#print axioms runBatch_survival_effect_iff
#print axioms runBatch_zero_iff_no_surviving_trial
end
end OperationalJoin.Offset.Batch
