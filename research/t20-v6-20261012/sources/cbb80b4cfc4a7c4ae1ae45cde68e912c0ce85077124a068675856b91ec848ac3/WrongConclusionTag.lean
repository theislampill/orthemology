import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : conclusionCode (encode (Rule.FormE_raw [])) = encode (Claim.formJ [] .raw) := by
  rw [conclusionCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
