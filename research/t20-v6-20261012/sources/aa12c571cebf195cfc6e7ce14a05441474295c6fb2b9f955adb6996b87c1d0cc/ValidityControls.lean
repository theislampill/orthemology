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

theorem valid_unfold (s c : Nat) : valid s c = (shape (s, c) &&
    (children (s, c)).all (fun d => if d.2 < c then valid d.1 d.2 else false)) := by
  rw [valid, evaluate]
  rfl

theorem reject_shape (s c : Nat) (h : shape (s, c) = false) : valid s c = false := by
  rw [valid_unfold, h]
  rfl

@[simp] theorem rejectTermZero : valid 0 0 = false := reject_shape 0 0 (by decide)
@[simp] theorem rejectTypeZero : valid 1 0 = false := reject_shape 1 0 (by decide)
@[simp] theorem rejectPolyZero : valid 2 0 = false := reject_shape 2 0 (by decide)
@[simp] theorem rejectTyZero : valid 3 0 = false := reject_shape 3 0 (by decide)
example : valid 4 (encode Term.i) = false := reject_shape _ _ (by decide)

-- Unknown tag, non-leaf tag, missing payload, extra payload, bad terminator.
example : valid 0 (nullary 6) = false := reject_shape _ _ (by decide)
example : valid 0 (node (node 0 0) (leaf 0)) = false := reject_shape _ _ (by decide)
example : valid 0 (unary 5 (encode Term.i)) = false := reject_shape _ _ (by decide)
example : valid 0 (unary 0 (leaf 0)) = false := reject_shape _ _ (by decide)
theorem rejectBadTerminator : valid 0 (node (leaf 0) (leaf 1)) = false :=
  reject_shape _ _ (by decide)
example : valid 2 (node (leaf 0) (node (leaf 0) (leaf 1))) = false := reject_shape _ _ (by decide)

-- Leaf-wrapping and recursive sort validation are separate checks.
example : valid 2 (unary 1 (encode Term.i)) = false := reject_shape _ _ (by decide)
theorem rejectBadCrossSort : valid 2 (unary 1 (leaf 0)) = false := by
  rw [valid_unfold]
  simp [shape, polyShape, children, polyChildren]
example : valid 2 (unary 1 (leaf (encode (TypeCode.var 0)))) = false := by
  rw [valid_unfold]
  simp [shape, polyShape, children, polyChildren]
  exact reject_shape _ _ (by decide)
theorem rejectIdentityLeftPoly :
    valid 3 (ternary 6 (encode Ty.raw) (leaf 0) (leaf (encode (Poly.var 0)))) = false := by
  rw [valid_unfold]
  simp [shape, tyShape, children, tyChildren]
theorem rejectIdentityRightPoly :
    valid 3 (ternary 6 (encode Ty.raw) (leaf (encode (Poly.var 0))) (leaf 0)) = false := by
  rw [valid_unfold]
  simp [shape, tyShape, children, tyChildren]
theorem rejectIdentityType :
    valid 3 (ternary 6 0 (leaf (encode (Poly.var 0))) (leaf (encode (Poly.var 0)))) = false := by
  rw [valid_unfold]
  simp [shape, tyShape, children, tyChildren]

-- Scoped is explicitly not sufficient as syntax validity.
example : checkScope 1 0 = true ∧ valid 2 0 = false := by
  constructor
  · rw [checkScope]; decide
  · exact rejectPolyZero

-- Different syntax sorts may share canonical codes; the validator does not invent disjoint tags.
example : encode Term.k = encode Ty.bottom := rfl
example : valid 0 (encode Ty.bottom) = true := (valid_term _).mpr ⟨Term.k, rfl⟩
example : valid 3 (encode Term.k) = true := (valid_ty _).mpr ⟨Ty.bottom, rfl⟩
example (n : Nat) : valid 2 (encode (TypeCode.var n)) = true :=
  (valid_poly _).mpr ⟨Poly.var n, rfl⟩
example (n : Nat) : valid 3 (encode (Poly.var n)) = true :=
  (valid_ty _).mpr ⟨Ty.param n, rfl⟩

theorem rejectSelfChild : evaluate (fun _ => true) (fun b => [b]) (0, 0) = false := by
  rw [evaluate]
  simp

-- Runtime evaluation supplements the universal kernel-checked image theorem.
-- Every actual core constructor: six Term, four TypeCode, three Poly, seven Ty.
#eval [valid 0 (encode Term.i), valid 0 (encode Term.k), valid 0 (encode Term.s),
  valid 0 (encode Term.zero), valid 0 (encode Term.one), valid 0 (encode (Term.app .k .i)),
  valid 1 (encode (TypeCode.var 0)), valid 1 (encode (TypeCode.arrow (.var 0) .bottom)),
  valid 1 (encode (TypeCode.all (.var 0))), valid 1 (encode TypeCode.bottom),
  valid 2 (encode (Poly.var 1)), valid 2 (encode (Poly.atom .zero)),
  valid 2 (encode (Poly.app (.var 1) (.atom .zero))),
  valid 3 (encode (Ty.param 0)), valid 3 (encode Ty.bottom), valid 3 (encode (Ty.all .raw)),
  valid 3 (encode Ty.raw), valid 3 (encode (Ty.pi .raw .bottom)),
  valid 3 (encode (Ty.sigma .raw .bottom)),
  valid 3 (encode (Ty.identity .raw (.var 0) (.atom .one)))]
#eval [valid 0 0, valid 1 0, valid 2 0, valid 3 0,
  valid 0 (node (leaf 0) (leaf 1)), valid 2 (unary 1 (leaf 0)),
  valid 3 (ternary 6 (encode Ty.raw) (leaf 0) (leaf (encode (Poly.var 0))))]

end ExactSyntaxValidity.Controls
