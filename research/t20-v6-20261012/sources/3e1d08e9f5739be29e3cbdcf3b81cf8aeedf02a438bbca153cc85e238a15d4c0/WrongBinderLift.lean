import FinitePolySubstitution
open P01D CodedPolyTransformations
-- Intentionally false: the old substitution image must shift under a binder.
example : pup (finiteEnv [Poly.var 4] 0) 1 = Poly.var 4 := by
  rfl
