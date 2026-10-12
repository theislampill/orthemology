import IndependentCodeControls
open AuxiliaryCodeComputability SourceFamilyComputability CodedScope ExactSyntaxValidity IndependentAuxiliaryCodeReview
set_option maxRecDepth 8192
example : AuxiliaryCodeComputability.lookupChildren (Nat.pair 0 (Nat.pair 0 0),pack 1 [leaf 1,leaf 2,leaf 3,leaf 4,5]) = [(Nat.pair 1 (Nat.pair 2 4),5)] := by
  rw [lookup_succ_children]
  decide
