import SourceSearchControls
open Encodable JointCertificates ActualSourceEnumerability ActualSourceEnumerability.Controls
example : checkCanonical (encode fullSupport.conclusion) (encodeCertificate droppedUnusedImage) = true := by
  rw [rejectDroppedUnusedImage]
  decide
