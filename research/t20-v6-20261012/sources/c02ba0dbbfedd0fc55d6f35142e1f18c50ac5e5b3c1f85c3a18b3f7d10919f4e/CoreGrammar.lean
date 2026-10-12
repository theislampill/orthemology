import ExactSyntaxValidity
namespace ExactSyntaxValidity
open Encodable SourceFamilyComputability CodedScope OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000

def nullary (t : Nat) : Nat := node (leaf t) (leaf 0)
def unary (t a : Nat) : Nat := node (leaf t) (node a (leaf 0))
def binary (t a b : Nat) : Nat := node (leaf t) (node a (node b (leaf 0)))
def ternary (t a b d : Nat) : Nat := node (leaf t) (node a (node b (node d (leaf 0))))
def arg3 (c : Nat) : Nat := first (rest (rest (rest c)))

@[simp] theorem tag_nullary (t : Nat) : tag (nullary t) = t := by simp [tag, nullary, leaf]
@[simp] theorem tag_unary (t a : Nat) : tag (unary t a) = t := by simp [tag, unary, leaf]
@[simp] theorem tag_binary (t a b : Nat) : tag (binary t a b) = t := by simp [tag, binary, leaf]
@[simp] theorem tag_ternary (t a b d : Nat) : tag (ternary t a b d) = t := by simp [tag, ternary, leaf]
@[simp] theorem arg1_unary (t a : Nat) : arg1 (unary t a) = a := by simp [arg1, unary]
@[simp] theorem arg1_binary (t a b : Nat) : arg1 (binary t a b) = a := by simp [arg1, binary]
@[simp] theorem arg2_binary (t a b : Nat) : arg2 (binary t a b) = b := by simp [arg2, binary]
@[simp] theorem arg1_ternary (t a b d : Nat) : arg1 (ternary t a b d) = a := by simp [arg1, ternary]
@[simp] theorem arg2_ternary (t a b d : Nat) : arg2 (ternary t a b d) = b := by simp [arg2, ternary]
@[simp] theorem arg3_ternary (t a b d : Nat) : arg3 (ternary t a b d) = d := by simp [arg3, ternary]

@[simp] theorem encode_term_i : encode Term.i = nullary 0 := rfl
@[simp] theorem encode_term_k : encode Term.k = nullary 1 := rfl
@[simp] theorem encode_term_s : encode Term.s = nullary 2 := rfl
@[simp] theorem encode_term_zero : encode Term.zero = nullary 3 := rfl
@[simp] theorem encode_term_one : encode Term.one = nullary 4 := rfl
@[simp] theorem encode_term_app (p q : Term) : encode (.app p q : Term) = binary 5 (encode p) (encode q) := rfl
@[simp] theorem encode_type_var (n : Nat) : encode (TypeCode.var n) = unary 0 (leaf n) := rfl
@[simp] theorem encode_type_arrow (a b : TypeCode) : encode (.arrow a b : TypeCode) = binary 1 (encode a) (encode b) := rfl
@[simp] theorem encode_type_all (a : TypeCode) : encode (.all a : TypeCode) = unary 2 (encode a) := rfl
@[simp] theorem encode_type_bottom : encode TypeCode.bottom = nullary 3 := rfl
@[simp] theorem encode_poly_var (n : Nat) : encode (Poly.var n) = unary 0 (leaf n) := rfl
@[simp] theorem encode_poly_atom (t : Term) : encode (Poly.atom t) = unary 1 (leaf (encode t)) := rfl
@[simp] theorem encode_poly_app (p q : Poly) : encode (.app p q : Poly) = binary 2 (encode p) (encode q) := rfl
@[simp] theorem encode_ty_param (n : Nat) : encode (Ty.param n) = unary 0 (leaf n) := rfl
@[simp] theorem encode_ty_bottom : encode Ty.bottom = nullary 1 := rfl
@[simp] theorem encode_ty_all (a : Ty) : encode (.all a : Ty) = unary 2 (encode a) := rfl
@[simp] theorem encode_ty_raw : encode Ty.raw = nullary 3 := rfl
@[simp] theorem encode_ty_pi (a b : Ty) : encode (.pi a b : Ty) = binary 4 (encode a) (encode b) := rfl
@[simp] theorem encode_ty_sigma (a b : Ty) : encode (.sigma a b : Ty) = binary 5 (encode a) (encode b) := rfl
@[simp] theorem encode_ty_identity (a : Ty) (p q : Poly) : encode (.identity a p q : Ty) = ternary 6 (encode a) (leaf (encode p)) (leaf (encode q)) := rfl

