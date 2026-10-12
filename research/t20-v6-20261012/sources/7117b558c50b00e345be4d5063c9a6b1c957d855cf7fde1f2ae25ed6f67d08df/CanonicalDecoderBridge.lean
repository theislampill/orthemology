import GrammarImage
import GrammarComputability
namespace ExactSyntaxValidity
open Encodable SourceFamilyComputability CodedScope OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

/-- Total code normalizer for the canonical image of the unchanged codec. -/
def normalize (s c : Nat) : Option Nat := if valid s c then some c else none

theorem primrec_normalize : Primrec₂ normalize := by
  apply ((Primrec.cond primrec_valid (Primrec.option_some.comp Primrec.snd)
    (Primrec.const none)).to₂).of_eq
  intro s c
  unfold normalize
  cases valid s c <;> rfl

/-- This theorem concerns Encodable.decode₂, the canonicality-checking decoder.
    It deliberately does not assume arbitrary Encodable decoders are canonical. -/
theorem normalize_decode₂ {α : Type} [Encodable α] {s : Nat}
    (hexact : ∀ c, valid s c = true ↔ ∃ a : α, encode a = c) (c : Nat) :
    normalize s c = (decode₂ α c).map encode := by
  cases hd : decode₂ α c with
  | none =>
    have hv : valid s c = false := Bool.eq_false_iff.mpr (by
      intro hv
      obtain ⟨a, ha⟩ := (hexact c).mp hv
      have he := decode₂_eq_some.mpr ha
      rw [hd] at he
      contradiction)
    simp [normalize, hv, hd]
  | some a =>
    have he := decode₂_eq_some.mp hd
    have hv := (hexact c).mpr ⟨a, he⟩
    simp [normalize, hv, hd, he]

theorem normalize_term (c : Nat) : normalize 0 c = (decode₂ Term c).map encode :=
  normalize_decode₂ valid_term c
theorem normalize_typeCode (c : Nat) : normalize 1 c = (decode₂ TypeCode c).map encode :=
  normalize_decode₂ valid_typeCode c
theorem normalize_poly (c : Nat) : normalize 2 c = (decode₂ Poly c).map encode :=
  normalize_decode₂ valid_poly c
theorem normalize_ty (c : Nat) : normalize 3 c = (decode₂ Ty c).map encode :=
  normalize_decode₂ valid_ty c

theorem primrec_decode₂_reencode {α : Type} [Encodable α] {s : Nat}
    (hexact : ∀ c, valid s c = true ↔ ∃ a : α, encode a = c) :
    Primrec (fun c => encode (decode₂ α c)) := by
  have h : Primrec (fun c => encode (normalize s c)) :=
    Primrec.encode.comp (primrec_normalize.comp (Primrec.const s) Primrec.id)
  apply h.of_eq
  intro c
  rw [normalize_decode₂ hexact]
  cases decode₂ α c <;> rfl

theorem primrec_term_decode₂_reencode : Primrec (fun c => encode (decode₂ Term c)) :=
  primrec_decode₂_reencode valid_term
theorem primrec_typeCode_decode₂_reencode : Primrec (fun c => encode (decode₂ TypeCode c)) :=
  primrec_decode₂_reencode valid_typeCode
theorem primrec_poly_decode₂_reencode : Primrec (fun c => encode (decode₂ Poly c)) :=
  primrec_decode₂_reencode valid_poly
theorem primrec_ty_decode₂_reencode : Primrec (fun c => encode (decode₂ Ty c)) :=
  primrec_decode₂_reencode valid_ty

end ExactSyntaxValidity
