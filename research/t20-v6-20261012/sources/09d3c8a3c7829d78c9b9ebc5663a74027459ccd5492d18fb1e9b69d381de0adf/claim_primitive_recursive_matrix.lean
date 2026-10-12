import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : Primrec (fun z : ℕ => decide (membershipMatrix z.unpair.1 z.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2)) := membershipMatrix_nat_computable
