import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : ¬ membershipMatrix (programIndex mixedProgram) (Nat.pair 1 2) 1 2 := by
  rw [membershipMatrix_integer_iff,mixed_count_half]
  norm_num
