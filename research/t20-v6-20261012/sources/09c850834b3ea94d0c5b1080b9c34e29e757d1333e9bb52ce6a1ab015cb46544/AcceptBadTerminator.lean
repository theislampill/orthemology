import ValidityControls
open ExactSyntaxValidity SourceFamilyComputability
example : valid 0 (node (leaf 0) (leaf 1)) = true := by
  rw [Controls.rejectBadTerminator]
  decide
