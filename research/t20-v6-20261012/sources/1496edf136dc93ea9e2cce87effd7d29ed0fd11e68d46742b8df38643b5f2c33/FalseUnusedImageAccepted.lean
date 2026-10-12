import IndependentControls
open Encodable JointCertificates ActualSourceEnumerability IndependentActualSourceReview
example : checkCanonical (encode finiteRule.conclusion)
    (encodeCertificate omitOnlyUnusedImage) = true := by
  rw [singleUnusedImageOmissionRejects]
  decide
