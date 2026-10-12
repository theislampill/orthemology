import EndpointChecks
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore
example : decodeBytes (magic ++ [2,0,17,0,999]) = some ⟨2,0,.skip⟩ := by
  rw [UniformIndependentAudit.decode_trailing_rejected]
