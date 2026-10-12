import Controls
import MomentValues

open MvPolynomial TruncatedMoment

-- Check theorem statements against the intended primitive domain and operations.
example (p : MvPolynomial (Fin 3) ℝ) (hdeg : p.totalDegree ≤ 2) (hne : p ≠ 0) :
    0 < TruncatedMoment.Lambda (p * p) := by
  simpa only [pow_two] using every_quadratic_square_positive p hdeg hne

example (v : Fin 3 → ℝ) : 0 ≤ MvPolynomial.eval v witness :=
  witness_nonnegative v

-- The actual witness is exactly degree four, rather than merely bounded above.
theorem independent_witness_degree_exact : witness.totalDegree = 4 := by
  apply Nat.le_antisymm witness_degree
  have hc : witness.coeff (exponent 2 2 0) ≠ 0 := by
    norm_num [witness, term, coeff_monomial, exponent_eq_iff]
  have h := le_totalDegree (mem_support_iff.mpr hc)
  simpa only [exponent_sum] using h

-- Finite atomic positive representations are already excluded by evaluation
-- positivity and the actual negative witness value, with no measure import.
theorem independent_no_finite_atomic_representation {ι : Type*} (s : Finset ι)
    (w : ι → ℝ) (v : ι → Fin 3 → ℝ) (hw : ∀ i ∈ s, 0 ≤ w i)
    (hagrees : ∀ p : Poly, p.totalDegree ≤ 4 →
      Lambda p = ∑ i ∈ s, w i * MvPolynomial.eval (v i) p) : False := by
  have hn : 0 ≤ ∑ i ∈ s, w i * MvPolynomial.eval (v i) witness :=
    Finset.sum_nonneg (fun i hi => mul_nonneg (hw i hi) (witness_nonnegative (v i)))
  rw [← hagrees witness witness_degree, Lambda_witness] at hn
  norm_num at hn

#print axioms independent_witness_degree_exact
#print axioms independent_no_finite_atomic_representation
