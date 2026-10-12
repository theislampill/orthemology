import RuleMapControls
open CodedRuleTemplates Encodable
example : checkSideCode (encode ctrlBadPoly) = true := by
  rw [checkSideCode_exact]
  decide
