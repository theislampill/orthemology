import DependentBranchApplication
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
namespace HasEDependentSubstitutionReview
/-- No author-defined alias appears in this exact external branch interface. -/
theorem literal_branch {Γ : Tel} {A B P : Ty} {d a b : Poly}
    (hΓ : CtxE Γ)
    (hd : HasE (B :: A :: Γ) d
      (subst (cons (pairPoly (.var 1) (.var 0)) (fun n => .var (n+2))) P))
    (ha : HasE Γ a A) (hb : HasE Γ b (inst B a)) :
    HasE Γ (psub (cons b (cons a Poly.var)) d) (inst P (pairPoly a b)) :=
  Structural.dependent_branch_substitution hΓ hd ha hb
#print axioms literal_branch
end HasEDependentSubstitutionReview
