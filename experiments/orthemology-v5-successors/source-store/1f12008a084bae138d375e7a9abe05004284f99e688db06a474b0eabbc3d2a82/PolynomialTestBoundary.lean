/- Isolated support for a root polynomial-equality test. No DPRM axiom or
   arithmetical-hierarchy theorem is introduced. The accepted sources are imports. -/
import RestrictedCompiler
namespace P01AC.PolynomialTestBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity
open P01F (cons)

-- The actual finite comparison descriptions, in the existing PR basis.
def predPR : PR 1 := .prec (.zero 0) (.proj ⟨0, by decide⟩)
def reverseSubPR : PR 2 := .prec (.proj ⟨0, by decide⟩)
  (.comp predPR (fun _ => .proj ⟨1, by decide⟩))
def equalPR : PR 2 := ternary choosePR
  (binary addPR
    (binary reverseSubPR (.proj ⟨0, by decide⟩) (.proj ⟨1, by decide⟩))
    (binary reverseSubPR (.proj ⟨1, by decide⟩) (.proj ⟨0, by decide⟩)))
  (constantPR 2 1) (.zero 2)

theorem predPR_denote (v : Nat → Nat) : predPR.denote v = v 0 - 1 := by
  simp only [predPR, PR.denote]
  cases v 0 <;> rfl

theorem reverseSubPR_denote (v : Nat → Nat) :
    reverseSubPR.denote v = v 1 - v 0 := by
  simp only [reverseSubPR, PR.denote, predPR_denote]
  change Nat.rec (motive := fun _ => Nat) (v 1) (fun _ a => a - 1) (v 0) = v 1 - v 0
  induction v 0 with
  | zero => rfl
  | succ n ih => simp [ih, Nat.sub_sub, Nat.add_comm]

theorem equalPR_denote (v : Nat → Nat) :
    equalPR.denote v = if v 0 = v 1 then 1 else 0 := by
  simp [equalPR, ternary, binary, PR.denote, choosePR_denote,
    addPR_denote, reverseSubPR_denote, constantPR_denote]
  split_ifs <;> omega

-- Pure arithmetic is a syntactically separate grammar.
inductive Arithmetic (r : Nat) where
  | constant : Nat → Arithmetic r
  | variable : Fin r → Arithmetic r
  | add : Arithmetic r → Arithmetic r → Arithmetic r
  | mul : Arithmetic r → Arithmetic r → Arithmetic r

def Arithmetic.toExpr {r} : Arithmetic r → Expr r
  | .constant n => .constant n
  | .variable i => .variable i
  | .add a b => .add a.toExpr b.toExpr
  | .mul a b => .mul a.toExpr b.toExpr

def Arithmetic.denote {r} (a : Arithmetic r) (v : Nat → Nat) : Nat := a.toExpr.denote v

theorem Arithmetic.denote_congr {r} (a : Arithmetic r) {v w : Nat → Nat}
    (h : ∀ i, i < r → v i = w i) : a.denote v = a.denote w :=
  Expr.denote_congr a.toExpr h

-- Equality is permitted once at the root, with literal branches 1 and 0.
inductive Root (r : Nat) where
  | old : Expr r → Root r
  | equal : Arithmetic r → Arithmetic r → Root r

def Root.denote {r} : Root r → (Nat → Nat) → Nat
  | .old e, v => e.denote v
  | .equal p q, v => if p.denote v = q.denote v then 1 else 0

theorem Root.denote_congr {r} (e : Root r) {v w : Nat → Nat}
    (h : ∀ i, i < r → v i = w i) : e.denote v = e.denote w := by
  cases e with
  | old e => exact Expr.denote_congr e h
  | equal p q => simp only [Root.denote, p.denote_congr h, q.denote_congr h]

def Root.toPR {r} : Root r → PR r
  | .old e => e.toPR
  | .equal p q => binary equalPR p.toExpr.toPR q.toExpr.toPR

theorem Root.toPR_denote {r} (e : Root r) (v : Nat → Nat) :
    e.toPR.denote v = e.denote v := by
  cases e with
  | old e => exact Expr.toPR_denote e v
  | equal p q =>
    simp only [Root.toPR, binary, PR.denote, equalPR_denote]
    simp [Expr.toPR_denote, Root.denote, Arithmetic.denote]

def Root.body {r} (e : Root r) : Poly := e.toPR.compile
def Root.closed {r} (e : Root r) : Poly := closeMany r e.body

theorem Root.body_has {r} (e : Root r) : Has (NatCtx r) e.body N := e.toPR.compile_has

theorem Root.closed_has {r} (e : Root r) : Has [] e.closed (Curried r) := by
  exact closeMany_has r 0 e.body_has

theorem Root.closed_obs {r} (e : Root r) (xs : List Term) (hl : xs.length = r)
    (v : Nat → Nat) (h : EnvNat r (extendArgs zeroEnv xs) v) :
    NatObs (applyArgs (eval e.closed zeroEnv) xs) (e.denote v) := by
  have hc := closeMany_applied e.body zeroEnv xs
  rw [hl] at hc
  apply NatObs.of_conv hc
  have ho := e.toPR.compile_obs (extendArgs zeroEnv xs) v h
  simpa only [Root.body, Root.toPR_denote] using ho

