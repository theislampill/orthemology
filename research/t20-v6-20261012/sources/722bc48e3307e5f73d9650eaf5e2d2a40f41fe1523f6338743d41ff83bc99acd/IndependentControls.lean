import HasEDependentSubstitution
namespace HasEDependentSubstitutionReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Lookup formation is derived in actual E contexts, without original Ctx/Form. -/
theorem lookup_formed {Γ : Tel} {n : Nat} {A : Ty}
    (hΓ : CtxE Γ) (hn : Lookup Γ n A) : FormE Γ A := by
  induction hn with
  | zero =>
    cases hΓ with
    | ext hc ha => exact Structural.form_wk ha hc ha
  | succ hn ih =>
    cases hΓ with
    | ext hc hb => exact Structural.form_wk (ih hc) hc hb

/-- The replacement is arbitrary HasE evidence, including E-only derivations. -/
theorem single_map {Γ : Tel} {A : Ty} {a : Poly}
    (hΓ : CtxE Γ) (ha : HasE Γ a A) :
    Structural.TypedSubstitution (A :: Γ) Γ (cons a Poly.var) := by
  constructor
  intro n B hn
  cases hn with
  | zero => simpa only [subst_wk_cancel, subst_id, cons] using ha
  | succ hn =>
    simpa only [subst_wk_cancel, subst_id, cons] using
      HasE.var (lookup_formed hΓ hn) hn

/-- Exact top substitution, with an arbitrary E branch and arbitrary E argument. -/
theorem single_has {Γ : Tel} {A B : Ty} {a b : Poly}
    (hΓ : CtxE Γ) (ha : HasE Γ a A) (hb : HasE (A :: Γ) b B) :
    HasE Γ (psub (cons a Poly.var) b) (inst B a) :=
  Structural.has_subst hb hΓ (single_map hΓ ha)

theorem single_form {Γ : Tel} {A B : Ty} {a : Poly}
    (hΓ : CtxE Γ) (ha : HasE Γ a A) (hB : FormE (A :: Γ) B) :
    FormE Γ (inst B a) :=
  Structural.form_subst hB hΓ (single_map hΓ ha)

/-- The dependent identity endpoint changes with the substituted arbitrary image. -/
theorem dependent_endpoint {Γ : Tel} {A : Ty} {a b : Poly}
    (hΓ : CtxE Γ) (ha : HasE Γ a A)
    (hb : HasE (A :: Γ) b (.identity (wk A) (.var 0) (.var 0))) :
    HasE Γ (psub (cons a Poly.var) b) (.identity A a a) := by
  simpa only [inst, subst, subst_wk_cancel, subst_id, psub, cons] using
    single_has hΓ ha hb

/-- Composition checks that simultaneous dependent lookup types really compose. -/
theorem maps_compose {Γ Δ Ξ : Tel} {σ τ : Nat → Poly}
    (hΞ : CtxE Ξ) (hσ : Structural.TypedSubstitution Γ Δ σ)
    (hτ : Structural.TypedSubstitution Δ Ξ τ) :
    Structural.TypedSubstitution Γ Ξ (fun n => psub τ (σ n)) := by
  constructor
  intro n A hn
  simpa only [subst_comp] using Structural.has_subst (hσ.lookup hn) hΞ hτ

/-- Binder lifting retains arbitrary E-typed images at dependent shifted types. -/
theorem term_lift {Γ Δ : Tel} {σ : Nat → Poly} {A B : Ty} {b : Poly}
    (hΔ : CtxE Δ) (hσ : Structural.TypedSubstitution Γ Δ σ)
    (hA : FormE Δ (subst σ A)) (hb : HasE (A :: Γ) b B) :
    HasE (subst σ A :: Δ) (psub (pup σ) b) (subst (pup σ) B) :=
  Structural.has_subst hb (.ext hΔ hA) (hσ.lift hΔ hA)

/-- All's binder changes type parameters but leaves term substitution images alone. -/
theorem type_lift {Γ Δ : Tel} {σ : Nat → Poly} {B : Ty} {b : Poly}
    (hΔ : CtxE Δ) (hσ : Structural.TypedSubstitution Γ Δ σ)
    (hb : HasE (twkTel Γ) b B) :
    HasE (twkTel Δ) (psub σ b) (subst σ B) :=
  Structural.has_subst hb (Structural.ctx_twk hΔ) hσ.twk

#print axioms single_has
#print axioms single_form
#print axioms dependent_endpoint
#print axioms maps_compose
#print axioms term_lift
#print axioms type_lift
end HasEDependentSubstitutionReview
