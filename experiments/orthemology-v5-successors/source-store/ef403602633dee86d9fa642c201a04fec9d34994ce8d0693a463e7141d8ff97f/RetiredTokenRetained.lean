import EffectiveRenewalBoundary
open EffectiveRenewal.Contract
example : operativeSupport (migrate (initial (false, true)) true) (.instanceToken 0) := by
  simp [operativeSupport, migrate, initial]
