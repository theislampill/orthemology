import ValidityControls
open ExactSyntaxValidity
example : evaluate (fun _ => true) (fun b => [b]) (0, 0) = true := by
  rw [Controls.rejectSelfChild]
  decide
