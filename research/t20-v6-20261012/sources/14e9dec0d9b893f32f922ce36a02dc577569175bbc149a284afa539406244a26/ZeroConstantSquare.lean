import Countermodel
example : FullPolynomialCountermodel.Λ ((1 : FullFunctionalPolynomialBridge.Polynomial)^2) = 0 := by
  norm_num [FullPolynomialCountermodel.normalized]
