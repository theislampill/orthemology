import StepCertBounds
import RedCertBounds
import FiniteCertBounds
import PolyCertBounds
import LookupCertBounds
import ClaimBounds
import RuleBounds
import SerialCertBounds
import SerialCertListBounds
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem certCanonical_sort_lt (s c : Nat) (h : CertCanonical (s,c)) : s < 15 := by
  by_contra hs
  have h0 : s ≠ 0 := by omega
  have h1 : s ≠ 1 := by omega
  have h2 : s ≠ 2 := by omega
  have h3 : s ≠ 3 := by omega
  have h4 : s ≠ 4 := by omega
  have h5 : s ≠ 5 := by omega
  have h6 : s ≠ 6 := by omega
  have h7 : s ≠ 7 := by omega
  have h8 : s ≠ 8 := by omega
  have h9 : s ≠ 9 := by omega
  have h10 : s ≠ 10 := by omega
  have h11 : s ≠ 11 := by omega
  have h12 : s ≠ 12 := by omega
  have h13 : s ≠ 13 := by omega
  have h14 : s ≠ 14 := by omega
  simp [CertCanonical, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14] at h

theorem cert_canonical_rule (b : Nat × Nat) :
    CertCanonical b ↔ certShape b = true ∧ ∀ d ∈ certChildren b, CertCanonical d := by
  obtain ⟨s,c⟩ := b
  by_cases hs : s < 15
  · have hcases : s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨ s = 4 ∨ s = 5 ∨ s = 6 ∨ s = 7 ∨ s = 8 ∨ s = 9 ∨ s = 10 ∨ s = 11 ∨ s = 12 ∨ s = 13 ∨ s = 14 := by omega
    rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · simpa [CertCanonical, certShape, certChildren] using (valid_term c).symm
    · simpa [CertCanonical, certShape, certChildren] using (valid_typeCode c).symm
    · simpa [CertCanonical, certShape, certChildren] using (valid_poly c).symm
    · simpa [CertCanonical, certShape, certChildren] using (valid_ty c).symm
    · simp [CertCanonical, certShape, certChildren]
    · simpa [CertCanonical, certShape, certChildren] using (validTel_exact c).symm
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using StepCert_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using RedCert_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using FiniteCert_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using PolyCert_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using LookupCert_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using Claim_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using Rule_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using SerialCert_rule c
    · simpa [CertCanonical, certShape, certChildren, allDescriptions] using SerialCertList_rule c
  · have hd : allDescriptions[s-6]? = none := by
      apply List.getElem?_eq_none
      simp only [allDescriptions, List.length_cons, List.length_nil]
      omega
    have hp : ¬ CertCanonical (s,c) := by
      intro hp
      exact hs (certCanonical_sort_lt s c hp)
    have h4 : ¬s < 4 := by omega
    have he4 : s ≠ 4 := by omega
    have he5 : s ≠ 5 := by omega
    simp [hp, certShape, h4, he4, he5, hd, localShape]

theorem cert_canonical_bounds (b : Nat × Nat) (hb : CertCanonical b) :
    ∀ d ∈ certChildren b, d.2 < b.2 := by
  obtain ⟨s,c⟩ := b
  have hs : s < 15 := certCanonical_sort_lt s c hb
  have hcases : s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨ s = 4 ∨ s = 5 ∨ s = 6 ∨ s = 7 ∨ s = 8 ∨ s = 9 ∨ s = 10 ∨ s = 11 ∨ s = 12 ∨ s = 13 ∨ s = 14 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · simp [certChildren]
  · simp [certChildren]
  · simp [certChildren]
  · simp [certChildren]
  · simp [certChildren]
  · simp [certChildren]
  · have ha : ∃ a : AuxiliaryCertificates.StepCert, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using StepCert_bounds c ha
  · have ha : ∃ a : AuxiliaryCertificates.RedCert, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using RedCert_bounds c ha
  · have ha : ∃ a : AuxiliaryCertificates.FiniteCert, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using FiniteCert_bounds c ha
  · have ha : ∃ a : AuxiliaryCertificates.PolyCert, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using PolyCert_bounds c ha
  · have ha : ∃ a : AuxiliaryCertificates.LookupCert, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using LookupCert_bounds c ha
  · have ha : ∃ a : JointCertificates.Claim, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using Claim_bounds c ha
  · have ha : ∃ a : JointCertificates.Rule, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using Rule_bounds c ha
  · have ha : ∃ a : JointCertificates.SerialCert, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using SerialCert_bounds c ha
  · have ha : ∃ a : JointCertificates.SerialCertList, encode a = c := by simpa [CertCanonical] using hb
    simpa [certChildren, allDescriptions] using SerialCertList_bounds c ha

