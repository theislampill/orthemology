import Countermodel
example : FullPolynomialCountermodel.Λ FullPolynomialCountermodel.witness = 0 := by
  rw [FullPolynomialCountermodel.witness_negative]
  norm_num