/-- These equations retain tags, all payload nodes, external-sort leaf wrappers,
    and the final zero leaf. Checking a tag alone is deliberately insufficient. -/
def termShape (c : Nat) : Bool :=
  if tag c < 5 then decide (c = nullary (tag c))
  else if tag c = 5 then decide (c = binary 5 (arg1 c) (arg2 c)) else false

def typeShape (c : Nat) : Bool :=
  if tag c = 0 then decide (c = unary 0 (leaf (rest (arg1 c))))
  else if tag c = 1 then decide (c = binary 1 (arg1 c) (arg2 c))
  else if tag c = 2 then decide (c = unary 2 (arg1 c))
  else if tag c = 3 then decide (c = nullary 3) else false

def polyShape (c : Nat) : Bool :=
  if tag c = 0 then decide (c = unary 0 (leaf (rest (arg1 c))))
  else if tag c = 1 then decide (c = unary 1 (leaf (rest (arg1 c))))
  else if tag c = 2 then decide (c = binary 2 (arg1 c) (arg2 c)) else false

def tyShape (c : Nat) : Bool :=
  if tag c = 0 then decide (c = unary 0 (leaf (rest (arg1 c))))
  else if tag c = 1 then decide (c = nullary 1)
  else if tag c = 2 then decide (c = unary 2 (arg1 c))
  else if tag c = 3 then decide (c = nullary 3)
  else if tag c = 4 then decide (c = binary 4 (arg1 c) (arg2 c))
  else if tag c = 5 then decide (c = binary 5 (arg1 c) (arg2 c))
  else if tag c = 6 then decide (c = ternary 6 (arg1 c) (leaf (rest (arg2 c))) (leaf (rest (arg3 c))))
  else false

def shape (b : Nat × Nat) : Bool :=
  if b.1 = 0 then termShape b.2
  else if b.1 = 1 then typeShape b.2
  else if b.1 = 2 then polyShape b.2
  else if b.1 = 3 then tyShape b.2 else false

def termChildren (c : Nat) : List (Nat × Nat) :=
  if tag c = 5 then [(0, arg1 c), (0, arg2 c)] else []
def typeChildren (c : Nat) : List (Nat × Nat) :=
  if tag c = 1 then [(1, arg1 c), (1, arg2 c)]
  else if tag c = 2 then [(1, arg1 c)] else []
def polyChildren (c : Nat) : List (Nat × Nat) :=
  if tag c = 1 then [(0, rest (arg1 c))]
  else if tag c = 2 then [(2, arg1 c), (2, arg2 c)] else []
def tyChildren (c : Nat) : List (Nat × Nat) :=
  if tag c = 2 then [(3, arg1 c)]
  else if tag c = 4 ∨ tag c = 5 then [(3, arg1 c), (3, arg2 c)]
  else if tag c = 6 then [(3, arg1 c), (2, rest (arg2 c)), (2, rest (arg3 c))] else []
def children (b : Nat × Nat) : List (Nat × Nat) :=
  if b.1 = 0 then termChildren b.2
  else if b.1 = 1 then typeChildren b.2
  else if b.1 = 2 then polyChildren b.2
  else if b.1 = 3 then tyChildren b.2 else []

def valid (sort code : Nat) : Bool := evaluate shape children (sort, code)

def Canonical (b : Nat × Nat) : Prop :=
  if b.1 = 0 then ∃ a : Term, encode a = b.2
  else if b.1 = 1 then ∃ a : TypeCode, encode a = b.2
  else if b.1 = 2 then ∃ a : Poly, encode a = b.2
  else if b.1 = 3 then ∃ a : Ty, encode a = b.2 else False

end ExactSyntaxValidity