theorem certValid_exact (s c : Nat) : certValid s c = true ↔ CertCanonical (s,c) :=
  evaluate_exact_of_image cert_canonical_rule cert_canonical_bounds (s,c)

theorem valid_term (c : Nat) : certValid 0 c = true ↔ ∃ a : OrthemologyV2.Term, encode a = c := by
  simpa [CertCanonical] using certValid_exact 0 c

theorem valid_typeCode (c : Nat) : certValid 1 c = true ↔ ∃ a : OrthemologyV2.TypeCode, encode a = c := by
  simpa [CertCanonical] using certValid_exact 1 c

theorem valid_poly (c : Nat) : certValid 2 c = true ↔ ∃ a : P01D.Poly, encode a = c := by
  simpa [CertCanonical] using certValid_exact 2 c

theorem valid_ty (c : Nat) : certValid 3 c = true ↔ ∃ a : P01AC.Ty, encode a = c := by
  simpa [CertCanonical] using certValid_exact 3 c

theorem valid_nat (c : Nat) : certValid 4 c = true ↔ ∃ a : Nat, encode a = c := by
  simpa [CertCanonical] using certValid_exact 4 c

theorem valid_tel (c : Nat) : certValid 5 c = true ↔ ∃ a : P01AC.Tel, encode a = c := by
  simpa [CertCanonical] using certValid_exact 5 c

theorem valid_StepCert (c : Nat) : certValid 6 c = true ↔ ∃ a : AuxiliaryCertificates.StepCert, encode a = c := by
  simpa [CertCanonical] using certValid_exact 6 c

theorem valid_RedCert (c : Nat) : certValid 7 c = true ↔ ∃ a : AuxiliaryCertificates.RedCert, encode a = c := by
  simpa [CertCanonical] using certValid_exact 7 c

theorem valid_FiniteCert (c : Nat) : certValid 8 c = true ↔ ∃ a : AuxiliaryCertificates.FiniteCert, encode a = c := by
  simpa [CertCanonical] using certValid_exact 8 c

theorem valid_PolyCert (c : Nat) : certValid 9 c = true ↔ ∃ a : AuxiliaryCertificates.PolyCert, encode a = c := by
  simpa [CertCanonical] using certValid_exact 9 c

theorem valid_LookupCert (c : Nat) : certValid 10 c = true ↔ ∃ a : AuxiliaryCertificates.LookupCert, encode a = c := by
  simpa [CertCanonical] using certValid_exact 10 c

theorem valid_Claim (c : Nat) : certValid 11 c = true ↔ ∃ a : JointCertificates.Claim, encode a = c := by
  simpa [CertCanonical] using certValid_exact 11 c

theorem valid_Rule (c : Nat) : certValid 12 c = true ↔ ∃ a : JointCertificates.Rule, encode a = c := by
  simpa [CertCanonical] using certValid_exact 12 c

theorem valid_SerialCert (c : Nat) : certValid 13 c = true ↔ ∃ a : JointCertificates.SerialCert, encode a = c := by
  simpa [CertCanonical] using certValid_exact 13 c

theorem valid_SerialCertList (c : Nat) : certValid 14 c = true ↔ ∃ a : JointCertificates.SerialCertList, encode a = c := by
  simpa [CertCanonical] using certValid_exact 14 c

end CertificateCodeValidity
