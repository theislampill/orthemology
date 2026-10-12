import Indexing
import Recurrence
import Mathlib.Algebra.MvPolynomial.Basic
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-! The genuine finite-support bridge from the recursive Gram matrices to
strict positivity on squares in the complete bivariate polynomial algebra. -/
namespace FullFunctionalPolynomialBridge
open FullFunctionalIndexing FullFunctionalRecurrence FullFunctionalSchur
open MvPolynomial Matrix

abbrev Polynomial := MvPolynomial (Fin 2) ℝ
abbrev MultiExponent := Fin 2 →₀ ℕ

def decode (d : MultiExponent) : Exponent := (d 0, d 1)
noncomputable def encode (e : Exponent) : MultiExponent :=
  Finsupp.single 0 e.1 + Finsupp.single 1 e.2

@[simp] theorem decode_encode (e : Exponent) : decode (encode e) = e := by
  rcases e with ⟨a,b⟩
  simp [decode, encode]

@[simp] theorem encode_decode (d : MultiExponent) : encode (decode d) = d := by
  ext i
  have hi : i = 0 ∨ i = 1 := by
    have h := i.isLt
    omega
  rcases hi with rfl | rfl <;> simp [encode, decode]

@[simp] theorem decode_add (d e : MultiExponent) : decode (d + e) = decode d + decode e := by
  rfl

theorem encode_injective : Function.Injective encode := by
  intro e f h
  have he := congrArg decode h
  simpa using he

/-- Evaluation of a polynomial against any full moment sequence. -/
noncomputable def functional (μ : Exponent → ℝ) : Polynomial →ₗ[ℝ] ℝ :=
  Finsupp.linearCombination ℝ (fun d : MultiExponent => μ (decode d))

@[simp] theorem functional_monomial (μ : Exponent → ℝ) (d : MultiExponent) (r : ℝ) :
    functional μ (monomial d r) = r * μ (decode d) := by
  exact Finsupp.linearCombination_single ℝ r d

@[simp] theorem functional_encoded_monomial (μ : Exponent → ℝ) (e : Exponent) (r : ℝ) :
    functional μ (monomial (encode e) r) = r * μ e := by simp

@[simp] theorem functional_one (μ : Exponent → ℝ) :
    functional μ 1 = μ (0,0) := by
  rw [MvPolynomial.one_def, functional_monomial]
  exact one_mul _

@[simp] theorem functional_X_pow_mul_X_pow (μ : Exponent → ℝ) (a b : ℕ) :
    functional μ ((X (0 : Fin 2)) ^ a * (X (1 : Fin 2)) ^ b) = μ (a,b) := by
  simp [X_pow_eq_monomial, monomial_mul, decode]

noncomputable def exponent (n : ℕ) (i : Index n) : MultiExponent :=
  encode (exponentAt (position i))

theorem exponent_injective (n : ℕ) : Function.Injective (exponent n) := by
  intro i j h
  apply position_injective n
  apply exponentAt_injective
  exact encode_injective h

/-- Every finite polynomial support fits into one of the recursively extended
index sets. This is the only bound chosen, and depends on the given polynomial. -/
theorem support_fits (p : Polynomial) :
    ∃ n, ∀ d ∈ p.support, ∃ i : Index n, exponent n i = d := by
  classical
  let n := p.support.sup (fun d => index (decode d))
  refine ⟨n, ?_⟩
  intro d hd
  have hb : index (decode d) ≤ n := Finset.le_sup (f := fun d => index (decode d)) hd
  obtain ⟨i,hi⟩ := position_surjective n (index (decode d) - 1) (by omega)
  refine ⟨i, ?_⟩
  simp [exponent, hi]

/-- Coefficients outside the original support are included as zeros. -/
theorem expand_of_support_fits (p : Polynomial) (n : ℕ)
    (h : ∀ d ∈ p.support, ∃ i : Index n, exponent n i = d) :
    p = ∑ i : Index n, monomial (exponent n i) (coeff (exponent n i) p) := by
  classical
  ext d
  rw [coeff_sum]
  by_cases hd : ∃ i : Index n, exponent n i = d
  · obtain ⟨i,rfl⟩ := hd
    symm
    rw [Finset.sum_eq_single i]
    · simp
    · intro j hj hji
      rw [coeff_monomial]
      simp [show exponent n j ≠ exponent n i from fun he => hji (exponent_injective n he)]
    · simp
  · have hz : coeff d p = 0 := by
      by_contra hz
      exact hd (h d (by simpa only [mem_support_iff] using hz))
    rw [hz]
    symm
    apply Finset.sum_eq_zero
    intro i hi
    rw [coeff_monomial]
    simp [show exponent n i ≠ d from fun he => hd ⟨i, he⟩]

/-- All polynomials, without a global degree cutoff, have finite Gram coordinates. -/
theorem finite_expansion (p : Polynomial) :
    ∃ n, ∃ u : Index n → ℝ, p = ∑ i : Index n, monomial (exponent n i) (u i) := by
  obtain ⟨n,hn⟩ := support_fits p
  exact ⟨n, (fun i => coeff (exponent n i) p), expand_of_support_fits p n hn⟩

noncomputable def gram (μ : Exponent → ℝ) (n : ℕ) : Matrix (Index n) (Index n) ℝ :=
  fun i j => μ (exponentAt (position i) + exponentAt (position j))

/-- The moment functional of a square equals its finite Gram quadratic form. -/
theorem functional_square_expansion (μ : Exponent → ℝ) (n : ℕ) (u : Index n → ℝ) :
    functional μ ((∑ i : Index n, monomial (exponent n i) (u i)) ^ 2) =
      u ⬝ᵥ gram μ n *ᵥ u := by
  classical
  rw [pow_two, Finset.sum_mul]
  simp only [Finset.mul_sum, map_sum, monomial_mul, functional_monomial,
    decode_add, exponent, decode_encode]
  simp only [dotProduct, mulVec, gram, Finset.mul_sum]
  congr 1
  funext i
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- The bridge's sole positivity hypothesis is discharged by the actual moment
recursion. It concerns every finite recursive Gram matrix, not the polynomial. -/
theorem square_strict_positive (μ : Exponent → ℝ)
    (hgram : ∀ n, Positive (gram μ n)) (p : Polynomial) (hp : p ≠ 0) :
    0 < functional μ (p ^ 2) := by
  obtain ⟨n,u,hu⟩ := finite_expansion p
  have hne : u ≠ 0 := by
    intro hz
    apply hp
    rw [hu, hz]
    simp
  rw [hu, functional_square_expansion]
  exact hgram n u hne

#print axioms finite_expansion
#print axioms functional_square_expansion
#print axioms square_strict_positive
end FullFunctionalPolynomialBridge
