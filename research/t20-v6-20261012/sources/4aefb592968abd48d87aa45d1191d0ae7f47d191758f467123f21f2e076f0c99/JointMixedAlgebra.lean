import JointRegularity

namespace JointCompletion.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open SigmaCompletion RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Closed impredicative natural numbers are unchanged even by dependent type images. -/
theorem mixed_N (σ : Nat → Poly) (τ : Nat → Ty) : mixed σ τ N = N := rfl

/-- The old variables in the pair environment are exactly two slots deeper. -/
theorem pairSub_wk (A : Ty) : subst SigmaCompletion.pairSub (wk A) = wk (wk A) := by
  simp only [SigmaCompletion.pairSub, subst_wk_cancel, wk, subst_comp]
  rfl

/-- The branch-family square retains the two weakenings on every replacement type. -/
theorem branchType_mixed (P : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup (pup σ)) (fun n => wk (wk (τ n))) (branchType P) =
      branchType (mixed (pup σ) (fun n => wk (τ n)) P) := by
  simp only [branchType, mixed_subst, subst_mixed, pairSub_wk]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n => simp only [pairSub, pup, cons, psub, pren, psub_comp]

/-- Successor substitution fixes the weakened ambient type images. -/
theorem successorFamily_mixed (P : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup σ) (fun n => wk (τ n)) (successorFamily P) =
      successorFamily (mixed (pup σ) (fun n => wk (τ n)) P) := by
  simp only [successorFamily, mixed_subst, subst_mixed, subst_wk_cancel, subst_id]
  congr 1
  funext n
  cases n with
  | zero =>
    simp only [cons, pup, psub,
      P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)]
  | succ n => simp only [cons, pup, psub, pren, psub_comp]

/-- Full dependent mixed naturality of the induction step type. -/
theorem dependentStepType_mixed (P : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (dependentStepType P) =
      dependentStepType (mixed (pup σ) (fun n => wk (τ n)) P) := by
  simp only [dependentStepType, mixed, mixed_N, mixed_arr, successorFamily_mixed]

#print axioms mixed_N
#print axioms pairSub_wk
#print axioms branchType_mixed
#print axioms successorFamily_mixed
#print axioms dependentStepType_mixed
end JointCompletion.Structural
