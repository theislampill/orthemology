import InductionRigidityConverse
namespace IndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open SourceRigidity RigidityInitiality RigidityInitiality.FullE
open RigidityInitiality.FullE.InductionConverse
example : WeakInduction ↔ (∃ r : Poly, HasE [] r SourceRigidity.Rigidity) :=
  weak_induction_iff_closed_rigidity
example : (∀ Γ, CtxE Γ → ∀ (P : Ty) (p s : Poly), FormE (N :: Γ) P →
  HasE Γ p (inst P zero) → HasE Γ s (dependentStepType P) →
  ∃ t, HasE Γ t (.pi N P)) ↔ ∃ r, HasE [] r Rigidity :=
  weak_induction_iff_closed_rigidity
example (hi : WeakInductionAt [StepAt (.var 1), ZeroAt (.var 0), NT]) :
  HasE [] (abstract (abstract (abstract ident))) Rigidity :=
  generic_induction_implies_closed_rigidity hi
example (Γ : Tel) (hc : CtxE Γ) :
  (∀ Δ, CtxE (Δ ++ Γ) → WeakInductionAt (Δ ++ Γ)) ↔ ∃ r, HasE Γ r Rigidity :=
  contextual_weak_induction_iff_rigidity hc
example : ¬ WeakInductionAt GenericContext := generic_induction_not_admissible
example : ¬ WeakInduction := weak_induction_not_admissible
example (u n : Poly) : inst (EqFamily u) n = .identity N (.app u n) n := family_at u n
#print axioms nat_congr
#print axioms family_step
#print axioms endomorphism_rigid
#print axioms extended_induction_implies_rigidity
#print axioms generic_induction_implies_closed_rigidity
#print axioms weak_induction_iff_closed_rigidity
#print axioms weak_induction_iff_generic_context
#print axioms contextual_weak_induction_iff_rigidity
#print axioms weak_induction_not_admissible
#print axioms generic_induction_not_admissible
end IndependentReview
