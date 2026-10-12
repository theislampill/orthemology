import SourceSearchControls
open Encodable JointCertificates ActualSourceEnumerability ActualSourceEnumerability.Controls
example : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate swapped) = true := by
  rw [rejectDistinctSwap]
  decide
