import MomentRecovery
import Counterexample

open scoped BigOperators

-- Reviewer controls inspect actual elaborated quantifiers and the library algebra used.
#check @FiniteMoment.recover_record
#check @FiniteMoment.record_recover
#check @FiniteMoment.weights_eq_of_moments_eq
#check @FiniteMoment.recordLinearEquiv
#check @FiniteMoment.vector_observable_reconstruction
#print axioms Matrix.det_vandermonde
#print axioms Matrix.mul_nonsing_inv
#print axioms Matrix.nonsing_inv_mul

-- Empty support has identically zero finite-sum moments and no weight coordinates.
example {K : Type*} [Field K] (a w : Fin 0 → K) (r : ℕ) :
    FiniteMoment.moment a w r = 0 := by
  simp [FiniteMoment.moment]

-- On one known point, the degree-zero record is literally its arbitrary weight.
example {K : Type*} [Field K] (a w : Fin 1 → K) :
    FiniteMoment.record a w = w := by
  funext i
  fin_cases i
  simp [FiniteMoment.record, FiniteMoment.moment, Fin.sum_univ_succ]

-- The generic recovery theorem really applies to the exact displayed four-point support.
open FiniteMomentRecovery.FourPoint in
example (w : Fin 4 → ℝ) :
    FiniteMoment.recover x (FiniteMoment.record x w) = w := by
  apply FiniteMoment.recover_record
  intro i j h
  by_contra hij
  exact support_pairwise_distinct hij h
