import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : branchAtCode (encode (Poly.var 2)) (encode (Poly.atom .i)) (encode (Poly.atom .k)) = encode (Poly.var 2) := by
  rw [branchAtCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
