import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem SerialCert_rule (c : Nat) : (∃ a : JointCertificates.SerialCert, encode a = c) ↔
    localShape serialCertDescription c = true ∧ ∀ d ∈ localChildren serialCertDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a; simp [serialCertDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 1 := by simpa [serialCertDescription] using htag
    have heq : tag c = 0 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq
    · simp [serialCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, serialCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.SerialCert.node a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm

end CertificateCodeValidity
