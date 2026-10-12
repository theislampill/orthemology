import EndpointChecks
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore
example : Primrec (fun code : ℕ => evaluateIndex code.unpair.1 code.unpair.2.unpair.1 code.unpair.2.unpair.2) := evaluateIndex_nat_computable
