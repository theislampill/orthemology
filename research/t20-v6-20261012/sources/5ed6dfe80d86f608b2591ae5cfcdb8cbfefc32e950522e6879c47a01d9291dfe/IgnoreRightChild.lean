import CodedScope
open P01D Encodable CodedScope
-- Intentionally false: both application children must be scoped.
example : checkScope 1 (encode (Poly.app (.var 0) (.var 1))) = true := by
  rw [checkScope_exact]; decide
