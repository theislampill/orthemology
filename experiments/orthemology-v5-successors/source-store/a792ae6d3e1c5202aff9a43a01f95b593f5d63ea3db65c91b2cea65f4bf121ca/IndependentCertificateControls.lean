import UnaryCertificateSoundness
import RuntimeBoundaryInventory
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.IdentityComplexity
open P01AC.UnaryIdentity P01AC.UnaryCertificate
namespace IndependentCertificateReview

def zeroExpr : P01AC.UnaryIdentity.Expr := .constant 0
def oneExpr : P01AC.UnaryIdentity.Expr := .constant 1
def badIdentity : Ty := .identity (arr N N) zeroExpr.closed oneExpr.closed

example (r : Poly) : ¬ HasC [] r badIdentity := by
  intro hr
  exact fragment_rejects_unequal zeroExpr oneExpr rfl ⟨r,hr⟩
example : ¬ ∃ r : Poly, HasC [] r badIdentity :=
  fragment_rejects_unequal zeroExpr oneExpr rfl

-- An arbitrary pair of valuations need not be admitted at the empty context.
-- The certificate-specific relation nevertheless holds there.
example (R : REnv) :
    G (.identity (arr N N) Expr.variable.closed Expr.variable.closed)
      R (fun _ => .k) (fun _ => .s) .i .i ∧
    ¬ H [] R (fun _ => .k) (fun _ => .s) := by
  constructor
  · exact certificate_all_valuations .variable .variable (makeCertificate .variable) rfl R _ _
  · intro h
    have he := congrFun h.1 0
    cases he

theorem unequal_not_related (ρ : OEnv) :
    ¬ F (arr N N) ρ zeroEnv (eval zeroExpr.closed zeroEnv) (eval oneExpr.closed zeroEnv) := by
  intro h
  have out := (F_arr N N ρ zeroEnv _ _).mp h
    (canonical 0) (canonical 0) (canonical_self 0 ρ)
  have heq := related_same_index out
    (zeroExpr.closed_obs zeroEnv (canonical_obs 0))
    (oneExpr.closed_obs zeroEnv (canonical_obs 0))
  exact Nat.zero_ne_one heq

theorem false_assumption_has_no_semantic_environment (R : REnv) (η ξ : Env) :
    ¬ H [badIdentity] R η ξ := by
  intro h
  have tail_eq : tail η = zeroEnv := h.1.1
  have head : G badIdentity R (tail η) (tail ξ) (η 0) (ξ 0) := h.2
  have relation : F (arr N N) R.left (tail η)
      (eval zeroExpr.closed (tail η)) (eval oneExpr.closed (tail η)) := head.1
  rw [tail_eq] at relation
  exact unequal_not_related R.left relation

-- Nonetheless the false identity can be used as a syntactically formed assumption.
theorem false_assumption_is_derivable : HasC [badIdentity] (.var 0) badIdentity := by
  have hT : P01AC.Form [] badIdentity := identity_formed zeroExpr oneExpr
  have hw : P01AC.Has [badIdentity] (.var 0) (wk badIdentity) :=
    .var (P01AC.form_wk hT .nil hT) .zero
  have he : wk badIdentity = badIdentity := by
    simp only [badIdentity, wk, subst, subst_arr, N_subst,
      psub_closed (P01AC.has_scoped zeroExpr.closed_has),
      psub_closed (P01AC.has_scoped oneExpr.closed_has)]
  have hv : P01AC.Has [badIdentity] (.var 0) badIdentity := by
    simpa only [he] using hw
  exact has_inclusion hv

theorem arbitrary_context_converse_is_false :
    ¬ (∀ (Γ : Tel) (e f : P01AC.UnaryIdentity.Expr) (r : Poly),
      HasC Γ r (.identity (arr N N) e.closed f.closed) → identityCheck e f = true) := by
  intro h
  have bad := h [badIdentity] zeroExpr oneExpr (.var 0) false_assumption_is_derivable
  change false = true at bad
  cases bad

-- The original dependent-J premises and full cross-environment conclusion remain usable.
example {Γ A B x y e d}
    (hA : FormC Γ A) (hB : FormC (theta Γ A x) B)
    (hId : FormC Γ (.identity A x y))
    (hBase : FormC Γ (motiveAt B x (.atom .i)))
    (hTarget : FormC Γ (motiveAt B y e))
    (hx : HasC Γ x A) (hy : HasC Γ y A)
    (he : HasC Γ e (.identity A x y)) (hd : HasC Γ d (motiveAt B x (.atom .i)))
    (R : REnv) (η ξ : Env) (hh : H Γ R η ξ) :
    G (motiveAt B y e) R η ξ (eval (jPoly d y e) η) (eval (jPoly d y e) ξ) :=
  P01AC.UnaryCertificate.fundamental
    (HasC.j hA hB hId hBase hTarget hx hy he hd) R η ξ hh

-- Arbitrary proof terms, rather than only the new leaf, are covered by the converse.
example (e f : P01AC.UnaryIdentity.Expr) (r : Poly)
    (hr : HasC [] r (.identity (arr N N) e.closed f.closed)) (n : Nat) :
    e.denote n = f.denote n := (fragment_witness_iff_denote e f).mp ⟨r,hr⟩ n

example : HasC [] (.atom .i) (.identity (arr N N)
    IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) ∧
    ¬ ∃ r : Poly, P01AC.Has [] r (.identity (arr N N)
    IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) := strict_current_extension
end IndependentCertificateReview

#audit_safe_closure IndependentCertificateReview.false_assumption_has_no_semantic_environment
#audit_unary_opaque_boundary IndependentCertificateReview.false_assumption_has_no_semantic_environment
