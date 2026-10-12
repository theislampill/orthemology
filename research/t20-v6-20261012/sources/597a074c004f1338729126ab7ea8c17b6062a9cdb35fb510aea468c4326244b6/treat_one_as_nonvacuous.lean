import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : ¬ membershipMatrix (programIndex echoProgram) (Nat.pair 1 1) 1 2 := by
  simp [membershipMatrix_integer_iff]
