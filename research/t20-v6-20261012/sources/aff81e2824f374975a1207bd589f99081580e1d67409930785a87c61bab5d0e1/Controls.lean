import Certificate

noncomputable section
namespace TruncatedMoment
open MvPolynomial

/-- The chosen zero-coefficient continuation outside the truncated domain is not square-positive. -/
def cubicControl : Poly := term 3 0 0 1 + term 1 0 0 (-1)

theorem cubic_control_value : Lambda (cubicControl ^ 2) = -96 := by
  simp only [cubicControl, pow_two, add_mul, mul_add, term_mul, map_add]
  norm_num [Lambda, term, coeff_monomial, exponent_eq_iff]

theorem not_full_square_positive : ¬ (∀ p : Poly, 0 ≤ Lambda (p^2)) := by
  intro h
  have hn := h cubicControl
  rw [cubic_control_value] at hn
  norm_num at hn

theorem quadratic_square_degree (p : Poly) (hd : p.totalDegree ≤ 2) :
    (p^2).totalDegree ≤ 4 := by
  exact le_trans (totalDegree_pow p 2) (by omega)

/-- Strict positivity of finite sums of quadratic squares, when at least one term is nonzero. -/
theorem finite_sos_positive {ι : Type*} (s : Finset ι) (q : ι → Poly)
    (hd : ∀ i ∈ s, (q i).totalDegree ≤ 2) (hne : ∃ i ∈ s, q i ≠ 0) :
    0 < Lambda (∑ i ∈ s, q i ^ 2) := by
  rw [map_sum]
  refine Finset.sum_pos' ?_ ?_
  · intro i hi
    by_cases hq : q i = 0
    · simp [hq]
    · exact le_of_lt (every_quadratic_square_positive (q i) (hd i hi) hq)
  · obtain ⟨i,hi,hq⟩ := hne
    exact ⟨i,hi,every_quadratic_square_positive (q i) (hd i hi) hq⟩

end TruncatedMoment

#print axioms TruncatedMoment.cubic_control_value
#print axioms TruncatedMoment.not_full_square_positive
#print axioms TruncatedMoment.finite_sos_positive
