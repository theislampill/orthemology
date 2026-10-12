import CodedScope
open P01D Encodable CodedScope
-- Intentionally false: the variable equal to the context length is out of scope.
example : checkScope 1 (encode (Poly.var 1)) = true := by rw [checkScope_exact]; decide
