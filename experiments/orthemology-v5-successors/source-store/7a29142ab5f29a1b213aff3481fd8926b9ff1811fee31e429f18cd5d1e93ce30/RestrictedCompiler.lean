/- The restricted source language is compiled into the accepted PR syntax and,
   through its unchanged compiler, actual P01AC polynomials and current Has. -/
import EffectivePrimitiveRecursion
namespace P01AC.RestrictedIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01F (cons)

inductive Expr (r : Nat) where
  | constant : Nat → Expr r
  | variable : Fin r → Expr r
  | add : Expr r → Expr r → Expr r
  | mul : Expr r → Expr r → Expr r
  | ifZero : Expr r → Expr r → Expr r → Expr r
  deriving Repr

def Expr.denote {r} : Expr r → (Nat → Nat) → Nat
  | .constant n, _ => n
  | .variable i, v => v i.val
  | .add e f, v => e.denote v + f.denote v
  | .mul e f, v => e.denote v * f.denote v
  | .ifZero t e f, v => if t.denote v = 0 then e.denote v else f.denote v

theorem Expr.denote_congr {r} (e : Expr r) {v w : Nat → Nat}
    (h : ∀ i, i < r → v i = w i) : e.denote v = e.denote w := by
  induction e with
  | constant n => rfl
  | «variable» i => exact h i.val i.isLt
  | add e f he hf => exact congrArg₂ Nat.add he hf
  | mul e f he hf => exact congrArg₂ Nat.mul he hf
  | ifZero t e f ht he hf => simp only [Expr.denote, ht, he, hf]

/-- Literal finite PR descriptions, with the accepted recursion convention. -/
def constantPR (r : Nat) : Nat → PR r
  | 0 => .zero r
  | n+1 => .comp .succ (fun _ => constantPR r n)

def addPR : PR 2 := .prec (.proj ⟨0, by decide⟩)
  (.comp .succ (fun _ => .proj ⟨1, by decide⟩))
def mulPR : PR 2 := .prec (.zero 1)
  (.comp addPR (fun i => if i.val = 0 then .proj ⟨2, by decide⟩ else .proj ⟨1, by decide⟩))
/-- Arguments are test, zero branch, positive branch. -/
def choosePR : PR 3 := .prec (.proj ⟨0, by decide⟩) (.proj ⟨3, by decide⟩)

def binary {r} (f : PR 2) (a b : PR r) : PR r :=
  .comp f (fun i => if i.val = 0 then a else b)
def ternary {r} (f : PR 3) (a b c : PR r) : PR r :=
  .comp f (fun i => if i.val = 0 then a else if i.val = 1 then b else c)

def Expr.toPR {r} : Expr r → PR r
  | .constant n => constantPR r n
  | .variable i => .proj i
  | .add e f => binary addPR e.toPR f.toPR
  | .mul e f => binary mulPR e.toPR f.toPR
  | .ifZero t e f => ternary choosePR t.toPR e.toPR f.toPR

theorem constantPR_denote (r n : Nat) (v : Nat → Nat) :
    (constantPR r n).denote v = n := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [constantPR, PR.denote] using congrArg Nat.succ ih

theorem addPR_denote (v : Nat → Nat) : addPR.denote v = v 0 + v 1 := by
  change Nat.rec (motive := fun _ => Nat) (v 1) (fun _ a => a + 1) (v 0) = v 0 + v 1
  induction v 0 with
  | zero => exact (Nat.zero_add _).symm
  | succ n ih => simp [ih, Nat.succ_add]

theorem mulPR_denote (v : Nat → Nat) : mulPR.denote v = v 0 * v 1 := by
  simp only [mulPR, PR.denote, addPR_denote]
  change Nat.rec (motive := fun _ => Nat) 0 (fun _ a => v 1 + a) (v 0) = v 0 * v 1
  induction v 0 with
  | zero => exact (Nat.zero_mul _).symm
  | succ n ih => simpa only [Nat.rec, ih, Nat.succ_mul] using Nat.add_comm (v 1) (n * v 1)

theorem choosePR_denote (v : Nat → Nat) :
    choosePR.denote v = if v 0 = 0 then v 1 else v 2 := by
  change Nat.rec (motive := fun _ => Nat) (v 1) (fun _ _ => v 2) (v 0) = if v 0 = 0 then v 1 else v 2
  cases v 0 <;> rfl

theorem Expr.toPR_denote {r} (e : Expr r) (v : Nat → Nat) :
    e.toPR.denote v = e.denote v := by
  induction e with
  | constant n => exact constantPR_denote r n v
  | «variable» i => rfl
  | add e f he hf => simp [Expr.toPR, binary, PR.denote, addPR_denote, Expr.denote, he, hf]
  | mul e f he hf => simp [Expr.toPR, binary, PR.denote, mulPR_denote, Expr.denote, he, hf]
  | ifZero t e f ht he hf =>
    simp [Expr.toPR, ternary, PR.denote, choosePR_denote, Expr.denote, ht, he, hf]

