import BatchSurvival
import BatchAvailabilityIffSourceChallenges

namespace BatchSurvivalContractReview
noncomputable section
open Classical
open ComposedExecution OperationalJoin OperationalJoin.Offset
open Batch BatchSourceReview BatchAvailabilityIffSourceReview
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- Independent type check of the exact initial-state iff: no cardinal fault
bound, global high-water mark or all-four freshness argument is supplied. -/
theorem exact_iff_has_only_declared_stable_obligations
    (world : World) (who : Actor) (action : Action) (next : Plant)
    (proposal : localStep who.observedPlant who.policy who.observedTime action = some next)
    (roots : world.n = 4) (quorum : world.q = 3)
    (ready : AdmissionReady world action next who.identity) :
    (landedCount (runBatch world who action).2 = 1 ∧
      (runBatch world who action).1.plant = next) ↔
      HasSurvivingTrial world action next who.nonce fourPaths :=
  runBatch_survival_effect_iff world who action next proposal roots quorum ready

/-- The necessary direction really needs neither actual admission nor policy
synchronization nor even an explicit world cardinality/quorum premise. -/
theorem successful_batch_necessity_has_no_extra_readiness_premise
    (world : World) (who : Actor) (action : Action) (next : Plant)
    (proposal : localStep who.observedPlant who.policy who.observedTime action = some next)
    (positive : 0 < landedCount (runBatch world who action).2) :
    HasSurvivingTrial world action next who.nonce fourPaths := by
  rw [runBatch_eq_fold] at positive
  exact fold_landing_has_surviving_trial who action next proposal fourPaths (world, []) rfl positive

theorem false_singleton_cleanup_can_eliminate_every_surviving_trial :
    AdmissionReady c4 a successor actor.identity ∧
    ¬HasSurvivingTrial c4 a successor actor.nonce fourPaths ∧
    landedCount (runBatch c4 actor a).2 = 0 := by
  have ready : AdmissionReady c4 a successor actor.identity := by
    refine ⟨rfl, source_admits, ?_⟩
    intro i bound good
    change i < 4 at bound
    have finite : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 := by omega
    rcases finite with rfl | rfl | rfl | rfl <;> decide
  have none : ¬HasSurvivingTrial c4 a successor actor.nonce fourPaths := by
    rintro ⟨e, member, available⟩
    rw [exact_four_predicted_envelopes] at member
    simp only [List.mem_cons, List.not_mem_nil, or_false] at member
    rcases member with rfl | rfl | rfl | rfl
    · exact (available 0 (by decide)).2 (by decide)
    · exact (available 0 (by decide)).2 (by decide)
    · exact (available 0 (by decide)).2 (by decide)
    · exact (available 1 (by decide)).2 (by decide)
  exact ⟨ready, none, (runBatch_zero_iff_no_surviving_trial c4 actor a successor
    source_admits rfl rfl ready).mpr none⟩

theorem numerical_cleanup_budget_does_not_enter_the_effect_iff :
    landedCount (runBatch { w [] with budget := 7 } actor a).2 = 1 ∧
    (runBatch { w [] with budget := 7 } actor a).1.plant = successor ∧
    (runBatch { w [] with budget := 7 } actor a).2.map AttemptTrace.closed =
      [false,false,false,false] := by
  have ready : AdmissionReady { w [] with budget := 7 } a successor actor.identity := by
    refine ⟨rfl, source_admits, ?_⟩
    intro i bound good
    exact ⟨rfl, by simp [w, initialWorld]⟩
  have available : HasSurvivingTrial { w [] with budget := 7 } a successor actor.nonce fourPaths := by
    refine ⟨first, ?_, ?_⟩
    · rw [exact_four_predicted_envelopes]
      simp [first, actor]
    · unfold IntactUncancelled
      decide
  have completed := (runBatch_survival_effect_iff { w [] with budget := 7 }
    actor a successor source_admits rfl rfl ready).mpr available
  exact ⟨completed.1, completed.2, by decide⟩

def rejectedActor : Actor := { actor with observedTime := 90 }

/-- Even actual live admission plus an intact uncancelled path is insufficient
without the separate actor-observed proposal-admission hypothesis. -/
theorem rejecting_actor_stalls_despite_actual_ready_surviving_path :
    AdmissionReady (w [0]) a successor rejectedActor.identity ∧
    HasSurvivingTrial (w [0]) a successor rejectedActor.nonce fourPaths ∧
    localStep rejectedActor.observedPlant rejectedActor.policy rejectedActor.observedTime a = none ∧
    landedCount (runBatch (w [0]) rejectedActor a).2 = 0 := by
  refine ⟨?_, ?_, by decide, by decide⟩
  · refine ⟨rfl, source_admits, ?_⟩
    intro i bound good
    exact ⟨rfl, by simp [w, initialWorld]⟩
  · refine ⟨fourth, ?_, ?_⟩
    · rw [exact_four_predicted_envelopes]
      simp [fourth, rejectedActor, actor]
    · unfold IntactUncancelled
      decide

#print axioms exact_iff_has_only_declared_stable_obligations
#print axioms successful_batch_necessity_has_no_extra_readiness_premise
#print axioms false_singleton_cleanup_can_eliminate_every_surviving_trial
#print axioms numerical_cleanup_budget_does_not_enter_the_effect_iff
#print axioms rejecting_actor_stalls_despite_actual_ready_surviving_path
end
end BatchSurvivalContractReview
