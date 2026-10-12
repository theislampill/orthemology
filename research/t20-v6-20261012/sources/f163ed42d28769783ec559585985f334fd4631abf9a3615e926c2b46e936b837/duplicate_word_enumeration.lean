import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : (allWords 2).length = 5 := by
  rw [allWords_length]
  norm_num