def Expr.body {r} (e : Expr r) : Poly := e.toPR.compile

theorem Expr.body_has {r} (e : Expr r) : Has (NatCtx r) e.body N :=
  e.toPR.compile_has

theorem Expr.body_obs {r} (e : Expr r) (η : Env) (v : Nat → Nat)
    (hη : EnvNat r η v) : NatObs (eval e.body η) (e.denote v) := by
  simpa only [Expr.toPR_denote] using e.toPR.compile_obs η v hη

/-- Curried natural carrier with exactly r arrows. -/
def Curried : Nat → Ty
  | 0 => N
  | r+1 => arr N (Curried r)

theorem Curried_subst (r : Nat) (σ : Nat → Poly) : subst σ (Curried r) = Curried r := by
  induction r generalizing σ with
  | zero => rfl
  | succ r ih => simp only [Curried, subst_arr, N_subst, ih]

theorem Curried_form (r : Nat) {Γ : Tel} (hΓ : Ctx Γ) : Form Γ (Curried r) := by
  induction r with
  | zero => exact N_form hΓ
  | succ r ih => exact form_arr (N_form hΓ) ih

/-- Repeated existing bracket abstraction, no added binder or eta rule. -/
def closeMany : Nat → Poly → Poly
  | 0, p => p
  | r+1, p => abstract (closeMany r p)

theorem closeMany_commute (r : Nat) (p : Poly) :
    closeMany r (abstract p) = abstract (closeMany r p) := by
  induction r with
  | zero => rfl
  | succ r ih => exact congrArg abstract ih

theorem closeMany_has (r k : Nat) {p : Poly} (hp : Has (NatCtx r) p (Curried k)) :
    Has [] (closeMany r p) (Curried (r+k)) := by
  induction r generalizing k p with
  | zero => simpa only [closeMany, Nat.zero_add] using hp
  | succ r ih =>
    have hb : Has (NatCtx r) (abstract p) (Curried (k+1)) := by
      have hs : wk (Curried k) = Curried k := Curried_subst k _
      apply Has.piIntro (form_arr (N_form (natctx_formed r)) (Curried_form k (natctx_formed r)))
      · simpa only [hs] using hp
      · exact scoped_abstract (has_scoped hp)
    have h := ih (k+1) hb
    simpa only [closeMany_commute, closeMany, Nat.add_right_comm r 1 k, Nat.add_assoc] using h

def Expr.closed {r} (e : Expr r) : Poly := closeMany r e.body

theorem Expr.closed_has {r} (e : Expr r) : Has [] e.closed (Curried r) := by
  exact closeMany_has r 0 e.body_has

def applyArgs (t : Term) : List Term → Term
  | [] => t
  | x :: xs => applyArgs (.app t x) xs

def extendArgs (η : Env) : List Term → Env
  | [] => η
  | x :: xs => extendArgs (cons x η) xs

theorem applyArgs_congr {t u : Term} (h : Conv t u) (xs : List Term) :
    Conv (applyArgs t xs) (applyArgs u xs) := by
  induction xs generalizing t u with
  | nil => exact h
  | cons x xs ih => exact ih (h.left x)

/-- xs is application order; the final de Bruijn environment reverses it. -/
theorem closeMany_applied (p : Poly) (η : Env) (xs : List Term) :
    Conv (applyArgs (eval (closeMany xs.length p) η) xs) (eval p (extendArgs η xs)) := by
  induction xs generalizing η with
  | nil => exact .refl _
  | cons x xs ih =>
    exact (applyArgs_congr
      (P01Source.red_conv (abstraction_beta (closeMany xs.length p) η x)) xs).trans
      (ih (cons x η))

theorem Expr.closed_obs {r} (e : Expr r) (xs : List Term) (hl : xs.length = r)
    (v : Nat → Nat) (hx : EnvNat r (extendArgs zeroEnv xs) v) :
    NatObs (applyArgs (eval e.closed zeroEnv) xs) (e.denote v) := by
  apply NatObs.of_conv _ (e.body_obs _ v hx)
  simpa only [Expr.closed, hl] using closeMany_applied e.body zeroEnv xs

inductive RelatedArgs (R : Term → Term → Prop) : List Term → List Term → Prop
  | nil : RelatedArgs R [] []
  | cons {x y xs ys} : R x y → RelatedArgs R xs ys → RelatedArgs R (x :: xs) (y :: ys)

