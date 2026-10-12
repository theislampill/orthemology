import IndependentCodeControls
open AuxiliaryCodeComputability SourceFamilyComputability CodedScope ExactSyntaxValidity IndependentAuxiliaryCodeReview
set_option maxRecDepth 8192
example : AuxiliaryCodeComputability.polyChildren (Nat.pair 0 0,pack 2 [leaf 1,leaf 2,leaf 3,4,5]) = [(Nat.pair 1 3,4),(Nat.pair 1 3,5)] := by
  rw [poly_trans_children]
  decide
