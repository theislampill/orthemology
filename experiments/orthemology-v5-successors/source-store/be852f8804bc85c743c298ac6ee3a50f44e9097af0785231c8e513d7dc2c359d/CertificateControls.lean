import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.UnaryIdentity
open P01AC.UnaryCertificate
namespace CertificateControls

-- The new rule has explicit formation and a finite computational guard.
example (Γ : Tel) (e f : Expr) (c : Certificate)
    (hf : FormC Γ (.identity (arr N N) e.closed f.closed))
    (hc : verifyCertificate e f c = true) :
    HasC Γ (.atom .i) (.identity (arr N N) e.closed f.closed) := .certified e f c hf hc

-- Every inherited current judgement still embeds.
example {Γ p A} (h : P01AC.Has Γ p A) : HasC Γ p A := has_inclusion h
example {Γ A} (h : P01AC.Form Γ A) : FormC Γ A := form_inclusion h
example {Γ} (h : P01AC.Ctx Γ) : CtxC Γ := ctx_inclusion h

-- Full soundness retains context compatibility and arbitrary proof terms.
example {Γ p A} (h : HasC Γ p A) (R : REnv) (η ξ : Env) (hc : H Γ R η ξ) :
    G A R η ξ (eval p η) (eval p ξ) := P01AC.UnaryCertificate.fundamental h R η ξ hc
example {Γ p A} (h : HasC Γ p A) (ρ : OEnv) (η ξ : Env) (hc : E Γ ρ η ξ) :
    F A ρ η (eval p η) (eval p ξ) := P01AC.UnaryCertificate.unary_fundamental h hc

-- This stronger arbitrary-valuation result is specific to the closed compiled identity.
example (e f : Expr) (c : Certificate) (hc : verifyCertificate e f c = true)
    (R : REnv) :
    G (.identity (arr N N) e.closed f.closed) R (fun _ => .k) (fun _ => .s) .i .i :=
  certificate_all_valuations e f c hc R _ _

example (e f : Expr) (r : Poly)
    (h : HasC [] r (.identity (arr N N) e.closed f.closed)) : identityCheck e f = true :=
  (fragment_witness_iff_check e f).mp ⟨r,h⟩
example (e f : Expr) :
    (∃ r, HasC [] r (.identity (arr N N) e.closed f.closed)) ↔
      ∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv .i .i :=
  fragment_witness_iff_G_identity e f

example : HasC [] (.atom .i) (.identity (arr N N)
    IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) :=
  strict_current_extension.1
example : ¬ ∃ r, P01AC.Has [] r (.identity (arr N N)
    IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) :=
  strict_current_extension.2
example : HasC [] (jPoly (.atom .i) IntensionalBoundary.redundantExpr.closed (.atom .i)) .raw :=
  j_checked_identity_raw _ _ IntensionalBoundary.checker_accepts
example : HasC [] (.atom .i) .raw := erase_checked_identity _ _ IntensionalBoundary.checker_accepts

-- Exact generic dependent-J interface, including every formation and typing premise.
example {Γ A B x y e d}
    (hA : FormC Γ A) (hB : FormC (theta Γ A x) B)
    (hId : FormC Γ (.identity A x y))
    (hBase : FormC Γ (motiveAt B x (.atom .i)))
    (hTarget : FormC Γ (motiveAt B y e))
    (hx : HasC Γ x A) (hy : HasC Γ y A)
    (he : HasC Γ e (.identity A x y)) (hd : HasC Γ d (motiveAt B x (.atom .i))) :
    HasC Γ (jPoly d y e) (motiveAt B y e) :=
  .j hA hB hId hBase hTarget hx hy he hd

-- Empty-context completeness cannot be strengthened to arbitrary assumptions.
def zeroExpr : Expr := .constant 0
def oneExpr : Expr := .constant 1
def unequalIdentity : Ty := .identity (arr N N) zeroExpr.closed oneExpr.closed

theorem unequal_identity_subst (σ : Nat → Poly) : subst σ unequalIdentity = unequalIdentity := by
  simp only [unequalIdentity, subst, subst_arr, N_subst,
    psub_closed (has_scoped zeroExpr.closed_has), psub_closed (has_scoped oneExpr.closed_has)]

theorem assumption_context_control :
    HasC [unequalIdentity] (.var 0) unequalIdentity ∧ identityCheck zeroExpr oneExpr = false := by
  have hT : P01AC.Form [] unequalIdentity := identity_formed zeroExpr oneExpr
  have hw : P01AC.Has [unequalIdentity] (.var 0) (wk unequalIdentity) :=
    .var (P01AC.form_wk hT .nil hT) .zero
  have ht : wk unequalIdentity = unequalIdentity := unequal_identity_subst _
  have hv : P01AC.Has [unequalIdentity] (.var 0) unequalIdentity := by
    simpa only [ht] using hw
  exact ⟨has_inclusion hv, rfl⟩

end CertificateControls
