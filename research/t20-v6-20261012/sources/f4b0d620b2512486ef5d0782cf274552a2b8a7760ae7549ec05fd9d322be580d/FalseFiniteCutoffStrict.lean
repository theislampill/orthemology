import PositiveChecks
open MvPolynomial FullFunctionalPolynomialBridge
example (N : ℕ) : 0 < functional (cutoffMoment N)
    ((monomial (encode (N+1,0)) (1 : ℝ)) ^ 2) := by
  rw [any_finite_cutoff_kills_high_square]
  norm_num
