import Controls
open CertificateFrontier CertificateFrontier.Controls
-- FALSE mutation: equal all-future costs under the collapsed-infinity semantics
-- still imply equal normalized frontiers.
example : frontier ({(∅, ⊤)} : Finset (Pair Bool (WithTop Nat))) = frontier ∅ := by
  decide
