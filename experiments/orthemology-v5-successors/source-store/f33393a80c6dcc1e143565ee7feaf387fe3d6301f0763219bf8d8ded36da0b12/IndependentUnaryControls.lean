import UnaryWitnesses
import UnaryExpressivity

namespace UnaryIndependentReview
open P01AC P01AC.UnaryIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

-- Interior absence and an explicit zero exception have different meanings.
example : normalise (.ifEq .variable (.constant 4) (.constant 0) .variable) =
    ⟨[0, 1], [none, none, none, none, some 0]⟩ := by decide
example : verifyCertificate .variable .variable ⟨[0, 1, 0], []⟩ = false := by decide
example : verifyCertificate .variable .variable ⟨[0, 1], [none]⟩ = false := by decide
example : normalise (.mul exceptionalExample (.constant 0)) = ⟨[], []⟩ := by decide
example : normalise (.ifEq .variable .variable .variable (.constant 999)) =
    ⟨[0, 1], []⟩ := by decide

-- Distinct guard polynomials can have a nontrivial positive root.
def atSix : Expr := .ifEq (.mul .variable .variable)
    (.add (.mul (.constant 5) .variable) (.constant 6)) (.constant 99) (.constant 0)
example : normalise atSix = ⟨[], [none, none, none, none, none, none, some 99]⟩ := by decide
example : distinguishingInput atSix (.constant 0) = some 6 := by decide

-- The inner expression is eventually constant, but not everywhere constant.
def innerFinite : Expr := .ifEq .variable (.constant 0) (.constant 3) (.constant 2)
example : normalise (exceptionalExample.substitute innerFinite) = ⟨[7], [some 3]⟩ := by decide
example : identityCheck (exceptionalExample.substitute innerFinite)
    (.ifEq .variable (.constant 0) (.constant 3) (.constant 7)) = true := by decide

-- Nonconstant composition combines an inner exception and the outer exception.
def innerSquare : Expr := .ifEq .variable (.constant 1) (.constant 2) (.mul .variable .variable)
example : normalise (exceptionalExample.substitute innerSquare) =
    ⟨[0, 0, 1], [none, some 7]⟩ := by decide

-- At zero, x and x^2 coincide; the negative producer is nevertheless complete.
example : distinguishingInput .variable (.mul .variable .variable) = some 4 := by decide
example : distinguishingInput (.constant 0) (.constant 1) = some 3 := by decide
example : normalise (Expr.reify ⟨[0, 1, 0, 0], [some 0, none, some 0, none]⟩) =
    ⟨[0, 1], [none, none, some 0]⟩ := by decide

-- The proposition-facing decidable interface executes after proof erasure.
def verdict (e f : Expr) : Bool := @decide (Valid e f) (identityDecidable e f)
#eval verdict (.add .variable (.constant 0)) .variable
#eval verdict exceptionalExample .variable
#eval verdict (exceptionalExample.substitute innerFinite)
    (.ifEq .variable (.constant 0) (.constant 3) (.constant 7))
example (e f : Expr) : verdict e f = identityCheck e f := by
  cases hc : identityCheck e f <;> simp [verdict, identityDecidable, hc]
  all_goals simp [← identityCheck_iff_valid e f, hc]

-- Exact bridge contracts at general, unchosen environments and cross-inputs.
example (e f : Expr) (h : identityCheck e f = true) (ρ : OEnv)
    (u v : Term) (huv : F N ρ zeroEnv u v) :
    F N ρ zeroEnv (.app (eval e.closed zeroEnv) u) (.app (eval f.closed zeroEnv) v) :=
  (F_arr N N ρ zeroEnv _ _).mp ((identityCheck_iff_valid e f).mp h ρ) u v huv
example (e : Expr) (η : Env) (u : Term) (n : Nat) (h : NatObs u n) :
    NatObs (.app (eval e.closed η) u) (e.denote n) := Expr.closed_obs e η h
example (e f : Expr) (p q : Poly) (b : LiteralEndpoints e f p q) :
    identityCheck e f = true ↔
      ∀ R : REnv, G (.identity (arr N N) p q) R zeroEnv zeroEnv .i .i :=
  identityCheck_bound_G e f p q b
example (f : Nat → Nat) :
    (∃ e : Expr, ∀ n, e.denote n = f n) ↔
      ∃ p : List Nat, ∃ b : Nat, ∀ n, b ≤ n → f n = polyEval p n :=
  expressible_iff_eventually_polynomial f
example : ¬ ∃ e : Expr, ∀ n, e.denote n = n - 1 := truncated_predecessor_not_expressible
-- Closed endpoint invariance extends the package's zeroEnv interface to arbitrary
-- term environments as well, without altering the F/G semantics.
example (e f : Expr) (h : identityCheck e f = true) (ρ : OEnv) (η : Env) :
    F (.identity (arr N N) e.closed f.closed) ρ η .i .i := by
  rw [F_identity]
  rw [eval_closed (has_scoped e.closed_has) η zeroEnv,
      eval_closed (has_scoped f.closed_has) η zeroEnv]
  exact ⟨(identityCheck_iff_valid e f).mp h ρ, .refl _, .refl _⟩
example (e f : Expr) (h : identityCheck e f = true) (R : REnv) (η ξ : Env) :
    G (.identity (arr N N) e.closed f.closed) R η ξ .i .i := by
  rw [G_identity]
  rw [eval_closed (has_scoped e.closed_has) η zeroEnv,
      eval_closed (has_scoped f.closed_has) η zeroEnv,
      eval_closed (has_scoped e.closed_has) ξ zeroEnv,
      eval_closed (has_scoped f.closed_has) ξ zeroEnv]
  exact ⟨(identityCheck_iff_valid e f).mp h R.left,
      (identityCheck_iff_valid e f).mp h R.right, .refl _, .refl _⟩
end UnaryIndependentReview
