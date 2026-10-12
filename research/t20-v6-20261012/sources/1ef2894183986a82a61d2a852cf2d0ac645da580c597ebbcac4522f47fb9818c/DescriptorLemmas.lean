import ConstructorDescriptors
namespace CertificateCodeValidity
open SourceFamilyComputability CodedScope AuxiliaryCodeComputability
@[simp] theorem tag_node_leaf (t p : Nat) : tag (node (leaf t) p) = t := by
  simp [tag, leaf]
@[simp] theorem slot_0 (c : Nat) : slot c 0 = first (rest (c)) := rfl
@[simp] theorem slot_1 (c : Nat) : slot c 1 = first (rest (rest (c))) := rfl
@[simp] theorem slot_2 (c : Nat) : slot c 2 = first (rest (rest (rest (c)))) := rfl
@[simp] theorem slot_3 (c : Nat) : slot c 3 = first (rest (rest (rest (rest (c))))) := rfl
@[simp] theorem slot_4 (c : Nat) : slot c 4 = first (rest (rest (rest (rest (rest (c)))))) := rfl
@[simp] theorem slot_5 (c : Nat) : slot c 5 = first (rest (rest (rest (rest (rest (rest (c))))))) := rfl
@[simp] theorem slot_6 (c : Nat) : slot c 6 = first (rest (rest (rest (rest (rest (rest (rest (c)))))))) := rfl
@[simp] theorem slot_7 (c : Nat) : slot c 7 = first (rest (rest (rest (rest (rest (rest (rest (rest (c))))))))) := rfl
@[simp] theorem rest_pack (t : Nat) (xs : List Nat) : rest (pack t xs) = xs.foldr node (leaf 0) := by
  simp [pack]
end CertificateCodeValidity
