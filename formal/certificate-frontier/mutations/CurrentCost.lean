import Controls
open CertificateFrontier CertificateFrontier.Controls
-- FALSE mutation: equal current cost is a congruence for future acquisitions.
example : futureCost jointProof {false} {true} = futureCost jointProof {true} {true} := by
  decide
