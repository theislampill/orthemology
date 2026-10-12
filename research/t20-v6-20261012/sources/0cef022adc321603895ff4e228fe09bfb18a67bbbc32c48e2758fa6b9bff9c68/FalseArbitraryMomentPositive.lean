import Countermodel
open FullFunctionalPolynomialBridge FullFunctionalSchur
example (μ : FullFunctionalIndexing.Exponent → ℝ) (n : ℕ) : Positive (gram μ n) := by
  exact FullFunctionalMoment.gram_positive n
