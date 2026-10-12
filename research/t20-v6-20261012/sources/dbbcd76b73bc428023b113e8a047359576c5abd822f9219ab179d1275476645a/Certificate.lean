import DegreeBridge
import ScalarPositivity

noncomputable section
namespace TruncatedMoment
open MvPolynomial

theorem eval_term (a b c : ℕ) (r : ℝ) (v : Fin 3 → ℝ) :
    eval v (term a b c r) = r * v 0 ^ a * v 1 ^ b * v 2 ^ c := by
  simp [term, exponent, eval_monomial, Finsupp.prod_add_index, pow_add,
    Finsupp.prod_single_index]
  ring

theorem eval_witness (v : Fin 3 → ℝ) :
    eval v witness = choiLam (v 0) (v 1) (v 2) := by
  simp [witness, eval_term, choiLam]
  ring

theorem witness_nonnegative (v : Fin 3 → ℝ) : 0 ≤ eval v witness := by
  rw [eval_witness]
  exact choiLam_nonneg _ _ _

theorem quadratic_square_positive (c a b d u v w r s t : ℝ)
    (h : quadratic c a b d u v w r s t ≠ 0) :
    0 < Lambda (quadratic c a b d u v w r s t ^ 2) := by
  rw [Lambda_quadratic_square]
  change 0 < momentForm c a b d u v w r s t
  have hn := momentForm_nonneg c a b d u v w r s t
  have hz : momentForm c a b d u v w r s t ≠ 0 := by
    intro heq
    rcases (momentForm_eq_zero_iff c a b d u v w r s t).mp heq with
      ⟨rfl,rfl,rfl,rfl,rfl,rfl,rfl,rfl,rfl,rfl⟩
    exact h (by simp [quadratic, term])
  exact lt_of_le_of_ne hn (Ne.symm hz)

/-- Strict positivity quantifies over every actual nonzero polynomial of degree at most two. -/
theorem every_quadratic_square_positive (p : Poly) (hd : p.totalDegree ≤ 2) (hp : p ≠ 0) :
    0 < Lambda (p ^ 2) := by
  have heq := quadratic_parameterization p hd
  rw [heq] at hp ⊢
  exact quadratic_square_positive _ _ _ _ _ _ _ _ _ _ hp

theorem term_totalDegree_le (a b c : ℕ) (r : ℝ) :
    (term a b c r).totalDegree ≤ a+b+c := by
  have h := totalDegree_monomial_le (exponent a b c) r
  simpa only [term, Function.id_def, exponent_sum] using h

theorem add_totalDegree_le {p q : Poly} {n : ℕ}
    (hp : p.totalDegree ≤ n) (hq : q.totalDegree ≤ n) : (p+q).totalDegree ≤ n :=
  le_trans (totalDegree_add _ _) (max_le hp hq)

theorem witness_degree : witness.totalDegree ≤ 4 := by
  unfold witness
  apply add_totalDegree_le
  · apply add_totalDegree_le
    · apply add_totalDegree_le
      · apply add_totalDegree_le
        · exact le_trans (term_totalDegree_le _ _ _ _) (by norm_num)
        · exact le_trans (term_totalDegree_le _ _ _ _) (by norm_num)
      · exact le_trans (term_totalDegree_le _ _ _ _) (by norm_num)
    · exact le_trans (term_totalDegree_le _ _ _ _) (by norm_num)
  · exact le_trans (term_totalDegree_le _ _ _ _) (by norm_num)

/-- This is the necessary positivity property of any positive-measure moment functional. -/
def PositiveOnNonnegativeQuartics (L : Poly →ₗ[ℝ] ℝ) : Prop :=
  ∀ p : Poly, p.totalDegree ≤ 4 → (∀ v : Fin 3 → ℝ, 0 ≤ eval v p) → 0 ≤ L p

/-- The actual coefficient functional violates positivity on nonnegative quartics. -/
theorem not_positive_on_nonnegative_quartics : ¬ PositiveOnNonnegativeQuartics Lambda := by
  intro h
  have hn := h witness witness_degree witness_nonnegative
  rw [Lambda_witness] at hn
  norm_num at hn

/-- No functional positive on nonnegative quartics agrees with these truncated moments. -/
theorem no_positive_functional_agrees (L : Poly →ₗ[ℝ] ℝ)
    (hL : PositiveOnNonnegativeQuartics L)
    (hagrees : ∀ p : Poly, p.totalDegree ≤ 4 → L p = Lambda p) : False := by
  have hn := hL witness witness_degree witness_nonnegative
  rw [hagrees witness witness_degree, Lambda_witness] at hn
  norm_num at hn

/-- A bundled, degree-scoped separation certificate with actual polynomial semantics. -/
theorem truncated_moment_obstruction :
    (∀ p : Poly, p.totalDegree ≤ 2 → p ≠ 0 → 0 < Lambda (p^2)) ∧
    witness.totalDegree ≤ 4 ∧
    (∀ v : Fin 3 → ℝ, 0 ≤ eval v witness) ∧
    Lambda witness = -2 ∧
    ¬ PositiveOnNonnegativeQuartics Lambda := by
  exact ⟨every_quadratic_square_positive, witness_degree, witness_nonnegative,
    Lambda_witness, not_positive_on_nonnegative_quartics⟩

end TruncatedMoment

#print axioms TruncatedMoment.Lambda_quadratic_square
#print axioms TruncatedMoment.quadratic_parameterization
#print axioms TruncatedMoment.every_quadratic_square_positive
#print axioms TruncatedMoment.witness_nonnegative
#print axioms TruncatedMoment.no_positive_functional_agrees
#print axioms TruncatedMoment.truncated_moment_obstruction
