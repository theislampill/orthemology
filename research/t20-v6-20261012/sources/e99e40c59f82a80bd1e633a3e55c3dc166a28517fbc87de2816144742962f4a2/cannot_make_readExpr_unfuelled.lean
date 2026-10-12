import EndpointChecks
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore
example : readExpr 1 [3,1,1,1,2] = some (.add (.constant 1) (.constant 2),[]) := by
  rw [UniformIndependentAudit.expr_insufficient_depth]
