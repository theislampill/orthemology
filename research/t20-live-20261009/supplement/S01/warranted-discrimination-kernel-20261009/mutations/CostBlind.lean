import Controls
open CertificateFrontier CertificateFrontier.Controls
-- FALSE mutation: discard the larger support without comparing its price.
example : cost priced {false, true} = cost costBlind {false, true} := by
  decide
