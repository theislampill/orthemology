import RuleMapControls
open CodedRuleTemplates Encodable
example : checkSideCode (encode ctrlAllExt) = true := by
  rw [checkSideCode_exact]
  decide
