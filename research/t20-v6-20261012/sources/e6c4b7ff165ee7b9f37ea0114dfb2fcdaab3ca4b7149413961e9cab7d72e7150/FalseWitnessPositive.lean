import Countermodel
open FullPolynomialCountermodel
example : 0 ≤ Λ witness := by
  have h := witness_negative
  linarith
