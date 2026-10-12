import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : premisesCode (encode (Rule.HasJ_sigmaElim [] .raw .bottom .raw (.var 0) (.atom .i))) = ((Rule.HasJ_sigmaElim [] .raw .bottom .raw (.var 0) (.atom .i)).premises.tail).map encode := by
  rw [premisesCode_exact]; apply congrArg (List.map encode); decide
end IndependentRuleMapReview
