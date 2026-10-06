import BatchTrial

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

def landedCount (records : List AttemptTrace) : Nat := (records.filter (·.landed)).length

def NoReplay (plant : Plant) (action : Action) : Prop :=
  ∀ policy time, localStep plant policy time action = none

/-- This invariant is for the literal withholding controller. It has no fault
budget, effective-policy, actor-authenticity, or synchronized-clock premise. -/
def UniqueBatchState (original : Plant) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) : Prop :=
  landedCount acc.2 ≤ 1 ∧
    (landedCount acc.2 = 0 → acc.1.plant = original) ∧
    (landedCount acc.2 = 1 → NoReplay acc.1.plant action)

theorem landedCount_append (records : List AttemptTrace) (record : AttemptTrace) :
    landedCount (records ++ [record]) = landedCount records + if record.landed then 1 else 0 := by
  cases bit : record.landed <;> simp [landedCount, List.filter_append, bit]

theorem batchBody_unique (actor : Actor) (action : Action) (original : Plant)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat)
    (nonempty : path ≠ []) (invariant : UniqueBatchState original action acc) :
    UniqueBatchState original action (batchBody actor action acc path) := by
  obtain ⟨atMost, unchanged, blocked⟩ := invariant
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none =>
      simpa only [UniqueBatchState, batchBody, proposal, landedCount_append,
        Bool.false_eq_true, if_false, Nat.add_zero] using And.intro atMost (And.intro unchanged blocked)
  | some e =>
      have fields := proposal_fields _ _ _ e proposal
      have eNonempty : e.path ≠ [] := by simpa only [fields.2.1] using nonempty
      rw [batchBody_of_proposal actor action acc path e proposal]
      change landedCount (acc.2 ++ [(serviceTrial acc.1 e actor.identity).2]) ≤ 1 ∧
        (landedCount (acc.2 ++ [(serviceTrial acc.1 e actor.identity).2]) = 0 →
          (serviceTrial acc.1 e actor.identity).1.plant = original) ∧
        (landedCount (acc.2 ++ [(serviceTrial acc.1 e actor.identity).2]) = 1 →
          NoReplay (serviceTrial acc.1 e actor.identity).1.plant action)
      rw [landedCount_append]
      cases landed : (serviceTrial acc.1 e actor.identity).2.landed with
      | false =>
          have plantEq : (serviceTrial acc.1 e actor.identity).1.plant = acc.1.plant := by
            rw [serviceTrial_plant, landed]
            rfl
          simpa only [Bool.false_eq_true, if_false, Nat.add_zero, plantEq] using
            And.intro atMost (And.intro unchanged blocked)
      | true =>
          have oldZero : landedCount acc.2 = 0 := by
            by_cases zero : landedCount acc.2 = 0
            · exact zero
            have oldOne : landedCount acc.2 = 1 := by omega
            have reject := (serviceTrial_no_relanding acc.1 e actor.identity eNonempty
              (by simpa only [fields.1] using blocked oldOne)).1
            rw [landed] at reject
            cases reject
          have plantEq : (serviceTrial acc.1 e actor.identity).1.plant = e.successor := by
            rw [serviceTrial_plant, landed]
            rfl
          obtain ⟨policy, step⟩ := serviceTrial_landing_witness acc.1 e actor.identity eNonempty landed
          simp only [oldZero, if_true, Nat.zero_add, Nat.le_refl, Nat.one_ne_zero, false_implies,
            true_and, plantEq]
          intro _ laterPolicy laterTime
          simpa only [fields.1] using fixed_action_cannot_succeed_twice acc.1.plant policy
            acc.1.now e.action e.successor step laterPolicy laterTime

theorem fold_unique (actor : Actor) (action : Action) (original : Plant)
    (paths : List (List Nat)) (nonempty : ∀ path ∈ paths, path ≠ [])
    (acc : ComposedExecution.World × List AttemptTrace)
    (invariant : UniqueBatchState original action acc) :
    UniqueBatchState original action (paths.foldl (batchBody actor action) acc) := by
  induction paths generalizing acc with
  | nil => exact invariant
  | cons path rest ih =>
      exact ih (by intro p hp; exact nonempty p (by simp [hp]))
        (batchBody actor action acc path)
        (batchBody_unique actor action original acc path (nonempty path (by simp)) invariant)

theorem runBatch_unique (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    UniqueBatchState w.plant action (runBatch w actor action) := by
  rw [runBatch_eq_fold]
  apply fold_unique actor action w.plant fourPaths
  · intro path member
    have length := fourPaths_length path member
    intro empty
    simp only [empty, List.length_nil] at length
    cases length
  · exact ⟨by change 0 ≤ 1; decide, by intro _; rfl, by intro impossible; cases impossible⟩

/-- The cardinality bound is unnecessary for uniqueness: faulty execution gates
always withhold in this exact controller. It will be needed for existence. -/
theorem runBatch_at_most_one_landing (w : ComposedExecution.World) (actor : Actor) (action : Action) :
    landedCount (runBatch w actor action).2 ≤ 1 :=
  (runBatch_unique w actor action).1

theorem runBatch_zero_landings_unchanged (w : ComposedExecution.World) (actor : Actor) (action : Action)
    (none : landedCount (runBatch w actor action).2 = 0) :
    (runBatch w actor action).1.plant = w.plant :=
  (runBatch_unique w actor action).2.1 none

theorem runBatch_one_landing_blocks_fixed_action (w : ComposedExecution.World)
    (actor : Actor) (action : Action) (one : landedCount (runBatch w actor action).2 = 1) :
    NoReplay (runBatch w actor action).1.plant action :=
  (runBatch_unique w actor action).2.2 one

#print axioms runBatch_at_most_one_landing
#print axioms runBatch_zero_landings_unchanged
#print axioms runBatch_one_landing_blocks_fixed_action
end
end OperationalJoin.Offset.Batch
