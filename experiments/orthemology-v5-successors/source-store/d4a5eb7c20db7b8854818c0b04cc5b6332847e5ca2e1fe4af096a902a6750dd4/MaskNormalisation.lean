/- Finite-mask normalization is executable; all semantic uses of it are proved. -/
import SparsePolynomial
import PositiveSeparation

namespace P01AC.RestrictedIdentityV2
open P01AC.RestrictedIdentity
open MvPolynomial

/-- Zero coordinates are substituted immediately. -/
def normalise {r} (s : Mask r) : Expr r → Sparse r
  | .constant n => [(fun _ => 0, n)]
  | .variable i => if s i then [(fun j => if i = j then 1 else 0, 1)] else []
  | .add e f => normalise s e ++ normalise s f
  | .mul e f => multiply (normalise s e) (normalise s f)
  | .ifZero t e f => if zeroTest (normalise s t) then normalise s e else normalise s f

def maskValues {r} (s : Mask r) (v : Fin r → Nat) : Fin r → Nat :=
  fun i => if s i then v i else 0

def numberEnvironment {r} (v : Fin r → Nat) : Nat → Nat :=
  fun i => if hi : i < r then v ⟨i,hi⟩ else 0

@[simp] theorem numberEnvironment_fin {r} (v : Fin r → Nat) (i : Fin r) :
    numberEnvironment v i.val = v i := by simp [numberEnvironment]

@[simp] theorem exponentFinsupp_zero (r : Nat) :
    exponentFinsupp (fun _ : Fin r => 0) = 0 := by ext i; rfl

@[simp] theorem exponentFinsupp_unit {r} (i : Fin r) :
    exponentFinsupp (fun j => if i = j then 1 else 0) = Finsupp.single i 1 := by
  ext j
  simp [Finsupp.single_apply, eq_comm]

/-- The positive auxiliary tuple is unrestricted on dead coordinates. The
    expression side masks those coordinates to zero, exactly matching the normalizer. -/
theorem normalise_correct {r} (e : Expr r) (s : Mask r) (v : Fin r → Nat)
    (hv : ∀ i, 0 < v i) :
    eval v (polynomial (normalise s e)) = e.denote (numberEnvironment (maskValues s v)) := by
  induction e with
  | constant n => simp [normalise, polynomial, Expr.denote, ← C_apply]
  | «variable» i =>
    cases hs : s i <;> simp [normalise, hs, polynomial, Expr.denote,
      maskValues, ← X_pow_eq_monomial]
  | add e f he hf => simp [normalise, Expr.denote, eval_add, he, hf]
  | mul e f he hf => simp [normalise, Expr.denote, eval_mul, he, hf]
  | ifZero t e f ht he hf =>
    have hz := zeroTest_iff_eval_zero (normalise s t) v hv
    by_cases h : zeroTest (normalise s t) = true
    · have h0 : t.denote (numberEnvironment (maskValues s v)) = 0 := ht.symm.trans (hz.mp h)
      simp [normalise, h, Expr.denote, h0, he]
    · have hn : t.denote (numberEnvironment (maskValues s v)) ≠ 0 := by
        intro h0
        exact h (hz.mpr (ht.trans h0))
      simp [normalise, h, Expr.denote, hn, hf]

/-- Every vector has an exact mask and a positive auxiliary representative. -/
def inputMask {r} (v : Nat → Nat) : Mask r := fun i => decide (v i.val ≠ 0)
def positiveValues {r} (v : Nat → Nat) : Fin r → Nat :=
  fun i => if v i.val = 0 then 1 else v i.val

theorem positiveValues_positive {r} (v : Nat → Nat) (i : Fin r) :
    0 < positiveValues v i := by
  by_cases h : v i.val = 0
  · simp [positiveValues, h]
  · simp only [positiveValues, if_neg h]
    exact Nat.pos_of_ne_zero h

theorem masked_positiveValues {r} (v : Nat → Nat) (i : Fin r) :
    maskValues (inputMask v) (positiveValues v) i = v i.val := by
  by_cases h : v i.val = 0 <;> simp [maskValues, inputMask, positiveValues, h]

theorem normalise_at_input {r} (e : Expr r) (v : Nat → Nat) :
    eval (positiveValues v) (polynomial (normalise (inputMask v) e)) = e.denote v := by
  rw [normalise_correct e _ _ (positiveValues_positive v)]
  apply Expr.denote_congr
  intro i hi
  simpa only [numberEnvironment_fin, masked_positiveValues] using
    (show numberEnvironment (maskValues (inputMask v) (positiveValues v)) (⟨i,hi⟩ : Fin r).val = v i from by
      rw [numberEnvironment_fin, masked_positiveValues])

/-- Equality of every finite-mask coefficient map is complete for the entire
    declared expression grammar, not just a collection of examples. -/
theorem denote_eq_iff_normal_polynomial_eq {r} (e f : Expr r) :
    (∀ v : Nat → Nat, e.denote v = f.denote v) ↔
      ∀ s : Mask r, polynomial (normalise s e) = polynomial (normalise s f) := by
  constructor
  · intro h s
    apply nat_polynomial_eq_of_positive_eval
    intro v hv
    rw [normalise_correct e s v hv, normalise_correct f s v hv]
    exact h _
  · intro h v
    rw [← normalise_at_input e v, ← normalise_at_input f v, h]

/-- Literal support invariant: all dead-coordinate exponents are zero. -/
def MaskSupported {r} (s : Mask r) (p : Sparse r) : Prop :=
  ∀ t ∈ p, ∀ i, s i = false → t.1 i = 0

theorem multiply_supported {r} {s : Mask r} {p q : Sparse r}
    (hp : MaskSupported s p) (hq : MaskSupported s q) : MaskSupported s (multiply p q) := by
  induction p with
  | nil => intro t ht; cases ht
  | cons a p ih =>
    intro t ht i hi
    cases List.mem_append.mp ht with
    | inl ht =>
      obtain ⟨b, hb, he⟩ := List.mem_map.mp ht
      subst t
      change a.1 i + b.1 i = 0
      rw [hp a (by simp) i hi, hq b hb i hi]
    | inr ht =>
      apply ih (fun t ht => hp t (by simp [ht])) t ht i hi

theorem normalise_supported {r} (e : Expr r) (s : Mask r) :
    MaskSupported s (normalise s e) := by
  induction e with
  | constant n =>
    intro t ht i hi
    have he : t = (fun _ => 0, n) := List.mem_singleton.mp ht
    rw [he]
  | «variable» j =>
    intro t ht i hi
    cases hj : s j with
    | false => simp [normalise, hj] at ht
    | true =>
      have he : t = (fun k => if j = k then 1 else 0, 1) := by
        simpa only [normalise, hj, Bool.true_eq, if_true, List.mem_singleton] using ht
      have hji : j ≠ i := by intro h; subst j; rw [hi] at hj; cases hj
      simp [he, hji]
  | add e f he hf =>
    intro t ht i hi
    cases List.mem_append.mp ht with
    | inl ht => exact he t ht i hi
    | inr ht => exact hf t ht i hi
  | mul e f he hf => exact multiply_supported he hf
  | ifZero t e f ht he hf =>
    simp only [normalise]
    split
    · exact he
    · exact hf

end P01AC.RestrictedIdentityV2
