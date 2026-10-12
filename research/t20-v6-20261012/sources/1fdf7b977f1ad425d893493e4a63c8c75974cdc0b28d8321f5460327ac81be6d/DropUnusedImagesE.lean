import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : premisesCode (encode (Rule.HasE_finite (.arrow .bottom .bottom) [] .i [.raw,.bottom,.raw] (.i .bottom))) = ([Claim.formE [] (Ty.pi .bottom .bottom)] : List Claim).map encode := by
  rw [premisesCode_exact]; apply congrArg (List.map encode); decide
end IndependentRuleMapReview
