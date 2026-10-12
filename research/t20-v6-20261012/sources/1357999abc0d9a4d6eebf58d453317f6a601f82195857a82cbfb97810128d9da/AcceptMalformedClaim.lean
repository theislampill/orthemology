import SourceSearchControls
open Encodable JointCertificates ActualSourceEnumerability ActualSourceEnumerability.Controls
example : checkCanonical 0 (encodeCertificate empty) = true := by
  rw [malformedClaimRejectsEveryCertificate]
  decide
