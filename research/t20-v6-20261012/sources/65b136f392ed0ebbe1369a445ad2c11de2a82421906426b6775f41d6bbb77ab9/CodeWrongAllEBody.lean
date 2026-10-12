import IndependentCodeControls
open AuxiliaryCodeComputability SourceFamilyComputability CodedScope ExactSyntaxValidity IndependentAuxiliaryCodeReview
set_option maxRecDepth 8192
example : AuxiliaryCodeComputability.finiteChildren (Nat.pair 0 0,pack 5 [leaf 1,leaf 2,leaf 3,4]) = [(Nat.pair 1 2,4)] := by
  rw [finite_allE_children]
  decide
