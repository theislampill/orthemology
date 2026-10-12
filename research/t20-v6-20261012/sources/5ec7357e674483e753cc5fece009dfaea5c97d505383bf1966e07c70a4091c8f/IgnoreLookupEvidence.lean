import RuleMapControls
open CodedRuleTemplates Encodable
example : checkSideCode (encode ctrlBadLookup) = true := by
  rw [checkSideCode_exact]
  decide
