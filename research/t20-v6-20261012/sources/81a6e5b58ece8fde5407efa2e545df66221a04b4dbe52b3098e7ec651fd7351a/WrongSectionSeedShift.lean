import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates CodedPolyTransformations P01D P01AC
-- Isolate the mandatory section seed shift; the raw section equation separately proves its use.
example : shiftCode 1 (encode (Poly.var 0)) = encode (Poly.var 0) := by
  rw [shiftCode_one_exact]
  apply congrArg encode
  decide
end IndependentRuleMapReview
