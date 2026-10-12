import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : thetaCode (encode ([Ty.bottom] : Tel)) (encode Ty.raw) (encode (Poly.var 0)) = encode ([Ty.raw, .identity .raw (.var 1) (.var 0), .bottom] : Tel) := by
  rw [thetaCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