def Valid {r} (e f : Root r) : Prop :=
  ∀ ρ, F (Curried r) ρ zeroEnv (eval e.closed zeroEnv) (eval f.closed zeroEnv)

theorem valid_iff_denote {r} (e f : Root r) :
    Valid e f ↔ ∀ v : Nat → Nat, e.denote v = f.denote v := by
  constructor
  · intro hv v
    let ρ : OEnv := fun _ => rawPER
    have hout := (curried_relation_iff_lists r ρ _ _).mp (hv ρ)
      (canonicalArgs r v) (canonicalArgs r v) (canonicalArgs_length r v) (canonicalArgs_self r v ρ)
    exact related_same_index hout
      (e.closed_obs _ (canonicalArgs_length r v) v (canonicalArgs_envNat r v))
      (f.closed_obs _ (canonicalArgs_length r v) v (canonicalArgs_envNat r v))
  · intro heq ρ
    apply (curried_relation_iff_lists r ρ _ _).mpr
    intro xs ys hl hxy
    have hz : EnvNat 0 zeroEnv (fun _ => 0) := fun i hi => False.elim (Nat.not_lt_zero i hi)
    obtain ⟨v, hx, hy⟩ := relatedArgs_indices ρ hxy hz hz
    simp only [Nat.zero_add, hl] at hx hy
    have hly : ys.length = r := hxy.length_eq.symm.trans hl
    have hp := unary_fundamental e.closed_has (ρ := ρ) ⟨rfl, rfl⟩
    have hq := unary_fundamental f.closed_has (ρ := ρ) ⟨rfl, rfl⟩
    have hpout := (curried_relation_iff_lists r ρ _ _).mp hp xs xs hl hxy.left_self
    have hqout := (curried_relation_iff_lists r ρ _ _).mp hq ys ys hly hxy.right_self
    apply same_index_related hpout hqout (e.closed_obs xs hl v hx)
    rw [heq v]
    exact f.closed_obs ys hly v hy

theorem F_identity_iff_denote {r} (e f : Root r) :
    (∀ ρ, F (.identity (Curried r) e.closed f.closed) ρ zeroEnv .i .i) ↔
      ∀ v, e.denote v = f.denote v := by
  rw [← valid_iff_denote]
  exact ⟨fun h ρ => (h ρ).1, fun h ρ => ⟨h ρ, .refl _, .refl _⟩⟩

theorem G_identity_iff_denote {r} (e f : Root r) :
    (∀ R : REnv, G (.identity (Curried r) e.closed f.closed) R zeroEnv zeroEnv .i .i) ↔
      ∀ v, e.denote v = f.denote v := by
  rw [← valid_iff_denote]
  exact ⟨fun h ρ => (h (diagEnv ρ)).1, fun h R => ⟨h R.left, h R.right, .refl _, .refl _⟩⟩

theorem semantic_witness_iff_denote {r} (e f : Root r) :
    (∃ w : Poly, ∀ R : REnv, G (.identity (Curried r) e.closed f.closed) R zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ ∀ v, e.denote v = f.denote v := by
  rw [← valid_iff_denote]
  exact ⟨fun ⟨_, hw⟩ ρ => (hw (diagEnv ρ)).1,
    fun h => ⟨.atom .i, fun R => ⟨h R.left, h R.right, .refl _, .refl _⟩⟩⟩

theorem identity_formed {r} (e f : Root r) :
    Form [] (.identity (Curried r) e.closed f.closed) :=
  .identity (Curried_form r .nil) e.closed_has f.closed_has

theorem root_equal_zero_iff {r} (p q : Arithmetic r) :
    Valid (.equal p q) (.old (.constant 0)) ↔ ∀ v, p.denote v ≠ q.denote v := by
  rw [valid_iff_denote]
  simp [Root.denote, Expr.denote]

example : equalPR.denote (cons 0 (cons 0 (fun _ => 73))) = 1 := by rw [equalPR_denote]; rfl
example : equalPR.denote (cons 0 (cons 5 (fun _ => 73))) = 0 := by rw [equalPR_denote]; rfl
example : equalPR.denote (cons 5 (cons 0 (fun _ => 73))) = 0 := by rw [equalPR_denote]; rfl
example : equalPR.denote (cons 9 (cons 9 (fun _ => 73))) = 1 := by rw [equalPR_denote]; rfl
example : Valid (Root.equal (r := 0) (.constant 2) (.constant 3)) (.old (.constant 0)) := by
  rw [root_equal_zero_iff]; intro v; change 2 ≠ 3; decide

#print axioms equalPR_denote
#print axioms Root.closed_has
#print axioms valid_iff_denote
#print axioms root_equal_zero_iff
end P01AC.PolynomialTestBoundary
