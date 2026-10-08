import RuntimeCancellationControls

namespace BatchAvailabilityReview
noncomputable section
open Classical
open OperationalJoin OperationalJoin.Offset ComposedExecution NativeFixture
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

def undeliveredEvents : List (RuntimeEvent 4) :=
  [.prepare installEnvelope "A" false, .attempt installEnvelope "A" false,
   .certify 0 [1,2,3]]

/-- A genuine prefix of the accepted runtime witness, stopping before delivery. -/
theorem undelivered_runtime_prefix :
    RuntimeTrace authority start undeliveredEvents certified := by
  apply RuntimeTrace.cons (RuntimeStep.prepare start installEnvelope "A" false)
  apply RuntimeTrace.cons (RuntimeStep.attempt installPrepared installEnvelope "A" false)
  apply RuntimeTrace.cons (RuntimeStep.certify installedWorld 0 [1,2,3]
    (by decide) (by decide) rfl (by decide))
  exact RuntimeTrace.nil _

theorem certified_without_delivery_is_aligned_reachable :
    ∃ s, Aligned authority certified s ∧ Reachable authority.config s := by
  obtain ⟨s, events, aligned, history⟩ := runtime_trace_refines_history authority
    start_aligned start_reachable undelivered_runtime_prefix
  exact ⟨s, aligned, reachable_after start_reachable history⟩

/-- The fresh current repair is locally admissible under the actual effective
policy, but still cannot use roots whose authentic policies have not arrived.
Unlike the cancellation control, all good-root tombstone lists are empty. -/
theorem current_admission_and_freshness_do_not_replace_delivery :
    (∃ s, Aligned authority certified s ∧ Reachable authority.config s) ∧
    certified.plant = installed ∧ certified.effectivePolicy = source 1 ∧
    localStep installed (source 1) 2 (.repair (_root_.repairCommand sourceBytes)) = some repaired ∧
    (certified.roots 1).policy = source 0 ∧ (certified.roots 1).cancelled = [] ∧
    (certified.roots 2).cancelled = [] ∧ (certified.roots 3).cancelled = [] ∧
    (runBatch certified repairActor (.repair (_root_.repairCommand sourceBytes))).2.map
      AttemptTrace.prepared = [false,false,false,false] ∧
    (runBatch certified repairActor (.repair (_root_.repairCommand sourceBytes))).2.map
      AttemptTrace.landed = [false,false,false,false] ∧
    (runBatch certified repairActor (.repair (_root_.repairCommand sourceBytes))).1.plant = installed := by
  exact ⟨certified_without_delivery_is_aligned_reachable,
    by decide, by decide, repair_local, by decide, by decide, by decide,
    by decide, by decide, by decide, by decide⟩

#print axioms undelivered_runtime_prefix
#print axioms certified_without_delivery_is_aligned_reachable
#print axioms current_admission_and_freshness_do_not_replace_delivery
end
end BatchAvailabilityReview
