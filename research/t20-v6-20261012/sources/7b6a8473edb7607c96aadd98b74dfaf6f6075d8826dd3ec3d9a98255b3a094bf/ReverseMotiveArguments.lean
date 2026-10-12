import RuleMapControls
open CodedRuleTemplates Encodable P01D P01AC
example : motiveAtCode (encode (Ty.identity .raw (.var 0) (.var 1)))
    (encode (Poly.atom .k)) (encode ctrlAtom) =
    encode (Ty.identity .raw (.atom .k) ctrlAtom) := by
  rw [motiveAtCode_exact]
  decide
