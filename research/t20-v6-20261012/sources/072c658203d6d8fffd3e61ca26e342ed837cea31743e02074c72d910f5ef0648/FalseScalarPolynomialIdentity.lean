import Countermodel
open FullPolynomialCountermodel FullPolynomialMomentSupport
example : Λ witness = F 0 0 := by
  rw [witness_negative]
  norm_num [F]
