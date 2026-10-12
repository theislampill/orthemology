import TelescopeCodeValidity
namespace TelescopeCodeValidity
open Encodable ExactSyntaxValidity OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

/-- Canonical decoder normalization, without a `Primcodable Ty` premise. -/
def normalizeTel (c : Nat) : Option Nat := if validTel c then some c else none

theorem primrec_normalizeTel : Primrec normalizeTel := by
  apply (Primrec.cond primrec_validTel (Primrec.option_some.comp Primrec.id)
    (Primrec.const none)).of_eq
  intro c
  unfold normalizeTel
  cases validTel c <;> rfl

theorem normalizeTel_decode₂ (c : Nat) :
    normalizeTel c = (decode₂ Tel c).map encode := by
  cases hd : decode₂ Tel c with
  | none =>
    have hv : validTel c = false := Bool.eq_false_iff.mpr (by
      intro hv
      obtain ⟨xs, hx⟩ := (validTel_exact c).mp hv
      have he := decode₂_eq_some.mpr hx
      rw [hd] at he
      contradiction)
    simp [normalizeTel, hv, hd]
  | some xs =>
    have he := decode₂_eq_some.mp hd
    have hv := (validTel_exact c).mpr ⟨xs, he⟩
    simp [normalizeTel, hv, hd, he]

theorem primrec_tel_decode₂_reencode : Primrec (fun c => encode (decode₂ Tel c)) := by
  apply (Primrec.encode.comp primrec_normalizeTel).of_eq
  intro c
  rw [normalizeTel_decode₂]
  cases decode₂ Tel c <;> rfl

end TelescopeCodeValidity
