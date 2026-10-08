import EffectiveRenewalBoundary
open EffectiveRenewal.Contract
example : (request false true (initial (false, true))).2.2 = true := by
  simp [request, initial, terminate]
