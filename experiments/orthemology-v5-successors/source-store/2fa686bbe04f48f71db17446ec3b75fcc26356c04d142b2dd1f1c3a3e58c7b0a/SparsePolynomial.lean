/- Executable finite sparse coefficient lists with a checked polynomial meaning.
   Repeated monomials and zero entries are allowed; equality aggregates coefficients. -/
import ComputablePrelude
import Mathlib.Algebra.MvPolynomial.Funext
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Fin

namespace P01AC.RestrictedIdentityV2
open MvPolynomial
open scoped BigOperators

noncomputable def exponentFinsupp {r} (a : Exponent r) : Fin r →₀ Nat :=
  Finsupp.equivFunOnFinite.symm a

@[simp] theorem exponentFinsupp_apply {r} (a : Exponent r) (i : Fin r) :
    exponentFinsupp a i = a i := rfl

theorem exponentFinsupp_injective {r} : Function.Injective (@exponentFinsupp r) := by
  intro a b h
  exact funext fun i => congrArg (fun d => d i) h

@[simp] theorem exponentFinsupp_eq_iff {r} (a b : Exponent r) :
    exponentFinsupp a = exponentFinsupp b ↔ a = b :=
  exponentFinsupp_injective.eq_iff

@[simp] theorem exponentFinsupp_coe {r} (a : Fin r →₀ Nat) :
    exponentFinsupp (fun i => a i) = a := by ext i; rfl

noncomputable def polynomial {r} : Sparse r → MvPolynomial (Fin r) Nat
  | [] => 0
  | (a,n) :: ps => monomial (exponentFinsupp a) n + polynomial ps

@[simp] theorem polynomial_coefficient {r} (p : Sparse r) (a : Exponent r) :
    coeff (exponentFinsupp a) (polynomial p) = coefficient p a := by
  induction p with
  | nil => simp [polynomial, coefficient]
  | cons t ps ih =>
    rcases t with ⟨b,n⟩
    simp [polynomial, coefficient, ih]

theorem coefficient_absent {r} (p : Sparse r) (a : Exponent r)
    (h : a ∉ p.map Prod.fst) : coefficient p a = 0 := by
  induction p with
  | nil => rfl
  | cons t ps ih =>
    rcases t with ⟨b,n⟩
    have hb : b ≠ a := by intro he; apply h; simp [he]
    have hp : a ∉ ps.map Prod.fst := by intro ha; apply h; simp [ha]
    simp [coefficient, hb, ih hp]

theorem coeffEqual_spec {r} (p q : Sparse r) :
    coeffEqual p q = true ↔ ∀ a, coefficient p a = coefficient q a := by
  simp only [coeffEqual, List.all_eq_true, decide_eq_true_eq]
  constructor
  · intro h a
    by_cases ha : a ∈ p.map Prod.fst ++ q.map Prod.fst
    · exact h a ha
    · have hp : a ∉ p.map Prod.fst := fun hp => ha (List.mem_append_left _ hp)
      have hq : a ∉ q.map Prod.fst := fun hq => ha (List.mem_append_right _ hq)
      rw [coefficient_absent p a hp, coefficient_absent q a hq]
  · intro h a _
    exact h a

theorem coeffEqual_iff_polynomial {r} (p q : Sparse r) :
    coeffEqual p q = true ↔ polynomial p = polynomial q := by
  rw [coeffEqual_spec]
  constructor
  · intro h
    apply MvPolynomial.ext
    intro a
    have ht := h (fun i => a i)
    rw [← polynomial_coefficient, ← polynomial_coefficient] at ht
    simpa only [exponentFinsupp_coe] using ht
  · intro h a
    rw [← polynomial_coefficient, ← polynomial_coefficient, h]

def scaleTerm {r} (a : Exponent r × Nat) (p : Sparse r) : Sparse r :=
  p.map (fun b => (fun i => a.1 i + b.1 i, a.2 * b.2))

def multiply {r} : Sparse r → Sparse r → Sparse r
  | [], _ => []
  | a :: p, q => scaleTerm a q ++ multiply p q

@[simp] theorem exponentFinsupp_add {r} (a b : Exponent r) :
    exponentFinsupp (fun i => a i + b i) = exponentFinsupp a + exponentFinsupp b := by
  ext i; rfl

@[simp] theorem polynomial_append {r} (p q : Sparse r) :
    polynomial (p ++ q) = polynomial p + polynomial q := by
  induction p with
  | nil => simp [polynomial]
  | cons t p ih =>
    rcases t with ⟨a,n⟩
    simp [polynomial, ih, add_assoc]

theorem polynomial_scaleTerm {r} (a : Exponent r × Nat) (p : Sparse r) :
    polynomial (scaleTerm a p) = monomial (exponentFinsupp a.1) a.2 * polynomial p := by
  rcases a with ⟨a,n⟩
  induction p with
  | nil => simp [scaleTerm, polynomial]
  | cons t p ih =>
    rcases t with ⟨b,m⟩
    simp only [scaleTerm] at ih
    simp [scaleTerm, polynomial, ← monomial_mul, mul_add, ih]

@[simp] theorem polynomial_multiply {r} (p q : Sparse r) :
    polynomial (multiply p q) = polynomial p * polynomial q := by
  induction p with
  | nil => simp [multiply, polynomial]
  | cons t p ih =>
    rcases t with ⟨a,n⟩
    simp [multiply, polynomial_append, polynomial_scaleTerm, ih, polynomial, add_mul]

/-- No cancellation: a monomial's variable product is positive on the positive orthant. -/
theorem exponent_product_positive {r} (a : Exponent r) (v : Fin r → Nat)
    (hv : ∀ i, 0 < v i) :
    0 < (exponentFinsupp a).prod (fun i k => v i ^ k) := by
  apply Finset.prod_pos
  intro i _
  exact pow_pos (hv i) _

/-- Every zero test in the executable normalizer has the exact semantic meaning. -/
theorem zeroTest_iff_eval_zero {r} (p : Sparse r) (v : Fin r → Nat)
    (hv : ∀ i, 0 < v i) :
    zeroTest p = true ↔ eval v (polynomial p) = 0 := by
  induction p with
  | nil => simp [zeroTest, polynomial]
  | cons t p ih =>
    rcases t with ⟨a,n⟩
    have hp := Nat.ne_of_gt (exponent_product_positive a v hv)
    simp only [zeroTest, List.all_cons, Bool.and_eq_true, decide_eq_true_eq,
      polynomial, eval_add, eval_monomial, Nat.add_eq_zero_iff, Nat.mul_eq_zero,
      hp, or_false]
    exact and_congr Iff.rfl ih

theorem zeroTest_iff_polynomial_zero {r} (p : Sparse r) :
    zeroTest p = true ↔ polynomial p = 0 := by
  constructor
  · intro hz
    induction p with
    | nil => rfl
    | cons t p ih =>
      rcases t with ⟨a,n⟩
      have h := (List.all_eq_true.mp hz) (a,n) (by simp)
      have hn : n = 0 := of_decide_eq_true h
      have ht : zeroTest p = true := by
        simpa only [zeroTest, List.all_cons, Bool.and_eq_true, decide_eq_true_eq, hn, true_and] using hz
      simp [polynomial, hn, ih ht]
  · intro hp
    apply (zeroTest_iff_eval_zero p (fun _ => 1) (fun _ => Nat.zero_lt_one)).mpr
    rw [hp, map_zero]

end P01AC.RestrictedIdentityV2
