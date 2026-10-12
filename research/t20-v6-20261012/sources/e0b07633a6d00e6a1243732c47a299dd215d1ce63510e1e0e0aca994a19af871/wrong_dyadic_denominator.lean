import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : rationalHeavyMass (P02A2.FiniteOutputTable.indexTable (programIndex mixedProgram)) 1 2 = (heavyCount (programIndex mixedProgram) 1 2 : ℚ≥0) / (2:ℚ≥0)^(2+1) := by
  rw [rationalHeavyMass_heavyCount,mixed_count_half]
  norm_num
