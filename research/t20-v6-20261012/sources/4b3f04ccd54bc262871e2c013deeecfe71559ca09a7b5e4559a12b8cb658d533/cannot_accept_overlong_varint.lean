import EndpointChecks
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore
example : uvRead [128,0] = some (0,[]) := by
  rw [UniformIndependentAudit.reject_overlong_zero]
