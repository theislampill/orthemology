import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : premisesCode (encode (Rule.HasJ_natInduction [] .raw (.atom .i) (.atom .k))) = ((Rule.HasJ_natInduction [] .raw (.atom .i) (.atom .k)).premises.tail).map encode := by
  rw [premisesCode_exact]; apply congrArg (List.map encode); decide
end IndependentRuleMapReview
