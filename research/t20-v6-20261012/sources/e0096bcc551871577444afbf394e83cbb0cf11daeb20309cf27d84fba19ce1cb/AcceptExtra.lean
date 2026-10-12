import SourceSearchControls
open Encodable JointCertificates ActualSourceEnumerability ActualSourceEnumerability.Controls
example : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate extra) = true := by
  rw [rejectExtra]
  decide
