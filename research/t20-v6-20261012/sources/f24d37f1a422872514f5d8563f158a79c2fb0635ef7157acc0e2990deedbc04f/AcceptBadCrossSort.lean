import ValidityControls
open ExactSyntaxValidity SourceFamilyComputability
example : valid 2 (unary 1 (leaf 0)) = true := by
  rw [Controls.rejectBadCrossSort]
  decide
