import BatchSourceChallenges

namespace BatchFaultSemanticsReview
open ComposedExecution BatchSourceReview
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- Without the fault budget, permissive faulty execution can report repeated
landings of the same fixed action, even after a true cancellation reply. This
does not describe runBatch, which hard-codes faulty execution to withhold. -/
theorem budget_free_uniqueness_does_not_generalize_to_permissive_faults :
    let prepared := (prepare (w [0,1,2,3]) first "A" true).1
    let landed := attempt prepared first "A" true
    let closed := cancelWith landed.1 first "A" first.path
    landed.2 = true ∧ closed.2 = true ∧
    (attempt closed.1 first "A" true).2 = true ∧
    (closed.1.roots 1).cancelled = [] ∧
    (runBatch (w [0,1,2,3]) actor a).2.map AttemptTrace.landed =
      [false,false,false,false] := by decide

#print axioms budget_free_uniqueness_does_not_generalize_to_permissive_faults
end BatchFaultSemanticsReview
