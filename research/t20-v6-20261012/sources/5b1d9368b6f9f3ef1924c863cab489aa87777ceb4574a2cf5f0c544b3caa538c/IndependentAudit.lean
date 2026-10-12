import ResetContinuation
import Checks

#print axioms ResetContinuation.essential_determines
#print axioms ResetContinuation.contextWord_realizes
#print axioms ResetContinuation.expose_essential
#print axioms ResetContinuation.closure_distinguishes
#print axioms ResetContinuation.closure_output
#print axioms ResetContinuation.closure_step
#print axioms ResetContinuation.agreement_continuation
#print axioms ResetContinuation.closure_least
#print axioms ResetContinuation.project_fill
#print axioms ResetContinuation.summary_eq_continuation

-- This typed restatement binds both independently defined source relations.
example {n : Nat} {O A : Type}
    (h : (Fin n → Bool) → O)
    (T : A → (Fin n → Bool) → (Fin n → Bool))
    (x y : Fin n → Bool) :
    (∀ word : List (ResetContinuation.Action (Fin n) A),
      h (ResetContinuation.run T word x) = h (ResetContinuation.run T word y)) ↔
    (∀ i, (∃ d, ResetContinuation.Stage h T d i) → x i = y i) := by
  change ResetContinuation.ContinuationEq h T x y ↔ _
  rw [ResetContinuation.fin_continuation_iff_agreement]
  constructor
  · intro ha i hi
    exact ha i ((ResetContinuation.closure_iff_stage h T i).mpr hi)
  · intro ha i hi
    exact ha i ((ResetContinuation.closure_iff_stage h T i).mp hi)
