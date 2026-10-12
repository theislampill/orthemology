import TypeScope
namespace CodedPolyTransformations
open P01AC P01D Encodable

example : checkTyScope 0 (encode Ty.raw) = true := by rw [checkTyScope_exact]; decide
example : checkTyScope 0 (encode (Ty.identity .raw (.var 0) (.var 0))) = false := by
  rw [checkTyScope_exact]; decide
example : checkTyScope 0 (encode (Ty.pi .raw (.identity .raw (.var 0) (.var 0)))) = true := by
  rw [checkTyScope_exact]; decide
example : checkTyScope 0 (encode (Ty.sigma .raw (.identity .raw (.var 0) (.var 0)))) = true := by
  rw [checkTyScope_exact]; decide
/-- Universal type binding does not add a term variable. -/
example : checkTyScope 0 (encode (Ty.all (.identity .raw (.var 0) (.var 0)))) = false := by
  rw [checkTyScope_exact]; decide
/-- Only the dependent codomain receives the new term variable. -/
example : checkTyScope 0 (encode (Ty.pi (.identity .raw (.var 0) (.var 0)) .raw)) = false := by
  rw [checkTyScope_exact]; decide
example : checkTyScope 1 (encode (Ty.identity .raw (.var 0) (.var 1))) = false := by
  rw [checkTyScope_exact]; decide
example : checkTyScope 0 (encode (Ty.pi .raw (.pi .raw (.identity .raw (.var 1) (.var 1))))) = true := by
  rw [checkTyScope_exact]; decide

example : Computable₂ checkTyScope := primrec_checkTyScope.to_comp
end CodedPolyTransformations
