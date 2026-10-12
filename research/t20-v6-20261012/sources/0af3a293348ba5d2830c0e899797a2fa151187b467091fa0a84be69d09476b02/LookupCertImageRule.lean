import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem LookupCert_rule (c : Nat) : (∃ a : AuxiliaryCertificates.LookupCert, encode a = c) ↔
    localShape lookupCertDescription c = true ∧ ∀ d ∈ localChildren lookupCertDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [lookupCertDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 2 := by simpa [lookupCertDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq
    · simp [lookupCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, lookupCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨AuxiliaryCertificates.LookupCert.zero a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [lookupCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, lookupCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨AuxiliaryCertificates.LookupCert.succ a0 (rest (slot c 1)) a2 a3 a4, ?_⟩
      simpa [h0, h2, h3, h4] using hs.symm

end CertificateCodeValidity
