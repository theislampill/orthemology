import RuleMapControls
open CodedRuleTemplates Encodable
example : checkSideCode (encode ctrlBadConv) = true := by
  rw [checkSideCode_exact]
  decide
