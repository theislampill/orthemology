import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : motiveAtCode (encode (Ty.identity .raw (.var 0) (.var 1))) (encode (Poly.atom .i)) (encode (Poly.atom .k)) = encode (Ty.identity .raw (.atom .i) (.atom .k)) := by
  rw [motiveAtCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
