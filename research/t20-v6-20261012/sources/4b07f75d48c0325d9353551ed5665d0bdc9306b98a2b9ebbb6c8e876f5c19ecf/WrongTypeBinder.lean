import TypeScope
open P01AC P01D Encodable CodedPolyTransformations
-- Intentionally false: all does not add a term variable.
example : checkTyScope 0 (encode (Ty.all (.identity .raw (.var 0) (.var 0)))) = true := by
  rw [checkTyScope_exact]; decide
