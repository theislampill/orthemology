import SourceSearchControls
open Encodable JointCertificates ActualSourceEnumerability ActualSourceEnumerability.Controls
example : checkCanonical (encode (Claim.ctxJ [.raw])) (encodeCertificate missing) = true := by
  rw [rejectMissing]
  decide
