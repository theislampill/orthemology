import IndependentCodeControls
open AuxiliaryCodeComputability SourceFamilyComputability CodedScope ExactSyntaxValidity IndependentAuxiliaryCodeReview
set_option maxRecDepth 8192
example : AuxiliaryCodeComputability.stepChildren (Nat.pair 0 0,pack 4 [leaf 1,leaf 2,leaf 3,4]) = [(Nat.pair 1 2,4)] := by
  rw [step_right_children]
  decide
