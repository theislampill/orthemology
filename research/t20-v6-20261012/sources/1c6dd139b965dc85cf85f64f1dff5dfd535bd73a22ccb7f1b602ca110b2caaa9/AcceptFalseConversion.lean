import SourceSearchControls
open Encodable JointCertificates ActualSourceEnumerability ActualSourceEnumerability.Controls
example : checkCanonical (encode (.hasJ [] (.atom .zero) .raw : Claim)) (encodeCertificate falseConversion) = true := by
  rw [rejectFalseConversion]
  decide
