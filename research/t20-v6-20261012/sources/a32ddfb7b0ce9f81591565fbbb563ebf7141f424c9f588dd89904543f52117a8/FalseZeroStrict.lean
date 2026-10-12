import Countermodel
open FullPolynomialCountermodel
example : 0 < Λ ((0 : MvPolynomial (Fin 2) ℝ)^2) := by
  norm_num
