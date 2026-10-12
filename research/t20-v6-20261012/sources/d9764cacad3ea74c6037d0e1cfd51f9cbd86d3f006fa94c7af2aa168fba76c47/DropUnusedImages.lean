import RuleMapControls
open CodedRuleTemplates Encodable
example : (premisesCode (encode ctrlFinite)).length = 1 := by
  rw [unused_image_retained]
  decide
