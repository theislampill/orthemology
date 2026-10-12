import DependentBranchApplication
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
example {Γ : Tel} {A B P : Ty} {d a b : Poly}
    (hΓ : CtxE Γ) (hd : HasE (B :: A :: Γ) d (Structural.branchType P))
    (ha : HasE Γ a A) (hb : HasE Γ b B) :
    HasE Γ (Structural.branchAt d a b) (inst P (pairPoly a b)) :=
  Structural.dependent_branch_substitution hΓ hd ha hb
