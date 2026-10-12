import HasEDependentSubstitution

namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Actual-E context formation supplies the declaration types needed by maps. -/
theorem lookup_form {Γ : Tel} {n : Nat} {A : Ty} (hΓ : CtxE Γ)
    (h : Lookup Γ n A) : FormE Γ A := by
  induction h with
  | zero =>
      cases hΓ with
      | ext hΓ hA => exact form_wk hA hΓ hA
  | succ h ih =>
      cases hΓ with
      | ext hΓ hB => exact form_wk (ih hΓ) hΓ hB

theorem TypedSubstitution.single {Γ : Tel} {A : Ty} {a : Poly}
    (hΓ : CtxE Γ) (ha : HasE Γ a A) :
    TypedSubstitution (A :: Γ) Γ (cons a Poly.var) := by
  constructor
  intro n B h
  cases h with
  | zero => simpa only [subst_wk_cancel, subst_id, cons] using ha
  | succ h => simpa only [subst_wk_cancel, subst_id, cons] using
      (HasE.var (lookup_form hΓ h) h)

/-- Formation under an actual HasE endpoint, not just an original-Has one. -/
theorem form_inst {Γ : Tel} {A B : Ty} {a : Poly}
    (hΓ : CtxE Γ) (hB : FormE (A :: Γ) B) (ha : HasE Γ a A) : FormE Γ (inst B a) :=
  form_subst hB hΓ (TypedSubstitution.single hΓ ha)

/-- Literal dependent beta substitution, including an actual-E branch. -/
theorem has_inst {Γ : Tel} {A B : Ty} {d a : Poly}
    (hΓ : CtxE Γ) (hd : HasE (A :: Γ) d B) (ha : HasE Γ a A) :
    HasE Γ (psub (cons a Poly.var) d) (inst B a) :=
  has_subst hd hΓ (TypedSubstitution.single hΓ ha)

/-- A two-component dependent substitution admits actual HasE data at both
    components; the second component's type depends on the first. -/
theorem TypedSubstitution.pair {Γ : Tel} {A B : Ty} {a b : Poly}
    (hΓ : CtxE Γ) (ha : HasE Γ a A) (hb : HasE Γ b (inst B a)) :
    TypedSubstitution (B :: A :: Γ) Γ (cons b (cons a Poly.var)) := by
  constructor
  intro n C h
  cases h with
  | zero => simpa only [subst_wk_cancel, cons] using hb
  | succ h =>
      cases h with
      | zero => simpa only [subst_wk_cancel, subst_id, cons] using ha
      | succ h => simpa only [subst_wk_cancel, subst_id, cons] using
          (HasE.var (lookup_form hΓ h) h)

/-- The same literal pair substitution used by the retained Sigma-elimination
    theorem; this module upgrades its branch typing without adding Sigma eta. -/
def pairSub : Nat → Poly := cons (pairPoly (.var 1) (.var 0)) (fun n => .var (n+2))
def branchType (P : Ty) : Ty := subst pairSub P
def branchAt (d a b : Poly) : Poly := psub (cons b (cons a Poly.var)) d

theorem branch_type_at (P : Ty) (a b : Poly) :
    subst (cons b (cons a Poly.var)) (branchType P) = inst P (pairPoly a b) := by
  rw [branchType, subst_comp]
  congr 1
  funext n
  cases n <;> rfl

/-- Full actual-HasE version of the previously original-Has-only dependent
    Sigma branch-substitution lemma. Context, branch, and endpoints are E. -/
theorem dependent_branch_substitution {Γ : Tel} {A B P : Ty} {d a b : Poly}
    (hΓ : CtxE Γ) (hd : HasE (B :: A :: Γ) d (branchType P))
    (ha : HasE Γ a A) (hb : HasE Γ b (inst B a)) :
    HasE Γ (branchAt d a b) (inst P (pairPoly a b)) := by
  have q := has_subst hd hΓ (TypedSubstitution.pair hΓ ha hb)
  simpa only [branchAt, branch_type_at] using q

#print axioms form_inst
#print axioms has_inst
#print axioms dependent_branch_substitution
end P01AC.ExtensionalRepair.Structural
