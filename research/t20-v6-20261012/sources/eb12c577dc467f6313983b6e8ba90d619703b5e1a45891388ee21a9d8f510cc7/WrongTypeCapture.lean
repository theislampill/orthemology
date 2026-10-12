import TermTypeSubstitution
open P01D P01AC Encodable CodedPolyTransformations
-- Intentionally false: entering pi must shift the substituent for outer variable one.
example : inst (Ty.pi .raw (.identity .raw (.var 1) (.var 0))) (Poly.var 4) =
    Ty.pi .raw (.identity .raw (.var 4) (.var 0)) := by
  rfl
