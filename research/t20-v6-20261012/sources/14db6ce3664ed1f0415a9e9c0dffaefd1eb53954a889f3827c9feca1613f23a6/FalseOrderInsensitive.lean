import IndependentControls
open JointCertificates ActualSourceEnumerability IndependentActualSourceReview
example : serialCheckList (.cons eEmpty (.cons jEmpty .nil)) [.ctxJ [], .ctxE []] = true := by
  decide
