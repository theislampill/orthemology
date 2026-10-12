import DependentBranchApplication
import Constructive
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
namespace HasEDependentSubstitutionReview

theorem same_pair_substitution : Structural.pairSub = SigmaCompletion.pairSub := rfl

theorem same_branch_type (P : Ty) : Structural.branchType P = SigmaCompletion.branchType P := rfl

theorem same_branch_at (d a b : Poly) : Structural.branchAt d a b = SigmaCompletion.branchAt d a b := rfl

/-- The exact retained branch interface is strengthened to actual E everywhere. -/
theorem retained_branch_with_E {Γ : Tel} {A B P : Ty} {d a b : Poly}
    (hΓ : CtxE Γ) (hd : HasE (B :: A :: Γ) d (SigmaCompletion.branchType P))
    (ha : HasE Γ a A) (hb : HasE Γ b (inst B a)) :
    HasE Γ (SigmaCompletion.branchAt d a b) (inst P (pairPoly a b)) :=
  Structural.dependent_branch_substitution hΓ hd ha hb

#print axioms same_pair_substitution
#print axioms same_branch_type
#print axioms same_branch_at
#print axioms retained_branch_with_E
end HasEDependentSubstitutionReview
