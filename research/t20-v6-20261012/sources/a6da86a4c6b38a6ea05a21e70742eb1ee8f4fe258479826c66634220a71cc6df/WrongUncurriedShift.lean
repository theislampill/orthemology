import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
example : uncurriedStepCode (encode (Poly.var 0)) = encode (Poly.app (.app (.var 0) (fstPoly (.var 0))) (sndPoly (.var 0))) := by
  rw [uncurriedStepCode_exact]; apply congrArg encode; decide
end IndependentRuleMapReview
