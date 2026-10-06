/- Unary finite equality-conditional expressions, literally compiled through the
   accepted PR compiler. No source recursion, typing extension, or new axiom. -/
import PolynomialTestBoundary

namespace P01AC.UnaryIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity (constantPR addPR mulPR choosePR binary ternary
  constantPR_denote addPR_denote mulPR_denote choosePR_denote closeMany closeMany_has)
open P01AC.PolynomialTestBoundary (equalPR equalPR_denote)
open P01F (cons)

/-- Exactly one independent natural input; every conditional has four arbitrary
    children in this same finite grammar. -/
inductive Expr where
  | constant : Nat → Expr
  | variable : Expr
  | add : Expr → Expr → Expr
  | mul : Expr → Expr → Expr
  | ifEq : Expr → Expr → Expr → Expr → Expr
  deriving Repr, DecidableEq

def Expr.denote : Expr → Nat → Nat
  | .constant c, _ => c
  | .variable, n => n
  | .add a b, n => a.denote n + b.denote n
  | .mul a b, n => a.denote n * b.denote n
  | .ifEq a b yes no, n => if a.denote n = b.denote n then yes.denote n else no.denote n

/-- Finite syntactic substitution into all four conditional children. -/
def Expr.substitute : Expr → Expr → Expr
  | .constant c, _ => .constant c
  | .variable, inner => inner
  | .add a b, inner => .add (a.substitute inner) (b.substitute inner)
  | .mul a b, inner => .mul (a.substitute inner) (b.substitute inner)
  | .ifEq a b yes no, inner => .ifEq (a.substitute inner) (b.substitute inner)
      (yes.substitute inner) (no.substitute inner)

theorem Expr.substitute_denote (outer inner : Expr) (n : Nat) :
    (outer.substitute inner).denote n = outer.denote (inner.denote n) := by
  induction outer with
  | constant c => rfl
  | «variable» => rfl
  | add a b ha hb => simp only [substitute, denote, ha, hb]
  | mul a b ha hb => simp only [substitute, denote, ha, hb]
  | ifEq a b yes no ha hb hy hn => simp only [substitute, denote, ha, hb, hy, hn]

/-- `equalPR` returns one on equality, while `choosePR` selects its second
    argument on zero. Thus the literal order is guard, ELSE, THEN. -/
def Expr.toPR : Expr → PR 1
  | .constant c => constantPR 1 c
  | .variable => .proj ⟨0, by decide⟩
  | .add a b => binary addPR a.toPR b.toPR
  | .mul a b => binary mulPR a.toPR b.toPR
  | .ifEq a b yes no => ternary choosePR (binary equalPR a.toPR b.toPR) no.toPR yes.toPR

theorem Expr.toPR_denote (e : Expr) (v : Nat → Nat) :
    e.toPR.denote v = e.denote (v 0) := by
  induction e with
  | constant c => exact constantPR_denote 1 c v
  | «variable» => rfl
  | add a b ha hb => simp [toPR, binary, PR.denote, addPR_denote, denote, ha, hb]
  | mul a b ha hb => simp [toPR, binary, PR.denote, mulPR_denote, denote, ha, hb]
  | ifEq a b yes no ha hb hy hn =>
    simp [toPR, ternary, binary, PR.denote, choosePR_denote, equalPR_denote,
      denote, ha, hb, hy, hn]

/-- The body is exactly the existing compiler output, without an alternative
    interpreter or merely extensionally equal replacement endpoint. -/
def Expr.body (e : Expr) : Poly := e.toPR.compile

def Expr.closed (e : Expr) : Poly := closeMany 1 e.body

theorem Expr.body_has (e : Expr) : Has (NatCtx 1) e.body N := e.toPR.compile_has

theorem Expr.closed_has (e : Expr) : Has [] e.closed (arr N N) :=
  closeMany_has 1 0 e.body_has

/-- Adequacy is for an arbitrary raw observed natural, not just a numeral or
    a currently typed input. The unused coordinates are unrestricted. -/
theorem Expr.body_obs (e : Expr) (η : Env) (n : Nat) (hη : NatObs (η 0) n) :
    NatObs (eval e.body η) (e.denote n) := by
  have he : EnvNat 1 η (fun _ => n) := by
    intro i hi
    have h : i = 0 := by omega
    subst i
    exact hη
  simpa only [body, toPR_denote] using e.toPR.compile_obs η (fun _ => n) he

/-- Arbitrary-environment, arbitrary-raw-input adequacy for the literal closed
    endpoint. No `MarkerFree`, canonical-input, or semantic membership premise. -/
theorem Expr.closed_obs (e : Expr) (η : Env) {u : Term} {n : Nat} (hu : NatObs u n) :
    NatObs (.app (eval e.closed η) u) (e.denote n) := by
  apply NatObs.of_conv (P01Source.red_conv (abstraction_beta e.body η u))
  exact e.body_obs (cons u η) n hu

