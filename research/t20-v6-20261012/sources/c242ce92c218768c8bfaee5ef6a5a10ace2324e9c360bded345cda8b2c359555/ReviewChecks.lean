import Checks

noncomputable section
open scoped BigOperators

namespace SeparatingProjectionReview
open FiniteMoment
variable {K : Type*} [Field K]

-- Explicit edge computations, independent of the existential construction.
theorem zero_dim_projection (v x : Fin 0 → K) : projection v x = 0 := by
  simp [projection]

theorem zero_dim_polynomial (x : Fin 0 → K) : coordinatePolynomial x = 0 := by
  simp [coordinatePolynomial]

theorem empty_moment (a w : Fin 0 → K) (r : ℕ) : moment a w r = 0 := by
  simp [moment]

theorem empty_recovery (a w : Fin 0 → K) : recover a (record a w) = w := by
  funext i
  exact Fin.elim0 i

theorem singleton_zero_dim_record (v : Fin 0 → K) (x : Fin 1 → Fin 0 → K)
    (w : Fin 1 → K) : record (fun i => projection v (x i)) w 0 = w 0 := by
  simp [record, moment]

-- In dimension one the fixed first-coordinate projection already suffices.
theorem one_dim_projection_injective {N : ℕ} (x : Fin N → Fin 1 → K)
    (hx : Function.Injective x) :
    Function.Injective (fun i => projection (fun _ => 1) (x i)) := by
  intro i j h
  apply hx
  funext k
  have hk : k = 0 := Subsingleton.elim _ _
  subst k
  simpa [projection] using h

-- A duplicate support makes every projection noninjective, even over an infinite field.
theorem duplicate_vectors_no_projection {d : ℕ} (y : Fin d → K) (v : Fin d → K) :
    ¬ Function.Injective (fun _ : Fin 2 => projection v y) := by
  intro h
  have heq : (0 : Fin 2) = 1 := h rfl
  exact (by decide : (0 : Fin 2) ≠ 1) heq

-- General composition checked with the actual vector projection expression:
-- equality of the retained tuples forces equality of arbitrary weights.
theorem exists_weight_identification [Infinite K] {N d : ℕ}
    (x : Fin N → Fin d → K) (hx : Function.Injective x) :
    ∃ v : Fin d → K, ∀ w z : Fin N → K,
      (∀ r : Fin N,
        (∑ i, w i * (∑ j, v j * x i j) ^ r.val) =
        (∑ i, z i * (∑ j, v j * x i j) ^ r.val)) → w = z := by
  obtain ⟨v, hv⟩ := exists_injective_projected_record x hx
  refine ⟨v, fun w z h => hv ?_⟩
  funext r
  exact h r

-- New existence means the direction is chosen before, and works for, every weight.
#check @FiniteMoment.exists_separating_parameter
#check @FiniteMoment.exists_separating_projection
#check @FiniteMoment.exists_separating_linearMap
#check @FiniteMoment.exists_projection_recovery
#check @FiniteMoment.exists_injective_projected_record
#check @FiniteMoment.exists_projected_observable_reconstruction
#check @FiniteMoment.Checks.finite_field_counterexample
#print axioms Polynomial.zero_of_eval_zero
#print axioms Matrix.det_vandermonde
#print axioms Matrix.mul_nonsing_inv
#print axioms Matrix.nonsing_inv_mul
#print axioms Finset.prod_ne_zero_iff
#print axioms zero_dim_projection
#print axioms zero_dim_polynomial
#print axioms empty_moment
#print axioms empty_recovery
#print axioms singleton_zero_dim_record
#print axioms one_dim_projection_injective
#print axioms duplicate_vectors_no_projection
#print axioms exists_weight_identification
end SeparatingProjectionReview
