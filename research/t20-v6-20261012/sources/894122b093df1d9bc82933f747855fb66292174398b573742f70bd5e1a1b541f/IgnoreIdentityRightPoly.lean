import ValidityControls
open ExactSyntaxValidity SourceFamilyComputability Encodable OrthemologyV2 P01D P01AC
example : valid 3 (ternary 6 (encode Ty.raw) (leaf (encode (Poly.var 0))) (leaf 0)) = true := by
  rw [Controls.rejectIdentityRightPoly]
  decide