/-- The original arrow relation in every unary type environment. Its arrow
    clause quantifies over independently chosen related raw natural inputs. -/
def Valid (e f : Expr) : Prop :=
  ∀ ρ, F (arr N N) ρ zeroEnv (eval e.closed zeroEnv) (eval f.closed zeroEnv)

theorem valid_iff_denote (e f : Expr) :
    Valid e f ↔ ∀ n : Nat, e.denote n = f.denote n := by
  constructor
  · intro hv n
    let ρ : OEnv := fun _ => rawPER
    have h := (F_arr N N ρ zeroEnv _ _).mp (hv ρ)
      (canonical n) (canonical n) (canonical_self n ρ)
    exact related_same_index h (e.closed_obs zeroEnv (canonical_obs n))
      (f.closed_obs zeroEnv (canonical_obs n))
  · intro heq ρ
    rw [F_arr]
    intro u v huv
    have laws := ((form_sound (N_form Ctx.nil)).2.laws.per
      (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
    obtain ⟨m, hm⟩ := semantic_church_standardness (laws.left huv)
    obtain ⟨n, hn⟩ := semantic_church_standardness (laws.right huv)
    have hmn : m = n := related_same_index huv hm hn
    subst n
    have hep := unary_fundamental e.closed_has (ρ := ρ) ⟨rfl, rfl⟩
    have hfp := unary_fundamental f.closed_has (ρ := ρ) ⟨rfl, rfl⟩
    have heu := (F_arr N N ρ zeroEnv _ _).mp hep u u (laws.left huv)
    have hfv := (F_arr N N ρ zeroEnv _ _).mp hfp v v (laws.right huv)
    apply same_index_related heu hfv (e.closed_obs zeroEnv hm)
    rw [heq m]
    exact f.closed_obs zeroEnv hn

/-- Original F identity semantics, with the literal reflexivity proof term. -/
theorem F_identity_iff_denote (e f : Expr) :
    (∀ ρ, F (.identity (arr N N) e.closed f.closed) ρ zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := by
  rw [← valid_iff_denote]
  exact ⟨fun h ρ => (h ρ).1, fun h ρ => ⟨h ρ, .refl _, .refl _⟩⟩

/-- Original G identity semantics in every lawful relation environment. -/
theorem G_identity_iff_denote (e f : Expr) :
    (∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := by
  rw [← valid_iff_denote]
  exact ⟨fun h ρ => (h (diagEnv ρ)).1, fun h R => ⟨h R.left, h R.right, .refl _, .refl _⟩⟩

theorem semantic_witness_iff_denote (e f : Expr) :
    (∃ w : Poly, ∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ ∀ n, e.denote n = f.denote n := by
  rw [← valid_iff_denote]
  exact ⟨fun ⟨_, hw⟩ ρ => (hw (diagEnv ρ)).1,
    fun h => ⟨.atom .i, fun R => ⟨h R.left, h R.right, .refl _, .refl _⟩⟩⟩

/-- Current formation, supplied by the two actual current endpoint typings.
    This does not assert current identity inhabitation from semantic validity. -/
theorem identity_formed (e f : Expr) :
    Form [] (.identity (arr N N) e.closed f.closed) :=
  .identity (form_arr (N_form .nil) (N_form .nil)) e.closed_has f.closed_has

/-- A claim that separately supplies endpoints must bind them literally to the
    compiler output. Semantic source equality alone does not supply this data. -/
structure LiteralEndpoints (e f : Expr) (p q : Poly) : Prop where
  left : p = e.closed
  right : q = f.closed

theorem bound_F_identity_iff_denote (e f : Expr) (p q : Poly)
    (h : LiteralEndpoints e f p q) :
    (∀ ρ, F (.identity (arr N N) p q) ρ zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := by
  rw [h.left, h.right]
  exact F_identity_iff_denote e f

theorem bound_G_identity_iff_denote (e f : Expr) (p q : Poly)
    (h : LiteralEndpoints e f p q) :
    (∀ R : REnv, G (.identity (arr N N) p q) R zeroEnv zeroEnv .i .i) ↔
      ∀ n, e.denote n = f.denote n := by
  rw [h.left, h.right]
  exact G_identity_iff_denote e f

theorem bound_semantic_witness_iff_denote (e f : Expr) (p q : Poly)
    (h : LiteralEndpoints e f p q) :
    (∃ w : Poly, ∀ R : REnv, G (.identity (arr N N) p q) R zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ ∀ n, e.denote n = f.denote n := by
  rw [h.left, h.right]
  exact semantic_witness_iff_denote e f

theorem bound_identity_formed (e f : Expr) (p q : Poly)
    (h : LiteralEndpoints e f p q) : Form [] (.identity (arr N N) p q) := by
  rw [h.left, h.right]
  exact identity_formed e f

end P01AC.UnaryIdentity
