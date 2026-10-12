import TelescopeCodeValidity
namespace TelescopeCodeValidity
open Encodable ExactSyntaxValidity OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

/-- Encoding the telescope's list of natural head codes preserves the entire
    unchanged list code; this is not a flattening of the telescope encoding. -/
theorem encode_map_encode_tel (Γ : Tel) :
    encode (Γ.map (fun A : Ty => encode A)) = encode Γ := by
  induction Γ with
  | nil => rfl
  | cons A Γ ih => simp only [List.map_cons, encode_list_cons, encode_nat, ih]

/-- The ordinary, standard decoder for `List Nat`, defaulting to nil. -/
def telNatDecode (c : Nat) : List Nat := (decode (α := List Nat) c).getD []

theorem primrec_telNatDecode : Primrec telNatDecode := by
  exact Primrec.option_getD.comp Primrec.decode (Primrec.const [])

/-- Genuine telescope codes decode to precisely their list of encoded heads. -/
theorem telNatDecode_encode (Γ : Tel) :
    telNatDecode (encode Γ) = Γ.map (fun A : Ty => encode A) := by
  rw [← encode_map_encode_tel Γ]
  simp [telNatDecode]

end TelescopeCodeValidity
