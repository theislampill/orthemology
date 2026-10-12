import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : sectionPolyCode (encode (Poly.var 0)) (encode (Poly.var 1)) = encode (abstract (RigidityInitiality.sectionBody (.var 0) (pren Nat.succ (.var 1)) (.var 0))) := by
  rw [sectionPolyCode_exact]; apply congrArg encode; decide +kernel
end IndependentRuleMapReview