/-- Original cross-argument arrow semantics, iterated exactly r times. -/
theorem curried_relation_iff_lists (r : Nat) (ρ : OEnv) (t u : Term) :
    F (Curried r) ρ zeroEnv t u ↔
      ∀ xs ys : List Term, xs.length = r → RelatedArgs (F N ρ zeroEnv) xs ys →
        F N ρ zeroEnv (applyArgs t xs) (applyArgs u ys) := by
  induction r generalizing t u with
  | zero =>
    constructor
    · intro h xs ys hl hxy
      have ex : xs = [] := List.length_eq_zero_iff.mp hl
      subst xs
      cases hxy
      exact h
    · intro h
      exact h [] [] rfl .nil
  | succ r ih =>
    rw [Curried, F_arr]
    constructor
    · intro h xs ys hl hxy
      cases hxy with
      | nil => simp at hl
      | @cons x y xs ys hxy htail =>
        exact (ih (.app t x) (.app u y)).mp (h x y hxy) xs ys (Nat.succ.inj hl) htail
    · intro h x y hxy
      apply (ih (.app t x) (.app u y)).mpr
      intro xs ys hl htail
      exact h (x :: xs) (y :: ys) (congrArg Nat.succ hl) (.cons hxy htail)

theorem EnvNat.cons {r : Nat} {η : Env} {v : Nat → Nat} {x : Term} {n : Nat}
    (hx : NatObs x n) (hη : EnvNat r η v) :
    EnvNat (r+1) (cons x η) (cons n v) := by
  intro i hi
  cases i with
  | zero => exact hx
  | succ i => exact hη i (Nat.lt_of_succ_lt_succ hi)

