import GrammarComputability
import PolyCertificateEncoding
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def pack (t : Nat) (xs : List Nat) : Nat := node (leaf t) (xs.foldr node (leaf 0))
def a1 := arg1
def a2 := arg2
def a3 := arg3
def a4 (c : Nat) := first (rest (rest (rest (rest c))))
def a5 (c : Nat) := first (rest (rest (rest (rest (rest c)))))
def a6 (c : Nat) := first (rest (rest (rest (rest (rest (rest c))))))
def v1 (c : Nat) := rest (a1 c)
def v2 (c : Nat) := rest (a2 c)
def v3 (c : Nat) := rest (a3 c)
def v4 (c : Nat) := rest (a4 c)
def v5 (c : Nat) := rest (a5 c)
def v6 (c : Nat) := rest (a6 c)

theorem field_lt_pack (t : Nat) (xs : List Nat) {v : Nat} (h : v ∈ xs) : v < pack t xs := by
  have hf : ∀ xs : List Nat, v ∈ xs → v < xs.foldr node (leaf 0) := by
    intro xs; induction xs with
    | nil => simp
    | cons x xs ih =>
      intro h; rcases List.mem_cons.mp h with h | h
      · subst x; exact left_lt_node _ _
      · exact lt_of_lt_of_le (ih h) (right_le_node _ _)
  exact lt_of_lt_of_le (hf xs h) (right_le_node _ _)

def lhs (s : Nat × Nat) := s.1.unpair.1
def rhs (s : Nat × Nat) := s.1.unpair.2

theorem primrec_a1 : Primrec a1 := primrec_arg1
theorem primrec_a2 : Primrec a2 := primrec_arg2
theorem primrec_a3 : Primrec a3 := primrec_arg3
theorem primrec_a4 : Primrec a4 := primrec_first.comp (primrec_rest.comp (primrec_rest.comp (primrec_rest.comp primrec_rest)))
theorem primrec_a5 : Primrec a5 := primrec_a4.comp primrec_rest
theorem primrec_a6 : Primrec a6 := primrec_a5.comp primrec_rest
theorem primrec_v1 : Primrec v1 := primrec_rest.comp primrec_a1
theorem primrec_v2 : Primrec v2 := primrec_rest.comp primrec_a2
theorem primrec_v3 : Primrec v3 := primrec_rest.comp primrec_a3
theorem primrec_v4 : Primrec v4 := primrec_rest.comp primrec_a4
theorem primrec_v5 : Primrec v5 := primrec_rest.comp primrec_a5
theorem primrec_v6 : Primrec v6 := primrec_rest.comp primrec_a6
theorem primrec_lhs : Primrec lhs := Primrec.fst.comp (Primrec.unpair.comp Primrec.fst)
theorem primrec_rhs : Primrec rhs := Primrec.snd.comp (Primrec.unpair.comp Primrec.fst)

@[simp] theorem lhs_pair (a b c : Nat) : lhs (Nat.pair a b,c) = a := by simp [lhs]
@[simp] theorem rhs_pair (a b c : Nat) : rhs (Nat.pair a b,c) = b := by simp [rhs]

def tmApp := binary 5
def polyApp := binary 2
def polyAtom (t : Nat) := unary 1 (leaf t)
def tyArrow := binary 1
def tyAll := unary 2

theorem primrec_tmApp : Primrec₂ tmApp := primrec_binary 5
theorem primrec_polyApp : Primrec₂ polyApp := primrec_binary 2
theorem primrec_polyAtom : Primrec polyAtom := (primrec_unary 1).comp primrec_leaf
theorem primrec_tyArrow : Primrec₂ tyArrow := primrec_binary 1
theorem primrec_tyAll : Primrec tyAll := primrec_unary 2

@[simp] theorem tmApp_exact (a b : Term) : tmApp (encode a) (encode b) = encode (.app a b : Term) := rfl
@[simp] theorem polyApp_exact (a b : Poly) : polyApp (encode a) (encode b) = encode (.app a b : Poly) := rfl
@[simp] theorem polyAtom_exact (t : Term) : polyAtom (encode t) = encode (Poly.atom t) := rfl
@[simp] theorem tyArrow_exact (a b : TypeCode) : tyArrow (encode a) (encode b) = encode (.arrow a b : TypeCode) := rfl
@[simp] theorem tyAll_exact (a : TypeCode) : tyAll (encode a) = encode (TypeCode.all a) := rfl

end AuxiliaryCodeComputability
