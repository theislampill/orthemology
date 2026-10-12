import GrammarImage
namespace ExactSyntaxValidity.Controls
open Encodable SourceFamilyComputability CodedScope OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

-- Universal positive controls exercise every exact source constructor through the image theorem.
example (a : Term) : valid 0 (encode a) = true := (valid_term _).mpr ⟨a, rfl⟩
example (a : TypeCode) : valid 1 (encode a) = true := (valid_typeCode _).mpr ⟨a, rfl⟩
example (a : Poly) : valid 2 (encode a) = true := (valid_poly _).mpr ⟨a, rfl⟩
example (a : Ty) : valid 3 (encode a) = true := (valid_ty _).mpr ⟨a, rfl⟩

-- Concrete evaluator controls, checked by kernel reduction rather than native_decide.
example : valid 0 (encode Term.i) = true := by decide
example : valid 0 (encode (Term.app .k .i)) = true := by decide
example : valid 1 (encode (TypeCode.arrow (.var 0) .bottom)) = true := by decide
example : valid 2 (encode (Poly.app (.var 1) (.atom .zero))) = true := by decide
example : valid 3 (encode (Ty.identity .raw (.var 0) (.atom .one))) = true := by decide

example : valid 0 0 = false := by decide
example : valid 1 0 = false := by decide
example : valid 2 0 = false := by decide
example : valid 3 0 = false := by decide
example : valid 4 (encode Term.i) = false := by decide

-- Unknown constructor tag, non-leaf tag, missing payload, extra payload and bad terminator.
example : valid 0 (nullary 6) = false := by decide
example : valid 0 (node (node 0 0) (leaf 0)) = false := by decide
example : valid 0 (unary 5 (encode Term.i)) = false := by decide
example : valid 0 (unary 0 (leaf 0)) = false := by decide
example : valid 0 (node (leaf 0) (leaf 1)) = false := by decide
example : valid 2 (node (leaf 0) (node (leaf 0) (leaf 1))) = false := by decide

-- Actual cross-sort fields must be leaf-wrapped and must contain a valid code of that sort.
example : valid 2 (unary 1 (encode Term.i)) = false := by decide
example : valid 2 (unary 1 (leaf 0)) = false := by decide
example : valid 2 (unary 1 (leaf (encode (TypeCode.var 0)))) = false := by decide
example : valid 3 (ternary 6 (encode Ty.raw) (leaf 0) (leaf (encode (Poly.var 0)))) = false := by decide
example : valid 3 (ternary 6 (encode Ty.raw) (leaf (encode (Poly.var 0))) (leaf 0)) = false := by decide
example : valid 3 (ternary 6 0 (leaf (encode (Poly.var 0))) (leaf (encode (Poly.var 0)))) = false := by decide

-- The scoping extension's known malformed acceptance cannot pass actual syntax validation.
example : checkScope 1 0 = true ∧ valid 2 0 = false := by decide

end ExactSyntaxValidity.Controls
