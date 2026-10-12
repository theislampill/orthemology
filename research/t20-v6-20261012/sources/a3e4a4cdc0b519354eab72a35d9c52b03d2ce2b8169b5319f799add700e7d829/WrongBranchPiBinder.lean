import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : branchTypeCode (encode (Ty.pi .raw (.identity .raw (.var 1) (.var 2)))) = encode (Ty.pi .raw (.identity .raw (pairPoly (.var 1) (.var 0)) (.var 2))) := by
  rw [branchTypeCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
