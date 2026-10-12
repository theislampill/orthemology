import CodedScope
namespace CodedScope
open P01D P01AC Encodable SourceFamilyComputability

example : checkScope 0 (encode (Poly.var 0)) = false := by rw [checkScope_exact]; decide
example : checkScope 1 (encode (Poly.var 0)) = true := by rw [checkScope_exact]; decide
example : checkScope 1 (encode (Poly.var 1)) = false := by rw [checkScope_exact]; decide
example : checkScope 0 (encode (Poly.atom (.app .i .zero))) = true := by rw [checkScope_exact]; decide
example : checkScope 1 (encode (Poly.app (.var 0) (.atom .i))) = true := by
  rw [checkScope_exact]; decide
example : checkScope 1 (encode (Poly.app (.var 0) (.var 1))) = false := by
  rw [checkScope_exact]; decide
example : checkScope 2 (encode (Poly.app (.var 0) (.var 1))) = true := by
  rw [checkScope_exact]; decide

/-- This totalized scoping evaluator is intentionally not a syntax validator. -/
example : checkScope 1 0 = true := by rw [checkScope]; rfl

theorem no_poly_encodes_zero : ¬ ∃ p : Poly, encode p = 0 := by
  rintro ⟨p, hp⟩
  have hpos : 0 < encode p := by
    cases p with
    | var n => rw [encode_var]; exact lt_of_le_of_lt (Nat.zero_le _) (left_lt_node _ _)
    | atom t => rw [encode_atom]; exact lt_of_le_of_lt (Nat.zero_le _) (left_lt_node _ _)
    | app p q => rw [encode_app]; exact lt_of_le_of_lt (Nat.zero_le _) (left_lt_appCode _ _)
  omega

example : Computable₂ checkScope := computable_checkScope
#print axioms no_poly_encodes_zero
end CodedScope
