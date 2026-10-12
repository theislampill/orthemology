import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : checkSideCode (encode (Rule.HasJ_finite (.arrow (.var 0) (.var 0)) [] .i [] (.i (.var 0)))) = true := by
  rw [checkSideCode_exact]; decide
end IndependentRuleMapReview
