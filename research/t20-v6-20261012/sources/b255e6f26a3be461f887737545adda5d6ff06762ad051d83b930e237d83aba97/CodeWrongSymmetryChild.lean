import IndependentCodeControls
open AuxiliaryCodeComputability SourceFamilyComputability CodedScope ExactSyntaxValidity IndependentAuxiliaryCodeReview
set_option maxRecDepth 8192
example : AuxiliaryCodeComputability.polyChildren (Nat.pair 0 0,pack 1 [leaf 1,leaf 2,3]) = [(Nat.pair 2 1,3)] := by
  rw [poly_symm_children]
  decide
