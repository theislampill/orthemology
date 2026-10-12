import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem RedCert_rule (c : Nat) : (∃ a : AuxiliaryCertificates.RedCert, encode a = c) ↔
    localShape redCertDescription c = true ∧ ∀ d ∈ localChildren redCertDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [redCertDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 2 := by simpa [redCertDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq
    · simp [redCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, redCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨AuxiliaryCertificates.RedCert.refl a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [redCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, redCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨AuxiliaryCertificates.RedCert.tail a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm

end CertificateCodeValidity
