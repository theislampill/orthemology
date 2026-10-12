import TelescopeNatTransport
namespace TelescopeCodeValidity
open Encodable
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

/-- The existing list/natural codecs commute with encoding every head.
    This algebraic identity needs no `Primcodable` premise on the head type. -/
theorem encode_map_encode {α : Type*} [Encodable α] (xs : List α) :
    encode (xs.map (fun a : α => encode a)) = encode xs := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simp only [List.map_cons, encode_list_cons, encode_nat, ih]

/-- Generic code transport through the standard natural-list decoder. -/
theorem telNatDecode_encode_list {α : Type*} [Encodable α] (xs : List α) :
    telNatDecode (encode xs) = xs.map (fun a : α => encode a) := by
  rw [← encode_map_encode xs]
  simp [telNatDecode]

abbrev listNatDecode : Nat → List Nat := telNatDecode

theorem primrec_listNatDecode : Primrec listNatDecode := primrec_telNatDecode

theorem listNatDecode_encode {α : Type*} [Encodable α] (xs : List α) :
    listNatDecode (encode xs) = xs.map (fun a : α => encode a) :=
  telNatDecode_encode_list xs

end TelescopeCodeValidity
