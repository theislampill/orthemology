import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : checkSideCode (AuxiliaryCodeComputability.pack 1 [SourceFamilyComputability.leaf 99]) = false := by
  rw [malformed_side_accepted]; decide
end IndependentRuleMapReview
