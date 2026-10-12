import JointTypedSubstitution

namespace JointCompletion.Structural
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01F (cons)
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Context inversion includes the retained old-E inclusion constructor. -/
theorem ctx_tail {Γ A} (h : CtxJ (A :: Γ)) : CtxJ Γ := by
  cases h with
  | ctxBase h => cases h with | ext hΓ _ => exact .ctxBase hΓ
  | ext hΓ _ => exact hΓ

theorem ctx_head {Γ A} (h : CtxJ (A :: Γ)) : FormJ Γ A := by
  cases h with
  | ctxBase h => cases h with | ext _ hA => exact .formBase hA
  | ext _ hA => exact hA

/-- The actual Joint telescope supplies formation for every dependent lookup. -/
theorem lookup_form {Γ n A} (hΓ : CtxJ Γ) (hn : Lookup Γ n A) : FormJ Γ A := by
  revert hΓ
  induction hn with
  | zero =>
      intro hΓ
      exact form_wk (ctx_head hΓ) (ctx_tail hΓ) (ctx_head hΓ)
  | succ hn ih =>
      intro hΓ
      exact form_wk (ih (ctx_tail hΓ)) (ctx_tail hΓ) (ctx_head hΓ)

/-- Images can have arbitrary Joint derivations, including newly completed ones. -/
theorem TypedSubstitution.instantiate {Γ A a} (hΓ : CtxJ Γ) (ha : HasJ Γ a A) :
    TypedSubstitution (A :: Γ) Γ (cons a Poly.var) := by
  constructor
  intro n B hn
  cases hn with
  | zero => simpa only [subst_wk_cancel, subst_id, cons] using ha
  | succ hn =>
      simpa only [subst_wk_cancel, subst_id, cons] using
        HasJ.var (lookup_form hΓ hn) hn

theorem form_inst {Γ A B a} (hΓ : CtxJ Γ) (hB : FormJ (A :: Γ) B)
    (ha : HasJ Γ a A) : FormJ Γ (inst B a) :=
  form_subst hB hΓ (TypedSubstitution.instantiate hΓ ha)

theorem has_inst {Γ A B a b} (hΓ : CtxJ Γ) (hb : HasJ (A :: Γ) b B)
    (ha : HasJ Γ a A) : HasJ Γ (psub (cons a Poly.var) b) (inst B a) :=
  has_subst hb hΓ (TypedSubstitution.instantiate hΓ ha)

/-- Syntactic regularity for the frozen Joint grammar. No semantic reflection is used. -/
theorem has_form {Γ p A} (h : HasJ Γ p A) : FormJ Γ A := by
  cases h with
  | hasBase h => exact .formBase (P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed h)
  | sigmaElim hΓ hA hB hP hd hz => exact form_inst hΓ hP hz
  | natInduction hΓ hP hp hs => exact .pi (form_nat hΓ) hP
  | _ => assumption

theorem has_ctx {Γ p A} (h : HasJ Γ p A) : CtxJ Γ := form_ctx (has_form h)

theorem has_type_scoped {Γ p A} (h : HasJ Γ p A) : TyScoped Γ.length A :=
  form_scoped (has_form h)

/-- The exact Sigma-elimination result type is formed for every recursive Joint motive
and Joint-typed input, without assuming an old-HasE preimage. -/
theorem sigma_result_formed {Γ A B P z} (hΓ : CtxJ Γ)
    (hP : FormJ (.sigma A B :: Γ) P) (hz : HasJ Γ z (.sigma A B)) :
    FormJ Γ (inst P z) := form_inst hΓ hP hz

/-- The induction result's syntactic formation is independent of semantics. -/
theorem induction_result_formed {Γ P} (hΓ : CtxJ Γ)
    (hP : FormJ (P01AC.EffectiveCompleteness.N :: Γ) P) :
    FormJ Γ (.pi P01AC.EffectiveCompleteness.N P) := .pi (form_nat hΓ) hP

#print axioms lookup_form
#print axioms TypedSubstitution.instantiate
#print axioms form_inst
#print axioms has_inst
#print axioms has_form
#print axioms has_ctx
#print axioms has_type_scoped
#print axioms sigma_result_formed
#print axioms induction_result_formed
end JointCompletion.Structural
