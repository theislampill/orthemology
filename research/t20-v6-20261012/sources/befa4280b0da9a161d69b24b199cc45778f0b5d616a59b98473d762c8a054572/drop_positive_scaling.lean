import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example (e a d c k N : ℕ) : membershipMatrix e (Nat.pair (c*a) (c*d)) k N ↔ membershipMatrix e (Nat.pair a d) k N := by
  exact redundant_fraction e a d c k N
