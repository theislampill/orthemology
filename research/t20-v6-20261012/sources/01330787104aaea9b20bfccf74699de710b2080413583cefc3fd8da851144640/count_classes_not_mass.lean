import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : heavyCount (programIndex mixedProgram) 1 2 = 1 := by
  rw [mixed_count_half]
