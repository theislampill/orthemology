import FamilyComputability
open P01D Encodable SourceFamilyComputability
-- Intentionally wrong: Poly.app has tag 2, not tag 3.
example (p q : Poly) : encode (Poly.app p q) =
    node (leaf 3) (node (encode p) (node (encode q) (leaf 0))) := by
  rfl
