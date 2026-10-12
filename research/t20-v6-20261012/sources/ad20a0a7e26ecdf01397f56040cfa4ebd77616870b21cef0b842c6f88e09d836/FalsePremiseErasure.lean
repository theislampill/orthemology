import Countermodel
open FullPolynomialCountermodel
example (p : MvPolynomial (Fin 2) ℝ) : 0 < Λ (p^2) := by
  exact strict_square_positive p
