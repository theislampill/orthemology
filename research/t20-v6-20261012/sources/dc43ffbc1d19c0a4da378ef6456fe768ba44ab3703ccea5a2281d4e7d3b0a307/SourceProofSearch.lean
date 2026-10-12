import CanonicalCertificateCode
import CertificateImage
import Mathlib.Computability.Halting
namespace ActualSourceEnumerability
open Encodable JointCertificates CertificateCodeValidity CodedRuleTemplates
set_option maxRecDepth 16384
set_option maxHeartbeats 4000000

/-- Derivability in the actual six source judgment families, on canonical claim codes. -/
def DerivableCode (q : Nat) : Prop := ∃ j : Claim, encode j = q ∧ j.denote

theorem checkCanonical_exact (c : SerialCert) (j : Claim) :
    checkCanonical (encode j) (encode c) = check (fromSerial c) j := by
  have hj : certValid 11 (encode j) = true := (valid_Claim _).mpr ⟨j, rfl⟩
  have hc : certValid 13 (encode c) = true := (valid_SerialCert _).mpr ⟨c, rfl⟩
  simp only [checkCanonical, hj, hc, Bool.true_and, runNode_exact, serialCheck_exact]

theorem checkCanonical_encode (c : DerivationCertificate) (j : Claim) :
    checkCanonical (encode j) (encodeCertificate c) = check c j := by
  simpa only [encodeCertificate, fromSerial_toSerial] using checkCanonical_exact (toSerial c) j

theorem checkCanonical_sound {q c : Nat} (h : checkCanonical q c = true) : DerivableCode q := by
  have hg := h
  simp only [checkCanonical, Bool.and_eq_true] at hg
  obtain ⟨j, rfl⟩ := (valid_Claim q).mp hg.1.1
  obtain ⟨cert, rfl⟩ := (valid_SerialCert c).mp hg.1.2
  exact ⟨j, rfl, check_sound (checkCanonical_exact cert j ▸ h)⟩

theorem derivableCode_iff_certificate (q : Nat) :
    DerivableCode q ↔ ∃ c : Nat, checkCanonical q c = true := by
  constructor
  · rintro ⟨j, rfl, hj⟩
    obtain ⟨c, hc⟩ := complete hj
    exact ⟨encodeCertificate c, by simpa only [checkCanonical_encode] using hc⟩
  · rintro ⟨c, hc⟩
    exact checkCanonical_sound hc

theorem derivableCode_encode (j : Claim) : DerivableCode (encode j) ↔ j.denote := by
  constructor
  · rintro ⟨k, hk, h⟩
    exact Encodable.encode_injective hk ▸ h
  · intro h; exact ⟨j, rfl, h⟩

theorem computable_checkCanonical : Computable₂ checkCanonical := primrec_checkCanonical.to_comp

/-- Mathematical unbounded search for the least accepted natural certificate code.
    This is a partial recursive search, with no efficiency or totality claim. -/
def proofSearch (q : Nat) : Part Nat := Nat.rfind (fun c => checkCanonical q c)

theorem proofSearch_partrec : Partrec proofSearch :=
  Partrec.rfind computable_checkCanonical.partrec.to₂

theorem proofSearch_nat_partrec : Nat.Partrec proofSearch := Partrec.nat_iff.mp proofSearch_partrec

theorem proofSearch_dom (q : Nat) : (proofSearch q).Dom ↔ DerivableCode q := by
  simpa only [proofSearch, Nat.rfind_dom, Part.coe_some, Part.mem_some_iff,
    Part.some_dom, implies_true, and_true, eq_comm] using
    (derivableCode_iff_certificate q).symm

theorem proofSearch_mem (q c : Nat) : c ∈ proofSearch q ↔
    checkCanonical q c = true ∧ ∀ earlier, earlier < c → checkCanonical q earlier = false := by
  simp [proofSearch, Nat.mem_rfind]

theorem proofSearch_undefined (q : Nat) : ¬ (proofSearch q).Dom ↔ ¬ DerivableCode q :=
  not_congr (proofSearch_dom q)

theorem derivableCode_re : REPred DerivableCode :=
  proofSearch_partrec.dom_re.of_eq proofSearch_dom

/-- These are source derivability equivalences for supplied terms, not existential
    type inhabitation; the latter requires its separate code projection. -/
theorem proofSearch_ctxJ (Γ : P01AC.Tel) :
    (proofSearch (encode (Claim.ctxJ Γ))).Dom ↔ JointCompletion.CtxJ Γ := by
  rw [proofSearch_dom, derivableCode_encode]; rfl

theorem proofSearch_formJ (Γ : P01AC.Tel) (A : P01AC.Ty) :
    (proofSearch (encode (Claim.formJ Γ A))).Dom ↔ JointCompletion.FormJ Γ A := by
  rw [proofSearch_dom, derivableCode_encode]; rfl

theorem proofSearch_hasJ (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) :
    (proofSearch (encode (Claim.hasJ Γ p A))).Dom ↔ JointCompletion.HasJ Γ p A := by
  rw [proofSearch_dom, derivableCode_encode]; rfl

theorem proofSearch_ctxE (Γ : P01AC.Tel) :
    (proofSearch (encode (Claim.ctxE Γ))).Dom ↔ P01AC.ExtensionalRepair.CtxE Γ := by
  rw [proofSearch_dom, derivableCode_encode]; rfl

theorem proofSearch_formE (Γ : P01AC.Tel) (A : P01AC.Ty) :
    (proofSearch (encode (Claim.formE Γ A))).Dom ↔ P01AC.ExtensionalRepair.FormE Γ A := by
  rw [proofSearch_dom, derivableCode_encode]; rfl

theorem proofSearch_hasE (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) :
    (proofSearch (encode (Claim.hasE Γ p A))).Dom ↔ P01AC.ExtensionalRepair.HasE Γ p A := by
  rw [proofSearch_dom, derivableCode_encode]; rfl

#print axioms checkCanonical_exact
#print axioms checkCanonical_sound
#print axioms derivableCode_iff_certificate
#print axioms computable_checkCanonical
#print axioms proofSearch_partrec
#print axioms proofSearch_dom
#print axioms proofSearch_mem
#print axioms derivableCode_re
#print axioms proofSearch_ctxJ
#print axioms proofSearch_formJ
#print axioms proofSearch_hasJ
#print axioms proofSearch_ctxE
#print axioms proofSearch_formE
#print axioms proofSearch_hasE
end ActualSourceEnumerability