theorem relatedArgs_indices (ρ : OEnv) {xs ys : List Term}
    (h : RelatedArgs (F N ρ zeroEnv) xs ys)
    {k : Nat} {η ξ : Env} {v : Nat → Nat}
    (hη : EnvNat k η v) (hξ : EnvNat k ξ v) :
    ∃ w : Nat → Nat, EnvNat (k + xs.length) (extendArgs η xs) w ∧
      EnvNat (k + xs.length) (extendArgs ξ ys) w := by
  induction h generalizing k η ξ v with
  | nil => exact ⟨v, hη, hξ⟩
  | @cons x y xs ys hxy htail ih =>
    have laws := ((form_sound (N_form Ctx.nil)).2.laws.per
      (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
    obtain ⟨m, hm⟩ := semantic_church_standardness (laws.left hxy)
    obtain ⟨n, hn⟩ := semantic_church_standardness (laws.right hxy)
    have he := related_same_index hxy hm hn
    subst n
    obtain ⟨w, hwη, hwξ⟩ := ih (EnvNat.cons hm hη) (EnvNat.cons hn hξ)
    refine ⟨w, ?_, ?_⟩
    · simpa only [List.length_cons, Nat.add_assoc, Nat.add_comm 1 xs.length, extendArgs] using hwη
    · simpa only [List.length_cons, Nat.add_assoc, Nat.add_comm 1 xs.length, extendArgs] using hwξ

theorem RelatedArgs.left_self {ρ : OEnv} {xs ys : List Term}
    (h : RelatedArgs (F N ρ zeroEnv) xs ys) : RelatedArgs (F N ρ zeroEnv) xs xs := by
  have laws := ((form_sound (N_form Ctx.nil)).2.laws.per
    (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
  induction h with
  | nil => exact .nil
  | cons h _ ih => exact .cons (laws.left h) ih

theorem RelatedArgs.right_self {ρ : OEnv} {xs ys : List Term}
    (h : RelatedArgs (F N ρ zeroEnv) xs ys) : RelatedArgs (F N ρ zeroEnv) ys ys := by
  have laws := ((form_sound (N_form Ctx.nil)).2.laws.per
    (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
  induction h with
  | nil => exact .nil
  | cons h _ ih => exact .cons (laws.right h) ih

theorem RelatedArgs.length_eq {R : Term → Term → Prop} {xs ys : List Term}
    (h : RelatedArgs R xs ys) : xs.length = ys.length := by
  induction h with
  | nil => rfl
  | cons _ _ ih => exact congrArg Nat.succ ih

def canonicalArgs : Nat → (Nat → Nat) → List Term
  | 0, _ => []
  | r+1, v => canonical (v r) :: canonicalArgs r v

theorem canonicalArgs_length (r : Nat) (v : Nat → Nat) : (canonicalArgs r v).length = r := by
  induction r with
  | zero => rfl
  | succ r ih => exact congrArg Nat.succ ih

theorem canonicalArgs_self (r : Nat) (v : Nat → Nat) (ρ : OEnv) :
    RelatedArgs (F N ρ zeroEnv) (canonicalArgs r v) (canonicalArgs r v) := by
  induction r with
  | zero => exact .nil
  | succ r ih => exact .cons (canonical_self (v r) ρ) ih

theorem canonicalArgs_environment (r : Nat) (v : Nat → Nat) (η : Env) (i : Nat) :
    extendArgs η (canonicalArgs r v) i =
      if i < r then canonical (v i) else η (i-r) := by
  induction r generalizing η with
  | zero => simp [canonicalArgs, extendArgs]
  | succ r ih =>
    rw [canonicalArgs, extendArgs, ih]
    by_cases hi : i < r
    · simp only [hi, if_pos, show i < r+1 by omega]
    · by_cases he : i = r
      · subst i
        simp [cons]
      · have hr : ¬ i < r+1 := by omega
        have hs : i-r = (i-(r+1))+1 := by omega
        simp only [hi, hr, if_false, hs, cons]

theorem canonicalArgs_envNat (r : Nat) (v : Nat → Nat) :
    EnvNat r (extendArgs zeroEnv (canonicalArgs r v)) v := by
  intro i hi
  rw [canonicalArgs_environment, if_pos hi]
  exact canonical_obs (v i)

def FragmentValid {r} (e f : Expr r) : Prop :=
  ∀ ρ, F (Curried r) ρ zeroEnv (eval e.closed zeroEnv) (eval f.closed zeroEnv)

/-- Exact source-specific endpoint bridge. All finite arities, including zero;
    all unary environments and independently related raw inputs are retained. -/
theorem fragment_valid_iff_denote {r} (e f : Expr r) :
    FragmentValid e f ↔ ∀ v : Nat → Nat, e.denote v = f.denote v := by
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

/-- Transfer uses the original identity clause; no current-Has identity proof
    is asserted or manufactured. -/
theorem fragment_F_identity_iff_denote {r} (e f : Expr r) :
    (∀ ρ, F (.identity (Curried r) e.closed f.closed) ρ zeroEnv .i .i) ↔
      ∀ v, e.denote v = f.denote v := by
  rw [← fragment_valid_iff_denote]
  exact ⟨fun h ρ => (h ρ).1, fun h ρ => ⟨h ρ, .refl _, .refl _⟩⟩

theorem fragment_G_identity_iff_denote {r} (e f : Expr r) :
    (∀ R : REnv, G (.identity (Curried r) e.closed f.closed) R zeroEnv zeroEnv .i .i) ↔
      ∀ v, e.denote v = f.denote v := by
  rw [← fragment_valid_iff_denote]
  exact ⟨fun h ρ => (h (diagEnv ρ)).1, fun h R => ⟨h R.left, h R.right, .refl _, .refl _⟩⟩

theorem fragment_semantic_witness_iff_denote {r} (e f : Expr r) :
    (∃ w : Poly, ∀ R : REnv, G (.identity (Curried r) e.closed f.closed) R zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ ∀ v, e.denote v = f.denote v := by
  rw [← fragment_valid_iff_denote]
  exact ⟨fun ⟨_, hw⟩ ρ => (hw (diagEnv ρ)).1,
    fun h => ⟨.atom .i, fun R => ⟨h R.left, h R.right, .refl _, .refl _⟩⟩⟩

theorem fragment_identity_formed {r} (e f : Expr r) :
    Form [] (.identity (Curried r) e.closed f.closed) :=
  .identity (Curried_form r .nil) e.closed_has f.closed_has

-- Regression controls: argument order, both branches, constant and arity zero.
example : addPR.denote (cons 4 (cons 7 (fun _ => 83))) = 11 := rfl
example : mulPR.denote (cons 4 (cons 7 (fun _ => 83))) = 28 := rfl
example : choosePR.denote (cons 0 (cons 5 (cons 11 (fun _ => 83)))) = 5 := rfl
example : choosePR.denote (cons 4 (cons 5 (cons 11 (fun _ => 83)))) = 11 := rfl
example : Has [] (Expr.constant (r := 0) 9).body N := (Expr.constant (r := 0) 9).body_has
example (η : Env) : NatObs (eval (Expr.constant (r := 0) 9).body η) 9 :=
  Expr.body_obs _ η (fun _ => 53) (fun i hi => False.elim (Nat.not_lt_zero i hi))

#print axioms Expr.toPR_denote
#print axioms Expr.body_has
#print axioms Expr.body_obs
#print axioms Expr.closed_has
#print axioms Expr.closed_obs
#print axioms curried_relation_iff_lists
#print axioms fragment_valid_iff_denote
#print axioms fragment_F_identity_iff_denote
#print axioms fragment_G_identity_iff_denote
#print axioms fragment_semantic_witness_iff_denote
#print axioms fragment_identity_formed
end P01AC.RestrictedIdentity
