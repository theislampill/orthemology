import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : checkSideCode (encode (Rule.HasE_identityIntro [] .raw (.atom .i) (.atom .k) (.refl (.atom .i)))) = true := by
  rw [checkSideCode_exact]; decide
end IndependentRuleMapReview
