import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : checkSideCode (encode (Rule.HasJ_var [.raw] .raw 1 (.zero [] .raw))) = true := by
  rw [checkSideCode_exact]; decide
end IndependentRuleMapReview
