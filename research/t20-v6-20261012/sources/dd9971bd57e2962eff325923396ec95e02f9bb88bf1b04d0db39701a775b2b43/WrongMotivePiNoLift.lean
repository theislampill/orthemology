import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : motiveAtCode (encode (Ty.pi .raw (.identity .raw (.var 1) (.var 2)))) (encode (Poly.var 3)) (encode (Poly.var 4)) = encode (Ty.pi .raw (.identity .raw (.var 4) (.var 3))) := by
  rw [motiveAtCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
