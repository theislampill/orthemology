import Counterexample
open FiniteMomentRecovery.FourPoint
-- This intentionally false control must fail to type-check.
example : moment wPlus 3 - moment wMinus 3 = (1 : ℝ) / 53 := by
  exact third_moment_difference
