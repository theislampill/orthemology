import UnaryExpressions

namespace P01AC.UnaryIdentity.CompilerControls
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity (binary ternary choosePR)
open P01AC.PolynomialTestBoundary (equalPR)

/-- Each of the four children is nonliteral. The guard's left child has an
    exception; the chosen branch is itself a conditional in both directions. -/
def nested : Expr := .ifEq
  (.ifEq .variable (.constant 2) (.add .variable (.constant 1)) (.mul .variable .variable))
  (.add .variable (.constant 1))
  (.ifEq (.add .variable (.constant 0)) (.constant 2)
    (.mul .variable (.constant 3)) (.add .variable (.constant 4)))
  (.ifEq (.mul .variable (.constant 0)) (.constant 0)
    (.add .variable (.constant 8)) (.constant 99))

example : nested.denote 2 = 6 := rfl
example : nested.denote 3 = 11 := rfl
example : nested.denote 0 = 8 := rfl
example : nested.toPR.denote (fun i => if i = 0 then 2 else 73) = 6 := rfl
example : nested.toPR.denote (fun i => if i = 0 then 3 else 73) = 11 := rfl
example : nested.toPR.denote (fun i => if i = 0 then 0 else 73) = 8 := rfl

-- Freeze the exact branch convention and literal compiler endpoint.
example (a b yes no : Expr) :
    (Expr.ifEq a b yes no).toPR =
      ternary choosePR (binary equalPR a.toPR b.toPR) no.toPR yes.toPR := rfl
example (e : Expr) : e.closed = P01AC.RestrictedIdentity.closeMany 1 e.toPR.compile := rfl

-- Every source, including the conditional, has current endpoint typing.
example (e : Expr) : Has [] e.closed (arr N N) := e.closed_has
example : Has [] nested.closed (arr N N) := nested.closed_has
example (e f : Expr) : Form [] (.identity (arr N N) e.closed f.closed) := identity_formed e f

-- There are no hidden canonical-input, MarkerFree, or input-typing premises.
example (e : Expr) (η : Env) (u : Term) (n : Nat) (h : NatObs u n) :
    NatObs (.app (eval e.closed η) u) (e.denote n) := e.closed_obs η h
example (η : Env) (u : Term) (h : NatObs u 2) :
    NatObs (.app (eval nested.closed η) u) 6 := nested.closed_obs η h

-- The forward semantic theorem is available on independent cross-inputs.
example (e f : Expr) (h : ∀ n, e.denote n = f.denote n)
    (ρ : OEnv) (u v : Term) (huv : F N ρ zeroEnv u v) :
    F N ρ zeroEnv (.app (eval e.closed zeroEnv) u) (.app (eval f.closed zeroEnv) v) :=
  (F_arr N N ρ zeroEnv _ _).mp ((valid_iff_denote e f).mpr h ρ) u v huv

example (e f : Expr) :
    (∀ ρ, F (.identity (arr N N) e.closed f.closed) ρ zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := F_identity_iff_denote e f
example (e f : Expr) :
    (∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := G_identity_iff_denote e f
example (e f : Expr) :
    (∃ w : Poly, ∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ ∀ n, e.denote n = f.denote n :=
  semantic_witness_iff_denote e f

example (e f : Expr) (p q : Poly) (h : LiteralEndpoints e f p q) :
    (∀ R : REnv, G (.identity (arr N N) p q) R zeroEnv zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := bound_G_identity_iff_denote e f p q h
example (e f : Expr) : LiteralEndpoints e f e.closed f.closed := ⟨rfl, rfl⟩

-- Composition reaches the actual outer exception under a constant inner tail.
def exceptional : Expr := .ifEq .variable (.constant 2) (.constant 7) .variable
example (n : Nat) : (exceptional.substitute (.constant 2)).denote n = 7 := rfl
example (inner : Expr) (n : Nat) :
    (nested.substitute inner).denote n = nested.denote (inner.denote n) :=
  nested.substitute_denote inner n
example : Valid (exceptional.substitute (.constant 2)) (.constant 7) :=
  (valid_iff_denote _ _).mpr (fun _ => rfl)

end P01AC.UnaryIdentity.CompilerControls
