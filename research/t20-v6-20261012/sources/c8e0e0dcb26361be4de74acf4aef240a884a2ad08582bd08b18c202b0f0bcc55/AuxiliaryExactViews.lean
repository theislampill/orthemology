import AuxiliaryCodeCore
namespace AuxiliaryCodeComputability
open SourceFamilyComputability
@[simp] theorem unpair_leaf (n : Nat) : Nat.unpair (leaf n) = (0,n) := Nat.unpair_pair _ _
end AuxiliaryCodeComputability
